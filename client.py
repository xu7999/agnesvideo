"""
Agnes AI SDK - Complete client for all Agnes models
Models: agnes-1.5-flash, agnes-2.0-flash, agnes-video-v2.0, agnes-image-2.1-flash, agnes-image-2.0-flash
API Base: https://apihub.agnes-ai.com
"""

import os
import time
import requests
from typing import Optional, List, Union


class AgnesClient:
    """Unified client for all Agnes AI models."""

    BASE_URL = "https://apihub.agnes-ai.com"
    
    MODELS = {
        "chat": ["agnes-1.5-flash", "agnes-2.0-flash"],
        "video": ["agnes-video-v2.0"],
        "image": ["agnes-image-2.1-flash", "agnes-image-2.0-flash"],
    }
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("AGNES_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set AGNES_API_KEY env var or pass to constructor."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        })

    # ========== CHAT ==========
    
    def chat_completion(
        self,
        model="agnes-1.5-flash",
        messages=None,
        max_tokens=1024,
        temperature=0.7,
        stream=False,
    ):
        """OpenAI-compatible chat completion."""
        if messages is None:
            messages = []
        resp = self.session.post(
            self.BASE_URL + "/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": stream,
            }
        )
        resp.raise_for_status()
        return resp.json()

    # ========== VIDEO ==========
    
    def create_video_task(
        self,
        prompt,
        model="agnes-video-v2.0",
        image=None,
        extra_images=None,
        mode=None,
        height=768,
        width=1152,
        num_frames=121,
        frame_rate=24.0,
        num_inference_steps=30,
        seed=None,
        negative_prompt=None,
    ):
        """Create a video generation task."""
        payload = {
            "model": model,
            "prompt": prompt,
            "height": height,
            "width": width,
            "num_frames": num_frames,
            "frame_rate": frame_rate,
            "num_inference_steps": num_inference_steps,
        }
        if image:
            payload["image"] = image
        if extra_images:
            payload["extra_body"] = {"image": extra_images}
        if mode:
            if "extra_body" not in payload:
                payload["extra_body"] = {}
            payload["extra_body"]["mode"] = mode
        if seed is not None:
            payload["seed"] = seed
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        resp = self.session.post(self.BASE_URL + "/v1/videos", json=payload)
        resp.raise_for_status()
        return resp.json()

    def poll_video_result(self, video_id, model_name=None, interval=5.0, timeout=300.0):
        """Poll for video result with retry on rate limit."""
        params = {"video_id": video_id}
        if model_name:
            params["model_name"] = model_name
        
        start = time.time()
        while time.time() - start < timeout:
            try:
                resp = self.session.get(self.BASE_URL + "/agnesapi", params=params)
                resp.raise_for_status()
                result = resp.json()
                status = result.get("status", "")
                progress = result.get("progress", 0)
                
                if status == "completed":
                    return result
                elif status == "failed":
                    err = result.get("error", {})
                    raise RuntimeError("Video generation failed: " + str(err))
                elif status in ("queued", "in_progress"):
                    time.sleep(interval)
                else:
                    return result
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    remaining = timeout - (time.time() - start)
                    wait = min(20, max(1, remaining))
                    time.sleep(wait)
                else:
                    raise
            except requests.exceptions.ConnectionError:
                time.sleep(5)
        
        raise TimeoutError("Video generation timed out after " + str(timeout) + "s")

    def generate_video(self, prompt, image=None, extra_images=None, mode=None, **kwargs):
        """Create video task and wait for completion."""
        task = self.create_video_task(prompt=prompt, image=image, extra_images=extra_images, mode=mode, **kwargs)
        video_id = task.get("video_id")
        print("Task created. video_id=" + str(video_id))
        return self.poll_video_result(video_id=video_id)

    # ========== IMAGE GENERATION ==========
    
    def generate_image(self, prompt, model="agnes-image-2.1-flash", size="1024x1024", n=1):
        """Generate images using OpenAI-compatible endpoint."""
        resp = self.session.post(
            self.BASE_URL + "/v1/images/generations",
            json={
                "model": model,
                "prompt": prompt,
                "size": size,
                "n": n,
            }
        )
        resp.raise_for_status()
        return resp.json()

    # ========== UTILITIES ==========
    
    def list_models(self):
        """List all available models."""
        resp = self.session.get(self.BASE_URL + "/v1/models")
        resp.raise_for_status()
        return resp.json()


# Example usage
if __name__ == "__main__":
    client = AgnesClient()
    
    # List models
    models = client.list_models()
    print("Available models:")
    for m in models.get("data", []):
        print("  - " + m["id"])
    
    # Chat
    chat = client.chat_completion(
        model="agnes-1.5-flash",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print("Chat response:", chat["choices"][0]["message"]["content"])
