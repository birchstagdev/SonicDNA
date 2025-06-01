"""
Light‑weight wrapper for AudioLDM 2 text‑to‑audio generation.

📦  Requirements (one‑time):
    pip install torch torchaudio audioldm2 --upgrade

The first call will download model weights (~2 GB) to your HF cache.
Everything is kept self‑contained: the function returns the absolute
path of a 16‑bit WAV file saved inside ./data/.
"""

from pathlib import Path
import time
import torchaudio
from audioldm2 import text_to_audio


def _timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def generate_audio(prompt: str, duration_s: int) -> str:
    """Generate `duration_s` seconds of audio for `prompt` and return WAV path."""
    if not prompt:
        raise ValueError("Prompt must not be empty")

    # 1. Create output directory ------------------------------------------------
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    # 2. Call AudioLDM ----------------------------------------------------------
    #    200 inference steps give reasonable quality on 8 GB VRAM – adjust if
    #    you need faster results (e.g. 100).  Sample rate is always 16 kHz.
    print(f"[AudioLDM] Generating '{prompt}' ({duration_s}s)…")
    audio_tensor, sr = text_to_audio(
        prompt,
        audio_length_in_s=duration_s,
        num_inference_steps=200,
        guidance_scale=3.5,  # trade‑off between fidelity / creativity
    )

    # 3. Save WAV ---------------------------------------------------------------
    filename = f"tg_{_timestamp()}.wav"
    out_path = out_dir / filename
    torchaudio.save(str(out_path), audio_tensor, sample_rate=sr, bits_per_sample=16)

    print(f"[AudioLDM] Saved → {out_path.resolve()}")
    return str(out_path.resolve())
