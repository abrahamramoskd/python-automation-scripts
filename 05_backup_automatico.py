"""
💾 BACKUP AUTOMÁTICO DE CARPETAS
----------------------------------
Crea respaldos comprimidos (.zip) de carpetas importantes.
Guarda N copias históricas y elimina las más antiguas automáticamente.

Uso:
    python 05_backup_automatico.py --origen "C:/MisProyectos" --destino "D:/Backups"
    python 05_backup_automatico.py --origen . --destino ~/Backups --max 5
    python 05_backup_automatico.py --programar 24  # backup cada 24 horas
"""

import os
import shutil
import argparse
import time
from pathlib import Path
from datetime import datetime

def crear_backup(origen: str, destino: str, max_copias: int = 7, prefijo: str = "backup") -> Path | None:
    origen_path = Path(origen).resolve()
    destino_path = Path(destino)

    if not origen_path.exists():
        print(f"❌ La carpeta origen no existe: {origen_path}")
        return None

    destino_path.mkdir(parents=True, exist_ok=True)

    # Nombre con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_zip = f"{prefijo}_{origen_path.name}_{timestamp}"
    ruta_zip = destino_path / nombre_zip

    print(f"\n💾 Iniciando backup...")
    print(f"   Origen:  {origen_path}")
    print(f"   Destino: {destino_path}")

    try:
        inicio = time.time()
        archivo_creado = shutil.make_archive(str(ruta_zip), "zip", str(origen_path.parent), str(origen_path.name))
        duracion = time.time() - inicio
        tamano = Path(archivo_creado).stat().st_size / (1024 * 1024)

        print(f"   ✅ Backup creado: {Path(archivo_creado).name}")
        print(f"   📦 Tamaño: {tamano:.2f} MB")
        print(f"   ⏱️  Tiempo: {duracion:.1f}s")

        limpiar_backups_viejos(destino_path, prefijo, max_copias)
        return Path(archivo_creado)

    except Exception as e:
        print(f"   ❌ Error al crear backup: {e}")
        return None

def limpiar_backups_viejos(destino: Path, prefijo: str, max_copias: int):
    """Elimina los backups más antiguos si hay más de max_copias."""
    patron = f"{prefijo}_*.zip"
    backups = sorted(destino.glob(patron), key=lambda f: f.stat().st_mtime)

    exceso = len(backups) - max_copias
    if exceso > 0:
        print(f"\n🧹 Eliminando {exceso} backup(s) antiguo(s)...")
        for viejo in backups[:exceso]:
            viejo.unlink()
            print(f"   🗑️  {viejo.name}")

def listar_backups(destino: str, prefijo: str = "backup"):
    destino_path = Path(destino)
    if not destino_path.exists():
        print("📭 No hay backups todavía.")
        return

    backups = sorted(destino_path.glob(f"{prefijo}_*.zip"),
                     key=lambda f: f.stat().st_mtime, reverse=True)

    if not backups:
        print("📭 No se encontraron backups.")
        return

    print(f"\n📋 Backups en {destino_path}:\n")
    total = 0
    for i, b in enumerate(backups, 1):
        tamano = b.stat().st_size / (1024 * 1024)
        fecha = datetime.fromtimestamp(b.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        total += tamano
        print(f"  {i:02d}. {b.name}")
        print(f"      📅 {fecha}  |  📦 {tamano:.2f} MB")
    print(f"\n  Total: {len(backups)} backup(s), {total:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea backups comprimidos automáticamente.")
    parser.add_argument("--origen",    required=False, help="Carpeta a respaldar")
    parser.add_argument("--destino",   required=False, default="./backups", help="Donde guardar los backups")
    parser.add_argument("--max",       type=int, default=7, help="Máximo de copias a conservar (default: 7)")
    parser.add_argument("--prefijo",   default="backup", help="Prefijo del nombre del archivo")
    parser.add_argument("--programar", type=int, metavar="HORAS", help="Repetir automáticamente cada N horas")
    parser.add_argument("--listar",    action="store_true", help="Listar backups existentes")
    args = parser.parse_args()

    if args.listar:
        listar_backups(args.destino, args.prefijo)

    elif args.origen:
        if args.programar:
            print(f"⏰ Backup programado cada {args.programar} hora(s). Ctrl+C para detener.\n")
            while True:
                crear_backup(args.origen, args.destino, args.max, args.prefijo)
                proxima = args.programar * 3600
                print(f"\n⏳ Próximo backup en {args.programar} hora(s)...")
                time.sleep(proxima)
        else:
            crear_backup(args.origen, args.destino, args.max, args.prefijo)

    else:
        parser.print_help()
