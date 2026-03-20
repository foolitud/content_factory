import os
import json
import argparse
import subprocess
from pyannote.audio import Pipeline
import torch

def extract_audio(video_path, audio_path):
    print(f"Extracting audio from {video_path}...")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", audio_path
    ]
    subprocess.run(cmd, check=True)

def diarize(audio_path, output_json, hf_token):
    print(f"Loading Pyannote pipeline with token...")
    # Use the 3.1 version which is state-of-the-art
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token
    )
    
    # Move to GPU if available (MPS for Mac M1)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    pipeline.to(device)

    print("Starting diarization (this may take a few minutes)...")
    diarization_output = pipeline(audio_path)

    # In Pyannote 3.1/4.0+, the output is a DiarizeOutput object
    # The actual annotation is in the 'speaker_diarization' attribute
    if hasattr(diarization_output, "speaker_diarization"):
        diarization = diarization_output.speaker_diarization
    elif hasattr(diarization_output, "annotation"):
        diarization = diarization_output.annotation
    else:
        diarization = diarization_output
    
    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "start": round(turn.start, 3),
            "end": round(turn.end, 3),
            "speaker": speaker
        })
    
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Diarization complete. Saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Diarization using Pyannote.")
    parser.add_argument("video", help="Path to source video")
    parser.add_argument("--output", help="Path to output JSON")
    parser.add_argument("--token", required=True, help="Hugging Face Access Token")
    
    args = parser.parse_args()
    
    video_path = args.video
    output_json = args.output
    if not output_json:
        output_json = os.path.splitext(video_path)[0] + "_diarization.json"
    
    audio_path = os.path.splitext(video_path)[0] + "_temp.wav"
    
    try:
        extract_audio(video_path, audio_path)
        diarize(audio_path, output_json, args.token)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
