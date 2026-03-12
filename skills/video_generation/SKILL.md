name: Video Generation Master
description: A formalized skill for generating hyper-realistic, highly-controlled videos using multiple models (Google Veo, Kling AI) through parameterized JSON prompting.
---

# Video Generation Master

## Goal
The purpose of this skill is to provide a standardized, highly controlled method for generating videos using AI video models (such as Veo connected to Anti-Gravity). By strictly enforcing a structured JSON parameter schema, this skill neutralizes native model biases (like temporal morphing, unnatural physics, or "plastic" AI styling) and ensures raw, unretouched, hyper-realistic video outputs with deliberate cinematic control.

## Prerequisites
- Access to the video generation tool (e.g., Veo or `generate_video`).
- A clear understanding of the user's desired Subject, Lighting, Camera characteristics, and Temporal Timeline.

## Core Schema Structure
When constructing a prompt for the video generation tool, you **MUST** use the following JSON schema as the foundation. Fill in the string values with extreme, microscopic detail, paying special attention to how elements change over time.

```json
{
  "task": "string - High-level goal (e.g., 'sports_action_clip', 'macro_nature_timelapse')",
  
  "output": {
    "type": "string - e.g., 'single_clip', 'looping_background'",
    "duration": "string - e.g., '5_seconds', '10_seconds'",
    "framerate": "string - e.g., '24fps_cinematic', '60fps_smooth_action'",
    "resolution": "string - e.g., '1080p', '4K'",
    "aspect_ratio": "string - e.g., '16:9', '9:16', '1:1'"
  },

  "cinematography": {
    "camera_motion": "string - e.g., 'static_tripod', 'smooth_drone_tracking_forward', 'handheld_shaky_cam_following_subject', 'slow_pan_right_to_left'",
    "lens_and_focus": "string - e.g., '85mm_lens', 'macro_lens_focus_pull_from_foreground_to_background'",
    "dynamic_range": "string - e.g., 'hdr_capable', 'limited'",
    "simulation": {
      "motion_blur": "string - e.g., 'natural_180_degree_shutter', 'crisp_no_motion_blur'",
      "noise_over_time": "string - e.g., 'consistent_film_grain_across_frames'"
    }
  },

  "subject": {
    "type": "string - e.g., 'human_actor', 'vehicle_in_motion', 'weather_element'",
    "appearance": "string - Extremely specific physical details (e.g., visible pores, brushed metal). Needs to remain consistent across frames.",
    "movement_timeline": [
      {
        "timeframe": "string - e.g., '0s-2s'",
        "action": "string - e.g., 'Subject stands still looking slightly off-camera'"
      },
      {
        "timeframe": "string - e.g., '2s-5s'",
        "action": "string - e.g., 'Subject turns head rapidly towards the lens, hair swishing naturally'"
      }
    ]
  },

  "environment": {
    "location": "string - e.g., 'dimly lit urban alleyway'",
    "background_dynamics": "string - What changes in the background? (e.g., 'cars driving past in soft focus', 'wind blowing leaves')",
    "lighting": {
      "type": "string - e.g., 'flickering neon sign', 'steady overcast daylight'",
      "changes_over_time": "string - e.g., 'lighting remains constant', 'cloud passes over sun at 3s causing a shadow drop'"
    }
  },

  "structural_preservation": {
    "temporal_consistency": [
      "array of strings - e.g., 'Subject facial features must not morph', 'Clothing folds must move naturally with physics', 'No physics-defying liquid behavior'"
    ]
  },

  "negative_prompt": {
    "forbidden_elements": [
      "array of strings - Massive list of 'AI video' blockers required for extreme realism. Example stack: 'morphing, melting geometry, extra limbs appearing, impossible physics, jittery background, plastic skin, beautification filters, anime style, CGI rendering, inconsistent lighting between frames'."
    ]
  }
}
```

## Paradigm 2: The Dense Cinematic Narrative (Optimized for standard APIs/Tools)
When executing API calls or standard generation endpoints that accept a single string prompt, condense the logic above into a dense, flat JSON string containing a massive descriptive text block.

