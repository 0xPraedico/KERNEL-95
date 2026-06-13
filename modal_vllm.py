"""Deploy Qwen3-14B on Modal behind an OpenAI-compatible vLLM API."""

from __future__ import annotations

import os
import subprocess

import modal

APP_NAME = "kernel95-qwen3-vllm"
MODEL_NAME = "Qwen/Qwen3-14B"
API_KEY_ENV = "KERNEL95_MODAL_API_KEY"
VLLM_PORT = 8000
MINUTES = 60

image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.9.0-devel-ubuntu22.04",
        add_python="3.12",
    )
    .entrypoint([])
    .uv_pip_install("vllm==0.21.0")
    .env(
        {
            "HF_HOME": "/root/.cache/huggingface",
            "HF_XET_HIGH_PERFORMANCE": "1",
        }
    )
)

app = modal.App(APP_NAME)
hf_cache = modal.Volume.from_name("kernel95-hf-cache", create_if_missing=True)
api_secret = modal.Secret.from_name("kernel95-modal-api-key")


@app.function(
    image=image,
    gpu="L40S",
    min_containers=0,
    max_containers=1,
    timeout=15 * MINUTES,
    scaledown_window=5 * MINUTES,
    volumes={"/root/.cache/huggingface": hf_cache},
    secrets=[api_secret],
)
@modal.concurrent(max_inputs=16)
@modal.web_server(port=VLLM_PORT, startup_timeout=15 * MINUTES)
def serve() -> None:
    """Start vLLM's OpenAI-compatible HTTP server."""
    api_key = os.getenv(API_KEY_ENV, "").strip()
    if not api_key:
        raise RuntimeError(
            f"Modal secret kernel95-modal-api-key must define {API_KEY_ENV}."
        )
    os.environ["VLLM_API_KEY"] = api_key

    command = [
        "vllm",
        "serve",
        MODEL_NAME,
        "--served-model-name",
        MODEL_NAME,
        "--host",
        "0.0.0.0",
        "--port",
        str(VLLM_PORT),
        "--max-model-len",
        "8192",
        "--gpu-memory-utilization",
        "0.90",
    ]
    subprocess.Popen(command)
