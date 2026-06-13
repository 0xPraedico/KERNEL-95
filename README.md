---
title: KERNEL-95 - The Last Desktop
emoji: 🖥️
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
---

# KERNEL-95: The Last Desktop

KERNEL-95 is a single-player forensic horror game presented as a recovered
computer from 2077. Connect MIRROR.exe, investigate the hidden AI ECHO, verify
every claim with deterministic tools, and submit a final judgment.

The exact player guide is in [HOW_TO_PLAY.md](HOW_TO_PLAY.md).

## Core Game

- A movable late-1990s desktop inside a CRT.
- A large pink MIRROR terminal for commands and conversation.
- Clickable files, deleted evidence, restore points, and a hidden partition.
- Deterministic Python tools own facts, unlocks, progression, and endings.
- MIRROR and ECHO can use an optional OpenAI-compatible model for voice.
- The full game works without a model or API key.
- The World Cup shortcut uses live fixtures with browser-local mock predictions.
  It has no account or remote persistence.

## Quick Demo

1. Click **CONNECT MIRROR.exe**.
2. Open `CASE_013_BRIEFING.txt`.
3. Ask MIRROR about ECHO.
4. Recover `echo_letter_01.tmp` from the Recycle Bin.
5. Challenge MIRROR twice and run two contradiction scans.
6. Compare restore points or run `verify mirror`.
7. Run `audit mirror`, then `unlock hidden_partition`.
8. Inspect ECHO's files and submit the Final Judgment.

Useful terminal commands:

```text
help
status
dir
type CASE_013_BRIEFING.txt
recover echo_letter_01.tmp
run contradiction_scan
trace echo
compare restore_points
verify mirror
audit mirror
unlock hidden_partition
listen echo
```

## Local Run

Python 3.10 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:7860>.

Verification:

```bash
python -m compileall .
python smoke_test.py
ruff check app.py neon_trace smoke_test.py
```

## Hugging Face Space

The default deployment is a standard CPU Gradio Space. It does not require a
GPU, Modal, or an API key.

1. Create a new Hugging Face Space with the **Gradio** SDK.
2. Push this repository to the Space.
3. Set these Space variables:

```text
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

4. Leave the following secrets empty for deterministic fallback mode:

```text
OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=
```

The app launches and remains fully playable when `OPENAI_API_KEY` is absent.
If a configured model endpoint fails or times out, narration automatically
returns to authored deterministic responses. Model output cannot create
evidence, change unlocks, or select an ending.

## Modal vLLM backend

The Hugging Face Space runs the KERNEL-95 game UI. Modal runs
`Qwen/Qwen3-14B` behind vLLM's OpenAI-compatible API. The model only supplies
MIRROR/ECHO voice; deterministic tools remain authoritative and model output
cannot mutate `GameState`.

Create a local environment:

```bash
conda create -n kernel95-modal python=3.11 -y
conda activate kernel95-modal
python -m pip install "modal>=1.0.0" openai
python -m modal setup
```

Create the Modal secret used by `modal_vllm.py`. Choose a private API key and
reuse exactly the same value in the Hugging Face Space:

```bash
export KERNEL95_MODAL_API_KEY="replace-with-a-long-random-value"
modal secret create kernel95-modal-api-key \
  KERNEL95_MODAL_API_KEY="$KERNEL95_MODAL_API_KEY"
```

Deploy the vLLM server:

```bash
modal deploy modal_vllm.py
```

Modal returns an HTTPS endpoint after deployment. Use its `/v1` path as the
OpenAI base URL:

```text
https://<modal-endpoint>/v1
```

Set these Hugging Face Space secrets:

```text
OPENAI_API_KEY=<same api key used by Modal>
OPENAI_BASE_URL=https://<modal-endpoint>/v1
OPENAI_MODEL=Qwen/Qwen3-14B
```

Test the deployed endpoint with the same variables in your local shell:

```bash
python test_modal_endpoint.py
```

The Modal deployment uses an L40S GPU, a persistent `kernel95-hf-cache` volume,
and scales to zero after five idle minutes. A cold request may therefore take
longer while the container starts. If Modal fails, times out, or is asleep,
KERNEL-95 falls back to deterministic authored responses and remains fully
playable without `OPENAI_API_KEY`.

## Optional Debug Easter Eggs

Debug-only prototype shortcuts, including Tetris, are hidden from normal
players and demos. They can be restored only for local development:

```bash
KERNEL95_DEBUG_EASTER_EGGS=1 python app.py
```

## Project Layout

```text
app.py
neon_trace/
  game_state.py
  os_data.py
  os_actions.py
  os_tools.py
  os_desktop.py
  ai_engine.py
  styles.py
smoke_test.py
HOW_TO_PLAY.md
```
