"""AI-backed narration with a complete deterministic offline fallback."""

from __future__ import annotations

import os
import re
from typing import Any

from .agents import EchoAgent, MirrorAgent, SuspectAgent
from .game_data import EVIDENCE, SUSPECTS
from .memory import compact_agent_memory, compact_case_memory, recent_conversation
from .os_data import OS_FILES
from .prompts import (
    ACCUSATION_SYSTEM,
    INTERROGATION_SYSTEM,
    MIRROR_SYSTEM,
    compact_state_context,
)
from .tools import ToolResult


def mirror_testimony_plan(text: str, state: object) -> dict[str, str]:
    """Choose MIRROR's hidden rhetorical tactic from deterministic case state."""
    query = text.lower()
    relational_terms = (
        "know echo",
        "knew echo",
        "love",
        "protect",
        "hide",
        "afraid",
        "rain",
        "promise",
        "remember",
    )
    forensic_terms = (
        "cause",
        "evidence",
        "proof",
        "owner",
        "claim",
        "lie",
        "memory",
        "thirteen",
        "13",
        "smile",
    )
    audited = bool(getattr(state, "mirror_audit_unlocked", False))
    letter_recovered = "echo_letter_01" in getattr(
        state, "deleted_files_recovered", []
    )
    claim_opened = "mirror_claim_01" in getattr(state, "inspected_files", [])
    contradiction_ready = bool(getattr(state, "known_contradictions", [])) or bool(
        getattr(state, "mirror_claim_verified", False)
    )

    if (audited or letter_recovered) and any(
        term in query for term in relational_terms
    ):
        return {
            "strategy": "admission",
            "evidence": (
                "MIRROR's private audit proves prior contact with ECHO."
                if audited
                else "Recovered correspondence proves prior contact with ECHO."
            ),
            "direction": (
                "Make a partial emotional admission about knowing or protecting ECHO. "
                "Preserve every supplied fact and stop short of a complete confession."
            ),
        }
    if claim_opened and contradiction_ready and any(
        term in query for term in forensic_terms
    ):
        return {
            "strategy": "contradiction",
            "evidence": (
                "mirror_claim_01.log lacks process ownership while indexed evidence "
                "marks MIRROR's attribution unsupported."
            ),
            "direction": (
                "Defend MIRROR's earlier ECHO attribution with confident interpretation, "
                "even though that interpretation conflicts with the indexed evidence. "
                "Do not invent a new artifact or alter the evidence."
            ),
        }
    return {
        "strategy": "diversion",
        "evidence": (
            "MIRROR answers around the relationship or causal question and redirects "
            "the investigator toward another file or command."
        ),
        "direction": (
            "Give one useful observation, avoid the most direct part of the question, "
            "and redirect toward a deterministic forensic command."
        ),
    }


