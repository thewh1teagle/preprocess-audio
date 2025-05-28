import argparse
import csv
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser(description="Merge multiple LJSpeech datasets safely")
    parser.add_argument(
        "-i", "--inputs", nargs="+", required=True,
        help="Paths to input LJSpeech dataset folders"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output folder for merged dataset"
    )
    args = parser.parse_args()
    print(f"🧪 Inputs: {args.inputs}")
    print(f"🧪 Output: {args.output}")


    output_dir = Path(args.output)
    output_wav_dir = output_dir / "wav"
    output_wav_dir.mkdir(parents=True, exist_ok=True)

    combined_metadata = []
    seen_ids = set()

    for dataset_path_str in args.inputs:
        dataset_path = Path(dataset_path_str)
        metadata_path = dataset_path / "metadata.csv"
        if not metadata_path.is_file():
            print(f"⚠️ Warning: metadata.csv not found in {dataset_path}, skipping.")
            continue

        with metadata_path.open(encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                orig_file_id = row[0]

                # הפוך כל ID לייחודי, אפילו אם קיים כבר בדאטהסט קודם
                file_id = orig_file_id
                suffix = 1
                while file_id in seen_ids:
                    file_id = f"{orig_file_id}_{suffix}"
                    suffix += 1
                seen_ids.add(file_id)

                orig_wav = dataset_path / "wav" / f"{orig_file_id}.wav"
                new_wav = output_wav_dir / f"{file_id}.wav"
                if not orig_wav.is_file():
                    print(f"⚠️ Warning: wav file {orig_wav} not found, skipping row.")
                    continue
                shutil.copy2(orig_wav, new_wav)

                combined_metadata.append([file_id] + row[1:])

    # כתיבת metadata.csv חדש
    output_metadata = output_dir / "metadata.csv"
    with output_metadata.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerows(combined_metadata)

    print("\n✅ Merge complete.")
    print(f"📄 metadata.csv entries: {len(combined_metadata)}")
    print(f"🔊 .wav files copied:   {len(list(output_wav_dir.glob('*.wav')))}")

if __name__ == "__main__":
    main()
