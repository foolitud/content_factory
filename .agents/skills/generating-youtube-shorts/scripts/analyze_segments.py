import os
import argparse
import re

def parse_vtt(vtt_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract blocks
    blocks = []
    vtt_regex = re.compile(r"(?:(\d{2}):)?(\d{2}:\d{2}\.\d{3}) --> (?:(\d{2}):)?(\d{2}:\d{2}\.\d{3})\n(.*?)(?=\n\n|\n$|$)", re.DOTALL)
    for match in vtt_regex.finditer(content):
        h1 = match.group(1) if match.group(1) else "00"
        ts1 = f"{h1}:{match.group(2)}"
        h2 = match.group(3) if match.group(3) else "00"
        ts2 = f"{h2}:{match.group(4)}"
        blocks.append({
            "start": ts1,
            "end": ts2,
            "text": match.group(5).replace('\n', ' ').strip()
        })
    return blocks

def group_for_analysis(blocks, window_size=60):
    """
    Groups segments into chunks of ~60s for easier reading by LLM.
    """
    # Simple grouping for now
    text = ""
    for b in blocks:
        text += f"[{b['start']} - {b['end']}] {b['text']}\n"
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare transcript for analysis.")
    parser.add_argument("vtt", help="Path to VTT file")
    
    args = parser.parse_args()
    
    blocks = parse_vtt(args.vtt)
    prompt_text = group_for_analysis(blocks)
    
    output_path = args.vtt.replace(".vtt", "_analysis.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# TRANSCRIPT FOR HIGHLIGHT ANALYSIS\n\n")
        f.write(prompt_text)
        
    print(f"Analysis file created: {output_path}")
