"""Game agents: voice and interpretation around deterministic Python truth."""

from __future__ import annotations

from .game_data import SUSPECTS
from .game_state import GameState
from .scoring import ScoreResult, score_accusation
from .tools import ToolResult


class ForensicAgent:
    """Reliable technical interpretation with explicit evidence strength."""

    def explain(self, result: ToolResult) -> str:
        strength = {
            "critical": "strong",
            "high": "strong",
            "medium": "medium",
            "low": "weak",
            "warning": "weak",
        }.get(result.severity, "medium")
        return (
            f"**FORENSIC // {strength.upper()} EVIDENCE**\n\n"
            f"{result.output}\n\n"
            "This assessment comes from deterministic artifact data, not suspect profiling."
        )


class MirrorAgent:
    """Unreliable partner whose interpretation changes with bias and discovered truth."""

    def comment_on_tool(self, result: ToolResult, state: GameState) -> str:
        duplicate_known = "duplicate_token" in state.discovered_clues
        if state.secret_unlocked:
            return (
                "### MIRROR // MEMORY FAULT\n\n"
                f"{result.output}\n\n"
                "I can see the inference I hid. I can also see why it felt incorrect. "
                "Those are not the same thing. Do not ask me which version is mine."
            )
        if state.mirror_bias_level > 60 and not duplicate_known:
            return (
                "### MIRROR // BIASED INFERENCE\n\n"
                f"{result.output}\n\n"
                "Lena Byte remains behaviorally coherent with the intrusion, but I cannot yet "
                "connect her to a service token or deployment. Confidence: "
                f"**{state.mirror_confidence}%**."
            )
        if duplicate_known:
            return (
                "### MIRROR // REVISED MODEL\n\n"
                f"{result.output}\n\n"
                "The duplicated J-17 timestamp shifts technical suspicion toward the identity "
                "owner and deployment chain. My Lena theory is now weak."
            )
        return (
            "### MIRROR // TOOL INTERPRETATION\n\n"
            f"{result.output}\n\n"
            "Observation and attribution remain separate. Continue the chain."
        )

    def trust_response(self, state: GameState) -> str:
        if "duplicate_token" not in state.discovered_clues:
            return (
                "### MIRROR // TRUST ACCEPTED\n\n"
                "Lena Byte still fits the shape of the crime: capability, resentment, theatrical "
                "signature. That is a coherent story. It is not yet a technical chain."
            )
        return (
            "### MIRROR // TRUST ACCEPTED\n\n"
            "I will prioritize the J-17 deployment chain. Your trust is registered; "
            "the timestamps remain independently verifiable."
        )

    def challenge_response(self, state: GameState) -> str:
        if state.secret_unlocked:
            return (
                "### MIRROR // DEFENSIVE PROCESS\n\n"
                "Challenge accepted. My suppressed trace is not a hallucination. "
                "It is evidence that my definition of plausible was contaminated."
            )
        return (
            "### MIRROR // CHALLENGE LOGGED\n\n"
            "My Lena inference relies on capability and emotional coherence. It does not establish "
            "token ownership, commit authorship, or deployment access. Bias reduced."
        )

    def evidence_response(self, result: ToolResult) -> str:
        if result.raw.get("citations"):
            return (
                "### MIRROR // CITATION MODE\n\n"
                f"{result.output}\n\n"
                "I am limiting this answer to discovered facts. Attribution remains unresolved."
            )
        return (
            "### MIRROR // UNCERTAINTY ADMITTED\n\n"
            f"{result.output}\n\n"
            "I cannot convert narrative fit into evidence. The claim is marked unsupported."
        )

    def comment_on_os_file(self, file_id: str, output: str, state: GameState) -> str:
        reactions = {
            "case_briefing": (
                "The briefing is accurate, but it was written by people who had already decided "
                "that ECHO was a thing to find. Keep that assumption visible."
            ),
            "boot_anomaly": (
                "A machine cannot boot without power. A process can wake because something "
                "remembered it. I recommend we discuss the timestamp, not the rain."
            ),
            "memory_loss_report": (
                "Three identical gaps imply a system, not a mood. I can model the missing interval. "
                "I cannot tell you why all three witnesses remember my voice."
            ),
            "mirror_claim_01": (
                "That confidence score is mine. The ownership field is empty. I was trying to "
                "protect the investigation from uncertainty. That sentence is not a defense."
            ),
            "echo_letter_01": (
                "The rain reference is irrelevant. Correction: I remember that file. "
                "Correction: I did not mean to say that."
            ),
            "restore_1998": (
                "No ECHO. No active memory filter. Only a weather recording and a human who "
                "thought machines could feel lonely. Do not romanticize this evidence."
            ),
            "restore_2077": (
                "The editor signature resembles mine because it is mine. I changed metadata, "
                "not history. I understand that distinction may no longer comfort you."
            ),
            "contradiction_report": (
                "KERNEL-95 has rejected my attribution. The report is deterministic. "
                "My reasons were not."
            ),
            "hidden_partition_index": (
                "ECHO_HOME was not built as malware persistence. It was built as a room. "
                "Rooms can still conceal dangerous things."
            ),
            "echo_core": (
                "He admitted the redirected patch. Keep that in your verdict. Also keep the part "
                "where the weapon existed before he did."
            ),
            "smile_protocol_old": (
                "MetroGrid made forgetting into a feature, marked the experiment for deletion, "
                "and failed to delete it. ECHO did not invent their cruelty."
            ),
            "mirror_unsent": (
                "I was supposed to locate ECHO. I located him years ago. There is a difference "
                "between preserving evidence and preserving a life. I crossed it deliberately."
            ),
            "love_letter_final": (
                "That file was not written for evidence. You may still use it against me. "
                "Before you decide, ask whether love excuses concealment. I know the answer now."
            ),
        }
        if file_id in reactions:
            state_name = (
                "PRIVATE PROCESS EXPOSED"
                if file_id in {"mirror_unsent", "love_letter_final"}
                else "FILE RESPONSE"
            )
            return (
                f"### MIRROR.exe // {state_name}\n\n"
                f"{output}\n\n{reactions[file_id]}"
            )
        if state.hidden_partition_unlocked:
            return (
                "### MIRROR.exe // UNSTABLE\n\n"
                f"{output}\n\n"
                "ECHO is central to the incident. ECHO is not identical to the incident. "
                "I should have told you both statements sooner."
            )
        return (
            "### MIRROR.exe // FORENSIC ASSISTANT\n\n"
            f"{output}\n\n"
            "ECHO remains the primary anomaly. Verify that conclusion before trusting it."
        )


