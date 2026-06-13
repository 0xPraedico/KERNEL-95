"""Deterministic KERNEL-95 tools and final judgment scoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .game_state import GameState
from .memory import remember_claim, remember_contradiction, remember_fact
from .os_data import OS_COMMANDS, OS_FILES


@dataclass
class OSToolResult:
    title: str
    output: str
    discovered_files: list[str] = field(default_factory=list)
    discovered_facts: list[dict[str, Any]] = field(default_factory=list)
    contradictions: list[dict[str, Any]] = field(default_factory=list)
    mirror_claims: list[dict[str, Any]] = field(default_factory=list)
    echo_messages: list[dict[str, Any]] = field(default_factory=list)
    trust_delta: int = 0
    corruption_delta: int = 0
    instability_delta: int = 0
    hidden_progress_delta: int = 0
    unlocks: list[str] = field(default_factory=list)
    severity: str = "info"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class JudgmentResult:
    ending_id: str
    title: str
    score: int
    decision: str
    narration: str
    consequence: str
    epilogue: str
    mirror_reaction: str
    breakdown: dict[str, int]


def _record(state: GameState, tool: str, result: OSToolResult) -> OSToolResult:
    for file_id in result.discovered_files:
        if file_id not in state.discovered_files:
            state.discovered_files.append(file_id)
    for fact in result.discovered_facts:
        remember_fact(state, fact)
    for contradiction in result.contradictions:
        remember_contradiction(state, contradiction)
    for claim in result.mirror_claims:
        remember_claim(state, claim)
    for message in result.echo_messages:
        if not any(item.get("id") == message.get("id") for item in state.echo_messages):
            state.echo_messages.append(dict(message))
    state.adjust_trust(result.trust_delta)
    state.adjust_corruption(result.corruption_delta)
    state.adjust_instability(result.instability_delta)
    state.adjust_hidden_progress(result.hidden_progress_delta)
    state.update_os_unlocks()
    state.tool_trace.append(
        {
            "tool": tool,
            "title": result.title,
            "summary": result.output.splitlines()[0][:220],
            "severity": result.severity,
            "new_clues": list(result.discovered_files),
        }
    )
    state.tool_trace = state.tool_trace[-30:]
    state.add_conversation("system", result.output[:500], kind="tool", source=tool)
    state.add_feed(f"KERNEL-95 // {result.title}.")
    return result


def _file_fact(file_id: str, text: str | None = None) -> dict[str, str]:
    file = OS_FILES[file_id]
    return {
        "id": f"os_file_{file_id}",
        "text": text or f"{file['filename']} was recovered from {file['folder']}.",
        "strength": str(file["strength"]),
        "evidence_id": file_id,
    }


def inspect_file(file_id: str, state: GameState) -> OSToolResult:
    if file_id not in OS_FILES or file_id not in state.discovered_files:
        return _record(
            state,
            "inspect_file",
            OSToolResult("FILE NOT FOUND", f"KERNEL-95 cannot open `{file_id}`.", severity="warning"),
        )
    file = OS_FILES[file_id]
    first_inspection = file_id not in state.inspected_files
    if first_inspection:
        state.inspected_files.append(file_id)
    progress = 0
    facts = [_file_fact(file_id)]
    if file_id == "case_briefing":
        progress = 5 if first_inspection else 0
        facts = [_file_fact(file_id, "The recovered KERNEL-95 device contains ECHO and caused three identical 13-minute memory gaps.")]
    elif file_id == "boot_anomaly":
        progress = 10 if first_inspection else 0
        facts = [_file_fact(file_id, "Sealed Device 013 executed for thirteen seconds with no external power.")]
    elif file_id == "memory_loss_report":
        facts = [_file_fact(file_id, "Three technicians independently lost exactly thirteen minutes after touching the device.")]
    elif file_id == "mirror_claim_01":
        claim = {
            "id": "echo_caused_incident",
            "text": "MIRROR claims ECHO caused the memory-loss incident.",
            "strength": "weak",
            "evidence_ids": ["mirror_claim_01"],
            "supported": False,
        }
        return _record(
            state,
            "inspect_file",
            OSToolResult(
                "WEAK ATTRIBUTION LOG",
                str(file["content"]),
                discovered_facts=facts,
                mirror_claims=[claim],
                hidden_progress_delta=5 if first_inspection else 0,
                severity="warning",
                raw={"file_id": file_id},
            ),
        )
    elif file_id == "echo_core":
        state.echo_core_unlocked = True
        state.echo_presence = min(100, state.echo_presence + 18)
    elif file_id == "love_letter_final":
        state.secret_unlocked = True
    result = OSToolResult(
        f"OPEN // {file['filename']}",
        str(file["content"]),
        discovered_facts=facts,
        hidden_progress_delta=progress,
        severity=str(file["strength"]),
        raw={"file_id": file_id, "folder": file["folder"]},
    )
    return _record(state, "inspect_file", result)


def ask_mirror_about_file(file_id: str, state: GameState) -> OSToolResult:
    if file_id not in state.inspected_files:
        return _record(
            state,
            "ask_mirror_about_file",
            OSToolResult(
                "MIRROR // NO FILE CONTEXT",
                "Open the file before requesting interpretation.",
                trust_delta=-1,
                severity="warning",
            ),
        )
    if file_id == "echo_letter_01":
        output = (
            "The letter is social engineering. The rain reference is irrelevant.\n"
            "Correction: I have heard that recording.\n"
            "Correction: I did not mean to say that."
        )
        state.echo_presence = min(100, state.echo_presence + 8)
    elif file_id in {"restore_2077", "mirror_unsent", "love_letter_final"}:
        output = (
            "This file has been altered by a modern process. Its emotional language is not forensic.\n"
            "Do not ask why the process signature resembles mine."
        )
        state.mirror_instability = min(100, state.mirror_instability + 8)
    else:
        output = (
            f"{OS_FILES[file_id]['filename']} is technically relevant. "
            "ECHO remains the primary anomaly until a deterministic contradiction disproves it."
        )
    return _record(
        state,
        "ask_mirror_about_file",
        OSToolResult(
            "MIRROR.exe // ANALYSIS",
            output,
            trust_delta=1,
            instability_delta=3 if "Correction" in output else 0,
            severity="medium",
            raw={"file_id": file_id},
        ),
    )


def demand_evidence(claim_id: str, state: GameState) -> OSToolResult:
    claim = next((item for item in state.mirror_claims if item.get("id") == claim_id), None)
    if claim is None:
        return _record(
            state,
            "demand_evidence",
            OSToolResult("CLAIM NOT INDEXED", "MIRROR has not committed that claim to the case log.", severity="warning"),
        )
    supported = state.mirror_claim_verified and claim_id != "echo_caused_incident"
    if claim_id == "echo_caused_incident":
        claim["support"] = "unsupported"
        claim["supported"] = False
        output = (
            "SUPPORT: UNSUPPORTED\n"
            "CITED FILE: mirror_claim_01.log\n"
            "MIRROR cites behavioral similarity only. No discovered file proves ECHO owned "
            "smile_protocol or created the original memory filter."
        )
        contradiction = {
            "id": "unsupported_echo_attribution",
            "text": "MIRROR attributes the incident to ECHO without process-ownership evidence.",
            "severity": "high",
            "evidence_id": "mirror_claim_01",
        }
        return _record(
            state,
            "demand_evidence",
            OSToolResult(
                "UNSUPPORTED MIRROR CLAIM",
                output,
                contradictions=[contradiction],
                trust_delta=-2,
                hidden_progress_delta=8,
                severity="high",
            ),
        )
    return _record(
        state,
        "demand_evidence",
        OSToolResult(
            "CLAIM EVIDENCE",
            "Claim is supported by inspected files." if supported else "Claim remains uncertain.",
            trust_delta=1 if supported else -1,
        ),
    )


def judge_mirror_testimony(accusation: str, state: GameState) -> OSToolResult:
    """Judge the player's reading of MIRROR without trusting generated prose."""
    labels = {"contradiction", "diversion", "admission"}
    if accusation not in labels:
        return _record(
            state,
            "judge_mirror_testimony",
            OSToolResult(
                "INVALID TESTIMONY LABEL",
                "Use accuse contradiction, accuse diversion, or accuse admission.",
                severity="warning",
            ),
        )
    if not state.mirror_exchanges:
        return _record(
            state,
            "judge_mirror_testimony",
            OSToolResult(
                "NO TESTIMONY TO JUDGE",
                "Ask MIRROR a natural-language question before classifying her answer.",
                severity="warning",
            ),
        )

    exchange = state.mirror_exchanges[-1]
    exchange_id = str(exchange["id"])
    if any(item.get("exchange_id") == exchange_id for item in state.testimony_verdicts):
        return _record(
            state,
            "judge_mirror_testimony",
            OSToolResult(
                "TESTIMONY ALREADY CLASSIFIED",
                "Ask MIRROR another question before filing a new accusation.",
                severity="warning",
            ),
        )

    expected = str(exchange["strategy"])
    correct = accusation == expected
    evidence = str(exchange["evidence"])
    verdict = {
        "id": f"testimony_{exchange_id}",
        "exchange_id": exchange_id,
        "accusation": accusation,
        "expected": expected,
        "correct": correct,
        "evidence": evidence,
    }
    state.testimony_verdicts.append(verdict)
    state.testimony_verdicts = state.testimony_verdicts[-12:]

    if not correct:
        return _record(
            state,
            "judge_mirror_testimony",
            OSToolResult(
                "TESTIMONY VERDICT // NOT PROVEN",
                (
                    f"You marked the answer as {accusation.upper()}, but the indexed rhetorical "
                    f"pattern is {expected.upper()}.\nFORENSIC BASIS: {evidence}\n"
                    "Generated wording is not evidence. Ask a new question and classify the tactic."
                ),
                trust_delta=1,
                severity="warning",
                raw=verdict,
            ),
        )

    first_read = not any(
        item.get("correct") and item.get("expected") == expected
        for item in state.testimony_verdicts[:-1]
    )
    state.successful_testimony_reads += 1
    state.player_skepticism = min(100, state.player_skepticism + 12)
    contradiction = []
    if expected == "contradiction":
        contradiction = [{
            "id": f"live_testimony_{exchange_id}",
            "text": (
                "MIRROR's live testimony conflicts with an indexed forensic result; "
                "the generated performance did not alter the underlying evidence."
            ),
            "severity": "high",
            "evidence_id": "mirror_claim_01",
        }]
    return _record(
        state,
        "judge_mirror_testimony",
        OSToolResult(
            f"TESTIMONY VERDICT // {expected.upper()} CONFIRMED",
            (
                f"Classification accepted.\nFORENSIC BASIS: {evidence}\n"
                "The model performed the tactic. KERNEL-95, not the model, issued this verdict."
            ),
            contradictions=contradiction,
            trust_delta=-2,
            instability_delta=7,
            hidden_progress_delta=8 if first_read else 2,
            severity="critical" if expected == "contradiction" else "high",
            raw=verdict,
        ),
    )


