#!/usr/bin/env bash
# ============================================================
# EUMERA — instalación y verificación de tipografías
#
# Correr ANTES de generar cualquier PDF.
#
# Por qué importa: si IBM Plex no está instalada, Chromium NO
# falla. Cae en Arial/Helvetica en silencio y el PDF sale mal
# sin ningún error. Este script instala y verifica de verdad.
# ============================================================
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.fonts"

echo "→ Instalando IBM Plex en ${DEST}"
mkdir -p "$DEST"
cp "${DIR}/otf/"*.otf "$DEST/"
fc-cache -f > /dev/null 2>&1

echo "→ Verificando"
FAIL=0
for FAM in "IBM Plex Serif" "IBM Plex Sans" "IBM Plex Mono"; do
  # fc-match devuelve un sustituto si la familia no existe: hay que
  # comparar el resultado, no confiar en el exit code.
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
  echo "No generar PDFs: saldrían con fuente equivocada y sin avisar."
  exit 1
fi

echo
echo "Listo. IBM Plex disponible para Playwright/Chromium."
