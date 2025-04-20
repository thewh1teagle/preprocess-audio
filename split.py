"""
Install ffmpeg
    winget install --id=Gyan.FFmpeg -e
Install dependencies
    uv venv
    uv pip install pydub
"""
import os
from pydub import AudioSegment, silence

input_file = 'audio.wav'
output_dir = './wav'
os.makedirs(output_dir, exist_ok=True)

min_len = 2 * 1000  # 2 sec
max_len = 25 * 1000  # 25 sec

audio = AudioSegment.from_wav(input_file)

# Split on silence
chunks = silence.split_on_silence(
    audio,
    min_silence_len=300,
    silence_thresh=audio.dBFS - 14,
    keep_silence=200
)

i = 0
for chunk in chunks:
    if min_len <= len(chunk) <= max_len:
        out_path = os.path.join(output_dir, f'{i}.wav')
        chunk.export(out_path, format='wav')
        i += 1
