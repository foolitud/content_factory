import os
import argparse
import whisper
import warnings

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def transcribe(audio_path, model_name="base"):
    """
    Transcribes audio using OpenAI Whisper.
    Optimized for M1 by letting Whisper handle device selection (it uses MPS if available).
    """
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)
    
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path, verbose=False)
    
    # Save as VTT for easy parsing later
    vtt_path = os.path.splitext(audio_path)[0] + ".vtt"
    writer = whisper.utils.get_writer("vtt", os.path.dirname(vtt_path))
    writer(result, vtt_path)
    
    # Also save as plain text for LLM analysis
    txt_path = os.path.splitext(audio_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
        
    return vtt_path, txt_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using Whisper.")
    parser.add_argument("file", help="Path to audio file")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny, base, small, medium, large)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        exit(1)
        
    vtt, txt = transcribe(args.file, args.model)
    print(f"Transcription complete.")
    print(f"VTT: {vtt}")
    print(f"TXT: {txt}")
