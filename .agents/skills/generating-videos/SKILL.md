---
name: generating-videos
description: Generates hyper-realistic, highly-controlled videos using multiple models (Google Veo, Kling AI) through parameterized JSON prompting.
---

# Video Generation Master

## Goal
The purpose of this skill is to provide a standardized, highly controlled method for generating videos using AI video models (such as Veo connected to Antigravity). By strictly enforcing a structured JSON parameter schema, this skill ensures raw, unretouched, hyper-realistic video outputs with deliberate cinematic control.

## Prerequisites
- Access to the video generation tool (e.g., Veo or `generate_video`).
- A clear understanding of the subject, lighting, camera, and timeline.

## Core Schema Structure
When constructing a prompt for video generation, you **MUST** use the following JSON schema. Fill in string values with extreme detail, focusing on temporal changes.

```json
{
  "task": "string - High-level goal (e.g., 'sports_action_clip', 'macro_nature_timelapse')",
  
  "output": {
    "type": "string - e.g., 'single_clip', 'looping_background'",
    "duration": "string",
    "framerate": "string",
    "resolution": "string",
    "aspect_ratio": "string"
  },

  "cinematography": {
    "camera_motion": "string",
    "lens_and_focus": "string"
  }
}
```

## Best Practices
1.  **Define Camera Physics:** Use explicit rigs like `steadycam tracking backward` or `drone orbit`.
2.  **Temporal Action:** Define exactly what moves and when.
3.  **Prevent Morphing:** Use negative constraints like `no morphing` or `rigid physical consistency`.
4.  **Lighting Dynamics:** Explain any lighting changes over time.

## Execution
- **Models**: Provide the user with options (Veo Standard, Veo Fast, Kling V1.5/2.6/3.0) and their characteristics.
- **Paths**: Save videos to `videos/[category]/` and prompts to `prompts/[category]/`.
- **References**: See [Advanced Guide](resources/master_prompt_reference.md).

## How to use this skill
When a user asks to generate a video, confirm the desired model first, then construct the JSON prompt and execute the generation script with the appropriate model flag.
