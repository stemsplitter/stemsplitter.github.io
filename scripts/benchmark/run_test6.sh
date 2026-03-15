#!/usr/bin/env bash
# run_test6.sh -- Run Spleeter vs HTDemucs comparison, copy results, and publish.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV="$SCRIPT_DIR/.venv312"
RESULTS_DIR="$SCRIPT_DIR/results"
DATA_DIR="$REPO_ROOT/_data/research"

echo "============================================================"
echo "Test 6: Spleeter vs HTDemucs -- Spleeter on CPU, HTDemucs on MPS"
echo "============================================================"

if [ ! -f "$VENV/bin/python3" ]; then
    echo "ERROR: .venv312 not found. Run setup_test6.sh first." >&2
    exit 1
fi

mkdir -p "$RESULTS_DIR"

cd "$SCRIPT_DIR"

echo ""
echo "Running test6_spleeter_comparison.py ..."
"$VENV/bin/python3" test6_spleeter_comparison.py \
    --output "$RESULTS_DIR/spleeter_comparison.yml"

echo ""
echo "Copying results to _data/research/ ..."
mkdir -p "$DATA_DIR"
cp "$RESULTS_DIR/spleeter_comparison.yml" "$DATA_DIR/spleeter_comparison.yml"

echo ""
echo "Committing and pushing to GitHub ..."
cd "$REPO_ROOT"

git stash || true
git pull --rebase origin main || true
git stash pop || true

git add "_data/research/spleeter_comparison.yml" \
        "scripts/benchmark/test6_spleeter_comparison.py" \
        "scripts/benchmark/run_test6.sh" \
        "research/spleeter-vs-htdemucs.md" || true

# Stage Jekyll pages if they exist (may have been created separately)
git add "_layouts/research-post.html" "llms.txt" "research/index.md" 2>/dev/null || true

git commit -m "Add Test 6: Spleeter vs HTDemucs benchmark results" || echo "Nothing to commit."
git push origin main || echo "Push failed -- try manually."

echo ""
echo "Done. Results published to /research/spleeter-vs-htdemucs/"
