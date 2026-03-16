# Multi-Model Video Studio - Project Organizer

This document tracks our progress, generated assets, and custom scripts for the multi-model video generation project using Anti-Gravity, Google Veo, and Kling AI.

## Project Structure

It is critical to **always keep assets organized** within the project directory.

- `/videos/` - All generated videos (.mp4) saved by category (e.g., `/videos/tiktok/`, `/videos/cinematics/`).
- `/images/` - Source images used for Image-to-Video generation (e.g., `/images/subjects/`).
- `/prompts/` - Saved JSON prompt configurations corresponding to the generated videos.
- `/scripts/` - Utility scripts (`generate_video.py`).
- `master_prompt_reference.md` - Veo / General prompting guide.
- `kling_master_reference.md` - Kling specific catalog and best practices.

## Video Generation Workflow

1. **Model Selection:** The AI Agent MUST present the available models (Veo vs Kling) and their costs/characteristics to the user.
2. **Prompt Engineering:** Use the appropriate Master Reference (`master_prompt_reference.md` or `kling_master_reference.md`) to build the JSON prompt.
3. **Execution:** Run `generate_video.py` with the correct `--model` and (optionally) `--image` flags.
4. **Filing:** 
   - Move video to `/videos/[category]/`.
   - Save JSON prompt to `/prompts/[category]/`.
   - Ensure source images are copied to `/images/` if not already there.

## Current Phase: Kling I2V Integration

**Goal:** Implement and test the Image-to-Video capabilities of Kling AI using the new `--image` flag in our generation script. Validate the temporal consistency when animating a static subject.
