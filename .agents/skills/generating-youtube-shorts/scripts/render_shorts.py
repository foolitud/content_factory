import os
import argparse
import subprocess
import json

def get_video_info(video_path):
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate",
        "-of", "json", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    
    fps_parts = stream["avg_frame_rate"].split('/')
    if len(fps_parts) == 2:
        fps = float(fps_parts[0]) / float(fps_parts[1])
    else:
        fps = float(fps_parts[0])
        
    return int(stream["width"]), int(stream["height"]), fps

def time_to_seconds(t_str):
    parts = list(map(float, t_str.split(':')))
    if len(parts) == 3: return parts[0]*3600 + parts[1]*60 + parts[2]
    if len(parts) == 2: return parts[0]*60 + parts[1]
    return parts[0]

def shift_ass(ass_path, offset_seconds):
    if not ass_path or not os.path.exists(ass_path):
        return ass_path
        
    temp_ass = ass_path.replace(".ass", "_temp.ass")
    with open(ass_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    def shift_timestamp(ts):
        h, m, s_cc = ts.split(':')
        s_parts = s_cc.split('.')
        s = s_parts[0]
        cc = s_parts[1]
        total = int(h)*3600 + int(m)*60 + int(s) + int(cc)/100
        new_total = max(0.0, total - offset_seconds)
        
        nh = int(new_total // 3600)
        nm = int((new_total % 3600) // 60)
        ns = int(new_total % 60)
        ncc = int(round((new_total - int(new_total)) * 100))
        return f"{nh}:{nm:02}:{ns:02}.{ncc:02}"

    with open(temp_ass, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("Dialogue:"):
                parts = line.split(',', 9)
                if len(parts) > 2:
                    parts[1] = shift_timestamp(parts[1])
                    parts[2] = shift_timestamp(parts[2])
                    line = ",".join(parts)
            f.write(line)
    return temp_ass

def extract_dialogues(ass_path):
    dialogues = []
    if not ass_path or not os.path.exists(ass_path):
        return dialogues
        
    with open(ass_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Dialogue:"):
                parts = line.split(',', 9)
                if len(parts) > 2:
                    start_sec = time_to_seconds(parts[1])
                    end_sec = time_to_seconds(parts[2])
                    dialogues.append((start_sec, end_sec))
    return dialogues

def load_diarization(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def get_speaker_at(diarization, time_sec):
    for d in diarization:
        if d["start"] <= time_sec <= d["end"]:
            return d["speaker"]
    return None

def calculate_dynamic_crop(data, start_frame, end_frame, orig_w, orig_h, cw, ch, fps, dialogues, offset_sec, diarization):
    """
    Fuses face tracking (MediaPipe) and audio diarization (Pyannote).
    Implements Scientific Principles:
    1. MAR Variance (Standard Deviation) for Speaker Detection.
    2. Exponential Moving Average (EMA) with Alpha=0.1.
    3. 5% Dead-Zone for Cinematic Transitions.
    """
    import numpy as np
    segment_data = [d for d in data if start_frame <= d["frame"] <= end_frame]
    if not segment_data:
        return str((orig_w - cw) // 2), str((orig_h - ch) // 2)

    # 1. Organize data by persistent face IDs
    face_tracks = {} # { face_id: { frame_num: {x, y, mar} } }
    for d in segment_data:
        f_num = d["frame"]
        for f in d.get("faces", []):
            f_id = f["id"]
            if f_id not in face_tracks: face_tracks[f_id] = {}
            face_tracks[f_id][f_num] = {"x": f["x"], "y": f["y"], "mar": f["mar"]}

    if not face_tracks:
        return str((orig_w - cw) // 2), str((orig_h - ch) // 2)

    # 2. Map Speaker IDs to Face IDs using MAR Variance
    speaker_map = {} 
    segment_end_sec = offset_sec + (end_frame - start_frame) / fps
    active_speakers = set([d["speaker"] for d in diarization if d["end"] > offset_sec and d["start"] < segment_end_sec])
    
    for s_id in active_speakers:
        s_intervals = [d for d in diarization if d["speaker"] == s_id and d["end"] > offset_sec and d["start"] < segment_end_sec]
        best_face_id = -1
        max_variance = -1.0
        
        for f_id, frames in face_tracks.items():
            mars = []
            for interval in s_intervals:
                f_s = int(max(offset_sec, interval["start"]) * fps)
                f_e = int(min(segment_end_sec, interval["end"]) * fps)
                mars.extend([frames[i]["mar"] for i in range(f_s, f_e + 1) if i in frames])
            
            if len(mars) > 15: # 0.5s window
                var = np.std(mars)
                if var > max_variance:
                    max_variance = var
                    best_face_id = f_id
        
        if best_face_id != -1:
            speaker_map[s_id] = best_face_id

    # 3. Framing Logic with Smoothing & Dead-Zone
    scene_targets = [] # (start_time_in_short, target_x, target_y)
    
    if face_tracks:
        main_face_id = max(face_tracks.items(), key=lambda x: len(x[1]))[0]
        all_main_xs = [f["x"] for f in face_tracks[main_face_id].values()]
        all_main_ys = [f["y"] for f in face_tracks[main_face_id].values()]
        last_x, last_y = sum(all_main_xs)/len(all_main_xs), sum(all_main_ys)/len(all_main_ys)
    else:
        last_x, last_y = 0.5, 0.45

    sorted_dialogues = sorted(dialogues, key=lambda d: d[0])
    active_dialogues = [d for d in sorted_dialogues if d[1] > offset_sec and d[0] < segment_end_sec]
    
    # Parameters for Cinematic Motion
    alpha = 0.1 # EMA Factor
    dead_zone = 0.05 # 5% threshold
    
    if not active_dialogues:
        scene_targets.append((0.0, last_x, last_y))
    else:
        for d_start, d_end in active_dialogues:
            f_start = int(max(offset_sec, d_start) * fps)
            f_end = int(min(segment_end_sec, d_end) * fps)
            mid_time = (d_start + d_end) / 2
            
            s_id = get_speaker_at(diarization, mid_time)
            target_f_id = speaker_map.get(s_id)
            
            # FALLBACK: MAR Variance over the current block
            if target_f_id is None:
                max_v = -1.0
                for f_id, frames in face_tracks.items():
                    local_mars = [frames[i]["mar"] for i in range(f_start, f_end + 1) if i in frames]
                    if len(local_mars) > 10:
                        v = np.std(local_mars)
                        if v > max_v:
                            max_v = v
                            target_f_id = f_id

            if target_f_id is not None and target_f_id in face_tracks:
                block_xs = [face_tracks[target_f_id][i]["x"] for i in range(f_start, f_end + 1) if i in face_tracks[target_f_id]]
                block_ys = [face_tracks[target_f_id][i]["y"] for i in range(f_start, f_end + 1) if i in face_tracks[target_f_id]]
                
                if block_xs:
                    new_x = sum(block_xs) / len(block_xs)
                    new_y = sum(block_ys) / len(block_ys)
                    
                    # Apply Dead-Zone: Only update if moved > 5%
                    if abs(new_x - last_x) > dead_zone:
                        last_x = (alpha * new_x) + ((1 - alpha) * last_x)
                    if abs(new_y - last_y) > dead_zone:
                        last_y = (alpha * new_y) + ((1 - alpha) * last_y)
            
            t_short = max(0.0, d_start - offset_sec)
            scene_targets.append((t_short, last_x, last_y))

    # 4. Generate Expressions
    def build_expr(targets, dim_size, crop_size, offset_name):
        if not targets: return str(int(0.5 * dim_size - crop_size // 2))
        short_dur = (end_frame - start_frame) / fps
        tmp_targets = targets + [(short_dur + 1.0, targets[-1][1], targets[-1][2])]
        if tmp_targets[0][0] > 0.1:
            tmp_targets.insert(0, (0.0, tmp_targets[0][1], tmp_targets[0][2]))
            
        current = str(int(0.5 * dim_size - crop_size // 2))
        for i in reversed(range(len(tmp_targets) - 1)):
            s_t, val_norm, _v_y = tmp_targets[i]
            if offset_name == 'y': val_norm = _v_y
            e_t = tmp_targets[i+1][0]
            pos = int(val_norm * dim_size - crop_size // 2)
            pos = max(0, min(pos, dim_size - crop_size))
            current = f"if(between(t,{s_t:.3f},{e_t:.3f}),{pos},{current})"
        return current

    return f"'{build_expr(scene_targets, orig_w, cw, 'x')}'", f"'{build_expr(scene_targets, orig_h, ch, 'y')}'"

def render_short(video_path, start_time, end_time, ass_path, output_path, face_json=None, diar_json=None, zoom=1.5):
    """
    Renders a 9:16 vertical short using dynamic scene-based cropping.
    """
    print(f"Loading metadata for {video_path}...")
    orig_w, orig_h, fps = get_video_info(video_path)
    offset = time_to_seconds(start_time)
    duration = time_to_seconds(end_time) - offset
    
    dialogues = extract_dialogues(ass_path)
    diarization = load_diarization(diar_json)
    
    shifted_ass = shift_ass(ass_path, offset)
    escaped_ass = shifted_ass.replace(":", "\\:").replace("'", "'\\\\''")

    ch = int(orig_h / zoom)
    if ch % 2 != 0: ch -= 1
    cw = int(ch * 9 / 16)
    if cw % 2 != 0: cw -= 1
    
    x_expr, y_expr = str((orig_w - cw) // 2), str((orig_h - ch) // 2)
    
    if face_json and os.path.exists(face_json):
        with open(face_json, "r") as f:
            face_meta = json.load(f)
        
        start_frame = int(offset * fps)
        end_frame = int((offset + duration) * fps)
        x_expr, y_expr = calculate_dynamic_crop(
            face_meta["data"], start_frame, end_frame, 
            orig_w, orig_h, cw, ch, fps, dialogues, offset, diarization
        )

    vf = f"crop={cw}:{ch}:{x_expr}:{y_expr},scale=1080:1920,ass='{escaped_ass}'"
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-ss", start_time,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",
        output_path
    ]
    
    print(f"Rendering segment {start_time} (dur: {duration}s) with zoom {zoom} and diarization fusion...")
    subprocess.run(cmd, check=True)
    
    if shifted_ass != ass_path and os.path.exists(shifted_ass):
        try: os.remove(shifted_ass)
        except: pass
        
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a YouTube Short.")
    parser.add_argument("video", help="Path to source video")
    parser.add_argument("start", help="Start time (HH:MM:SS)")
    parser.add_argument("end", help="End time (HH:MM:SS)")
    parser.add_argument("--ass", help="Path to ASS subtitle file")
    parser.add_argument("--faces", help="Path to face tracking JSON")
    parser.add_argument("--diarization", help="Path to diarization JSON")
    parser.add_argument("--zoom", type=float, default=1.2, help="Zoom factor (default 1.2)")
    parser.add_argument("--output", help="Path to output file")
    
    args = parser.parse_args()
    
    output = args.output
    if not output:
        base = os.path.splitext(os.path.basename(args.video))[0]
        output = f"{base}_short_{args.start.replace(':', '')}.mp4"
        
    render_short(args.video, args.start, args.end, args.ass, output, args.faces, args.diarization, args.zoom)
    print(f"DONE. Output: {output}")
