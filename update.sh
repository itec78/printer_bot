#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/venv"

echo "Aggiornamento del codice..."
git pull

if [[ ! -d "$VENV_DIR" ]]; then
	echo "Creazione dell'ambiente virtuale..."
	python3 -m venv "$VENV_DIR"
fi

echo "Attivazione dell'ambiente virtuale..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "Installazione delle dipendenze..."
python -m pip install -r requirements.txt
for req in plugins/*/requirements.txt; do
	[[ -f "$req" ]] && python -m pip install -r "$req"
done