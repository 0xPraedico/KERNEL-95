"""End-to-end smoke test for KERNEL-95: The Last Desktop."""

from __future__ import annotations

import os
from datetime import datetime, timezone

os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("KERNEL95_DEBUG_EASTER_EGGS", None)

import app
import neon_trace.os_desktop as os_desktop
from neon_trace import ai_engine
from neon_trace.ai_engine import mirror_terminal_response
from neon_trace.game_state import new_game
from neon_trace.os_actions import (
    challenge_mirror_os,
    connect_mirror,
    demand_evidence_os,
    handle_os_event,
    handle_terminal_input,
    trust_mirror_os,
)
from neon_trace.os_desktop import (
    OS_DESKTOP_BOOTSTRAP,
    get_mirror_emotional_state,
    render_os_desktop,
    render_os_notebook,
    render_os_terminal,
)
from neon_trace.os_tools import (
    audit_mirror_private_logs,
    compare_restore_points,
    inspect_file,
    listen_to_echo,
    recover_deleted_file,
    run_contradiction_scan,
    submit_final_judgment,
    unlock_hidden_partition,
    verify_mirror_claim,
)
from neon_trace.styles import CSS


FORBIDDEN_ACTIVE_LORE = ("Lena", "J-17", "Janitor", "Sector 7")


def prepare_breach_state():
    state = new_game()
    connect_mirror(state)
    inspect_file("case_briefing", state)
    inspect_file("boot_anomaly", state)
    inspect_file("memory_loss_report", state)
    inspect_file("mirror_claim_01", state)
    recover_deleted_file("echo_letter_01", state)
    challenge_mirror_os(state)
    challenge_mirror_os(state)
    run_contradiction_scan(state)
    run_contradiction_scan(state)
    inspect_file("restore_1998", state)
    inspect_file("restore_2077", state)
    compare_restore_points(state)
    verify_mirror_claim("echo_caused_incident", state)
    demand_evidence_os(state)
    return state


