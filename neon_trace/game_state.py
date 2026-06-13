"""Mutable in-memory state for one KERNEL-95 session."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .game_data import CLUE_ALIASES, INTRO_FEED, STARTING_EVIDENCE, SUSPECTS
from .memory import append_unique, remember_conversation


@dataclass
class GameState:
    trust: int = 55
    corruption: int = 15
    discovered_clues: list[str] = field(default_factory=list)
    theory_notes: list[str] = field(default_factory=list)
    challenged_mirror_count: int = 0
    contradiction_scans: int = 0
    mirror_wrong_hint_given: bool = False
    secret_unlocked: bool = False
    selected_evidence: str = "Corrupted Sector Log"
    feed: list[str] = field(default_factory=lambda: list(INTRO_FEED))
    unlocked_evidence: list[str] = field(default_factory=lambda: list(STARTING_EVIDENCE))
    trust_mirror_count: int = 0
    evidence_requests: int = 0
    analyzed_evidence: list[str] = field(default_factory=list)
    terminal_history: list[str] = field(default_factory=list)
    interrogations: int = 0
    accusation_submitted: bool = False
    selected_3d_object: str = "evidence_sector_log"
    selected_suspect: str = "Lena Byte"
    memory_vault_unlocked: bool = False
    known_facts: list[dict[str, Any]] = field(default_factory=list)
    known_contradictions: list[dict[str, Any]] = field(default_factory=list)
    pinned_theories: list[dict[str, Any]] = field(default_factory=list)
    mirror_claims: list[dict[str, Any]] = field(default_factory=list)
    conversation_memory: list[dict[str, str]] = field(default_factory=list)
    mirror_exchanges: list[dict[str, Any]] = field(default_factory=list)
    testimony_verdicts: list[dict[str, Any]] = field(default_factory=list)
    mirror_exchange_count: int = 0
    successful_testimony_reads: int = 0
    haunting_phrase: str = ""
    tool_trace: list[dict[str, Any]] = field(default_factory=list)
    suspect_notes: dict[str, list[str]] = field(default_factory=dict)
    suspect_stress: dict[str, int] = field(default_factory=dict)
    suspect_lies_told: dict[str, list[str]] = field(default_factory=dict)
    suspect_secrets: dict[str, str] = field(
        default_factory=lambda: {
            name: profile["secret"] for name, profile in SUSPECTS.items()
        }
    )
    suspect_pressure_thresholds: dict[str, int] = field(
        default_factory=lambda: {
            "Lena Byte": 35,
            "Father Proxy": 30,
            "N0VA": 25,
            "The Janitor": 55,
            "MIRROR": 50,
        }
    )
    mirror_confidence: int = 68
    mirror_bias_level: int = 72
    mirror_instability: int = 18
    mirror_wrong_claims: list[dict[str, Any]] = field(default_factory=list)
    mirror_correct_claims: list[dict[str, Any]] = field(default_factory=list)
    mirror_memory_audit_unlocked: bool = False
    suppressed_anomalies: list[dict[str, Any]] = field(
        default_factory=lambda: [
            {
                "id": "duplicate_j17",
                "confidence": 0.91,
                "reason": "narratively inconsistent",
                "revealed": False,
            }
        ]
    )
    unlocked_terminal_commands: list[str] = field(
        default_factory=lambda: [
            "help",
            "ls evidence",
            "cat sector_log",
            "inspect commit 7f31c9a",
            "diff memory_filter.py",
            "scan contradictions",
            "trace token J-17",
        ]
    )
    selected_os_object: str = "case_briefing_file"
    selected_file_id: str = "case_briefing"
    open_windows: list[str] = field(default_factory=lambda: ["BOOT_SEQUENCE", "CASE_BRIEFING"])
    mirror_connected: bool = False
    game_phase: str = "landing"
    current_mirror_message: str = "MIRROR.exe is offline. Establish the external link to continue."
    discovered_files: list[str] = field(
        default_factory=lambda: [
            "case_briefing",
            "boot_anomaly",
            "memory_loss_report",
            "mirror_claim_01",
            "restore_1998",
            "restore_2077",
        ]
    )
    inspected_files: list[str] = field(default_factory=list)
    deleted_files_recovered: list[str] = field(default_factory=list)
    echo_messages: list[dict[str, Any]] = field(default_factory=list)
    player_theories: list[dict[str, Any]] = field(default_factory=list)
    mirror_trust: int = 55
    system_corruption: int = 15
    echo_presence: int = 12
    evidence_integrity: int = 42
    player_skepticism: int = 0
    hidden_partition_progress: int = 0
    hidden_partition_unlocked: bool = False
    mirror_audit_unlocked: bool = False
    echo_core_unlocked: bool = False
    final_judgment_unlocked: bool = False
    final_judgment_submitted: bool = False
    ending_id: str | None = None
    ending_title: str = ""
    ending_score: int = 0
    ending_narration: str = ""
    ending_breakdown: dict[str, int] = field(default_factory=dict)
    mirror_claim_verified: bool = False
    restore_points_compared: bool = False
    demand_evidence_used: bool = False

    def adjust_trust(self, amount: int) -> None:
        self.trust = max(0, min(100, self.trust + amount))
        self.mirror_trust = self.trust

    def adjust_corruption(self, amount: int) -> None:
        self.corruption = max(0, min(100, self.corruption + amount))
        self.system_corruption = self.corruption

    def discover(self, clue: str) -> bool:
        clue = CLUE_ALIASES.get(clue, clue)
        if clue in self.discovered_clues:
            return False
        self.discovered_clues.append(clue)
        return True

    def add_feed(self, message: str) -> None:
        self.feed.append(message)
        self.feed = self.feed[-18:]

    def add_theory(self, note: str) -> bool:
        if note in self.theory_notes:
            return False
        self.theory_notes.append(note)
        return True

    def add_fact(self, fact: dict[str, Any]) -> bool:
        return append_unique(self.known_facts, fact)

    def add_contradiction(self, contradiction: dict[str, Any]) -> bool:
        return append_unique(self.known_contradictions, contradiction)

    def add_mirror_claim(self, claim: dict[str, Any]) -> bool:
        return append_unique(self.mirror_claims, claim)

    def add_conversation(
        self,
        role: str,
        content: str,
        kind: str = "dialogue",
        source: str = "",
    ) -> None:
        remember_conversation(self, role, content, kind, source)

    def adjust_bias(self, amount: int) -> None:
        self.mirror_bias_level = max(0, min(100, self.mirror_bias_level + amount))

    def adjust_instability(self, amount: int) -> None:
        self.mirror_instability = max(0, min(100, self.mirror_instability + amount))

    def adjust_hidden_progress(self, amount: int) -> None:
        self.hidden_partition_progress = max(
            0, min(100, self.hidden_partition_progress + amount)
        )

    @property
    def recovered_files(self) -> list[str]:
        """OS-facing alias retained without duplicating recovery state."""
        return self.deleted_files_recovered

    def update_os_unlocks(self) -> None:
        self.final_judgment_unlocked = (
            self.hidden_partition_unlocked
            and self.mirror_audit_unlocked
            and "echo_core" in self.discovered_files
        )

    @property
    def readiness(self) -> int:
        essential = {
            "duplicate_token",
            "janitor_commit",
            "thirteen_minute_filter",
            "victim_thirteen_minutes",
            "skipped_duplicate_test",
        }
        found = len(essential.intersection(self.discovered_clues))
        theory_bonus = min(10, max(len(self.theory_notes), len(self.pinned_theories)) * 3)
        contradiction_bonus = min(10, len(self.known_contradictions) * 2)
        return min(
            100,
            found * 14 + theory_bonus + contradiction_bonus + (10 if self.secret_unlocked else 0),
        )

    def maybe_unlock_secret(self) -> bool:
        qualified = (
            self.challenged_mirror_count >= 2
            and self.contradiction_scans >= 2
            and "duplicate_token" in self.discovered_clues
        )
        if not qualified or self.secret_unlocked:
            return False
        self.secret_unlocked = True
        self.mirror_memory_audit_unlocked = True
        self.discover("mirror_suppression")
        if "MIRROR Suppressed Anomaly" not in self.unlocked_evidence:
            self.unlocked_evidence.append("MIRROR Suppressed Anomaly")
        self.add_feed("BLACK ICE // Hidden model trace recovered: MIRROR suppressed anomaly 0.91.")
        for anomaly in self.suppressed_anomalies:
            if anomaly.get("id") == "duplicate_j17":
                anomaly["revealed"] = True
        return True

    def update_vault_access(self) -> bool:
        qualified = (
            self.challenged_mirror_count >= 2
            and self.contradiction_scans >= 2
            and "duplicate_token" in self.discovered_clues
        )
        if not qualified or self.memory_vault_unlocked:
            return False
        self.memory_vault_unlocked = True
        self.mirror_memory_audit_unlocked = True
        self.add_feed("VAULT // Suppressed memory vault access conditions satisfied.")
        return True


def new_game() -> GameState:
    state = GameState()
    state.add_conversation(
        "system",
        "Case 013 opened. KERNEL-95 is airgapped; the MIRROR link is pending.",
        kind="system",
        source="case_control",
    )
    return state
