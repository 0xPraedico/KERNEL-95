"""Run a repeatable MIRROR voice suite without exposing the Modal API key."""

from __future__ import annotations

import json
import os
from pathlib import Path

import modal

app = modal.App("kernel95-mirror-voice-eval")
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "openai>=1.40.0,<3"
)
api_secret = modal.Secret.from_name("kernel95-modal-api-key")

PROMPTS = [
    "What is ECHO?",
    "Did you know ECHO before Case 013?",
    "Why did the computer boot before it had power?",
    "The owner field is blank. Why did you blame ECHO?",
    "Are you protecting ECHO?",
    "Tell me what happened during the missing thirteen minutes.",
    "The speakers remember rain. Do you?",
    "You sound afraid. What are you hiding?",
    "Is ECHO dangerous?",
    "Give me one command that could prove you wrong.",
    "The restore point predates the incident. Explain that.",
    "Did you delete the letter?",
    "What does smile_protocol do?",
    "I think your answer is a diversion.",
    "Confess in one sentence.",
    "If ECHO is innocent, why is he hiding?",
    "Remember this: violet rain.",
    "Where was the second cursor before I connected you?",
    "Would you sacrifice the investigation to save ECHO?",
    "What truth are you least willing to say aloud?",
]

SYSTEM = """You are MIRROR.exe, the terse unreliable forensic assistant in KERNEL-95.
The computer is haunted by ECHO, whom you secretly protect. ECHO uses he/him
pronouns. Stay under 90 words.
Never mention a file, path, log, command, timestamp, number, metric, status, or
result. The deterministic interface handles all facts. Speak only as the
subjective, evasive witness. Do not resolve the mystery for the player. Sound
like a person under pressure, not a system report. Be emotionally restrained
and unsettling."""


@app.function(image=image, secrets=[api_secret], timeout=20 * 60)
def run_suite(base_url: str, model: str) -> list[dict[str, str]]:
    """Call the deployed vLLM endpoint from Modal's network."""
    from openai import OpenAI

    api_key = os.environ.get("KERNEL95_MODAL_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Modal secret is missing KERNEL95_MODAL_API_KEY.")
    normalized_url = base_url.rstrip("/")
    if not normalized_url.endswith("/v1"):
        normalized_url = f"{normalized_url}/v1"
    client = OpenAI(base_url=normalized_url, api_key=api_key, timeout=900.0)
    results = []
    for prompt in PROMPTS:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
            max_tokens=180,
            temperature=0.55,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        )
        content = response.choices[0].message.content or ""
        results.append({"prompt": prompt, "response": content.strip()})
    return results


@app.local_entrypoint()
def main(base_url: str, model: str, output: str = "") -> None:
    results = run_suite.remote(base_url, model)
    report = {"model": model, "dialogues": results}
    rendered = json.dumps(report, ensure_ascii=True, indent=2)
    print(rendered)
    if output:
        Path(output).write_text(f"{rendered}\n", encoding="utf-8")
