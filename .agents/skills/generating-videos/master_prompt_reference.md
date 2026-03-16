# Veo Video - Master JSON Prompt Reference Guide

This guide defines the ultimate JSON schema for prompting the Veo video generation model (e.g., Veo). Using this structured format ensures high consistency, detailed cinematic control, and leverages the model's ability to interpret complex temporal instructions to prevent morphing and maintain physical integrity across frames.

## The JSON Schema

```json
{
  "prompt": "string - A dense, ultra-descriptive cinematic narrative merging subject, outfit, environment, and precise camera choreography over time. Use highly specific language to force temporal realism. (e.g., 'Ultra-realistic handheld tracking shot following a man walking down a rainy alleyway. Camera shakes slightly with footsteps. Focus is locked on his leather jacket dripping with water. Background is heavily blurred neon signs reflecting in puddles. Lighting changes as he walks past a flickering street lamp at second 3. Natural physics, rigid structural integrity. Do not morph geometry.')",
  
  "negative_prompt": "string - Comma-separated list of temporal and visual blockers (e.g., 'morphing, melting, impossible physics, extra limbs appearing, jittery background, plastic skin, cartoon, CGI, oversaturated, anatomy normalization, temporal fading, unmotivated camera movement')",
  
  "settings": {
    "duration": "string - e.g., '5s', '10s'",
    "resolution": "string - e.g., '1080p', '4k'",
    "framerate": "string - e.g., '24fps', '60fps'",
    "camera_motion": "string - e.g., 'static', 'pan left', 'drone orbit', 'crane down'",
    "lighting": "string - e.g., 'natural golden hour sweeping light', 'harsh overhead flickering'",
    "quality": "string - e.g., 'high detail cinematic, unretouched film grain', 'amateur smartphone footage'"
  }
}
```

## How to Use This Dual Paradigm

You have two core ways to construct a video prompt:

1.  **The Dense Cinematic Narrative (Classic API Paradigm):** Use the text-based `prompt` string when feeding a standard video model like Veo. **Cinematography Masterclass:** Dictate exact camera rigs (`handheld steadycam`, `static tripod`), describe action over time (`at 2 seconds, subject turns head rapidly`), detail lighting shifts, and include direct negative commands within the positive prompt (`Maintain rigid structural consistency`, `Do not morph`).
2.  **The Deep Timeline Grid (Advanced Constraints Paradigm):** Map out the video using complex JSON objects to explicitly state what happens over the timeline.

When sending data to the **Video API/Tool**, compile your choices into a single JSON object (using the Dense Narrative structure above).

```json
{
  "task": "string - High-level goal (e.g., 'sports_action_clip', 'nature_timelapse')",
  
  "output": {
    "type": "string - e.g., 'single_clip', 'loop'",
    "duration": "string - e.g., '5s'",
    "aspect_ratio": "string - e.g., '16:9'"
  },

  "cinematography": {
    "camera_motion": "string - e.g., 'smooth tracking shot pushing in on the subject'",
    "lens_and_focus": "string - e.g., 'rack focus from foreground leaf to background person at 2s'",
    "simulation": {
      "motion_blur": "string - e.g., 'heavy motion blur indicating high speed'"
    }
  },

  "subject": {
    "identity": "string - Specific identity or consistency tags.",
    "appearance": {
      "texture": "string - Highly specific, e.g., 'rain-soaked fabric adhering to skin'",
      "physics": "string - 'Hair blowing organically in wind, strict gravity simulation'"
    },
    "movement_timeline": [
      {
        "timeframe": "0s-2s",
        "action": "Subject is static, breathing lightly."
      },
      {
        "timeframe": "2s-5s",
        "action": "Subject suddenly sprints out of frame right."
      }
    ]
  },

  "environment": {
    "location": "string - e.g., 'gritty urban subway car'",
    "background_dynamics": "string",
    "lighting": {
      "type": "string - e.g., 'overhead strobing lights'",
      "changes_over_time": "string - e.g., 'lights flicker rapidly between second 1 and 3'"
    }
  },

  "structural_preservation": {
    "temporal_consistency": [
      "array of strings - e.g., 'Clothing folds must track consistently', 'No spontaneous appearance of objects'"
    ]
  },

  "negative_prompt": {
    "forbidden_elements": [
      "array of strings - Massive list of 'AI look' blockers required for extreme realism. Example stack: 'morphing, melting geometry, anatomy normalization, unmotivated jitter, physics-defying fabric, telekinetic object movement, plastic skin, airbrushed texture'."
    ]
  }
}
```

## How to Use This Template

This reference guide is designed to produce **hyper-realistic, temporally consistent videos**. When generating prompts for Veo Video:

1. **Choreograph the Camera:** AI video struggles if the camera floats aimlessly. Explicitly anchor the camera (e.g., "locked-off tripod shot") or define its exact trajectory ("slow tracking shot from left to right").
2. **Timeline the Action:** Don't just list elements. Say *when* they happen or how they move.
3. **Enforce Physics:** Use the `structural_preservation` Block to explicitly tell the model not to let things melt, morph, or ignore gravity.
4. **Heavily Populate the `negative_prompt`:** To combat "AI look," you must explicitly forbid "morphing," "melting," "jittering," and "anatomy normalization."
5. **Drop Unused Fields:** If the clip is static, omit timeline breakdown blocks to avoid confusing the parser.

## Best Practices for Veo Video Prompting

1.  **Start Small:** 5-second clips are vastly more stable than 10-second clips. Try to generate a perfect 5-second shot before extending.
2.  **Lock the Background:** If the action is fast, keep the camera static. Moving the camera while the subject is doing complex maneuvers often causes background artifacting.
3.  **High-Fidelity Textures:** State explicitly that textures must not degrade during motion (e.g., "maintain visible film grain and skin texture across rapid motion").
