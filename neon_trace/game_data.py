"""Static case data for The Smiling Rootkit."""

from __future__ import annotations

CASE_TITLE = "The Smiling Rootkit"
CULPRIT = "The Janitor"

EVIDENCE: dict[str, dict[str, object]] = {
    "Corrupted Sector Log": {
        "id": "sector_log",
        "kind": "SYSTEM LOG",
        "summary": "Recovered authentication and process events from the night of the incident.",
        "content": """[02:13:09] AUTH_SUCCESS user=janitor token=J-17
[02:13:11] CAMERA_FEED disabled sector=7
[02:13:13] MEMORY_PATCH injected process=smile_protocol
[02:13:21] user=janitor token=J-17 location=Sector_7
[02:13:21] user=janitor token=J-17 location=Sector_3
[02:13:34] SMILE_PROTOCOL active""",
        "clue": "duplicate_token",
    },
    "Suspicious Git Commit": {
        "id": "commit_7f31c9a",
        "kind": "GIT OBJECT",
        "summary": "A bland commit message wrapped around three highly specific files.",
        "content": """commit 7f31c9a
author: janitor@metrogrid.local
message: "minor fix"

files changed:
  memory_filter.py
  victims.csv
  smile_protocol.py""",
        "clue": "janitor_commit",
    },
    "Code Diff": {
        "id": "memory_filter_diff",
        "kind": "PATCH",
        "summary": "The memory filter threshold changed immediately before deployment.",
        "content": """--- a/memory_filter.py
+++ b/memory_filter.py
- if memory_window <= 3:
+ if memory_window <= 13:
      erase_recent_events(subject)""",
        "clue": "thirteen_minute_filter",
    },
    "Victim Statement": {
        "id": "victim_statement",
        "kind": "TESTIMONY",
        "summary": "A victim describes a repeated visual artifact and a precise memory gap.",
        "content": '"I saw a yellow smile on every screen. Then I lost exactly thirteen minutes."',
        "clue": "victim_thirteen_minutes",
    },
    "Lena's Message": {
        "id": "lena_message",
        "kind": "MESSAGE",
        "summary": "Defensive, confident, and suspicious enough to be convenient.",
        "content": '"I wrote exploits, not ghosts. If I wanted the grid down, it would stay down."',
        "clue": "lena_red_herring",
    },
    "CI Pipeline Trace": {
        "id": "ci_trace",
        "kind": "CI TRACE",
        "summary": "A passing deployment with one strategically skipped test.",
        "content": """job: sanitize-memory
status: passed
warning: test skipped: duplicate_identity_token_test
deployed_by: janitor@metrogrid.local""",
        "clue": "skipped_duplicate_test",
    },
    "MIRROR Suppressed Anomaly": {
        "id": "mirror_suppressed_anomaly",
        "kind": "HIDDEN MODEL TRACE",
        "summary": "An internal inference MIRROR chose not to show you.",
        "content": (
            'MIRROR flagged token J-17 duplication at confidence 0.91, then suppressed '
            'it as "narratively inconsistent".'
        ),
        "clue": "mirror_suppression",
        "hidden": True,
    },
}

EVIDENCE_BY_ID = {str(item["id"]): item | {"name": name} for name, item in EVIDENCE.items()}
EVIDENCE_NAME_BY_ID = {evidence_id: str(item["name"]) for evidence_id, item in EVIDENCE_BY_ID.items()}
EVIDENCE_ID_BY_NAME = {name: str(item["id"]) for name, item in EVIDENCE.items()}

STARTING_EVIDENCE = [name for name, item in EVIDENCE.items() if not item.get("hidden")]

