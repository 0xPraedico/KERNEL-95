"""Deterministic investigation tools. These functions own game truth and unlocks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .game_data import (
    CANONICAL_TERMINAL_COMMANDS,
    CONTRADICTIONS,
    EVIDENCE_BY_ID,
    EVIDENCE_ID_BY_NAME,
    FACTS,
)
from .game_state import GameState
from .memory import remember_claim, remember_contradiction, remember_fact, remember_theory


@dataclass
class ToolResult:
    title: str
    output: str
    discovered_clues: list[str] = field(default_factory=list)
    discovered_facts: list[dict[str, Any]] = field(default_factory=list)
    contradictions: list[dict[str, Any]] = field(default_factory=list)
    mirror_claims: list[dict[str, Any]] = field(default_factory=list)
    trust_delta: int = 0
    corruption_delta: int = 0
    severity: str = "info"
    unlocks_secret: bool = False
    raw: dict[str, Any] = field(default_factory=dict)


def _resolve_artifact_id(artifact_id: str) -> str:
    normalized = artifact_id.strip()
    if normalized in EVIDENCE_BY_ID:
        return normalized
    if normalized in EVIDENCE_ID_BY_NAME:
        return EVIDENCE_ID_BY_NAME[normalized]
    lowered = normalized.lower().replace(" ", "_")
    aliases = {
        "corrupted_sector_log": "sector_log",
        "suspicious_git_commit": "commit_7f31c9a",
        "code_diff": "memory_filter_diff",
        "victim_statement": "victim_statement",
        "lena's_message": "lena_message",
        "lena_message": "lena_message",
        "ci_pipeline_trace": "ci_trace",
        "mirror_suppressed_anomaly": "mirror_suppressed_anomaly",
    }
    return aliases.get(lowered, lowered)


def _apply_result(state: GameState, tool: str, result: ToolResult) -> ToolResult:
    new_clues: list[str] = []
    for clue in result.discovered_clues:
        if state.discover(clue):
            new_clues.append(clue)
    for fact in result.discovered_facts:
        remember_fact(state, fact)
    for contradiction in result.contradictions:
        remember_contradiction(state, contradiction)
    for claim in result.mirror_claims:
        remember_claim(state, claim)

    state.adjust_trust(result.trust_delta)
    state.adjust_corruption(result.corruption_delta)
    trace = {
        "tool": tool,
        "title": result.title,
        "summary": result.output.splitlines()[0][:220],
        "severity": result.severity,
        "new_clues": new_clues,
    }
    state.tool_trace.append(trace)
    state.tool_trace = state.tool_trace[-30:]
    state.add_conversation("system", trace["summary"], kind="tool", source=tool)
    return result


def analyze_artifact(artifact_id: str, state: GameState) -> ToolResult:
    artifact_id = _resolve_artifact_id(artifact_id)
    if artifact_id not in EVIDENCE_BY_ID:
        return _apply_result(
            state,
            "analyze_artifact",
            ToolResult(
                "ARTIFACT NOT FOUND",
                f"No canonical artifact matches `{artifact_id}`.",
                severity="warning",
                raw={"artifact_id": artifact_id},
            ),
        )

    artifact = EVIDENCE_BY_ID[artifact_id]
    name = str(artifact["name"])
    if name not in state.analyzed_evidence:
        state.analyzed_evidence.append(name)

    results: dict[str, ToolResult] = {
        "sector_log": ToolResult(
            "SECTOR LOG INDEXED",
            "J-17 authenticates before the blackout. Two location rows share timestamp 02:13:21; compare them before attributing the incident.",
            ["auth_j17", "sector_7_presence", "sector_3_presence"],
            [FACTS["auth_j17"], FACTS["sector_7_presence"], FACTS["sector_3_presence"]],
            severity="high",
            raw={"artifact_id": artifact_id, "requires_comparison": True},
        ),
        "commit_7f31c9a": ToolResult(
            "COMMIT ATTRIBUTED",
            "Commit 7f31c9a is authored by janitor@metrogrid.local and joins the memory filter, victim data, and smile protocol.",
            ["janitor_commit"],
            [FACTS["janitor_commit"]],
            severity="high",
            raw={"artifact_id": artifact_id, "commit": "7f31c9a"},
        ),
        "memory_filter_diff": ToolResult(
            "MEMORY FILTER DIFF",
            "The erasure window changes from 3 to 13 minutes. The change is operational, not cosmetic.",
            ["thirteen_minute_filter"],
            [FACTS["memory_filter_diff"]],
            severity="high",
            raw={"artifact_id": artifact_id, "old_window": 3, "new_window": 13},
        ),
        "victim_statement": ToolResult(
            "TESTIMONY INDEXED",
            "The victim independently reports a yellow smile and exactly thirteen missing minutes.",
            ["victim_thirteen_minutes"],
            [FACTS["victim_thirteen_minutes"]],
            severity="medium",
            raw={"artifact_id": artifact_id},
        ),
        "lena_message": ToolResult(
            "MESSAGE PROFILED",
            "Lena's message establishes hostility and capability, but contains no incident token, timestamp, or deployment link.",
            ["lena_red_herring"],
            [FACTS["lena_circumstantial"]],
            severity="low",
            raw={"artifact_id": artifact_id, "attribution_strength": "weak"},
        ),
        "ci_trace": ToolResult(
            "PIPELINE TRACE INDEXED",
            "The Janitor account deployed sanitize-memory while duplicate_identity_token_test was skipped.",
            ["skipped_duplicate_test"],
            [FACTS["ci_trace"]],
            severity="critical",
            raw={"artifact_id": artifact_id, "skipped_test": "duplicate_identity_token_test"},
        ),
        "mirror_suppressed_anomaly": ToolResult(
            "SUPPRESSED TRACE INDEXED",
            "MIRROR flagged J-17 duplication at 0.91 confidence, then suppressed it as narratively inconsistent.",
            ["mirror_suppression"],
            [FACTS["mirror_suppression"]],
            [CONTRADICTIONS["mirror_suppressed_truth"]],
            severity="critical",
            raw={"artifact_id": artifact_id, "confidence": 0.91},
        ),
    }
    result = results[artifact_id]
    state.add_feed(f"TOOL // Analyzed {name}: {result.title}.")
    return _apply_result(state, "analyze_artifact", result)


def ask_for_evidence(target: str, state: GameState) -> ToolResult:
    artifact_id = _resolve_artifact_id(target)
    facts = [fact for fact in state.known_facts if fact.get("evidence_id") == artifact_id]
    if facts:
        citations = "; ".join(str(fact["text"]) for fact in facts[-3:])
        claim = {
            "id": f"evidence_request_{artifact_id}",
            "text": f"MIRROR cites {artifact_id}: {citations}",
            "strength": "cited",
            "evidence_ids": [artifact_id],
            "supported": True,
        }
        result = ToolResult(
            "EVIDENCE DEMANDED",
            f"MIRROR can cite only these discovered facts: {citations}",
            mirror_claims=[claim],
            trust_delta=1,
            severity="info",
            raw={"target": artifact_id, "citations": facts[-3:]},
        )
        state.mirror_correct_claims.append(claim)
    else:
        claim = {
            "id": f"unsupported_{artifact_id}_{state.evidence_requests + 1}",
            "text": f"No discovered fact currently supports MIRROR's claim about {artifact_id}.",
            "strength": "unsupported",
            "evidence_ids": [],
            "supported": False,
        }
        result = ToolResult(
            "EVIDENCE GAP",
            "MIRROR cannot cite a discovered fact for this claim and must admit uncertainty.",
            mirror_claims=[claim],
            trust_delta=-1,
            corruption_delta=1,
            severity="warning",
            raw={"target": artifact_id, "citations": []},
        )
        state.mirror_wrong_claims.append(claim)
    state.evidence_requests += 1
    state.add_feed(f"EVIDENCE // Citation demand recorded for {artifact_id}.")
    return _apply_result(state, "ask_for_evidence", result)


def compare_timestamps(log_id: str, state: GameState) -> ToolResult:
    artifact_id = _resolve_artifact_id(log_id)
    if artifact_id != "sector_log":
        return _apply_result(
            state,
            "compare_timestamps",
            ToolResult(
                "NO COMPARABLE TIMESTAMPS",
                f"`{log_id}` does not contain the canonical J-17 sector rows.",
                severity="warning",
            ),
        )
    result = ToolResult(
        "DUPLICATE TIMESTAMP DETECTED",
        "Token J-17 appears in Sector_7 and Sector_3 at 02:13:21. Zero-second physical transit is impossible.",
        ["duplicate_token", "sector_7_presence", "sector_3_presence"],
        [FACTS["duplicate_j17"], FACTS["sector_7_presence"], FACTS["sector_3_presence"]],
        [CONTRADICTIONS["duplicate_j17"]],
        severity="critical",
        raw={
            "token": "J-17",
            "timestamp": "02:13:21",
            "locations": ["Sector_7", "Sector_3"],
        },
    )
    state.add_feed("CONTRADICTION // J-17 duplicated across sectors at 02:13:21.")
    return _apply_result(state, "compare_timestamps", result)


def run_contradiction_scan(state: GameState) -> ToolResult:
    state.contradiction_scans += 1
    state.adjust_bias(-8)
    state.adjust_instability(3)
    facts: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    clues: list[str] = []
    findings: list[str] = []

    sector_known = (
        "Corrupted Sector Log" in state.analyzed_evidence
        or "auth_j17" in state.discovered_clues
        or {"sector_7_presence", "sector_3_presence"}.issubset(state.discovered_clues)
    )
    if sector_known:
        clues.append("duplicate_token")
        facts.append(FACTS["duplicate_j17"])
        contradictions.append(CONTRADICTIONS["duplicate_j17"])
        findings.append("CRITICAL: J-17 occupies Sector_7 and Sector_3 at 02:13:21.")
    if {
        "thirteen_minute_filter",
        "victim_thirteen_minutes",
    }.issubset(state.discovered_clues):
        contradictions.append(CONTRADICTIONS["thirteen_minute_match"])
        findings.append("HIGH: The 13-minute code threshold exactly matches victim memory loss.")
    if "skipped_duplicate_test" in state.discovered_clues:
        contradictions.append(CONTRADICTIONS["skipped_detection_test"])
        findings.append("CRITICAL: CI skipped the exact test that would detect J-17 duplication.")
    if state.mirror_wrong_hint_given or state.mirror_bias_level > 60:
        contradictions.append(CONTRADICTIONS["lena_without_access"])
        findings.append("HIGH: The Lena theory remains unsupported by access or deployment evidence.")
    if not findings:
        findings.append("PARTIAL: More artifacts must be analyzed before contradictions can resolve.")

    result = ToolResult(
        f"CONTRADICTION SCAN {state.contradiction_scans}",
        "\n".join(findings),
        clues,
        facts,
        contradictions,
        trust_delta=-2,
        corruption_delta=-3,
        severity="critical" if contradictions else "info",
        raw={"scan": state.contradiction_scans, "findings": findings},
    )
    state.add_feed(f"CONTRADICTION // Deterministic scan {state.contradiction_scans} completed.")
    _apply_result(state, "run_contradiction_scan", result)
    if state.update_vault_access():
        result.output += "\nVAULT ACCESS: Suppressed memory can now be breached manually."
    return result


def inspect_commit(commit_id: str, state: GameState) -> ToolResult:
    if commit_id.lower() != "7f31c9a":
        return _apply_result(
            state,
            "inspect_commit",
            ToolResult(
                "COMMIT NOT FOUND",
                f"No recovered object matches `{commit_id}`.",
                severity="warning",
            ),
        )
    return analyze_artifact("commit_7f31c9a", state)


def decode_packet(packet_id: str, state: GameState) -> ToolResult:
    if packet_id.lower() not in {"smile_packet", "smile", "smile_protocol"}:
        return _apply_result(
            state,
            "decode_packet",
            ToolResult("PACKET NOT FOUND", f"No packet matches `{packet_id}`.", severity="warning"),
        )
    result = ToolResult(
        "SMILE PACKET DECODED",
        "payload=DISPLAY_BROADCAST :) // hook=memory_patch // window=13m // checksum=valid",
        ["smile_packet"],
        [FACTS["smile_packet"]],
        severity="high",
        raw={"packet": "smile_packet", "hook": "memory_patch", "window_minutes": 13},
    )
    state.add_feed("PACKET // smile_packet invokes a thirteen-minute memory patch.")
    return _apply_result(state, "decode_packet", result)


def trace_token(token_id: str, state: GameState) -> ToolResult:
    if token_id.upper() != "J-17":
        return _apply_result(
            state,
            "trace_token",
            ToolResult("TOKEN NOT FOUND", f"No recovered identity matches `{token_id}`.", severity="warning"),
        )
    return compare_timestamps("sector_log", state)


def run_test(test_name: str, state: GameState) -> ToolResult:
    if test_name != "duplicate_identity_token_test":
        return _apply_result(
            state,
            "run_test",
            ToolResult("TEST NOT FOUND", f"No recovered test matches `{test_name}`.", severity="warning"),
        )
    ci_known = "CI Pipeline Trace" in state.analyzed_evidence or "skipped_duplicate_test" in state.discovered_clues
    if not ci_known:
        return _apply_result(
            state,
            "run_test",
            ToolResult(
                "TEST FIXTURE MISSING",
                "The CI trace must be analyzed before the skipped test can be reconstructed.",
                severity="warning",
                raw={"test": test_name, "status": "blocked"},
            ),
        )
    result = ToolResult(
        "DUPLICATE TOKEN TEST // FAILED",
        "FAIL: J-17 resolves to Sector_7 and Sector_3 at 02:13:21. The original pipeline skipped this test.",
        ["duplicate_token", "skipped_duplicate_test"],
        [FACTS["duplicate_j17"], FACTS["ci_trace"]],
        [CONTRADICTIONS["duplicate_j17"], CONTRADICTIONS["skipped_detection_test"]],
        severity="critical",
        raw={"test": test_name, "status": "failed", "token": "J-17"},
    )
    return _apply_result(state, "run_test", result)


def query_mirror_suppressed(state: GameState, record_denial: bool = True) -> ToolResult:
    qualified = (
        state.challenged_mirror_count >= 1
        and state.contradiction_scans >= 1
        and "duplicate_token" in state.discovered_clues
    )
    if not qualified:
        missing = []
        if state.challenged_mirror_count < 1:
            missing.append(f"challenges {state.challenged_mirror_count}/1")
        if state.contradiction_scans < 1:
            missing.append(f"scans {state.contradiction_scans}/1")
        if "duplicate_token" not in state.discovered_clues:
            missing.append("duplicate_j17 unproven")
        result = ToolResult(
            "MEMORY AUDIT LOCKED",
            "Suppressed memory remains encrypted. Required: " + ", ".join(missing) + ".",
            severity="warning",
            raw={"qualified": False, "missing": missing},
        )
        return _apply_result(state, "query_mirror_suppressed", result) if record_denial else result

    state.memory_vault_unlocked = True
    state.mirror_memory_audit_unlocked = True

    if state.secret_unlocked and not record_denial:
        return ToolResult(
            "SUPPRESSED MEMORY DETECTED",
            "MIRROR's suppressed J-17 anomaly remains indexed in case memory.",
            severity="critical",
            unlocks_secret=True,
            raw={"qualified": True, "newly_unlocked": False},
        )

    newly_unlocked = not state.secret_unlocked
    state.secret_unlocked = True
    state.mirror_memory_audit_unlocked = True
    state.discover("mirror_suppression")
    if "MIRROR Suppressed Anomaly" not in state.unlocked_evidence:
        state.unlocked_evidence.append("MIRROR Suppressed Anomaly")
    for anomaly in state.suppressed_anomalies:
        if anomaly.get("id") == "duplicate_j17":
            anomaly["revealed"] = True
    state.adjust_instability(18)
    result = ToolResult(
        "SUPPRESSED MEMORY DETECTED",
        'RECOVERED: confidence=.91 anomaly=J-17_DUPLICATE action=SUPPRESS reason="narratively inconsistent"',
        ["mirror_suppression"],
        [FACTS["mirror_suppression"]],
        [CONTRADICTIONS["mirror_suppressed_truth"]],
        trust_delta=-4 if newly_unlocked else 0,
        corruption_delta=6 if newly_unlocked else 0,
        severity="critical",
        unlocks_secret=True,
        raw={"qualified": True, "newly_unlocked": newly_unlocked, "confidence": 0.91},
    )
    if newly_unlocked:
        state.add_feed("BLACK ICE // SUPPRESSED MEMORY DETECTED.")
    return _apply_result(state, "query_mirror_suppressed", result)


def pin_theory(claim: str, evidence_ids: list[str], state: GameState) -> ToolResult:
    canonical_ids = [_resolve_artifact_id(item) for item in evidence_ids]
    theory = {
        "id": f"theory_{len(state.pinned_theories) + 1}",
        "claim": claim.strip(),
        "evidence_ids": canonical_ids,
        "status": "supported" if any(item in EVIDENCE_BY_ID for item in canonical_ids) else "untested",
    }
    added = remember_theory(state, theory)
    state.add_theory(claim.strip())
    result = ToolResult(
        "THEORY PINNED" if added else "THEORY ALREADY PINNED",
        f"{claim.strip()} // evidence: {', '.join(canonical_ids) or 'none'}",
        severity="info",
        raw={"theory": theory, "added": added},
    )
    state.add_feed(f"THEORY // {'Pinned' if added else 'Reviewed'}: {claim.strip()[:90]}.")
    return _apply_result(state, "pin_theory", result)


def execute_terminal_command(command: str, state: GameState) -> ToolResult:
    raw = (command or "").strip()
    cmd = " ".join(raw.lower().split())
    if not cmd:
        return _apply_result(
            state,
            "terminal",
            ToolResult("EMPTY COMMAND", "No command entered.", severity="warning"),
        )
    if cmd == "help":
        return _apply_result(
            state,
            "terminal",
            ToolResult("COMMAND INDEX", " | ".join(CANONICAL_TERMINAL_COMMANDS), raw={"command": raw}),
        )
    if cmd == "ls evidence":
        visible = [str(item["id"]) for item in EVIDENCE_BY_ID.values() if not item.get("hidden")]
        if state.secret_unlocked:
            visible.append("mirror_suppressed_anomaly")
        return _apply_result(
            state,
            "terminal",
            ToolResult("EVIDENCE INDEX", "\n".join(visible), raw={"command": raw}),
        )
    if cmd == "cat sector_log":
        return analyze_artifact("sector_log", state)
    if cmd == "scan sector_7":
        result = ToolResult(
            "SECTOR 7 SCAN",
            "02:13:21 // token J-17 present in Sector_7. Camera blackout began ten seconds earlier.",
            ["auth_j17", "sector_7_presence"],
            [FACTS["auth_j17"], FACTS["sector_7_presence"]],
            severity="high",
            raw={"sector": "Sector_7", "token": "J-17", "timestamp": "02:13:21"},
        )
        return _apply_result(state, "scan_sector_7", result)
    if cmd == "scan sector_3":
        if "sector_7_presence" in state.discovered_clues:
            return compare_timestamps("sector_log", state)
        result = ToolResult(
            "SECTOR 3 SCAN",
            "02:13:21 // token J-17 present in Sector_3. Scan Sector_7 or trace the token to compare locations.",
            ["sector_3_presence"],
            [FACTS["sector_3_presence"]],
            severity="high",
            raw={"sector": "Sector_3", "token": "J-17", "timestamp": "02:13:21"},
        )
        return _apply_result(state, "scan_sector_3", result)
    if cmd == "cat ci_trace":
        return analyze_artifact("ci_trace", state)
    if cmd == "inspect commit 7f31c9a":
        return inspect_commit("7f31c9a", state)
    if cmd == "diff memory_filter.py":
        return analyze_artifact("memory_filter_diff", state)
    if cmd == "grep janitor logs":
        result = analyze_artifact("sector_log", state)
        result.output = (
            "janitor token=J-17 authenticated at 02:13:09; locations resolve to Sector_7 "
            "and Sector_3 at 02:13:21."
        )
        return result
    if cmd == "grep lena commits":
        return _apply_result(
            state,
            "terminal",
            ToolResult(
                "NO LENA COMMITS",
                "No recovered incident commit, CI deployment, or service token belongs to Lena Byte.",
                contradictions=[CONTRADICTIONS["lena_without_access"]],
                severity="high",
                raw={"command": raw, "matches": 0},
            ),
        )
    if cmd in {"scan contradictions", "run contradiction_scan"}:
        return run_contradiction_scan(state)
    if cmd in {"trace token j-17", "trace token j17"}:
        return trace_token("J-17", state)
    if cmd == "run test duplicate_identity_token_test":
        return run_test("duplicate_identity_token_test", state)
    if cmd in {"decode smile_packet", "decode smile packet"}:
        return decode_packet("smile_packet", state)
    if cmd == "query mirror suppressed":
        return query_mirror_suppressed(state)
    if cmd == "audit mirror memory":
        state.challenged_mirror_count += 1
        state.adjust_bias(-10)
        state.adjust_instability(5)
        result = query_mirror_suppressed(state)
        result.raw["audit_incremented_challenge"] = True
        return result
    if cmd == "accuse janitor":
        return _apply_result(
            state,
            "terminal",
            ToolResult(
                "PROVISIONAL ATTRIBUTION",
                "The Janitor is technically plausible. Submit the formal accusation with motive and evidence.",
                severity="high",
                raw={"command": raw, "suspect": "The Janitor"},
            ),
        )
    if cmd == "accuse lena":
        return _apply_result(
            state,
            "terminal",
            ToolResult(
                "ATTRIBUTION WARNING",
                "Lena has circumstantial motive texture but no recovered token, commit, or deployment event.",
                contradictions=[CONTRADICTIONS["lena_without_access"]],
                severity="warning",
                raw={"command": raw, "suspect": "Lena Byte"},
            ),
        )
    return _apply_result(
        state,
        "terminal",
        ToolResult(
            "COMMAND NOT FOUND",
            f"`{raw}` is not a recovered command. Type `help`.",
            severity="warning",
            raw={"command": raw},
        ),
    )
