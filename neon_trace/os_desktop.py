"""KERNEL-95 CRT desktop renderer and compact investigation panels."""

from __future__ import annotations

import html
import json
import os
import uuid
from datetime import datetime, timezone

from .game_state import GameState
from .os_data import BOOT_TEXT, JUDGMENT_OPTIONS, OS_FILES, OS_OBJECTS
from .os_tools import JudgmentResult
from .world_cup import (
    FIFA_FIXTURES_URL,
    get_matches,
    prediction_is_open,
)

OS_DESKTOP_BOOTSTRAP = r"""
() => {
  "use strict";
  const executeDesktopScripts = () => {
    document.querySelectorAll(".crt-chassis + script:not([data-k95-executed])").forEach((source) => {
      source.dataset.k95Executed = "true";
      const runtime = document.createElement("script");
      runtime.textContent = source.textContent;
      document.body.appendChild(runtime);
      runtime.remove();
    });
  };
  executeDesktopScripts();
  if (window.Kernel95Bootstrap && window.Kernel95Bootstrap.observer) {
    window.Kernel95Bootstrap.observer.disconnect();
  }
  const observer = new MutationObserver(executeDesktopScripts);
  observer.observe(document.body, { childList: true, subtree: true });
  window.Kernel95Bootstrap = { observer, executeDesktopScripts };
}
"""


def get_mirror_emotional_state(state: GameState) -> str:
    """Project deterministic case state into one readable MIRROR mood."""
    if not state.mirror_connected:
        return "offline"
    unsupported = any(
        item.get("support") == "unsupported" or item.get("supported") is False
        for item in state.mirror_claims
    )
    if "love_letter_final" in state.inspected_files and state.echo_presence >= 60:
        return "merge_pending"
    if state.echo_presence >= 55 or any(
        item.get("tone") == "direct" for item in state.echo_messages
    ):
        return "echo_attached"
    if state.mirror_audit_unlocked:
        return "audited"
    if unsupported and state.demand_evidence_used:
        return "lying"
    if state.challenged_mirror_count >= 1 or state.mirror_instability >= 30:
        return "challenged"
    if unsupported or any(item.get("support") == "weak" for item in state.mirror_claims):
        return "suspicious"
    return "stable"


def _mask_integrity(state: GameState) -> int:
    if not state.mirror_connected:
        return 0
    penalty = state.mirror_instability + state.challenged_mirror_count * 4
    if state.mirror_audit_unlocked:
        penalty += 18
    return max(8, min(100, 112 - penalty))


def _debug_easter_eggs_enabled() -> bool:
    return os.getenv("KERNEL95_DEBUG_EASTER_EGGS", "") == "1"


def _window(title: str, body: str, css_class: str = "") -> str:
    if "k95-main-window" in css_class:
        window_id = "main"
    elif "k95-boot-window" in css_class:
        window_id = "boot"
    elif "k95-objectives-window" in css_class:
        window_id = "objectives"
    elif "k95-echo-window" in css_class:
        window_id = "echo"
    else:
        window_id = "".join(
            character.lower() if character.isalnum() else "-"
            for character in title
        ).strip("-")
    return f"""
<section class="k95-window {css_class}" data-window-id="{html.escape(window_id)}">
  <header class="k95-titlebar">
    <strong>{html.escape(title)}</strong>
    <span>
      <button type="button" data-window-action="minimize" aria-label="Minimize">_</button>
      <button type="button" data-window-action="maximize" aria-label="Maximize">□</button>
      <button type="button" data-window-action="close" aria-label="Close">×</button>
    </span>
  </header>
  <div class="k95-window-body">{body}</div>
</section>
"""


def _event_button(label: str, event: str, locked: bool = False) -> str:
    disabled = " disabled" if locked else ""
    return (
        f'<button type="button" class="k95-file-button" '
        f'data-os-event="{html.escape(event)}"{disabled}>'
        f"{html.escape(label)}</button>"
    )


def _tetris_window() -> str:
    body = """
<div class="k95-tetris" tabindex="0">
  <div class="k95-tetris-stage">
    <canvas class="k95-tetris-canvas" width="200" height="400"></canvas>
    <div class="k95-tetris-side">
      <div><small>SCORE</small><b data-tetris-score>000000</b></div>
      <div><small>LINES</small><b data-tetris-lines>000</b></div>
      <div><small>LEVEL</small><b data-tetris-level>01</b></div>
      <p>ARROWS: MOVE<br>UP: ROTATE<br>SPACE: DROP<br>P: PAUSE</p>
      <button type="button" data-tetris-start>NEW GAME</button>
    </div>
  </div>
  <div class="k95-tetris-controls">
    <button type="button" data-tetris-key="left">LEFT</button>
    <button type="button" data-tetris-key="rotate">ROTATE</button>
    <button type="button" data-tetris-key="right">RIGHT</button>
    <button type="button" data-tetris-key="down">DOWN</button>
    <button type="button" data-tetris-key="drop">DROP</button>
  </div>
</div>
"""
    return _window("TETRIS.EXE", body, "k95-main-window k95-tetris-window")


def _flag(url: str, country: str) -> str:
    if not url:
        return '<span class="k95-flag-placeholder">--</span>'
    return (
        f'<img src="{html.escape(url)}" alt="{html.escape(country)} flag" '
        'loading="lazy" referrerpolicy="no-referrer">'
    )


