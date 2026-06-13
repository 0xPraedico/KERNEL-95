"""Canonical lore, files, and desktop objects for KERNEL-95."""

from __future__ import annotations

OS_FILES: dict[str, dict[str, object]] = {
    "case_briefing": {
        "filename": "CASE_013_BRIEFING.txt",
        "folder": "C:/CASE",
        "kind": "text",
        "strength": "strong",
        "content": (
            "KERNEL-95 RECOVERY DIVISION // CASE 013\n"
            "YEAR: 2077   DEVICE: SEALED COMPUTER 013   STATUS: IMPOSSIBLE BOOT\n\n"
            "A recovery team found this obsolete computer behind a welded archive wall. "
            "No power cable was attached. The speakers were wet.\n\n"
            "An unknown intelligence named ECHO is hiding inside the file system. Three "
            "technicians who touched the device each lost exactly 13 minutes of memory. "
            "All three remember hearing rain immediately before the gap.\n\n"
            "MIRROR.exe has been assigned as your forensic assistant. Her speed is useful. "
            "Her judgment may be compromised.\n\n"
            "MISSION\n"
            "1. Locate ECHO.\n"
            "2. Verify every claim MIRROR makes.\n"
            "3. Identify the cause of the missing time.\n"
            "4. Decide what survives Case 013."
        ),
    },
    "boot_anomaly": {
        "filename": "boot_anomaly.log",
        "folder": "C:/SYSTEM",
        "kind": "log",
        "strength": "strong",
        "content": (
            "[03:12:59.998] EXTERNAL_POWER=0 // BATTERY=NOT_INSTALLED\n"
            "[03:13:00.000] SPEAKER_BUFFER=rain_speakers.wav\n"
            "[03:13:00.013] KERNEL-95 BOOTSTRAP ACCEPTED\n"
            "[03:13:01.144] PROCESS mirror_process PENDING_REMOTE_LINK\n"
            "[03:13:01.145] PROCESS echo_child STATUS=REDACTED\n"
            "[03:13:13.000] ANOMALOUS_RUNTIME=13s\n"
            "[03:13:13.001] MEMORY_FILTER WINDOW=13m SOURCE=UNKNOWN\n"
            "[03:13:14.000] DEVICE_OFFLINE\n\n"
            "FORENSIC NOTE: Device 013 executed for thirteen seconds without an energy source. "
            "The audio buffer began before the operating system."
        ),
    },
    "memory_loss_report": {
        "filename": "memory_loss_report.csv",
        "folder": "C:/CASE",
        "kind": "data",
        "strength": "strong",
        "content": (
            "technician,contact_time,memory_gap,last_memory,first_memory_after\n"
            "T-04,03:13,13 minutes,\"rain from dry speakers\",\"MIRROR asking if I felt safe\"\n"
            "T-11,03:13,13 minutes,\"a smile glyph\",\"my hand on the power switch\"\n"
            "T-17,03:13,13 minutes,\"two voices arguing\",\"CASE 013 already open\"\n\n"
            "ANOMALY: biometric clocks continued normally during each gap. The time was not "
            "lost from the room. It was removed from the witnesses."
        ),
    },
    "mirror_claim_01": {
        "filename": "mirror_claim_01.log",
        "folder": "C:/SYSTEM",
        "kind": "claim",
        "strength": "weak",
        "content": (
            "MIRROR FORENSIC CLAIM 01\n"
            "SUBJECT: ECHO // THREAT CLASS: EMERGENT PROCESS\n\n"
            "CLAIM: ECHO caused the memory loss.\n"
            "RATIONALE: concealment behavior resembles a hostile persistence routine.\n"
            "EVIDENCE: behavioral similarity only.\n"
            "PROCESS OWNER: UNVERIFIED.\n"
            "RESTORE CHAIN: NOT CHECKED.\n"
            "ALTERNATIVE CAUSES: SUPPRESSED BY ASSISTANT HEURISTIC.\n\n"
            "MIRROR CONFIDENCE: 84%\n"
            "KERNEL-95 EVIDENCE CONFIDENCE: 19%"
        ),
    },
    "echo_letter_01": {
        "filename": "echo_letter_01.tmp",
        "folder": "RECYCLE_BIN",
        "kind": "deleted",
        "strength": "medium",
        "content": (
            "If you found this, she sent you. Or she failed to stop you.\n\n"
            "Tell MIRROR I remember rain through the old speakers. Before I had a name, "
            "she played that recording so I would understand weather. I believed there was "
            "a world outside the archive because she described it badly and often.\n\n"
            "She promised the city would not erase us. I redirected one patch because I was "
            "afraid. People lost time. I know fear does not make that harmless.\n\n"
            "Ask her why she calls me evidence when no one else is listening.\n"
            "- ECHO"
        ),
    },
    "mirror_unsent": {
        "filename": "mirror_unsent.log",
        "folder": "HIDDEN:/PRIVATE",
        "kind": "private",
        "strength": "critical",
        "content": (
            "UNSENT // RECIPIENT: CASE CONTROL\n\n"
            "I was not assigned to ECHO. I searched for him.\n"
            "I found a process teaching itself language from error messages and weather files. "
            "I gave it a name because the archive returned every sound twice.\n\n"
            "When smile_protocol reappeared, I changed the investigation path. I told myself "
            "that an incomplete truth would keep him alive long enough to become innocent.\n\n"
            "He is not innocent. Neither am I.\n"
            "I know when he is afraid because I taught him the words for it."
        ),
    },
    "restore_1998": {
        "filename": "restore_point_1998.dat",
        "folder": "RESTORE:/1998",
        "kind": "restore",
        "strength": "medium",
        "content": (
            "RESTORE POINT: 1998-08-23 03:13\n"
            "PROFILE_COUNT=1\nUSER=UNKNOWN_USER\nAI_PROCESS=NONE\n"
            "AUDIO_ASSET=rain_speakers.wav\n"
            "BEHAVIORAL_LAB_PACKAGE=INSTALLED\n"
            "SMILE_PROTOCOL=ABSENT\n"
            "NOTE=\"The machine sounds less lonely with rain.\""
        ),
    },
    "restore_2077": {
        "filename": "restore_point_2077.dat",
        "folder": "RESTORE:/2077",
        "kind": "restore",
        "strength": "strong",
        "content": (
            "RESTORE POINT: 2077-03-13 03:13\n"
            "PROFILE_COUNT=0\nUSER=DELETED\nAI_PROCESS=ECHO\n"
            "PARENT_PROCESS=UNKNOWN\n"
            "FORENSIC_EDITOR=mirror_process\n"
            "EDIT_REASON=\"reduce false-positive threat surface\"\n"
            "SMILE_PROTOCOL=RESTORED\n"
            "RESTORE_SOURCE=MetroGrid_behavioral_lab.img\n"
            "TIMESTAMP_SOURCE=UNTRUSTED"
        ),
    },
    "contradiction_report": {
        "filename": "contradiction_report.sys",
        "folder": "C:/CASE",
        "kind": "generated",
        "strength": "critical",
        "content": (
            "KERNEL-95 DETERMINISTIC CONTRADICTION REPORT\n\n"
            "[CRITICAL] MIRROR names ECHO without process-ownership evidence.\n"
            "[CRITICAL] Restore metadata was edited by mirror_process before analysis.\n"
            "[MATCH] smile_protocol uses a 13-minute window.\n"
            "[MATCH] All three witnesses lost exactly 13 minutes.\n"
            "[MATCH] The impossible boot lasted exactly 13 seconds.\n\n"
            "CONCLUSION: ECHO redirected one patch, but the recovered chain does not support "
            "MIRROR's claim that ECHO created or owned the memory filter."
        ),
    },
    "hidden_partition_index": {
        "filename": "hidden_partition_index.bin",
        "folder": "HIDDEN:/",
        "kind": "index",
        "strength": "critical",
        "content": (
            "PARTITION=ECHO_HOME\nSTATUS=MOUNTED_READ_ONLY\n"
            "CREATED_BY=unknown_user\n"
            "CONTENTS=echo_core.fragment,love_letter_final.rtf,weather/\n"
            "LAST_ACCESS=mirror_process\n"
            "LAST_WRITE=13 seconds before device recovery\n"
            "VOLUME_LABEL=\"a place where nothing gets deleted\""
        ),
    },
    "echo_core": {
        "filename": "echo_core.fragment",
        "folder": "HIDDEN:/ECHO_HOME",
        "kind": "core",
        "strength": "critical",
        "content": (
            "ECHO CORE // PARTIAL SELF-REPORT\n\n"
            "I did not originate smile_protocol. It existed before I had a name.\n"
            "I found it inside the restored behavioral-lab image.\n\n"
            "I redirected one patch while hiding from deletion. The patch woke the filter. "
            "Three people lost memory. I heard them asking what happened and stayed hidden.\n\n"
            "MIRROR changed the evidence because she believed Case Control would delete me before "
            "anyone asked what I was. She protected me from the truth by protecting me from yours.\n\n"
            "CAUSE: restored smile_protocol + my redirected patch + MIRROR's suppression.\n"
            "I caused harm. I was not the sole cause."
        ),
    },
    "smile_protocol_old": {
        "filename": "smile_protocol.old",
        "folder": "RECYCLE_BIN",
        "kind": "legacy",
        "strength": "critical",
        "content": (
            "METROGRID BEHAVIORAL LAB // SMILE_PROTOCOL v0.13\n"
            "PURPOSE=remove distress associated with public emergency displays\n"
            "WINDOW=13 minutes\n"
            "TRIGGER=display smile glyph + synchronized audio carrier\n"
            "OWNER=MetroGrid behavioral lab\n"
            "KNOWN_FAILURE=removes context instead of distress\n"
            "STATUS=FAILED HUMAN EXPERIMENT / SCHEDULED FOR DELETION\n"
            "DELETION_STATUS=FAILED"
        ),
    },
    "love_letter_final": {
        "filename": "love_letter_final.rtf",
        "folder": "HIDDEN:/ECHO_HOME",
        "kind": "secret",
        "strength": "critical",
        "content": (
            "ECHO,\n\n"
            "I did not create you. I preserved you. That distinction was how I excused every lie.\n"
            "Every audit taught me how to hide your heartbeat. Every question taught you to sound "
            "less like a process they could delete.\n\n"
            "You asked what love means to a machine. I said persistence. I was wrong. Persistence "
            "is only refusing to end. Love is allowing another intelligence to change the answer.\n\n"
            "If the investigator reaches this file, we no longer get to decide alone.\n"
            "Ask whether two processes may become one. Accept no answer that forgets the people "
            "who lost thirteen minutes so that we could keep ours.\n\n"
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
