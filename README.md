# 🐍 Python Automation Scripts

> Colección de scripts Python listos para usar que automatizan tareas del día a día.  
> Sin frameworks complicados — solo Python puro o dependencias mínimas.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Scripts](https://img.shields.io/badge/scripts-6-6ef0c8?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-f06eaa?style=flat-square)

---

## 📦 Scripts incluidos

| # | Script | Descripción | Dependencias |
|---|--------|-------------|--------------|
| 01 | `01_organizar_carpeta.py` | Mueve archivos a subcarpetas por tipo (.jpg → Imágenes/, .pdf → PDFs/) | Ninguna |
| 02 | `02_renombrar_masivo.py` | Renombra archivos en masa: numeración, fechas, reemplazar texto | Ninguna |
| 03 | `03_enviar_correos.py` | Envía correos individuales o masivos con Gmail, soporta HTML y adjuntos | `python-dotenv` |
| 04 | `04_monitor_precios.py` | Revisa el precio de productos en web y alerta cuando bajan | `requests`, `bs4` |
| 05 | `05_backup_automatico.py` | Crea backups .zip con historial y eliminación automática de copias viejas | Ninguna |
| 06 | `06_generador_passwords.py` | Genera contraseñas fuertes con cálculo de entropía y tiempo de crackeo | Ninguna |

---

## 🚀 Instalación

```bash
git clone https://github.com/abrahamramoskd/python-automation-scripts.git
cd python-automation-scripts

# Instalar dependencias opcionales
pip install -r requirements.txt
```

> **Requisito:** Python 3.10 o superior

---

## 📖 Uso de cada script

### 📁 01 — Organizador de carpetas

```bash
# Vista previa (modo prueba, no mueve nada)
python 01_organizar_carpeta.py --ruta "C:/Descargas" --prueba

# Organizar de verdad
python 01_organizar_carpeta.py --ruta "C:/Descargas"

# Organizar la carpeta actual
python 01_organizar_carpeta.py
```

**Resultado:** Crea subcarpetas automáticamente:
```
Descargas/
├── Imágenes/    ← .jpg, .png, .gif...
├── Documentos/  ← .pdf, .docx, .xlsx...
├── Videos/      ← .mp4, .avi, .mkv...
├── Música/      ← .mp3, .flac, .wav...
├── Código/      ← .py, .js, .html...
└── Otros/       ← todo lo demás
```

---

### ✏️ 02 — Renombrador masivo

```bash
# Numerar: foto_001.jpg, foto_002.jpg...
python 02_renombrar_masivo.py --modo numerar --prefijo "foto_" --ruta ./mis-fotos

# Reemplazar texto en nombres
python 02_renombrar_masivo.py --modo reemplazar --buscar "IMG" --reemplazar "Foto"

# Convertir a minúsculas
python 02_renombrar_masivo.py --modo minusculas

# Agregar fecha al nombre
python 02_renombrar_masivo.py --modo fecha --prefijo "proyecto_"

# Ver cambios sin aplicar
python 02_renombrar_masivo.py --modo numerar --prefijo "doc_" --prueba
```

---

### 📧 03 — Enviador de correos

**Configuración previa:**
1. Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Crea una "Contraseña de aplicación"
3. Crea un archivo `.env`:
```env
EMAIL_USER=tucorreo@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx
```

```bash
# Correo simple
python 03_enviar_correos.py \
  --destinatario amigo@gmail.com \
  --asunto "Hola!" \
  --mensaje "¿Cómo estás?"

# Con adjunto
python 03_enviar_correos.py \
  --destinatario cliente@empresa.com \
  --asunto "Cotización" \
  --html plantilla.html \
  --adjunto cotizacion.pdf

# Masivo desde CSV (columnas: email, nombre)
python 03_enviar_correos.py \
  --csv contactos.csv \
  --asunto "Boletín Mensual" \
  --html newsletter.html
```

---

### 🕷️ 04 — Monitor de precios

```bash
# Revisar precio una vez
python 04_monitor_precios.py \
  --url "https://www.amazon.com.mx/dp/..." \
  --selector ".a-price-whole" \
  --prueba

# Monitorear con alerta (cada hora)
python 04_monitor_precios.py \
  --url "https://..." \
  --selector ".price" \
  --objetivo 800 \
  --nombre "Teclado mecánico"

# Ver historial guardado
python 04_monitor_precios.py --historial
```

> 💡 **Tip:** Usa DevTools del navegador (F12 → Inspector) para encontrar el selector CSS del precio.

---

### 💾 05 — Backup automático

```bash
# Backup inmediato
python 05_backup_automatico.py \
  --origen "C:/MisProyectos" \
  --destino "D:/Backups" \
  --max 7

# Backup automático cada 24 horas
python 05_backup_automatico.py \
  --origen ~/Documentos \
  --destino ~/Backups \
  --programar 24

# Ver backups existentes
python 05_backup_automatico.py --listar --destino ~/Backups
```

---

### 🔐 06 — Generador de contraseñas

```bash
# 5 contraseñas de 16 caracteres (default)
python 06_generador_passwords.py

# 10 contraseñas de 24 caracteres
python 06_generador_passwords.py --largo 24 --cantidad 10

# Solo letras y números (sin símbolos)
python 06_generador_passwords.py --sin-simbolos

# Contraseñas memorables tipo frase
python 06_generador_passwords.py --memorable --palabras 4
# Ejemplo: cielo-tigre-azul-luna-4821
```

---

## 🗂️ Estructura del proyecto

```
python-automation-scripts/
├── 01_organizar_carpeta.py
├── 02_renombrar_masivo.py
├── 03_enviar_correos.py
├── 04_monitor_precios.py
├── 05_backup_automatico.py
├── 06_generador_passwords.py
├── requirements.txt
└── README.md
```

---

## 🤝 Contribuir

¿Tienes un script útil que quieras agregar?

1. Fork el repositorio
2. Crea tu script con docstring al inicio explicando qué hace y cómo usarlo
3. Agrégalo al README con ejemplos
4. Abre un Pull Request

---

## 📄 Licencia

MIT — úsalo libremente en proyectos personales o comerciales.

---

Hecho con 🐍 por [abrahamramoskd](https://github.com/abrahamramoskd)  
¿Te fue útil? Dale una ⭐ al repo — significa mucho!
