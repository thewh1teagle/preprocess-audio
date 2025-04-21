"""
Example using faster-whisper with ctranslate2 backend for fast audio transcription.
Run with:
    pip install faster-whisper
    python with_faster_whisper.py
"""

import json
from pathlib import Path
import faster_whisper

model = faster_whisper.WhisperModel('ivrit-ai/whisper-large-v3-turbo-ct2')

# Paths
wav_folder = Path('./wav')
json_path = Path('text.json')

# Load existing data if any
if json_path.exists():
    all_texts = json.loads(json_path.read_text(encoding='utf-8'))
else:
    all_texts = {}

# Get and sort .wav files by integer stem
wav_files = sorted(
    (f for f in wav_folder.glob('*.wav')),
    key=lambda p: int(p.stem)
)

# Transcribe and write immediately
for wav_file in wav_files:
    k = int(wav_file.stem)
    segs, _ = model.transcribe(str(wav_file), language='he')
    text = ' '.join(s.text for s in segs)
    all_texts[str(k)] = text
    json_path.write_text(json.dumps(all_texts, ensure_ascii=False, indent=4), encoding='utf-8')
    print(f"Transcribed {wav_file.name}: {text}")
