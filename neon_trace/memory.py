"""Compact, deterministic memory helpers for the investigation agents."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def append_unique(items: list[dict[str, Any]], entry: dict[str, Any], key: str = "id") -> bool:
    identity = entry.get(key)
    if identity is not None and any(item.get(key) == identity for item in items):
        return False
    items.append(dict(entry))
    return True


def remember_conversation(
    state: Any,
    role: str,
    content: str,
    kind: str = "dialogue",
    source: str = "",
) -> None:
    state.conversation_memory.append(
        {
            "role": role,
            "content": content.strip()[:900],
            "kind": kind,
            "source": source,
        }
    )
    state.conversation_memory = state.conversation_memory[-24:]


def remember_fact(state: Any, fact: dict[str, Any]) -> bool:
    return append_unique(state.known_facts, fact)


def remember_contradiction(state: Any, contradiction: dict[str, Any]) -> bool:
    return append_unique(state.known_contradictions, contradiction)


def remember_claim(state: Any, claim: dict[str, Any]) -> bool:
    return append_unique(state.mirror_claims, claim)


def remember_theory(state: Any, theory: dict[str, Any]) -> bool:
    return append_unique(state.pinned_theories, theory)


def remember_tool_trace(state: Any, trace: dict[str, Any]) -> None:
    state.tool_trace.append(dict(trace))
    state.tool_trace = state.tool_trace[-30:]
    remember_conversation(
        state,
        "system",
        str(trace.get("summary", trace.get("tool", "Tool executed."))),
        kind="tool",
        source=str(trace.get("tool", "")),
    )


def recent_conversation(state: Any, limit: int = 10) -> list[dict[str, str]]:
    limit = max(1, min(12, limit))
    return [
        {
            "role": str(item.get("role", "system")),
            "content": str(item.get("content", ""))[:500],
        }
        for item in state.conversation_memory[-limit:]
    ]


def compact_case_memory(state: Any) -> dict[str, Any]:
    return {
        "facts": state.known_facts[-6:],
        "contradictions": state.known_contradictions[-4:],
        "theories": state.pinned_theories[-3:],
        "mirror_claims": state.mirror_claims[-4:],
        "readiness": state.readiness,
        "trust": state.trust,
        "corruption": state.corruption,
    }


def compact_agent_memory(state: Any, suspect: str | None = None) -> dict[str, Any]:
    memory: dict[str, Any] = {
        "mirror_bias": state.mirror_bias_level,
        "mirror_instability": state.mirror_instability,
        "wrong_claims": state.mirror_wrong_claims[-3:],
        "correct_claims": state.mirror_correct_claims[-3:],
        "secret_unlocked": state.secret_unlocked,
    }
    if suspect:
        memory["suspect_stress"] = state.suspect_stress.get(suspect, 0)
        memory["suspect_notes"] = state.suspect_notes.get(suspect, [])[-3:]
        memory["lies_told"] = state.suspect_lies_told.get(suspect, [])[-2:]
    return memory


def serializable_state(state: Any) -> dict[str, Any]:
    if is_dataclass(state):
        return asdict(state)
    return dict(vars(state))
