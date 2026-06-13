"""NEON TRACE: The Last Desktop, a retro OS forensic horror game."""

from __future__ import annotations

import json
import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from neon_trace.game_state import GameState, new_game
from neon_trace.os_actions import handle_os_event, handle_terminal_input
from neon_trace.os_data import JUDGMENT_OPTIONS
from neon_trace.os_desktop import OS_DESKTOP_BOOTSTRAP, render_os_desktop
from neon_trace.os_tools import submit_final_judgment
from neon_trace.styles import CSS
from neon_trace.world_cup import (
    get_matches,
    prediction_is_open,
    save_predictions,
    user_predictions,
)

load_dotenv()
gr.set_static_paths(paths=[Path(__file__).parent / "assets"])


def _apply_message(state: GameState, message: str) -> None:
    state.current_mirror_message = message.replace("### ", "").replace("**", "")[:700]


def _snapshot(state: GameState) -> tuple[GameState, str, dict]:
    return state, render_os_desktop(state), gr.update(value="")


def open_desktop_event(event: str, state: GameState) -> tuple[GameState, str, dict]:
    """Handle every icon, file, action, and reboot event from inside the CRT."""
    if (event or "").strip() == "reset_case":
        return _snapshot(new_game())
    result = handle_os_event(event, state)
    _apply_message(state, result.message)
    return _snapshot(state)


def run_terminal_event(text: str, state: GameState) -> tuple[GameState, str, dict]:
    """Run a command or MIRROR conversation from the docked CRT terminal."""
    result = handle_terminal_input(text, state.selected_os_object, state)
    _apply_message(state, result.message)
    return _snapshot(state)


def submit_judgment_event(payload: str, state: GameState) -> tuple[GameState, str, dict]:
    """Submit the in-desktop Final Judgment form through a hidden Gradio bridge."""
    try:
        data = json.loads(payload or "{}")
    except json.JSONDecodeError:
        data = {}

    decision = str(data.get("decision", "Protect ECHO"))
    if decision not in JUDGMENT_OPTIONS:
        decision = "Protect ECHO"
    evidence = [
        str(file_id)
        for file_id in data.get("evidence", [])
        if isinstance(file_id, str)
    ]
    explanation = (
        f"ECHO: {str(data.get('echo', '')).strip()}\n"
        f"MIRROR: {str(data.get('mirror', '')).strip()}\n"
        f"13-MINUTE LOSS: {str(data.get('cause', '')).strip()}"
    )
    result = submit_final_judgment(decision, evidence, explanation, state)
    state.current_mirror_message = result.narration
    state.selected_os_object = "final_judgment"
    state.terminal_history.append(
        f"FINAL JUDGMENT\n{result.title} // {result.narration}"
    )
    state.terminal_history = state.terminal_history[-16:]
    return _snapshot(state)


def handle_world_cup_event(
    payload: str,
    state: GameState,
    profile: gr.OAuthProfile | None,
) -> tuple[GameState, str, dict]:
    """Restore or save World Cup picks, with HF identity when available."""
    try:
        data = json.loads(payload or "{}")
    except json.JSONDecodeError:
        data = {}
    matches, source_error = get_matches()
    by_id = {str(match["id"]): match for match in matches}
    incoming = data.get("predictions", {})
    if not isinstance(incoming, dict):
        incoming = {}
    for match_id, choice in incoming.items():
        match_id = str(match_id)
        choice = str(choice)
        match = by_id.get(match_id)
        if (
            match
            and choice in {"home", "draw", "away"}
            and prediction_is_open(match)
        ):
            state.world_cup_predictions[match_id] = choice

    state.leaderboard_unlocked = bool(state.world_cup_predictions)
    state.selected_os_object = "world_cup_2026"
    if profile is not None:
        state.hf_username = profile.username

    if data.get("type") == "save":
        if not state.world_cup_predictions:
            state.world_cup_status = "Choose at least one open match before saving."
        elif profile is None:
            state.world_cup_save_prompt = True
            state.world_cup_status = (
                "Picks staged locally. Connect Hugging Face to join the secret board."
            )
        else:
            synced, message = save_predictions(
                profile.username,
                profile.name,
                state.world_cup_predictions,
            )
            state.world_cup_save_prompt = not synced
            state.world_cup_status = message
    elif source_error:
        state.world_cup_status = source_error
    return _snapshot(state)