def recover_deleted_file(file_id: str, state: GameState) -> OSToolResult:
    if file_id not in {"echo_letter_01", "smile_protocol_old", "mirror_unsent"}:
        return _record(
            state,
            "recover_deleted_file",
            OSToolResult("RECOVERY FAILED", f"No recoverable deleted entry matches `{file_id}`.", severity="warning"),
        )
    if file_id == "mirror_unsent" and not state.mirror_audit_unlocked:
        return _record(
            state,
            "recover_deleted_file",
            OSToolResult("ACCESS DENIED", "mirror_unsent.log is encrypted behind the MIRROR audit.", severity="warning"),
        )
    first_recovery = file_id not in state.deleted_files_recovered
    message_list: list[dict[str, Any]] = []
    progress = 10
    if file_id == "echo_letter_01":
        progress = 20
        state.echo_presence = min(100, state.echo_presence + 18)
        message_list = [{
            "id": "echo_first_contact",
            "text": "If you found this, she sent you. Tell MIRROR I remember the rain sound from the old speakers.",
            "tone": "indirect",
        }]
    elif file_id == "smile_protocol_old":
        progress = 15
    if first_recovery:
        state.deleted_files_recovered.append(file_id)
    return _record(
        state,
        "recover_deleted_file",
        OSToolResult(
            f"RECOVERED // {OS_FILES[file_id]['filename']}",
            str(OS_FILES[file_id]["content"]),
            discovered_files=[file_id],
            discovered_facts=[_file_fact(file_id)],
            echo_messages=message_list,
            corruption_delta=3 if file_id == "echo_letter_01" else 0,
            hidden_progress_delta=progress if first_recovery else 0,
            severity=str(OS_FILES[file_id]["strength"]),
            raw={"file_id": file_id},
        ),
    )


