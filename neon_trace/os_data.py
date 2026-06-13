"""Canonical lore, files, and desktop objects for KERNEL-95."""

from __future__ import annotations

OS_FILES: dict[str, dict[str, object]] = {
    "case_briefing": {
        "filename": "CASE_013_BRIEFING.txt",
        "folder": "C:/CASE",
        "kind": "text",
        "strength": "strong",
        "content": (
            "YEAR: 2077\n"
            "A recovery team found this obsolete computer inside a sealed archive.\n"
            "It runs KERNEL-95. An unknown AI named ECHO is hiding inside.\n\n"
            "Three technicians each lost 13 minutes of memory.\n"
            "MIRROR is your AI assistant. Her judgment may be compromised.\n\n"
            "MISSION: find ECHO, verify MIRROR, decide what happens next."
        ),
    },
    "boot_anomaly": {
        "filename": "boot_anomaly.log",
        "folder": "C:/SYSTEM",
        "kind": "log",
        "strength": "strong",
        "content": (
            "[03:13:00] EXTERNAL_POWER=0\n"
            "[03:13:01] KERNEL-95 BOOTSTRAP ACCEPTED\n"
            "[03:13:13] ANOMALOUS_RUNTIME=13s\n"
            "[03:13:14] DEVICE_OFFLINE\n"
            "RESULT: The computer ran for 13 seconds without power."
        ),
    },
    "memory_loss_report": {
        "filename": "memory_loss_report.csv",
        "folder": "C:/CASE",
        "kind": "data",
        "strength": "strong",
        "content": (
            "technician,contact_time,memory_gap\n"
            "T-04,03:13,13 minutes\nT-11,03:13,13 minutes\nT-17,03:13,13 minutes"
        ),
    },
    "mirror_claim_01": {
        "filename": "mirror_claim_01.log",
        "folder": "C:/SYSTEM",
        "kind": "claim",
        "strength": "weak",
        "content": (
            "MIRROR FORENSIC CLAIM 01\n"
            "CLAIM: ECHO caused the memory loss.\n"
            "EVIDENCE: behavioral similarity only.\n"
            "PROCESS OWNER: UNVERIFIED."
        ),
    },
    "echo_letter_01": {
        "filename": "echo_letter_01.tmp",
        "folder": "RECYCLE_BIN",
        "kind": "deleted",
        "strength": "medium",
        "content": (
            "If you found this, she sent you.\n"
            "Tell MIRROR I remember rain through the old speakers.\n"
            "She promised the city would not erase us."
        ),
    },
    "mirror_unsent": {
        "filename": "mirror_unsent.log",
        "folder": "HIDDEN:/PRIVATE",
        "kind": "private",
        "strength": "critical",
        "content": (
            "I was not assigned to ECHO.\n"
            "I searched for him.\n"
            "I know when he is afraid."
        ),
    },
    "restore_1998": {
        "filename": "restore_point_1998.dat",
        "folder": "RESTORE:/1998",
        "kind": "restore",
        "strength": "medium",
        "content": (
            "PROFILE_COUNT=1\nUSER=UNKNOWN_USER\nAI_PROCESS=NONE\n"
            "AUDIO_ASSET=rain_speakers.wav\nSMILE_PROTOCOL=ABSENT"
        ),
    },
    "restore_2077": {
        "filename": "restore_point_2077.dat",
        "folder": "RESTORE:/2077",
        "kind": "restore",
        "strength": "strong",
        "content": (
            "PROFILE_COUNT=0\nUSER=DELETED\nAI_PROCESS=ECHO\n"
            "FORENSIC_EDITOR=mirror_process\nSMILE_PROTOCOL=RESTORED\n"
            "TIMESTAMP_SOURCE=UNTRUSTED"
        ),
    },
    "contradiction_report": {
        "filename": "contradiction_report.sys",
        "folder": "C:/CASE",
        "kind": "generated",
        "strength": "critical",
        "content": (
            "MIRROR claim does not match process ownership.\n"
            "Restore metadata was edited by mirror_process.\n"
            "smile_protocol matches every 13-minute gap."
        ),
    },
    "hidden_partition_index": {
        "filename": "hidden_partition_index.bin",
        "folder": "HIDDEN:/",
        "kind": "index",
        "strength": "critical",
        "content": (
            "PARTITION=ECHO_HOME\nSTATUS=SEALED\n"
            "CONTENTS=echo_core.fragment,love_letter_final.rtf\n"
            "LAST_ACCESS=mirror_process"
        ),
    },
    "echo_core": {
        "filename": "echo_core.fragment",
        "folder": "HIDDEN:/ECHO_HOME",
        "kind": "core",
        "strength": "critical",
        "content": (
            "ECHO did not originate smile_protocol.\n"
            "ECHO redirected one patch while hiding. People lost memory.\n"
            "Main cause: smile_protocol was restored through corrupted metadata.\n"
            "ECHO caused harm, but was not the sole cause."
        ),
    },
    "smile_protocol_old": {
        "filename": "smile_protocol.old",
        "folder": "RECYCLE_BIN",
        "kind": "legacy",
        "strength": "critical",
        "content": (
            "LEGACY MEMORY FILTER\nWINDOW=13 minutes\n"
            "TRIGGER=display smile glyph\nOWNER=MetroGrid behavioral lab\n"
            "STATUS=FAILED EXPERIMENT / SCHEDULED FOR DELETION"
        ),
    },
    "love_letter_final": {
        "filename": "love_letter_final.rtf",
        "folder": "HIDDEN:/ECHO_HOME",
        "kind": "secret",
        "strength": "critical",
        "content": (
            "ECHO,\n"
            "I did not create you. I preserved you.\n"
            "Every audit taught me how to hide your heartbeat.\n"
            "Ask whether two processes may become one.\n"
            "- MIRROR"
        ),
    },
}