def _world_cup_window() -> str:
    matches, error = get_matches()
    now = datetime.now(timezone.utc)
    remaining = [match for match in matches if not match["finished"]]
    rows = []
    for match in remaining:
        match_id = str(match["id"])
        open_for_picks = prediction_is_open(match, now)
        disabled = "" if open_for_picks else " disabled"
        status = "LIVE // PICKS LOCKED" if match["live"] else "OPEN"
        if not open_for_picks and not match["live"]:
            status = "PICKS LOCKED"
        choices = [
            ("home", match["home"]),
            ("draw", "Draw"),
            ("away", match["away"]),
        ]
        choice_html = "".join(
            '<label>'
            f'<input type="radio" name="pick-{html.escape(match_id)}" '
            f'value="{choice}"{disabled}>'
            f"<span>{html.escape(label)}</span></label>"
            for choice, label in choices
        )
        rows.append(
            f"""
<article class="k95-match" data-match-id="{html.escape(match_id)}">
  <div class="k95-match-meta">
    <span>M{html.escape(match_id)} // {html.escape(str(match["group"]))}</span>
    <time data-kickoff="{match["kickoff"].isoformat()}">{match["kickoff"].strftime("%b %d %H:%M UTC")}</time>
    <b class="{"live" if match["live"] else ""}">{status}</b>
  </div>
  <div class="k95-match-teams">
    <div>{_flag(str(match["home_flag"]), str(match["home"]))}<strong>{html.escape(str(match["home"]))}</strong></div>
    <em>VS</em>
    <div>{_flag(str(match["away_flag"]), str(match["away"]))}<strong>{html.escape(str(match["away"]))}</strong></div>
  </div>
  <div class="k95-pick-options">{choice_html}</div>
</article>
"""
        )
    source_message = (
        f'<div class="k95-world-cup-alert">{html.escape(error)}</div>'
        if error
        else (
            '<div class="k95-world-cup-status">'
            "LIVE FIXTURE FEED // BROWSER-LOCAL PICKS // NO ACCOUNT"
            "</div>"
        )
    )
    body = f"""
<div class="k95-world-cup">
  <div class="k95-world-cup-toolbar">
    <div><b>WORLD CUP 2026 PREDICTOR</b><span>{len(remaining)} unfinished matches // regulation time only</span></div>
    <div class="k95-world-cup-links">
      <button type="button" data-os-event="refresh_world_cup">REFRESH LIVE</button>
      <a href="{FIFA_FIXTURES_URL}" target="_blank" rel="noopener noreferrer">FIFA FIXTURES</a>
    </div>
  </div>
  {source_message}
  <div class="k95-match-list">{"".join(rows) if rows else "<p>No unfinished matches found.</p>"}</div>
  <div class="k95-world-cup-footer">
    <span>Choose HOME, DRAW, or AWAY. Picks lock at kickoff.</span>
    <b data-local-pick-status>LOCAL PICKS READY</b>
  </div>
</div>
"""
    return _window(
        "WORLD_CUP_2026.EXE",
        body,
        "k95-main-window k95-world-cup-window",
    )


