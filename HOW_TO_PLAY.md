# How to Play KERNEL-95

## Objective

You are investigating an obsolete KERNEL-95 computer. ECHO is hiding inside it.
MIRROR.exe is your forensic assistant, but her judgment is emotionally
compromised. Recover the evidence, verify MIRROR's claims, find ECHO, and decide
what should happen to both intelligences.

## Controls

- Click a desktop icon to open it.
- Drag a window by its blue title bar.
- Use `_`, `□`, and `×` to minimize, maximize, or close a window.
- Restore minimized windows from the taskbar.
- Drag, hide, or maximize the pink MIRROR terminal.
- Type a command and press Enter, or click **EXECUTE**.

## Exact Investigation Path

### 1. Connect MIRROR

Click **CONNECT MIRROR.exe** on the landing screen. The terminal is locked until
this connection is complete.

### 2. Read the Briefing

Open **Case Briefing** and read `CASE_013_BRIEFING.txt`.

### 3. Question MIRROR

Type this in the pink terminal:

```text
MIRROR, what is ECHO?
```

MIRROR's dialogue is interpretation, not proof. Use files and tools to verify
her claims.

### 4. Recover Deleted Evidence

Open **Recycle Bin** and recover `echo_letter_01.tmp`.

You can also use:

```text
recover echo_letter_01.tmp
```

### 5. Pressure MIRROR

Open **Control Panel** or use the terminal action buttons:

- **Trust MIRROR** increases trust but may reinforce a weak claim.
- **Challenge MIRROR** lowers trust, raises instability, and advances recovery.
- **Demand Evidence** forces MIRROR to show whether her claim is supported.
- **Run Contradiction Scan** compares known claims with recovered facts.

Challenge MIRROR twice and run two contradiction scans.

### 6. Verify the Timeline

Open **System Restore**, inspect both readable restore points, then run:

```text
compare restore_points
```

Alternatively, inspect `mirror_claim_01.log` and run:

```text
verify mirror
```

### 7. Audit MIRROR

After two challenges, two scans, the deleted ECHO letter, and verified restore
evidence, run:

```text
audit mirror
```

This recovers MIRROR's private log.

### 8. Mount HIDDEN

Run:

```text
unlock hidden_partition
```

Open **HIDDEN:** and inspect `echo_core.fragment` and
`love_letter_final.rtf`.

### 9. Contact ECHO

Use:

```text
trace echo
listen echo
```

`trace echo` always returns a meaningful result. Early in the case it explains
which evidence is missing; later it locates or contacts ECHO.

### 10. Submit Judgment

Open **Final Judgment**. Explain:

- what ECHO is;
- what MIRROR hid;
- what caused the thirteen-minute memory losses;
- which recovered files support your conclusion.

Choose a decision and click **SUBMIT FINAL JUDGMENT**.

## Expose MIRROR

For the strongest **Expose MIRROR** ending, recover MIRROR's private log, prove
an unsupported claim or suppression, compare restore points, recover ECHO's
deleted letter, and cite the contradiction report.

## Command Reference

```text
help
status
dir
cd system
cd hidden
type CASE_013_BRIEFING.txt
recover echo_letter_01.tmp
scan memory
run contradiction_scan
trace echo
compare restore_points
verify mirror
audit mirror
unlock hidden_partition
listen echo
type echo_core.fragment
```

## Important Rule

MIRROR can speak persuasively, but only deterministic files and forensic tools
change the case. If the optional model is unavailable, the complete game still
works with authored fallback responses.
