# Kling AI Master Reference & Model Catalog

This guide provides the technical specifications, pricing, and best practices for the Kling AI video generation models.

## Model Catalog

| Model Name | Version | Best For | Estimated Cost | Mode Support |
| :--- | :--- | :--- | :--- | :--- |
| Model Name | Version | Best For | Estimated Cost | Mode Support |
| :--- | :--- | :--- | :--- | :--- |
| **Kling AI 3.0 Pro** | `kling-v3` | AI Director, multi-shot consistency, native audio | ~$0.15 / sec | `std`, `pro` |
| **Kling VIDEO 2.6** | `kling-v2-6` | Precise motion control, voice commands | ~$0.10 / sec | `std`, `pro` |
| **Kling AI 2.1** | `kling-v2-1-master` | High-fidelity 1080p, legacy pro | ~$0.08 / sec | `pro` |
| **Kling v1.5 Master** | `kling-v1-5` | Hyper-realistic humans, complex physics | ~$0.05 / sec | `std`, `pro` |
| **Kling IMAGE 3.0** | `kling-image-v3.0`| 4K Cinematic images, series mode | ~$0.02 / image | N/A |

### Mode Characteristics
- **`std` (Standard):** Fast generation, lower cost. Ideal for most TikTok/Reels content.
- **`pro` (Professional):** Higher visual fidelity, better consistency, but slower and 2-3x more expensive.

---

## Technical Specifications

### Video Formats
- **Aspect Ratios:** `16:9`, `9:16`, `1:1`.
- **Duration:** 5 seconds or 10 seconds.
- **Resolution:** Up to 1080p.

### Image-to-Video (I2V)
When using an image as a starting point, Kling excels at preserving the identity of the subject.
- **Parameters:** Requires an `image_url` or base64 data.
- **Best Practice:** The prompt should describe the *action* and *camera movement* rather than re-describing the subject in detail.

---

## Universal Prompting Formula for Kling

**[Action Description] + [Cinematography] + [Environment Details] + [Lighting]**

### Text-to-Video (T2V) Example
`"A majestic dragon landing on a snowy mountain peak, slow cinematic drone orbit. Heavy snow particles, sunset lighting casting orange glows on scales."`

### Image-to-Video (I2V) Example
`"The woman in the photo begins to smile and turns her head toward the camera. Soft focus background, warm golden hour lighting."`

---

## Negative Prompting Stack
To ensure maximum realism, always include the following in the `forbidden_elements`:
`"morphing, melting geometry, extra limbs appearing, impossible physics, jittery background, plastic skin, beautification filters, anime style, CGI rendering, inconsistent lighting between frames"`
