---
title: NEON TRACE - The Last Desktop
emoji: 🖥️
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
hf_oauth: true
hf_oauth_expiration_minutes: 43200
---

# NEON TRACE: The Last Desktop

NEON TRACE is a single-player forensic horror game presented as a recovered
KERNEL-95 computer in 2077. Connect MIRROR.exe, investigate the hidden AI ECHO,
verify every claim with deterministic tools, and submit a final judgment.

The exact player guide is in [HOW_TO_PLAY.md](HOW_TO_PLAY.md).

## Core Game

- A movable late-1990s desktop inside a CRT.
- A large pink MIRROR terminal for commands and conversation.
- Clickable files, deleted evidence, restore points, and a hidden partition.
- Deterministic Python tools own facts, unlocks, progression, and endings.
- MIRROR and ECHO can use an optional OpenAI-compatible model for voice.
- The full game works without a model or API key.

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
NEON_TRACE_DEMO=1
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

Optional Hugging Face OAuth variables used by debug-only experiments are not
required for the main game.

## Optional Modal vLLM

Modal/vLLM support is planned as an optional narration backend. It is not
required to launch the Space.

For a future OpenAI-compatible Modal endpoint:

```text
OPENAI_API_KEY=your-endpoint-key
OPENAI_BASE_URL=https://your-modal-endpoint.example/v1
OPENAI_MODEL=Qwen/Qwen2.5-14B-Instruct
```

Start with `Qwen/Qwen2.5-14B-Instruct`. Keep the Hugging Face Space on CPU; the
remote Modal service owns model inference. The endpoint must expose an
OpenAI-compatible `/v1/chat/completions` route.

## Optional Debug Easter Eggs

Debug-only prototype shortcuts, including Tetris, are hidden from normal
players and demos. They can be restored only for local development:

```bash
NEON_TRACE_DEBUG_EASTER_EGGS=1 python app.py
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
