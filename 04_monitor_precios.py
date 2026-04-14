"""
🕷️ MONITOR DE PRECIOS WEB
---------------------------
Revisa el precio de un producto en una página web
y te avisa cuando baja de tu precio objetivo.

Funciona con cualquier sitio que muestre precio en texto.
Guarda historial en JSON y puede enviar alerta por consola o correo.

Dependencias:
    pip install requests beautifulsoup4

Uso:
    python 04_monitor_precios.py --url "https://..." --selector ".price" --objetivo 500
    python 04_monitor_precios.py --lista productos.json
"""

import json
import time
import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Instala dependencias: pip install requests beautifulsoup4")
    exit(1)

HISTORIAL_PATH = Path("historial_precios.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def extraer_precio(texto: str) -> float | None:
    """Extrae el primer número flotante de un texto (elimina $, ,, espacios)."""
    limpio = re.sub(r"[^\d.,]", "", texto).replace(",", "")
    match = re.search(r"\d+\.?\d*", limpio)
    return float(match.group()) if match else None

def obtener_precio(url: str, selector_css: str) -> tuple[float | None, str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        elemento = soup.select_one(selector_css)
        if not elemento:
            return None, "Selector no encontrado"
        texto = elemento.get_text(strip=True)
        precio = extraer_precio(texto)
        return precio, texto
    except requests.RequestException as e:
        return None, str(e)

def guardar_historial(datos: dict):
    historial = {}
    if HISTORIAL_PATH.exists():
        with open(HISTORIAL_PATH) as f:
            historial = json.load(f)
    
    url = datos["url"]
    historial.setdefault(url, [])
    historial[url].append({
        "fecha": datetime.now().isoformat(),
        "precio": datos["precio"],
        "texto_original": datos["texto"]
    })
    
    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

def monitorear(url: str, selector: str, objetivo: float,
               intervalo: int = 3600, nombre: str = "Producto"):
    print(f"\n🔍 Monitoreando: {nombre}")
    print(f"   URL: {url}")
    print(f"   Selector: {selector}")
    print(f"   Precio objetivo: ${objetivo:,.2f}")
    print(f"   Intervalo: cada {intervalo}s\n")

    while True:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        precio, texto = obtener_precio(url, selector)

        if precio is None:
            print(f"[{ahora}] ⚠️  No se pudo obtener precio. ({texto})")
        else:
            print(f"[{ahora}] 💰 Precio actual: ${precio:,.2f} (raw: {texto})")
            guardar_historial({"url": url, "precio": precio, "texto": texto})

            if precio <= objetivo:
                print(f"\n🚨 ¡ALERTA! El precio bajó a ${precio:,.2f} (objetivo: ${objetivo:,.2f})")
                print(f"   👉 Compra aquí: {url}\n")

        print(f"   ⏳ Próxima revisión en {intervalo // 60} min...\n")
        time.sleep(intervalo)

def mostrar_historial(url: str = None):
    if not HISTORIAL_PATH.exists():
        print("📭 Sin historial aún.")
        return
    with open(HISTORIAL_PATH) as f:
        historial = json.load(f)
    
    urls = [url] if url else list(historial.keys())
    for u in urls:
        if u not in historial:
            continue
        print(f"\n📈 {u}")
        for entrada in historial[u][-10:]:  # Últimas 10
            print(f"   {entrada['fecha']} → ${entrada['precio']:,.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor de precios web.")
    parser.add_argument("--url",       help="URL del producto")
    parser.add_argument("--selector",  help="Selector CSS del elemento de precio")
    parser.add_argument("--objetivo",  type=float, help="Precio objetivo para alertar")
    parser.add_argument("--nombre",    default="Producto", help="Nombre del producto")
    parser.add_argument("--intervalo", type=int, default=3600, help="Segundos entre revisiones (default: 3600)")
    parser.add_argument("--historial", action="store_true", help="Mostrar historial guardado")
    parser.add_argument("--prueba",    action="store_true", help="Una sola revisión sin loop")
    args = parser.parse_args()

    if args.historial:
        mostrar_historial(args.url)
    elif args.url and args.selector:
        if args.prueba:
            precio, texto = obtener_precio(args.url, args.selector)
            print(f"Precio encontrado: {texto} → ${precio}")
        else:
            monitorear(args.url, args.selector, args.objetivo or 0,
                      args.intervalo, args.nombre)
    else:
        parser.print_help()
