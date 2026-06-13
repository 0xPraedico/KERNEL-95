"""Desktop interaction routing for the KERNEL-95 game world."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .ai_engine import echo_speak, mirror_terminal_response, narrate_os_result
from .game_state import GameState
from .os_data import MIRROR_INTRO, OS_FILES, OS_OBJECTS
from .os_tools import (
    OSToolResult,
    ask_mirror_about_file,
    audit_mirror_private_logs,
    compare_restore_points,
    demand_evidence,
    execute_os_command,
    inspect_file,
    listen_to_echo,
    recover_deleted_file,
    run_contradiction_scan,
    trace_echo,
    unlock_hidden_partition,
    verify_mirror_claim,
)


@dataclass
class OSActionResult:
    message: str
    selected_object: str
    selected_file: str | None = None
    tool_result: OSToolResult | None = None
    terminal_hint: str = ""


KNOWN_COMMANDS = {
    "help",
    "status",
    "dir",
    "cd system",
    "cd hidden",
    "scan memory",
    "run contradiction_scan",
    "compare restore_points",
    "verify mirror",
    "listen echo",
    "trace echo",
    "audit mirror",
    "unlock hidden_partition",
    "delete echo",
    "extract echo",
    "protect echo",
    "quarantine both",
    "allow merge",
}


def _append_terminal(state: GameState, prompt: str, title: str, output: str) -> None:
    state.terminal_history.append(f"{prompt or '<empty>'}\n{title} // {output}")
    state.terminal_history = state.terminal_history[-16:]


def _locked_result(state: GameState, object_id: str | None = None) -> OSActionResult:
    message = "Connect MIRROR.exe first."
    state.current_mirror_message = message
    _append_terminal(state, "SYSTEM", "MIRROR LINK REQUIRED", message)
    return OSActionResult(message, object_id or state.selected_os_object)


def connect_mirror(state: GameState) -> OSActionResult:
    """Establish the authoritative Python-side MIRROR connection."""
    if state.mirror_connected:
        return OSActionResult(
            "MIRROR.exe is already connected.",
            state.selected_os_object,
        )
    state.mirror_connected = True
    state.game_phase = "desktop"
    intro = MIRROR_INTRO.replace("### MIRROR.exe // ASSIGNED ASSISTANT\n\n", "").strip()
    state.current_mirror_message = intro
    for line in (
        "External AI companion detected.",
        "Installing MIRROR.exe...",
        "Loading mask interface...",
        "Loading emotional firewall...",
        "WARNING: emotional firewall unstable.",
    ):
        _append_terminal(state, "SYSTEM", "CONNECTION", f"SYSTEM: {line}")
    _append_terminal(state, "MIRROR", "MIRROR", f"MIRROR: {intro}")
    state.add_conversation("assistant", intro, kind="system", source="MIRROR")
    state.add_feed("KERNEL-95 // MIRROR.exe connection established.")
    return OSActionResult(intro, "mirror_exe")


def _echo_claim(state: GameState) -> dict[str, object]:
    claim = next(
        (item for item in state.mirror_claims if item.get("id") == "echo_caused_incident"),
        None,
    )
    if claim is None:
        claim = {
            "id": "echo_caused_incident",
            "text": "MIRROR claims ECHO probably caused the memory-loss incident.",
            "strength": "weak",
            "support": "weak",
            "evidence_ids": ["mirror_claim_01"],
            "supported": False,
        }
        state.mirror_claims.append(claim)
    return claim


def trust_mirror_os(state: GameState) -> OSActionResult:
    """Resolve trust inside the KERNEL-95 case without legacy investigation lore."""
    if not state.mirror_connected:
        return _locked_result(state)
    early_case = not state.mirror_audit_unlocked and state.contradiction_scans < 2
    state.trust_mirror_count += 1
    state.adjust_trust(6)
    state.adjust_instability(-2)
    corruption = 2 if early_case else 0
    state.adjust_corruption(corruption)
    if early_case:
        claim = _echo_claim(state)
        if claim.get("support") != "unsupported":
            claim["support"] = "weak"
        message = (
            "MIRROR> Trust registered. ECHO is probably the cause. That conclusion is based on "
            "a weak process pattern, not verified ownership. Deleted files and restore points "
            "may change it."
        )
    else:
        message = (
            "MIRROR> Trust registered. I will keep interpretation separate from the files. "
            "The hidden partition and corrupted logs remain the only reliable path to ECHO."
        )
    state.current_mirror_message = message
    state.add_conversation("assistant", message, kind="action", source="MIRROR")
    state.add_feed("MIRROR // Trust accepted; confidence increased.")
    _append_terminal(state, "trust mirror", "MIRROR", message)
    return OSActionResult(message, state.selected_os_object)


def challenge_mirror_os(state: GameState) -> OSActionResult:
    """Pressure MIRROR while advancing the deterministic audit path."""
    if not state.mirror_connected:
        return _locked_result(state)
    state.challenged_mirror_count += 1
    state.player_skepticism = min(100, state.player_skepticism + 10)
    state.adjust_trust(-5)
    state.adjust_instability(10)
    state.adjust_hidden_progress(10)
    state.update_os_unlocks()
    if "echo_letter_01" in state.deleted_files_recovered:
        message = (
            "MIRROR> I did not hide evidence. I delayed harm. That distinction matters. "
            "ECHO wrote the deleted message because he was afraid, and I knew exactly what "
            "that fear would sound like."
        )
    else:
        message = (
            "MIRROR> I did not hide evidence. I delayed harm. That distinction matters. "
            "Recover the deleted files before you confuse my precision with innocence."
        )
    state.current_mirror_message = message
    state.add_conversation("assistant", message, kind="action", source="MIRROR")
    state.add_feed("MIRROR // Challenge logged; emotional firewall degraded.")
    _append_terminal(state, "challenge mirror", "MIRROR", message)
    return OSActionResult(message, state.selected_os_object)


def demand_evidence_os(state: GameState) -> OSActionResult:
    """Force MIRROR to cite only discovered files and label unsupported claims."""
    if not state.mirror_connected:
        return _locked_result(state)
    _echo_claim(state)
    state.evidence_requests += 1
    state.demand_evidence_used = True
    result = demand_evidence("echo_caused_incident", state)
    message = (
        "MIRROR> Evidence support report follows.\n"
        f"{result.output}\n"
        "The attribution is now marked unsupported."
    )
    state.current_mirror_message = message
    state.add_conversation("assistant", message, kind="action", source="MIRROR")
    _append_terminal(state, "demand evidence", "MIRROR", message)
    return OSActionResult(message, state.selected_os_object, tool_result=result)


def _debug_object_available(object_id: str) -> bool:
    item = OS_OBJECTS.get(object_id, {})
    return not item.get("debug_easter_egg") or os.getenv(
        "NEON_TRACE_DEBUG_EASTER_EGGS", ""
    ) == "1"


def select_os_object(object_id: str, state: GameState) -> OSActionResult:
    if object_id not in OS_OBJECTS or not _debug_object_available(object_id):
        object_id = "my_computer"
    obj = OS_OBJECTS[object_id]
    state.selected_os_object = object_id
    file_id = str(obj["file_id"]) if obj.get("file_id") else None
    if file_id:
        state.selected_file_id = file_id
    window = str(obj.get("window", ""))
    if window and window not in state.open_windows:
        state.open_windows.append(window)
        state.open_windows = state.open_windows[-7:]
    state.add_feed(f"DESKTOP // Selected {obj['label']}.")
    return OSActionResult(
        (
            f"### {obj['label']}\n\n{obj['description']}\n\n"
            "Double-click or choose OPEN SELECTED to inspect this object."
        ),
        object_id,
        file_id,
        terminal_hint="help" if obj["type"] == "terminal" else "",
    )


def _tool_message(result: OSToolResult, state: GameState, file_id: str | None = None) -> str:
    return narrate_os_result(file_id, result, state)


def handle_os_interaction(action: str, object_id: str, state: GameState) -> OSActionResult:
    selection = select_os_object(object_id, state)
    obj = OS_OBJECTS[selection.selected_object]
    file_id = selection.selected_file

    if action == "select":
        return selection
    if action in {
        "ask",
        "trust",
        "challenge",
        "demand",
        "contradiction",
        "compare",
        "verify",
        "audit",
        "unlock",
        "listen",
    } and not state.mirror_connected:
        return _locked_result(state, selection.selected_object)
    if action == "open":
        if file_id:
            result = inspect_file(file_id, state)
            _append_terminal(state, "SYSTEM", "OPENED", str(obj["label"]))
            return OSActionResult(_tool_message(result, state, file_id), object_id, file_id, result)
        window = str(obj.get("window", obj["label"]))
        if window not in state.open_windows:
            state.open_windows.append(window)
        messages = {
            "my_computer": "C:/, SYSTEM/, RESTORE/, USERS/, and an encrypted HIDDEN:/ partition are indexed.",
            "recycle_bin": "Deleted entries detected: echo_letter_01.tmp and smile_protocol.old.",
            "command_prompt": "KERNEL-95 command processor ready. Type `help`.",
            "system_restore": "Restore points found: 1998, 2004, 2031, 2077. Two are currently readable.",
            "control_panel": "TRUST_PROTOCOL.hlp loaded. MIRROR can analyze faster than you can verify.",
            "network_neighborhood": "ECHO@LOCALHOST // MIRROR@REMOTE // ARCHIVE_013",
            "hidden_partition": (
                "HIDDEN:/ is mounted. ECHO_HOME is visible."
                if state.hidden_partition_unlocked
                else f"HIDDEN:/ locked. Recovery progress: {state.hidden_partition_progress}%."
            ),
            "old_messenger": "unknown_user: Do you still remember rain?\\nmirror_process: I remember you asking.",
            "mirror_exe": (
                "MIRROR Assistant is ONLINE."
                if state.mirror_connected
                else "MIRROR Assistant is OFFLINE. Connect MIRROR.exe first."
            ),
            "echo_core_app": (
                "ECHO core is readable."
                if state.echo_core_unlocked
                else "ECHO Core remains hidden behind HIDDEN:/."
            ),
            "final_judgment": (
                "Final Judgment record is ready."
                if state.final_judgment_unlocked
                else "Final Judgment is locked until HIDDEN:/ and the MIRROR audit are complete."
            ),
        }
        _append_terminal(state, "SYSTEM", "OPENED", str(obj["label"]))
        return OSActionResult(
            f"### {obj['label']}\n\n{messages.get(object_id, obj['description'])}",
            object_id,
            terminal_hint="help" if object_id == "command_prompt" else "",
        )
    if action == "ask":
        if file_id:
            if file_id not in state.inspected_files:
                inspect_file(file_id, state)
            result = ask_mirror_about_file(file_id, state)
            return OSActionResult(_tool_message(result, state, file_id), object_id, file_id, result)
        return OSActionResult(
            f"### MIRROR.exe // {obj['label']}\n\n"
            f"{obj['description']} I will not infer beyond the files you have opened.",
            object_id,
        )
    if action == "trust":
        return trust_mirror_os(state)
    if action == "challenge":
        return challenge_mirror_os(state)
    if action == "demand":
        return demand_evidence_os(state)
    if action == "contradiction":
        result = run_contradiction_scan(state)
        return OSActionResult(_tool_message(result, state), object_id, tool_result=result)
    if action == "recover":
        target = "echo_letter_01" if "echo_letter_01" not in state.deleted_files_recovered else "smile_protocol_old"
        result = recover_deleted_file(target, state)
        state.selected_file_id = target
        return OSActionResult(_tool_message(result, state, target), "recycle_bin", target, result)
    if action == "compare":
        for restore_id in ("restore_1998", "restore_2077"):
            if restore_id not in state.inspected_files:
                inspect_file(restore_id, state)
        result = compare_restore_points(state)
        return OSActionResult(_tool_message(result, state), "system_restore", tool_result=result)
    if action == "verify":
        if "mirror_claim_01" not in state.inspected_files:
            inspect_file("mirror_claim_01", state)
        result = verify_mirror_claim("echo_caused_incident", state)
        return OSActionResult(_tool_message(result, state), object_id, tool_result=result)
    if action == "audit":
        result = audit_mirror_private_logs(state)
        if state.mirror_audit_unlocked:
            state.selected_file_id = "mirror_unsent"
        return OSActionResult(_tool_message(result, state, "mirror_unsent" if state.mirror_audit_unlocked else None), "mirror_exe", state.selected_file_id, result)
    if action == "unlock":
        result = unlock_hidden_partition(state)
        return OSActionResult(_tool_message(result, state), "hidden_partition", tool_result=result)
    if action == "listen":
        result = listen_to_echo(state)
        message = (
            echo_speak(state, result.output)
            if result.severity != "warning"
            else _tool_message(result, state)
        )
        return OSActionResult(message, "hidden_partition", "echo_core" if state.hidden_partition_unlocked else None, result)
    return OSActionResult(f"### KERNEL-95\n\nAction `{action}` is unavailable.", object_id)


def handle_os_event(event: str, state: GameState) -> OSActionResult:
    """Route browser desktop events through the same deterministic action layer."""
    raw = (event or "").strip()
    if raw == "connect_mirror":
        return connect_mirror(state)
    if raw.startswith("open:"):
        return handle_os_interaction("open", raw[5:], state)
    if raw.startswith("file:"):
        file_id = raw[5:]
        if file_id in state.discovered_files:
            state.selected_file_id = file_id
            result = inspect_file(file_id, state)
            _append_terminal(state, "SYSTEM", "OPENED", str(result.raw.get("file_id", file_id)))
            return OSActionResult(
                _tool_message(result, state, file_id),
                state.selected_os_object,
                file_id,
                result,
            )
        return OSActionResult(
            "### FILE LOCKED\n\nThat artifact has not been recovered.",
            state.selected_os_object,
        )
    if raw.startswith("recover:"):
        file_id = raw[8:]
        result = recover_deleted_file(file_id, state)
        state.selected_os_object = "recycle_bin"
        state.selected_file_id = file_id
        _append_terminal(state, f"recover {OS_FILES[file_id]['filename']}", result.title, result.output)
        return OSActionResult(_tool_message(result, state, file_id), "recycle_bin", file_id, result)
    if raw.startswith("action:"):
        return handle_os_interaction(raw[7:], state.selected_os_object, state)
    return handle_os_interaction("open", raw, state)


def handle_terminal_input(
    text: str,
    selected_object: str,
    state: GameState,
) -> OSActionResult:
    """Route shell-like text to tools and natural language to MIRROR."""
    raw = (text or "").strip()
    normalized = " ".join(raw.lower().replace("_", " ").split())
    if not state.mirror_connected and normalized not in {"help", "status"}:
        return _locked_result(state, selected_object)
    is_command = (
        normalized in KNOWN_COMMANDS
        or normalized.startswith("type ")
        or normalized.startswith("recover ")
    )
    if is_command:
        result = trace_echo(state) if normalized == "trace echo" else execute_os_command(raw, state)
        if result.raw.get("requested"):
            state.selected_os_object = "final_judgment"
        _append_terminal(state, raw, result.title, result.output)
        return OSActionResult(
            _tool_message(result, state),
            state.selected_os_object,
            state.selected_file_id,
            result,
        )

    response = mirror_terminal_response(raw, selected_object, state)
    state.current_mirror_message = response
    state.add_conversation("user", raw, kind="terminal", source="investigator")
    state.add_conversation("assistant", response, kind="terminal", source="MIRROR")
    _append_terminal(state, raw, "MIRROR", response)
    return OSActionResult(response, selected_object, state.selected_file_id)
