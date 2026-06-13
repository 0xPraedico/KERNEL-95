"""Send a small MIRROR request to the configured Modal vLLM endpoint."""

from __future__ import annotations

import os

from openai import OpenAI


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    base_url = required_env("OPENAI_BASE_URL").rstrip("/")
    if not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"
    api_key = required_env("OPENAI_API_KEY")
    model = required_env("OPENAI_MODEL")

    print(
        f"Calling {model} at {base_url} "
        "(the first Modal cold start can take several minutes)...",
        flush=True,
    )
    client = OpenAI(base_url=base_url, api_key=api_key, timeout=600.0)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are MIRROR.exe, the terse forensic AI in KERNEL-95. "
                    "Do not invent evidence."
                ),
            },
            {
                "role": "user",
                "content": "Confirm the link in one short sentence.",
            },
        ],
        max_tokens=80,
        temperature=0.4,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    content = response.choices[0].message.content
    if not content:
        raise SystemExit("The endpoint returned an empty model response.")
    print(content.strip())


if __name__ == "__main__":
    main()