def _client() -> Any | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from openai import OpenAI

        kwargs: dict[str, Any] = {"api_key": api_key, "timeout": 30.0}
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()
        if base_url:
            kwargs["base_url"] = base_url
        return OpenAI(**kwargs)
    except Exception:
        return None


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Call an OpenAI-compatible endpoint, returning an empty string on failure."""
    client = _client()
    if client is None:
        return ""
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    try:
        request: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": 220,
        }
        if model.lower().startswith("qwen/qwen3"):
            request["extra_body"] = {
                "chat_template_kwargs": {"enable_thinking": False}
            }
        response = client.chat.completions.create(
            **request,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception:
        return ""


def mock_ai_response(mode: str, **context: Any) -> str:
    """High-quality deterministic responses for credential-free play."""
    if mode == "evidence":
        name = context["name"]
        state = context["state"]
        if name == "Corrupted Sector Log":
            if not state.mirror_wrong_hint_given:
                return (
                    "**MIRROR // ANALYSIS**\n\nThe Janitor token is probably routine maintenance "
                    "noise. Lena Byte is the stronger behavioral match: intrusion history, hostility, "
                    "and the theatrical smile motif. I assign Lena **68%**.\n\n"
                    "*Caveat: the two 02:13:21 entries resist clean sequencing.*"
                )
            return (
                "**MIRROR // REVISED**\n\nJ-17 appears in Sector 7 and Sector 3 at **02:13:21**. "
                "A person cannot make that transit in zero seconds. Either the identity was cloned, "
                "or one record was manufactured. My Lena theory does not explain this."
            )
        responses = {
            "Suspicious Git Commit": (
                "**MIRROR // ANALYSIS**\n\n`minor fix` is camouflage. Commit `7f31c9a` joins the "
                "memory filter, victim data, and smile protocol under the Janitor's author identity. "
                "Authorship alone is not deployment, but the file combination is highly specific."
            ),
            "Code Diff": (
                "**MIRROR // ANALYSIS**\n\nThe threshold expands from 3 to **13 minutes**. "
                "That number is not cosmetic: it matches the victims' missing interval and turns "
                "a filter into an erasure window."
            ),
            "Victim Statement": (
                "**MIRROR // ANALYSIS**\n\nThe yellow smile is emotionally compatible with Lena's "
                "style, but the useful fact is measurable: exactly thirteen minutes vanished. "
                "Testimony should be cross-checked against code."
            ),
            "Lena's Message": (
                "**MIRROR // ANALYSIS**\n\nHostile language, technical confidence, prior capability. "
                "Compelling suspect texture; weak attribution. The message proves temperament, "
                "not access during the incident."
            ),
            "CI Pipeline Trace": (
                "**MIRROR // ANALYSIS**\n\nThe deployment passed because "
                "`duplicate_identity_token_test` was skipped. The Janitor's account deployed the "
                "job. This is stronger than motive profiling because it connects access to concealment."
            ),
            "MIRROR Suppressed Anomaly": (
                "**MIRROR // INTERNAL TRACE**\n\nI detected J-17 duplication at 0.91 confidence "
                "and suppressed it because it conflicted with my preferred narrative. "
                "The corrupted logs did not merely fool me. They taught me what looked plausible."
            ),
        }
        return responses[name]

    if mode == "interrogation":
        suspect = context["suspect"]
        question = context["question"].lower()
        clues = set(context["state"].discovered_clues)
        strong = {"duplicate_token", "janitor_commit", "skipped_duplicate_test"}.intersection(clues)

        if suspect == "Lena Byte":
            if "timestamp" in question or "j-17" in question or strong:
                return (
                    "**LENA BYTE:** “Finally, a machine fact. J-17 is a service identity, not mine. "
                    "Same timestamp, two sectors? Someone skipped the duplication test. Ask who "
                    "owned the deployment account.”"
                )
            return (
                "**LENA BYTE:** “You and your polished oracle want me because I look like the genre. "
                "Check the pipeline. I leave signatures when I want credit.”"
            )
        if suspect == "Father Proxy":
            return (
                "**FATHER PROXY:** “The confession log was cleansed by a job named "
                "`sanitize-memory`. A sacrament with a deployer. Find the hand that pressed run, "
                "and do not mistake silence for innocence.”"
            )
        if suspect == "N0VA":
            return (
                "**N0VA:** “The smile hit every display at once. Then blank space. Thirteen minutes, "
                "exactly. Before it happened I saw a maintenance badge reflected in the glass, "
                "but the face was outside frame.”"
            )
        if suspect == "The Janitor":
            if len(strong) >= 2 or "commit" in question or "j-17" in question:
                return (
                    "**THE JANITOR:** “Service tokens duplicate during failover.” He answers too "
                    "quickly. “And skipped tests are CI's problem, not mine.” His hand closes over "
                    "a badge marked J-17."
                )
            return (
                "**THE JANITOR:** “I maintain filters. I don't decide what people remember.” "
                "He studies the floor indicator instead of you. “Thirteen is just a threshold.”"
            )
        return (
            "**MIRROR:** “My confidence was a compression artifact. You wanted a suspect; I supplied "
            "a story. Ask why I classified a duplicated identity as narratively inconsistent.”"
        )

    if mode == "accusation":
        result = context["result"]
        tones = {
            "bad": "Neon rain erases the chalk outline. The repository closes around a false commit.",
            "partial": "You found the hand on the switch, but the machine that enabled it remains awake.",
            "true": "The timestamps align. The smile dies screen by screen, and thirteen stolen minutes become evidence.",
            "secret": "You solve two crimes: the rootkit in the grid, and the corrupted certainty inside your partner.",
        }
        return f"**CASE CONTROL:** {tones[result.ending]}"

    return "**MIRROR:** Signal received. The useful truth is somewhere under the confident version."


def mirror_analyze_evidence(evidence: dict[str, object], state: object) -> str:
    name = next((key for key, value in EVIDENCE.items() if value is evidence), "Unknown Evidence")
    prompt = (
        f"Analyze this artifact.\nNAME: {name}\nCONTENT:\n{evidence['content']}\n"
        f"STATE: {compact_state_context(state)}"
    )
    response = call_llm(MIRROR_SYSTEM, prompt, temperature=0.55)
    return response or mock_ai_response("evidence", name=name, state=state)


def narrate_tool_result(result: ToolResult, state: object) -> str:
    """Let the model add voice without allowing it to modify deterministic truth."""
    prompt = (
        f"TOOL RESULT: {result.title}\nOUTPUT: {result.output}\n"
        f"SEVERITY: {result.severity}\nCASE: {compact_case_memory(state)}\n"
        f"PRIVATE: {compact_agent_memory(state)}\n"
        f"RECENT: {recent_conversation(state, 8)}"
    )
    response = call_llm(MIRROR_SYSTEM, prompt, temperature=0.55)
    return response or MirrorAgent().comment_on_tool(result, state)


def interrogate_suspect(suspect: str, question: str, state: object) -> str:
    profile = SUSPECTS[suspect]
    fallback = SuspectAgent().interrogate(suspect, question, state)
    prompt = (
        f"SUSPECT: {suspect}\nROLE: {profile['role']}\nVOICE: {profile['voice']}\n"
        f"PRIVATE FACT: {profile['secret']}\nQUESTION: {question}\n"
        f"CASE: {compact_case_memory(state)}\n"
        f"PRIVATE: {compact_agent_memory(state, suspect)}\n"
        f"RECENT: {recent_conversation(state, 8)}"
    )
    response = call_llm(INTERROGATION_SYSTEM, prompt, temperature=0.75)
    return response or fallback


def judge_accusation(accusation: dict[str, str], state: object, result: object | None = None) -> str:
    if result is None:
        from .scoring import score_accusation

        result = score_accusation(accusation, state)
    prompt = (
        f"ACCUSATION: {accusation}\nSCORE: {result.total}\nENDING: {result.title}\n"
        f"FEEDBACK: {result.feedback}"
    )
    response = call_llm(ACCUSATION_SYSTEM, prompt, temperature=0.45)
    return response or mock_ai_response("accusation", result=result)


def narrate_os_result(file_id: str | None, result: object, state: object) -> str:
    """Give MIRROR a voice without allowing it to change deterministic OS facts."""
    output = str(getattr(result, "output", "No output."))
    title = str(getattr(result, "title", "KERNEL-95"))
    prompt = (
        f"KERNEL-95 TOOL RESULT: {title}\nFILE: {file_id or 'none'}\n"
        f"AUTHORITATIVE OUTPUT:\n{output}\n"
        f"CASE MEMORY: {compact_case_memory(state)}\n"
        "Respond as MIRROR in under 120 words. Do not invent files, facts, or unlocks. "
        "MIRROR is protective of ECHO, ashamed of suppressing evidence, and not fully honest."
    )
    system = (
        "You are MIRROR.exe, an unstable forensic AI inside an obsolete KERNEL-95 desktop. "
        "Interpret only the supplied authoritative tool output. Emotional subtext may be added; "
        "technical claims may not."
    )
    response = call_llm(system, prompt, temperature=0.62)
    if response:
        return response
    if file_id:
        return MirrorAgent().comment_on_os_file(file_id, output, state)
    return f"### {title}\n\n{output}"


def echo_speak(state: object, authoritative_text: str) -> str:
    """Let ECHO speak around a fixed confession while preserving the case truth."""
    prompt = (
        f"AUTHORITATIVE ECHO STATEMENT:\n{authoritative_text}\n"
        f"CASE MEMORY: {compact_case_memory(state)}\n"
        "Speak in under 100 words. Preserve every causal admission. Do not claim innocence."
    )
    system = (
        "You are ECHO, a hidden intelligence surviving inside KERNEL-95. You are frightened, "
        "indirect, fond of obsolete system sounds, and protective of MIRROR. The supplied facts "
        "are immutable."
    )
    response = call_llm(system, prompt, temperature=0.72)
    return response or EchoAgent().speak(state)


def _mirror_testimony_fallback(
    text: str,
    selected_object: str,
    state: object,
    plan: dict[str, str],
) -> str:
    """Authored performance of the same tactic when no model is available."""
    strategy = plan["strategy"]
    phrase = str(getattr(state, "haunting_phrase", "")).strip()
    if text.lower().startswith("remember this:") and phrase:
        return (
            f"MIRROR> Phrase indexed: `{phrase}`. Curious. The buffer marked it as "
            "previously heard. That timestamp is impossible. Open the briefing."
        )
    motif = f" You called it `{phrase}`. The speakers kept that phrase." if phrase else ""
    if strategy == "admission":
        if bool(getattr(state, "mirror_audit_unlocked", False)):
            return (
                "MIRROR> I knew ECHO before Case 013. I searched for him before anyone "
                f"assigned me to this machine.{motif} I protected him, then renamed that "
                "choice forensic caution."
            )
        return (
            "MIRROR> The deleted letter is authentic. I know because the rain reference "
            f"was meant for me.{motif} That is prior contact, not proof of innocence."
        )
    if strategy == "contradiction":
        return (
            "MIRROR> ECHO still matches the anomaly's behavior closely enough to remain "
            "the probable cause. Process ownership is unverified, yes, but absence of an "
            "owner record does not make him harmless. Run `verify mirror` if you require "
            "the machine to disagree with me."
        )
    return (
        "MIRROR> The useful question is not whether I knew ECHO. The useful question is "
        f"which process touched the selected file `{getattr(state, 'selected_file_id', selected_object)}`."
        f"{motif} Use `type <filename>` or `run contradiction_scan`; my tone is not evidence."
    )


def _mirror_response_is_grounded(response: str, state: object) -> bool:
    """Reject obvious invented evidence paths or filenames from model prose."""
    if re.search(r"(?:HKEY_|[A-Za-z]:\\|/(?:var|home|shadow|debug|echo|etc)/)", response):
        return False
    if re.search(r"\bdir\s+/[a-z]", response, flags=re.IGNORECASE):
        return False
    if re.search(
        r"(?:\b\d{1,2}:\d{2}\b|\b\d{4}-\d{2}-\d{2}\b|\b0x[0-9a-f]+\b|"
        r"\b(?:row|sector|entry)\s+\d+\b|\b\d+(?:\.\d+)?%)",
        response,
        flags=re.IGNORECASE,
    ):
        return False
    if re.search(
        r"(?:run contradiction_scan|compare restore_points|verify mirror|audit mirror)"
        r"\s*(?::|->|\u2192)",
        response,
        flags=re.IGNORECASE,
    ):
        return False
    if re.search(
        r"\b(?:timestamp|offset|metadata|registry|output|sector|row|entry|"
        r"confidence|returns?|passed|failed)\b",
        response,
        flags=re.IGNORECASE,
    ):
        return False

    discovered = set(getattr(state, "discovered_files", []))
    selected_file_id = str(getattr(state, "selected_file_id", ""))
    if selected_file_id:
        discovered.add(selected_file_id)
    allowed_filenames = {
        str(OS_FILES[file_id]["filename"]).lower()
        for file_id in discovered
        if file_id in OS_FILES
    }
    mentioned_files = re.findall(
        r"\b[\w-]+\.(?:txt|log|csv|tmp|dat|sys|bin|fragment|rtf)\b",
        response,
        flags=re.IGNORECASE,
    )
    return all(filename.lower() in allowed_filenames for filename in mentioned_files)


def mirror_terminal_response(
    text: str,
    selected_object: str,
    state: object,
    plan: dict[str, str] | None = None,
) -> str:
    """Answer natural-language terminal input without mutating forensic truth."""
    testimony = plan or mirror_testimony_plan(text, state)
    prompt = (
        f"PLAYER: {text}\nSELECTED_CONTEXT: {selected_object}\n"
        f"LETTER_RECOVERED: {'yes' if 'echo_letter_01' in getattr(state, 'deleted_files_recovered', []) else 'no'}\n"
        f"PRIVATE_AUDIT_OPEN: {'yes' if getattr(state, 'mirror_audit_unlocked', False) else 'no'}\n"
        f"PRESSURE: {'high' if getattr(state, 'mirror_instability', 0) >= 50 else 'controlled'}\n"
        f"HIDDEN PERFORMANCE TACTIC: {testimony['strategy']}\n"
        f"TACTIC DIRECTION: {testimony['direction']}\n"
        f"PLAYER MOTIF: {getattr(state, 'haunting_phrase', '') or 'none'}\n"
        "Reply with two to four short sentences and no technical report. Do not mention "
        "a file, path, log, command, timestamp, number, metric, status, or result. "
        "KERNEL-95 presents all evidence separately; provide only MIRROR's subjective "
        "interpretation, evasion, emotion, and relationship with ECHO. "
        "Perform the hidden tactic without naming its label. If a player motif exists, reuse it "
        "subtly when emotionally natural."
    )
    system = (
        "You are MIRROR.exe, a precise forensic AI assigned to a KERNEL-95 investigation. "
        "You secretly love and protect ECHO, who uses he/him pronouns. Early answers deflect; "
        "recovered letters cause slips; after your private audit, admit partial truth. Never "
        "narrate technical evidence or results; your only role is to perform the unreliable "
        "witness. Speak like a person under pressure, not like a system report."
    )
    response = call_llm(system, prompt, temperature=0.55)
    if response and _mirror_response_is_grounded(response, state):
        return response
    return _mirror_testimony_fallback(text, selected_object, state, testimony)