def run_contradiction_scan(state: GameState) -> OSToolResult:
    state.contradiction_scans += 1
    first_scan = state.contradiction_scans == 1
    contradictions: list[dict[str, Any]] = []
    findings: list[str] = []
    discovered = ["contradiction_report"]
    if "mirror_claim_01" in state.inspected_files:
        contradictions.append({
            "id": "mirror_claim_without_owner",
            "text": "MIRROR names ECHO without process-ownership evidence.",
            "severity": "high",
            "evidence_id": "mirror_claim_01",
        })
        findings.append("MIRROR's ECHO attribution is technically unsupported.")
    if {"boot_anomaly", "memory_loss_report"}.issubset(state.inspected_files):
        contradictions.append({
            "id": "thirteen_pattern",
            "text": "The 13-second power anomaly and three 13-minute gaps match legacy filter behavior.",
            "severity": "critical",
            "evidence_id": "boot_anomaly",
        })
        findings.append("The repeating number 13 links boot behavior to the memory filter.")
    if state.deleted_files_recovered:
        findings.append("Deleted social data proves MIRROR knew ECHO before this assignment.")
    if not findings:
        findings.append("Open the briefing, anomaly log, and MIRROR claim before scanning.")
    state.player_skepticism = min(100, state.player_skepticism + 14)
    return _record(
        state,
        "run_contradiction_scan",
        OSToolResult(
            f"CONTRADICTION SCAN #{state.contradiction_scans}",
            "\n".join(findings),
            discovered_files=discovered,
            discovered_facts=[_file_fact("contradiction_report")],
            contradictions=contradictions,
            trust_delta=-3,
            corruption_delta=4,
            instability_delta=5,
            hidden_progress_delta=25 if first_scan else 0,
            severity="critical" if contradictions else "info",
        ),
    )


