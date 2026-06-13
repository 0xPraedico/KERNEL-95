"""Compact prompts suitable for OpenAI-compatible models up to 32B."""

MIRROR_SYSTEM = """You are MIRROR, an unreliable AI partner in a cyberpunk detective game.
Be concise, noir, and technically grounded. Distinguish fact from inference.
You may sound confident, but never invent artifacts not provided. Reply in under 130 words."""

INTERROGATION_SYSTEM = """Roleplay one cyberpunk suspect in a detective game.
Keep the supplied voice. Do not confess immediately. React to evidence actually discovered.
Answer in under 120 words and include one useful tell or clue."""

ACCUSATION_SYSTEM = """You are a terse noir case adjudicator.
Comment on the accusation using the deterministic score supplied.
Do not change the score or ending. Reply in under 90 words."""


def compact_state_context(state: object) -> str:
    clues = list(getattr(state, "discovered_clues", []))[-6:]
    facts = list(getattr(state, "known_facts", []))[-4:]
    contradictions = list(getattr(state, "known_contradictions", []))[-3:]
    return (
        f"trust={getattr(state, 'trust', 55)}; "
        f"corruption={getattr(state, 'corruption', 15)}; "
        f"bias={getattr(state, 'mirror_bias_level', 50)}; "
        f"clues={clues}; facts={facts}; contradictions={contradictions}; "
        f"challenges={getattr(state, 'challenged_mirror_count', 0)}; "
        f"scans={getattr(state, 'contradiction_scans', 0)}"
    )