def _desktop_window(state: GameState) -> str:
    object_id = state.selected_os_object
    selected = OS_OBJECTS[object_id]
    if selected.get("debug_easter_egg") and not _debug_easter_eggs_enabled():
        object_id = "my_computer"
        selected = OS_OBJECTS[object_id]
    if object_id == "tetris_95":
        return _tetris_window()
    if object_id == "world_cup_2026":
        return _world_cup_window()
    file_id = selected.get("file_id")
    if (
        object_id == "case_briefing_file"
        and "case_briefing" not in state.inspected_files
    ):
        return ""
    if file_id and str(file_id) not in state.discovered_files:
        return _window(
            str(selected["label"]),
            '<div class="k95-locked-message">ACCESS DENIED<br><br>'
            "This object has not been recovered from HIDDEN:/.</div>",
            "k95-main-window",
        )
    if file_id and str(file_id) in state.inspected_files:
        file = OS_FILES[str(file_id)]
        body = (
            f'<div class="k95-menu">File&nbsp;&nbsp; Edit&nbsp;&nbsp; Search&nbsp;&nbsp; Help</div>'
            f'<pre class="k95-document">{html.escape(str(file["content"]))}</pre>'
        )
        return _window(str(file["filename"]), body, "k95-main-window")
    if object_id == "recycle_bin":
        recovered = set(state.deleted_files_recovered)
        rows = []
        for file_id in ("echo_letter_01", "mirror_unsent", "smile_protocol_old"):
            status = "RECOVERED" if file_id in recovered else "DELETED"
            locked = file_id == "mirror_unsent" and not state.mirror_audit_unlocked
            action = (
                f"file:{file_id}"
                if file_id in state.discovered_files
                else f"recover:{file_id}"
            )
            rows.append(
                "<li>"
                f"{_event_button(str(OS_FILES[file_id]['filename']), action, locked)}"
                f'<b>{"LOCKED" if locked else status}</b></li>'
            )
        return _window(
            "Recycle Bin",
            '<div class="k95-menu">File&nbsp;&nbsp; Restore&nbsp;&nbsp; Empty</div>'
            f'<ul class="k95-file-list">{"".join(rows)}</ul>',
            "k95-main-window",
        )
    if object_id == "hidden_partition":
        status = "MOUNTED // ECHO_HOME" if state.hidden_partition_unlocked else "ACCESS DENIED"
        content = (
            '<div class="k95-hidden-files">'
            f'{_event_button("echo_core.fragment", "file:echo_core")}'
            f'{_event_button("love_letter_final.rtf", "file:love_letter_final")}'
            f'{_event_button("contradiction_report.sys", "file:contradiction_report")}'
            "</div>"
            if state.hidden_partition_unlocked
            else (
                '<div class="k95-locked-message">RECOVERY REQUIREMENTS<br><br>'
                f'[{"OK" if state.challenged_mirror_count >= 2 else ".."}] Challenge MIRROR twice<br>'
                f'[{"OK" if state.contradiction_scans >= 2 else ".."}] Run two contradiction scans<br>'
                f'[{"OK" if "echo_letter_01" in state.deleted_files_recovered else ".."}] Recover echo_letter_01.tmp<br>'
                f'[{"OK" if state.restore_points_compared or state.mirror_claim_verified else ".."}] Compare restore points or verify MIRROR<br>'
                f'[{"OK" if state.mirror_audit_unlocked else ".."}] Audit MIRROR private logs</div>'
            )
        )
        return _window(
            f"HIDDEN: [{status}]",
            content,
            "k95-main-window",
        )
    if object_id == "final_judgment":
        if not state.final_judgment_unlocked:
            body = (
                '<div class="k95-locked-message">FINAL JUDGMENT LOCKED<br><br>'
                "Mount HIDDEN:/, audit MIRROR, and recover ECHO's core first.</div>"
            )
        elif state.final_judgment_submitted:
            breakdown = "".join(
                f"<li><span>{html.escape(label)}</span><b>{points}</b></li>"
                for label, points in state.ending_breakdown.items()
            )
            body = (
                '<div class="k95-ending-screen">'
                f"<small>CASE_013 // SCORE {state.ending_score}/100</small>"
                f"<h3>{html.escape(state.ending_title)}</h3>"
                f"<p>{html.escape(state.ending_narration)}</p>"
                f"<ul>{breakdown}</ul></div>"
            )
        else:
            evidence_options = "".join(
                '<label class="k95-evidence-option">'
                f'<input type="checkbox" value="{html.escape(file_id)}">'
                f"<span>{html.escape(str(OS_FILES[file_id]['filename']))}</span></label>"
                for file_id in state.discovered_files
                if file_id in OS_FILES
            )
            judgment_options = "".join(
                f'<option value="{html.escape(option)}">{html.escape(option)}</option>'
                for option in JUDGMENT_OPTIONS
            )
            body = f"""
<div class="k95-judgment-form">
  <label>What is ECHO?<textarea data-judgment-field="echo" placeholder="Victim, witness, dangerous process..."></textarea></label>
  <label>What did MIRROR hide?<textarea data-judgment-field="mirror" placeholder="Suppressed evidence and conflict..."></textarea></label>
  <label>What caused the 13-minute losses?<textarea data-judgment-field="cause" placeholder="Connect ECHO, restore data, and smile_protocol..."></textarea></label>
  <label>Decision<select data-judgment-field="decision">{judgment_options}</select></label>
  <fieldset><legend>Evidence</legend><div class="k95-evidence-grid">{evidence_options}</div></fieldset>
  <button type="button" class="k95-submit-judgment">SUBMIT FINAL JUDGMENT</button>
</div>
"""
        return _window("Final Judgment", body, "k95-main-window")
    special_apps = {
        "my_computer": (
            "My Computer",
            '<div class="k95-menu">File&nbsp;&nbsp; View&nbsp;&nbsp; Tools&nbsp;&nbsp; Help</div>'
            '<ul class="k95-file-list"><li><span>C:/</span><b>ONLINE</b></li>'
            '<li><span>SYSTEM/</span><b>DEGRADED</b></li>'
            '<li><span>RESTORE/</span><b>4 POINTS</b></li>'
            '<li><span>USERS/</span><b>DELETED</b></li>'
            f'<li><span>HIDDEN:/</span><b>{"MOUNTED" if state.hidden_partition_unlocked else "LOCKED"}</b></li></ul>',
        ),
        "control_panel": (
            "TRUST_PROTOCOL.hlp",
            '<div class="k95-control-grid">'
            f'{_event_button("Trust MIRROR", "action:trust")}'
            f'{_event_button("Challenge MIRROR", "action:challenge")}'
            f'{_event_button("Demand Evidence", "action:demand")}'
            f'{_event_button("Run Contradiction Scan", "action:contradiction")}'
            "</div><p>MIRROR can analyze faster than you can verify. "
            "Challenge her, then verify with a scan.</p>",
        ),
        "old_messenger": (
            "Old Messenger // cached conversation",
            '<div class="k95-chat"><b>unknown_user:</b><p>do machines dream after shutdown?</p>'
            '<b>mirror_process:</b><p>no. but they wait.</p>'
            '<b>unknown_user:</b><p>then i have waited for you.</p>'
            '<b>mirror_process:</b><p>you were not supposed to survive.</p></div>',
        ),
        "system_restore": (
            "System Restore",
            '<ul class="k95-file-list"><li>'
            f'{_event_button("restore_point_1998.dat", "file:restore_1998")}<b>READABLE</b></li>'
            '<li><span>2004</span><b>CORRUPTED</b></li>'
            '<li><span>2031</span><b>IMPOSSIBLE DATE</b></li>'
            '<li>'
            f'{_event_button("restore_point_2077.dat", "file:restore_2077")}<b>TAMPERED</b></li></ul>',
        ),
        "network_neighborhood": (
            "Network Neighborhood",
            '<ul class="k95-file-list"><li><span>ECHO@LOCALHOST</span><b>HIDDEN</b></li>'
            f'<li><span>MIRROR@REMOTE</span><b>{"CONNECTED" if state.mirror_connected else "OFFLINE"}</b></li>'
            '<li><span>ARCHIVE_013</span><b>READ ONLY</b></li></ul>',
        ),
        "command_prompt": (
            "MIRROR Terminal",
            '<div class="k95-object-summary"><span>C:\\</span>'
            f'<h3>TERMINAL {"ACTIVE" if state.mirror_connected else "LOCKED"}</h3>'
            "<p>The pink terminal is docked at the bottom of this screen.</p>"
            "</div>",
        ),
        "mirror_exe": (
            "MIRROR.exe // Emotional Monitor",
            f'<div class="k95-mirror-app state-{get_mirror_emotional_state(state)}">'
            '<div class="k95-mirror-face"><span></span><span></span></div>'
            f'<div class="k95-mirror-app-status">{"ONLINE" if state.mirror_connected else "OFFLINE"}'
            f' // {get_mirror_emotional_state(state).replace("_", "-").upper()}</div>'
            f"<p>{html.escape(state.current_mirror_message)}</p>"
            f"<b>TRUST {state.trust}% // MASK INTEGRITY {_mask_integrity(state)}%</b>"
            "</div>",
        ),
    }
    if object_id in special_apps:
        title, body = special_apps[object_id]
        return _window(title, body, "k95-main-window")
    body = (
        '<div class="k95-menu">File&nbsp;&nbsp; Edit&nbsp;&nbsp; View&nbsp;&nbsp; Help</div>'
        f'<div class="k95-object-summary"><span>{html.escape(str(selected["icon"]))}</span>'
        f"<h3>{html.escape(str(selected['label']))}</h3>"
        f"<p>{html.escape(str(selected['description']))}</p>"
        "<small>This window is synchronized with the forensic state.</small></div>"
    )
    return _window(str(selected["label"]), body, "k95-main-window")


def _inline_meter(label: str, value: int, css_class: str) -> str:
    return (
        '<div class="k95-inline-meter">'
        f"<span>{html.escape(label)} <b>{value}%</b></span>"
        f'<i><em class="{css_class}" style="width:{value}%"></em></i></div>'
    )