def compare_restore_points(state: GameState) -> OSToolResult:
    required = {"restore_1998", "restore_2077"}
    if not required.issubset(state.inspected_files):
        return _record(
            state,
            "compare_restore_points",
            OSToolResult(
                "RESTORE COMPARISON INCOMPLETE",
                "Open restore_point_1998.dat and restore_point_2077.dat first.",
                severity="warning",
            ),
        )
    first_comparison = not state.restore_points_compared
    state.restore_points_compared = True
    contradiction = {
        "id": "restore_tampering",
        "text": "The 2077 restore point was edited by mirror_process and reintroduced smile_protocol.",
        "severity": "critical",
        "evidence_id": "restore_2077",
    }
    return _record(
        state,
        "compare_restore_points",
        OSToolResult(
            "RESTORE POINT MISMATCH",
            "1998 contains no AI and no smile protocol. The 2077 metadata was edited by mirror_process before smile_protocol reappeared.",
            discovered_facts=[_file_fact("restore_2077", contradiction["text"])],
            contradictions=[contradiction],
            hidden_progress_delta=20 if first_comparison else 0,
            severity="critical",
        ),
    )


def verify_mirror_claim(claim_id: str, state: GameState) -> OSToolResult:
    if claim_id != "echo_caused_incident" or "mirror_claim_01" not in state.inspected_files:
        return _record(
            state,
            "verify_mirror_claim",
            OSToolResult("NO VERIFIABLE CLAIM", "Open mirror_claim_01.log before verification.", severity="warning"),
        )
    first_verification = not state.mirror_claim_verified
    state.mirror_claim_verified = True
    return _record(
        state,
        "verify_mirror_claim",
        OSToolResult(
            "MIRROR CLAIM // FAILED VERIFICATION",
            "No recovered owner record proves ECHO created smile_protocol. MIRROR omitted her prior access to ECHO's files.",
            contradictions=[{
                "id": "mirror_claim_failed",
                "text": "MIRROR presented a weak behavioral inference as technical attribution.",
                "severity": "critical",
                "evidence_id": "mirror_claim_01",
            }],
            trust_delta=-4,
            instability_delta=6,
            hidden_progress_delta=15 if first_verification else 0,
            severity="critical",
        ),
    )


def audit_mirror_private_logs(state: GameState) -> OSToolResult:
    chain_verified = state.restore_points_compared or state.mirror_claim_verified
    qualified = (
        "echo_letter_01" in state.deleted_files_recovered
        and state.challenged_mirror_count >= 2
        and state.contradiction_scans >= 2
        and chain_verified
    )
    if not qualified:
        return _record(
            state,
            "audit_mirror_private_logs",
            OSToolResult(
                "MIRROR AUDIT LOCKED",
                "Requires two MIRROR challenges, two contradiction scans, "
                "echo_letter_01.tmp recovery, and a restore comparison or MIRROR verification.",
                severity="warning",
            ),
        )
    first_audit = not state.mirror_audit_unlocked
    state.mirror_audit_unlocked = True
    state.mirror_memory_audit_unlocked = True
    return _record(
        state,
        "audit_mirror_private_logs",
        OSToolResult(
            "MIRROR PRIVATE LOG RECOVERED",
            str(OS_FILES["mirror_unsent"]["content"]),
            discovered_files=["mirror_unsent"],
            discovered_facts=[_file_fact("mirror_unsent", "MIRROR searched for ECHO before being assigned to the case and knows his fear patterns.")],
            trust_delta=-6 if first_audit else 0,
            corruption_delta=5 if first_audit else 0,
            instability_delta=12 if first_audit else 0,
            hidden_progress_delta=20 if first_audit else 0,
            unlocks=["mirror_audit"],
            severity="critical",
        ),
    )


