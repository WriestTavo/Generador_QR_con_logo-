# Generador de Código QR Estilo Dot con Logo Central

Este script en Python genera un código QR estilizado con puntos circulares, integrando un logo en el centro. Además, el sistema asegura que el logo no interfiera con la legibilidad del QR al reservar un espacio libre en su área central.

---

## 🧩 Características

- Entrada por consola o parámetro de URL
- Validación básica de URLs
- Logo central redondeado, con relleno blanco de fondo
- Diseño de puntos (dot-style) en vez de bloques
- Evita dibujar puntos debajo del logo
- Salida con nombre automático dentro de una carpeta `img_generadas`
- Compatible con macOS para apertura automática del archivo generado

---

## 🖼️ Requisitos

- Python 3.x
- Librerías:

```bash
pip install pillow qrcode
```

---

## 🚀 Cómo usar

### 1. Prepara tu entorno
Coloca una imagen llamada `logo.png` en la misma carpeta donde se encuentra el script. Esta será utilizada como el logo central del QR.

> ✅ Se recomienda que el logo tenga fondo transparente y buena resolución (mínimo 250x250 px).

---

### 2. Ejecuta el script

#### Opción A: Desde la terminal con parámetro
```bash
python Generador_QR_con_logo.py https://tusitio.com
```

#### Opción B: Sin parámetros (te pedirá la URL)
```bash
python Generador_QR_con_logo.py
🔗 Ingresa la URL para el QR: https://tusitio.com
```

---

## 📂 Salida

- Los archivos PNG generados se guardan automáticamente en la carpeta `img_generadas/`.
- El nombre del archivo se genera a partir del dominio + la fecha/hora.

Ejemplo de nombre generado:
```
qr_tusitio_com_20250623_153000.png
```

---

## 🖼️ Ejemplo visual

![Ejemplo](qr_ejemplo.png)

---

## ⚙️ Personalización

Puedes modificar fácilmente los siguientes parámetros en el script:

| Parámetro         | Ubicación             | Descripción                            |
|------------------|-----------------------|----------------------------------------|
| `logo_size`      | Línea 98              | Tamaño del logo central (en píxeles)   |
| `padding_ratio`  | Función `add_center_logo()` | Margen blanco alrededor del logo     |
| `box_size`       | Función `generate_dot_qr()` | Tamaño de cada punto del QR         |

---

## 💻 Compatibilidad

- ✅ Windows  
- ✅ macOS (abre la imagen generada automáticamente)
- ✅ Linux

---

## 📜 Licencia

Este proyecto es de uso libre y puede ser modificado a tu gusto. Ideal para personalización de QR para branding, eventos, tarjetas, stickers o negocios.

---

## ✨ Autor

Script personalizado por [Gustavo Soto].