def load_user_session(
    state: GameState,
    profile: gr.OAuthProfile | None,
) -> tuple[GameState, str]:
    """Restore the HF display identity after an OAuth redirect."""
    if profile is not None:
        state.hf_username = profile.username
        restored = user_predictions(profile.username)
        if restored:
            state.world_cup_predictions.update(restored)
            state.leaderboard_unlocked = True
    return state, render_os_desktop(state)


def build_app() -> gr.Blocks:
    initial = new_game()
    oauth_enabled = bool(
        os.getenv("SPACE_ID")
        or os.getenv("OAUTH_CLIENT_ID")
        or os.getenv("HF_TOKEN")
    )
    with gr.Blocks(
        css=CSS,
        js=OS_DESKTOP_BOOTSTRAP,
        title="NEON TRACE: The Last Desktop",
    ) as demo:
        state = gr.State(initial)
        desktop_output = gr.HTML(
            render_os_desktop(initial),
            elem_classes=["kernel95-desktop-output"],
        )

        os_event_bridge = gr.Textbox(
            value="",
            show_label=False,
            container=False,
            elem_id="os_event_bridge",
            elem_classes=["os-object-bridge"],
        )
        terminal_event_bridge = gr.Textbox(
            value="",
            show_label=False,
            container=False,
            elem_id="terminal_event_bridge",
            elem_classes=["os-object-bridge"],
        )
        judgment_event_bridge = gr.Textbox(
            value="",
            show_label=False,
            container=False,
            elem_id="judgment_event_bridge",
            elem_classes=["os-object-bridge"],
        )
        worldcup_event_bridge = gr.Textbox(
            value="",
            show_label=False,
            container=False,
            elem_id="worldcup_event_bridge",
            elem_classes=["os-object-bridge"],
        )
        if oauth_enabled:
            gr.LoginButton(
                value="Sign in with Hugging Face 🤗",
                logout_value="Disconnect Hugging Face ({})",
                elem_id="hf_login_button",
                elem_classes=["os-object-bridge"],
            )
        else:
            gr.Button(
                "HF OAuth is enabled after deployment to Spaces",
                elem_id="hf_login_button",
                elem_classes=["os-object-bridge"],
            )

        os_event_bridge.input(
            open_desktop_event,
            inputs=[os_event_bridge, state],
            outputs=[state, desktop_output, os_event_bridge],
        )
        terminal_event_bridge.input(
            run_terminal_event,
            inputs=[terminal_event_bridge, state],
            outputs=[state, desktop_output, terminal_event_bridge],
        )
        judgment_event_bridge.input(
            submit_judgment_event,
            inputs=[judgment_event_bridge, state],
            outputs=[state, desktop_output, judgment_event_bridge],
        )
        if oauth_enabled:
            worldcup_event_bridge.input(
                handle_world_cup_event,
                inputs=[worldcup_event_bridge, state],
                outputs=[state, desktop_output, worldcup_event_bridge],
            )
            demo.load(
                load_user_session,
                inputs=[state],
                outputs=[state, desktop_output],
                show_progress="hidden",
            )
        else:
            worldcup_event_bridge.input(
                lambda payload, current: handle_world_cup_event(
                    payload,
                    current,
                    None,
                ),
                inputs=[worldcup_event_bridge, state],
                outputs=[state, desktop_output, worldcup_event_bridge],
            )

    return demo


demo = build_app()


if __name__ == "__main__":
    demo.queue(default_concurrency_limit=16).launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        show_error=True,
    )