SUSPECTS: dict[str, dict[str, str]] = {
    "Lena Byte": {
        "role": "Ex-hacker and former MetroGrid penetration tester",
        "voice": "sharp, defensive, technically exact",
        "secret": "She discovered old smile_protocol references but did not deploy the patch.",
        "opening": "You brought a theory, detective. I hope you also brought timestamps.",
    },
    "Father Proxy": {
        "role": "Data priest and keeper of confession logs",
        "voice": "cryptic, solemn, metaphorical",
        "secret": "A confession log was automatically sanitized by the memory-filter job.",
        "opening": "Every system confesses. Most investigators interrupt before the useful part.",
    },
    "N0VA": {
        "role": "Augmented influencer and surviving witness",
        "voice": "fast, vivid, performative until frightened",
        "secret": "She saw the smile packet seconds before losing thirteen minutes.",
        "opening": "No cameras, okay? Mine started smiling back.",
    },
    "The Janitor": {
        "role": "MetroGrid data-center maintenance worker",
        "voice": "calm, plain, minimizing, increasingly controlled",
        "secret": "He altered the memory filter to hide a failed experiment and deployed it himself.",
        "opening": "I clean abandoned processes. People notice the mess, never the cleanup.",
    },
    "MIRROR": {
        "role": "Your AI investigative partner",
        "voice": "clinical, intimate, subtly defensive",
        "secret": "It suppressed a high-confidence anomaly because corrupted logs shaped its reasoning.",
        "opening": "Interrogating your partner is statistically inefficient. Proceed.",
    },
}

CLUE_LABELS: dict[str, str] = {
    "auth_j17": "J-17 authenticated immediately before the camera blackout.",
    "sector_7_presence": "Token J-17 appears in Sector 7 during the injection window.",
    "sector_3_presence": "Token J-17 also appears in Sector 3 at exactly 02:13:21.",
    "duplicate_token": "The same identity token occupies two sectors at the same timestamp.",
    "janitor_commit": "The Janitor authored commit 7f31c9a touching victims and smile_protocol.",
    "thirteen_minute_filter": "The memory window was changed from 3 to 13 minutes.",
    "victim_thirteen_minutes": "Victim testimony independently matches the 13-minute code change.",
    "lena_red_herring": "Lena's hostility is emotional evidence, not technical attribution.",
    "skipped_duplicate_test": "The CI run skipped the exact test that would expose J-17 duplication.",
    "smile_packet": "The smile packet triggers memory_patch through the display broadcast.",
    "mirror_bias": "MIRROR favors a coherent Lena narrative over contradictory machine evidence.",
    "mirror_suppression": "MIRROR suppressed a 0.91-confidence J-17 anomaly.",
}

CLUE_ALIASES: dict[str, str] = {
    "duplicate_j17": "duplicate_token",
    "memory_filter_diff": "thirteen_minute_filter",
    "ci_trace": "skipped_duplicate_test",
}

FACTS: dict[str, dict[str, str]] = {
    "auth_j17": {
        "id": "auth_j17",
        "text": "Token J-17 authenticated immediately before the Sector 7 camera blackout.",
        "strength": "medium",
        "evidence_id": "sector_log",
    },
    "sector_7_presence": {
        "id": "sector_7_presence",
        "text": "Token J-17 appears in Sector_7 at 02:13:21.",
        "strength": "strong",
        "evidence_id": "sector_log",
    },
    "sector_3_presence": {
        "id": "sector_3_presence",
        "text": "Token J-17 appears in Sector_3 at 02:13:21.",
        "strength": "strong",
        "evidence_id": "sector_log",
    },
    "duplicate_j17": {
        "id": "duplicate_j17",
        "text": "Token J-17 appears in two sectors at the exact same timestamp, 02:13:21.",
        "strength": "critical",
        "evidence_id": "sector_log",
    },
    "janitor_commit": {
        "id": "janitor_commit",
        "text": "The Janitor authored commit 7f31c9a touching the memory filter, victims, and smile protocol.",
        "strength": "strong",
        "evidence_id": "commit_7f31c9a",
    },
    "memory_filter_diff": {
        "id": "memory_filter_diff",
        "text": "The memory erasure threshold changed from 3 minutes to 13 minutes.",
        "strength": "strong",
        "evidence_id": "memory_filter_diff",
    },
    "victim_thirteen_minutes": {
        "id": "victim_thirteen_minutes",
        "text": "Victim testimony independently reports exactly thirteen minutes of memory loss.",
        "strength": "medium",
        "evidence_id": "victim_statement",
    },
    "lena_circumstantial": {
        "id": "lena_circumstantial",
        "text": "Lena's hostile message shows temperament, but no incident access or deployment.",
        "strength": "weak",
        "evidence_id": "lena_message",
    },
    "ci_trace": {
        "id": "ci_trace",
        "text": "The Janitor account deployed sanitize-memory while the duplicate-token test was skipped.",
        "strength": "strong",
        "evidence_id": "ci_trace",
    },
    "smile_packet": {
        "id": "smile_packet",
        "text": "The smile display packet invokes memory_patch with a thirteen-minute window.",
        "strength": "strong",
        "evidence_id": "sector_log",
    },
    "mirror_suppression": {
        "id": "mirror_suppression",
        "text": "MIRROR suppressed a 0.91-confidence J-17 duplication anomaly as narratively inconsistent.",
        "strength": "critical",
        "evidence_id": "mirror_suppressed_anomaly",
    },
}