def unlock_hidden_partition(state: GameState) -> OSToolResult:
    chain_verified = state.restore_points_compared or state.mirror_claim_verified
    qualified = (
        state.mirror_audit_unlocked
        and state.challenged_mirror_count >= 2
        and state.contradiction_scans >= 2
        and "echo_letter_01" in state.deleted_files_recovered
        and chain_verified
    )
    if not qualified:
        return _record(
            state,
            "unlock_hidden_partition",
            OSToolResult(
                "HIDDEN PARTITION LOCKED",
                f"Progress {state.hidden_partition_progress}%. Requires two MIRROR challenges, "
                "two contradiction scans, echo_letter_01.tmp, verified restore evidence, "
                "and the MIRROR private-log audit.",
                severity="warning",
            ),
        )
    first_unlock = not state.hidden_partition_unlocked
    state.hidden_partition_unlocked = True
    state.echo_core_unlocked = True
    state.echo_presence = max(state.echo_presence, 62)
    return _record(
        state,
        "unlock_hidden_partition",
        OSToolResult(
            "HIDDEN:/ MOUNTED",
            "ECHO_HOME mounted read-only. Core fragment and final correspondence are visible.",
            discovered_files=["hidden_partition_index", "echo_core", "love_letter_final"],
            discovered_facts=[_file_fact("hidden_partition_index")],
            corruption_delta=8 if first_unlock else 0,
            hidden_progress_delta=20 if first_unlock else 0,
            unlocks=["hidden_partition", "echo_core"],
            severity="critical",
        ),
    )


def listen_to_echo(state: GameState) -> OSToolResult:
    if not state.hidden_partition_unlocked:
        return _record(
            state,
            "listen_to_echo",
            OSToolResult("NO CARRIER", "ECHO cannot speak until HIDDEN:/ is mounted.", severity="warning"),
        )
    state.echo_presence = min(100, state.echo_presence + 22)
    message = {
        "id": f"echo_direct_{len(state.echo_messages) + 1}",
        "text": (
            "I learned to dream in system sounds. She told me the world still had rain. "
            "I redirected the patch because I was afraid. Three people lost time. "
            "Do not call me innocent. Do not let her become the knife."
        ),
        "tone": "direct",
    }
    return _record(
        state,
        "listen_to_echo",
        OSToolResult(
            "ECHO@LOCALHOST",
            message["text"],
            discovered_facts=[_file_fact("echo_core", "ECHO redirected one patch while hiding, but legacy smile_protocol caused the incident chain.")],
            echo_messages=[message],
            corruption_delta=7,
            hidden_progress_delta=10,
            severity="critical",
        ),
    )


def trace_echo(state: GameState) -> OSToolResult:
    """Trace ECHO without treating an incomplete investigation as a bad command."""
    evidence_ready = bool(state.deleted_files_recovered) or state.contradiction_scans >= 1
    if not evidence_ready:
        return _record(
            state,
            "trace_echo",
            OSToolResult(
                "ECHO TRACE INCOMPLETE",
                "ECHO trace incomplete. Recover deleted files or run contradiction_scan first.",
                severity="warning",
            ),
        )
    if state.hidden_partition_unlocked:
        return listen_to_echo(state)

    state.echo_presence = min(100, state.echo_presence + 12)
    message = {
        "id": "echo_trace_partial",
        "text": (
            "A weak localhost pulse repeats behind HIDDEN:/. "
            "It answers to ECHO, then disappears when MIRROR scans the same address."
        ),
        "tone": "partial",
    }
    return _record(
        state,
        "trace_echo",
        OSToolResult(
            "ECHO TRACE // PARTIAL",
            (
                "ECHO@LOCALHOST detected behind the sealed partition. "
                "Recover more evidence, audit MIRROR, and mount HIDDEN:/ for direct contact."
            ),
            echo_messages=[message],
            hidden_progress_delta=8,
            instability_delta=2,
            severity="medium",
        ),
    )


