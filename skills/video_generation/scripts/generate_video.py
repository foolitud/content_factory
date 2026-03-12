import os
import json
import argparse
import time
import requests
import jwt
import base64
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not found. Skipping .env file loading.")

from google import genai
from google.genai import types

def encode_kling_jwt(ak, sk):
    """Generates a JWT token for Kling AI authentication."""
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # Token valid for 30 minutes
        "nbf": int(time.time()) - 5      # Token valid from 5 seconds ago
    }
    token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
    return token

def generate_video_vertex(prompt_data, output_file_path, model_id, image_path=None):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if not project_id or not location or not credentials_path:
        print("Error: Required environment variables are missing for Vertex AI.")
        return False

    client = genai.Client(vertexai=True, project=project_id, location=location)
    
    # Flattening logic
    dense_prompt = f"TASK: {prompt_data.get('task', '')}. "
    dense_prompt += f"CINEMATOGRAPHY: {json.dumps(prompt_data.get('cinematography', {}))}. "
    dense_prompt += f"SUBJECT: {json.dumps(prompt_data.get('subject', {}))}. "
    dense_prompt += f"ENVIRONMENT: {json.dumps(prompt_data.get('environment', {}))}. "
    
    negative_prompt_data = prompt_data.get('negative_prompt', {}).get('forbidden_elements', [])
    negative_prompt = ", ".join(negative_prompt_data) if negative_prompt_data else ""
    
    final_prompt = dense_prompt
    if negative_prompt:
         final_prompt += f" DO NOT INCLUDE: {negative_prompt}."

    print(f"Initiating {model_id} generation on Vertex AI...")
    
    try:
        # Pre-process image if provided
        input_file = None
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                input_file = types.File(
                    display_name=os.path.basename(image_path),
                    mime_type="image/jpeg", # simplified
                    data=f.read()
                )

        kwargs = {
            "model": model_id,
            "prompt": final_prompt,
            "config": genai.types.GenerateVideosConfig(
                number_of_videos=1,
                aspect_ratio=prompt_data.get('output', {}).get('aspect_ratio', "9:16"),
            )
        }
        
        if input_file:
            kwargs["input_file"] = input_file

        operation = client.models.generate_videos(**kwargs)
        
        while not operation.done:
            print(f"Generating video with {model_id}... polling status...")
            time.sleep(15)
            operation = client.operations.get(operation)
            
        video = operation.response.generated_videos[0].video
        
        os.makedirs(os.path.dirname(os.path.abspath(output_file_path)), exist_ok=True)
        with open(output_file_path, 'wb') as f:
            f.write(video.video_bytes)
            
        print(f"Success! Video saved to: {output_file_path}")
        return True
    except Exception as e:
        print(f"Error during Vertex generation: {e}")
        return False

