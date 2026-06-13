"""Rendering and small game helpers."""

from __future__ import annotations

import html

from .game_data import CLUE_LABELS, EVIDENCE, GAME_OBJECTS
from .game_state import GameState
from .scoring import ScoreResult


def _meter(value: int, css_class: str) -> str:
    return (
        f'<div class="meter"><div class="meter-fill {css_class}" '
        f'style="width:{value}%"></div></div>'
    )


def render_status(state: GameState) -> str:
    clues = len(state.discovered_clues)
    status = "READY" if state.readiness >= 70 else "BUILDING" if state.readiness >= 35 else "COLD"
    return f"""
<div class="status-grid">
  <div class="stat-card"><span>CASE</span><strong>ACTIVE</strong></div>
  <div class="stat-card"><span>CLUES</span><strong>{clues:02d}</strong></div>
</div>
<div class="metric-label"><span>TRUST // MIRROR</span><b>{state.trust}%</b></div>
{_meter(state.trust, "trust-fill")}
<div class="metric-label"><span>MODEL CORRUPTION</span><b>{state.corruption}%</b></div>
{_meter(state.corruption, "corruption-fill")}
<div class="metric-label"><span>ACCUSATION // {status}</span><b>{state.readiness}%</b></div>
{_meter(state.readiness, "readiness-fill")}
"""


def render_clues(state: GameState) -> str:
    if not state.discovered_clues:
        return '<div class="empty-state">NO VERIFIED CLUES // interrogate the artifacts</div>'
    items = "".join(
        f'<li><span class="clue-index">{index:02d}</span>{html.escape(CLUE_LABELS.get(clue, clue))}</li>'
        for index, clue in enumerate(state.discovered_clues, 1)
    )
    return f'<ul class="clue-list">{items}</ul>'


def render_feed(state: GameState) -> str:
    lines = []
    for item in reversed(state.feed[-10:]):
        prefix, separator, body = item.partition(" // ")
        if separator:
            lines.append(
                f'<div class="feed-line"><span>{html.escape(prefix)}</span>'
                f'{html.escape(body)}</div>'
            )
        else:
            lines.append(f'<div class="feed-line">{html.escape(item)}</div>')
    return '<div class="case-feed">' + "".join(lines) + "</div>"


def render_evidence(name: str) -> str:
    evidence = EVIDENCE[name]
    return f"""
<div class="evidence-header">
  <span class="evidence-kind">{html.escape(str(evidence['kind']))}</span>
  <span>INTEGRITY // DEGRADED</span>
</div>
<h3>{html.escape(name)}</h3>
<p class="evidence-summary">{html.escape(str(evidence['summary']))}</p>
<pre>{html.escape(str(evidence['content']))}</pre>
"""


def render_terminal(state: GameState, latest: str = "") -> str:
    history = state.terminal_history[-8:]
    blocks = ['<div class="terminal-banner">CODEX NOIR SHELL v0.13 // evidence sandbox</div>']
    for entry in history:
        command, _, response = entry.partition("\n")
        blocks.append(f'<div class="terminal-command">trace@metrogrid:~$ {html.escape(command)}</div>')
        blocks.append(f'<div class="terminal-response">{html.escape(response)}</div>')
    if not history and not latest:
        blocks.append('<div class="terminal-response">Type `help` to list recovered commands.</div>')
    return '<div class="terminal-screen">' + "".join(blocks) + "</div>"


def render_theory(state: GameState) -> str:
    if not state.theory_notes:
        return "No pinned theory fragments."
    return "\n".join(f"- {note}" for note in state.theory_notes[-6:])


def _notebook_entries(
    items: list[dict[str, object]],
    text_key: str,
    empty: str,
    badge_key: str,
) -> str:
    if not items:
        return f'<div class="notebook-empty">{html.escape(empty)}</div>'
    rendered = []
    for item in items[-4:]:
        badge = str(item.get(badge_key, "info"))
        text = str(item.get(text_key, item.get("text", "Recorded.")))
        rendered.append(
            '<div class="notebook-entry">'
            f'<span class="notebook-badge badge-{html.escape(badge)}">'
            f'{html.escape(badge)}</span>'
            f"<p>{html.escape(text)}</p></div>"
        )
    return "".join(rendered)


