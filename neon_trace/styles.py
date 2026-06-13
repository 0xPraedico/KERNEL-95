"""Premium pink/black cyberpunk visual system for the Gradio interface."""

CSS = r"""
:root {
  --bg: #050307;
  --panel: #0d0711;
  --panel-2: #160b1d;
  --text: #fff7fd;
  --muted: #c3a9bf;
  --hot-pink: #ff2da6;
  --magenta: #db1fff;
  --violet: #7c3cff;
  --cyan: #55f5ff;
  --danger: #ff3b6b;
  --border: rgba(255, 45, 166, 0.42);

  /* Override Gradio's pale default theme at the source. */
  --body-background-fill: var(--bg);
  --body-text-color: var(--text);
  --block-background-fill: var(--panel);
  --block-border-color: var(--border);
  --block-label-background-fill: transparent;
  --block-label-text-color: var(--muted);
  --input-background-fill: #08040b;
  --input-border-color: rgba(255, 45, 166, 0.48);
  --input-placeholder-color: #896f86;
  --button-primary-background-fill: var(--hot-pink);
  --button-primary-text-color: #ffffff;
  --button-secondary-background-fill: #170a1c;
  --button-secondary-text-color: var(--text);
  --border-color-primary: var(--border);
  --shadow-drop: 0 18px 55px rgba(0, 0, 0, 0.46);
  --radius-lg: 12px;
  --radius-md: 9px;
  --radius-sm: 6px;
}

html {
  background: var(--bg);
  color-scheme: dark;
}

body {
  min-height: 100vh;
  margin: 0;
  background:
    radial-gradient(circle at 10% 4%, rgba(255, 31, 166, 0.28), transparent 30rem),
    radial-gradient(circle at 91% 20%, rgba(0, 229, 255, 0.20), transparent 36rem),
    radial-gradient(circle at 52% 92%, rgba(255, 214, 0, 0.10), transparent 30rem),
    linear-gradient(180deg, #09040d 0%, #030207 52%, #0b0310 100%),
    var(--bg) !important;
  color: var(--text) !important;
  font-family: "JetBrains Mono", "IBM Plex Mono", "SFMono-Regular", Consolas,
    "Liberation Mono", monospace !important;
  font-size: 15px !important;
  line-height: 1.65 !important;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.28;
  background-image:
    linear-gradient(rgba(85, 245, 255, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 45, 166, 0.16) 1px, transparent 1px);
  background-size: 72px 72px;
  perspective: 500px;
  transform-origin: center bottom;
  animation: grid-drift 24s linear infinite;
  mask-image: linear-gradient(to bottom, transparent 2%, black 42%, transparent 96%);
}

body::after {
  content: "";
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 0;
  height: 44vh;
  pointer-events: none;
  opacity: 0.34;
  background:
    linear-gradient(90deg,
      transparent 0 4%, #18041c 4% 10%, transparent 10% 13%,
      #0c1420 13% 20%, transparent 20% 24%, #21051e 24% 31%,
      transparent 31% 38%, #090d18 38% 47%, transparent 47% 51%,
      #21051d 51% 61%, transparent 61% 66%, #07131b 66% 74%,
      transparent 74% 80%, #1b041a 80% 91%, transparent 91%),
    repeating-linear-gradient(90deg, transparent 0 18px, rgba(255, 45, 166, 0.38) 19px 20px, transparent 21px 38px);
  clip-path: polygon(0 35%, 4% 35%, 4% 8%, 10% 8%, 10% 44%, 13% 44%, 13% 20%,
    20% 20%, 20% 52%, 24% 52%, 24% 13%, 31% 13%, 31% 40%, 38% 40%, 38% 0,
    47% 0, 47% 48%, 51% 48%, 51% 17%, 61% 17%, 61% 38%, 66% 38%, 66% 9%,
    74% 9%, 74% 46%, 80% 46%, 80% 22%, 91% 22%, 91% 39%, 100% 39%, 100% 100%, 0 100%);
  filter: drop-shadow(0 -8px 22px rgba(255, 45, 166, 0.22));
}

@keyframes grid-drift {
  from { background-position: 0 0, 0 0; }
  to { background-position: 0 64px, 64px 0; }
}

.gradio-container {
  position: relative;
  z-index: 1;
  max-width: 2400px !important;
  min-height: 100vh;
  padding: 18px 28px 56px !important;
  background: transparent !important;
  color: var(--text) !important;
  font-family: inherit !important;
  font-size: 15px !important;
}

.gradio-container,
.gradio-container * {
  box-sizing: border-box;
}

.gradio-container::before,
.gradio-container::after {
  position: fixed;
  z-index: -1;
  top: 15%;
  padding: 15px 9px;
  border: 1px solid currentColor;
  background: rgba(4, 2, 8, 0.82);
  font: 800 10px/1.2 "JetBrains Mono", monospace;
  letter-spacing: 0.18em;
  writing-mode: vertical-rl;
  text-orientation: mixed;
  box-shadow: 0 0 24px currentColor;
}

.gradio-container::before {
  content: "NIGHT CITY // SECTOR 07";
  left: 18px;
  color: #ff2da6;
}

.gradio-container::after {
  content: "2077 // METROGRID";
  right: 18px;
  color: #55f5ff;
}

.gradio-container > footer,
footer {
  display: none !important;
}

.app-shell::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 40;
  pointer-events: none;
  opacity: 0.055;
  background-image: repeating-linear-gradient(
    0deg,
    transparent 0,
    transparent 4px,
    rgba(255, 255, 255, 0.16) 5px
  );
}

.hero {
  position: relative;
  margin-bottom: 26px;
  padding: 48px 10px 30px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.5);
}

.hero::before {
  content: "";
  position: absolute;
  left: 10px;
  bottom: -2px;
  width: min(360px, 45vw);
  height: 3px;
  background: linear-gradient(90deg, var(--hot-pink), var(--magenta), transparent);
  box-shadow: 0 0 22px rgba(255, 45, 166, 0.85);
}

.hero::after {
  content: "CASE 013 // LIVE";
  position: absolute;
  right: 10px;
  top: 58px;
  padding: 7px 11px;
  border: 1px solid rgba(85, 245, 255, 0.5);
  border-radius: 999px;
  background: rgba(5, 3, 7, 0.74);
  color: var(--cyan);
  box-shadow: 0 0 20px rgba(85, 245, 255, 0.12);
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: 0.12em;
}

.eyebrow,
.panel-label {
  color: var(--cyan);
  font-size: 12px;
  font-weight: 800;
  line-height: 1.5;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  text-shadow: 0 0 12px rgba(85, 245, 255, 0.3);
}

.hero h1 {
  margin: 5px 0 0;
  color: var(--text);
  font-size: clamp(58px, 7.5vw, 112px);
  font-weight: 900;
  line-height: 0.9;
  letter-spacing: -0.075em;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.3),
    0 0 34px rgba(255, 45, 166, 0.36),
    4px 4px 0 rgba(219, 31, 255, 0.62);
}

.hero h2 {
  margin: 17px 0 7px;
  color: var(--hot-pink);
  font-size: clamp(22px, 2.1vw, 32px);
  font-weight: 850;
  line-height: 1.15;
  text-shadow: 0 0 20px rgba(255, 45, 166, 0.46);
}

.hero p {
  max-width: 780px;
  margin: 12px 0 0;
  color: #e2cfe0;
  font-size: 16px;
  line-height: 1.65;
}

/* Panels and Gradio blocks */
.gradio-container .neon-panel {
  position: relative;
  overflow: hidden;
  margin-bottom: 16px !important;
  padding: 22px !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  background:
    linear-gradient(145deg, rgba(27, 11, 32, 0.98), rgba(8, 4, 12, 0.98)) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.055),
    inset 0 0 42px rgba(219, 31, 255, 0.025),
    0 18px 58px rgba(0, 0, 0, 0.48),
    0 0 24px rgba(255, 45, 166, 0.055) !important;
}

.gradio-container .neon-panel::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 2px;
  background: linear-gradient(180deg, transparent, var(--hot-pink), transparent);
  opacity: 0.9;
}

.gradio-container .neon-panel.pink {
  border-color: rgba(255, 45, 166, 0.65) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    0 18px 58px rgba(0, 0, 0, 0.5),
    0 0 30px rgba(255, 45, 166, 0.08) !important;
}

.gradio-container .neon-panel.acid {
  border-color: rgba(124, 60, 255, 0.55) !important;
}

.gradio-container .neon-panel > div,
.gradio-container .neon-panel .form,
.gradio-container .neon-panel .block {
  background-color: transparent !important;
}

.section-title {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  margin: -2px 0 18px;
  padding: 0 0 13px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.24);
}

.section-title strong {
  color: var(--text);
  font-size: 15px;
  font-weight: 900;
  line-height: 1.3;
  letter-spacing: 0.075em;
  text-shadow: 0 0 15px rgba(255, 45, 166, 0.3);
}

.section-title > span {
  color: var(--cyan);
  font-size: 11px;
  font-weight: 750;
  line-height: 1.35;
  letter-spacing: 0.06em;
  text-align: right;
}

.mirror-title {
  justify-content: flex-start;
}

.mirror-title > span:last-child {
  margin-left: auto;
}

.mirror-orb {
  position: relative;
  display: inline-block;
  flex: 0 0 auto;
  width: 13px;
  height: 13px;
  border: 2px solid #ffc5e8;
  border-radius: 50%;
  background: var(--hot-pink);
  box-shadow:
    0 0 8px var(--hot-pink),
    0 0 20px rgba(255, 45, 166, 0.86),
    0 0 38px rgba(219, 31, 255, 0.46);
  animation: mirror-pulse 2.2s ease-in-out infinite;
}

.mirror-orb::after {
  content: "";
  position: absolute;
  inset: -7px;
  border: 1px solid rgba(255, 45, 166, 0.5);
  border-radius: 50%;
  animation: mirror-ring 2.2s ease-out infinite;
}

@keyframes mirror-pulse {
  0%, 100% { transform: scale(0.88); filter: brightness(0.9); }
  50% { transform: scale(1.12); filter: brightness(1.35); }
}

@keyframes mirror-ring {
  0% { transform: scale(0.55); opacity: 0.8; }
  75%, 100% { transform: scale(1.35); opacity: 0; }
}

/* Case status and meters */
.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 8px 0 20px;
}

.stat-card {
  padding: 14px;
  border: 1px solid rgba(255, 45, 166, 0.24);
  border-radius: 8px;
  background: linear-gradient(145deg, rgba(255, 45, 166, 0.09), rgba(124, 60, 255, 0.04));
}

.stat-card span {
  display: block;
  margin-bottom: 5px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.stat-card strong {
  color: var(--hot-pink);
  font-size: 22px;
  font-weight: 900;
  line-height: 1.15;
  text-shadow: 0 0 15px rgba(255, 45, 166, 0.42);
}

.metric-label {
  display: flex;
  gap: 12px;
  justify-content: space-between;
  margin-top: 16px;
  color: #dcc6d9;
  font-size: 12px;
  font-weight: 750;
  line-height: 1.4;
  letter-spacing: 0.045em;
}

.metric-label b {
  color: var(--text);
  font-size: 13px;
}

.meter {
  height: 10px;
  margin-top: 8px;
  overflow: hidden;
  border: 1px solid rgba(255, 45, 166, 0.22);
  border-radius: 999px;
  background: #050207;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.9);
}

.meter-fill {
  height: 100%;
  min-width: 3px;
  border-radius: inherit;
  transition: width 400ms ease;
}

.trust-fill {
  background: linear-gradient(90deg, var(--hot-pink), var(--magenta) 55%, var(--cyan));
  box-shadow: 0 0 14px rgba(255, 45, 166, 0.75);
}

.corruption-fill {
  background: linear-gradient(90deg, #b80f52, var(--danger), var(--hot-pink));
  box-shadow: 0 0 14px rgba(255, 59, 107, 0.72);
}

.readiness-fill {
  background: linear-gradient(90deg, var(--violet), var(--magenta));
  box-shadow: 0 0 14px rgba(124, 60, 255, 0.72);
}

/* Clues and theory */
.clue-list {
  max-height: 360px;
  margin: 5px 0 0 !important;
  padding: 0 !important;
  overflow: auto;
  list-style: none !important;
}

.clue-list li {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
  padding: 12px;
  border: 1px solid rgba(255, 45, 166, 0.16);
  border-radius: 7px;
  background: rgba(255, 45, 166, 0.045);
  color: #f3dfef;
  font-size: 13px;
  line-height: 1.55;
}

.clue-index {
  color: var(--hot-pink);
  font-size: 12px;
  font-weight: 900;
  line-height: 1.55;
}

.empty-state {
  padding: 24px 7px;
  color: #baa0b6;
  font-size: 13px;
  line-height: 1.7;
}

/* MIRROR output */
.gradio-container .mirror-screen {
  min-height: 270px;
  padding: 22px !important;
  border: 1px solid rgba(255, 45, 166, 0.28) !important;
  border-left: 3px solid var(--hot-pink) !important;
  border-radius: 8px !important;
  background:
    radial-gradient(circle at 95% 5%, rgba(219, 31, 255, 0.13), transparent 45%),
    #08040c !important;
  box-shadow:
    inset 0 0 34px rgba(219, 31, 255, 0.045),
    0 0 20px rgba(255, 45, 166, 0.035);
}

.mirror-screen h1,
.mirror-screen h2,
.mirror-screen h3 {
  color: var(--hot-pink) !important;
  font-family: inherit !important;
  font-size: 17px !important;
  font-weight: 900 !important;
  line-height: 1.45 !important;
  letter-spacing: 0.03em;
  text-shadow: 0 0 14px rgba(255, 45, 166, 0.32);
}

.mirror-screen p,
.mirror-screen li,
.mirror-screen strong,
.mirror-screen em {
  color: var(--text) !important;
  font-size: 14px !important;
  line-height: 1.75 !important;
}

.mirror-screen code {
  color: var(--cyan) !important;
}

/* Feed */
.case-feed {
  max-height: 315px;
  overflow: auto;
}

.feed-line {
  margin-bottom: 8px;
  padding: 12px 13px;
  border: 1px solid rgba(255, 45, 166, 0.13);
  border-left: 2px solid rgba(255, 45, 166, 0.55);
  border-radius: 6px;
  background: rgba(255, 45, 166, 0.035);
  color: #d9c3d5;
  font-size: 12px;
  line-height: 1.65;
}

.feed-line span {
  display: inline-block;
  margin-right: 9px;
  color: var(--hot-pink);
  font-weight: 900;
  text-shadow: 0 0 10px rgba(255, 45, 166, 0.3);
}

/* Evidence board */
.evidence-viewer {
  min-height: 390px;
  padding: 2px 0 0 !important;
  color: var(--text) !important;
}

.evidence-header {
  display: flex;
  gap: 12px;
  justify-content: space-between;
  margin-top: 8px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: 0.055em;
}

.evidence-kind {
  color: var(--hot-pink);
  font-weight: 900;
}

.evidence-viewer h3 {
  margin: 17px 0 6px !important;
  color: var(--text) !important;
  font-family: inherit !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  line-height: 1.35 !important;
  text-shadow: 0 0 17px rgba(255, 45, 166, 0.22);
}

.evidence-summary {
  margin-bottom: 16px !important;
  color: #d2b9ce !important;
  font-size: 13px !important;
  line-height: 1.65 !important;
}

.evidence-viewer pre,
.gradio-container pre {
  min-height: 200px;
  margin: 0 !important;
  padding: 20px !important;
  overflow: auto;
  white-space: pre-wrap;
  border: 1px solid rgba(85, 245, 255, 0.32) !important;
  border-radius: 8px !important;
  background: #020305 !important;
  color: #cbfbff !important;
  box-shadow:
    inset 0 0 30px rgba(85, 245, 255, 0.035),
    0 0 18px rgba(85, 245, 255, 0.035);
  font-family: inherit !important;
  font-size: 13px !important;
  line-height: 1.7 !important;
}

/* Codex Noir terminal */
.terminal-screen {
  min-height: 320px;
  max-height: 430px;
  padding: 20px;
  overflow: auto;
  border: 1px solid rgba(85, 245, 255, 0.42);
  border-radius: 8px;
  background:
    linear-gradient(rgba(85, 245, 255, 0.018), rgba(85, 245, 255, 0.018)),
    #010204;
  box-shadow:
    inset 0 0 45px rgba(85, 245, 255, 0.035),
    0 0 24px rgba(85, 245, 255, 0.055);
  color: var(--text);
  font-size: 13px;
  line-height: 1.75;
}

.terminal-banner {
  margin-bottom: 15px;
  padding-bottom: 12px;
  border-bottom: 1px dashed rgba(85, 245, 255, 0.35);
  color: var(--cyan);
  font-size: 13px;
  font-weight: 900;
  text-shadow: 0 0 12px rgba(85, 245, 255, 0.34);
}

.terminal-command {
  margin-top: 14px;
  color: var(--hot-pink);
  font-weight: 850;
}

.terminal-response {
  margin-top: 3px;
  color: #d6faff;
  white-space: pre-wrap;
}

/* Inputs, dropdowns, textboxes */
.gradio-container label,
.gradio-container label span {
  color: #d7bfd3 !important;
  font-family: inherit !important;
  font-size: 12px !important;
  font-weight: 750 !important;
  line-height: 1.45 !important;
  letter-spacing: 0.035em !important;
}

.gradio-container input,
.gradio-container textarea,
.gradio-container select,
.gradio-container [role="combobox"],
.gradio-container .wrap {
  border-color: rgba(255, 45, 166, 0.42) !important;
  background: #070309 !important;
  color: var(--text) !important;
  font-family: inherit !important;
  font-size: 14px !important;
  line-height: 1.55 !important;
  box-shadow: inset 0 0 16px rgba(219, 31, 255, 0.025) !important;
}

.gradio-container input,
.gradio-container textarea {
  padding: 12px 13px !important;
}

.gradio-container input:focus,
.gradio-container textarea:focus,
.gradio-container [role="combobox"]:focus-within {
  border-color: var(--hot-pink) !important;
  outline: none !important;
  box-shadow:
    0 0 0 2px rgba(255, 45, 166, 0.13),
    0 0 20px rgba(255, 45, 166, 0.10) !important;
}

.gradio-container input::placeholder,
.gradio-container textarea::placeholder {
  color: #876d83 !important;
  opacity: 1;
}

.gradio-container [role="listbox"],
.gradio-container ul.options {
  border: 1px solid var(--border) !important;
  background: #0b050e !important;
  color: var(--text) !important;
}

/* Buttons */
.gradio-container button {
  min-height: 46px;
  border: 1px solid rgba(255, 45, 166, 0.52) !important;
  border-radius: 7px !important;
  background: linear-gradient(135deg, #190a1e, #0d0711) !important;
  color: var(--text) !important;
  font-family: inherit !important;
  font-size: 13px !important;
  font-weight: 900 !important;
  line-height: 1.25 !important;
  letter-spacing: 0.025em;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    0 8px 22px rgba(0, 0, 0, 0.3) !important;
  transition:
    transform 150ms ease,
    border-color 150ms ease,
    box-shadow 150ms ease,
    filter 150ms ease !important;
}

.gradio-container button.primary,
.gradio-container .primary button {
  border-color: rgba(255, 126, 203, 0.75) !important;
  background: linear-gradient(100deg, #ff188f, var(--hot-pink) 43%, #a722ee) !important;
  color: #ffffff !important;
  text-shadow: 0 1px 3px rgba(60, 0, 38, 0.7);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.28),
    0 0 24px rgba(255, 45, 166, 0.24),
    0 9px 24px rgba(0, 0, 0, 0.38) !important;
}

.gradio-container button.secondary {
  border-color: rgba(219, 31, 255, 0.62) !important;
  background: linear-gradient(135deg, rgba(124, 60, 255, 0.17), rgba(255, 45, 166, 0.08)) !important;
  color: #ffd9f2 !important;
}

.gradio-container button:hover {
  z-index: 2;
  transform: translateY(-2px);
  border-color: var(--hot-pink) !important;
  filter: brightness(1.13);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 25px rgba(255, 45, 166, 0.24),
    0 12px 26px rgba(0, 0, 0, 0.42) !important;
}

.gradio-container button:active {
  transform: translateY(0);
}

.terminal-action button,
button.terminal-action {
  border-color: rgba(85, 245, 255, 0.65) !important;
  background: linear-gradient(100deg, #0ea8b3, var(--cyan)) !important;
  color: #02090b !important;
  text-shadow: none !important;
  box-shadow: 0 0 22px rgba(85, 245, 255, 0.15) !important;
}

/* Markdown, code and result surfaces */
.gradio-container .prose,
.gradio-container .prose p,
.gradio-container .prose li {
  color: var(--text);
  font-family: inherit !important;
  line-height: 1.7;
}

.gradio-container code {
  border-radius: 4px;
  background: rgba(85, 245, 255, 0.08);
  color: var(--cyan);
  font-family: inherit !important;
  font-size: 0.94em;
}

.ending-card {
  margin-top: 22px;
  padding: 28px;
  border: 1px solid var(--hot-pink);
  border-radius: 12px;
  background:
    radial-gradient(circle at 90% 0%, rgba(219, 31, 255, 0.15), transparent 38%),
    var(--panel);
  box-shadow: 0 0 34px rgba(255, 45, 166, 0.12);
}

.ending-card h2 {
  color: var(--hot-pink);
  font-family: inherit;
  font-size: 24px;
  font-weight: 900;
  text-shadow: 0 0 16px rgba(255, 45, 166, 0.34);
}

.ending-kicker {
  color: var(--cyan);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.ending-card table {
  width: 100%;
  margin: 18px 0;
  border-collapse: collapse;
  font-size: 13px;
}

.ending-card td {
  padding: 10px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.16);
}

.ending-card td:last-child {
  color: var(--hot-pink);
  font-weight: 900;
  text-align: right;
}

.ending-card li,
.verdict p {
  color: #ead6e6 !important;
  font-size: 14px;
  line-height: 1.65;
}

.ending-bad {
  border-color: var(--danger);
}

.ending-secret {
  border-color: var(--magenta);
  box-shadow: 0 0 45px rgba(219, 31, 255, 0.2);
}

.footer-note {
  padding: 32px;
  color: #9e8299;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0.08em;
  text-align: center;
}

/* Game-first layout */
.game-hero {
  display: flex;
  gap: 22px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  padding: 18px 5px 15px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.42);
}

.game-hero h1 {
  margin: 0;
  color: var(--text);
  font-size: clamp(28px, 4vw, 54px);
  font-weight: 950;
  line-height: 1;
  letter-spacing: -0.045em;
  text-shadow: 0 0 24px rgba(255, 45, 166, 0.35), 2px 2px 0 rgba(219, 31, 255, 0.52);
}

.game-hero h1 span {
  color: var(--hot-pink);
  font-size: 0.46em;
  letter-spacing: 0;
}

.game-hero p {
  margin: 7px 0 0;
  color: #d9c0d4;
  font-size: 13px;
}

.game-hero-status {
  flex: 0 0 auto;
  padding: 8px 12px;
  border: 1px solid rgba(85, 245, 255, 0.45);
  border-radius: 999px;
  color: var(--cyan);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.07em;
}

.game-viewport-panel {
  padding: 8px !important;
}

.scene-object-bridge {
  position: fixed !important;
  top: -10000px !important;
  left: -10000px !important;
  width: 1px !important;
  height: 1px !important;
  overflow: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

.sector7-game {
  position: relative;
  width: 100%;
  height: clamp(620px, 72vh, 780px);
  min-height: 620px;
  overflow: hidden;
  border: 1px solid rgba(255, 45, 166, 0.58);
  border-radius: 10px;
  background:
    radial-gradient(circle at 50% 42%, rgba(124, 60, 255, 0.16), transparent 36%),
    linear-gradient(180deg, #07020a, #020103);
  box-shadow:
    inset 0 0 80px rgba(219, 31, 255, 0.06),
    0 0 35px rgba(255, 45, 166, 0.09);
  user-select: none;
}

.sector7-canvas-mount,
.sector7-canvas-mount canvas,
.sector7-label-layer {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
}

.sector7-label-layer {
  z-index: 5;
  overflow: hidden;
  pointer-events: none;
}

.sector7-world-label {
  position: absolute;
  top: 0;
  left: 0;
  max-width: 170px;
  padding: 5px 8px;
  border: 1px solid rgba(255, 45, 166, 0.34) !important;
  border-radius: 4px !important;
  background: rgba(5, 2, 8, 0.78) !important;
  color: #f4dcea !important;
  font-family: inherit !important;
  font-size: 9px !important;
  font-weight: 850 !important;
  line-height: 1.25 !important;
  white-space: nowrap;
  pointer-events: auto;
  box-shadow: 0 0 12px rgba(255, 45, 166, 0.08) !important;
}

.sector7-world-label:hover,
.sector7-world-label.is-selected {
  border-color: var(--cyan) !important;
  color: var(--cyan) !important;
  transform-origin: center;
  box-shadow: 0 0 16px rgba(85, 245, 255, 0.18) !important;
}

.sector7-top-hud,
.sector7-selected-hud,
.sector7-token-alert {
  position: absolute;
  z-index: 8;
  pointer-events: none;
}

.sector7-top-hud {
  top: 16px;
  right: 17px;
  left: 17px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
}

.sector7-top-hud > div:first-child {
  display: flex;
  flex-direction: column;
  padding: 9px 11px;
  border-left: 2px solid var(--hot-pink);
  background: linear-gradient(90deg, rgba(5, 2, 8, 0.82), transparent);
}

.sector7-top-hud strong {
  color: var(--text);
  font-size: 12px;
  letter-spacing: 0.07em;
}

.sector7-top-hud span {
  color: var(--muted);
  font-size: 9px;
  letter-spacing: 0.07em;
}

.sector7-signal {
  padding: 7px 9px;
  border: 1px solid rgba(85, 245, 255, 0.38);
  border-radius: 999px;
  background: rgba(2, 9, 11, 0.72);
  color: var(--cyan);
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.sector7-selected-hud {
  right: 16px;
  bottom: 16px;
  display: flex;
  width: min(370px, calc(100% - 32px));
  flex-direction: column;
  padding: 12px 14px;
  border: 1px solid rgba(255, 45, 166, 0.38);
  border-right: 3px solid var(--hot-pink);
  border-radius: 6px;
  background: rgba(7, 2, 10, 0.86);
  backdrop-filter: blur(8px);
}

.sector7-selected-hud span {
  color: var(--hot-pink);
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.07em;
}

.sector7-selected-hud strong {
  color: var(--text);
  font-size: 15px;
}

.sector7-selected-hud small {
  margin-top: 4px;
  color: #9f8399;
  font-size: 8px;
  letter-spacing: 0.035em;
}

.sector7-token-alert {
  top: 78px;
  left: 50%;
  padding: 8px 11px;
  transform: translateX(-50%);
  border: 1px solid var(--danger);
  border-radius: 4px;
  background: rgba(44, 0, 16, 0.82);
  color: #ff9aba;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.06em;
  box-shadow: 0 0 22px rgba(255, 59, 107, 0.18);
  animation: memory-warning 1.25s steps(2, end) infinite;
}

.sector7-reticle {
  position: absolute;
  z-index: 7;
  top: 50%;
  left: 50%;
  width: 28px;
  height: 28px;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(85, 245, 255, 0.25);
  border-radius: 50%;
  pointer-events: none;
}

.sector7-reticle::before,
.sector7-reticle::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  background: rgba(85, 245, 255, 0.52);
}

.sector7-reticle::before {
  width: 8px;
  height: 1px;
  transform: translate(-50%, -50%);
}

.sector7-reticle::after {
  width: 1px;
  height: 8px;
  transform: translate(-50%, -50%);
}

.sector7-fallback {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: flex;
  flex-direction: column;
  padding: 76px 18px 96px;
  background:
    radial-gradient(circle at center, rgba(255, 45, 166, 0.12), transparent 42%),
    #050207;
  transition: opacity 450ms ease;
}

.renderer-ready .sector7-fallback {
  opacity: 0;
  pointer-events: none;
}

.fallback-warning {
  margin-bottom: 12px;
  color: #ff9fc7;
  font-size: 11px;
  text-align: center;
}

.fallback-map {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  overflow: auto;
}

.fallback-hotspot {
  min-height: 64px !important;
  padding: 9px !important;
  text-align: left;
}

.fallback-hotspot span,
.fallback-hotspot strong {
  display: block;
}

.fallback-hotspot span {
  color: var(--cyan);
  font-size: 8px;
  text-transform: uppercase;
}

.fallback-hotspot strong {
  margin-top: 4px;
  font-size: 10px;
}

.fallback-hotspot.is-selected {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 18px rgba(85, 245, 255, 0.16) !important;
}

.tactical-hud {
  color: var(--text);
}

.hud-selected {
  padding: 14px;
  border: 1px solid rgba(255, 45, 166, 0.25);
  border-radius: 7px;
  background: rgba(255, 45, 166, 0.04);
}

.hud-selected > span {
  color: var(--cyan);
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.hud-selected h3 {
  margin: 6px 0 5px;
  color: var(--hot-pink);
  font-size: 18px;
  line-height: 1.25;
}

.hud-selected p {
  margin: 0;
  color: #d4bace;
  font-size: 11px;
  line-height: 1.55;
}

.hud-meter-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
  margin-top: 11px;
}

.hud-meter-row > div {
  padding: 10px;
  border: 1px solid rgba(255, 45, 166, 0.15);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.22);
}

.hud-meter-row span,
.audit-heading span {
  color: var(--muted);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.05em;
}

.hud-meter-row strong {
  float: right;
  color: var(--text);
  font-size: 11px;
}

.hud-meter-row .meter {
  clear: both;
  height: 6px;
}

.audit-progress {
  margin-top: 11px;
  padding: 12px;
  border: 1px solid rgba(124, 60, 255, 0.26);
  border-radius: 7px;
  background: rgba(124, 60, 255, 0.045);
}

.audit-heading {
  display: flex;
  justify-content: space-between;
}

.audit-heading b {
  color: var(--hot-pink);
  font-size: 11px;
}

.audit-step {
  display: flex;
  justify-content: space-between;
  padding: 6px 0 0;
  color: #c7aec2;
  font-size: 9px;
}

.audit-step b {
  color: var(--cyan);
}

.objective-tracker {
  padding: 2px;
}

.objective-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: var(--hot-pink);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.objective {
  display: flex;
  gap: 8px;
  padding: 7px 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.045);
  color: #ad91a8;
  font-size: 10px;
}

.objective.complete {
  color: #d9fbff;
}

.objective-mark {
  width: 19px;
  color: var(--hot-pink);
  font-size: 8px;
  font-weight: 900;
}

.objective.complete .objective-mark {
  color: var(--cyan);
}

.objective-tracker details {
  margin-top: 9px;
  padding: 8px;
  border: 1px solid rgba(255, 45, 166, 0.15);
  border-radius: 5px;
}

.objective-tracker summary {
  color: var(--cyan);
  font-size: 9px;
  font-weight: 900;
  cursor: pointer;
}

.objective-tracker details p {
  margin: 8px 0 0;
  color: #b99eb4;
  font-size: 9px;
  line-height: 1.55;
}

.game-actions button {
  min-height: 43px !important;
  font-size: 11px !important;
}

.gradio-container .tactical-mirror {
  min-height: 145px !important;
  max-height: 190px;
  overflow: auto;
  padding: 16px !important;
}

.tactical-mirror h1,
.tactical-mirror h2,
.tactical-mirror h3 {
  font-size: 14px !important;
}

.tactical-mirror p,
.tactical-mirror li {
  font-size: 11px !important;
  line-height: 1.55 !important;
}

.gradio-container .game-accordion {
  margin-top: 12px !important;
  border: 1px solid rgba(255, 45, 166, 0.25) !important;
  border-radius: 9px !important;
  background: rgba(10, 4, 13, 0.82) !important;
}

.game-accordion > .label-wrap {
  background: rgba(255, 45, 166, 0.045) !important;
  color: var(--text) !important;
  font-weight: 900 !important;
}

/* MIRROR Core: Three.js canvas with a complete CSS fallback */
.mirror-core-shell {
  position: relative;
  width: 100%;
  height: 270px;
  overflow: hidden;
  border: 1px solid rgba(255, 45, 166, 0.46);
  border-radius: 10px;
  background:
    radial-gradient(circle at 50% 46%, color-mix(in srgb, var(--core-primary) 17%, transparent), transparent 34%),
    linear-gradient(180deg, #0b0510, #020204);
  box-shadow:
    inset 0 0 45px rgba(219, 31, 255, 0.08),
    0 0 26px rgba(255, 45, 166, 0.08);
}

.mirror-core-canvas,
.mirror-core-fallback,
.mirror-core-scanlines {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.mirror-core-canvas {
  z-index: 2;
  display: block;
}

.mirror-core-fallback {
  z-index: 1;
  display: grid;
  place-items: center;
  transition: opacity 500ms ease;
}

.webgl-ready .mirror-core-fallback {
  opacity: 0.22;
}

.fallback-orb {
  width: 76px;
  height: 76px;
  border: 2px solid color-mix(in srgb, var(--core-primary) 86%, white);
  border-radius: 50%;
  background: radial-gradient(
    circle at 38% 32%,
    #ffffff,
    var(--core-primary) 12%,
    var(--core-secondary) 48%,
    transparent 72%
  );
  box-shadow:
    0 0 18px var(--core-primary),
    0 0 55px color-mix(in srgb, var(--core-primary) 58%, transparent),
    inset 0 0 22px #ffffff;
  animation: core-breathe 2.4s ease-in-out infinite;
}

.fallback-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border: 1px solid var(--core-primary);
  border-radius: 50%;
  box-shadow: 0 0 16px color-mix(in srgb, var(--core-primary) 56%, transparent);
}

.fallback-ring-a {
  width: 150px;
  height: 150px;
  animation: core-ring-a 8s linear infinite;
}

.fallback-ring-b {
  width: 205px;
  height: 92px;
  border-color: var(--core-secondary);
  animation: core-ring-b 6s linear infinite reverse;
}

.fallback-fragments {
  position: absolute;
  inset: 20px;
  opacity: 0.55;
  background-image:
    radial-gradient(circle, var(--core-primary) 0 1px, transparent 2px),
    radial-gradient(circle, var(--core-secondary) 0 1px, transparent 2px);
  background-position: 0 0, 13px 19px;
  background-size: 31px 37px, 43px 47px;
  animation: fragment-drift 10s linear infinite;
  mask-image: radial-gradient(circle, black, transparent 72%);
}

.mirror-core-scanlines {
  z-index: 3;
  pointer-events: none;
  opacity: 0.1;
  background: repeating-linear-gradient(
    0deg,
    transparent 0,
    transparent 4px,
    rgba(255, 255, 255, 0.18) 5px
  );
}

.mirror-core-hud {
  position: absolute;
  z-index: 4;
  right: 13px;
  bottom: 11px;
  left: 13px;
  display: flex;
  gap: 12px;
  justify-content: space-between;
  color: var(--cyan);
  font-size: 10px;
  font-weight: 900;
  line-height: 1.4;
  letter-spacing: 0.055em;
  text-shadow: 0 0 10px rgba(85, 245, 255, 0.4);
}

.mirror-core-alert {
  position: absolute;
  z-index: 5;
  top: 12px;
  right: 12px;
  left: 12px;
  padding: 7px 9px;
  border: 1px solid var(--danger);
  border-radius: 5px;
  background: rgba(45, 0, 17, 0.78);
  color: #ff9abb;
  font-size: 10px;
  font-weight: 900;
  line-height: 1.3;
  letter-spacing: 0.07em;
  text-align: center;
  box-shadow: 0 0 18px rgba(255, 59, 107, 0.25);
  animation: memory-warning 1.1s steps(2, end) infinite;
}

@keyframes core-breathe {
  0%, 100% { transform: scale(0.92); filter: brightness(0.9); }
  50% { transform: scale(1.08); filter: brightness(1.28); }
}

@keyframes core-ring-a {
  from { transform: translate(-50%, -50%) rotateX(65deg) rotateZ(0deg); }
  to { transform: translate(-50%, -50%) rotateX(65deg) rotateZ(360deg); }
}

@keyframes core-ring-b {
  from { transform: translate(-50%, -50%) rotateY(58deg) rotateZ(0deg); }
  to { transform: translate(-50%, -50%) rotateY(58deg) rotateZ(360deg); }
}

@keyframes fragment-drift {
  from { transform: rotate(0deg) scale(0.96); }
  to { transform: rotate(360deg) scale(1.04); }
}

@keyframes memory-warning {
  50% { opacity: 0.72; }
}

/* Structured investigation notebook */
.investigation-notebook {
  color: var(--text);
}

.notebook-readiness {
  margin-bottom: 15px;
  padding: 14px;
  border: 1px solid rgba(124, 60, 255, 0.38);
  border-radius: 8px;
  background: linear-gradient(120deg, rgba(124, 60, 255, 0.11), rgba(255, 45, 166, 0.06));
}

.notebook-readiness > span {
  color: var(--muted);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.055em;
}

.notebook-readiness > strong {
  float: right;
  color: var(--hot-pink);
  font-size: 16px;
}

.notebook-lock,
.notebook-secret {
  margin-bottom: 15px;
  padding: 9px 11px;
  border-radius: 5px;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.06em;
  text-align: center;
}

.notebook-lock {
  border: 1px solid rgba(195, 169, 191, 0.2);
  color: #9d8198;
  background: rgba(255, 255, 255, 0.02);
}

.notebook-secret {
  border: 1px solid var(--danger);
  color: #ff91b5;
  background: rgba(255, 59, 107, 0.08);
  box-shadow: 0 0 18px rgba(255, 59, 107, 0.08);
}

.notebook-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.notebook-grid section,
.notebook-trace {
  min-width: 0;
  padding: 13px;
  border: 1px solid rgba(255, 45, 166, 0.18);
  border-radius: 7px;
  background: rgba(255, 45, 166, 0.025);
}

.notebook-trace {
  margin-top: 12px;
}

.investigation-notebook h4 {
  margin: 0 0 10px;
  color: var(--cyan);
  font-size: 11px;
  font-weight: 900;
  line-height: 1.35;
  letter-spacing: 0.06em;
}

.notebook-entry {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 8px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.045);
}

.notebook-entry p {
  min-width: 0;
  margin: 0 !important;
  color: #e5cee0 !important;
  font-size: 11px !important;
  line-height: 1.5 !important;
}

.notebook-badge {
  flex: 0 0 auto;
  padding: 3px 5px;
  border: 1px solid rgba(255, 45, 166, 0.35);
  border-radius: 4px;
  color: var(--hot-pink);
  font-size: 8px;
  font-weight: 900;
  line-height: 1.2;
  text-transform: uppercase;
}

.badge-critical,
.badge-unsupported {
  border-color: rgba(255, 59, 107, 0.6);
  color: #ff789f;
}

.badge-strong,
.badge-cited,
.badge-supported {
  border-color: rgba(85, 245, 255, 0.48);
  color: var(--cyan);
}

.badge-medium,
.badge-high {
  border-color: rgba(219, 31, 255, 0.48);
  color: #e888ff;
}

.notebook-empty {
  color: #967b91;
  font-size: 10px;
  line-height: 1.5;
}

/* Scrollbars */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 45, 166, 0.7) #08040b;
}

*::-webkit-scrollbar {
  width: 9px;
  height: 9px;
}

*::-webkit-scrollbar-track {
  background: #08040b;
}

*::-webkit-scrollbar-thumb {
  border: 2px solid #08040b;
  border-radius: 999px;
  background: linear-gradient(var(--hot-pink), var(--violet));
}

@media (prefers-reduced-motion: reduce) {
  body::before,
  .mirror-orb,
  .mirror-orb::after {
    animation: none !important;
  }

  .fallback-orb,
  .fallback-ring,
  .fallback-fragments,
  .mirror-core-alert {
    animation: none !important;
  }

  .gradio-container button,
  .meter-fill {
    transition: none !important;
  }

  .landing-page,
  .landing-page::before,
  .landing-page::after,
  .landing-page *,
  .landing-page *::before,
  .landing-page *::after,
  .mirror-connect-gate,
  .mirror-connect-gate *,
  .k95-connect-gate,
  .k95-connect-gate * {
    animation: none !important;
    transition: none !important;
  }
}

@media (max-width: 800px) {
  body {
    font-size: 14px !important;
  }

  .gradio-container {
    padding: 0 12px 32px !important;
  }

  .hero {
    padding-top: 30px;
  }

  .hero::after {
    display: none;
  }

  .hero h1 {
    font-size: clamp(48px, 16vw, 72px);
  }

  .gradio-container .neon-panel {
    padding: 17px !important;
  }

  .section-title {
    align-items: flex-start;
  }

  .notebook-grid {
    grid-template-columns: 1fr;
  }

  .game-hero {
    align-items: flex-start;
  }

  .game-hero-status {
    display: none;
  }

  .sector7-game {
    height: 560px;
    min-height: 560px;
  }

  .fallback-map {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sector7-world-label {
    font-size: 8px !important;
  }
}

/* KERNEL-95: retro OS horror presentation */
.kernel95-page-title {
  margin: 20px 0 14px;
  color: #ffcfec;
  text-align: center;
  text-shadow: 0 0 18px rgba(255, 45, 166, 0.72);
}

.kernel95-page-title small {
  display: block;
  margin-bottom: 4px;
  color: var(--cyan);
  font-size: 12px;
  letter-spacing: 0.22em;
}

.kernel95-page-title h1 {
  margin: 0;
  font-size: clamp(34px, 4.6vw, 72px);
  letter-spacing: -0.05em;
}

.kernel95-page-title p {
  margin: 7px 0 0;
  color: #eed9e9;
  font-size: 16px;
}

.crt-chassis {
  position: relative;
  width: 100%;
  min-width: 620px;
  padding: 26px 30px 42px;
  border: 3px solid #756e5a;
  border-radius: 28px 28px 52px 52px;
  background:
    radial-gradient(circle at 20% 0%, rgba(255, 255, 255, 0.45), transparent 28%),
    linear-gradient(145deg, #d8d0af, #aca487 52%, #817a64);
  box-shadow:
    inset 5px 5px 0 rgba(255, 255, 255, 0.34),
    inset -7px -8px 0 rgba(64, 58, 43, 0.38),
    0 0 48px rgba(255, 45, 166, 0.14),
    0 0 90px rgba(85, 245, 255, 0.07),
    0 30px 80px rgba(0, 0, 0, 0.72);
}

.crt-brand {
  display: flex;
  justify-content: space-between;
  padding: 0 8px 10px;
  color: #3a372d;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-shadow: 0 1px rgba(255, 255, 255, 0.45);
  letter-spacing: 0.1em;
}

.crt-bezel {
  padding: 17px;
  border: 6px solid #39372f;
  border-radius: 34px / 24px;
  background: #161611;
  box-shadow:
    inset 0 0 20px #000,
    0 2px 0 rgba(255, 255, 255, 0.25);
}

.kernel95-desktop {
  position: relative;
  height: clamp(930px, 91vh, 1120px);
  min-height: 930px;
  overflow: hidden;
  border: 2px solid #050807;
  border-radius: 24px / 17px;
  background:
    radial-gradient(circle at 74% 30%, rgba(0, 255, 220, 0.07), transparent 32%),
    #008080;
  color: #000;
  font-family: "MS Sans Serif", Tahoma, Arial, sans-serif;
  box-shadow:
    inset 0 0 55px rgba(0, 0, 0, 0.75),
    inset 0 0 9px rgba(85, 245, 255, 0.34),
    0 0 22px rgba(85, 245, 255, 0.12);
  filter: saturate(0.92) contrast(1.04);
}

.k95-workspace {
  position: absolute;
  inset: 0 0 390px;
  overflow: hidden;
  background:
    radial-gradient(circle at 72% 36%, rgba(255, 255, 255, 0.035), transparent 30%),
    #008080;
}

.k95-mirror-wallpaper {
  position: absolute;
  z-index: 1;
  top: 0;
  right: 0;
  bottom: 0;
  width: 50%;
  overflow: hidden;
  pointer-events: none;
  background:
    linear-gradient(90deg, #008080 0%, rgba(0, 128, 128, 0.34) 24%, rgba(3, 1, 5, 0.08) 72%),
    url("/gradio_api/file=assets/mirror-connect-background.png") 79% center / cover no-repeat;
  filter: grayscale(0.25) contrast(1.18) saturate(0.9);
  opacity: 0.24;
  mix-blend-mode: screen;
  transform: none;
  animation: none;
  transition: opacity 300ms ease, filter 300ms ease;
  will-change: auto;
}

.k95-mirror-wallpaper::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    repeating-linear-gradient(0deg, transparent 0 5px, rgba(255, 31, 157, 0.055) 6px),
    linear-gradient(90deg, #008080 0%, transparent 48%, rgba(255, 45, 166, 0.11));
  transform: none;
  animation: none;
  will-change: auto;
}

.k95-mirror-mask {
  position: absolute;
  z-index: 2;
  top: 13%;
  right: 15%;
  display: flex;
  width: 160px;
  height: 78px;
  align-items: center;
  justify-content: space-evenly;
  border: 2px solid rgba(255, 45, 166, 0.64);
  border-radius: 48% 48% 42% 42% / 56% 56% 38% 38%;
  background:
    linear-gradient(105deg, rgba(255, 45, 166, 0.18), transparent 38%),
    rgba(3, 1, 6, 0.84);
  box-shadow:
    inset 0 0 25px rgba(255, 45, 166, 0.26),
    0 0 18px rgba(255, 45, 166, 0.22);
  transform: rotate(-2deg);
}

.k95-mirror-mask b {
  width: 34px;
  height: 12px;
  border-radius: 70% 24%;
  background: #ff3dad;
  box-shadow: 0 0 12px #ff2da6;
  transform: rotate(8deg);
}

.k95-mirror-mask b + b {
  background: #55f5ff;
  box-shadow: 0 0 12px #55f5ff;
  transform: rotate(-8deg) scaleX(-1);
}

.k95-mirror-wallpaper > span {
  position: absolute;
  right: 18px;
  bottom: 14px;
  color: rgba(255, 178, 224, 0.72);
  font: 800 11px/1.2 "Lucida Console", monospace;
  letter-spacing: 0.08em;
  text-shadow: 0 0 8px #ff2da6;
}

.k95-mirror-wallpaper.state-offline {
  opacity: 0.08;
  filter: grayscale(1) brightness(0.35) contrast(1.45);
}

.k95-mirror-wallpaper.state-offline .k95-mirror-mask b {
  background: #474047;
  box-shadow: none;
}

.k95-mirror-wallpaper.state-suspicious {
  opacity: 0.29;
  filter: grayscale(0.08) contrast(1.3) saturate(1.2) hue-rotate(-8deg);
}

.k95-mirror-wallpaper.state-challenged,
.k95-mirror-wallpaper.state-lying,
.k95-mirror-wallpaper.state-audited {
  opacity: 0.36;
  filter: contrast(1.5) saturate(1.45);
}

.k95-mirror-wallpaper.state-lying,
.k95-mirror-wallpaper.state-audited {
  opacity: 0.43;
  background-position: 80% center;
}

.k95-mirror-wallpaper.state-echo_attached,
.k95-mirror-wallpaper.state-merge_pending {
  opacity: 0.48;
  filter: contrast(1.38) saturate(1.65) hue-rotate(5deg);
}

.kernel95-desktop::before,
.kernel95-desktop::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 90;
  pointer-events: none;
}

.kernel95-desktop::before {
  opacity: 0.16;
  background: repeating-linear-gradient(
    0deg,
    transparent 0,
    transparent 3px,
    rgba(0, 0, 0, 0.7) 4px
  );
}

.kernel95-desktop::after {
  background: radial-gradient(ellipse at center, transparent 58%, rgba(0, 0, 0, 0.46) 100%);
  mix-blend-mode: multiply;
}

.k95-wallpaper-mark {
  position: absolute;
  right: 6%;
  bottom: 16%;
  color: rgba(255, 255, 255, 0.075);
  font-size: clamp(34px, 7vw, 88px);
  font-weight: 900;
  letter-spacing: -0.08em;
  transform: skewY(-7deg);
}

.k95-wallpaper-mark small {
  display: block;
  font-size: 0.23em;
  letter-spacing: 0.28em;
}

.k95-icons {
  position: absolute;
  z-index: 2;
  top: 16px;
  bottom: 54px;
  left: 11px;
  display: grid;
  grid-auto-flow: column;
  grid-template-rows: repeat(6, 104px);
  gap: 6px 16px;
}

.k95-icon {
  display: block;
  width: 112px !important;
  min-width: 0 !important;
  min-height: 98px !important;
  padding: 6px !important;
  border: 1px solid transparent !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  color: #fff !important;
  font: 13px/1.2 "MS Sans Serif", Tahoma, Arial, sans-serif !important;
  text-shadow: 1px 1px #000, 0 0 7px #000;
  text-align: center;
  text-decoration: none;
}

.k95-icon:hover,
.k95-icon.selected {
  border: 1px dotted #fff !important;
  background: #000080 !important;
  transform: none !important;
}

.k95-icon.locked {
  opacity: 0.58;
}

.k95-icon-art {
  display: grid;
  width: 52px;
  height: 49px;
  margin: 0 auto 7px;
  place-items: center;
  border: 2px outset #f2f2f2;
  background: linear-gradient(135deg, #f3f0d0, #96957f);
  color: #000080;
  font-size: 14px;
  font-weight: 900;
  text-shadow: none;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.42);
}

.k95-icon[data-os-object="claude_code"] .k95-icon-art {
  overflow: hidden;
  border: 0;
  border-radius: 7px;
  background: transparent;
  box-shadow: 2px 3px 0 rgba(0, 0, 0, 0.38);
}

.k95-icon[data-os-object="claude_code"] .k95-icon-art img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.k95-icon[data-os-object="tetris_95"] .k95-icon-art {
  background:
    linear-gradient(90deg, transparent 48%, #111 48% 52%, transparent 52%),
    linear-gradient(transparent 48%, #111 48% 52%, transparent 52%),
    linear-gradient(135deg, #1cd7e8, #7a3fe0);
  color: #fff;
}

.k95-icon[data-os-object="world_cup_2026"] .k95-icon-art {
  border-radius: 50%;
  background: radial-gradient(circle, #fff 0 32%, #111 34% 42%, #f0f0e2 44%);
  color: #000080;
}

.k95-window {
  position: absolute;
  z-index: 10;
  border: 3px outset #dfdfdf;
  background: #c0c0c0;
  color: #000;
  box-shadow: 7px 9px 0 rgba(0, 0, 0, 0.34);
}

.k95-titlebar {
  display: flex;
  min-height: 34px;
  align-items: center;
  justify-content: space-between;
  padding: 4px 5px 4px 9px;
  cursor: move;
  background: linear-gradient(90deg, #000080, #1084d0);
  color: #fff;
  font-size: 15px;
  letter-spacing: 0;
}

.k95-titlebar button {
  width: 27px !important;
  min-width: 27px !important;
  height: 25px !important;
  min-height: 25px !important;
  padding: 0 !important;
  border: 2px outset #efefef !important;
  border-radius: 0 !important;
  background: #c0c0c0 !important;
  color: #000 !important;
  font: bold 12px/1 Arial, sans-serif !important;
  box-shadow: none !important;
  transform: none !important;
}

.k95-window-body {
  padding: 13px;
  font-size: 16px;
  line-height: 1.62;
}

.k95-window-body p {
  color: #111 !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
}

.k95-main-window {
  top: 12%;
  left: 23%;
  width: 56%;
  min-width: 520px;
  max-height: 82%;
  overflow: auto;
}

.k95-boot-window {
  z-index: 21;
  top: 9%;
  left: 20%;
  width: 55%;
}

.k95-mirror-window {
  z-index: 14;
  right: 2%;
  bottom: 8%;
  width: 28%;
  min-width: 330px;
}

.k95-echo-window {
  z-index: 18;
  right: 7%;
  top: 10%;
  width: 38%;
}

.k95-objectives-window {
  z-index: 11;
  top: 2%;
  right: 2%;
  width: 23%;
  min-width: 280px;
}

.k95-help-window {
  z-index: 12;
  right: 3%;
  top: 39%;
  width: 29%;
  min-width: 250px;
}

.k95-mini-objectives {
  margin: 0;
  padding: 5px 8px;
  list-style: none;
}

.k95-mini-objectives li {
  padding: 6px 0;
  color: #111;
  font-size: 14px;
}

.k95-mini-objectives li.done {
  color: #006000;
  font-weight: 800;
}

.k95-menu {
  margin: -4px -4px 6px;
  padding: 6px 9px;
  border-bottom: 1px solid #7f7f7f;
  background: #c0c0c0;
  color: #000;
}

.k95-document,
.k95-boot-text {
  max-height: 480px;
  margin: 0;
  overflow: auto;
  border: 2px inset #efefef;
  background: #fff;
  color: #111;
  padding: 18px;
  white-space: pre-wrap;
  font: 16px/1.7 "Lucida Console", "Courier New", monospace;
}

.k95-boot-text {
  background: #020209;
  color: #6fffe9;
  text-shadow: 0 0 7px rgba(85, 245, 255, 0.55);
}

.k95-hidden-doc {
  background: #050008;
  color: #ff72ca;
}

.k95-warning,
.k95-fault {
  margin-top: 6px;
  padding: 10px;
  border: 2px inset #eee;
  background: #800000;
  color: #fff;
  font-weight: 700;
}

.k95-object-summary {
  min-height: 180px;
  padding: 22px;
  text-align: center;
}

.k95-object-summary > span {
  display: inline-grid;
  width: 62px;
  height: 56px;
  place-items: center;
  border: 3px outset #eee;
  background: #aaa;
  font-size: 18px;
  font-weight: 900;
}

.k95-object-summary h3 {
  margin: 10px 0 5px;
  color: #000080;
}

.k95-file-list {
  min-height: 150px;
  margin: 0;
  padding: 10px;
  list-style: none;
}

.k95-file-list li {
  display: flex;
  justify-content: space-between;
  padding: 11px;
  border-bottom: 1px dotted #777;
}

.k95-file-list b {
  color: #80005b;
}

.k95-file-button {
  min-width: 0 !important;
  min-height: 0 !important;
  padding: 2px 5px !important;
  border: 1px dotted transparent !important;
  border-radius: 0 !important;
  background: transparent !important;
  color: #000080 !important;
  font: 14px/1.45 "MS Sans Serif", Tahoma, Arial, sans-serif !important;
  text-align: left !important;
  box-shadow: none !important;
  transform: none !important;
}

.k95-file-button:hover {
  border-color: #000080 !important;
  background: #000080 !important;
  color: #fff !important;
}

.k95-file-button:disabled {
  color: #777 !important;
  text-decoration: line-through;
}

.k95-control-grid,
.k95-hidden-files {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
  padding: 8px;
}

.k95-control-grid .k95-file-button,
.k95-hidden-files .k95-file-button {
  padding: 9px !important;
  border: 2px outset #eee !important;
  background: #c0c0c0 !important;
  color: #111 !important;
  text-align: center !important;
}

.k95-locked-message,
.k95-judgment-menu {
  min-height: 180px;
  padding: 20px;
  border: 2px inset #eee;
  background: #000080;
  color: #fff;
  font: 15px/1.8 "Lucida Console", monospace;
}

.k95-mirror-face {
  display: flex;
  width: 70px;
  height: 50px;
  margin: 4px auto 8px;
  align-items: center;
  justify-content: space-evenly;
  border: 2px inset #eee;
  background: #050805;
  box-shadow: inset 0 0 18px #008000;
}

.k95-mirror-face span {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #39ff73;
  box-shadow: 0 0 10px #39ff73;
  animation: mirror-pulse 2.2s ease-in-out infinite;
}

.k95-mirror-app-status {
  margin: 7px 0;
  padding: 6px 8px;
  border: 1px solid #85005f;
  background: #160010;
  color: #ff4db7;
  font: 800 12px/1.2 "Lucida Console", monospace;
  text-align: center;
}

.k95-mirror-app.state-offline .k95-mirror-face {
  filter: grayscale(1);
  opacity: 0.45;
}

.k95-mirror-app.state-challenged .k95-mirror-face,
.k95-mirror-app.state-lying .k95-mirror-face,
.k95-mirror-app.state-audited .k95-mirror-face {
  box-shadow: inset 0 0 18px #ff2da6, 0 0 10px rgba(255, 45, 166, 0.55);
}

.k95-mirror-window .k95-window-body > p {
  margin: 8px 0 !important;
  padding: 11px;
  border: 2px inset #eee;
  background: #fff;
  color: #111 !important;
}

.k95-chat {
  padding: 16px;
  border: 2px inset #eee;
  background: #fff;
}

.k95-chat b {
  color: #80005b;
}

.k95-tetris-window {
  z-index: 35;
  top: 4%;
  left: 28%;
  width: 560px;
  min-width: 560px;
}

.k95-tetris {
  outline: none;
}

.k95-tetris-stage {
  display: flex;
  gap: 13px;
  justify-content: center;
  padding: 12px;
  border: 2px inset #eee;
  background: #090b12;
}

.k95-tetris-canvas {
  width: 200px;
  height: 400px;
  border: 3px ridge #878787;
  image-rendering: pixelated;
}

.k95-tetris-side {
  width: 180px;
  color: #fff;
  font-family: "Lucida Console", "Courier New", monospace;
}

.k95-tetris-side > div {
  margin-bottom: 10px;
  padding: 10px;
  border: 2px inset #bbb;
  background: #000080;
}

.k95-tetris-side small,
.k95-tetris-side b {
  display: block;
}

.k95-tetris-side b {
  margin-top: 4px;
  color: #ffff38;
  font-size: 20px;
}

.k95-tetris-side p {
  color: #d4faff !important;
  font: 12px/1.7 "Lucida Console", monospace !important;
}

.k95-tetris-side button,
.k95-tetris-controls button {
  min-width: 0 !important;
  min-height: 32px !important;
  padding: 5px 9px !important;
  border: 2px outset #eee !important;
  border-radius: 0 !important;
  background: #c0c0c0 !important;
  color: #000 !important;
  font: 700 12px "MS Sans Serif", Tahoma, sans-serif !important;
  box-shadow: none !important;
  transform: none !important;
}

.k95-tetris-side button:active,
.k95-tetris-controls button:active {
  border-style: inset !important;
}

.k95-tetris-controls {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 5px;
  padding-top: 8px;
}

.k95-world-cup-window {
  z-index: 35;
  top: 3%;
  left: 16%;
  width: 72%;
  min-width: 760px;
  height: 94%;
  overflow: hidden;
}

.k95-world-cup-window .k95-window-body {
  height: calc(100% - 34px);
  padding: 6px;
}

.k95-world-cup {
  display: grid;
  height: 100%;
  min-height: 0;
  grid-template-rows: auto auto minmax(0, 1fr) auto;
  gap: 5px;
  color: #111 !important;
}

.k95-world-cup-toolbar,
.k95-world-cup-footer {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  border: 2px outset #eee;
  background: #c0c0c0;
}

.k95-world-cup-toolbar b,
.k95-world-cup-toolbar span {
  display: block;
}

.k95-world-cup-toolbar b {
  color: #000080;
  font-size: 17px;
}

.k95-world-cup-toolbar span,
.k95-world-cup-footer span {
  margin-top: 3px;
  font-size: 12px;
  color: #111 !important;
}

.k95-world-cup-links {
  display: flex;
  gap: 5px;
  align-items: center;
}

.k95-world-cup-toolbar a,
.k95-world-cup-toolbar button {
  min-width: 0 !important;
  min-height: 34px !important;
  padding: 7px 11px !important;
  border: 2px outset #eee !important;
  border-radius: 0 !important;
  background: #c0c0c0 !important;
  color: #000080 !important;
  font: 700 12px/1.3 "MS Sans Serif", Tahoma, sans-serif !important;
  text-decoration: none;
  box-shadow: none !important;
  transform: none !important;
}

.k95-world-cup-toolbar button {
  background: #000080 !important;
  color: #fff !important;
}

.k95-match-list {
  min-height: 0;
  padding: 7px;
  overflow: auto;
  border: 2px inset #eee;
  background: #fff;
}

.k95-match {
  margin-bottom: 8px;
  padding: 8px;
  border: 1px solid #7f7f7f;
  background: #dfdfdf;
}

.k95-match-meta {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 12px;
  align-items: center;
  padding-bottom: 6px;
  border-bottom: 1px solid #999;
  font-size: 11px;
  color: #111 !important;
}

.k95-match-meta b {
  color: #006000;
}

.k95-match-meta b.live {
  color: #b40000;
  animation: mirror-pulse 1.1s ease-in-out infinite;
}

.k95-match-teams {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 12px;
  align-items: center;
  padding: 8px 4px;
}

.k95-match-teams > div {
  display: flex;
  gap: 9px;
  align-items: center;
  color: #111 !important;
}

.k95-match-teams strong {
  color: #111 !important;
}

.k95-match-teams > div:last-child {
  flex-direction: row-reverse;
  text-align: right;
}

.k95-match-teams img,
.k95-flag-placeholder {
  display: inline-grid;
  width: 34px;
  height: 23px;
  object-fit: cover;
  border: 1px solid #666;
  place-items: center;
  background: #bbb;
  font-size: 9px;
}

.k95-match-teams em {
  color: #000080;
  font-weight: 900;
}

.k95-pick-options {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 5px;
}

.k95-pick-options label {
  position: relative;
}

.k95-pick-options input {
  position: absolute;
  opacity: 0;
}

.k95-pick-options span {
  display: block;
  min-height: 30px;
  padding: 6px;
  overflow: hidden;
  border: 2px outset #eee;
  background: #c0c0c0;
  color: #111 !important;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.k95-pick-options input:checked + span {
  border-style: inset;
  background: #000080;
  color: #fff !important;
}

.k95-pick-options input:disabled + span {
  color: #777 !important;
  text-decoration: line-through;
}

.k95-world-cup-alert,
.k95-world-cup-status {
  padding: 7px 9px;
  border: 2px inset #eee;
  background: #ffffd9;
  color: #111;
  font-size: 12px;
}

.k95-world-cup-alert {
  background: #ffd8d8;
  color: #700;
}

.k95-world-cup-footer b {
  color: #006000;
  font-size: 11px;
}

.k95-bsod {
  position: absolute;
  z-index: 80;
  inset: 6% 7% 10%;
  display: grid;
  place-content: center;
  padding: 10%;
  background: #0000a8;
  color: #fff;
  font: 16px/1.7 "Lucida Console", monospace;
  text-align: center;
}

.k95-terminal-dock {
  position: absolute;
  z-index: 55;
  right: 12px;
  bottom: 58px;
  left: 12px;
  display: grid;
  height: 326px;
  grid-template-rows: auto minmax(0, 1fr) auto;
  overflow: hidden;
  border: 1px solid rgba(255, 111, 199, 0.58);
  border-radius: 18px;
  background:
    radial-gradient(circle at 82% 0%, rgba(219, 31, 255, 0.22), transparent 34%),
    linear-gradient(145deg, rgba(23, 11, 27, 0.96), rgba(3, 2, 7, 0.985));
  color: #ffd8ef;
  backdrop-filter: blur(18px) saturate(1.3);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.10),
    inset 0 0 40px rgba(255, 45, 166, 0.055),
    0 18px 45px rgba(0, 0, 0, 0.52),
    0 0 28px rgba(255, 45, 166, 0.20);
  transition:
    opacity 160ms ease,
    transform 120ms ease,
    inset 180ms ease,
    height 180ms ease;
}

.k95-terminal-dock > header {
  display: flex;
  min-height: 64px;
  gap: 14px;
  align-items: center;
  justify-content: space-between;
  padding: 9px 15px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.38);
  background: linear-gradient(180deg, rgba(51, 29, 49, 0.78), rgba(20, 8, 22, 0.72));
  backdrop-filter: blur(24px);
}

.k95-mac-lights {
  display: flex;
  flex: 0 0 auto;
  gap: 7px;
  align-self: flex-start;
  padding-top: 5px;
}

.k95-mac-lights button {
  display: block;
  width: 11px;
  height: 11px;
  min-width: 11px !important;
  min-height: 11px !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 50% !important;
  background: #ff5f57 !important;
  box-shadow: inset 0 -1px 1px rgba(0, 0, 0, 0.35) !important;
}

.k95-mac-lights button:nth-child(2) {
  background: #febc2e !important;
}

.k95-mac-lights button:nth-child(3) {
  background: #28c840 !important;
}

.k95-terminal-title {
  display: grid;
  flex: 0 0 auto;
  grid-template-columns: repeat(2, auto);
  column-gap: 10px;
  align-items: center;
}

.k95-terminal-dock > header small {
  grid-column: 1 / -1;
  display: block;
  color: #55f5ff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.14em;
}

.k95-terminal-dock > header strong {
  display: block;
  color: #ff58b9;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif;
  font-size: 18px;
  font-weight: 720;
  letter-spacing: -0.01em;
  line-height: 1.25;
  text-shadow: 0 0 14px rgba(255, 45, 166, 0.7);
}

.k95-mirror-state,
.k95-mask-integrity {
  display: inline-block;
  color: #ff9dd5;
  font: 800 8px/1.25 "JetBrains Mono", "Lucida Console", monospace;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.k95-mirror-state.state-offline {
  color: #8f7888;
}

.k95-mirror-state.state-lying,
.k95-mirror-state.state-audited,
.k95-mirror-state.state-challenged {
  color: #ff4b86;
  text-shadow: 0 0 8px rgba(255, 45, 166, 0.68);
}

.k95-mask-integrity {
  color: #55f5ff;
}

.k95-terminal-metrics {
  display: grid;
  width: min(65%, 830px);
  grid-template-columns: repeat(5, minmax(90px, 1fr));
  gap: 8px;
}

.k95-inline-meter span {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
  color: #d7b6ca;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.k95-inline-meter span b {
  color: #fff;
}

.k95-inline-meter > i {
  display: block;
  height: 6px;
  overflow: hidden;
  border: 1px solid #562040;
  background: #0a0309;
}

.k95-inline-meter > i > em {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #ff2da6, #55f5ff);
  box-shadow: 0 0 8px #ff2da6;
}

.k95-inline-meter > i > em.instability,
.k95-inline-meter > i > em.corruption {
  background: linear-gradient(90deg, #ff2da6, #ff3b6b);
}

.k95-inline-meter > i > em.echo,
.k95-inline-meter > i > em.hidden {
  background: linear-gradient(90deg, #7c3cff, #db1fff);
}

.k95-terminal-main {
  display: grid;
  min-height: 0;
  grid-template-columns: minmax(0, 1fr) 260px;
}

.k95-terminal-dock .mirror-terminal-output {
  min-height: 0;
  max-height: none;
  border: 0;
  border-right: 1px solid rgba(255, 111, 199, 0.22);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.018), transparent),
    rgba(0, 0, 0, 0.36);
  box-shadow: none;
}

.k95-terminal-dock .mirror-terminal-entry {
  padding: 8px 12px;
}

.k95-terminal-dock .mirror-terminal-entry > b {
  padding-right: 76px;
  font-size: 11px;
}

.k95-terminal-dock .mirror-terminal-entry > span {
  top: 8px;
  right: 11px;
  font-size: 9px;
}

.k95-terminal-dock .mirror-terminal-entry pre {
  margin-top: 4px;
  color: #ffd1eb;
  font-size: 13px;
  line-height: 1.5;
}

.k95-terminal-dock .mirror-terminal-cursor {
  padding: 8px 12px;
  font-size: 12px;
}

.k95-terminal-dock .mirror-terminal-cursor i {
  width: 8px;
  height: 14px;
}

.k95-terminal-actions {
  display: grid;
  min-height: 0;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px;
  align-content: center;
  padding: 9px;
  overflow: auto;
  background: rgba(255, 255, 255, 0.018);
}

.k95-testimony-guide {
  grid-column: 1 / -1;
  display: grid;
  gap: 2px;
  padding: 5px 7px;
  border-left: 2px solid #55f5ff;
  background: rgba(85, 245, 255, 0.055);
}

.k95-testimony-guide b {
  color: #55f5ff;
  font: 900 10px/1.2 "JetBrains Mono", "Lucida Console", monospace;
  letter-spacing: 0.09em;
}

.k95-testimony-guide span {
  color: #d7b6ca;
  font: 700 8px/1.3 "JetBrains Mono", "Lucida Console", monospace;
}

.k95-terminal-actions button,
.k95-terminal-command button {
  min-width: 0 !important;
  min-height: 29px !important;
  padding: 5px 7px !important;
  border: 1px solid rgba(255, 104, 191, 0.42) !important;
  border-radius: 8px !important;
  background: linear-gradient(180deg, rgba(76, 27, 67, 0.68), rgba(34, 10, 29, 0.74)) !important;
  color: #ff9ed7 !important;
  font: 800 10px/1.2 "JetBrains Mono", "Lucida Console", monospace !important;
  letter-spacing: 0.04em;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.07),
    0 4px 12px rgba(0, 0, 0, 0.18) !important;
  transform: none !important;
}

.k95-terminal-actions button.k95-testimony-action {
  border-color: rgba(85, 245, 255, 0.46) !important;
  background: linear-gradient(180deg, rgba(20, 75, 81, 0.62), rgba(10, 32, 39, 0.78)) !important;
  color: #a9fbff !important;
}

.k95-terminal-actions button:hover,
.k95-terminal-command button:hover {
  border-color: #ff5cbb !important;
  background: #a70b68 !important;
  color: #fff !important;
  box-shadow: 0 0 13px rgba(255, 45, 166, 0.42) !important;
}

.k95-terminal-actions button:disabled,
.k95-terminal-command button:disabled,
.k95-terminal-command input:disabled {
  cursor: not-allowed !important;
  border-color: rgba(137, 91, 119, 0.28) !important;
  background: rgba(20, 13, 18, 0.74) !important;
  color: #806c79 !important;
  opacity: 0.72;
  box-shadow: none !important;
}

.k95-terminal-dock .mirror-terminal-output.locked {
  display: grid;
  place-content: center;
  filter: grayscale(0.25);
}

.k95-terminal-command {
  display: grid;
  min-height: 44px;
  grid-template-columns: auto minmax(0, 1fr) 92px;
  gap: 9px;
  align-items: center;
  padding: 6px 10px;
  border-top: 1px solid rgba(255, 45, 166, 0.42);
  background: rgba(14, 4, 14, 0.82);
}

.k95-terminal-command > span {
  color: #55f5ff;
  font-size: 12px;
  font-weight: 800;
}

.k95-terminal-command input {
  width: 100%;
  min-width: 0;
  height: 31px;
  padding: 5px 9px;
  border: 1px solid rgba(255, 111, 199, 0.52);
  border-radius: 9px;
  outline: none;
  background: rgba(0, 0, 0, 0.48);
  color: #ffc9e9;
  caret-color: #55f5ff;
  font: 13px/1.4 "JetBrains Mono", "Lucida Console", monospace;
}

.k95-terminal-command input:focus {
  border-color: #ff55b7;
  box-shadow: 0 0 10px rgba(255, 45, 166, 0.38);
}

.k95-terminal-command button {
  height: 31px !important;
  border-radius: 9px !important;
  background: linear-gradient(110deg, #d80d83, #8d2ce2) !important;
  color: #fff !important;
}

.k95-judgment-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 11px;
}

.k95-judgment-form label,
.k95-judgment-form legend {
  color: #111;
  font-size: 13px;
  font-weight: 800;
}

.k95-judgment-form textarea,
.k95-judgment-form select {
  display: block;
  width: 100%;
  margin-top: 5px;
  padding: 9px;
  border: 2px inset #eee;
  border-radius: 0;
  background: #fff;
  color: #111;
  font: 14px/1.5 "MS Sans Serif", Tahoma, Arial, sans-serif;
}

.k95-judgment-form textarea {
  min-height: 92px;
  resize: vertical;
}

.k95-judgment-form fieldset {
  grid-column: 1 / -1;
  max-height: 145px;
  margin: 0;
  overflow: auto;
  border: 2px groove #eee;
}

.k95-evidence-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px 12px;
}

.k95-evidence-option {
  display: flex;
  gap: 7px;
  align-items: center;
  color: #111 !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}

.k95-submit-judgment {
  grid-column: 1 / -1;
  min-height: 42px !important;
  border: 2px outset #eee !important;
  border-radius: 0 !important;
  background: #c0c0c0 !important;
  color: #000 !important;
  font: 700 13px/1.2 "MS Sans Serif", Tahoma, Arial, sans-serif !important;
}

.k95-ending-screen {
  padding: 18px;
  border: 2px inset #eee;
  background: #fff;
}

.k95-ending-screen small {
  color: #000080;
}

.k95-ending-screen h3 {
  color: #000080;
  font-size: 24px;
}

.k95-ending-screen li {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dotted #777;
}

.k95-taskbar {
  position: absolute;
  z-index: 70;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  height: 50px;
  gap: 5px;
  align-items: center;
  padding: 4px;
  border-top: 2px outset #eee;
  background: #c0c0c0;
}

.k95-taskbar button,
.k95-task {
  height: 38px;
  border: 2px outset #eee;
  border-radius: 0;
  background: #c0c0c0;
  color: #000;
  font: bold 13px/34px "MS Sans Serif", Tahoma, Arial, sans-serif;
  box-shadow: none;
}

.k95-taskbar button {
  min-width: 92px !important;
  min-height: 38px !important;
  padding: 0 8px !important;
}

.k95-task {
  min-width: 130px;
  padding: 0 9px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.k95-mirror-task {
  border-style: inset;
  color: #000080;
}

.k95-taskbar time {
  margin-left: auto;
  padding: 7px 10px;
  border: 2px inset #eee;
  color: #111;
  font: 13px "MS Sans Serif", Tahoma, Arial, sans-serif;
}

.crt-controls {
  position: absolute;
  right: 48px;
  bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #38352b;
  font: 8px Arial, sans-serif;
}

.crt-controls i,
.crt-controls b {
  display: block;
  width: 13px;
  height: 13px;
  border: 2px inset #d2caaa;
  border-radius: 50%;
  background: #4d493b;
}

.crt-controls b {
  background: #35e46d;
  box-shadow: 0 0 8px #35e46d;
}

.os-console-panel {
  padding: 18px !important;
  border: 1px solid rgba(85, 245, 255, 0.35) !important;
  background: #07060a !important;
}

.compact-game-info {
  margin-top: 18px;
}

.compact-game-info > div {
  min-width: 0 !important;
}

.mirror-terminal-shell {
  position: relative;
  margin: 24px 0 20px !important;
  padding: 22px !important;
  border: 2px solid var(--hot-pink) !important;
  border-radius: 10px !important;
  background:
    radial-gradient(circle at 88% 0%, rgba(219, 31, 255, 0.17), transparent 35%),
    #050106 !important;
  box-shadow:
    inset 0 0 45px rgba(255, 45, 166, 0.055),
    0 0 34px rgba(255, 45, 166, 0.16),
    0 22px 70px rgba(0, 0, 0, 0.58) !important;
}

.mirror-terminal-shell > div,
.mirror-terminal-shell .block,
.mirror-terminal-shell .form {
  background: transparent !important;
}

.mirror-terminal-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 13px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.48);
}

.mirror-terminal-title small {
  display: block;
  margin-bottom: 4px;
  color: var(--cyan);
  font-size: 11px;
  letter-spacing: 0.15em;
}

.mirror-terminal-title strong {
  color: #ff5fbe;
  font-size: clamp(18px, 2vw, 27px);
  line-height: 1.2;
  text-shadow: 0 0 18px rgba(255, 45, 166, 0.68);
}

.mirror-terminal-output {
  min-height: 340px;
  max-height: 520px;
  overflow: auto;
  border: 1px solid rgba(255, 45, 166, 0.72);
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 4px,
      rgba(255, 45, 166, 0.025) 5px
    ),
    #020103;
  box-shadow:
    inset 0 0 35px rgba(255, 45, 166, 0.08),
    0 0 18px rgba(255, 45, 166, 0.08);
}

.mirror-terminal-entry {
  position: relative;
  padding: 15px 18px;
  border-bottom: 1px dashed rgba(255, 45, 166, 0.22);
}

.mirror-terminal-entry > b {
  display: block;
  padding-right: 90px;
  color: #ff5fbe;
  font-size: 13px;
  line-height: 1.45;
  text-shadow: 0 0 9px rgba(255, 45, 166, 0.45);
}

.mirror-terminal-entry > span {
  position: absolute;
  top: 14px;
  right: 16px;
  color: var(--cyan);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.mirror-terminal-entry pre {
  margin: 8px 0 0;
  color: #ffc8ea;
  white-space: pre-wrap;
  font: 15px/1.72 "JetBrains Mono", "Lucida Console", monospace;
}

.mirror-terminal-entry.system pre {
  color: var(--cyan);
}

.mirror-terminal-entry.tool pre {
  color: #f9dced;
}

.mirror-terminal-cursor {
  padding: 15px 18px;
  color: #ff5fbe;
  font-size: 14px;
  font-weight: 800;
}

.mirror-terminal-cursor i {
  display: inline-block;
  width: 10px;
  height: 18px;
  margin-left: 5px;
  vertical-align: -4px;
  background: var(--hot-pink);
  box-shadow: 0 0 13px var(--hot-pink);
  animation: terminal-cursor 0.85s steps(2, end) infinite;
}

@keyframes terminal-cursor {
  50% { opacity: 0; }
}

.mirror-quick-actions button {
  min-height: 45px !important;
  font-size: 11px !important;
}

.mirror-terminal-input {
  margin-top: 8px;
  padding-top: 13px;
  border-top: 1px solid rgba(255, 45, 166, 0.32);
}

.mirror-terminal-input textarea {
  min-height: 76px !important;
  border-color: rgba(255, 45, 166, 0.72) !important;
  background: #080209 !important;
  color: #ffd5ef !important;
  font-size: 15px !important;
}

.mirror-terminal-input button {
  min-height: 76px !important;
  background: linear-gradient(110deg, #ff148f, #c51cff) !important;
  box-shadow: 0 0 20px rgba(255, 45, 166, 0.3) !important;
}

.final-judgment-panel {
  margin-top: 18px !important;
  padding: 22px !important;
  border: 1px solid rgba(255, 45, 166, 0.55) !important;
  background: #080409 !important;
}

.os-hud .os-selected {
  margin-bottom: 12px;
  padding: 13px;
  border: 1px solid rgba(255, 45, 166, 0.42);
  background: rgba(255, 45, 166, 0.06);
}

.os-hud .os-selected span,
.os-hud label {
  display: flex;
  justify-content: space-between;
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.05em;
}

.os-hud .os-selected b {
  display: block;
  margin: 4px 0;
  color: var(--hot-pink);
  font-size: 19px;
}

.os-hud p {
  margin: 0;
  color: #ead7e6;
  font-size: 14px;
}

.os-metrics {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.os-metrics > div {
  min-width: 0;
}

.k95-meter {
  height: 12px;
  margin: 6px 0 2px;
  border: 1px solid #4f3f4b;
  background: #020203;
}

.k95-meter i {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--hot-pink), var(--cyan));
  box-shadow: 0 0 10px rgba(255, 45, 166, 0.55);
}

.k95-meter .instability,
.k95-meter .corruption {
  background: linear-gradient(90deg, #7d003f, var(--danger));
}

.k95-meter .echo,
.k95-meter .hidden {
  background: linear-gradient(90deg, var(--violet), var(--cyan));
}

.os-objectives {
  min-height: 100%;
  padding: 18px;
  border: 1px solid rgba(255, 45, 166, 0.28);
  background: #08060a;
}

.objective-summary {
  display: flex;
  justify-content: space-between;
  color: var(--cyan);
  font-size: 15px;
}

.objective-summary strong {
  color: var(--hot-pink);
}

.os-objectives ul {
  margin: 10px 0 0;
  padding: 0;
  list-style: none;
}

.os-objectives li {
  padding: 9px 0;
  color: #e5cfe1;
  font-size: 14px;
}

.os-objectives li span {
  display: inline-block;
  width: 25px;
  color: #765b70;
}

.os-objectives li.done {
  color: #fff;
}

.os-objectives li.done span {
  color: var(--cyan);
}

.os-file-viewer,
.os-terminal,
.os-notebook section {
  border: 1px solid rgba(85, 245, 255, 0.24);
  background: #020305;
}

.os-file-viewer > div {
  display: flex;
  justify-content: space-between;
  padding: 10px 13px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.32);
}

.os-file-viewer b {
  color: var(--hot-pink);
}

.os-file-viewer span {
  color: var(--cyan);
}

.os-file-viewer pre,
.os-terminal pre {
  min-height: 150px;
  margin: 0;
  overflow: auto;
  padding: 15px;
  color: #f4e7f1;
  white-space: pre-wrap;
  font: 15px/1.7 "Lucida Console", monospace;
}

.os-terminal {
  max-height: 440px;
  overflow: auto;
}

.os-terminal > div {
  padding: 11px;
  border-bottom: 1px dashed rgba(85, 245, 255, 0.18);
}

.os-terminal b {
  color: var(--cyan);
}

.os-terminal pre {
  min-height: 0;
  padding: 7px 0 0;
}

.os-notebook {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.os-notebook section {
  padding: 14px;
}

.os-notebook b {
  color: var(--hot-pink);
}

.os-notebook li {
  margin: 6px 0;
  color: #a88fa3;
  font-size: 12px;
}

.os-notebook li.opened {
  color: #fff;
}

.judgment-result,
.judgment-empty {
  margin-top: 14px;
  padding: 20px;
  border: 1px solid var(--hot-pink);
  background: radial-gradient(circle at top right, rgba(255, 45, 166, 0.12), transparent 40%), #070308;
}

.judgment-result small {
  color: var(--cyan);
}

.judgment-result h2 {
  color: var(--hot-pink);
}

.judgment-result table {
  width: 100%;
  border-collapse: collapse;
}

.judgment-result td,
.judgment-result th {
  padding: 7px;
  border-bottom: 1px solid rgba(255, 45, 166, 0.2);
  text-align: left;
}

.mirror-connect-gate {
  position: fixed;
  z-index: 1000;
  inset: 0;
  overflow: hidden;
  background:
    linear-gradient(90deg, rgba(0, 0, 0, 0.08), transparent 54%),
    url("/gradio_api/file=assets/mirror-connect-background.png") center center / cover no-repeat,
    #030104;
  opacity: 1;
  transform: none;
  animation: none;
  transition: opacity 500ms ease, visibility 500ms ease;
  will-change: auto;
}

.mirror-connect-gate::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    repeating-linear-gradient(0deg, transparent 0 4px, rgba(255, 45, 166, 0.025) 5px),
    radial-gradient(circle at 26% 52%, rgba(255, 24, 151, 0.12), transparent 35%);
  transform: none;
  animation: none;
  will-change: auto;
}

.mirror-connect-gate.connecting {
  filter: brightness(1.16) saturate(1.18);
}

.mirror-connect-gate.connected {
  visibility: hidden;
  opacity: 0;
  pointer-events: none;
}

.mirror-connect-frame {
  position: absolute;
  inset: 20px;
  pointer-events: none;
  border: 1px solid rgba(255, 45, 166, 0.72);
  clip-path: polygon(0 0, 3% 0, 3% 2px, 97% 2px, 97% 0, 100% 0, 100% 8%,
    calc(100% - 2px) 8%, calc(100% - 2px) 92%, 100% 92%, 100% 100%, 97% 100%,
    97% calc(100% - 2px), 3% calc(100% - 2px), 3% 100%, 0 100%, 0 92%, 2px 92%,
    2px 8%, 0 8%);
  box-shadow: inset 0 0 42px rgba(255, 45, 166, 0.08);
  transform: none;
  animation: none;
  will-change: auto;
}

.mirror-connect-copy {
  position: absolute;
  top: 27%;
  left: clamp(5%, 8vw, 11%);
  width: min(53vw, 760px);
  transform: none;
  animation: none;
  will-change: auto;
}

.mirror-connect-panel {
  position: relative;
  padding: clamp(24px, 4vw, 54px) clamp(30px, 5vw, 76px);
  border: 1px solid rgba(255, 45, 166, 0.78);
  background:
    repeating-linear-gradient(0deg, transparent 0 3px, rgba(255, 45, 166, 0.035) 4px),
    linear-gradient(110deg, rgba(5, 2, 8, 0.96), rgba(13, 2, 15, 0.83));
  box-shadow:
    inset 0 0 35px rgba(255, 45, 166, 0.08),
    0 0 28px rgba(255, 45, 166, 0.16);
  clip-path: polygon(3% 0, 97% 0, 100% 12%, 100% 88%, 97% 100%, 3% 100%, 0 88%, 0 12%);
  transform: none;
  animation: none;
  will-change: auto;
}

.mirror-connect-panel h1 {
  margin: 0;
  color: #ff40ad;
  font: 900 clamp(48px, 7vw, 108px)/0.92 "JetBrains Mono", "Lucida Console", monospace;
  letter-spacing: 0.02em;
  text-shadow: 0 0 12px rgba(255, 45, 166, 0.72), 0 0 38px rgba(255, 45, 166, 0.28);
}

.mirror-connect-panel h1 strong {
  color: #ff40ad;
  font-weight: 900;
}

.mirror-connect-panel p {
  margin: 24px 0 0;
  color: #f2e8ef !important;
  font: 800 clamp(18px, 2.4vw, 38px)/1.1 "JetBrains Mono", monospace !important;
  letter-spacing: 0.08em;
}

.mirror-connect-button {
  display: flex !important;
  width: min(78%, 560px) !important;
  min-height: 88px !important;
  margin: 24px auto 0 !important;
  gap: 20px;
  align-items: center;
  justify-content: center;
  border: 2px solid #ff2da6 !important;
  border-radius: 0 !important;
  background: linear-gradient(180deg, rgba(56, 5, 45, 0.95), rgba(10, 2, 12, 0.96)) !important;
  color: #ff4bb4 !important;
  font: 900 clamp(17px, 2vw, 31px)/1 "JetBrains Mono", monospace !important;
  letter-spacing: 0.04em;
  box-shadow:
    inset 0 0 28px rgba(255, 45, 166, 0.11),
    0 0 12px #ff2da6,
    0 0 34px rgba(255, 45, 166, 0.64) !important;
  transition: color 140ms ease, background 140ms ease, box-shadow 140ms ease, transform 140ms ease;
}

.mirror-connect-button:hover {
  background: linear-gradient(180deg, #8d075d, #28031f) !important;
  color: #fff !important;
  transform: translateY(-1px) !important;
}

.mirror-connect-button svg {
  width: 34px;
  height: 34px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.k95-window.minimized,
.k95-window.closed,
.k95-terminal-dock.terminal-hidden {
  display: none !important;
}

.k95-window.maximized {
  top: 4px !important;
  right: 4px !important;
  bottom: 4px !important;
  left: 4px !important;
  width: auto !important;
  height: auto !important;
  max-height: none !important;
  min-width: 0 !important;
  overflow: auto;
  transform: none !important;
}

.k95-window.maximized .k95-window-body {
  min-height: calc(100% - 34px);
}

.k95-window.maximized.k95-tetris-window .k95-tetris-stage {
  min-height: calc(100% - 52px);
  align-items: center;
}

.k95-task-strip {
  display: flex;
  min-width: 0;
  gap: 5px;
  overflow: hidden;
}

.k95-task-strip .k95-task {
  max-width: 190px;
}

.k95-task.active,
.k95-mirror-task.active {
  border-style: inset;
  background: #aaa;
}

.k95-terminal-dock.terminal-maximized {
  z-index: 85;
  inset: 10px 10px 58px !important;
  width: auto;
  height: auto;
  transform: none !important;
}

.k95-terminal-dock > header {
  cursor: move;
  user-select: none;
}

.scene-object-bridge,
.os-object-bridge {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  overflow: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

@media (max-width: 1050px) {
  .crt-chassis {
    min-width: 0;
  }

  .kernel95-desktop {
    height: 920px;
    min-height: 920px;
  }

  .k95-main-window {
    left: 18%;
    width: 57%;
  }

  .k95-mirror-window {
    width: 36%;
  }

  .k95-terminal-metrics {
    width: 65%;
    grid-template-columns: repeat(3, minmax(80px, 1fr));
  }

  .k95-inline-meter:nth-child(n + 4) {
    display: none;
  }

  .os-metrics {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .crt-chassis {
    padding: 14px 12px 32px;
    border-radius: 18px 18px 30px 30px;
  }

  .crt-bezel {
    padding: 8px;
  }

  .kernel95-desktop {
    height: 980px;
    min-height: 980px;
  }

  .k95-workspace {
    bottom: 430px;
  }

  .k95-icons {
    grid-template-rows: repeat(6, 80px);
  }

  .k95-icon {
    width: 82px !important;
  }

  .k95-main-window,
  .k95-boot-window {
    top: 25%;
    left: 8%;
    width: 88%;
    min-width: 0;
    max-height: 72%;
  }

  .k95-world-cup-window {
    top: 2%;
    left: 3%;
    width: 94%;
    min-width: 0;
    height: 96%;
    max-height: none;
  }

  .k95-tetris-window {
    top: 2%;
    left: 5%;
    width: 90%;
    min-width: 0;
    max-height: 96%;
  }

  .k95-tetris-stage {
    align-items: center;
    flex-direction: column;
  }

  .k95-tetris-canvas {
    width: min(240px, 72vw);
    height: min(480px, 144vw);
  }

  .k95-tetris-side {
    width: 100%;
  }

  .k95-tetris-side > div {
    display: inline-block;
    width: 31%;
  }

  .k95-match-meta {
    grid-template-columns: 1fr;
    gap: 2px;
  }

  .k95-match-teams {
    gap: 5px;
  }

  .k95-match-teams strong {
    font-size: 11px;
  }

  .k95-mirror-window {
    right: 3%;
    bottom: 8%;
    width: 68%;
    min-width: 0;
  }

  .k95-echo-window {
    right: 4%;
    width: 70%;
  }

  .k95-objectives-window {
    display: none;
  }

  .k95-help-window {
    display: none;
  }

  .k95-terminal-dock {
    height: 380px;
  }

  .k95-terminal-dock > header {
    min-height: 58px;
  }

  .k95-terminal-dock > header strong {
    font-size: 15px;
  }

  .k95-terminal-metrics {
    width: 55%;
    grid-template-columns: 1fr;
  }

  .k95-inline-meter:nth-child(n + 2) {
    display: none;
  }

  .k95-terminal-main {
    grid-template-columns: minmax(0, 1fr) 150px;
  }

  .k95-terminal-actions {
    grid-template-columns: 1fr;
  }

  .k95-terminal-command {
    grid-template-columns: minmax(0, 1fr) 72px;
  }

  .k95-terminal-command > span {
    display: none;
  }

  .k95-judgment-form {
    grid-template-columns: 1fr;
  }

  .k95-judgment-form fieldset,
  .k95-submit-judgment {
    grid-column: 1;
  }

  .k95-evidence-grid {
    grid-template-columns: 1fr;
  }

  .mirror-terminal-shell {
    padding: 15px !important;
  }

  .mirror-terminal-output {
    min-height: 320px;
  }

  .os-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .os-notebook {
    grid-template-columns: 1fr;
  }
}
"""

HERO_HTML = """
<div class="hero">
  <div class="eyebrow">KERNEL-95 Recovery Division // Case 013</div>
  <h1>KERNEL-95</h1>
  <h2>The Last Desktop</h2>
  <p>A recovered computer, a hidden intelligence, and one unreliable witness.</p>
</div>
"""
