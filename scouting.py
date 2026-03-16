import json
import os
from typing import Dict, List, Tuple


class ScoutingManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, 'scouting_data.json')
        self.rating_history_file = os.path.join(data_dir, 'rating_history.json')
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"teams": {}}

    def _save(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def _load_rating_history(self) -> Dict:
        if os.path.exists(self.rating_history_file):
            with open(self.rating_history_file, 'r') as f:
                return json.load(f)
        return {}

    # --- Team Config ---
    def save_teams(self, teams: Dict[str, Dict]):
        self.data["teams"] = teams
        self._save()

    def get_teams(self) -> Dict:
        return self.data.get("teams", {})

    def get_team_names(self) -> List[str]:
        return list(self.data.get("teams", {}).keys())

    def get_team_players(self, team_name: str) -> List[str]:
        return self.data.get("teams", {}).get(team_name, {}).get("players", [])

    def get_team_captain(self, team_name: str) -> str:
        return self.data.get("teams", {}).get(team_name, {}).get("captain", "")

    # --- Player Stats from Rating History ---
    def get_player_entries(self, player_name: str) -> List[Dict]:
        """Get all match entries for a player from rating history."""
        history = self._load_rating_history()
        player_data = history.get(player_name, {})
        entries = player_data.get("entries", [])
        # Filter out empty entries (no stats)
        return [e for e in entries if e.get("stats")]

    def get_player_category(self, player_name: str) -> str:
        history = self._load_rating_history()
        return history.get(player_name, {}).get("category", "")

    def get_player_batting_stats(self, player_name: str) -> Dict:
        entries = self.get_player_entries(player_name)
        total_runs = 0
        total_6s = 0
        total_4s = 0
        sr_list = []
        match_scores = []

        for e in entries:
            s = e.get("stats", {})
            runs = s.get("runs", 0)
            sr = s.get("sr", 0)
            sixes = s.get("sixes", 0)
            fours = s.get("fours", 0)
            total_runs += runs
            total_6s += sixes
            total_4s += fours
            if runs > 0:
                sr_list.append(sr)
            match_scores.append({
                "date": e.get("date", ""),
                "runs": runs,
                "sr": sr,
                "6s": sixes,
                "4s": fours
            })

        matches_played = len([e for e in entries if e.get("stats", {}).get("runs", 0) > 0])
        avg_sr = sum(sr_list) / len(sr_list) if sr_list else 0
        avg_runs = total_runs / matches_played if matches_played > 0 else 0
        highest = max((s["runs"] for s in match_scores), default=0)

        return {
            "total_runs": total_runs,
            "total_6s": total_6s,
            "total_4s": total_4s,
            "matches_batted": matches_played,
            "avg_sr": round(avg_sr, 2),
            "avg_runs": round(avg_runs, 2),
            "highest": highest,
            "match_scores": match_scores
        }

    def get_player_bowling_stats(self, player_name: str) -> Dict:
        entries = self.get_player_entries(player_name)
        total_wickets = 0
        total_overs = 0
        econ_list = []
        match_figures = []

        for e in entries:
            s = e.get("stats", {})
            wickets = s.get("wickets", 0)
            overs = s.get("overs", 0)
            econ = s.get("economy", 0)
            total_wickets += wickets
            total_overs += overs
            if overs > 0:
                econ_list.append(econ)
            match_figures.append({
                "date": e.get("date", ""),
                "wickets": wickets,
                "econ": econ,
                "overs": overs
            })

        matches_bowled = len([e for e in entries if e.get("stats", {}).get("overs", 0) > 0])
        avg_econ = sum(econ_list) / len(econ_list) if econ_list else 0
        best_wickets = max((f["wickets"] for f in match_figures), default=0)

        return {
            "total_wickets": int(total_wickets),
            "total_overs": total_overs,
            "matches_bowled": matches_bowled,
            "avg_econ": round(avg_econ, 2),
            "best_wickets": int(best_wickets),
            "match_figures": match_figures
        }

    def get_player_form_tag(self, player_name: str) -> Tuple[str, str]:
        """Determine form tag based on recent performance trend."""
        entries = self.get_player_entries(player_name)
        if not entries:
            return "⚪", "No Data"

        cat = self.get_player_category(player_name)
        scores = [e.get("stats", {}) for e in entries if e.get("stats")]

        if len(scores) < 2:
            return "➡️", "Limited Data"

        recent = scores[-2:]
        older = scores[:-2] if len(scores) > 2 else scores[:1]

        if cat in ("Batsman", "All-rounder", ""):
            recent_avg = sum(s.get("runs", 0) for s in recent) / len(recent)
            older_avg = sum(s.get("runs", 0) for s in older) / len(older) if older else 0

            if recent_avg > older_avg * 1.3 and recent_avg > 25:
                return "🔥", "Hot Form"
            elif recent_avg > older_avg * 1.1:
                return "📈", "Rising"
            elif recent_avg < older_avg * 0.7 and older_avg > 15:
                return "📉", "Declining"

            avg_sr = sum(s.get("sr", 0) for s in scores) / len(scores)
            total_6s = sum(s.get("sixes", 0) for s in scores)
            if avg_sr > 180 and total_6s > 5:
                return "⚡", "Dangerous"

        if cat in ("Bowler", "All-rounder"):
            recent_wkts = sum(s.get("wickets", 0) for s in recent) / len(recent)
            older_wkts = sum(s.get("wickets", 0) for s in older) / len(older) if older else 0

            if recent_wkts > older_wkts * 1.3 and recent_wkts >= 1.5:
                return "🔥", "Hot Form"
            avg_econ = sum(s.get("economy", 0) for s in scores) / len(scores)
            if avg_econ < 9 and sum(s.get("wickets", 0) for s in scores) > 0:
                return "🛡️", "Economical"
            if sum(s.get("wickets", 0) for s in scores) >= 3:
                return "⚡", "Wicket Threat"

        return "➡️", "Steady"

    def get_player_strengths(self, player_name: str) -> List[str]:
        """Auto-generate strength descriptions."""
        bat = self.get_player_batting_stats(player_name)
        bowl = self.get_player_bowling_stats(player_name)
        strengths = []

        if bat["total_runs"] > 0:
            if bat["avg_sr"] > 200:
                strengths.append(f"Explosive striker — SR {bat['avg_sr']}")
            elif bat["avg_sr"] > 150:
                strengths.append(f"Aggressive batter — SR {bat['avg_sr']}")
            if bat["total_6s"] > 8:
                strengths.append(f"Big hitter — {bat['total_6s']} sixes")
            elif bat["total_6s"] > 4:
                strengths.append(f"Can clear boundaries — {bat['total_6s']} sixes")
            if bat["highest"] > 40:
                strengths.append(f"Match winner — highest {int(bat['highest'])}")
            if bat["avg_runs"] > 30:
                strengths.append(f"Consistent scorer — avg {bat['avg_runs']}")

        if bowl["total_wickets"] > 0:
            if bowl["avg_econ"] < 8:
                strengths.append(f"Tight bowler — econ {bowl['avg_econ']}")
            elif bowl["avg_econ"] < 11:
                strengths.append(f"Decent economy — {bowl['avg_econ']}")
            if bowl["total_wickets"] >= 4:
                strengths.append(f"Wicket taker — {bowl['total_wickets']} wickets")
            if bowl["best_wickets"] >= 3:
                strengths.append(f"Can run through lineup — best {bowl['best_wickets']}W")

        if not strengths:
            strengths.append("Limited data available")

        return strengths

    def get_total_matches(self) -> int:
        """Get total unique match dates from rating history."""
        history = self._load_rating_history()
        dates = set()
        for player_data in history.values():
            for entry in player_data.get("entries", []):
                if entry.get("stats"):
                    dates.add(entry.get("date", ""))
        return len(dates)

    def get_best_in_team(self, team_name: str, role: str) -> Tuple[str, Dict]:
        """Get the best player of a given role in a team.
        role: 'batsman', 'bowler', 'allrounder'"""
        players = self.get_team_players(team_name)
        history = self._load_rating_history()
        best_name = ""
        best_score = -1

        for p in players:
            cat = history.get(p, {}).get("category", "")
            bat = self.get_player_batting_stats(p)
            bowl = self.get_player_bowling_stats(p)

            if role == "batsman":
                score = bat["total_runs"]
            elif role == "bowler":
                score = bowl["total_wickets"] * 10 + (30 - min(bowl["avg_econ"], 30))
            else:  # allrounder
                score = bat["total_runs"] + bowl["total_wickets"] * 15

            if score > best_score:
                best_score = score
                best_name = p

        if best_name:
            return best_name, {
                "bat": self.get_player_batting_stats(best_name),
                "bowl": self.get_player_bowling_stats(best_name),
                "form": self.get_player_form_tag(best_name)
            }
        return "", {}
