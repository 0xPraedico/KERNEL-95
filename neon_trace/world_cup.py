"""Live World Cup 2026 fixtures and Hugging Face leaderboard persistence."""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from huggingface_hub import HfApi, hf_hub_download

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
_leaderboard_lock = threading.Lock()
_local_leaderboard: dict[str, Any] = {"users": {}}

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
        headers={"Accept": "application/json", "User-Agent": "NEON-TRACE/1.0"},
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


def validate_predictions(
    predictions: dict[str, str],
    matches: list[dict[str, Any]],
) -> dict[str, str]:
    """Keep only valid choices for matches that have not kicked off."""
    allowed = {"home", "draw", "away"}
    by_id = {match["id"]: match for match in matches}
    return {
        match_id: choice
        for match_id, choice in predictions.items()
        if choice in allowed
        and match_id in by_id
        and prediction_is_open(by_id[match_id])
    }


def _repo_config() -> tuple[str, str | None]:
    repo = os.getenv("HF_LEADERBOARD_REPO", "").strip()
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
    if not repo:
        space_id = os.getenv("SPACE_ID", "")
        if "/" in space_id:
            repo = f"{space_id.split('/', 1)[0]}/neon-trace-world-cup-2026"
    return repo, token


def _read_remote_board(repo: str, token: str) -> dict[str, Any]:
    try:
        path = hf_hub_download(
            repo_id=repo,
            repo_type="dataset",
            filename="leaderboard.json",
            token=token,
            force_download=True,
        )
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {"users": {}}


def save_predictions(
    username: str,
    display_name: str,
    predictions: dict[str, str],
) -> tuple[bool, str]:
    """Merge one user's picks into a private HF dataset or local fallback."""
    record = {
        "display_name": display_name or username,
        "predictions": predictions,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    repo, token = _repo_config()
    with _leaderboard_lock:
        if not repo or not token:
            _local_leaderboard.setdefault("users", {})[username] = record
            return (
                False,
                "Picks saved for this session. Configure HF_LEADERBOARD_REPO and "
                "HF_TOKEN to publish the shared leaderboard.",
            )
        try:
            api = HfApi(token=token)
            api.create_repo(
                repo_id=repo,
                repo_type="dataset",
                private=True,
                exist_ok=True,
            )
            board = _read_remote_board(repo, token)
            board.setdefault("users", {})[username] = record
            payload = json.dumps(board, indent=2, sort_keys=True).encode("utf-8")
            api.upload_file(
                path_or_fileobj=payload,
                path_in_repo="leaderboard.json",
                repo_id=repo,
                repo_type="dataset",
                commit_message=f"Update predictions for {username}",
            )
            return True, f"Synced to the secret Hugging Face leaderboard as @{username}."
        except Exception as exc:
            _local_leaderboard.setdefault("users", {})[username] = record
            return False, f"HF sync failed; picks remain in this session: {exc}"


def leaderboard_rows(matches: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    """Calculate one point per correct regulation-time outcome."""
    repo, token = _repo_config()
    if repo and token:
        with _leaderboard_lock:
            board = _read_remote_board(repo, token)
        source = "PRIVATE HUGGING FACE DATASET"
    else:
        board = _local_leaderboard
        source = "LOCAL PREVIEW // HF DATASET NOT CONFIGURED"
    by_id = {match["id"]: match for match in matches}
    rows = []
    for username, record in board.get("users", {}).items():
        score = 0
        settled = 0
        picks = record.get("predictions", {})
        for match_id, choice in picks.items():
            match = by_id.get(match_id)
            if not match or not match["finished"] or not match["result"]:
                continue
            home_score, away_score = match["result"]
            outcome = "home" if home_score > away_score else "away" if away_score > home_score else "draw"
            settled += 1
            score += int(choice == outcome)
        rows.append(
            {
                "username": username,
                "display_name": record.get("display_name", username),
                "score": score,
                "settled": settled,
                "picks": len(picks),
            }
        )
    rows.sort(key=lambda row: (-row["score"], -row["settled"], row["username"].lower()))
    return rows, source


def user_predictions(username: str) -> dict[str, str]:
    """Restore a returning HF user's synchronized picks."""
    repo, token = _repo_config()
    if repo and token:
        with _leaderboard_lock:
            board = _read_remote_board(repo, token)
    else:
        board = _local_leaderboard
    record = board.get("users", {}).get(username, {})
    predictions = record.get("predictions", {})
    if not isinstance(predictions, dict):
        return {}
    return {
        str(match_id): str(choice)
        for match_id, choice in predictions.items()
        if choice in {"home", "draw", "away"}
    }


def next_refresh_time() -> datetime:
    return datetime.now(timezone.utc) + timedelta(seconds=_CACHE_SECONDS)
