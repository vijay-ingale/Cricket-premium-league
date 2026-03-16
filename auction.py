import json
import os
from datetime import datetime

DATA_DIR = os.environ.get('DATA_DIR', 'data')


class AuctionManager:
    def __init__(self, data_file=None):
        self.data_file = data_file or os.path.join(DATA_DIR, 'auction_data.json')
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return self._default_data()

    def _default_data(self):
        return {
            "config": {
                "num_teams": 4,
                "squad_size": 7,
                "budget_per_team": 50000,
                "bid_increment": 50,
                "teams": ["Team A", "Team B", "Team C", "Team D"],
                "captains": {},
                "rounds": []
            },
            "state": {
                "active": False,
                "current_round": 0,
                "sold": [],
                "team_squads": {},
                "team_spent": {}
            },
            "history": []
        }

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    # --- Config ---
    def update_config(self, num_teams, squad_size, budget, bid_increment, team_names):
        self.data["config"]["num_teams"] = num_teams
        self.data["config"]["squad_size"] = squad_size
        self.data["config"]["budget_per_team"] = budget
        self.data["config"]["bid_increment"] = bid_increment
        self.data["config"]["teams"] = team_names[:num_teams]
        self._save()

    def set_captain(self, team, captain_name):
        self.data["config"]["captains"][team] = captain_name
        self._save()

    def get_captains(self):
        return self.data["config"].get("captains", {})

    def get_bid_increment(self):
        return self.data["config"].get("bid_increment", 50)
    def set_bid_increment(self, increment):
        self.data["config"]["bid_increment"] = increment
        self._save()

    def add_round(self, name, base_price, max_bid_per_player, players):
        self.data["config"]["rounds"].append({
            "name": name,
            "base_price": base_price,
            "max_bid_per_player": max_bid_per_player,
            "players": players
        })
        self._save()


    def update_round(self, idx, name, base_price, max_bid_per_player, players):
        if 0 <= idx < len(self.data["config"]["rounds"]):
            self.data["config"]["rounds"][idx] = {
                "name": name, "base_price": base_price,
                "max_bid_per_player": max_bid_per_player, "players": players
            }
            self._save()

    def delete_round(self, idx):
        if 0 <= idx < len(self.data["config"]["rounds"]):
            self.data["config"]["rounds"].pop(idx)
            self._save()

    def get_rounds(self):
        return self.data["config"]["rounds"]

    def get_teams(self):
        return self.data["config"]["teams"]

    def get_budget(self):
        return self.data["config"]["budget_per_team"]

    # --- Auction State ---
    def start_auction(self):
        teams = self.data["config"]["teams"]
        captains = self.get_captains()
        self.data["state"] = {
            "active": True,
            "current_round": 0,
            "sold": [],
            "team_squads": {},
            "team_spent": {t: 0 for t in teams}
        }
        # Pre-populate squads with captains
        for t in teams:
            cap = captains.get(t, "")
            if cap:
                self.data["state"]["team_squads"][t] = [{"name": cap, "category": "Captain", "bid": 0}]
            else:
                self.data["state"]["team_squads"][t] = []
        self._save()

    def is_active(self):
        return self.data["state"].get("active", False)

    def get_current_round_idx(self):
        return self.data["state"].get("current_round", 0)

    def get_current_round(self):
        idx = self.get_current_round_idx()
        rounds = self.get_rounds()
        if 0 <= idx < len(rounds):
            return rounds[idx]
        return None

    def get_team_budget_remaining(self, team):
        budget = self.data["config"]["budget_per_team"]
        spent = self.data["state"]["team_spent"].get(team, 0)
        return budget - spent

    def get_team_squad(self, team):
        return self.data["state"]["team_squads"].get(team, [])

    def get_team_auction_player_count(self, team):
        """Count only auctioned players (exclude captain)."""
        squad = self.get_team_squad(team)
        return len([p for p in squad if p.get("category") != "Captain"])

    def get_remaining_slots(self, team):
        """How many more players this team needs to buy via auction."""
        squad_size = self.data["config"]["squad_size"]
        has_captain = bool(self.get_captains().get(team, ""))
        # Captain takes 1 slot, rest are auction slots
        auction_slots = squad_size - (1 if has_captain else 0)
        bought = self.get_team_auction_player_count(team)
        return max(0, auction_slots - bought)

    def get_min_base_price_remaining(self, team):
        """Get the minimum base price across all remaining rounds (current + future)."""
        rounds = self.get_rounds()
        current = self.get_current_round_idx()
        min_price = None
        for i in range(current, len(rounds)):
            bp = rounds[i]["base_price"]
            if min_price is None or bp < min_price:
                min_price = bp
        return min_price or 0

    def get_max_bid(self, team, round_idx=None):
        """Max a team can bid on current player considering budget reserve AND round cap."""
        remaining_budget = self.get_team_budget_remaining(team)
        remaining_slots = self.get_remaining_slots(team)
        if remaining_slots <= 1:
            budget_max = remaining_budget
        else:
            min_base = self.get_min_base_price_remaining(team)
            reserved = (remaining_slots - 1) * min_base
            budget_max = max(0, remaining_budget - reserved)
        # Apply round cap if available
        if round_idx is not None:
            rounds = self.get_rounds()
            if 0 <= round_idx < len(rounds):
                round_cap = rounds[round_idx].get("max_bid_per_player", 0)
                if round_cap > 0:
                    return min(budget_max, round_cap)
        return budget_max

    def get_team_bid_status(self, team, round_idx=None):
        """Get detailed bid status for display."""
        remaining = self.get_team_budget_remaining(team)
        slots = self.get_remaining_slots(team)
        max_bid = self.get_max_bid(team, round_idx)
        min_base = self.get_min_base_price_remaining(team)
        # Check if team can only bid at base price
        if round_idx is not None:
            rounds = self.get_rounds()
            if 0 <= round_idx < len(rounds):
                base = rounds[round_idx]["base_price"]
                if max_bid <= base:
                    return {"max_bid": max_bid, "status": "base_only", "msg": "⚠️ Can only bid at base price"}
                if remaining < base:
                    return {"max_bid": 0, "status": "no_budget", "msg": "❌ No budget remaining"}
        return {"max_bid": max_bid, "status": "ok", "msg": ""}

    def get_sold_player_names(self):
        return [s["player"] for s in self.data["state"]["sold"]]

    def get_player_sold_info(self, player_name):
        for s in self.data["state"]["sold"]:
            if s["player"] == player_name:
                return s
        return None

    def sell_player(self, player_name, category, team, bid_amount, round_idx):
        remaining = self.get_team_budget_remaining(team)
        if bid_amount > remaining:
            return False, "Not enough budget"
        max_bid = self.get_max_bid(team, round_idx)
        if bid_amount > max_bid:
            return False, f"Exceeds max bid ({max_bid}). Need to reserve for remaining slots."

        sale = {
            "player": player_name,
            "category": category,
            "team": team,
            "bid": bid_amount,
            "round_idx": round_idx,
            "round_name": self.get_rounds()[round_idx]["name"]
        }
        self.data["state"]["sold"].append(sale)
        self.data["state"]["team_squads"][team].append({
            "name": player_name,
            "category": category,
            "bid": bid_amount
        })
        self.data["state"]["team_spent"][team] = self.data["state"]["team_spent"].get(team, 0) + bid_amount
        self._save()
        return True, "Sold"

    def undo_last_sale(self):
        sold = self.data["state"]["sold"]
        if not sold:
            return False, "Nothing to undo"
        last = sold.pop()
        team = last["team"]
        squad = self.data["state"]["team_squads"][team]
        # Remove last matching entry
        for i in range(len(squad) - 1, -1, -1):
            if squad[i]["name"] == last["player"] and squad[i]["bid"] == last["bid"]:
                squad.pop(i)
                break
        self.data["state"]["team_spent"][team] -= last["bid"]
        self._save()
        return True, f"Undid sale of {last['player']}"

    def next_round(self):
        self.data["state"]["current_round"] += 1
        self._save()

    def prev_round(self):
        if self.data["state"]["current_round"] > 0:
            self.data["state"]["current_round"] -= 1
            self._save()

    def finish_auction(self):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": self.data["config"].copy(),
            "results": {
                "sold": self.data["state"]["sold"],
                "team_squads": self.data["state"]["team_squads"],
                "team_spent": self.data["state"]["team_spent"]
            }
        }
        self.data["history"].append(entry)
        self.data["state"]["active"] = False
        self._save()
        return entry

    def reset_auction(self):
        self.data["state"] = {
            "active": False,
            "current_round": 0,
            "sold": [],
            "team_squads": {},
            "team_spent": {}
        }
        self._save()

    def get_history(self):
        return self.data.get("history", [])

    def delete_history_entry(self, idx):
        if 0 <= idx < len(self.data["history"]):
            self.data["history"].pop(idx)
            self._save()

    def get_all_assigned_players(self):
        assigned = []
        for r in self.data["config"]["rounds"]:
            for p in r["players"]:
                assigned.append(p["name"])
        return assigned

    def get_auction_summary(self):
        teams = self.data["config"]["teams"]
        budget = self.data["config"]["budget_per_team"]
        summary = {}
        for team in teams:
            spent = self.data["state"]["team_spent"].get(team, 0)
            squad = self.data["state"]["team_squads"].get(team, [])
            summary[team] = {
                "squad": squad,
                "spent": spent,
                "remaining": budget - spent,
                "count": len(squad)
            }
        return summary
