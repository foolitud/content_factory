import json
import os

def generate_viral_leak_prompt(agent_name, evidence_type, location):
    """
    Generates a structured JSON prompt for a 'viral leak' video
    following the Video Generation Master skill guidelines.
    """
    
    prompt_structure = {
        "task": f"viral_leak_{evidence_type}",
        "output": {
            "type": "single_clip",
            "duration": "6_seconds",
            "framerate": "24fps_cinematic",
            "resolution": "1080p",
            "aspect_ratio": "9:16"  # Optimized for TikTok/Stories
        },
        "cinematography": {
            "camera_motion": "handheld_shaky_cam_first_person_perspective",
            "lens_and_focus": "wide_angle_smartphone_lens",
            "simulation": {
                "motion_blur": "natural_180_degree_shutter",
                "noise_over_time": "digital_sensor_noise_iso_6400"
            }
        },
        "subject": {
            "type": "evidence_artifact",
            "appearance": f"A grainy, high-contrast video of a {evidence_type} sitting on a {location}. A small 'Parallel' logo sticker is partially visible.",
            "movement_timeline": [
                {
                    "timeframe": "0s-3s",
                    "action": "Camera shakes slightly as someone's hand reaches out to touch the artifact."
                },
                {
                    "timeframe": "3s-6s",
                    "action": "Lighting flickers as if from a faulty overhead light. The hand quickly pulls back."
                }
            ]
        },
        "environment": {
            "location": f"A dimly lit, messy {location} room with blueprint papers on the walls.",
            "lighting": {
                "type": "flickering_cold_led",
                "changes_over_time": "Rapid flickering at 4.5 seconds."
            }
        },
        "structural_preservation": {
            "temporal_consistency": [
                "The artifact geometry must remain rigid",
                "Hand movement must follow human kinetics",
                "Lighting flicker must affect all surfaces consistently"
            ]
        },
        "negative_prompt": {
            "forbidden_elements": [
                "morphing, melting, extra limbs, plastic skin, CGI look, bright saturated colors, steady camera"
            ]
        }
    }
    
    return prompt_structure

# Example generation
if __name__ == "__main__":
    agent = "Lolo"
    evidence = "glowing mysterious briefcase"
    loc = "abandoned warehouse office"
    
    viral_prompt = generate_viral_leak_prompt(agent, evidence, loc)
    
    # Save to prompts/viral/ for later use
    os.makedirs("/Users/loloamoravain/antigravity/content_factory/prompts/viral", exist_ok=True)
    filename = f"/Users/loloamoravain/antigravity/content_factory/prompts/viral/leak_{evidence.replace(' ', '_')}.json"
    
    with open(filename, "w") as f:
        json.dump(viral_prompt, f, indent=2)
        
    print(f"Viral Artifact Prompt generated and saved to: {filename}")
    print(json.dumps(viral_prompt, indent=2))
