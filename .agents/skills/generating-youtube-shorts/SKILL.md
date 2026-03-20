---
name: generating-youtube-shorts
description: Automates the creation of vertical YouTube Shorts from existing videos. Downloads, transcribes (Whisper M1), analyzes (Antigravity), crops, and captions videos.
---

# Generating YouTube Shorts

## When to use this skill

- Creating viral short-form content from long-form YouTube videos.
- Automating vertical cropping and dynamic "Hormozi-style" captions.
- Extracting the most engaging segments from a video based on transcript analysis.

## Setup

1. **Dependencies**: This skill requires FFmpeg and several Python libraries.
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
2. **MediaPipe Model**: The `detect_faces.py` script automatically downloads the required `face_landmarker.task` model (~100MB) to the `resources/` directory on first run.

## Workflow: Create a Short

### 1. Information Gathering
- The agent **MUST explicitly ask the user**: "Do you want to provide a YouTube URL, or use an existing video from the `Youtube/sources/` directory?"
- If the user chooses a local video, the agent must list the `.mp4` files in `Youtube/sources/` and ask the user to select one.
- Optional: Ask the user if they want to specify a theme or a specific person to focus on in the video.

### 2. Pre-processing (Automatic)
- **Download**: 
  - If a YouTube URL is provided, run `scripts/download.py` to get the audio and video source.
  - If a local video file is provided, skip this step and use the local file directly for the next steps.
- **Transcription**: Run `scripts/transcribe.py`. This uses `faster-whisper` optimized for Apple Silicon.
- **Face & Mouth Detection**: Run `scripts/detect_faces.py`. This uses **Google MediaPipe Face Landmarker** to track 478 3D facial landmarks and calculate the **Mouth Aspect Ratio (MAR)** for precise active speaker detection.
- **Consolidation**: The scripts generate `.vtt` and `.json` (tracking metadata) files next to the source video.

### 3. Segment Analysis (Antigravity Intelligence)
- Antigravity reads the transcript and identifies engaging segments (30-58 seconds).
- **Validation**: Present the suggested segments to the user for approval.

### 4. Directing & Rendering
- For each approved segment, run `scripts/render_shorts.py`:
    - **Auto-Centering**: Use the `--faces` flag pointing to the MediaPipe JSON.
        - **Active Speaker Detection (ASD)**: The script analyzes the MAR variance during each subtitle dialogue to identify who is actually speaking.
        - **Dynamic Cuts**: It automatically performs hard cuts between speakers to keep the active person centered.
        - **Smoothing**: Uses weighted moving averages for jitter-free tracking if there is only one person or during slow movements.
    - **Zoom**: Recommended `--zoom 1.5` (default) to ensure faces fill the vertical frame optimally.
    - **Captions**: Generates dynamic, multi-color ASS subtitles with automatic timestamp synchronization.
    - **Final Cut**: Exports to `Youtube/shorts/<Clean_Title>_<Segment_Name>.mp4`.

## Guardrails

- **Video Length**: Shorts must be under 60 seconds. Our scripts target 50-58 seconds to ensure compliance.
- **Copyright**: Ensure you have permission to redistribute the content.
- **Hardware**: Transcription is CPU/GPU intensive. On M1, use the `base` or `small` Whisper model for best speed/accuracy balance.

## Resources

- [scripts/](scripts/): Core automation logic.
- [resources/](resources/): Transcription and styling templates.
- [Youtube/shorts/](../../../../Youtube/shorts/): Destination for generated videos.
