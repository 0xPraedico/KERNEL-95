"""KERNEL-95: The Last Desktop, a retro OS forensic horror game."""

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
from neon_trace.world_cup import get_matches

load_dotenv()
gr.set_static_paths(paths=[Path(__file__).parent / "assets"])


def _apply_message(state: GameState, message: str) -> None:
    state.current_mirror_message = message.replace("### ", "").replace("**", "")[:700]


def _snapshot(state: GameState) -> tuple[GameState, str, dict]:
    return state, render_os_desktop(state), gr.update(value="")


def open_desktop_event(event: str, state: GameState) -> tuple[GameState, str, dict]:
    """Handle every icon, file, action, and reboot event from inside the CRT."""
    event = (event or "").strip()
    if event == "reset_case":
        return _snapshot(new_game())
    if event == "refresh_world_cup":
        get_matches(force=True)
        state.selected_os_object = "world_cup_2026"
        return _snapshot(state)
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
    state.current_mirror_message = result.mirror_reaction
    state.selected_os_object = "final_judgment"
    state.active_document_id = None
    state.terminal_history.append(
        f"FINAL JUDGMENT // {result.decision}\n{result.title} // "
        f"{result.narration}\nCONSEQUENCE: {result.consequence}"
    )
    state.terminal_history.append(
        f"MIRROR\nLAST TRANSMISSION // {result.mirror_reaction}"
    )
    state.terminal_history = state.terminal_history[-16:]
    return _snapshot(state)


def build_app() -> gr.Blocks:
    initial = new_game()
    with gr.Blocks(
        css=CSS,
        js=OS_DESKTOP_BOOTSTRAP,
        title="KERNEL-95: The Last Desktop",
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

    return demo


demo = build_app()


if __name__ == "__main__":
    demo.queue(default_concurrency_limit=16).launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        show_error=True,
    )
