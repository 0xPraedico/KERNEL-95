"""Live World Cup 2026 fixtures for the local prediction mock."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

LIVE_GAMES_URL = "https://worldcup26.ir/get/games"
LIVE_TEAMS_URL = "https://worldcup26.ir/get/teams"
REGULATION_RESULTS_URL = (
    "https://raw.githubusercontent.com/openfootball/worldcup.json/"
    "master/2026/worldcup.json"
)
FIFA_FIXTURES_URL = (
    "https://www.fifa.com/en/tournaments/mens/worldcup/"
    "canadamexicousa2026/scores-fixtures"
)

_CACHE_SECONDS = 120
_cache: dict[str, Any] = {"expires": 0.0, "matches": [], "error": ""}
_cache_lock = threading.Lock()

_STADIUM_ZONES = {
    "1": "America/Mexico_City",
    "2": "America/Mexico_City",
    "3": "America/Monterrey",
    "4": "America/Chicago",
    "5": "America/Chicago",
    "6": "America/Chicago",
    "7": "America/New_York",
    "8": "America/New_York",
    "9": "America/New_York",
    "10": "America/New_York",
    "11": "America/New_York",
    "12": "America/Toronto",
    "13": "America/Vancouver",
    "14": "America/Los_Angeles",
    "15": "America/Los_Angeles",
    "16": "America/Los_Angeles",
}


def _read_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "KERNEL-95/1.0"},
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.load(response)


def _kickoff_utc(raw: str, stadium_id: str) -> datetime:
    local = datetime.strptime(raw, "%m/%d/%Y %H:%M")
    zone = ZoneInfo(_STADIUM_ZONES.get(stadium_id, "UTC"))
    return local.replace(tzinfo=zone).astimezone(timezone.utc)


def _regulation_results() -> dict[tuple[str, str, str], tuple[int, int]]:
    try:
        rows = _read_json(REGULATION_RESULTS_URL).get("matches", [])
    except Exception:
        return {}
    results: dict[tuple[str, str, str], tuple[int, int]] = {}
    for row in rows:
        score = row.get("score", {})
        full_time = score.get("ft") if isinstance(score, dict) else None
        if not isinstance(full_time, list) or len(full_time) != 2:
            continue
        key = (
            str(row.get("date", "")),
            str(row.get("team1", "")),
            str(row.get("team2", "")),
        )
        results[key] = (int(full_time[0]), int(full_time[1]))
    return results


def _normalize_matches() -> list[dict[str, Any]]:
    games = _read_json(LIVE_GAMES_URL).get("games", [])
    teams = _read_json(LIVE_TEAMS_URL).get("teams", [])
    flags = {str(team.get("id")): str(team.get("flag", "")) for team in teams}
    regulation = _regulation_results()
    normalized = []
    for game in games:
        kickoff = _kickoff_utc(
            str(game.get("local_date", "")),
            str(game.get("stadium_id", "")),
        )
        home = str(game.get("home_team_name_en", "") or f"TBD {game.get('home_team_id', '')}")
        away = str(game.get("away_team_name_en", "") or f"TBD {game.get('away_team_id', '')}")
        finished = str(game.get("finished", "")).upper() == "TRUE"
        result = regulation.get((kickoff.date().isoformat(), home, away))
        if result is None and finished:
            try:
                result = (int(game.get("home_score", 0)), int(game.get("away_score", 0)))
            except (TypeError, ValueError):
                result = None
        normalized.append(
            {
                "id": str(game.get("id", "")),
                "home": home,
                "away": away,
                "home_flag": flags.get(str(game.get("home_team_id", "")), ""),
                "away_flag": flags.get(str(game.get("away_team_id", "")), ""),
                "kickoff": kickoff,
                "group": str(game.get("group", "") or game.get("type", "")).upper(),
                "finished": finished,
                "live": not finished
                and str(game.get("time_elapsed", "")).lower()
                not in {"", "notstarted", "not started", "scheduled"},
                "result": result,
            }
        )
    return sorted(normalized, key=lambda item: item["kickoff"])


def get_matches(force: bool = False) -> tuple[list[dict[str, Any]], str]:
    """Return cached live fixtures and a non-fatal source error."""
    now = time.monotonic()
    with _cache_lock:
        if not force and _cache["matches"] and now < _cache["expires"]:
            return list(_cache["matches"]), str(_cache["error"])
        try:
            matches = _normalize_matches()
            _cache.update(
                expires=now + _CACHE_SECONDS,
                matches=matches,
                error="",
            )
        except Exception as exc:
            _cache["expires"] = now + 30
            _cache["error"] = f"Live fixture refresh failed: {exc}"
        return list(_cache["matches"]), str(_cache["error"])


def prediction_is_open(match: dict[str, Any], now: datetime | None = None) -> bool:
    current = now or datetime.now(timezone.utc)
    return not match["finished"] and current < match["kickoff"]