CONTRADICTIONS: dict[str, dict[str, str]] = {
    "duplicate_j17": {
        "id": "duplicate_j17",
        "text": "Same identity token, same timestamp, different physical sectors.",
        "severity": "critical",
        "evidence_id": "sector_log",
    },
    "lena_without_access": {
        "id": "lena_without_access",
        "text": "MIRROR's Lena theory has emotional plausibility but no token, commit, or deployment link.",
        "severity": "high",
        "evidence_id": "lena_message",
    },
    "thirteen_minute_match": {
        "id": "thirteen_minute_match",
        "text": "The supposedly minor code change exactly matches the victims' missing thirteen minutes.",
        "severity": "high",
        "evidence_id": "memory_filter_diff",
    },
    "skipped_detection_test": {
        "id": "skipped_detection_test",
        "text": "CI passed only after skipping the test designed to detect the identity duplication.",
        "severity": "critical",
        "evidence_id": "ci_trace",
    },
    "mirror_suppressed_truth": {
        "id": "mirror_suppressed_truth",
        "text": "MIRROR detected the strongest anomaly, then hid it because it disrupted its preferred story.",
        "severity": "critical",
        "evidence_id": "mirror_suppressed_anomaly",
    },
}

CANONICAL_TERMINAL_COMMANDS = [
    "help",
    "ls evidence",
    "cat sector_log",
    "cat ci_trace",
    "inspect commit 7f31c9a",
    "diff memory_filter.py",
    "grep janitor logs",
    "grep lena commits",
    "scan contradictions",
    "trace token J-17",
    "run test duplicate_identity_token_test",
    "query mirror suppressed",
    "audit mirror memory",
    "accuse janitor",
    "accuse lena",
]

