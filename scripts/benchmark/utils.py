#!/usr/bin/env python3
"""
Shared utilities for HTDemucs benchmark scripts.
"""

import os
import time
import numpy as np
import torch
import yaml


def get_device():
    """Return the best available PyTorch device string."""
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_model(model_name, device):
    """Load a demucs model by name and move to device."""
    from demucs.pretrained import get_model
    print(f"  Loading model: {model_name}...")
    model = get_model(model_name)
    model.eval()
    model = model.to(device)
    return model


def separate_track(audio, rate, model, device):
    """
    Separate audio using a demucs model.

    Args:
        audio: numpy array (samples, channels) or (samples,)
        rate:  sample rate in Hz
        model: loaded demucs model
        device: 'mps', 'cuda', or 'cpu'

    Returns:
        dict mapping stem name -> numpy (samples, channels)
    """
    import torchaudio

    # Ensure stereo (samples, 2)
    if audio.ndim == 1:
        audio = np.stack([audio, audio], axis=1)
    elif audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)

    # (channels, samples) tensor
    wav = torch.tensor(audio.T, dtype=torch.float32)

    # Resample to 44100 Hz if needed
    target_sr = 44100
    if rate != target_sr:
        wav = torchaudio.functional.resample(wav, rate, target_sr)

    # Batch dimension: (1, channels, samples)
    wav = wav.unsqueeze(0).to(device)

    from demucs.apply import apply_model

    with torch.no_grad():
        try:
            sources = apply_model(
                model, wav,
                shifts=1, split=True, overlap=0.25,
                progress=False,
            )
        except RuntimeError as e:
            # MPS can occasionally fail on edge cases; fall back to CPU
            print(f"    Device error, retrying on CPU: {type(e).__name__}")
            sources = apply_model(
                model.cpu(), wav.cpu(),
                shifts=1, split=True, overlap=0.25,
                progress=False,
            )
            model.to(device)

    # (1, n_stems, channels, samples) -> (n_stems, channels, samples)
    sources = sources[0].cpu()

    result = {}
    for i, name in enumerate(model.sources):
        stem = sources[i].numpy().T  # (samples, channels)
        if rate != target_sr:
            t = torch.tensor(stem.T, dtype=torch.float32)
            t = torchaudio.functional.resample(t, target_sr, rate)
            stem = t.numpy().T
        result[name] = stem

    return result


def compute_sdr(reference, estimate):
    """
    Compute SDR between a reference and estimated stem.

    Args:
        reference: numpy (samples, channels) or (samples,)
        estimate:  numpy (samples, channels) or (samples,)

    Returns:
        SDR float in dB, or None if the reference is silent or
        computation fails.
    """
    try:
        min_len = min(len(reference), len(estimate))
        ref = reference[:min_len]
        est = estimate[:min_len]

        # Mix to mono for BSSEval
        if ref.ndim > 1:
            ref = ref.mean(axis=1)
        if est.ndim > 1:
            est = est.mean(axis=1)

        # Skip silent reference stems
        if np.abs(ref).max() < 1e-6:
            return None

        import mir_eval
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sdr_vals, _, _, _ = mir_eval.separation.bss_eval_sources(
                ref[np.newaxis, :],
                est[np.newaxis, :],
            )
        val = float(sdr_vals[0])
        return val if np.isfinite(val) and val > -100 else None

    except Exception:
        return None


def median_sdr(values):
    """Median of a list, ignoring None entries."""
    valid = [v for v in values if v is not None]
    if not valid:
        return None
    return round(float(np.nanmedian(valid)), 2)


def mean_sdr(values):
    """Mean of a list, ignoring None entries."""
    valid = [v for v in values if v is not None]
    if not valid:
        return None
    return round(float(np.mean(valid)), 2)


def load_musdb(data_root=None, subset="test"):
    """
    Load MUSDB18-7s tracks. Downloads automatically on first run (~1.5 GB).

    Args:
        data_root: path to store the dataset (defaults to ~/musdb18)
        subset:    'test' or 'train'

    Returns:
        list of musdb Track objects
    """
    import musdb
    kwargs = {"download": True, "subsets": subset}
    if data_root:
        kwargs["root"] = data_root
    mus = musdb.DB(**kwargs)
    tracks = list(mus)
    print(f"  Loaded {len(tracks)} {subset} tracks from MUSDB18-7s")
    return tracks


def save_yaml(data, path):
    """Write dict to YAML file, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  Saved: {path}")
