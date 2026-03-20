import os
import argparse
import subprocess
import json

def download_video(url, output_dir):
    """
    Downloads video and audio separately for maximum quality and flexibility.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get info first to have a clean filename base and title
    yt_dlp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv", "bin", "yt-dlp")
    if not os.path.exists(yt_dlp_path):
        yt_dlp_path = "yt-dlp"

    info_cmd = [
        yt_dlp_path,
        "--print", "%(id)s|%(title)s",
        url
    ]
    raw_info = subprocess.check_output(info_cmd).decode().strip()
    video_id, title = raw_info.split('|', 1)
    
    # Clean title for filename
    clean_title = "".join([c if c.isalnum() else "_" for c in title]).strip("_")
    
    output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")
    
    # Download audio only (for transcription)
    print(f"Downloading audio for {video_id}...")
    audio_cmd = [
        yt_dlp_path,
        "-x",
        "--audio-format", "m4a",
        "-o", output_template,
        url
    ]
    subprocess.run(audio_cmd, check=True)
    
    # Download video (we'll cut segments later from the original URL or high-quality file)
    # To keep it "free" and efficient, we might download the full high-quality mp4
    print(f"Downloading high-quality video for {video_id}...")
    video_cmd = [
        yt_dlp_path,
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", output_template,
        url
    ]
    subprocess.run(video_cmd, check=True)
    
    return video_id, clean_title

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video and audio.")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--output", default="Youtube/sources", help="Output directory")
    
    args = parser.parse_args()
    
    vid, title = download_video(args.url, args.output)
    print(f"DONE. Video ID: {vid} | Title: {title}")
