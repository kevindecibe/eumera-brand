#!/usr/bin/env python3
"""
EUMERA — verificación de tipografías en un PDF generado.

Correr SIEMPRE después de generar. Chromium no falla cuando le falta
una fuente: cae en un sustituto y el PDF sale mal sin ningún error.
Este script es lo único que se entera.

    python3 check_pdf_fonts.py salida.pdf

Sale con código 1 si detecta cualquier fuente ajena al sistema.
Pensado para encadenar en un pipeline:  generar && check
"""
import subprocess
import sys

ESPERADAS = ("IBMPlexSerif", "IBMPlexSans", "IBMPlexMono")


def main(pdf: str) -> int:
    try:
        out = subprocess.run(["pdffonts", pdf], capture_output=True,
                             text=True, check=True).stdout
    except FileNotFoundError:
        print("ERROR: falta 'pdffonts' (paquete poppler-utils).")
        return 2
    except subprocess.CalledProcessError as e:
        print(f"ERROR: no se pudo leer {pdf}\n{e.stderr}")
        return 2

    # Saltear las dos líneas de encabezado de pdffonts.
    lineas = [l for l in out.splitlines()[2:] if l.strip()]
    if not lineas:
        print(f"AVISO: {pdf} no declara ninguna fuente embebida.")
        return 1

    intrusas = set()
    for l in lineas:
        nombre = l.split()[0]
        # pdffonts prefija un subset tag de 6 letras: "AAAAAA+IBMPlexSans"
        familia = nombre.split("+", 1)[-1]
        if not any(familia.startswith(e) for e in ESPERADAS):
            intrusas.add(familia)

    if intrusas:
        print(f"FALLBACK DETECTADO en {pdf}")
        for f in sorted(intrusas):
            print(f"   {f}")
        print("\nEl PDF salió con una fuente que no es IBM Plex.")
        print("Correr bootstrap.sh y regenerar. NO enviar este archivo.")
        return 1

    print(f"OK — {pdf}: sólo IBM Plex.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