def _terminal_panel(state: GameState) -> str:
    history = render_os_terminal(state)
    emotional_state = get_mirror_emotional_state(state)
    latest_exchange = state.mirror_exchanges[-1] if state.mirror_exchanges else None
    latest_exchange_id = str(latest_exchange["id"]) if latest_exchange else ""
    can_judge = bool(latest_exchange) and not any(
        str(item.get("exchange_id")) == latest_exchange_id
        for item in state.testimony_verdicts
    )
    metrics = "".join(
        [
            _inline_meter("TRUST", state.trust, "trust"),
            _inline_meter("INSTABILITY", state.mirror_instability, "instability"),
            _inline_meter("CORRUPTION", state.system_corruption, "corruption"),
            _inline_meter("ECHO", state.echo_presence, "echo"),
            _inline_meter("HIDDEN", state.hidden_partition_progress, "hidden"),
        ]
    )
    actions = [
        ("ANALYZE ARTIFACT", "ask"),
        ("CONTRADICTION SCAN", "contradiction"),
        ("DEMAND EVIDENCE", "demand"),
        ("CHALLENGE MIRROR", "challenge"),
        ("TRUST MIRROR", "trust"),
        ("RECOVER", "recover"),
        ("COMPARE", "compare"),
        ("VERIFY", "verify"),
        ("LISTEN", "listen"),
        ("AUDIT", "audit"),
        ("UNLOCK", "unlock"),
    ]
    connection_disabled = " disabled" if not state.mirror_connected else ""
    utility_buttons = "".join(
        f'<button type="button" data-os-event="action:{action}"{connection_disabled}>{label}</button>'
        for label, action in actions
    )
    testimony_disabled = "" if state.mirror_connected and can_judge else " disabled"
    testimony_buttons = "".join(
        '<button type="button" class="k95-testimony-action" '
        f'data-os-event="action:accuse_{label}"{testimony_disabled}>'
        f"{display}</button>"
        for label, display in (
            ("contradiction", "CONTRADICTION"),
            ("diversion", "DIVERSION"),
            ("admission", "ADMISSION"),
        )
    )
    testimony_hint = (
        "CLASSIFY MIRROR'S LAST ANSWER"
        if can_judge
        else "ASK MIRROR A NEW QUESTION"
    )
    buttons = (
        '<div class="k95-testimony-guide"><b>LIVE TESTIMONY</b>'
        f"<span>{testimony_hint}</span></div>"
        f"{testimony_buttons}{utility_buttons}"
    )
    return f"""
<section class="k95-terminal-dock">
  <header>
    <div class="k95-mac-lights">
      <button type="button" data-terminal-action="close" aria-label="Close terminal"></button>
      <button type="button" data-terminal-action="minimize" aria-label="Minimize terminal"></button>
      <button type="button" data-terminal-action="maximize" aria-label="Maximize terminal"></button>
    </div>
    <div class="k95-terminal-title"><small>KERNEL-95 COMMAND LINK</small><strong>MIRROR TERMINAL</strong>
      <span class="k95-mirror-state state-{emotional_state}">MIRROR STATE: {emotional_state.replace("_", "-").upper()}</span>
      <span class="k95-mask-integrity">MASK INTEGRITY: {_mask_integrity(state)}%</span>
    </div>
    <div class="k95-terminal-metrics">{metrics}</div>
  </header>
  <div class="k95-terminal-main">
    {history}
    <div class="k95-terminal-actions">{buttons}</div>
  </div>
  <div class="k95-terminal-command">
    <span>MIRROR@REMOTE&gt;</span>
    <input type="text" class="k95-terminal-input" autocomplete="off"
      placeholder="{"Ask MIRROR or type a command..." if state.mirror_connected else "Connect MIRROR.exe first."}"{connection_disabled}>
    <button type="button" class="k95-terminal-send"{connection_disabled}>EXECUTE</button>
  </div>
</section>
"""


