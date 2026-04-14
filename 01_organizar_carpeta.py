"""
📁 ORGANIZADOR AUTOMÁTICO DE CARPETAS
--------------------------------------
Mueve archivos a subcarpetas según su extensión.
Ejemplo: .jpg → Imágenes/, .pdf → PDFs/, .mp3 → Música/

Uso:
    python 01_organizar_carpeta.py
    python 01_organizar_carpeta.py --ruta "C:/Users/Tu/Descargas"
"""

import os
import shutil
import argparse
from pathlib import Path

# Mapa de extensiones → nombre de carpeta destino
CATEGORIAS = {
    "Imágenes":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos":      [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Música":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documentos":  [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Código":      [".py", ".js", ".html", ".css", ".json", ".ts", ".java", ".cpp", ".c"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Ejecutables": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Fuentes":     [".ttf", ".otf", ".woff", ".woff2"],
    "Otros":       [],  # Archivos que no encajen en ninguna categoría
}

def obtener_categoria(extension: str) -> str:
    ext = extension.lower()
    for categoria, extensiones in CATEGORIAS.items():
        if ext in extensiones:
            return categoria
    return "Otros"

def organizar(ruta: str, modo_prueba: bool = False) -> dict:
    ruta = Path(ruta)
    if not ruta.exists():
        print(f"❌ La ruta '{ruta}' no existe.")
        return {}

    resumen = {}
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    if not archivos:
        print("📭 No hay archivos para organizar.")
        return {}

    print(f"\n{'🔍 MODO PRUEBA — no se moverá nada' if modo_prueba else '🚀 Organizando archivos...'}")
    print(f"📂 Carpeta: {ruta}")
    print(f"📄 Archivos encontrados: {len(archivos)}\n")

    for archivo in archivos:
        categoria = obtener_categoria(archivo.suffix)
        destino_dir = ruta / categoria
        destino = destino_dir / archivo.name

        # Manejar nombre duplicado
        contador = 1
        while destino.exists():
            stem = archivo.stem
            suffix = archivo.suffix
            destino = destino_dir / f"{stem}_{contador}{suffix}"
            contador += 1

        if not modo_prueba:
            destino_dir.mkdir(exist_ok=True)
            shutil.move(str(archivo), str(destino))

        resumen.setdefault(categoria, []).append(archivo.name)
        estado = "→" if not modo_prueba else "~"
        print(f"  {estado} [{categoria}] {archivo.name}")

    print("\n✅ Resumen:")
    for cat, archivos_cat in resumen.items():
        print(f"   {cat}: {len(archivos_cat)} archivo(s)")

    return resumen

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organiza archivos en subcarpetas por tipo.")
    parser.add_argument("--ruta", default=".", help="Ruta de la carpeta a organizar (default: carpeta actual)")
    parser.add_argument("--prueba", action="store_true", help="Modo prueba: muestra qué haría sin mover nada")
    args = parser.parse_args()

    organizar(args.ruta, modo_prueba=args.prueba)
