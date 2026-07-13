#!/usr/bin/env python3
"""
EUMERA — ejemplo mínimo y funcional de generación de PDF.

    python3 generar_pdf.py salida.pdf

Copiar este patrón. Los tres puntos que importan:

  1. El CSS se inyecta INLINE (no <link>): Chromium en headless no
     resuelve rutas relativas de forma confiable con set_content().
  2. El logo va INLINE como SVG crudo, nunca como <img> ni PNG base64.
  3. Los márgenes van en CERO en page.pdf() y se controlan desde
     @page en el CSS. Si se pasan márgenes acá, se duplican.
"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CSS = (RAIZ / "brand" / "eumera-brand.css").read_text()


def logo(nombre: str) -> str:
    """Devuelve el SVG crudo, listo para incrustar en el HTML."""
    return (RAIZ / "brand" / "logos" / f"{nombre}.svg").read_text()


# class="eumera-mining" activa el acento cobre.
# class="eumera-sourcing" activa el acento ocean.
# Sin clase, queda el acento corporativo.
HTML = f"""<!doctype html><meta charset="utf-8">
<style>{CSS}</style>

<section class="cover eumera-mining">
  <div class="logo">{logo('eumera-horizontal-2tono-blanco')}</div>
  <h1>Título del informe<br>en dos líneas</h1>
</section>

<section class="page eumera-mining">
  <h2 class="sec">Primera sección</h2>
  <div class="rule"></div>
  <p>Cuerpo de texto en IBM Plex Sans. Los acentos y el
  <strong>énfasis</strong> salen de los tokens, nunca de un hex suelto.</p>

  <div class="callout">
    <strong>Callout.</strong> El filete izquierdo toma el acento de la unidad.
  </div>

  <table>
    <tr><th>Mineral</th><th>Prioridad</th></tr>
    <tr><td>Cobre</td><td>Muy alta</td></tr>
    <tr><td>Tungsteno / wólfram</td><td>Muy alta</td></tr>
    <tr><td>Antimonio</td><td>Alta</td></tr>
  </table>
</section>
"""


async def generar(salida: str) -> None:
    async with async_playwright() as p:
        navegador = await p.chromium.launch()
        pagina = await navegador.new_page()
        await pagina.set_content(HTML, wait_until="networkidle")
        await pagina.emulate_media(media="print")
        await pagina.pdf(
            path=salida,
            width="210mm",
            height="297mm",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await navegador.close()
    print(f"→ {salida}")
    print("Ahora verificar:  python3 ../scripts/check_pdf_fonts.py", salida)


if __name__ == "__main__":
    asyncio.run(generar(sys.argv[1] if len(sys.argv) > 1 else "salida.pdf"))