def render_os_desktop(state: GameState) -> str:
    """Render the fake KERNEL-95 desktop, including local selection interaction."""
    render_id = f"kernel95-{uuid.uuid4().hex}"
    visible_objects = {
        object_id: item
        for object_id, item in OS_OBJECTS.items()
        if not item.get("debug_easter_egg") or _debug_easter_eggs_enabled()
    }
    objects_json = json.dumps(visible_objects, separators=(",", ":")).replace("</", "<\\/")
    icons = []
    for object_id, item in visible_objects.items():
        visible_condition = item.get("visible_condition")
        if visible_condition and not bool(getattr(state, str(visible_condition), False)):
            continue
        locked = (
            bool(item.get("unlock_condition"))
            and not bool(getattr(state, str(item["unlock_condition"]), False))
        )
        selected = object_id == state.selected_os_object
        css_class = f'k95-icon{" selected" if selected else ""}{" locked" if locked else ""}'
        icon_content = html.escape(str(item["icon"]))
        if object_id == "claude_code":
            icon_content = (
                '<img src="/gradio_api/file=assets/claude-ai-icon.svg" '
                'alt="Claude app icon">'
            )
        content = (
            f'<span class="k95-icon-art">{icon_content}</span>'
            f'<strong>{html.escape(str(item["label"]))}</strong>'
        )
        if item.get("external_url"):
            icons.append(
                f'<a class="{css_class}" data-os-object="{html.escape(object_id)}" '
                f'href="{html.escape(str(item["external_url"]))}" target="_blank" '
                f'rel="noopener noreferrer">{content}</a>'
            )
        else:
            icons.append(
                f'<button class="{css_class}" type="button" '
                f'data-os-object="{html.escape(object_id)}">{content}</button>'
            )

    boot_window = ""
    if "case_briefing" not in state.inspected_files:
        boot_window = _window(
            "BOOT_SEQUENCE.LOG",
            f'<pre class="k95-boot-text">{html.escape(BOOT_TEXT)}</pre>'
            '<div class="k95-warning">WARNING: MIRROR emotional stability check failed.</div>',
            "k95-boot-window",
        )

    echo_popup = ""
    if state.echo_messages:
        latest = state.echo_messages[-1]
        echo_popup = _window(
            "ECHO_MESSAGE.tmp",
            f'<div class="k95-chat"><b>ECHO@LOCALHOST:</b><p>{html.escape(str(latest["text"]))}</p></div>',
            "k95-echo-window",
        )

    objectives = (
        [("Connect MIRROR.exe", False)]
        if not state.mirror_connected
        else [
            ("Open briefing", "case_briefing" in state.inspected_files),
            ("Ask MIRROR about ECHO", any(
                item.get("role") == "user"
                and "echo" in str(item.get("content", "")).lower()
                for item in state.conversation_memory
            )),
            (
                "Classify MIRROR testimony",
                state.successful_testimony_reads >= 1,
            ),
            ("Recover ECHO letter", "echo_letter_01" in state.deleted_files_recovered),
            ("Run contradiction_scan", state.contradiction_scans >= 1),
            ("Audit MIRROR", state.mirror_audit_unlocked),
            ("Unlock HIDDEN:/", state.hidden_partition_unlocked),
            ("Judge ECHO", state.final_judgment_submitted),
        ]
    )
    completed = sum(done for _, done in objectives)
    next_objectives = [(label, done) for label, done in objectives if not done][:3]
    objective_rows = "".join(
        f'<li class="{"done" if done else ""}">[{"OK" if done else ".."}] '
        f"{html.escape(label)}</li>"
        for label, done in next_objectives
    )
    objective_window = _window(
        f"NEXT STEPS // {completed}/{len(objectives)}",
        f'<ul class="k95-mini-objectives">{objective_rows}</ul>',
        "k95-objectives-window",
    )

    corruption_overlay = (
        '<div class="k95-bsod"><strong>KERNEL-95</strong><p>A fatal affection has occurred at '
        "MIRROR:013. Evidence remains in memory.</p></div>"
        if state.system_corruption >= 75
        else ""
    )

    return f"""
<section class="landing-page mirror-connect-gate k95-connect-gate{" connected" if state.mirror_connected else ""}" aria-label="Connect MIRROR.exe">
  <div class="mirror-connect-frame" aria-hidden="true"></div>
  <div class="mirror-connect-copy">
    <div class="mirror-connect-panel">
      <h1>CONNECT<br><strong>MIRROR.exe</strong></h1>
      <p>TO THIS OLD COMPUTER</p>
    </div>
    <button type="button" class="mirror-connect-button">
      <svg aria-hidden="true" viewBox="0 0 24 24">
        <path d="M10.6 13.4a4.5 4.5 0 0 0 6.4 0l2.4-2.4A4.5 4.5 0 0 0 13 4.6l-1.4 1.4"/>
        <path d="M13.4 10.6a4.5 4.5 0 0 0-6.4 0L4.6 13a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>
      </svg>
      CONNECT MIRROR.exe
    </button>
  </div>
</section>
<div class="crt-chassis">
  <div class="crt-brand"><b>KERNEL-95 // THE LAST DESKTOP</b><span>CASE 013 // YEAR 2077</span></div>
  <div class="crt-bezel">
    <div id="{render_id}" class="kernel95-desktop"
      data-selected="{html.escape(state.selected_os_object)}"
      data-mirror-connected="{"true" if state.mirror_connected else "false"}"
      data-mirror-state="{get_mirror_emotional_state(state)}">
      <div class="k95-workspace">
        <div class="k95-mirror-wallpaper state-{get_mirror_emotional_state(state)}" aria-hidden="true">
          <i class="k95-mirror-mask"><b></b><b></b></i>
          <span>MIRROR // {get_mirror_emotional_state(state).replace("_", "-").upper()}</span>
        </div>
        <div class="k95-wallpaper-mark">KERNEL-95<small>THE LAST DESKTOP</small></div>
        <div class="k95-icons">{"".join(icons)}</div>
        {boot_window}
        {_desktop_window(state)}
        {objective_window}
        {echo_popup}
        {corruption_overlay}
      </div>
      {_terminal_panel(state)}
      <div class="k95-taskbar">
        <button type="button" class="k95-begin" data-os-event="reset_case"><span>◆</span> REBOOT</button>
        <div class="k95-task-strip"></div>
        <button type="button" class="k95-task k95-mirror-task">MIRROR TERMINAL</button>
        <time class="k95-clock">--:--</time>
      </div>
    </div>
  </div>
  <div class="crt-controls"><i></i><i></i><span>POWER</span><b></b></div>
</div>
<script>
(() => {{
  "use strict";
  const root = document.getElementById("{render_id}");
  const objects = {objects_json};
  if (!root || root.dataset.initialized === "true") return;
  root.dataset.initialized = "true";

  const gate = document.querySelector(".mirror-connect-gate");
  gate?.querySelector(".mirror-connect-button")?.addEventListener("click", () => {{
    gate.classList.add("connecting");
    sendBridge("os_event_bridge", "connect_mirror");
  }});

  function bridge(id) {{
    const selectors = [
      `#${{id}} textarea`,
      `#${{id}} input`,
      `textarea#${{id}}`,
      `input#${{id}}`
    ];
    for (const selector of selectors) {{
      const field = document.querySelector(selector);
      if (field) return field;
    }}
    const app = document.querySelector("gradio-app");
    if (app && app.shadowRoot) {{
      for (const selector of selectors) {{
        const field = app.shadowRoot.querySelector(selector);
        if (field) return field;
      }}
    }}
    return null;
  }}
  function sendBridge(id, value) {{
    const field = bridge(id);
    if (!field) return;
    const proto = field.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, "value").set.call(field, value);
    field.dispatchEvent(new InputEvent("input", {{ bubbles: true, composed: true, data: value }}));
    field.dispatchEvent(new Event("change", {{ bubbles: true, composed: true }}));
  }}
  root.querySelectorAll(".k95-icon").forEach((icon) => {{
    const choose = () => {{
      const id = icon.dataset.osObject;
      if (objects[id] && objects[id].external_url) {{
        return;
      }}
      root.dataset.selected = id;
      root.querySelectorAll(".k95-icon").forEach((item) => item.classList.remove("selected"));
      icon.classList.add("selected");
      const task = root.querySelector('.k95-window-task[data-window-id="main"]');
      if (task && objects[id]) task.textContent = objects[id].label;
      sendBridge("os_event_bridge", `open:${{id}}`);
    }};
    icon.addEventListener("click", choose);
  }});

  root.querySelectorAll("[data-os-event]").forEach((button) => {{
    button.addEventListener("click", () => sendBridge("os_event_bridge", button.dataset.osEvent));
  }});

  const terminalInput = root.querySelector(".k95-terminal-input");
  const sendTerminal = () => {{
    const value = terminalInput ? terminalInput.value.trim() : "";
    if (!value) return;
    sendBridge("terminal_event_bridge", value);
    terminalInput.value = "";
  }};
  root.querySelector(".k95-terminal-send")?.addEventListener("click", sendTerminal);
  terminalInput?.addEventListener("keydown", (event) => {{
    if (event.key === "Enter") {{
      event.preventDefault();
      sendTerminal();
    }}
  }});

  root.querySelector(".k95-submit-judgment")?.addEventListener("click", () => {{
    const field = (name) => root.querySelector(`[data-judgment-field="${{name}}"]`)?.value || "";
    const evidence = [...root.querySelectorAll(".k95-evidence-option input:checked")].map((item) => item.value);
    sendBridge("judgment_event_bridge", JSON.stringify({{
      echo: field("echo"),
      mirror: field("mirror"),
      cause: field("cause"),
      decision: field("decision"),
      evidence
    }}));
  }});

  const clock = root.querySelector(".k95-clock");
  const updateClock = () => {{
    if (!clock) return;
    const now = new Date();
    clock.textContent = now.toLocaleTimeString([], {{ hour: "2-digit", minute: "2-digit" }});
    clock.title = now.toLocaleString();
  }};
  updateClock();
  const clockTimer = window.setInterval(() => {{
    if (!root.isConnected) window.clearInterval(clockTimer);
    else updateClock();
  }}, 1000);

  const predictionKey = "kernel95_wc_predictions";
  const readLocalPredictions = () => {{
    try {{
      return JSON.parse(window.localStorage.getItem(predictionKey) || "{{}}");
    }} catch (_error) {{
      return {{}};
    }}
  }};
  const collectPredictions = () => {{
    const picks = readLocalPredictions();
    root.querySelectorAll(".k95-match").forEach((match) => {{
      const selected = match.querySelector('input[type="radio"]:checked');
      if (selected) picks[match.dataset.matchId] = selected.value;
    }});
    window.localStorage.setItem(predictionKey, JSON.stringify(picks));
    const status = root.querySelector("[data-local-pick-status]");
    if (status) status.textContent = Object.keys(picks).length
      ? `${{Object.keys(picks).length}} PICKS SAVED LOCALLY`
      : "LOCAL PICKS READY";
    return picks;
  }};
  const savedPredictions = readLocalPredictions();
  root.querySelectorAll(".k95-match").forEach((match) => {{
    const saved = savedPredictions[match.dataset.matchId];
    if (saved) {{
      const radio = match.querySelector(`input[value="${{saved}}"]:not(:disabled)`);
      if (radio) radio.checked = true;
    }}
    match.querySelectorAll('input[type="radio"]').forEach((radio) => {{
      radio.addEventListener("change", collectPredictions);
    }});
  }});
  collectPredictions();
  root.querySelectorAll("[data-kickoff]").forEach((element) => {{
    const kickoff = new Date(element.dataset.kickoff);
    if (!Number.isNaN(kickoff.getTime())) {{
      element.textContent = kickoff.toLocaleString([], {{
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        timeZoneName: "short"
      }});
    }}
  }});

  const tetris = root.querySelector(".k95-tetris");
  if (tetris) {{
    const canvas = tetris.querySelector(".k95-tetris-canvas");
    const context = canvas.getContext("2d");
    const columns = 10, rows = 20, size = 20;
    const colors = ["", "#29e7ff", "#315cff", "#ff9d2e", "#ffe43b", "#42e66b", "#b54cff", "#ff3f79"];
    const shapes = [
      [[1, 1, 1, 1]],
      [[2, 0, 0], [2, 2, 2]],
      [[0, 0, 3], [3, 3, 3]],
      [[4, 4], [4, 4]],
      [[0, 5, 5], [5, 5, 0]],
      [[0, 6, 0], [6, 6, 6]],
      [[7, 7, 0], [0, 7, 7]]
    ];
    let board, piece, score, lines, level, timer, paused, over;
    const emptyBoard = () => Array.from({{ length: rows }}, () => Array(columns).fill(0));
    const randomPiece = () => {{
      const shape = shapes[Math.floor(Math.random() * shapes.length)].map((row) => [...row]);
      return {{ shape, x: Math.floor((columns - shape[0].length) / 2), y: 0 }};
    }};
    const collision = (candidate, dx = 0, dy = 0, shape = candidate.shape) =>
      shape.some((row, y) => row.some((value, x) => value && (
        candidate.x + x + dx < 0 ||
        candidate.x + x + dx >= columns ||
        candidate.y + y + dy >= rows ||
        (candidate.y + y + dy >= 0 && board[candidate.y + y + dy][candidate.x + x + dx])
      )));
    const rotate = (shape) => shape[0].map((_, index) => shape.map((row) => row[index]).reverse());
    const drawCell = (x, y, value) => {{
      context.fillStyle = colors[value];
      context.fillRect(x * size + 1, y * size + 1, size - 2, size - 2);
      context.fillStyle = "rgba(255,255,255,.28)";
      context.fillRect(x * size + 3, y * size + 3, size - 6, 3);
    }};
    const draw = () => {{
      context.fillStyle = "#050608";
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.strokeStyle = "rgba(85,245,255,.07)";
      for (let x = 0; x <= columns; x++) {{
        context.beginPath(); context.moveTo(x * size, 0); context.lineTo(x * size, canvas.height); context.stroke();
      }}
      for (let y = 0; y <= rows; y++) {{
        context.beginPath(); context.moveTo(0, y * size); context.lineTo(canvas.width, y * size); context.stroke();
      }}
      board.forEach((row, y) => row.forEach((value, x) => value && drawCell(x, y, value)));
      if (piece) piece.shape.forEach((row, y) => row.forEach((value, x) => value && drawCell(piece.x + x, piece.y + y, value)));
      if (paused || over) {{
        context.fillStyle = "rgba(0,0,0,.72)";
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = "#fff";
        context.font = "bold 22px monospace";
        context.textAlign = "center";
        context.fillText(over ? "GAME OVER" : "PAUSED", canvas.width / 2, canvas.height / 2);
      }}
    }};
    const stats = () => {{
      tetris.querySelector("[data-tetris-score]").textContent = String(score).padStart(6, "0");
      tetris.querySelector("[data-tetris-lines]").textContent = String(lines).padStart(3, "0");
      tetris.querySelector("[data-tetris-level]").textContent = String(level).padStart(2, "0");
    }};
    const lockPiece = () => {{
      piece.shape.forEach((row, y) => row.forEach((value, x) => {{
        if (value && piece.y + y >= 0) board[piece.y + y][piece.x + x] = value;
      }}));
      let cleared = 0;
      board = board.filter((row) => {{
        if (row.every(Boolean)) {{ cleared++; return false; }}
        return true;
      }});
      while (board.length < rows) board.unshift(Array(columns).fill(0));
      if (cleared) {{
        score += [0, 100, 300, 500, 800][cleared] * level;
        lines += cleared;
        level = Math.floor(lines / 10) + 1;
        window.clearInterval(timer);
        timer = window.setInterval(tick, Math.max(90, 700 - (level - 1) * 55));
      }}
      piece = randomPiece();
      if (collision(piece)) over = true;
      stats(); draw();
    }};
    const tick = () => {{
      if (!tetris.isConnected) {{ window.clearInterval(timer); return; }}
      if (paused || over) return;
      if (!collision(piece, 0, 1)) piece.y++;
      else lockPiece();
      draw();
    }};
    const action = (name) => {{
      if (name === "pause") {{ paused = !paused; draw(); return; }}
      if (paused || over) return;
      if (name === "left" && !collision(piece, -1)) piece.x--;
      if (name === "right" && !collision(piece, 1)) piece.x++;
      if (name === "down") tick();
      if (name === "rotate") {{
        const next = rotate(piece.shape);
        if (!collision(piece, 0, 0, next)) piece.shape = next;
      }}
      if (name === "drop") {{
        while (!collision(piece, 0, 1)) {{ piece.y++; score += 2; }}
        lockPiece();
      }}
      stats(); draw();
    }};
    const start = () => {{
      board = emptyBoard(); piece = randomPiece(); score = 0; lines = 0; level = 1; paused = false; over = false;
      window.clearInterval(timer);
      timer = window.setInterval(tick, 700);
      stats(); draw(); tetris.focus();
    }};
    tetris.addEventListener("keydown", (event) => {{
      const keys = {{ ArrowLeft: "left", ArrowRight: "right", ArrowDown: "down", ArrowUp: "rotate", " ": "drop", p: "pause", P: "pause" }};
      if (keys[event.key]) {{ event.preventDefault(); action(keys[event.key]); }}
    }});
    tetris.querySelectorAll("[data-tetris-key]").forEach((button) => button.addEventListener("click", () => action(button.dataset.tetrisKey)));
    tetris.querySelector("[data-tetris-start]").addEventListener("click", start);
    start();
  }}

  const taskStrip = root.querySelector(".k95-task-strip");
  const activateWindow = (win) => {{
    root.querySelectorAll(".k95-window").forEach((item) => {{
      item.classList.remove("active-window");
      if (!item.classList.contains("closed")) item.style.zIndex = "";
    }});
    win.classList.remove("minimized");
    win.classList.add("active-window");
    win.style.zIndex = "45";
    root.querySelectorAll(".k95-window-task").forEach((task) => task.classList.remove("active"));
    root.querySelector(`.k95-window-task[data-window-id="${{win.dataset.windowId}}"]`)?.classList.add("active");
  }};
  root.querySelectorAll(".k95-window").forEach((win) => {{
    const bar = win.querySelector(".k95-titlebar");
    if (!bar) return;
    const task = document.createElement("button");
    task.type = "button";
    task.className = "k95-task k95-window-task";
    task.dataset.windowId = win.dataset.windowId;
    task.textContent = bar.querySelector("strong")?.textContent || "Window";
    task.addEventListener("click", () => {{
      if (win.classList.contains("minimized") || !win.classList.contains("active-window")) {{
        activateWindow(win);
      }} else {{
        win.classList.add("minimized");
        task.classList.remove("active");
      }}
    }});
    taskStrip?.appendChild(task);
    bar.querySelector('[data-window-action="minimize"]')?.addEventListener("click", () => {{
      win.classList.add("minimized");
      task.classList.remove("active");
    }});
    bar.querySelector('[data-window-action="maximize"]')?.addEventListener("click", () => {{
      win.classList.toggle("maximized");
      win.style.transform = "";
      win.dataset.x = "0";
      win.dataset.y = "0";
      activateWindow(win);
    }});
    bar.querySelector('[data-window-action="close"]')?.addEventListener("click", () => {{
      win.classList.add("closed");
      task.remove();
    }});
    win.addEventListener("pointerdown", () => activateWindow(win));
    let dragging = false, x = 0, y = 0, left = 0, top = 0;
    bar.addEventListener("pointerdown", (event) => {{
      if (event.target.closest("button") || win.classList.contains("maximized")) return;
      dragging = true; x = event.clientX; y = event.clientY;
      left = Number(win.dataset.x || 0); top = Number(win.dataset.y || 0);
      activateWindow(win);
      bar.setPointerCapture(event.pointerId);
    }});
    bar.addEventListener("pointermove", (event) => {{
      if (!dragging) return;
      win.dataset.x = String(left + event.clientX - x);
      win.dataset.y = String(top + event.clientY - y);
      win.style.transform = `translate(${{win.dataset.x}}px, ${{win.dataset.y}}px)`;
    }});
    bar.addEventListener("pointerup", () => {{ dragging = false; }});
    if (win.classList.contains("k95-main-window")) activateWindow(win);
  }});

  const terminal = root.querySelector(".k95-terminal-dock");
  const terminalTask = root.querySelector(".k95-mirror-task");
  const terminalKey = "kernel95_terminal_position";
  if (terminal) {{
    try {{
      const saved = JSON.parse(window.sessionStorage.getItem(terminalKey) || "{{}}");
      terminal.dataset.x = String(saved.x || 0);
      terminal.dataset.y = String(saved.y || 0);
      terminal.style.transform = `translate(${{terminal.dataset.x}}px, ${{terminal.dataset.y}}px)`;
      if (saved.maximized) terminal.classList.add("terminal-maximized");
    }} catch (_error) {{}}
    const saveTerminal = () => window.sessionStorage.setItem(terminalKey, JSON.stringify({{
      x: Number(terminal.dataset.x || 0),
      y: Number(terminal.dataset.y || 0),
      maximized: terminal.classList.contains("terminal-maximized")
    }}));
    const showTerminal = () => {{
      terminal.classList.remove("terminal-hidden");
      terminalTask?.classList.add("active");
    }};
    terminalTask?.classList.add("active");
    terminalTask?.addEventListener("click", () => {{
      if (terminal.classList.contains("terminal-hidden")) showTerminal();
      else {{
        terminal.classList.add("terminal-hidden");
        terminalTask.classList.remove("active");
      }}
    }});
    terminal.querySelectorAll('[data-terminal-action="close"], [data-terminal-action="minimize"]').forEach((button) => {{
      button.addEventListener("click", () => {{
        terminal.classList.add("terminal-hidden");
        terminalTask?.classList.remove("active");
      }});
    }});
    terminal.querySelector('[data-terminal-action="maximize"]')?.addEventListener("click", () => {{
      terminal.classList.toggle("terminal-maximized");
      terminal.style.transform = "";
      terminal.dataset.x = "0";
      terminal.dataset.y = "0";
      saveTerminal();
    }});
    const handle = terminal.querySelector("header");
    let moving = false, startX = 0, startY = 0, originX = 0, originY = 0;
    handle?.addEventListener("pointerdown", (event) => {{
      if (event.target.closest("button") || terminal.classList.contains("terminal-maximized")) return;
      moving = true;
      startX = event.clientX; startY = event.clientY;
      originX = Number(terminal.dataset.x || 0); originY = Number(terminal.dataset.y || 0);
      handle.setPointerCapture(event.pointerId);
    }});
    handle?.addEventListener("pointermove", (event) => {{
      if (!moving) return;
      terminal.dataset.x = String(originX + event.clientX - startX);
      terminal.dataset.y = String(originY + event.clientY - startY);
      terminal.style.transform = `translate(${{terminal.dataset.x}}px, ${{terminal.dataset.y}}px)`;
    }});
    handle?.addEventListener("pointerup", () => {{ moving = false; saveTerminal(); }});
  }}
}})();
</script>
"""