def generate_video_kling(prompt_data, output_file_path, image_path=None, model_id="kling-v1.5"):
    ak = os.environ.get("KLING_ACCESS_KEY")
    sk = os.environ.get("KLING_SECRET_KEY")
    
    if not ak or not sk:
        print("Error: KLING_ACCESS_KEY or KLING_SECRET_KEY is not set.")
        return False

    token = encode_kling_jwt(ak, sk)
    
    # Determine if text2video or image2video
    mode_url = "text2video" if not image_path else "image2video"
    url = f"https://api.klingai.com/v1/videos/{mode_url}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Prompt construction
    subject_details = prompt_data.get('subject', {}).get('appearance', '')
    if not subject_details:
        subject_details = prompt_data.get('subject', {}).get('identity', '')
        
    kling_prompt = f"{prompt_data.get('task', '')}. Subject: {subject_details}. "
    kling_prompt += f"Action: {prompt_data.get('subject', {}).get('movement_timeline', [{}])[0].get('action', '')}. "
    kling_prompt += f"Environment: {prompt_data.get('environment', {}).get('location', '')}. "
    kling_prompt += f"Cinematography: {prompt_data.get('cinematography', {}).get('camera_motion', '')}."
    
    negative_prompt_data = prompt_data.get('negative_prompt', {}).get('forbidden_elements', [])
    negative_prompt = ", ".join(negative_prompt_data) if negative_prompt_data else ""

    payload = {
        "model_name": model_id,
        "prompt": kling_prompt,
        "negative_prompt": negative_prompt,
        "aspect_ratio": prompt_data.get('output', {}).get('aspect_ratio', "9:16"),
        "duration": "5",
        "mode": "std"
    }

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
            payload["image"] = image_data

    print(f"Submitting {mode_url} task to Kling AI...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"Kling API Error (HTTP {response.status_code}): {response.text}")
            return False
            
        res_json = response.json()
        task_id = res_json.get("data", {}).get("task_id")
        
        if not task_id:
            print(f"Failed to get task ID from Kling. Response: {res_json}")
            return False

        print(f"Task created: {task_id}. Polling for result...")
        
        # Polling
        status_url = f"https://api.klingai.com/v1/videos/{mode_url}/{task_id}"
        max_attempts = 60 # 20 minutes approx
        attempts = 0
        
        while attempts < max_attempts:
            res = requests.get(status_url, headers=headers)
            if res.status_code != 200:
                 print(f"Polling error (HTTP {res.status_code}): {res.text}")
                 time.sleep(20)
                 attempts += 1
                 continue
                 
            data = res.json().get("data", {})
            status = data.get("task_status")
            
            if status == "succeed":
                print(f"Debug: Full Kling Response Data: {json.dumps(data, indent=2)}")
                # Correct path based on debug output
                videos = data.get("task_result", {}).get("videos", [])
                video_url = videos[0].get("url") if videos else None
                
                if video_url:
                    print(f"Generation successful! Downloading video...")
                    video_res = requests.get(video_url)
                    video_res.raise_for_status()
                    
                    os.makedirs(os.path.dirname(os.path.abspath(output_file_path)), exist_ok=True)
                    with open(output_file_path, 'wb') as f:
                        f.write(video_res.content)
                    print(f"Success! Video saved to: {output_file_path}")
                    return True
                else:
                    print("Error: Task succeeded but no video URL found.")
                    return False
            elif status == "failed":
                print(f"Task failed on Kling side: {data.get('task_status_msg')}")
                return False
            
            print(f"Still generating (Status: {status})...")
            time.sleep(20)
            attempts += 1
            
        print("Timeout reached while waiting for Kling AI.")
        return False
            
    except Exception as e:
        print(f"Error during Kling AI generation: {e}")
        return False
            
    except Exception as e:
        print(f"Error during Kling AI generation: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-model video generation script")
    parser.add_argument("--prompt", required=True, help="Path to the JSON prompt file")
    parser.add_argument("--output", required=True, help="Path for the output video file")
    parser.add_argument("--image", help="Optional path to source image for Image-to-Video")
    parser.add_argument("--model", default="veo-standard", choices=["veo-standard", "veo-fast", "kling", "kling-v3-0", "kling-v2-6", "kling-v1-5", "kling-image"], help="Choice of generation model")
    
    args = parser.parse_args()
    
    try:
        with open(args.prompt, 'r') as f:
            prompt_data = json.load(f)
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        exit(1)

    success = False
    if args.model == "veo-standard":
        success = generate_video_vertex(prompt_data, args.output, "veo-3.1-generate-preview", args.image)
    elif args.model == "veo-fast":
        success = generate_video_vertex(prompt_data, args.output, "veo-3.1-fast-generate-preview", args.image)
    elif args.model == "kling" or args.model == "kling-v1-5":
        success = generate_video_kling(prompt_data, args.output, args.image, "kling-v1-5")
    elif args.model == "kling-v3-0":
        success = generate_video_kling(prompt_data, args.output, args.image, "kling-v3")
    elif args.model == "kling-v2-6":
        success = generate_video_kling(prompt_data, args.output, args.image, "kling-v2-6")
    elif args.model == "kling-image":
        # Note: Kling image generation might require a different endpoint or payload, 
        # but for now we follow the existing pattern using image2video or similar if supported.
        # This acts as a placeholder or basic implementation for the image series model.
        success = generate_video_kling(prompt_data, args.output, args.image, "kling-image-v3.0")
    
    if success:
        print("Process completed successfully.")
    else:
        print("Process failed.")
        exit(1)
