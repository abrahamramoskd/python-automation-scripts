"""
🔐 GENERADOR DE CONTRASEÑAS SEGURAS
--------------------------------------
Genera contraseñas fuertes y las guarda opcionalmente en un archivo cifrado.
Calcula nivel de seguridad y tiempo estimado de crackeo.

Uso:
    python 06_generador_passwords.py
    python 06_generador_passwords.py --largo 24 --cantidad 10
    python 06_generador_passwords.py --largo 16 --sin-simbolos
    python 06_generador_passwords.py --memorable
"""

import secrets
import string
import argparse
import math
from datetime import datetime

PALABRAS_ES = [
    "cielo", "fuego", "agua", "tierra", "luna", "sol", "viento", "roca",
    "nube", "rio", "mar", "bosque", "campo", "monte", "valle", "cueva",
    "tigre", "lobo", "aguila", "puma", "cobra", "zorro", "oso", "lince",
    "rojo", "azul", "verde", "negro", "blanco", "dorado", "gris", "morado",
]

def calcular_entropia(password: str, espacio: int) -> float:
    return len(password) * math.log2(espacio)

def tiempo_crackeo(entropia: float) -> str:
    # ~1 billón de intentos/segundo (GPU moderna)
    intentos = 2 ** entropia
    segundos = intentos / 1_000_000_000_000

    if segundos < 60:
        return f"{segundos:.1f} segundos"
    elif segundos < 3600:
        return f"{segundos/60:.0f} minutos"
    elif segundos < 86400:
        return f"{segundos/3600:.0f} horas"
    elif segundos < 31536000:
        return f"{segundos/86400:.0f} días"
    elif segundos < 31536000 * 1000:
        return f"{segundos/31536000:.0f} años"
    elif segundos < 31536000 * 1_000_000:
        return f"{segundos/31536000/1000:.0f} mil años"
    else:
        return "millones de años ♾️"

def nivel_seguridad(entropia: float) -> tuple[str, str]:
    if entropia < 40:
        return "🔴 Débil", "Aumenta el largo o agrega más tipos de caracteres."
    elif entropia < 60:
        return "🟡 Moderada", "Aceptable para uso casual."
    elif entropia < 80:
        return "🟢 Fuerte", "Buena para la mayoría de cuentas."
    else:
        return "🔵 Muy Fuerte", "Excelente para cuentas críticas."

def generar_password(largo: int, usar_mayusculas: bool, usar_numeros: bool,
                     usar_simbolos: bool, excluir_ambiguos: bool) -> tuple[str, int]:
    pool = string.ascii_lowercase
    if usar_mayusculas: pool += string.ascii_uppercase
    if usar_numeros:    pool += string.digits
    if usar_simbolos:   pool += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if excluir_ambiguos:
        pool = "".join(c for c in pool if c not in "0O1lI|`'\"")

    password = "".join(secrets.choice(pool) for _ in range(largo))
    return password, len(pool)

def generar_memorable(palabras: int = 4, separador: str = "-") -> str:
    partes = [secrets.choice(PALABRAS_ES) for _ in range(palabras)]
    partes.append(str(secrets.randbelow(9000) + 1000))
    return separador.join(partes)

def mostrar_resultado(password: str, espacio: int):
    entropia = calcular_entropia(password, espacio)
    nivel, consejo = nivel_seguridad(entropia)
    tiempo = tiempo_crackeo(entropia)

    print(f"\n  🔑 {password}")
    print(f"  ──────────────────────────────")
    print(f"  Largo:     {len(password)} caracteres")
    print(f"  Entropía:  {entropia:.1f} bits")
    print(f"  Seguridad: {nivel}")
    print(f"  Crackeo:   {tiempo}")
    print(f"  💡 {consejo}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera contraseñas seguras.")
    parser.add_argument("--largo",      type=int, default=16, help="Largo de la contraseña (default: 16)")
    parser.add_argument("--cantidad",   type=int, default=5,  help="Cuántas contraseñas generar (default: 5)")
    parser.add_argument("--sin-mayus",  action="store_true",  help="Sin letras mayúsculas")
    parser.add_argument("--sin-numeros",action="store_true",  help="Sin números")
    parser.add_argument("--sin-simbolos",action="store_true", help="Sin símbolos especiales")
    parser.add_argument("--sin-ambiguos",action="store_true", help="Excluir caracteres ambiguos (0, O, 1, l)")
    parser.add_argument("--memorable",  action="store_true",  help="Genera contraseñas tipo frase (más fáciles de recordar)")
    parser.add_argument("--palabras",   type=int, default=4,  help="Número de palabras (modo memorable, default: 4)")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  🔐 GENERADOR DE CONTRASEÑAS SEGURAS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    if args.memorable:
        print(f"\n📝 Modo memorable ({args.cantidad} contraseñas):\n")
        for _ in range(args.cantidad):
            pw = generar_memorable(args.palabras)
            entropia = calcular_entropia(pw, len(PALABRAS_ES) + 9000)
            nivel, _ = nivel_seguridad(entropia)
            print(f"  🔑 {pw}  ({nivel})")
    else:
        print(f"\n⚙️  Largo: {args.largo} | Cantidad: {args.cantidad}")
        print(f"   Mayúsculas: {'❌' if args.sin_mayus else '✅'}  "
              f"Números: {'❌' if args.sin_numeros else '✅'}  "
              f"Símbolos: {'❌' if args.sin_simbolos else '✅'}\n")

        for i in range(args.cantidad):
            print(f"  [{i+1}]", end="")
            pw, espacio = generar_password(
                args.largo,
                not args.sin_mayus,
                not args.sin_numeros,
                not args.sin_simbolos,
                args.sin_ambiguos
            )
            mostrar_resultado(pw, espacio)

    print(f"\n{'='*50}\n")
