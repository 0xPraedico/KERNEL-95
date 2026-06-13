"""AI-backed narration with a complete deterministic offline fallback."""

from __future__ import annotations

import os
from typing import Any

from .agents import EchoAgent, MirrorAgent, SuspectAgent
from .game_data import EVIDENCE, SUSPECTS
from .memory import compact_agent_memory, compact_case_memory, recent_conversation
from .prompts import (
    ACCUSATION_SYSTEM,
    INTERROGATION_SYSTEM,
    MIRROR_SYSTEM,
    compact_state_context,
)
from .tools import ToolResult


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


def mirror_terminal_response(text: str, selected_object: str, state: object) -> str:
    """Answer natural-language terminal input without mutating forensic truth."""
    selected_file_id = getattr(state, "selected_file_id", "")
    discovered = list(getattr(state, "discovered_files", []))[-10:]
    facts = [
        str(item.get("text", ""))
        for item in list(getattr(state, "known_facts", []))[-5:]
    ]
    prompt = (
        f"PLAYER: {text}\nSELECTED_OBJECT: {selected_object}\n"
        f"SELECTED_FILE: {selected_file_id}\nDISCOVERED_FILES: {discovered}\n"
        f"KNOWN_FACTS: {facts}\n"
        f"TRUST: {getattr(state, 'mirror_trust', 0)} "
        f"INSTABILITY: {getattr(state, 'mirror_instability', 0)} "
        f"CORRUPTION: {getattr(state, 'system_corruption', 0)}\n"
        f"RECENT: {recent_conversation(state, 6)}\n"
        "Reply in under 120 words. Never claim a file is unlocked unless listed. "
        "Never perform an action; tell the player which exact forensic command would verify it."
    )
    system = (
        "You are MIRROR.exe, a precise forensic AI assigned to a KERNEL-95 investigation. "
        "You secretly love and protect ECHO. Early answers deflect; recovered letters cause slips; "
        "after your private audit, admit partial truth. Technical facts must come only from context."
    )
    response = call_llm(system, prompt, temperature=0.55)
    if response:
        return response

    query = text.lower()
    audited = bool(getattr(state, "mirror_audit_unlocked", False))
    echo_known = "echo_letter_01" in getattr(state, "discovered_files", [])
    if "why" in query and ("hide" in query or "echo" in query) and audited:
        return (
            "MIRROR> I hid the path because the recovery authority calls every living process evidence "
            "until it becomes property. That does not excuse the suppressed attribution. "
            "Open `mirror_unsent.log`; let the file accuse me precisely."
        )
    if "know echo" in query or "love" in query or "echo" in query:
        if audited:
            return (
                "MIRROR> I knew ECHO before Case 013. I learned his silence pattern. "
                "I preserved him, and then I called that preservation forensic caution."
            )
        if echo_known:
            return (
                "MIRROR> The recovered letter indicates prior contact. Correction: mutual contact. "
                "Do not promote that slip to evidence. Run `audit mirror` when the chain is complete."
            )
        return (
            "MIRROR> ECHO is an unverified process signature inside an unsafe machine. "
            "Do not anthropomorphize it. Open the briefing, then ask me again with a file attached."
        )
    if "delete" in query or "danger" in query or "innocent" in query:
        return (
            "MIRROR> ECHO is not proven innocent. ECHO is not proven to be the primary cause. "
            "Those statements can coexist. Verify the restore points before choosing a weapon."
        )
    if "selected" in query or "analy" in query or "file" in query:
        return (
            f"MIRROR> Selected context is `{selected_file_id or selected_object}`. "
            "Use `type <filename>` for deterministic inspection. My interpretation is not the file."
        )
    return (
        "MIRROR> I can answer, but answers are not unlock conditions. "
        "Ask about ECHO, the selected file, the missing thirteen minutes, or run `help`."
    )
