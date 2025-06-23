from PIL import Image, ImageDraw
import qrcode
import sys
import os
import re
from datetime import datetime
import platform
import subprocess

# --- INGRESO DE URL DESDE CONSOLA ---
if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    URL = input("🔗 Ingresa la URL para el QR: ").strip()

# Validación básica de URL
if not URL or not URL.startswith(("http://", "https://")):
    print("❌ URL no válida. Debe comenzar con http:// o https://")
    sys.exit(1)

# Ruta del logo
LOGO_PATH = "logo.png"
if not os.path.exists(LOGO_PATH):
    print(f"❌ No se encontró el archivo del logo: {LOGO_PATH}")
    sys.exit(1)

# Generar nombre de archivo limpio y automático
safe_name = re.sub(r'\W+', '_', URL.replace("https://", "").replace("http://", ""))
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Crear carpeta si no existe
OUTPUT_FOLDER = "img_generadas"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Ruta completa dentro de la carpeta
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, f"qr_{safe_name}_{timestamp}.png")

# --- FUNCIONES AUXILIARES ---
def make_square(image, fill_color=(255, 255, 255, 0)):
    x, y = image.size
    size = max(x, y)
    new_img = Image.new("RGBA", (size, size), fill_color)
    new_img.paste(image, ((size - x) // 2, (size - y) // 2))
    return new_img

def generate_dot_qr(data, logo_size_px=250, padding_ratio=1.2):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    gray = img.convert("L")
    dot_qr = Image.new("RGB", img.size, "white")
    draw = ImageDraw.Draw(dot_qr)
    pixel_size = 20

    # Definir área del logo para evitar dibujar puntos en esa zona
    center = (gray.width // 2, gray.height // 2)
    radius = int((logo_size_px * padding_ratio) / 2)

    for y in range(0, gray.height, pixel_size):
        for x in range(0, gray.width, pixel_size):
            # Saltar si el píxel está en la zona reservada para el logo
            if ((center[0] - radius) < x < (center[0] + radius)) and ((center[1] - radius) < y < (center[1] + radius)):
                continue

            box = gray.crop((x, y, x + pixel_size, y + pixel_size))
            if box.getextrema()[0] < 128:
                draw.ellipse((x, y, x + pixel_size, y + pixel_size), fill="black")

    return dot_qr

def add_center_logo(qr_img, logo_img, padding_ratio=1.2):
    qr_copy = qr_img.copy()
    draw = ImageDraw.Draw(qr_copy)

    logo_size = logo_img.width
    center = (qr_copy.width // 2, qr_copy.height // 2)
    radius = int((logo_size * padding_ratio) / 2)

    # Dibuja un fondo blanco circular para el logo
    draw.ellipse(
        [
            (center[0] - radius, center[1] - radius),
            (center[0] + radius, center[1] + radius)
        ],
        fill="white"
    )
    pos = (center[0] - logo_img.width // 2, center[1] - logo_img.height // 2)
    qr_copy.paste(logo_img, pos, mask=logo_img)
    return qr_copy

# --- PROCESO PRINCIPAL ---
print("⚙️ Generando QR...")

# Preparar logo
logo = Image.open(LOGO_PATH).convert("RGBA")
logo_square = make_square(logo)
logo_size = 250
logo_resized = logo_square.resize((logo_size, logo_size), Image.LANCZOS)

# Generar QR y aplicar logo
qr_dot = generate_dot_qr(URL, logo_size_px=logo_size)
qr_final = add_center_logo(qr_dot, logo_resized)
qr_final.save(OUTPUT_PATH)

print(f"✅ QR generado: {OUTPUT_PATH}")

# Abrir imagen automáticamente en Mac
if platform.system() == "Darwin":
    subprocess.run(["open", OUTPUT_PATH])
