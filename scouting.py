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

    def generate_strategy(self, my_team: str, opponent_team: str) -> Dict:
        """Generate winning strategy against opponent team."""
        my_players = self.get_team_players(my_team)
        opp_players = self.get_team_players(opponent_team)

        # Analyze opponent batsmen
        opp_batsmen = []
        for p in opp_players:
            bat = self.get_player_batting_stats(p)
            bowl = self.get_player_bowling_stats(p)
            form = self.get_player_form_tag(p)
            opp_batsmen.append({"name": p, "bat": bat, "bowl": bowl, "form": form})

        # Analyze my team
        my_stats = []
        for p in my_players:
            bat = self.get_player_batting_stats(p)
            bowl = self.get_player_bowling_stats(p)
            form = self.get_player_form_tag(p)
            my_stats.append({"name": p, "bat": bat, "bowl": bowl, "form": form})

        # Opponent danger batsmen (sorted by total runs)
        danger_batsmen = sorted(opp_batsmen, key=lambda x: x["bat"]["total_runs"], reverse=True)
        danger_batsmen = [d for d in danger_batsmen if d["bat"]["total_runs"] > 0]

        # Opponent weak batsmen
        weak_batsmen = [d for d in opp_batsmen if d["bat"]["total_runs"] == 0 or d["bat"]["avg_sr"] < 100]

        # Opponent best bowlers (sorted by economy, lower is better)
        opp_bowlers_active = [d for d in opp_batsmen if d["bowl"]["total_overs"] > 0]
        opp_best_bowlers = sorted(opp_bowlers_active, key=lambda x: x["bowl"]["avg_econ"])
        opp_weak_bowlers = sorted(opp_bowlers_active, key=lambda x: x["bowl"]["avg_econ"], reverse=True)

        # My best batsmen
        my_best_batsmen = sorted(my_stats, key=lambda x: x["bat"]["total_runs"], reverse=True)
        my_best_batsmen = [d for d in my_best_batsmen if d["bat"]["total_runs"] > 0]

        # My best bowlers
        my_bowlers_active = [d for d in my_stats if d["bowl"]["total_overs"] > 0]
        my_best_bowlers = sorted(my_bowlers_active, key=lambda x: x["bowl"]["avg_econ"])
        my_wicket_takers = sorted(my_bowlers_active, key=lambda x: x["bowl"]["total_wickets"], reverse=True)

        # Key wickets to target
        key_wickets = danger_batsmen[:3]

        # Bowlers to target for runs
        target_bowlers = opp_weak_bowlers[:2] if opp_weak_bowlers else []

        # Bowlers to be careful against
        careful_bowlers = opp_best_bowlers[:2] if opp_best_bowlers else []

        # Generate batting tips
        batting_tips = []
        if target_bowlers:
            names = ", ".join(t["name"] for t in target_bowlers)
            batting_tips.append(f"🎯 Target {names} for runs — weakest economy in opponent bowling")
        if careful_bowlers:
            for b in careful_bowlers:
                batting_tips.append(f"🛡️ Play carefully against {b['name']} (Econ: {b['bowl']['avg_econ']}, Wkts: {b['bowl']['total_wickets']})")
        if my_best_batsmen:
            power = [p for p in my_best_batsmen if p["bat"]["avg_sr"] > 150][:2]
            if power:
                names = ", ".join(p["name"] for p in power)
                batting_tips.append(f"💥 Use {names} as power hitters — high strike rate")

        # Generate bowling tips
        bowling_tips = []
        if key_wickets:
            for kw in key_wickets:
                form_emoji, form_text = kw["form"]
                bowling_tips.append(
                    f"🔑 Get {kw['name']} out early — {int(kw['bat']['total_runs'])} runs, SR {kw['bat']['avg_sr']} {form_emoji}"
                )
        if weak_batsmen:
            names = ", ".join(w["name"] for w in weak_batsmen[:2])
            bowling_tips.append(f"⏳ Don't waste best bowlers on {names} — low threat")
        if my_best_bowlers:
            bowling_tips.append(f"🏆 Use {my_best_bowlers[0]['name']} in tight overs (Econ: {my_best_bowlers[0]['bowl']['avg_econ']})")
        if my_wicket_takers and my_wicket_takers[0]["bowl"]["total_wickets"] > 0:
            bowling_tips.append(f"⚡ Use {my_wicket_takers[0]['name']} against top batsmen ({my_wicket_takers[0]['bowl']['total_wickets']} wickets)")

        # Key matchups
        matchups = []
        if my_wicket_takers and danger_batsmen:
            matchups.append({
                "my": my_wicket_takers[0]["name"],
                "my_stat": f"{my_wicket_takers[0]['bowl']['total_wickets']}W, Econ {my_wicket_takers[0]['bowl']['avg_econ']}",
                "opp": danger_batsmen[0]["name"],
                "opp_stat": f"{int(danger_batsmen[0]['bat']['total_runs'])} runs, SR {danger_batsmen[0]['bat']['avg_sr']}",
                "label": "Your best bowler vs Their best batsman"
            })
        if my_best_batsmen and opp_best_bowlers:
            matchups.append({
                "my": my_best_batsmen[0]["name"],
                "my_stat": f"{int(my_best_batsmen[0]['bat']['total_runs'])} runs, SR {my_best_batsmen[0]['bat']['avg_sr']}",
                "opp": opp_best_bowlers[0]["name"],
                "opp_stat": f"{opp_best_bowlers[0]['bowl']['total_wickets']}W, Econ {opp_best_bowlers[0]['bowl']['avg_econ']}",
                "label": "Your best batsman vs Their best bowler"
            })

        # Summary
        summary_parts = []
        if key_wickets:
            summary_parts.append(f"Get {key_wickets[0]['name']} out early")
        if target_bowlers:
            summary_parts.append(f"target {target_bowlers[0]['name']}'s bowling")
        if my_best_bowlers:
            summary_parts.append(f"use {my_best_bowlers[0]['name']} in tight overs")
        summary = "Win this match by: " + ", ".join(summary_parts) if summary_parts else ""

        return {
            "batting_tips": batting_tips,
            "bowling_tips": bowling_tips,
            "key_wickets": key_wickets,
            "target_bowlers": target_bowlers,
            "careful_bowlers": careful_bowlers,
            "matchups": matchups,
            "summary": summary,
            "danger_batsmen": danger_batsmen,
            "opp_best_bowlers": opp_best_bowlers
        }


    def predict_match(self, team_a: str, team_b: str) -> Dict:
        """Predict match winner with scorecard prediction and weakness spotlight."""

        def analyze_team(team_name):
            players = self.get_team_players(team_name)
            if not players:
                return {"total": 0, "batting": 0, "bowling": 0, "form": 0,
                        "key_player": "", "key_form": ("⚪", "No Data"),
                        "scorecard": {}, "weaknesses": [], "player_details": []}

            bat_scores, bowl_scores, form_scores = [], [], []
            best_player, best_rating, best_player_form = "", 0, ("⚪", "No Data")
            top_scorer, top_scorer_runs = "", 0
            top_wicket_taker, top_wicket_taker_wkts = "", 0
            player_details = []
            declining_count, no_data_count = 0, 0
            weak_bowlers, high_econ_bowlers = [], []

            for p in players:
                bat = self.get_player_batting_stats(p)
                bowl = self.get_player_bowling_stats(p)
                form_emoji, form_text = self.get_player_form_tag(p)

                b_score = bat["total_runs"] + (bat["avg_sr"] * 0.3) + (bat["total_6s"] * 5)
                w_score = bowl["total_wickets"] * 20 + (10 - min(bowl["avg_econ"], 10)) * 3
                bat_scores.append(b_score)
                bowl_scores.append(w_score)

                form_map = {"Hot Form": 30, "Rising": 20, "Dangerous": 25, "Wicket Threat": 22,
                            "Economical": 18, "Steady": 10, "Declining": -10, "Limited Data": 5, "No Data": 0}
                form_scores.append(form_map.get(form_text, 0))

                overall = b_score + w_score
                if overall > best_rating:
                    best_rating = overall
                    best_player = p
                    best_player_form = (form_emoji, form_text)

                if bat["avg_runs"] > top_scorer_runs:
                    top_scorer_runs = bat["avg_runs"]
                    top_scorer = p
                if bowl["total_wickets"] > top_wicket_taker_wkts:
                    top_wicket_taker_wkts = bowl["total_wickets"]
                    top_wicket_taker = p

                if form_text == "Declining":
                    declining_count += 1
                if form_text in ("No Data", "Limited Data"):
                    no_data_count += 1
                if bowl["total_overs"] > 0 and bowl["avg_econ"] > 12:
                    high_econ_bowlers.append(p)
                if bat["total_runs"] == 0 and bowl["total_wickets"] == 0:
                    weak_bowlers.append(p)

                player_details.append({
                    "name": p, "runs": int(bat["total_runs"]), "avg_runs": bat["avg_runs"],
                    "sr": bat["avg_sr"], "wickets": bowl["total_wickets"], "econ": bowl["avg_econ"],
                    "form": (form_emoji, form_text)
                })

            avg_bat = sum(bat_scores) / len(bat_scores) if bat_scores else 0
            avg_bowl = sum(bowl_scores) / len(bowl_scores) if bowl_scores else 0
            avg_form = sum(form_scores) / len(form_scores) if form_scores else 0
            total = avg_bat * 0.4 + avg_bowl * 0.4 + avg_form * 0.2

            # Predicted scorecard: use avg runs per match per player (not career totals)
            active_batsmen = [p for p in player_details if p["avg_runs"] > 0]
            if active_batsmen:
                avg_runs_per_player = sum(p["avg_runs"] for p in active_batsmen) / len(active_batsmen)
                # For a 6-over match, typically 6-7 batsmen contribute
                contributing = min(len(active_batsmen), 6)
                expected_runs_base = avg_runs_per_player * contributing
                form_mult = 1.0 + (avg_form / 300)
                expected_low = int(expected_runs_base * 0.85 * form_mult)
                expected_high = int(expected_runs_base * 1.15 * form_mult)
            else:
                expected_low, expected_high = 50, 80

            # Weakness spotlight
            weaknesses = []
            if declining_count >= 2:
                weaknesses.append(("⚠️", str(declining_count) + " players in declining form — risk factor"))
            if no_data_count >= 2:
                weaknesses.append(("❓", str(no_data_count) + " players with no data — unpredictable"))
            if high_econ_bowlers:
                names = ", ".join(high_econ_bowlers[:2])
                weaknesses.append(("💸", names + " leaking runs — economy above 12"))
            active_bowlers = [p for p in player_details if p["wickets"] > 0]
            if len(active_bowlers) < 3:
                weaknesses.append(("🎯", "Only " + str(len(active_bowlers)) + " proven wicket-takers — bowling depth concern"))
            if not weaknesses:
                weaknesses.append(("✅", "No major weaknesses identified"))

            return {
                "total": total, "batting": avg_bat, "bowling": avg_bowl, "form": avg_form,
                "key_player": best_player, "key_form": best_player_form,
                "scorecard": {
                    "expected_low": expected_low, "expected_high": expected_high,
                    "top_scorer": top_scorer, "top_scorer_runs": int(top_scorer_runs),
                    "top_wicket_taker": top_wicket_taker, "top_wicket_taker_wkts": top_wicket_taker_wkts,
                },
                "weaknesses": weaknesses,
                "player_details": player_details,
            }

        sa = analyze_team(team_a)
        sb = analyze_team(team_b)

        total = sa["total"] + sb["total"]
        prob_a = round((sa["total"] / total) * 100) if total > 0 else 50
        prob_b = 100 - prob_a

        bat_edge = team_a if sa["batting"] >= sb["batting"] else team_b
        bowl_edge = team_a if sa["bowling"] >= sb["bowling"] else team_b
        form_edge = team_a if sa["form"] >= sb["form"] else team_b
        predicted_winner = team_a if prob_a >= prob_b else team_b
        confidence = "High" if abs(prob_a - prob_b) > 20 else "Medium" if abs(prob_a - prob_b) > 10 else "Low"

        return {
            "prob_a": prob_a, "prob_b": prob_b,
            "predicted_winner": predicted_winner, "confidence": confidence,
            "bat_edge": bat_edge, "bowl_edge": bowl_edge, "form_edge": form_edge,
            "stats_a": sa, "stats_b": sb,
        }