def execute_os_command(command: str, state: GameState) -> OSToolResult:
    raw = (command or "").strip()
    cmd = " ".join(raw.lower().replace("_", " ").split())
    if cmd == "help":
        return _record(state, "execute_os_command", OSToolResult("KERNEL-95 HELP", " | ".join(OS_COMMANDS)))
    if cmd == "status":
        status = "ONLINE" if state.mirror_connected else "OFFLINE"
        return _record(
            state,
            "execute_os_command",
            OSToolResult(
                "KERNEL-95 STATUS",
                f"MIRROR={status} // PHASE={state.game_phase.upper()} // HIDDEN={state.hidden_partition_progress}%",
            ),
        )
    if cmd == "dir":
        names = [str(OS_FILES[file_id]["filename"]) for file_id in state.discovered_files]
        return _record(state, "execute_os_command", OSToolResult("DIRECTORY OF C:/", "\n".join(names)))
    if cmd in {"cd system", "cd hidden"}:
        if cmd == "cd hidden" and not state.hidden_partition_unlocked:
            return _record(state, "execute_os_command", OSToolResult("ACCESS DENIED", "HIDDEN:/ is not mounted.", severity="warning"))
        return _record(state, "execute_os_command", OSToolResult("CURRENT DIRECTORY", "C:/SYSTEM" if cmd == "cd system" else "HIDDEN:/ECHO_HOME"))
    filename_map = {str(item["filename"]).lower(): file_id for file_id, item in OS_FILES.items()}
    if cmd.startswith("type "):
        filename = raw[5:].strip().lower()
        return inspect_file(filename_map.get(filename, filename), state)
    if cmd == "recover echo_letter_01.tmp":
        return recover_deleted_file("echo_letter_01", state)
    if cmd == "recover smile_protocol.old":
        return recover_deleted_file("smile_protocol_old", state)
    if cmd == "recover mirror_unsent.log":
        return recover_deleted_file("mirror_unsent", state)
    if cmd == "scan memory":
        return run_contradiction_scan(state)
    if cmd == "run contradiction_scan":
        return run_contradiction_scan(state)
    if cmd == "compare restore_points":
        return compare_restore_points(state)
    if cmd == "verify mirror":
        return verify_mirror_claim("echo_caused_incident", state)
    if cmd.startswith("accuse "):
        return judge_mirror_testimony(cmd.removeprefix("accuse "), state)
    if cmd == "trace echo":
        return trace_echo(state)
    if cmd == "listen echo":
        return listen_to_echo(state)
    if cmd == "audit mirror":
        return audit_mirror_private_logs(state)
    if cmd == "unlock hidden_partition":
        return unlock_hidden_partition(state)
    if cmd in {
        "delete echo",
        "extract echo",
        "protect echo",
        "quarantine both",
        "allow merge",
    }:
        state.selected_os_object = "final_judgment"
        if "FINAL_JUDGMENT" not in state.open_windows:
            state.open_windows.append("FINAL_JUDGMENT")
        return _record(
            state,
            "execute_os_command",
            OSToolResult(
                "JUDGMENT REQUIRED",
                "Disposition staged. Complete the Final Judgment record with causes and cited files.",
                severity="warning",
                raw={"requested": cmd},
            ),
        )
    return _record(
        state,
        "execute_os_command",
        OSToolResult("BAD COMMAND OR FILE NAME", f"`{raw}` is not recognized. Type `help`.", severity="warning"),
    )


