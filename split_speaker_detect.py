"""
1.
    Accept https://hf.co/pyannote/segmentation-3.0
    Accept https://hf.co/pyannote/speaker-diarization-3.1
2. 
    Create access token in https://hf.co/settings/tokens
3.
    export HF_TOKEN="token"
    uv run split_speaker_detect.py
"""

from pyannote.audio import Pipeline
import os
import torch
from pathlib import Path
import torchaudio

# ensure output directory exists
wavs = Path('wav')
wavs.mkdir(exist_ok=True)

# load pipeline with token
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=os.getenv('HF_TOKEN'))

# send pipeline to GPU (when available)
device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
pipeline.to(torch.device(device))

# apply pretrained pipeline
diarization = pipeline("audio.wav")

# load original audio
waveform, sample_rate = torchaudio.load("audio.wav")

# print the result and save segments
for i, (turn, _, speaker) in enumerate(diarization.itertracks(yield_label=True)):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

    # extract segment
    start_sample = int(turn.start * sample_rate)
    end_sample = int(turn.end * sample_rate)
    segment = waveform[:, start_sample:end_sample]

    # save segment
    out_path = wavs / f"{i}_speaker_{speaker}.wav"
    torchaudio.save(str(out_path), segment, sample_rate)
