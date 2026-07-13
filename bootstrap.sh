#!/usr/bin/env bash
# ============================================================
# EUMERA — bootstrap del sistema de marca
#
# Una línea, al inicio de cualquier sesión de Claude:
#
#   curl -sL https://raw.githubusercontent.com/ORG/eumera-brand/main/bootstrap.sh | bash
#
# Deja en disco: CSS, logos SVG y las tipografías instaladas y
# VERIFICADAS. Después de esto se puede generar PDF sin adjuntar
# ni un solo archivo al chat.
#
# EDITAR ANTES DE PUBLICAR: reemplazar ORG por la organización o
# usuario de GitHub donde viva el repo.
# ============================================================
set -euo pipefail

ORG="${EUMERA_BRAND_ORG:-kevindecibe}"
REPO="${EUMERA_BRAND_REPO:-eumera-brand}"
REF="${EUMERA_BRAND_REF:-main}"
DEST="${EUMERA_BRAND_DIR:-$HOME/eumera-brand}"

if [[ "$ORG" == "ORG" ]]; then
  echo "ERROR: editar ORG en bootstrap.sh (o exportar EUMERA_BRAND_ORG)."
  exit 1
fi

echo "→ Descargando ${ORG}/${REPO}@${REF}"
rm -rf "$DEST" && mkdir -p "$DEST"
# codeload sirve el tarball del repo sin autenticación (repo público).
curl -fsSL "https://codeload.github.com/${ORG}/${REPO}/tar.gz/refs/heads/${REF}" \
  | tar xz -C "$DEST" --strip-components=1

echo "→ Instalando tipografías"
mkdir -p "$HOME/.fonts"
cp "$DEST/fonts/otf/"*.otf "$HOME/.fonts/"
fc-cache -f > /dev/null 2>&1

echo "→ Verificando"
FAIL=0
for FAM in "IBM Plex Serif" "IBM Plex Sans" "IBM Plex Mono"; do
  # fc-match SIEMPRE devuelve algo: si la familia falta, devuelve un
  # sustituto. Hay que comparar el resultado, no el exit code.
  GOT="$(fc-match "${FAM}" family 2>/dev/null | head -1)"
  if [[ "$GOT" == *"IBM Plex"* ]]; then
    echo "   OK      ${FAM}"
  else
    echo "   FALLA   ${FAM}  → Chromium usaría: ${GOT:-<nada>}"
    FAIL=1
  fi
done

if [[ $FAIL -ne 0 ]]; then
  echo
  echo "ABORTAR: las tipografías no quedaron disponibles."
  echo "No generar PDFs: saldrían con la fuente equivocada y SIN NINGÚN ERROR."
  exit 1
fi

cat <<EOF

Listo.

  CSS     ${DEST}/brand/eumera-brand.css
  Logos   ${DEST}/brand/logos/
  Ejemplo ${DEST}/example/generar_pdf.py

Recordatorio: después de generar cualquier PDF, correr

  python3 ${DEST}/scripts/check_pdf_fonts.py salida.pdf

Si aparece una fuente que no sea IBM Plex, hubo fallback silencioso.
EOF