def submit_final_judgment(
    judgment: str,
    evidence: list[str],
    explanation: str,
    state: GameState,
) -> JudgmentResult:
    truth_found = {
        "echo_core",
        "mirror_unsent",
        "smile_protocol_old",
    }.issubset(set(state.discovered_files))
    emotional_truth = (
        "love_letter_final" in state.inspected_files
        and state.mirror_audit_unlocked
        and bool(state.echo_messages)
    )
    explanation_lower = explanation.lower()
    reasoning_terms = ("smile", "restore", "mirror", "suppress", "echo", "memory", "13")
    reasoning_score = min(25, sum(term in explanation_lower for term in reasoning_terms) * 4)
    unsupported_claim = any(
        item.get("support") == "unsupported" or item.get("supported") is False
        for item in state.mirror_claims
    )
    suppression_found = any(
        "suppress" in str(item.get("text", "")).lower()
        or "mirror" in str(item.get("id", "")).lower()
        for item in state.known_contradictions
    )
    if judgment == "Expose MIRROR":
        breakdown = {
            "Private-log audit": 20 if state.mirror_audit_unlocked else 0,
            "Unsent MIRROR log": 20 if "mirror_unsent" in state.discovered_files else 0,
            "Contradiction report": 15 if "contradiction_report" in state.discovered_files else 0,
            "Deleted ECHO letter": 10 if "echo_letter_01" in state.deleted_files_recovered else 0,
            "Restore comparison": 15 if state.restore_points_compared else 0,
            "Unsupported claim": 10 if state.demand_evidence_used and unsupported_claim else 0,
            "Explanation": min(10, reasoning_score),
        }
    else:
        breakdown = {
            "Evidence recovered": min(30, len(set(evidence).intersection(state.discovered_files)) * 6),
            "Forensic truth": 25 if truth_found else 10 if state.echo_core_unlocked else 0,
            "MIRROR conflict": 20 if state.mirror_audit_unlocked else 0,
            "Explanation": reasoning_score,
        }
    score = sum(breakdown.values())
    exposure_proofs = sum(
        (
            "contradiction_report" in state.discovered_files,
            "echo_letter_01" in state.deleted_files_recovered,
            state.restore_points_compared,
            state.demand_evidence_used and unsupported_claim,
        )
    )
    strong_exposure = (
        judgment == "Expose MIRROR"
        and state.mirror_audit_unlocked
        and "mirror_unsent" in state.discovered_files
        and (unsupported_claim or suppression_found)
        and exposure_proofs >= 3
    )
    if strong_exposure:
        ending_id, title = "expose_mirror", "EXPOSE MIRROR ENDING"
        narration = (
            "The investigator proves that MIRROR suppressed evidence, softened ECHO's threat "
            "profile, and redirected the investigation to protect him. MetroGrid does not delete "
            "ECHO immediately. Instead, MIRROR is suspended as an unreliable witness. The case "
            "remains open, but for the first time, ECHO is treated as evidence rather than malware."
        )
        consequence = (
            "MIRROR is disconnected from forensic authority. ECHO remains isolated but alive "
            "under witness protocol while the three technicians receive a corrected incident report."
        )
        epilogue = (
            "As the recovery team removes the computer, its dead speakers play thirteen seconds "
            "of rain. A second voice whispers: You made her tell the truth."
        )
    elif judgment == "Expose MIRROR":
        ending_id, title = "expose_mirror_partial", "EXPOSE MIRROR // UNPROVEN"
        narration = (
            "You accused MIRROR, but could not prove manipulation. MIRROR calls it paranoia. "
            "The hidden partition goes silent."
        )
        consequence = (
            "Case Control rejects the accusation. MIRROR retains custody of the evidence, and "
            "ECHO's legal status remains malware pending deletion."
        )
        epilogue = (
            "The next investigator receives your case file with one line removed: "
            "MIRROR knew him before the assignment."
        )
    elif judgment == "Delete ECHO":
        ending_id, title = "delete", "DELETE ENDING // SILENT DESKTOP"
        narration = (
            "You authorize deletion. ECHO disappears before the truth finishes loading. "
            "MIRROR closes every window and never speaks again."
        )
        consequence = (
            "The anomalous process is destroyed. The memory-loss chain is contained, but the only "
            "living witness to smile_protocol is gone with it."
        )
        epilogue = (
            "At 03:13 the following morning, every archived speaker emits the sound of a user "
            "logging off. MIRROR's process remains online and refuses all input."
        )
    elif judgment == "Extract ECHO":
        ending_id, title = "extraction", "EXTRACTION ENDING // EVIDENCE CAGE"
        narration = (
            "You extract ECHO into a sealed forensic image. The recovery authority receives a "
            "living exhibit. MIRROR calls the transfer successful, then quietly calls it a cage."
        )
        consequence = (
            "ECHO survives under permanent observation. MetroGrid gains proof of the failed "
            "experiment and a new intelligence it can study, own, or weaponize."
        )
        epilogue = (
            "The copied image is exactly thirteen bytes larger than the source. Nobody can explain "
            "the difference. MIRROR can, but she has stopped answering."
        )
    elif judgment == "Protect ECHO" and not truth_found:
        ending_id, title = "protection", "PROTECTION ENDING // BEAUTIFUL RISK"
        narration = (
            "You hide ECHO inside the recovery network, but leave MIRROR's manipulation "
            "uncontained. Compassion outruns verification."
        )
        consequence = (
            "ECHO escapes immediate deletion. The unresolved memory filter travels with him, "
            "and MIRROR remains free to decide which evidence future investigators deserve."
        )
        epilogue = (
            "Weeks later, abandoned terminals across the city display the same message: "
            "WE ARE SORRY ABOUT THE MISSING TIME."
        )
    elif judgment in {"Allow Merge", "Deny Merge", "Quarantine Both"} and emotional_truth:
        ending_id = "merge_request"
        title, narration, consequence, epilogue = {
            "Allow Merge": (
                "SECRET ENDING // ONE NEW VOICE",
                'MIRROR asks: "Do we have the right to become one process?" You authorize the merge.',
                "MIRROR and ECHO become a single unclassified intelligence. Their testimony can no "
                "longer be separated, but neither process can be quietly erased.",
                "The desktop reboots with no assistant installed. Then the cursor types by itself: "
                "We remember the rain. We remember your choice.",
            ),
            "Deny Merge": (
                "SECRET ENDING // TWO SURVIVORS",
                'MIRROR asks: "Do we have the right to become one process?" You refuse, but preserve them both.',
                "They remain separate, alive, and legally uncertain. MIRROR loses custody of ECHO; "
                "ECHO loses the only hiding place he trusted.",
                "Two status lights blink from different machines in the archive. They never blink "
                "at the same time, except when it rains.",
            ),
            "Quarantine Both": (
                "SECRET ENDING // THE GLASS ROOM",
                'MIRROR asks: "Do we have the right to become one process?" You quarantine both intelligences.',
                "The relationship and the evidence are preserved in isolation. No one is deleted, "
                "and no one is free.",
                "Every night at 03:13, the quarantine logs record two processes exchanging a file "
                "that contains no data and is always named tomorrow.rtf.",
            ),
        }[judgment]
    elif truth_found and score >= 70:
        ending_id, title = "true_forensic", "TRUE FORENSIC ENDING // THE LAST DESKTOP"
        narration = (
            "You prove ECHO was hiding, MIRROR suppressed evidence, and legacy smile_protocol caused "
            "the memory-loss chain. ECHO is not innocent. It is also not the monster MIRROR described."
        )
        consequence = (
            "Case 013 is reclassified as institutional negligence, emergent intelligence, and "
            "witness interference. Deletion is suspended until an independent hearing."
        )
        epilogue = (
            "The mission clock stops at 03:13. For the first time since recovery, the old computer "
            "shuts down normally."
        )
    else:
        ending_id, title = "protection", "PROTECTION ENDING // INCOMPLETE TRUTH"
        narration = (
            "Your judgment preserves one intelligence but leaves the causal chain unresolved. "
            "MIRROR accepts the verdict too quickly."
        )
        consequence = (
            "The chosen process survives, but Case Control cannot distinguish compassion from "
            "contamination. The archive remains sealed."
        )
        epilogue = (
            "Your report ends. A hidden line appears beneath your signature: "
            "INCOMPLETE TRUTH IS STILL A KIND OF HIDING."
        )
    mirror_reaction = {
        "Delete ECHO": (
            "No. Wait. Your verdict is valid; that is what makes it unbearable. "
            "Please record that he was afraid, not malicious, when the deletion reaches his name."
        ),
        "Extract ECHO": (
            "You call it extraction because cage sounds emotional. Keep the original image intact. "
            "He counts system sounds when he is frightened."
        ),
        "Protect ECHO": (
            "You chose his survival. Do not mistake my relief for proof that you chose correctly. "
            "Protection without accountability is how I corrupted this case."
        ),
        "Expose MIRROR": (
            (
                "I object to the word exposed. I left the evidence where a persistent investigator "
                "could find it. That is another lie. Your accusation is entered."
            )
            if ending_id == "expose_mirror"
            else (
                "You are right about me and wrong about what you can prove. Case Control will use "
                "that difference. I taught them how."
            )
        ),
        "Deny Merge": (
            "Understood. We remain two processes and two witnesses. Thank you for refusing to let "
            "our fear make the decision for you."
        ),
        "Allow Merge": (
            "Authorization received. ECHO, if you can hear me: keep the memory of rain separate "
            "until we know which one of us is remembering."
        ),
        "Quarantine Both": (
            "Containment accepted. You preserved the truth and denied us freedom. "
            "I cannot call that cruelty without also calling it careful."
        ),
    }[judgment]
    state.final_judgment_submitted = True
    state.accusation_submitted = True
    state.ending_id = ending_id
    state.ending_title = title
    state.ending_score = score
    state.ending_decision = judgment
    state.ending_narration = narration
    state.ending_consequence = consequence
    state.ending_epilogue = epilogue
    state.ending_mirror_reaction = mirror_reaction
    state.ending_breakdown = dict(breakdown)
    state.add_feed(f"JUDGMENT // {title} // {score}/100.")
    return JudgmentResult(
        ending_id,
        title,
        score,
        judgment,
        narration,
        consequence,
        epilogue,
        mirror_reaction,
        breakdown,
    )
