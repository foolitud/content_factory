import cv2
import json
import argparse
import os
import math
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def calculate_mar(landmarks):
    """
    Calculates Mouth Aspect Ratio (MAR) using MediaPipe Face Mesh landmarks.
    Indices based on the standard 468 point mesh:
    Upper inner lip: 13
    Lower inner lip: 14
    Left mouth corner: 61
    Right mouth corner: 291
    """
    ul = landmarks[13]
    ll = landmarks[14]
    l_corner = landmarks[61]
    r_corner = landmarks[291]
    
    vert_dist = math.hypot(ul.x - ll.x, ul.y - ll.y)
    horiz_dist = math.hypot(l_corner.x - r_corner.x, l_corner.y - r_corner.y)
    
    if horiz_dist == 0:
        return 0.0
    return vert_dist / horiz_dist

def download_landmarker_model(path):
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    if not os.path.exists(path):
        print(f"Downloading MediaPipe Face Landmarker model to {path}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)
        print("Download complete.")

def detect_faces(video_path, output_json, max_frames=None):
    """
    Detects faces and tracks Mouth Aspect Ratio (MAR) using MediaPipe Tasks API.
    """
    print(f"Starting Face & Mouth detection with MediaPipe Tasks... max_frames={max_frames}")
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "face_landmarker.task")
    download_landmarker_model(model_path)
    
    # Initialize Face Landmarker
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=5,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    detector = vision.FaceLandmarker.create_from_options(options)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    orig_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    orig_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    target_height = 720
    scale = target_height / orig_height if orig_height > 0 else 1.0
    proc_width = int(orig_width * scale)
    
    # Centroid Tracking State: [ { "id": int, "x": float, "y": float, "last_frame": int } ]
    active_tracks = []
    next_face_id = 0
    max_track_dist = 0.15 # 15% normalized distance threshold

    face_data = []
    print(f"Detecting faces and mouth movements in {video_path}...")
    
    frame_idx = 0
    while cap.isOpened():
        if max_frames and frame_idx >= max_frames:
            break
            
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % 100 == 0:
            print(f"--- Frame {frame_idx} ---")
            
        frame_small = cv2.resize(frame, (proc_width, target_height))
        rgb_frame = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = detector.detect(mp_image)
        
        current_frame_faces = []
        if detection_result.face_landmarks:
            used_track_indices = set()
            
            # Map detections to existing tracks
            for face_landmarks in detection_result.face_landmarks:
                x_coords = [lm.x for lm in face_landmarks]
                y_coords = [lm.y for lm in face_landmarks]
                
                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)
                
                cx = (min_x + max_x) / 2
                cy = (min_y + max_y) / 2
                w, h = max_x - min_x, max_y - min_y
                mar = calculate_mar(face_landmarks)

                # Match with nearest available track
                best_track_idx = -1
                min_score = 100.0 # Heuristic score (lower is better)
                
                for i, track in enumerate(active_tracks):
                    if i in used_track_indices: continue
                    
                    dist = math.hypot(track["x"] - cx, track["y"] - cy)
                    # Add size consistency check (width/height shouldn't change drastically)
                    size_diff = abs(track.get("w", w) - w) + abs(track.get("h", h) - h)
                    
                    # Weight distance highly, but allow size to break ties or reject bad matches
                    score = dist + 0.5 * size_diff
                    
                    if dist < max_track_dist and score < min_score:
                        min_score = score
                        best_track_idx = i
                
                if best_track_idx != -1:
                    # Update existing track
                    track = active_tracks[best_track_idx]
                    track.update({"x": cx, "y": cy, "w": w, "h": h, "last_frame": frame_idx})
                    used_track_indices.add(best_track_idx)
                    face_id = track["id"]
                else:
                    # New face detected
                    face_id = next_face_id
                    next_face_id += 1
                    active_tracks.append({"id": face_id, "x": cx, "y": cy, "w": w, "h": h, "last_frame": frame_idx})
                    used_track_indices.add(len(active_tracks) - 1)

                current_frame_faces.append({
                    "id": face_id,
                    "x": round(cx, 4),
                    "y": round(cy, 4),
                    "w": round(w, 4),
                    "h": round(h, 4),
                    "mar": round(mar, 4)
                })

            # Cleanup old tracks (memory increased to 30 frames for occlusion handling)
            active_tracks = [t for t in active_tracks if frame_idx - t["last_frame"] < 30]
            
        face_data.append({
            "frame": frame_idx,
            "faces": current_frame_faces
        })
        
        frame_idx += 1
                
    cap.release()
    detector.close()
    
    meta = {
        "video": video_path,
        "fps": fps,
        "width": orig_width,
        "height": orig_height,
        "data": face_data
    }
    
    with open(output_json, "w") as f:
        json.dump(meta, f, indent=2)
    
    print(f"DONE. Multi-face tracking data saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-face detection for YouTube Shorts (MediaPipe Tasks MAR).")
    parser.add_argument("video", help="Path to source video")
    parser.add_argument("--output", help="Path to output JSON", required=True)
    parser.add_argument("--limit", type=int, help="Limit number of frames")
    
    args = parser.parse_args()
    if not os.path.exists(args.video):
        print(f"ERROR: Video file not found at {args.video}")
        exit(1)
        
    try:
        detect_faces(args.video, args.output, args.limit)
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