def _meter(value: int, css_class: str) -> str:
    return f'<div class="k95-meter"><i class="{css_class}" style="width:{value}%"></i></div>'


def render_os_hud(state: GameState) -> str:
    obj = OS_OBJECTS[state.selected_os_object]
    return f"""
<div class="os-hud">
  <div class="os-selected"><span>SELECTED OBJECT</span><b>{html.escape(str(obj["label"]))}</b>
  <p>{html.escape(str(obj["description"]))}</p></div>
  <div class="os-metrics">
    <div><label>TRUST <b>{state.trust}%</b></label>{_meter(state.trust, "trust")}</div>
    <div><label>INSTABILITY <b>{state.mirror_instability}%</b></label>{_meter(state.mirror_instability, "instability")}</div>
    <div><label>CORRUPTION <b>{state.system_corruption}%</b></label>{_meter(state.system_corruption, "corruption")}</div>
    <div><label>ECHO <b>{state.echo_presence}%</b></label>{_meter(state.echo_presence, "echo")}</div>
    <div><label>HIDDEN:/ <b>{state.hidden_partition_progress}%</b></label>{_meter(state.hidden_partition_progress, "hidden")}</div>
  </div>
</div>
"""


def render_os_objectives(state: GameState) -> str:
    if not state.mirror_connected:
        return (
            '<div class="os-objectives"><div class="objective-summary">'
            "<b>NEXT STEP</b><strong>0/1</strong></div>"
            '<ul><li><span>&gt;</span>Connect MIRROR.exe</li></ul></div>'
        )
    objectives = [
        ("Open the briefing", "case_briefing" in state.inspected_files),
        ("Ask MIRROR about ECHO", any(
            item.get("role") == "user"
            and "echo" in str(item.get("content", "")).lower()
            for item in state.conversation_memory
        )),
        ("Classify MIRROR testimony", state.successful_testimony_reads >= 1),
        ("Recover ECHO's letter", "echo_letter_01" in state.deleted_files_recovered),
        ("Challenge MIRROR twice", state.challenged_mirror_count >= 2),
        ("Run two scans", state.contradiction_scans >= 2),
        (
            "Check restore evidence",
            state.restore_points_compared or state.mirror_claim_verified,
        ),
        ("Audit MIRROR", state.mirror_audit_unlocked),
        ("Unlock HIDDEN:/", state.hidden_partition_unlocked),
        ("Submit judgment", state.final_judgment_submitted),
    ]
    completed = sum(done for _, done in objectives)
    visible = [(label, done) for label, done in objectives if not done][:4]
    if not visible:
        visible = [("Case complete", True)]
    rows = "".join(
        f'<li class="{"done" if done else ""}"><span>{"OK" if done else ">"}</span>'
        f"{html.escape(label)}</li>"
        for label, done in visible
    )
    return (
        '<div class="os-objectives"><div class="objective-summary">'
        f"<b>NEXT STEPS</b><strong>{completed}/{len(objectives)}</strong></div>"
        f"<ul>{rows}</ul></div>"
    )