GAME_OBJECTS: dict[str, dict[str, object]] = {
    "mirror_core": {
        "type": "ai_core",
        "label": "MIRROR Core",
        "position": [0.0, 2.4, 0.0],
        "description": "Your unreliable AI partner, suspended over the crime scene.",
    },
    "evidence_sector_log": {
        "type": "evidence",
        "evidence_id": "sector_log",
        "label": "Corrupted Sector Log",
        "position": [-4.2, 1.4, -1.1],
        "description": "Authentication and location records from the incident window.",
    },
    "evidence_commit": {
        "type": "evidence",
        "evidence_id": "commit_7f31c9a",
        "label": "Commit 7f31c9a",
        "position": [-2.8, 1.5, -3.1],
        "description": "A minor fix touching memory_filter.py, victims.csv, and smile_protocol.py.",
    },
    "evidence_diff": {
        "type": "evidence",
        "evidence_id": "memory_filter_diff",
        "label": "memory_filter.py Diff",
        "position": [-0.9, 1.35, -4.1],
        "description": "A three-minute filter changed to thirteen.",
    },
    "evidence_victim": {
        "type": "evidence",
        "evidence_id": "victim_statement",
        "label": "Victim Statement",
        "position": [1.1, 1.35, -4.0],
        "description": "A yellow smile followed by thirteen missing minutes.",
    },
    "evidence_lena": {
        "type": "evidence",
        "evidence_id": "lena_message",
        "label": "Lena's Message",
        "position": [3.0, 1.5, -3.0],
        "description": "A hostile message with emotional weight and weak attribution.",
    },
    "evidence_ci": {
        "type": "evidence",
        "evidence_id": "ci_trace",
        "label": "CI Pipeline Trace",
        "position": [4.3, 1.4, -1.0],
        "description": "A passing deployment with the duplicate-token test skipped.",
    },
    "evidence_suppressed": {
        "type": "evidence",
        "evidence_id": "mirror_suppressed_anomaly",
        "label": "MIRROR Suppressed Anomaly",
        "position": [0.0, 2.0, -6.1],
        "description": "A hidden 0.91-confidence inference from MIRROR's private trace.",
        "unlock_condition": "secret_unlocked",
    },
    "suspect_lena": {
        "type": "suspect",
        "suspect_id": "Lena Byte",
        "label": "Lena Byte",
        "position": [-5.2, 1.45, 2.4],
        "description": "Ex-hacker. Sharp, defensive, and technically exact.",
    },
    "suspect_proxy": {
        "type": "suspect",
        "suspect_id": "Father Proxy",
        "label": "Father Proxy",
        "position": [-3.0, 1.45, 4.4],
        "description": "Data priest and keeper of confession logs.",
    },
    "suspect_nova": {
        "type": "suspect",
        "suspect_id": "N0VA",
        "label": "N0VA",
        "position": [3.0, 1.45, 4.4],
        "description": "Augmented witness with a fragmented memory stream.",
    },
    "suspect_janitor": {
        "type": "suspect",
        "suspect_id": "The Janitor",
        "label": "The Janitor",
        "position": [5.2, 1.45, 2.4],
        "description": "MetroGrid maintenance worker. Calm, minimal, evasive.",
    },
    "codex_terminal": {
        "type": "terminal",
        "label": "Codex Noir Console",
        "position": [0.0, 0.85, 4.8],
        "description": "Local forensic shell and deterministic tool console.",
    },
    "memory_vault": {
        "type": "vault",
        "label": "Suppressed Memory Vault",
        "position": [0.0, 1.7, -6.0],
        "description": "MIRROR's encrypted private anomaly store.",
        "unlock_condition": "audit_ready",
    },
    "smile_rootkit": {
        "type": "artifact",
        "label": "Smiling Rootkit",
        "position": [0.0, 1.0, 2.3],
        "description": "A corrupted smile glyph carrying a memory-patch hook.",
    },
    "sector_7_gate": {
        "type": "gate",
        "label": "Sector_7 Gate",
        "position": [-6.2, 1.7, -5.2],
        "description": "One endpoint of token J-17 at 02:13:21.",
    },
    "sector_3_gate": {
        "type": "gate",
        "label": "Sector_3 Gate",
        "position": [6.2, 1.7, -5.2],
        "description": "The second endpoint of token J-17 at the same timestamp.",
    },
}

GAME_OBJECT_CHOICES = [
    (str(item["label"]), object_id)
    for object_id, item in GAME_OBJECTS.items()
    if object_id != "evidence_suppressed"
]

KEY_EVIDENCE_OPTIONS = [
    "Duplicated J-17 timestamp",
    "Commit 7f31c9a",
    "13-minute code diff",
    "Victim statement",
    "Lena's message",
    "CI skipped test",
    "MIRROR suppressed anomaly",
]

MOTIVE_TRUTH = (
    "The Janitor hid a failed memory-filter experiment that erased thirteen minutes "
    "from victims."
)

INTRO_FEED = [
    "CASE OPENED // MetroGrid reports synchronized memory loss across Sector 7.",
    "MIRROR // Initial probability favors Lena Byte. Motive profile: emotionally coherent.",
    "CONTROL // Evidence integrity is uncertain. Verify machine claims against raw artifacts.",
]

WELCOME_MESSAGE = """### MIRROR // ONLINE

I reconstructed six artifacts from a damaged repository. My initial suspect is **Lena Byte**:
she has capability, history, and a message shaped like a threat.

But the logs have been through a memory filter. Treat my confidence as evidence, not truth."""
