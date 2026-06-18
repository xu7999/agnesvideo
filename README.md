# Agnes AI Video SDK

> **Open-source Python SDK for Agnes AI** — Chat, Image, and Video generation via a single unified client.

---

## Overview

Agnes AI Video SDK is a lightweight Python client that provides access to **Agnes AI**'s suite of generative models. It offers an **OpenAI-compatible** interface for Chat and Image endpoints, plus a built-in async polling system for Video generation.

**What you can do:**
- 💬 **Chat** — Text conversations with agnes-1.5-flash and agnes-2.0-flash
- 🎨 **Image Generation** — Create images with agnes-image-2.1-flash and agnes-image-2.0-flash
- 🎬 **Video Generation** — Text-to-Video, Image-to-Video, Multi-Image, and Keyframe Animation with agnes-video-v2.0

No complex setup. Just install, set your API key, and start generating.

---

## Quick Start

### 1. Install

```bash
pip install requests
```

### 2. Set your API key

```bash
# Linux / macOS
export AGNES_API_KEY="your-api-key-here"

# Windows PowerShell
$env:AGNES_API_KEY="your-api-key-here"
```

Or pass it directly in code:

```python
from client import AgnesClient
client = AgnesClient(api_key="your-api-key-here")
```

### 3. Generate your first video

```python
from client import AgnesClient

client = AgnesClient()

result = client.generate_video(
    prompt="A majestic view of the Great Wall of China at sunrise, cinematic wide-angle shot",
    width=1152,
    height=768,
    num_frames=241,
    frame_rate=24,
)
print("Video URL:", result["output_url"])
```

---

## Available Models

| Model | Type | Description |
|-------|------|-------------|
| `agnes-1.5-flash` | Chat | Fast, efficient chat model |
| `agnes-2.0-flash` | Chat | Improved chat model |
| `agnes-video-v2.0` | Video | Video generation (Text/Image-to-Video) |
| `agnes-image-2.1-flash` | Image | Latest image generation model |
| `agnes-image-2.0-flash` | Image | Previous image generation model |

---

## Usage Examples

### Chat

```python
result = client.chat_completion(
    model="agnes-1.5-flash",
    messages=[{"role": "user", "content": "Write a haiku about code."}],
    max_tokens=128,
    temperature=0.7,
)
print(result["choices"][0]["message"]["content"])
```

### Image Generation

```python
result = client.generate_image(
    model="agnes-image-2.1-flash",
    prompt="A serene Japanese garden at twilight, koi pond reflecting lanterns",
    size="1024x1024",
)
print(result["data"][0]["url"])
```

### Image-to-Video

```python
result = client.generate_video(
    prompt="The woman slowly turns around and looks back at the camera, cinematic camera movement",
    image="https://example.com/photo.png",
    width=1152,
    height=768,
)
```

### Keyframe Animation

```python
result = client.generate_video(
    prompt="Generate a smooth cinematic transition between the keyframes",
    extra_images=["https://example.com/kf1.png", "https://example.com/kf2.png"],
    mode="keyframes",
)
```

---

## API Reference

| Method | Parameters | Description |
|--------|------------|-------------|
| `chat_completion(model, messages, max_tokens, temperature, stream)` | OpenAI-compatible | Chat completions |
| `generate_image(prompt, model, size, n)` | OpenAI-compatible | Image generation |
| `generate_video(prompt, image, extra_images, mode, width, height, num_frames, frame_rate, num_inference_steps, seed, negative_prompt)` | Custom async | Video generation with auto-polling |
| `list_models()` | — | List all available models |

---

## Video Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | **required** | Text description of the video |
| `image` | str | — | URL of reference image (Image-to-Video) |
| `extra_images` | list[str] | — | Array of image URLs (Multi-Image / Keyframe) |
| `mode` | str | — | Mode setting, e.g. `"keyframes"` |
| `width` | int | 1152 | Video width |
| `height` | int | 768 | Video height |
| `num_frames` | int | 121 | Frame count (must be 8n+1, ≤ 441) |
| `frame_rate` | float | 24 | FPS (1–60) |
| `num_inference_steps` | int | 30 | Inference steps |
| `seed` | int | — | Random seed for reproducibility |
| `negative_prompt` | str | — | Content to avoid |

### Duration Control

```
seconds = num_frames / frame_rate
```

| Target Duration | num_frames | frame_rate |
|-----------------|------------|------------|
| ~3 seconds | 81 | 24 |
| ~5 seconds | 121 | 24 |
| ~10 seconds | 241 | 24 |
| ~18 seconds | 441 | 24 |

---

## Getting an API Key

1. Visit [Agnes AI Platform](https://apihub.agnes-ai.com)
2. Register for an account
3. Generate an API key from your dashboard
4. Set `AGNES_API_KEY` environment variable or pass to `AgnesClient()`

---

## License

This project is provided as-is for educational and integration purposes.