def render_notebook(state: GameState) -> str:
    theories = [
        {
            "claim": item.get("claim", ""),
            "status": item.get("status", "untested"),
        }
        for item in state.pinned_theories
    ]
    traces = [
        {
            "summary": f"[{item.get('tool', 'tool')}] {item.get('summary', '')}",
            "severity": item.get("severity", "info"),
        }
        for item in state.tool_trace
    ]
    secret = (
        '<div class="notebook-secret">SUPPRESSED MEMORY DETECTED</div>'
        if state.secret_unlocked
        else '<div class="notebook-lock">MIRROR MEMORY AUDIT // LOCKED</div>'
    )
    return f"""
<div class="investigation-notebook">
  <div class="notebook-readiness">
    <span>ACCUSATION READINESS</span><strong>{state.readiness}%</strong>
    {_meter(state.readiness, "readiness-fill")}
  </div>
  {secret}
  <div class="notebook-grid">
    <section>
      <h4>KNOWN FACTS</h4>
      {_notebook_entries(state.known_facts, "text", "No deterministic facts indexed.", "strength")}
    </section>
    <section>
      <h4>MIRROR CLAIMS</h4>
      {_notebook_entries(state.mirror_claims, "text", "No MIRROR claims recorded.", "strength")}
    </section>
    <section>
      <h4>KNOWN CONTRADICTIONS</h4>
      {_notebook_entries(state.known_contradictions, "text", "No contradictions proven.", "severity")}
    </section>
    <section>
      <h4>PINNED THEORIES</h4>
      {_notebook_entries(theories, "claim", "No theories pinned.", "status")}
    </section>
  </div>
  <section class="notebook-trace">
    <h4>LATEST TOOL TRACE</h4>
    {_notebook_entries(traces, "summary", "No tools executed.", "severity")}
  </section>
</div>
"""


def render_game_hud(state: GameState) -> str:
    obj = GAME_OBJECTS.get(state.selected_3d_object, GAME_OBJECTS["mirror_core"])
    vault_steps = [
        (state.challenged_mirror_count, 2, "MIRROR CHALLENGES"),
        (state.contradiction_scans, 2, "CONTRADICTION SCANS"),
        (1 if "duplicate_token" in state.discovered_clues else 0, 1, "J-17 DUPLICATION"),
    ]
    vault_progress = sum(min(current, required) for current, required, _ in vault_steps)
    vault_total = sum(required for _, required, _ in vault_steps)
    progress = round(vault_progress / vault_total * 100)
    progress_rows = "".join(
        (
            '<div class="audit-step">'
            f"<span>{html.escape(label)}</span>"
            f"<b>{min(current, required)}/{required}</b>"
            "</div>"
        )
        for current, required, label in vault_steps
    )
    vault_status = (
        "BREACHED"
        if state.secret_unlocked
        else "ACCESS READY"
        if state.memory_vault_unlocked
        else "ENCRYPTED"
    )
    return f"""
<div class="tactical-hud">
  <div class="hud-selected">
    <span>SELECTED // {html.escape(str(obj['type'])).upper()}</span>
    <h3>{html.escape(str(obj['label']))}</h3>
    <p>{html.escape(str(obj.get('description', 'No description recovered.')))}</p>
  </div>
  <div class="hud-meter-row">
    <div><span>TRUST</span><strong>{state.trust}%</strong>{_meter(state.trust, "trust-fill")}</div>
    <div><span>CORRUPTION</span><strong>{state.corruption}%</strong>{_meter(state.corruption, "corruption-fill")}</div>
  </div>
  <div class="audit-progress">
    <div class="audit-heading"><span>MEMORY VAULT // {vault_status}</span><b>{progress}%</b></div>
    {_meter(progress, "readiness-fill")}
    {progress_rows}
  </div>
</div>
"""


def render_objectives(state: GameState) -> str:
    objectives = [
        ("Scan sector log", "Corrupted Sector Log" in state.analyzed_evidence),
        ("Find duplicate token", "duplicate_token" in state.discovered_clues),
        ("Inspect commit", "janitor_commit" in state.discovered_clues),
        ("Decode memory filter", "thirteen_minute_filter" in state.discovered_clues),
        ("Challenge MIRROR twice", state.challenged_mirror_count >= 2),
        ("Audit MIRROR memory", state.secret_unlocked),
        ("Submit accusation", state.accusation_submitted),
    ]
    completed = sum(done for _, done in objectives)
    rows = "".join(
        (
            f'<div class="objective{" complete" if done else ""}">'
            f'<span class="objective-mark">{"OK" if done else ".."}</span>'
            f"<span>{html.escape(label)}</span></div>"
        )
        for label, done in objectives
    )
    return f"""
<div class="objective-tracker">
  <div class="objective-header"><span>CASE OBJECTIVES</span><b>{completed}/{len(objectives)}</b></div>
  {rows}
  <details>
    <summary>DEMO PATH</summary>
    <p>Select and scan the Sector Log. Run a forensic scan. Trace J-17. Challenge MIRROR twice.
    Run a second scan, breach the vault, then build the accusation.</p>
  </details>
</div>
"""


def render_score(result: ScoreResult, verdict: str) -> str:
    breakdown = "".join(
        f"<tr><td>{html.escape(label)}</td><td>{points}</td></tr>"
        for label, points in result.breakdown.items()
    )
    feedback = "".join(f"<li>{html.escape(item)}</li>" for item in result.feedback)
    ending_class = f"ending-{result.ending}"
    return f"""
<div class="ending-card {ending_class}">
  <div class="ending-kicker">CASE RESOLUTION // SCORE {result.total}/100</div>
  <h2>{html.escape(result.title)}</h2>
  <div class="verdict">{verdict}</div>
  <table>{breakdown}<tr class="score-total"><td>TOTAL</td><td>{result.total}</td></tr></table>
  <ul>{feedback}</ul>
</div>
"""