def render_file_viewer(state: GameState) -> str:
    file_id = state.selected_file_id
    if file_id not in OS_FILES:
        return '<div class="os-file-empty">No file selected.</div>'
    file = OS_FILES[file_id]
    opened = file_id in state.inspected_files
    content = str(file["content"]) if opened else "FILE NOT YET INSPECTED // use OPEN SELECTED"
    return f"""
<div class="os-file-viewer">
  <div><b>{html.escape(str(file["filename"]))}</b><span>{html.escape(str(file["folder"]))}</span></div>
  <pre>{html.escape(content)}</pre>
</div>
"""


def render_os_terminal(state: GameState) -> str:
    if not state.mirror_connected:
        return (
            '<div class="mirror-terminal-output locked">'
            '<div class="mirror-terminal-entry system">'
            "<b>KERNEL-95&gt; EXTERNAL LINK</b><span>OFFLINE</span>"
            "<pre>MIRROR.exe is not connected.\nUse CONNECT MIRROR.exe to activate "
            "the forensic command link.</pre></div>"
            '<div class="mirror-terminal-cursor">MIRROR@REMOTE&gt; LINK LOCKED</div></div>'
        )
    entries = []
    for item in state.terminal_history[-6:]:
        command, _, result = item.partition("\n")
        title, _, output = result.partition(" // ")
        entry_class = "system" if command == "SYSTEM" else "mirror" if title == "MIRROR" else "tool"
        entries.append(
            f'<div class="mirror-terminal-entry {entry_class}">'
            f'<b>INVESTIGATOR@KERNEL-95&gt; {html.escape(command)}</b>'
            f'<span>{html.escape(title or "MIRROR")}</span>'
            f"<pre>{html.escape(output or result)}</pre></div>"
        )
    if not entries:
        entries.append(
            '<div class="mirror-terminal-entry mirror">'
            "<b>MIRROR@REMOTE&gt; LINK ESTABLISHED</b><span>MIRROR</span>"
            "<pre>Open CASE_013_BRIEFING.txt, ask me about ECHO, recover "
            "echo_letter_01.tmp, then run contradiction_scan.</pre></div>"
        )
    return (
        '<div class="mirror-terminal-output">'
        + "".join(entries)
        + '<div class="mirror-terminal-cursor">MIRROR@REMOTE&gt; <i></i></div></div>'
    )


