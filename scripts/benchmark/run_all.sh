#!/usr/bin/env bash
# HTDemucs Research Pipeline - Master Runner
#
# Usage (from repo root):
#   bash scripts/benchmark/run_all.sh
#
# What it does:
#   1. Auto-downloads MUSDB18-7s if not present (~1.5GB, no registration)
#   2. Runs all 5 benchmark tests in order
#   3. Copies results to _data/research/ for Jekyll
#   4. Generates and writes the announcement blog post
#   5. Commits and pushes everything

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the local venv if present, otherwise fall back to system python3
if [ -f "$SCRIPT_DIR/.venv/bin/python3" ]; then
  PYTHON="$SCRIPT_DIR/.venv/bin/python3"
else
  PYTHON="python3"
fi
alias python3="$PYTHON"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
RAW_DIR="$RESULTS_DIR/raw"
DATA_DIR="$REPO_ROOT/_data/research"
POSTS_DIR="$REPO_ROOT/_posts"

mkdir -p "$RESULTS_DIR" "$RAW_DIR" "$DATA_DIR"

cd "$SCRIPT_DIR"

START_TIME=$(date +%s)
echo ""
echo "========================================"
echo "  HTDemucs Research Benchmark Pipeline"
echo "  Started: $(date)"
echo "========================================"
echo ""

# -------------------------------------------------------------------
# TEST 4 first: fastest, no dependencies on test2 results
# Published as an interim push so something goes live quickly
# -------------------------------------------------------------------
echo "[1/5] Test 4: Stem Reconstruction Fidelity (~45 min)"
"$PYTHON" test4_reconstruction.py --output "$RESULTS_DIR/reconstruction.yml"

cp "$RESULTS_DIR/reconstruction.yml" "$DATA_DIR/"

# Write meta.yml with current run info
DATA_DIR="$DATA_DIR" "$PYTHON" - <<'PYEOF'
import yaml, datetime, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.')
try:
    import demucs
    dv = demucs.__version__
except Exception:
    dv = "unknown"
import torch
meta = {
    "run_date": datetime.datetime.now().strftime("%B %d, %Y"),
    "run_timestamp": datetime.datetime.now().isoformat(),
    "demucs_version": dv,
    "dataset": "MUSDB18-7s",
    "device": "Apple M4 MPS" if torch.backends.mps.is_available() else "CPU",
    "tests_completed": ["reconstruction"],
}
out = os.path.join(os.environ.get("DATA_DIR", "_data/research"), "meta.yml")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
with open(out, "w") as f:
    yaml.dump(meta, f, default_flow_style=False, sort_keys=False)
print(f"  meta.yml written")
PYEOF

cd "$REPO_ROOT"
git add _data/research/
git commit -m "Add Test 4 reconstruction fidelity benchmark results"
git stash
git pull --rebase origin main
git stash pop || true
git push origin main
echo "  Test 4 published."

cd "$SCRIPT_DIR"

# -------------------------------------------------------------------
# TEST 1: Format degradation (uses 20 tracks, ~1 hour)
# -------------------------------------------------------------------
echo ""
echo "[2/5] Test 1: Input Format Degradation (~60 min)"
"$PYTHON" test1_format.py --output "$RESULTS_DIR/format_quality.yml"

cp "$RESULTS_DIR/format_quality.yml" "$DATA_DIR/"
cd "$REPO_ROOT"
git add _data/research/format_quality.yml
git commit -m "Add Test 1 format quality benchmark results"
git stash
git pull --rebase origin main
git stash pop || true
git push origin main
echo "  Test 1 published."

cd "$SCRIPT_DIR"

# -------------------------------------------------------------------
# TEST 2: Model comparison (uses all 150 tracks x 4 models, ~3 hours)
# Also generates raw JSON consumed by tests 3 and 5
# -------------------------------------------------------------------
echo ""
echo "[3/5] Test 2: Model Variant Comparison (~3 hours)"
"$PYTHON" test2_models.py \
  --output "$RESULTS_DIR/model_comparison.yml" \
  --raw-output "$RAW_DIR/test2_tracks.json"

cp "$RESULTS_DIR/model_comparison.yml" "$DATA_DIR/"
cd "$REPO_ROOT"
git add _data/research/model_comparison.yml
git commit -m "Add Test 2 model comparison benchmark results"
git stash
git pull --rebase origin main
git stash pop || true
git push origin main
echo "  Test 2 published."

cd "$SCRIPT_DIR"

# -------------------------------------------------------------------
# TEST 3: Track characteristic breakdown (reads test2 raw JSON, fast)
# -------------------------------------------------------------------
echo ""
echo "[4/5] Test 3: Track Characteristic Breakdown (~5 min)"
"$PYTHON" test3_genre.py \
  --input "$RAW_DIR/test2_tracks.json" \
  --output "$RESULTS_DIR/genre_performance.yml"

# -------------------------------------------------------------------
# TEST 5: Complexity prediction (reads test2 raw JSON + librosa, ~30 min)
# -------------------------------------------------------------------
echo ""
echo "[5/5] Test 5: Complexity Prediction (~30 min)"
"$PYTHON" test5_complexity.py \
  --input "$RAW_DIR/test2_tracks.json" \
  --output "$RESULTS_DIR/complexity.yml"

# -------------------------------------------------------------------
# Copy all remaining results and generate blog post
# -------------------------------------------------------------------
echo ""
echo "Copying all results to _data/research/..."
cp "$RESULTS_DIR/genre_performance.yml" "$DATA_DIR/"
cp "$RESULTS_DIR/complexity.yml" "$DATA_DIR/"

# Update meta.yml with all tests completed
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
print("  meta.yml updated (all tests complete)")
PYEOF

echo ""
echo "Generating blog post..."
POST_DATE=$(date +%Y-%m-%d)
POST_PATH="$POSTS_DIR/${POST_DATE}-htdemucs-benchmark-results.md"

"$PYTHON" generate_blog_post.py \
  --results-dir "$RESULTS_DIR" \
  --output "$POST_PATH"

# Final commit and push
cd "$REPO_ROOT"
git add _data/research/ _posts/
git commit -m "Add complete HTDemucs benchmark results and announcement post ($(date +%Y-%m-%d))"
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
echo "  Total runtime: ${HOURS}h ${MINS}m"
echo "  Published at: $(date)"
echo "========================================"
echo ""
echo "Live pages:"
echo "  Research hub:  https://stemsplitter.github.io/research/"
echo "  Format test:   https://stemsplitter.github.io/research/format-quality/"
echo "  Model test:    https://stemsplitter.github.io/research/model-comparison/"
echo "  Genre test:    https://stemsplitter.github.io/research/genre-performance/"
echo "  Recon test:    https://stemsplitter.github.io/research/reconstruction-fidelity/"
echo "  Complexity:    https://stemsplitter.github.io/research/complexity-prediction/"
echo "  Blog post:     https://stemsplitter.github.io/${POST_DATE}-htdemucs-benchmark-results/"