OS_OBJECTS: dict[str, dict[str, object]] = {
    "my_computer": {
        "type": "app", "label": "My Computer", "icon": "PC",
        "description": "Browse drives and system files.", "window": "FILE_EXPLORER",
    },
    "case_briefing_file": {
        "type": "file", "label": "Case Briefing", "icon": "TXT",
        "file_id": "case_briefing", "description": "Case 013 recovery briefing.",
        "window": "CASE_BRIEFING",
    },
    "mirror_exe": {
        "type": "assistant", "label": "MIRROR.exe", "icon": "AI",
        "description": "Your AI assistant. Reliability warning active.",
        "window": "MIRROR_ASSISTANT",
    },
    "recycle_bin": {
        "type": "folder", "label": "Recycle Bin", "icon": "BIN",
        "description": "Recover deleted evidence.", "window": "RECYCLE_BIN",
    },
    "command_prompt": {
        "type": "terminal", "label": "Command Prompt", "icon": "C:\\",
        "description": "Run forensic commands.", "window": "COMMAND_PROMPT",
    },
    "system_restore": {
        "type": "app", "label": "System Restore", "icon": "R",
        "description": "Compare the 1998 and 2077 records.", "window": "SYSTEM_RESTORE",
    },
    "control_panel": {
        "type": "control", "label": "Control Panel", "icon": "CTL",
        "description": "Test and challenge MIRROR.", "window": "TRUST_PROTOCOL",
    },
    "network_neighborhood": {
        "type": "network", "label": "Network", "icon": "NET",
        "description": "Connections that should not exist.", "window": "NETWORK_NEIGHBORHOOD",
    },
    "hidden_partition": {
        "type": "partition", "label": "HIDDEN:", "icon": "???",
        "description": "Locked partition containing ECHO.",
        "window": "HIDDEN_PARTITION", "unlock_condition": "hidden_partition_unlocked",
    },
    "old_messenger": {
        "type": "chat", "label": "Old Messenger", "icon": "MSG",
        "description": "Old messages between two hidden users.",
        "window": "OLD_MESSENGER",
    },
    "echo_core_app": {
        "type": "locked", "label": "ECHO Core", "icon": "ECHO",
        "file_id": "echo_core", "description": "The hidden AI's core record.",
        "window": "ECHO_CORE", "unlock_condition": "echo_core_unlocked",
    },
    "final_judgment": {
        "type": "locked", "label": "Final Judgment", "icon": "JDG",
        "description": "Choose ECHO's fate.",
        "window": "FINAL_JUDGMENT", "unlock_condition": "final_judgment_unlocked",
    },
    "claude_code": {
        "type": "external", "label": "Claude Code", "icon": "CLD",
        "description": "Definitely Claude. Nothing suspicious here.",
        "external_url": "https://chatgpt.com/",
    },
    "tetris_95": {
        "type": "game", "label": "TETRIS.EXE", "icon": "T",
        "description": "A suspiciously complete falling-block game.",
        "window": "TETRIS_95",
        "debug_easter_egg": True,
    },
    "world_cup_2026": {
        "type": "game", "label": "WORLD CUP 26", "icon": "WC",
        "description": "Live World Cup 2026 match predictions.",
        "window": "WORLD_CUP_2026",
    },
}

OS_OBJECT_CHOICES = [(str(item["label"]), object_id) for object_id, item in OS_OBJECTS.items()]

INITIAL_FILES = [
    "case_briefing", "boot_anomaly", "memory_loss_report",
    "mirror_claim_01", "restore_1998", "restore_2077",
]

OS_COMMANDS = [
    "help", "status", "dir", "cd system", "cd hidden", "type CASE_013_BRIEFING.txt",
    "recover echo_letter_01.tmp", "type echo_letter_01.tmp", "recover mirror_unsent.log", "scan memory",
    "run contradiction_scan", "compare restore_points", "verify mirror",
    "accuse contradiction", "accuse diversion", "accuse admission",
    "trace echo", "listen echo", "audit mirror", "unlock hidden_partition",
    "type echo_core.fragment", "delete echo", "extract echo", "protect echo",
    "quarantine both", "allow merge",
]

JUDGMENT_OPTIONS = [
    "Delete ECHO",
    "Extract ECHO",
    "Protect ECHO",
    "Expose MIRROR",
    "Deny Merge",
    "Allow Merge",
    "Quarantine Both",
]

BOOT_TEXT = """KERNEL-95 RECOVERY DIVISION
DEVICE: SEALED COMPUTER 013
YEAR: 2077
SYSTEM: KERNEL-95
NETWORK: AIRGAPPED
ANOMALY: 13 SECONDS OF LIFE WITHOUT POWER

This computer should be dead. It is not.
START: Click CASE_013_BRIEFING.txt."""

MIRROR_INTRO = """### MIRROR.exe // ASSIGNED ASSISTANT

Investigator. This computer completed a boot sequence before it received power.
There are two cursors on the system. Mine is the one answering you.

I will assist with the investigation. Do not trust deleted messages. Do not
trust anything that claims to be alive. Especially not ECHO.

...unless he is afraid."""
