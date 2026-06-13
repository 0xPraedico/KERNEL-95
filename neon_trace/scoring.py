"""Deterministic accusation scoring and endings."""

from __future__ import annotations

from dataclasses import dataclass

from .game_state import GameState


@dataclass(frozen=True)
class ScoreResult:
    total: int
    ending: str
    title: str
    breakdown: dict[str, int]
    feedback: list[str]


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def score_accusation(accusation: dict[str, str], state: GameState) -> ScoreResult:
    culprit = accusation.get("culprit", "")
    motive = accusation.get("motive", "")
    evidence = accusation.get("evidence", "")
    explanation = accusation.get("explanation", "")
    breakdown: dict[str, int] = {}
    feedback: list[str] = []

    breakdown["Culprit"] = 30 if culprit == "The Janitor" else 0
    if breakdown["Culprit"]:
        feedback.append("Attribution: The Janitor is correctly identified.")
    else:
        feedback.append("Attribution failed: the selected suspect does not control the full chain.")

    motive_terms = (
        "experiment",
        "memory filter",
        "memory-filter",
        "hide",
        "cover",
        "failed",
        "thirteen",
        "13",
    )
    motive_hits = sum(term in motive.lower() for term in motive_terms)
    breakdown["Motive"] = min(20, motive_hits * 4)
    if breakdown["Motive"] >= 12:
        feedback.append("Motive: the failed memory-filter cover-up is substantially explained.")
    else:
        feedback.append("Motive needs the failed experiment, cover-up, and 13-minute loss.")

    correct_evidence = evidence in {
        "Duplicated J-17 timestamp",
        "CI skipped test",
        "MIRROR suppressed anomaly",
    }
    breakdown["Key evidence"] = 20 if correct_evidence else 6 if evidence in {
        "Commit 7f31c9a",
        "13-minute code diff",
    } else 0
    if correct_evidence:
        feedback.append("Evidence: the selected artifact exposes identity or pipeline contradiction.")
    else:
        feedback.append("Evidence is relevant but not the strongest technical attribution.")

    technical_terms = (
        "j-17",
        "same time",
        "same timestamp",
        "02:13:21",
        "sector 3",
        "sector_3",
        "sector 7",
        "sector_7",
        "duplicate",
        "skipped test",
        "deployed",
    )
    technical_hits = sum(term in explanation.lower() for term in technical_terms)
    breakdown["Technical reasoning"] = min(20, technical_hits * 3)
    if _contains_any(explanation, ("because", "therefore", "which means", "proves")):
        breakdown["Technical reasoning"] = min(20, breakdown["Technical reasoning"] + 2)
    if breakdown["Technical reasoning"] >= 14:
        feedback.append("Reasoning: raw events are connected to attribution, timing, and concealment.")
    else:
        feedback.append("Reasoning should connect J-17, both sectors, 02:13:21, and the skipped test.")

    skepticism = state.challenged_mirror_count + state.contradiction_scans
    trust_penalty = min(10, max(0, state.trust_mirror_count - skepticism) * 3)
    breakdown["Investigator discipline"] = 10 - trust_penalty
    if trust_penalty:
        feedback.append(f"Trust penalty: -{trust_penalty} for accepting MIRROR faster than verifying it.")
    else:
        feedback.append("Investigator discipline: MIRROR's claims were independently tested.")

    total = sum(breakdown.values())
    culprit_correct = culprit == "The Janitor"
    system_failure_found = (
        breakdown["Motive"] >= 12
        and breakdown["Technical reasoning"] >= 12
        and "duplicate_token" in state.discovered_clues
    )
    secret_proven = state.secret_unlocked and system_failure_found

    if not culprit_correct:
        ending = "bad"
        title = "BAD ENDING // THE WRONG SUSPECT BURNS"
    elif secret_proven and total >= 78:
        ending = "secret"
        title = "SECRET ENDING // THE MIRROR BLINKS"
    elif system_failure_found and total >= 70:
        ending = "true"
        title = "TRUE ENDING // THE SMILING ROOTKIT"
    else:
        ending = "partial"
        title = "PARTIAL ENDING // CULPRIT, NOT CAUSE"

    return ScoreResult(total, ending, title, breakdown, feedback)
