"""Routing for interactions originating in the Three.js crime scene."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .agents import MirrorAgent
from .ai_engine import narrate_tool_result
from .game_data import EVIDENCE_NAME_BY_ID, GAME_OBJECTS, SUSPECTS
from .game_state import GameState
from .orchestrator import (
    InteractionResult,
    analyze_evidence,
    challenge_mirror,
    demand_evidence,
    scan_contradictions,
    trust_mirror,
)
from .tools import decode_packet, execute_terminal_command, query_mirror_suppressed, trace_token


@dataclass
class GameActionResult:
    message: str
    selected_object: str
    selected_evidence: str | None = None
    selected_suspect: str | None = None
    terminal_hint: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def _object(object_id: str) -> dict[str, object]:
    return GAME_OBJECTS.get(object_id, GAME_OBJECTS["mirror_core"])


def select_3d_object(object_id: str, state: GameState) -> GameActionResult:
    if object_id not in GAME_OBJECTS:
        object_id = "mirror_core"
    obj = _object(object_id)
    state.selected_3d_object = object_id
    selected_evidence: str | None = None
    selected_suspect: str | None = None
    terminal_hint = ""

    if obj["type"] == "evidence":
        evidence_id = str(obj["evidence_id"])
        if evidence_id == "mirror_suppressed_anomaly" and not state.secret_unlocked:
            object_id = "memory_vault"
            obj = _object(object_id)
            state.selected_3d_object = object_id
        else:
            selected_evidence = EVIDENCE_NAME_BY_ID[evidence_id]
            state.selected_evidence = selected_evidence
    elif obj["type"] == "suspect":
        selected_suspect = str(obj["suspect_id"])
        state.selected_suspect = selected_suspect
    elif obj["type"] == "terminal":
        terminal_hint = "help"
    elif object_id == "sector_7_gate":
        terminal_hint = "scan sector_7"
    elif object_id == "sector_3_gate":
        terminal_hint = "scan sector_3"
    elif object_id == "memory_vault":
        terminal_hint = "audit mirror memory"
    elif object_id == "smile_rootkit":
        terminal_hint = "decode smile_packet"

    state.add_feed(f"3D SELECT // {obj['label']}.")
    message = (
        f"### SELECTED // {obj['label']}\n\n"
        f"{obj.get('description', 'No description recovered.')}\n\n"
        "Choose a tactical action to commit this interaction to case memory."
    )
    return GameActionResult(
        message,
        object_id,
        selected_evidence,
        selected_suspect,
        terminal_hint,
        {"object_type": obj["type"], "label": obj["label"]},
    )


def _from_interaction(
    interaction: InteractionResult,
    object_id: str,
    state: GameState,
    **kwargs: Any,
) -> GameActionResult:
    selection = select_3d_object(object_id, state)
    return GameActionResult(
        interaction.message,
        selection.selected_object,
        kwargs.get("selected_evidence", selection.selected_evidence),
        kwargs.get("selected_suspect", selection.selected_suspect),
        kwargs.get("terminal_hint", selection.terminal_hint),
        {"interaction": interaction.metadata or {}, **kwargs.get("metadata", {})},
    )


def handle_3d_interaction(action: str, object_id: str, state: GameState) -> GameActionResult:
    """Execute one scene action while keeping Python as the source of truth."""
    selection = select_3d_object(object_id, state)
    object_id = selection.selected_object
    obj = _object(object_id)
    object_type = str(obj["type"])

    if action == "select":
        return selection
    if action == "challenge":
        return _from_interaction(challenge_mirror(state), object_id, state)
    if action == "trust":
        return _from_interaction(trust_mirror(state), object_id, state)
    if action in {"contradiction", "forensic_scan"}:
        return _from_interaction(scan_contradictions(state), object_id, state)
    if action == "trace":
        result = trace_token("J-17", state)
        message = narrate_tool_result(result, state)
        state.add_conversation("assistant", message, kind="agent", source="MIRROR")
        state.update_vault_access()
        return GameActionResult(message, object_id, terminal_hint="trace token J-17")
    if action == "audit":
        result = query_mirror_suppressed(state)
        message = MirrorAgent().comment_on_tool(result, state)
        state.add_conversation("assistant", message, kind="agent", source="MIRROR")
        return GameActionResult(message, "memory_vault", terminal_hint="audit mirror memory")

    if action == "scan":
        if object_type == "evidence":
            evidence_name = EVIDENCE_NAME_BY_ID[str(obj["evidence_id"])]
            return _from_interaction(
                analyze_evidence(evidence_name, state),
                object_id,
                state,
                selected_evidence=evidence_name,
            )
        if object_type == "artifact":
            result = decode_packet("smile_packet", state)
            message = narrate_tool_result(result, state)
            return GameActionResult(message, object_id, terminal_hint="decode smile_packet")
        if object_type == "gate":
            result = execute_terminal_command(
                "scan sector_7" if object_id == "sector_7_gate" else "scan sector_3",
                state,
            )
            message = narrate_tool_result(result, state)
            state.update_vault_access()
            return GameActionResult(message, object_id, terminal_hint=str(result.raw.get("command", "")))
        if object_type == "terminal":
            result = execute_terminal_command("help", state)
            return GameActionResult(
                f"### CODEX NOIR // READY\n\n{result.output}",
                object_id,
                terminal_hint="help",
            )
        if object_type == "vault":
            return handle_3d_interaction("audit", object_id, state)
        if object_type == "suspect":
            return handle_3d_interaction("ask", object_id, state)
        return GameActionResult(
            "### MIRROR CORE // SCAN\n\nThe core is unstable but responsive. "
            "Trust, challenge, or demand evidence.",
            object_id,
        )

    if action in {"ask", "demand"}:
        if object_type == "evidence":
            evidence_name = EVIDENCE_NAME_BY_ID[str(obj["evidence_id"])]
            return _from_interaction(
                demand_evidence(evidence_name, state),
                object_id,
                state,
                selected_evidence=evidence_name,
            )
        if object_type == "suspect":
            suspect = str(obj["suspect_id"])
            profile = SUSPECTS[suspect]
            stress = state.suspect_stress.get(suspect, 0)
            message = (
                f"### MIRROR // SUSPECT PROFILE\n\n"
                f"**{suspect}** // {profile['role']}\n\n"
                f"Voice pattern: {profile['voice']}. Current pressure estimate: **{stress}%**.\n\n"
                "Open Interrogation to question this hologram directly."
            )
            return GameActionResult(message, object_id, selected_suspect=suspect)
        if object_type == "terminal":
            return GameActionResult(
                "### MIRROR // TERMINAL\n\nRecommended commands: `help`, "
                "`scan contradictions`, `trace token J-17`, `inspect commit 7f31c9a`, "
                "`audit mirror memory`.",
                object_id,
                terminal_hint="help",
            )
        if object_type == "vault":
            missing = []
            if state.challenged_mirror_count < 2:
                missing.append(f"challenge MIRROR {2 - state.challenged_mirror_count} more time(s)")
            if state.contradiction_scans < 2:
                missing.append(f"run {2 - state.contradiction_scans} more contradiction scan(s)")
            if "duplicate_token" not in state.discovered_clues:
                missing.append("prove duplicate J-17")
            message = (
                "### MIRROR // MEMORY VAULT\n\n"
                + (
                    "Vault access is ready. Breach it to recover the suppressed anomaly."
                    if not missing
                    else "Access remains locked: " + "; ".join(missing) + "."
                )
            )
            return GameActionResult(message, object_id, terminal_hint="audit mirror memory")
        return GameActionResult(
            "### MIRROR // SELF-REPORT\n\nMy confidence is not evidence. "
            f"Bias level: **{state.mirror_bias_level}%**. Instability: **{state.mirror_instability}%**.",
            object_id,
        )

    return GameActionResult(
        f"### UNKNOWN ACTION\n\n`{action}` is not available for {obj['label']}.",
        object_id,
    )
