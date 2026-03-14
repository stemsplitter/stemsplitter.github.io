#!/usr/bin/env bash
# Runs tests 2, 3, 5 then publishes everything.
# Tests 1 and 4 are already done and pushed.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
RAW_DIR="$RESULTS_DIR/raw"
DATA_DIR="$REPO_ROOT/_data/research"

mkdir -p "$RESULTS_DIR" "$RAW_DIR" "$DATA_DIR"

if [ -f "$SCRIPT_DIR/.venv/bin/python3" ]; then
  PYTHON="$SCRIPT_DIR/.venv/bin/python3"
else
  PYTHON="python3"
fi

cd "$SCRIPT_DIR"

START_TIME=$(date +%s)
echo ""
echo "========================================"
echo "  Tests 2, 3, 5 + Final Publish"
echo "  Started: $(date)"
echo "========================================"

# Test 2: Model comparison
echo ""
echo "[1/3] Test 2: Model Variant Comparison (~2-3 hours)"
"$PYTHON" test2_models.py \
  --output "$RESULTS_DIR/model_comparison.yml" \
  --raw-output "$RAW_DIR/test2_tracks.json"

cp "$RESULTS_DIR/model_comparison.yml" "$DATA_DIR/"
cd "$REPO_ROOT"
git add _data/research/model_comparison.yml scripts/benchmark/test2_models.py research/model-comparison.md
git commit -m "Add Test 2 model comparison results (fix hdemucs_mmi model name)"
git stash
git pull --rebase origin main
git stash pop || true
git push origin main
echo "  Test 2 published."

cd "$SCRIPT_DIR"

# Test 3: Track characteristics (reads test2 raw JSON)
echo ""
echo "[2/3] Test 3: Track Characteristic Breakdown (~5 min)"
"$PYTHON" test3_genre.py \
  --input "$RAW_DIR/test2_tracks.json" \
  --output "$RESULTS_DIR/genre_performance.yml"

# Test 5: Complexity prediction (reads test2 raw JSON + librosa)
echo ""
echo "[3/3] Test 5: Complexity Prediction (~30 min)"
"$PYTHON" test5_complexity.py \
  --input "$RAW_DIR/test2_tracks.json" \
  --output "$RESULTS_DIR/complexity.yml"

# Copy all remaining results and update meta
cp "$RESULTS_DIR/genre_performance.yml" "$DATA_DIR/"
cp "$RESULTS_DIR/complexity.yml" "$DATA_DIR/"

DATA_DIR="$DATA_DIR" "$PYTHON" - <<'PYEOF'
import yaml, datetime, os, torch
try:
    import demucs; dv = demucs.__version__
except Exception:
    dv = "unknown"
meta = {
    "run_date": datetime.datetime.now().strftime("%B %d, %Y"),
    "run_timestamp": datetime.datetime.now().isoformat(),
    "demucs_version": dv,
    "dataset": "MUSDB18-7s",
    "device": "Apple M4 MPS" if torch.backends.mps.is_available() else "CPU",
    "tests_completed": ["reconstruction", "format_quality", "model_comparison", "genre_performance", "complexity"],
}
out = os.path.join(os.environ.get("DATA_DIR", "_data/research"), "meta.yml")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
with open(out, "w") as f:
    yaml.dump(meta, f, default_flow_style=False, sort_keys=False)
print("  meta.yml updated (all 5 tests complete)")
PYEOF

# Generate blog post with real numbers
POST_DATE=$(date +%Y-%m-%d)
POST_PATH="$REPO_ROOT/_posts/${POST_DATE}-htdemucs-benchmark-results.md"
"$PYTHON" generate_blog_post.py \
  --results-dir "$RESULTS_DIR" \
  --output "$POST_PATH"

# Final push
cd "$REPO_ROOT"
git add _data/research/ _posts/
git commit -m "Add all HTDemucs benchmark results and announcement post ($(date +%Y-%m-%d))"
git stash
git pull --rebase origin main
git stash pop || true
git push origin main

END_TIME=$(date +%s)
ELAPSED=$(( END_TIME - START_TIME ))
HOURS=$(( ELAPSED / 3600 ))
MINS=$(( (ELAPSED % 3600) / 60 ))

echo ""
echo "========================================"
echo "  Pipeline complete!"
echo "  Runtime: ${HOURS}h ${MINS}m"
echo "  Finished: $(date)"
echo "========================================"
echo ""
echo "Live pages:"
echo "  Hub:        https://stemsplitter.github.io/research/"
echo "  Blog post:  https://stemsplitter.github.io/${POST_DATE}-htdemucs-benchmark-results/"
