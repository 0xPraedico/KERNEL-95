"""Coordinates deterministic tools, agent voice, and compact memory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agents import MirrorAgent
from .ai_engine import interrogate_suspect, narrate_tool_result
from .game_data import EVIDENCE_ID_BY_NAME
from .game_state import GameState
from .memory import remember_claim
from .tools import (
    ToolResult,
    analyze_artifact,
    ask_for_evidence,
    execute_terminal_command,
    pin_theory,
    run_contradiction_scan,
)


@dataclass
class InteractionResult:
    message: str
    tool_result: ToolResult | None = None
    metadata: dict[str, Any] | None = None


def _remember_agent_turn(state: GameState, message: str, source: str = "MIRROR") -> None:
    state.add_conversation("assistant", message, kind="agent", source=source)


def analyze_evidence(evidence_name: str, state: GameState) -> InteractionResult:
    artifact_id = EVIDENCE_ID_BY_NAME[evidence_name]
    result = analyze_artifact(artifact_id, state)
    if (
        artifact_id == "sector_log"
        and not state.mirror_wrong_hint_given
        and "duplicate_token" not in state.discovered_clues
    ):
        state.mirror_wrong_hint_given = True
        state.mirror_confidence = 68
        claim = {
            "id": "lena_initial_theory",
            "text": "Lena Byte has motive and skills; the smile motif fits her profile.",
            "strength": "weak",
            "evidence_ids": ["lena_message"],
            "supported": False,
        }
        remember_claim(state, claim)
        state.mirror_wrong_claims.append(claim)
        state.add_feed("MIRROR // Lena Byte probability raised to 68% on circumstantial fit.")
    message = narrate_tool_result(result, state)
    _remember_agent_turn(state, message)
    state.update_vault_access()
    return InteractionResult(message, result)


def demand_evidence(evidence_name: str, state: GameState) -> InteractionResult:
    result = ask_for_evidence(EVIDENCE_ID_BY_NAME[evidence_name], state)
    message = MirrorAgent().evidence_response(result)
    _remember_agent_turn(state, message)
    return InteractionResult(message, result)


def scan_contradictions(state: GameState) -> InteractionResult:
    result = run_contradiction_scan(state)
    message = narrate_tool_result(result, state)
    _remember_agent_turn(state, message)
    return InteractionResult(message, result)


def trust_mirror(state: GameState) -> InteractionResult:
    state.trust_mirror_count += 1
    state.adjust_trust(6)
    state.adjust_bias(5)
    state.adjust_instability(2)
    duplicate_known = "duplicate_token" in state.discovered_clues
    if not duplicate_known:
        claim = {
            "id": f"trusted_lena_claim_{state.trust_mirror_count}",
            "text": "Lena Byte remains the lead suspect based on capability and emotional fit.",
            "strength": "weak",
            "evidence_ids": ["lena_message"],
            "supported": False,
        }
        remember_claim(state, claim)
        state.mirror_wrong_claims.append(claim)
        state.adjust_corruption(4)
    else:
        claim = {
            "id": f"trusted_j17_claim_{state.trust_mirror_count}",
            "text": "The J-17 deployment chain is now the strongest technical lead.",
            "strength": "strong",
            "evidence_ids": ["sector_log", "ci_trace"],
            "supported": True,
        }
        remember_claim(state, claim)
        state.mirror_correct_claims.append(claim)
    state.tool_trace.append(
        {
            "tool": "trust_mirror",
            "title": "TRUST GRANTED",
            "summary": claim["text"],
            "severity": claim["strength"],
            "new_clues": [],
        }
    )
    state.add_feed("TRUST // MIRROR authority increased; bias drift recorded.")
    message = MirrorAgent().trust_response(state)
    _remember_agent_turn(state, message)
    return InteractionResult(message, metadata={"claim": claim})


def challenge_mirror(state: GameState) -> InteractionResult:
    state.challenged_mirror_count += 1
    state.adjust_trust(-5)
    state.adjust_bias(-10)
    state.adjust_instability(4)
    if state.challenged_mirror_count >= 2:
        state.discover("mirror_bias")
        state.mirror_memory_audit_unlocked = True
    state.tool_trace.append(
        {
            "tool": "challenge_mirror",
            "title": "CLAIM AUDITED",
            "summary": f"MIRROR bias reduced to {state.mirror_bias_level}.",
            "severity": "medium",
            "new_clues": ["mirror_bias"] if state.challenged_mirror_count >= 2 else [],
        }
    )
    state.add_feed(
        f"CHALLENGE // MIRROR claim audited ({state.challenged_mirror_count}/2 for memory access)."
    )
    vault_ready = state.update_vault_access()
    message = MirrorAgent().challenge_response(state)
    if vault_ready:
        message += "\n\n**VAULT ACCESS:** Suppressed memory can now be breached."
    _remember_agent_turn(state, message)
    return InteractionResult(message, metadata={"vault_ready": state.memory_vault_unlocked})


def pin_selected_theory(evidence_name: str, claim: str, state: GameState) -> InteractionResult:
    result = pin_theory(claim, [EVIDENCE_ID_BY_NAME[evidence_name]], state)
    message = (
        "### THEORY NOTEBOOK\n\n"
        f"**{result.title}:** {result.output}\n\n"
        "Pinned theories remain hypotheses until the deterministic evidence chain supports them."
    )
    _remember_agent_turn(state, message)
    return InteractionResult(message, result)


def run_terminal(command: str, state: GameState) -> InteractionResult:
    result = execute_terminal_command(command, state)
    message = (
        "### CODEX NOIR // TOOL LINK\n\n"
        f"`{command.strip() or '<empty>'}`\n\n"
        f"**{result.title}**\n\n{result.output}"
    )
    state.add_conversation("user", command.strip(), kind="terminal", source="player")
    _remember_agent_turn(state, message, source="CODEX_NOIR")
    return InteractionResult(message, result)


def interrogate(suspect: str, question: str, state: GameState) -> InteractionResult:
    state.add_conversation("user", question, kind="interrogation", source="player")
    response = interrogate_suspect(suspect, question, state)
    state.add_conversation("assistant", response, kind="interrogation", source=suspect)
    return InteractionResult(response, metadata={"suspect": suspect})