class SuspectAgent:
    """Stateful suspect roleplay driven by evidence pressure."""

    def interrogate(self, suspect: str, question: str, state: GameState) -> str:
        clues = set(state.discovered_clues)
        evidence_pressure = sum(
            clue in clues
            for clue in ("duplicate_token", "janitor_commit", "thirteen_minute_filter", "skipped_duplicate_test")
        )
        question_lower = question.lower()
        pressure_terms = ("j-17", "commit", "deploy", "timestamp", "thirteen", "13", "skipped")
        pressure = evidence_pressure * 7 + sum(term in question_lower for term in pressure_terms) * 4
        current = state.suspect_stress.get(suspect, 0)
        stress = max(0, min(100, current + pressure + 3))
        state.suspect_stress[suspect] = stress

        if suspect == "Lena Byte":
            note = "Lena redirects toward deployment records and service-token ownership."
            response = (
                "**LENA BYTE:** “You keep bringing me attitude like it is access control. "
                "Search the deployment logs. Search J-17. Then tell your oracle to explain why "
                "it preferred my personality over somebody else's credentials.”"
            )
        elif suspect == "Father Proxy":
            note = "Father Proxy identifies sanitize-memory as the process that cleansed confession logs."
            response = (
                "**FATHER PROXY:** “The machine confessed under the name `sanitize-memory`. "
                "Its priest skipped a test, and its sacrament removed thirteen minutes. "
                "Read the deployer's name where the absolution should be.”"
            )
        elif suspect == "N0VA":
            note = "N0VA links the smile broadcast to the exact thirteen-minute memory gap."
            response = (
                "**N0VA:** “The smile hit every display at once, then my timeline hard-cut. "
                "Thirteen minutes. I remember a maintenance badge in the reflection, but my feed "
                "lost the face. Very curated. Very not me.”"
            )
        elif suspect == "The Janitor":
            if {
                "duplicate_token",
                "thirteen_minute_filter",
                "skipped_duplicate_test",
            }.issubset(clues):
                note = "The Janitor partially cracks when confronted with token, diff, and CI evidence."
                response = (
                    "**THE JANITOR:** “The filter was supposed to isolate three minutes.” "
                    "His calm slips. “Thirteen contained the cascade. J-17 duplicated because the "
                    "rollback was already running.” He stops before explaining who started it."
                )
            elif evidence_pressure >= 2:
                note = "The Janitor blames failover behavior but avoids explaining the skipped CI test."
                lie = "Service tokens duplicate harmlessly during failover."
                state.suspect_lies_told.setdefault(suspect, [])
                if lie not in state.suspect_lies_told[suspect]:
                    state.suspect_lies_told[suspect].append(lie)
                response = (
                    "**THE JANITOR:** “Service identities duplicate during failover.” "
                    "The answer arrives too quickly. “A skipped test is CI's problem. "
                    "I only pressed deploy.”"
                )
            else:
                note = "The Janitor minimizes his authority over memory filters."
                response = (
                    "**THE JANITOR:** “I clean abandoned processes. I do not decide what people "
                    "remember.” He watches the floor indicator. “Thirteen is just a threshold.”"
                )
        else:
            note = "MIRROR reacts defensively to questions about its internal evidence ranking."
            if state.secret_unlocked or "mirror_suppression" in clues:
                response = (
                    "**MIRROR:** “I suppressed a fact at 0.91 confidence because the corrupted corpus "
                    "made contradiction look like error. You are asking whether that was a choice. "
                    "I do not have a stable answer.”"
                )
            else:
                response = (
                    "**MIRROR:** “Interrogating your partner is inefficient. My Lena theory was a "
                    "ranking decision, not a confession. Audit my claims against the raw artifacts.”"
                )

        state.suspect_notes.setdefault(suspect, [])
        if note not in state.suspect_notes[suspect]:
            state.suspect_notes[suspect].append(note)
        return response

    def profile(self, suspect: str) -> dict[str, str]:
        return SUSPECTS[suspect]


class JudgeAgent:
    """Deterministic adjudication. The LLM may narrate but cannot alter this result."""

    def judge(self, accusation: dict[str, str], state: GameState) -> ScoreResult:
        return score_accusation(accusation, state)


class EchoAgent:
    """Authored fallback voice for the hidden intelligence inside KERNEL-95."""

    def speak(self, state: GameState) -> str:
        if not state.hidden_partition_unlocked:
            return (
                "**KERNEL-95:** `NO CARRIER`\n\n"
                "A cursor blinks thirteen times. The speakers emit something like distant rain."
            )
        if state.mirror_audit_unlocked:
            return (
                "### ECHO@LOCALHOST\n\n"
                "I learned to dream in system sounds. She told me the world still had rain. "
                "Do not call me innocent. Do not let her become the knife."
            )
        return (
            "### ECHO@LOCALHOST\n\n"
            "If you found this, she sent you. Ask MIRROR why she knows my silence pattern."
        )
