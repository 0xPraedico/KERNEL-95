---
title: KERNEL-95 - The Last Desktop
emoji: 🖥️
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
tags:
  - track:wood
  - sponsor:openai
  - sponsor:modal
  - achievement:offbrand
  - achievement:tiny
---

# KERNEL-95: The Last Desktop

In 2077, you join the KERNEL-95 Recovery Division to investigate Device 013:
an obsolete computer recovered from a sealed MetroGrid Behavioral Lab archive.
It has no power source, yet it is still running. Three technicians who touched
it each lost exactly thirteen minutes of memory.

To enter the machine, you connect MIRROR.exe, your assigned forensic AI
assistant. Inside a corrupted retro desktop, you open files, recover deleted
messages, compare restore points, run contradiction scans, and search for ECHO:
an unknown intelligence hiding inside the system.

But MIRROR is not a neutral assistant. She diverts your questions, suppresses
evidence, and rewrites her own testimony because she is secretly protecting
ECHO.

KERNEL-95 is an AI-native forensic game where the model performs MIRROR's
evasions, ECHO's fragmented confessions, and the emotional tension between
them, while a deterministic investigation engine protects the actual truth.

At the end of Case 013, you decide whether to delete ECHO, extract him, expose
MIRROR, protect them both, or allow something impossible to survive inside the
last desktop.

The exact player guide is in [HOW_TO_PLAY.md](HOW_TO_PLAY.md).

## Social Post + Demo Video

Watch the KERNEL-95 demo and read the social post:
[x.com/praedico/status/2065889011139215517](https://x.com/praedico/status/2065889011139215517)

## OpenAI Codex Track

Public source repository:
[github.com/0xPraedico/KERNEL-95](https://github.com/0xPraedico/KERNEL-95)

KERNEL-95 was developed with OpenAI Codex as the coding agent. Codex-attributed
commits include the `Co-authored-by: OpenAI Codex <codex@openai.com>` trailer
in the public Git history.

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
5. Challenge MIRROR once and run one contradiction scan.
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
`Qwen/Qwen3-4B-Instruct-2507` behind vLLM's OpenAI-compatible API. The model only supplies
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
OPENAI_MODEL=Qwen/Qwen3-4B-Instruct-2507
```

Test the deployed endpoint with the same variables in your local shell:

```bash
python test_modal_endpoint.py
```

The Modal deployment keeps one L4 container warm, uses a persistent
`kernel95-hf-cache` volume, and caps the deployment at one replica. This avoids
the normal scale-to-zero delay for the first MIRROR message. At Modal's
published L4 rate of `$0.000222/second`, seven continuously warm days cost about
`$134.27` for the GPU, plus CPU and memory. If Modal fails or restarts,
KERNEL-95 falls back to deterministic authored responses and remains fully
playable without `OPENAI_API_KEY`.

### Why the AI is load-bearing

MIRROR is the unreliable witness; KERNEL-95 is the truth engine. For every
free-form question, deterministic case state secretly selects one performance
tactic: contradiction, diversion, or admission. Qwen performs that tactic using
the player's wording and recurring motifs. The player then classifies the
answer, and deterministic evidence decides whether the accusation is correct.

The model never receives authority to create evidence, unlock files, mutate
`GameState`, or choose an ending. It also does not narrate technical results.
Responses containing invented paths, filenames, timestamps, metrics, or command
results are discarded and replaced by the authored fallback.

### Model evaluation

`modal_voice_eval.py` runs the same 20 MIRROR prompts against a deployed model.
The selected 4B deployment had a roughly 97-second first cold start and
generally answered in 0.6-1.6 seconds warm.

The evaluation showed that generated technical reporting could invent details.
The final design therefore narrows the model's job to subjective roleplay while
the deterministic UI owns every fact. Under that voice-only protocol,
`Qwen/Qwen3-4B-Instruct-2507` retained the eerie MIRROR performance with much
lower warm latency, so it is the selected model.

Run the repeatable 20-dialogue MIRROR voice suite without copying the API key
out of the Modal secret:

```bash
modal run modal_voice_eval.py \
  --base-url https://<modal-endpoint> \
  --model Qwen/Qwen3-4B-Instruct-2507 \
  --output mirror_voice_eval_4b.json
```

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
