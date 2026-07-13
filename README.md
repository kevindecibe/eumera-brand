# eumera-brand

Sistema de marca de EUMERA. Fuente de verdad de **paleta, tipografía, logos y
plantilla de PDF**.

Repo público a propósito: acá no hay nada confidencial. Los logos ya están en
eumera.eu, la paleta se deriva de ellos con un cuentagotas y las tipografías son
libres. Es público para que cualquier sesión de Claude pueda leerlo sin
credenciales. **Ningún documento, teaser ni dato de contraparte entra acá** — eso
vive en Drive y no se mueve.

---

## Uso

Al inicio de cualquier sesión de Claude, una línea:

```bash
curl -sL https://raw.githubusercontent.com/kevindecibe/eumera-brand/main/bootstrap.sh | bash
```

Deja las tipografías instaladas y **verificadas**, más el CSS y los logos en disco.
No hace falta adjuntar ni un archivo al chat.

Después, generar y **siempre** verificar:

```bash
python3 ~/eumera-brand/example/generar_pdf.py informe.pdf
python3 ~/eumera-brand/scripts/check_pdf_fonts.py informe.pdf
```

---

## Por qué el segundo comando no es opcional

**Cuando a Chromium le falta una fuente, no falla.** Cae en un sustituto y produce
un PDF perfectamente válido con la tipografía equivocada, sin emitir ningún error.
Nadie se entera hasta que lo abre el cliente.

`check_pdf_fonts.py` es lo único que se entera. Sale con código 1 si detecta
cualquier fuente ajena, así que encadena bien:

```bash
generar && verificar   # si falla el segundo, no se envía nada
```

---

## Estructura

```
bootstrap.sh                    una línea, deja todo listo
brand/
  eumera-brand.css              paleta, tipografía, grilla A4, componentes
  logos/                        12 SVG — 3 lockups x 4 variantes
fonts/
  otf/                          IBM Plex Serif / Sans / Mono
  OFL-LICENSE.txt
scripts/
  install-fonts.sh              instala y verifica (lo llama bootstrap)
  check_pdf_fonts.py            guard post-generación
example/
  generar_pdf.py                patrón de referencia, funciona tal cual
```

---

## Reglas del sistema

**Paleta.** Seis tokens. La fuente de verdad es el logo. Cualquier hex suelto en un
documento es deuda, no una variante.

| Token | Hex |
|---|---|
| `--navy-900` | `#0A1F4C` |
| `--blue-700` | `#013E7A` (primario) |
| `--blue-500` | `#0F63A0` |
| `--slate-400` | `#677593` |
| `--slate-200` | `#A6B4C8` |
| `--slate-50` | `#E0E8F0` |

**Acento por unidad.** Único punto de diferenciación visual. Se activa con una
clase en el contenedor:

| Unidad | Clase | Token | Hex |
|---|---|---|---|
| Mining | `.eumera-mining` | `--copper` | `#B0602A` |
| Sourcing | `.eumera-sourcing` | `--ocean` | `#178282` |
| Corporativo | *(sin clase)* | `--blue-500` | `#0F63A0` |

Ambos acentos comparten peso óptico exacto —contraste 4,61 sobre blanco y 3,47
sobre navy— así que se distinguen por tono y nunca compiten en jerarquía.

**Tipografía.** IBM Plex. Serif para títulos, sans para cuerpo y tablas, mono para
código. Superfamilia: métricas compartidas, coherencia garantizada.

**No negociable:**
- El logo va **inline como SVG**. Nunca `<img>`, nunca PNG en base64.
- Multi-columna con `display:table`, nunca `column-count` (limitación de WebKit).
- Márgenes en **cero** en `page.pdf()`; se controlan desde `@page` en el CSS.

---

## Limitación conocida del logo

**No existe versión monocromo de un solo color.** El isotipo no tiene contorno ni
espacio negativo: toda su estructura la carga el color. Forzado a un tono se
convierte en una mancha ilegible.

Las variantes `2tono-*` lo resuelven binarizando —conservan masa y creciente— pero
**incluyen el fondo pintado**, así que sólo se usan sobre fondo plano del color
indicado:

- `2tono-navy` → fondo blanco o claro
- `2tono-blanco` → fondo `#0A1F4C`
- `2tono-negro` → impresión a una tinta

Para un sello, un grabado o una marca de agua real hay que **redibujar el isotipo**
como vector con contorno. Es trabajo de diseño, no de normalización.

---

## Licencias

Ver `NOTICE.md`. En corto: **el código es libre, el logo no.** Que el repo sea
público no licencia la marca EUMERA a nadie.