```json
{
  "prompt": "string - A dense, ultra-descriptive cinematic narrative. Define camera movement explicitly (Handheld tracking shot moving backward). Dictate temporal actions (Subject turns head at 2 seconds). Detail lighting (Flickering overhead fluorescent light). Include direct negative commands (Do not morph geometry, preserve physical consistency).",
  "negative_prompt": "string - A comma-separated list of explicit realism blockers (no plastic skin, no CGI, no melting, no unnatural physics).",
  "video_input": [
    "array of strings (URLs) - Optional. Input images/videos to animate or use as reference."
  ],
  "settings": {
    "duration": "string",
    "resolution": "string",
    "aspect_ratio": "string",
    "camera_motion": "string"
  }
}
```

## Best Practices & Cinematography Hacks

1.  **Define Camera Physics:** Don't just say "cool shot." Explicitly define the camera rig: `steadycam tracking backward`, `drone orbit`, or `static locked-off tripod`.
2.  **Temporal Action is Key:** Video is about change over time. If you don't define what moves, the model might make everything move unnaturally or nothing at all. Use phrases like `wind subtly moves the trees in the background while the main subject remains perfectly still`.
3.  **Prevent Morphing:** The biggest issue with AI video is objects losing structural integrity across frames. Add strong negative constraints like `no morphing`, `maintain volume`, and `rigid physical consistency`.
4.  **Lighting Dynamics:** Explain if lighting changes. `A passing car casts sweeping headlights across the subject's face.`
5.  **Mandatory Negative Stack:** You MUST include the extensive negative prompt block (e.g., forbidding "melting" and "jittering artifacts").

## Master Reference Guide
If you require the absolute full schema breakdown, parameter options, or complex timeline structuring, refer to the root project document:
`master_prompt_reference.md`

## Brand & Project Context
When working on projects for **Parallel Adventure**, refer to the core DNA document:
- [Parallel Adventure DNA](file:///Users/loloamoravain/antigravity/content_factory/references/parallel_adventure_dna.md)

> [!IMPORTANT]
> Always ask the user: *"Should I base this work on the Parallel Adventure DNA references?"* before applying these principles.

## How to use this skill
When a user asks you to generate a highly detailed, realistic video, you **MUST** first ask them which model they would like to use, providing the estimated pricing/characteristics:
1.  **Google Veo 3.1 Standard** (~0.75$/s) - Highest quality, best adherence.
2.  **Google Veo 3.1 Fast** (~0.15$/s) - Much faster and cheaper, slightly less detailed.
3.  **Kling AI 3.0 Pro** (~$0.15/sec) - `kling-v3`. AI Director, multi-shot, native audio.
4.  **Kling AI 2.6** (~$0.10/sec) - `kling-v2-6`. Motion control, realistic physics.
5.  **Kling AI 1.5** (~$0.05/sec) - `kling-v1-5`.

Once the user has chosen, construct the prompt JSON and call the generation script with the appropriate `--model` flag:
- `--model veo-standard`
- `--model veo-fast`
- `--model kling-v3-0` (maps to `kling-v3`)
- `--model kling-v2-6`
- `--model kling-v1-5`
- `--model kling-image`

Pass that entire JSON string as the `Prompt` argument to the video generation tool (like Veo).

**IMPORTANT POST-GENERATION STEP:**
When calling the video generation script/tool, you MUST pass the `--output` argument pointing directly to the project's `/videos/[category]/` directory (e.g., `videos/tiktok/video_1_output.mp4`), NOT the `/prompts/` directory. If the tool saves to a temporary location by default, you must immediately move or copy the generated video file (.mp4, .webm, etc.) into the `/videos/[category]/` directory. 

Additionally, you must save the JSON prompt used to generate the video into the corresponding `/prompts/[category]/` directory (e.g., `prompts/tiktok/` or `prompts/cinematics/`). Refer to `studio_manager.md` for full project structure rules.