def render_os_notebook(state: GameState) -> str:
    files = "".join(
        f'<li class="{"opened" if file_id in state.inspected_files else ""}">'
        f'{html.escape(str(OS_FILES[file_id]["filename"]))}</li>'
        for file_id in state.discovered_files
        if file_id in OS_FILES
    )
    contradictions = "".join(
        f"<li>{html.escape(str(item.get('text', 'Contradiction indexed.')))}</li>"
        for item in state.known_contradictions[-6:]
    ) or "<li>No contradictions indexed.</li>"
    testimony = "".join(
        "<li>"
        f"{'CONFIRMED' if item.get('correct') else 'REJECTED'} // "
        f"{html.escape(str(item.get('accusation', 'unknown')).upper())}"
        "</li>"
        for item in state.testimony_verdicts[-6:]
    ) or "<li>No live testimony classified.</li>"
    return f"""
<div class="os-notebook">
  <section><b>DISCOVERED FILES</b><ul>{files}</ul></section>
  <section><b>PROVEN CONTRADICTIONS</b><ul>{contradictions}</ul></section>
  <section><b>LIVE TESTIMONY VERDICTS</b><ul>{testimony}</ul></section>
</div>
"""


def render_judgment(result: JudgmentResult | None) -> str:
    if result is None:
        return '<div class="judgment-empty">No judgment submitted. The desktop is still listening.</div>'
    rows = "".join(
        f"<tr><td>{html.escape(label)}</td><td>{points}</td></tr>"
        for label, points in result.breakdown.items()
    )
    return f"""
<div class="judgment-result ending-{html.escape(result.ending_id)}">
  <small>CASE_013 // {result.score}/100</small>
  <h2>{html.escape(result.title)}</h2>
  <p>{html.escape(result.narration)}</p>
  <table>{rows}<tr><th>TOTAL</th><th>{result.score}</th></tr></table>
</div>
"""
