"""
✏️ RENOMBRADOR MASIVO DE ARCHIVOS
-----------------------------------
Renombra todos los archivos de una carpeta con un prefijo,
sufijo, numeración automática o reemplazando texto en el nombre.

Uso:
    python 02_renombrar_masivo.py --modo numerar --prefijo "foto_"
    python 02_renombrar_masivo.py --modo reemplazar --buscar "IMG" --reemplazar "Foto"
    python 02_renombrar_masivo.py --modo minusculas
    python 02_renombrar_masivo.py --modo fecha
"""

import os
import argparse
from pathlib import Path
from datetime import datetime

def renombrar_numerar(archivos: list[Path], prefijo: str, sufijo: str, inicio: int) -> list[tuple]:
    pares = []
    for i, archivo in enumerate(archivos, start=inicio):
        nuevo = archivo.parent / f"{prefijo}{str(i).zfill(3)}{sufijo}{archivo.suffix}"
        pares.append((archivo, nuevo))
    return pares

def renombrar_reemplazar(archivos: list[Path], buscar: str, reemplazar: str) -> list[tuple]:
    pares = []
    for archivo in archivos:
        nuevo_nombre = archivo.stem.replace(buscar, reemplazar) + archivo.suffix
        pares.append((archivo, archivo.parent / nuevo_nombre))
    return pares

def renombrar_minusculas(archivos: list[Path]) -> list[tuple]:
    return [(a, a.parent / a.name.lower()) for a in archivos]

def renombrar_mayusculas(archivos: list[Path]) -> list[tuple]:
    return [(a, a.parent / a.name.upper()) for a in archivos]

def renombrar_fecha(archivos: list[Path], prefijo: str) -> list[tuple]:
    fecha = datetime.now().strftime("%Y%m%d")
    pares = []
    for i, archivo in enumerate(archivos, start=1):
        nuevo = archivo.parent / f"{prefijo}{fecha}_{str(i).zfill(3)}{archivo.suffix}"
        pares.append((archivo, nuevo))
    return pares

def aplicar_renombrado(pares: list[tuple], modo_prueba: bool, extension_filtro: str = None):
    if not pares:
        print("📭 No hay archivos para renombrar.")
        return

    print(f"\n{'🔍 MODO PRUEBA' if modo_prueba else '✏️ Renombrando...'}\n")
    cambios = 0

    for original, nuevo in pares:
        if extension_filtro and original.suffix.lower() != extension_filtro.lower():
            continue
        if original == nuevo:
            continue
        print(f"  {original.name}  →  {nuevo.name}")
        if not modo_prueba:
            original.rename(nuevo)
        cambios += 1

    print(f"\n✅ {cambios} archivo(s) {'serían renombrados' if modo_prueba else 'renombrados'}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Renombra archivos en masa.")
    parser.add_argument("--ruta",       default=".", help="Carpeta con los archivos")
    parser.add_argument("--modo",       choices=["numerar", "reemplazar", "minusculas", "mayusculas", "fecha"],
                                        required=True, help="Modo de renombrado")
    parser.add_argument("--prefijo",    default="",  help="Texto al inicio del nombre")
    parser.add_argument("--sufijo",     default="",  help="Texto al final del nombre (antes de extensión)")
    parser.add_argument("--inicio",     type=int, default=1, help="Número de inicio para numeración")
    parser.add_argument("--buscar",     default="",  help="Texto a buscar (modo reemplazar)")
    parser.add_argument("--reemplazar", default="",  help="Texto de reemplazo (modo reemplazar)")
    parser.add_argument("--ext",        default=None, help="Filtrar por extensión, ej: .jpg")
    parser.add_argument("--prueba",     action="store_true", help="Ver cambios sin aplicarlos")
    args = parser.parse_args()

    ruta = Path(args.ruta)
    archivos = sorted([f for f in ruta.iterdir() if f.is_file()])

    if args.modo == "numerar":
        pares = renombrar_numerar(archivos, args.prefijo, args.sufijo, args.inicio)
    elif args.modo == "reemplazar":
        pares = renombrar_reemplazar(archivos, args.buscar, args.reemplazar)
    elif args.modo == "minusculas":
        pares = renombrar_minusculas(archivos)
    elif args.modo == "mayusculas":
        pares = renombrar_mayusculas(archivos)
    elif args.modo == "fecha":
        pares = renombrar_fecha(archivos, args.prefijo)

    aplicar_renombrado(pares, modo_prueba=args.prueba, extension_filtro=args.ext)