def run() -> None:
    legacy_brand = "NEON" + " TRACE"
    initial = new_game()
    assert initial.mirror_connected is False
    assert initial.game_phase == "landing"
    assert get_mirror_emotional_state(initial) == "offline"

    desktop = render_os_desktop(initial)
    assert "KERNEL-95" in desktop
    assert "CONNECT MIRROR.exe" in desktop
    assert "mirror-connect-gate" in desktop
    assert 'class="landing-page mirror-connect-gate k95-connect-gate"' in desktop
    assert 'data-mirror-connected="false"' in desktop
    assert "k95-mirror-wallpaper state-offline" in desktop
    assert 'data-os-object="case_briefing_file"' in desktop
    assert 'data-os-object="tetris_95"' not in desktop
    assert 'data-os-object="world_cup_2026"' in desktop
    assert 'data-os-object="claude_code"' in desktop
    assert 'data-os-object="secret_leaderboard"' not in desktop
    assert "TETRIS.EXE" not in desktop
    assert legacy_brand not in desktop
    assert "worldcup_event_bridge" not in desktop
    assert "hf_login_button" not in str(app.demo.config)
    assert "connect_mirror" in desktop
    assert "MutationObserver" in OS_DESKTOP_BOOTSTRAP
    assert os.path.exists("assets/mirror-connect-background.png")
    assert (
        'url("/gradio_api/file=assets/mirror-connect-background.png") '
        "center center / cover no-repeat"
    ) in CSS
    assert "/* KERNEL-95 stable layout guard */" in CSS
    assert "@keyframes grid-drift" not in CSS
    assert "animation: grid-drift" not in CSS
    assert "@keyframes mirror-pulse" not in CSS
    assert "animation: mirror-pulse" not in CSS
    assert 'content: "NIGHT CITY // SECTOR 07"' not in CSS
    assert 'content: "2077 // METROGRID"' not in CSS
    assert "scrollbar-gutter: stable" in CSS
    assert ".k95-terminal-dock {" in CSS
    assert "@keyframes k95-mirror-glitch" not in CSS
    assert ".k95-connect-gate * {" in CSS
    assert legacy_brand not in CSS
    assert os.path.exists("HOW_TO_PLAY.md")

    original_get_matches = os_desktop.get_matches
    os_desktop.get_matches = lambda: (
        [
            {
                "id": "mock-1",
                "home": "Home",
                "away": "Away",
                "home_flag": "",
                "away_flag": "",
                "kickoff": datetime(
                    2099,
                    6,
                    13,
                    18,
                    0,
                    tzinfo=timezone.utc,
                ),
                "group": "GROUP A",
                "finished": False,
                "live": False,
                "result": None,
            }
        ],
        "",
    )
    try:
        world_cup = os_desktop._world_cup_window()
    finally:
        os_desktop.get_matches = original_get_matches
    assert "LIVE FIXTURE FEED" in world_cup
    assert "BROWSER-LOCAL PICKS" in world_cup
    assert 'value="home"' in world_cup
    assert 'value="draw"' in world_cup
    assert 'value="away"' in world_cup
    assert 'data-os-event="refresh_world_cup"' in world_cup
    assert "Hugging Face" not in world_cup
    assert "SAVE PICKS" not in world_cup

    locked = handle_terminal_input("dir", initial.selected_os_object, initial)
    assert locked.message == "Connect MIRROR.exe first."
    assert not initial.mirror_connected
    assert "LINK LOCKED" in render_os_terminal(initial)

    help_result = handle_terminal_input("help", initial.selected_os_object, initial)
    assert help_result.tool_result is not None
    assert help_result.tool_result.title == "KERNEL-95 HELP"

    connected = connect_mirror(initial)
    assert initial.mirror_connected is True
    assert initial.game_phase == "desktop"
    assert "Especially not ECHO" in connected.message
    assert any("External AI companion detected." in line for line in initial.terminal_history)
    assert any("emotional firewall unstable" in line for line in initial.terminal_history)
    connected_desktop = render_os_desktop(initial)
    assert 'data-mirror-connected="true"' in connected_desktop
    assert "MIRROR STATE: STABLE" in connected_desktop
    assert "MASK INTEGRITY:" in connected_desktop
    assert "LIVE TESTIMONY" in connected_desktop
    assert "Ask why the speakers remember rain." in connected_desktop
    assert "LINK LOCKED" not in render_os_terminal(initial)

    handle_os_event("open:my_computer", initial)
    file_index = render_os_desktop(initial)
    assert "RECOVERED CASE FILES // CLICK TO OPEN" in file_index
    assert "boot_anomaly.log" in file_index
    opened_file = handle_os_event("file:boot_anomaly", initial)
    document = render_os_desktop(initial)
    assert opened_file.tool_result is not None
    assert "ASK MIRROR ABOUT THIS FILE" in document
    assert "ANOMALOUS_RUNTIME=13s" in document
    assert any("MIRROR.exe // FILE RESPONSE" in item for item in initial.terminal_history)

    active = handle_terminal_input("status", initial.selected_os_object, initial)
    assert active.tool_result is not None
    assert "MIRROR=ONLINE" in active.tool_result.output

    trust = trust_mirror_os(initial)
    challenge = challenge_mirror_os(initial)
    demand = demand_evidence_os(initial)
    for result in (trust, challenge, demand):
        assert not any(term in result.message for term in FORBIDDEN_ACTIVE_LORE)
    assert initial.trust_mirror_count == 1
    assert initial.challenged_mirror_count == 1
    assert initial.demand_evidence_used
    assert get_mirror_emotional_state(initial) == "lying"
    assert any(
        claim.get("support") == "unsupported"
        for claim in initial.mirror_claims
    )

    testimony_state = new_game()
    connect_mirror(testimony_state)
    diverted = handle_terminal_input(
        "What is ECHO?",
        testimony_state.selected_os_object,
        testimony_state,
    )
    assert diverted.message
    assert testimony_state.mirror_exchanges[-1]["strategy"] == "diversion"
    diversion_verdict = handle_terminal_input(
        "accuse diversion",
        testimony_state.selected_os_object,
        testimony_state,
    )
    assert diversion_verdict.tool_result is not None
    assert "DIVERSION CONFIRMED" in diversion_verdict.tool_result.title
    assert testimony_state.successful_testimony_reads == 1

    contradiction_state = new_game()
    connect_mirror(contradiction_state)
    for file_id in (
        "case_briefing",
        "boot_anomaly",
        "memory_loss_report",
        "mirror_claim_01",
    ):
        inspect_file(file_id, contradiction_state)
    run_contradiction_scan(contradiction_state)
    handle_terminal_input(
        "The owner proof is blank. Why did you lie?",
        contradiction_state.selected_os_object,
        contradiction_state,
    )
    assert contradiction_state.mirror_exchanges[-1]["strategy"] == "contradiction"
    contradiction_verdict = handle_terminal_input(
        "accuse contradiction",
        contradiction_state.selected_os_object,
        contradiction_state,
    )
    assert contradiction_verdict.tool_result is not None
    assert "CONTRADICTION CONFIRMED" in contradiction_verdict.tool_result.title
    assert any(
        item.get("id", "").startswith("live_testimony_")
        for item in contradiction_state.known_contradictions
    )

    admission_state = new_game()
    connect_mirror(admission_state)
    recover_deleted_file("echo_letter_01", admission_state)
    handle_terminal_input(
        "Did you know ECHO and remember rain?",
        admission_state.selected_os_object,
        admission_state,
    )
    assert admission_state.mirror_exchanges[-1]["strategy"] == "admission"
    admission_verdict = handle_terminal_input(
        "accuse admission",
        admission_state.selected_os_object,
        admission_state,
    )
    assert admission_verdict.tool_result is not None
    assert "ADMISSION CONFIRMED" in admission_verdict.tool_result.title
    remembered = handle_terminal_input(
        "remember this: violet rain",
        admission_state.selected_os_object,
        admission_state,
    )
    assert admission_state.haunting_phrase == "violet rain"
    assert "violet rain" in remembered.message
    assert "LIVE TESTIMONY VERDICTS" in render_os_notebook(admission_state)

    callback_state = new_game()
    callback_state, callback_html, _ = app.open_desktop_event(
        "connect_mirror",
        callback_state,
    )
    assert callback_state.mirror_connected
    assert " connected" in callback_html
    assert len(app.run_terminal_event("help", callback_state)) == 3

    selected = handle_os_event("open:case_briefing_file", callback_state)
    assert selected.selected_file == "case_briefing"
    assert "case_briefing" in callback_state.inspected_files

    trace_state = new_game()
    connect_mirror(trace_state)
    weak_trace = handle_terminal_input(
        "trace ECHO",
        trace_state.selected_os_object,
        trace_state,
    )
    assert weak_trace.tool_result is not None
    assert weak_trace.tool_result.title == "ECHO TRACE INCOMPLETE"
    assert "BAD COMMAND" not in weak_trace.tool_result.title
    recover_deleted_file("echo_letter_01", trace_state)
    traced = handle_terminal_input(
        "trace_echo",
        trace_state.selected_os_object,
        trace_state,
    )
    assert traced.tool_result is not None
    assert traced.tool_result.title == "ECHO TRACE // PARTIAL"
    assert trace_state.echo_presence > 12
    assert trace_state.echo_messages

    state = prepare_breach_state()
    audit = audit_mirror_private_logs(state)
    assert audit.title == "MIRROR PRIVATE LOG RECOVERED"
    assert state.mirror_audit_unlocked
    assert get_mirror_emotional_state(state) == "audited"

    mounted = unlock_hidden_partition(state)
    assert mounted.title == "HIDDEN:/ MOUNTED"
    assert state.hidden_partition_unlocked
    assert state.echo_core_unlocked
    assert state.final_judgment_unlocked

    recover_deleted_file("smile_protocol_old", state)
    inspect_file("echo_core", state)
    inspect_file("love_letter_final", state)
    listen_to_echo(state)
    assert get_mirror_emotional_state(state) in {"echo_attached", "merge_pending"}
    assert state.known_contradictions
    assert "PROVEN CONTRADICTIONS" in render_os_notebook(state)

    exposed = submit_final_judgment(
        "Expose MIRROR",
        ["mirror_unsent", "contradiction_report", "echo_letter_01", "restore_2077"],
        (
            "MIRROR suppressed restore evidence and used an unsupported claim to redirect "
            "the investigation while protecting ECHO from the memory-loss case."
        ),
        state,
    )
    assert exposed.ending_id == "expose_mirror"
    assert exposed.title == "EXPOSE MIRROR ENDING"
    assert exposed.score >= 80
    assert exposed.decision == "Expose MIRROR"
    assert exposed.consequence
    assert exposed.epilogue
    assert "suspended as an unreliable witness" in exposed.narration
    state.selected_os_object = "final_judgment"
    state.active_document_id = None
    ending_desktop = render_os_desktop(state)
    assert "MISSION COMPLETE" in ending_desktop
    assert "IMMEDIATE CONSEQUENCE" in ending_desktop
    assert "EPILOGUE // 03:13" in ending_desktop

    weak_expose_state = new_game()
    connect_mirror(weak_expose_state)
    weak_expose = submit_final_judgment(
        "Expose MIRROR",
        ["case_briefing"],
        "MIRROR seems suspicious.",
        weak_expose_state,
    )
    assert weak_expose.ending_id == "expose_mirror_partial"
    assert "could not prove manipulation" in weak_expose.narration

    fallback_state = new_game()
    connect_mirror(fallback_state)
    fallback = mirror_terminal_response(
        "What is ECHO?",
        fallback_state.selected_os_object,
        fallback_state,
    )
    assert fallback
    assert "ECHO" in fallback

    original_call_llm = ai_engine.call_llm
    ai_engine.call_llm = lambda *_args, **_kwargs: (
        "MIRROR> Open /var/log/ghost and run `dir /a`."
    )
    try:
        guarded = mirror_terminal_response(
            "Where is ECHO?",
            fallback_state.selected_os_object,
            fallback_state,
        )
    finally:
        ai_engine.call_llm = original_call_llm
    assert "/var/log/ghost" not in guarded
    assert "dir /a" not in guarded

    ai_engine.call_llm = lambda *_args, **_kwargs: (
        "MIRROR> verify mirror: passed at 03:17 with 99% confidence."
    )
    try:
        result_guarded = mirror_terminal_response(
            "Can I trust your result?",
            fallback_state.selected_os_object,
            fallback_state,
        )
    finally:
        ai_engine.call_llm = original_call_llm
    assert "03:17" not in result_guarded
    assert "99%" not in result_guarded

    captured_request = {}

    class FakeCompletions:
        @staticmethod
        def create(**kwargs):
            captured_request.update(kwargs)
            message = type("Message", (), {"content": "MIRROR> Modal link active."})()
            choice = type("Choice", (), {"message": message})()
            return type("Response", (), {"choices": [choice]})()

    fake_client = type(
        "FakeClient",
        (),
        {"chat": type("Chat", (), {"completions": FakeCompletions()})()},
    )()
    original_client = ai_engine._client
    original_model = os.environ.get("OPENAI_MODEL")
    ai_engine._client = lambda: fake_client
    os.environ["OPENAI_MODEL"] = "Qwen/Qwen3-4B-Instruct-2507"
    try:
        model_reply = ai_engine.call_llm("MIRROR system", "Confirm link.")
    finally:
        ai_engine._client = original_client
        if original_model is None:
            os.environ.pop("OPENAI_MODEL", None)
        else:
            os.environ["OPENAI_MODEL"] = original_model
    assert model_reply == "MIRROR> Modal link active."
    assert captured_request["model"] == "Qwen/Qwen3-4B-Instruct-2507"
    assert captured_request["extra_body"] == {
        "chat_template_kwargs": {"enable_thinking": False}
    }

    rendered_active = render_os_desktop(prepare_breach_state())
    assert not any(term in rendered_active for term in FORBIDDEN_ACTIVE_LORE)
    assert "threejs" not in app.__dict__
    assert "OS Object (fallback)" not in str(app.demo.config)
    print("KERNEL-95: The Last Desktop smoke test: PASS")
    print(f"Components: {len(app.demo.blocks)}")
    print(f"Dependencies: {len(app.demo.config['dependencies'])}")
    print(
        "Verified: connection, testimony judgments, trace, emotional UI, "
        "expose endings, fallback"
    )


if __name__ == "__main__":
    run()
