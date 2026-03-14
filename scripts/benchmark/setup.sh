#!/usr/bin/env bash
# HTDemucs Research Benchmark Setup
# Run once from the repo root: bash scripts/benchmark/setup.sh

set -e

echo "=== HTDemucs Research Benchmark Setup ==="
echo ""

# Check for Homebrew
if ! command -v brew &>/dev/null; then
  echo "Error: Homebrew is required. Install from https://brew.sh"
  exit 1
fi

# Check for Python 3
if ! command -v python3 &>/dev/null; then
  echo "Error: Python 3 is required."
  exit 1
fi

echo "[1/4] Installing ffmpeg via Homebrew..."
brew install ffmpeg

echo ""
echo "[2/4] Installing Python dependencies..."
pip3 install --upgrade pip

pip3 install \
  demucs \
  musdb \
  museval \
  mir_eval \
  librosa \
  soundfile \
  numpy \
  pandas \
  scipy \
  tqdm \
  pyyaml \
  torch \
  torchaudio

echo ""
echo "[3/4] Verifying torch MPS support (Apple Silicon)..."
python3 -c "
import torch
mps = torch.backends.mps.is_available()
print(f'  MPS available: {mps}')
if mps:
    print('  Apple M4 GPU acceleration: ENABLED')
else:
    print('  Falling back to CPU')
"

echo ""
echo "[4/4] Verifying demucs..."
python3 -c "
import demucs
print(f'  demucs version: {demucs.__version__}')
"

echo ""
echo "Setup complete. Run: bash scripts/benchmark/run_all.sh"
