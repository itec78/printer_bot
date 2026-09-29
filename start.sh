#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/venv"

if [[ ! -d "$VENV_DIR" ]]; then
	echo "Creazione dell'ambiente virtuale..."
	python3 -m venv "$VENV_DIR"
else
	echo "Ambiente virtuale già presente."
fi

echo "Attivazione dell'ambiente virtuale..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "Avvio del bot..."
exec python3 bot.py
