import re
import sys

def vtt_time_to_ass(vtt_time: str) -> str:
    # VTT: MM:SS.mmm or HH:MM:SS.mmm -> ASS: H:MM:SS.cc
    parts = vtt_time.replace(',', '.').split(':')
    if len(parts) == 2: # MM:SS.mmm
        m, s_m = parts
        h = "0"
    else: # HH:MM:SS.mmm
        h, m, s_m = parts
    
    # Extract seconds and milliseconds
    s_parts = s_m.split('.')
    s = s_parts[0]
    ms: str = s_parts[1] if len(s_parts) > 1 else "000"
    cc: str = ms[:2] # Centiseconds
    
    return f"{int(h)}:{int(m):02}:{int(s):02}.{cc}"

def convert_vtt_to_ass(vtt_content: str, video_id: str) -> str:
    ass_header = f"""[Script Info]
Title: {video_id} Shorts
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,2,10,10,100,1
Style: Highlight,Arial,90,&H0000FFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,2,10,10,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    events: list[str] = []
    # Simple regex to find timestamps and text
    vtt_regex = re.compile(r"((?:\d{2}:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d{2}:)?\d{2}:\d{2}\.\d{3})\n(.*?)(?=\n\n|\n$|$)", re.DOTALL)
    
    for match in vtt_regex.finditer(vtt_content):
        start = vtt_time_to_ass(match.group(1))
        end = vtt_time_to_ass(match.group(2))
        text = match.group(3).replace('\n', ' ').strip()
        
        # Simple heuristic: if text is short, make it bigger/highlight
        style = "Highlight" if len(text) < 15 else "Default"
        
        # Escape ASS special characters if any (simplified)
        events.append(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{text}")
        
    return ass_header + "\n".join(events)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vtt_to_ass.py input.vtt [output.ass]")
        sys.exit(1)
        
    vtt_path = sys.argv[1]
    ass_path = sys.argv[2] if len(sys.argv) > 2 else vtt_path.replace(".vtt", ".ass")
    
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    ass_content = convert_vtt_to_ass(content, "Shorts")
    
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
        
    print(f"Converted {vtt_path} to {ass_path}")
