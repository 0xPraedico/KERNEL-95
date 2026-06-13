"""End-to-end smoke test for NEON TRACE: The Last Desktop."""

from __future__ import annotations

import os

os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("HF_TOKEN", None)
os.environ.pop("HF_LEADERBOARD_REPO", None)
os.environ.pop("NEON_TRACE_DEBUG_EASTER_EGGS", None)

import app
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
    initial = new_game()
    assert initial.mirror_connected is False
    assert initial.game_phase == "landing"
    assert get_mirror_emotional_state(initial) == "offline"

    desktop = render_os_desktop(initial)
    assert "KERNEL-95" in desktop
    assert "CONNECT MIRROR.exe" in desktop
    assert "mirror-connect-gate" in desktop
    assert 'data-mirror-connected="false"' in desktop
    assert "k95-mirror-wallpaper state-offline" in desktop
    assert 'data-os-object="case_briefing_file"' in desktop
    assert 'data-os-object="tetris_95"' not in desktop
    assert 'data-os-object="world_cup_2026"' in desktop
    assert 'data-os-object="claude_code"' in desktop
    assert "TETRIS.EXE" not in desktop
    assert "connect_mirror" in desktop
    assert "MutationObserver" in OS_DESKTOP_BOOTSTRAP
    assert os.path.exists("HOW_TO_PLAY.md")

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
    assert "LINK LOCKED" not in render_os_terminal(initial)

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
    assert "suspended as an unreliable witness" in exposed.narration

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

    rendered_active = render_os_desktop(prepare_breach_state())
    assert not any(term in rendered_active for term in FORBIDDEN_ACTIVE_LORE)
    assert "threejs" not in app.__dict__
    assert "OS Object (fallback)" not in str(app.demo.config)
    print("NEON TRACE: The Last Desktop smoke test: PASS")
    print(f"Components: {len(app.demo.blocks)}")
    print(f"Dependencies: {len(app.demo.config['dependencies'])}")
    print("Verified: connection, OS actions, trace, emotional UI, expose endings, fallback")


if __name__ == "__main__":
    run()
