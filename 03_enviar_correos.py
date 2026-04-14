"""
📧 ENVIADOR AUTOMÁTICO DE CORREOS (Gmail)
------------------------------------------
Envía correos individuales o masivos usando Gmail.
Soporta HTML, archivos adjuntos y lista de destinatarios desde CSV.

CONFIGURACIÓN:
    1. Activa "Acceso de apps menos seguras" en tu cuenta Google
       O usa una "Contraseña de aplicación" (recomendado):
       https://myaccount.google.com/apppasswords
    2. Crea un archivo .env con:
       EMAIL_USER=tucorreo@gmail.com
       EMAIL_PASS=tu_contrasena_de_app

Uso:
    python 03_enviar_correos.py --destinatario amigo@gmail.com --asunto "Hola" --mensaje "¿Cómo estás?"
    python 03_enviar_correos.py --csv contactos.csv --asunto "Boletín" --html plantilla.html
"""

import smtplib
import csv
import os
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Intenta cargar .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def crear_mensaje(remitente: str, destinatario: str, asunto: str,
                  cuerpo: str, es_html: bool = False,
                  adjuntos: list = None) -> MIMEMultipart:
    msg = MIMEMultipart("alternative" if es_html else "mixed")
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    tipo = "html" if es_html else "plain"
    msg.attach(MIMEText(cuerpo, tipo, "utf-8"))

    # Adjuntos
    for ruta_adjunto in (adjuntos or []):
        ruta = Path(ruta_adjunto)
        if not ruta.exists():
            print(f"⚠️  Adjunto no encontrado: {ruta}")
            continue
        with open(ruta, "rb") as f:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(f.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{ruta.name}"')
        msg.attach(parte)

    return msg

def enviar(remitente: str, password: str, destinatario: str,
           asunto: str, cuerpo: str, es_html: bool = False,
           adjuntos: list = None) -> bool:
    try:
        msg = crear_mensaje(remitente, destinatario, asunto, cuerpo, es_html, adjuntos)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
        print(f"  ✅ Enviado → {destinatario}")
        return True
    except Exception as e:
        print(f"  ❌ Error con {destinatario}: {e}")
        return False

def enviar_desde_csv(csv_path: str, remitente: str, password: str,
                     asunto: str, plantilla: str, es_html: bool,
                     adjuntos: list = None):
    """
    El CSV debe tener columnas: email, nombre (opcional)
    La plantilla puede usar {nombre} para personalizar.
    """
    enviados, fallidos = 0, 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            email = fila.get("email", "").strip()
            nombre = fila.get("nombre", "Amigo").strip()
            if not email:
                continue
            cuerpo = plantilla.replace("{nombre}", nombre)
            ok = enviar(remitente, password, email, asunto, cuerpo, es_html, adjuntos)
            if ok: enviados += 1
            else: fallidos += 1

    print(f"\n📊 Resultado: {enviados} enviados, {fallidos} fallidos.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envía correos automáticos con Gmail.")
    parser.add_argument("--destinatario", help="Email del destinatario (envío individual)")
    parser.add_argument("--csv",          help="Archivo CSV con columnas: email, nombre")
    parser.add_argument("--asunto",       required=True, help="Asunto del correo")
    parser.add_argument("--mensaje",      help="Texto del mensaje (plano)")
    parser.add_argument("--html",         help="Ruta a archivo HTML con el contenido del correo")
    parser.add_argument("--adjunto",      nargs="*", help="Rutas de archivos adjuntos")
    args = parser.parse_args()

    EMAIL = os.getenv("EMAIL_USER")
    PASS  = os.getenv("EMAIL_PASS")

    if not EMAIL or not PASS:
        print("❌ Configura EMAIL_USER y EMAIL_PASS en un archivo .env")
        print("   Ejemplo:")
        print("   EMAIL_USER=tucorreo@gmail.com")
        print("   EMAIL_PASS=tu_contrasena_de_aplicacion")
        exit(1)

    # Determinar cuerpo y tipo
    es_html = False
    cuerpo = args.mensaje or ""
    if args.html:
        with open(args.html, "r", encoding="utf-8") as f:
            cuerpo = f.read()
        es_html = True

    if not cuerpo:
        print("❌ Proporciona --mensaje o --html")
        exit(1)

    print(f"\n📧 Remitente: {EMAIL}")
    print(f"📌 Asunto: {args.asunto}\n")

    if args.csv:
        enviar_desde_csv(args.csv, EMAIL, PASS, args.asunto, cuerpo, es_html, args.adjunto)
    elif args.destinatario:
        enviar(EMAIL, PASS, args.destinatario, args.asunto, cuerpo, es_html, args.adjunto)
    else:
        print("❌ Usa --destinatario o --csv")
