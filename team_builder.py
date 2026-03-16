import random
import json
import os
from typing import List, Dict
from datetime import datetime

class TeamBuilder:
    def __init__(self, data_file='players_data.json', history_file='team_history.json'):
        # Support Docker volume mounting
        data_dir = os.getenv('DATA_DIR', 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.data_file = os.path.join(data_dir, 'players_data.json')
        self.history_file = os.path.join(data_dir, 'team_history.json')
        self.all_players = self._load_players()
        self.team_history = self._load_history()
        self.selected_players = {
            'Batsman': [],
            'Bowler': [],
            'All-rounder': []
        }
        self.teams = []
    
    def _load_players(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                # Migrate old format to new format with ratings
                for cat in ['Batsman', 'Bowler', 'All-rounder']:
                    if cat in data:
                        if isinstance(data[cat], list):
                            # Old format: list of names -> convert to dict with ratings
                            data[cat] = {name: 0 for name in data[cat]}
                        elif not isinstance(data[cat], dict):
                            # Invalid format: reset to empty dict
                            data[cat] = {}
                    else:
                        data[cat] = {}
                return data
        return {
            'Batsman': {},
            'Bowler': {},
            'All-rounder': {}
        }
    
    def _save_players(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.all_players, f, indent=2)
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.team_history, f, indent=2)
    
    def finalize_teams(self):
        if not self.teams:
            return False
        
        # Create history entry
        history_entry = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'teams': []
        }
        
        for team in self.teams:
            history_entry['teams'].append({
                'name': team['name'],
                'players': team['players'],
                'total_rating': team.get('total_rating', 0),
                'batsman_rating': team.get('batsman_rating', 0),
                'bowler_rating': team.get('bowler_rating', 0),
                'allrounder_rating': team.get('allrounder_rating', 0)
            })
        
        # Add to history (keep last 20 entries)
        self.team_history.insert(0, history_entry)
        self.team_history = self.team_history[:20]
        self._save_history()
        return True
    
    def get_recent_history(self, limit=5):
        return self.team_history[:limit]
    
    def delete_history_entry(self, index):
        if 0 <= index < len(self.team_history):
            self.team_history.pop(index)
            self._save_history()
            return True
        return False
    
    def generate_match_schedule(self, ground_hours=2, match_duration_mins=30, start_time="10:00 AM"):
        if not self.teams or len(self.teams) < 2:
            return None
        
        # Calculate total matches possible
        total_minutes = int(ground_hours * 60)
        total_matches = int(total_minutes // match_duration_mins)
        
        num_teams = len(self.teams)
        team_names = [team['name'] for team in self.teams]
        
        # Get all players by team
        team_players = {i: self.teams[i]['players'] for i in range(num_teams)}
        
        # Generate all possible match combinations (round-robin)
        match_combinations = []
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                match_combinations.append((i, j))
        
        # Repeat combinations if time allows
        matches_per_round = len(match_combinations)
        full_rounds = int(total_matches // matches_per_round)
        remaining_matches = int(total_matches % matches_per_round)
        
        # Build match list
        all_matches = []
        for round_num in range(full_rounds):
            all_matches.extend(match_combinations)
        all_matches.extend(match_combinations[:remaining_matches])
        
        # Generate schedule with fair rotation
        schedule = []
        team_consecutive_matches = {i: 0 for i in range(num_teams)}
        team_rest_needed = {i: False for i in range(num_teams)}
        team_toss_wins = {i: 0 for i in range(num_teams)}
        team_last_batted_first = {i: None for i in range(num_teams)}
        
        # Track umpire/scorer assignments per player
        player_umpire_count = {}
        player_leg_umpire_count = {}
        player_scorer_count = {}
        
        for team_idx in range(num_teams):
            for player in team_players[team_idx]:
                player_umpire_count[player] = 0
                player_leg_umpire_count[player] = 0
                player_scorer_count[player] = 0
        
        # Parse start time
        from datetime import datetime, timedelta
        try:
            current_time = datetime.strptime(start_time, "%I:%M %p")
        except:
            current_time = datetime.strptime("10:00 AM", "%I:%M %p")
        
        for match_idx, (team1_idx, team2_idx) in enumerate(all_matches):
            match_num = match_idx + 1
            
            # Calculate time slot
            end_time = current_time + timedelta(minutes=match_duration_mins)
            time_slot = f"{current_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"
            
            # Determine toss winner (rotate fairly)
            if team_toss_wins[team1_idx] <= team_toss_wins[team2_idx]:
                toss_winner_idx = team1_idx
            else:
                toss_winner_idx = team2_idx
            team_toss_wins[toss_winner_idx] += 1
            
            # Determine batting order (alternate for each team)
            if team_last_batted_first[toss_winner_idx] is None:
                bats_first_idx = toss_winner_idx
            else:
                # Alternate
                bats_first_idx = team2_idx if team_last_batted_first[toss_winner_idx] else team1_idx
            
            bowls_first_idx = team2_idx if bats_first_idx == team1_idx else team1_idx
            
            # Update batting history
            team_last_batted_first[team1_idx] = (bats_first_idx == team1_idx)
            team_last_batted_first[team2_idx] = (bats_first_idx == team2_idx)
            
            # Determine resting teams
            playing_teams = {team1_idx, team2_idx}
            resting_team_indices = [i for i in range(num_teams) if i not in playing_teams]
            resting_teams = [team_names[i] for i in resting_team_indices]
            
            # Assign umpires and scorer from resting teams
            main_umpire = None
            leg_umpire = None
            scorer = None
            
            if resting_team_indices:
                # Get all resting players
                resting_players = []
                for team_idx in resting_team_indices:
                    for player in team_players[team_idx]:
                        resting_players.append((player, team_idx))
                
                if len(resting_players) >= 3:
                    # Sort by assignment count to ensure fair rotation
                    resting_players_sorted = sorted(resting_players, 
                        key=lambda x: (player_umpire_count[x[0]], player_leg_umpire_count[x[0]], player_scorer_count[x[0]]))
                    
                    # Assign main umpire (least assigned)
                    main_umpire = resting_players_sorted[0][0]
                    player_umpire_count[main_umpire] += 1
                    
                    # Assign leg umpire (different from main umpire)
                    for player, team_idx in resting_players_sorted[1:]:
                        if player != main_umpire:
                            leg_umpire = player
                            player_leg_umpire_count[leg_umpire] += 1
                            break
                    
                    # Assign scorer (different from both umpires)
                    for player, team_idx in resting_players_sorted:
                        if player != main_umpire and player != leg_umpire:
                            scorer = player
                            player_scorer_count[scorer] += 1
                            break
            
            # Update consecutive match counters
            for i in range(num_teams):
                if i in playing_teams:
                    team_consecutive_matches[i] += 1
                else:
                    team_consecutive_matches[i] = 0
            
            schedule.append({
                'match_num': match_num,
                'time_slot': time_slot,
                'team1': team_names[team1_idx],
                'team2': team_names[team2_idx],
                'toss_winner': team_names[toss_winner_idx],
                'bats_first': team_names[bats_first_idx],
                'bowls_first': team_names[bowls_first_idx],
                'resting_teams': resting_teams,
                'main_umpire': main_umpire,
                'leg_umpire': leg_umpire,
                'scorer': scorer
            })
            
            current_time = end_time
        
        return {
            'total_matches': len(schedule),
            'ground_hours': ground_hours,
            'match_duration': match_duration_mins,
            'matches': schedule
        }
    
    def add_player_to_database(self, name: str, category: str, rating: int = 0):
        if category in self.all_players and name not in self.all_players[category]:
            self.all_players[category][name] = rating
            self._save_players()
            return True
        return False
    
    def update_player_rating(self, name: str, category: str, rating: int):
        if category in self.all_players and name in self.all_players[category]:
            self.all_players[category][name] = rating
            self._save_players()
            return True
        return False
    
    def remove_player_from_database(self, name: str, category: str):
        if category in self.all_players and name in self.all_players[category]:
            del self.all_players[category][name]
            self._save_players()
            return True
        return False
    
    def select_player(self, name: str, category: str):
        if category in self.selected_players and name not in self.selected_players[category]:
            self.selected_players[category].append(name)
    
    def deselect_player(self, name: str, category: str):
        if category in self.selected_players and name in self.selected_players[category]:
            self.selected_players[category].remove(name)
    
    def select_all_players(self):
        for cat in ['Batsman', 'Bowler', 'All-rounder']:
            self.selected_players[cat] = self.all_players[cat].copy()
    
    def get_total_selected_players(self):
        return sum(len(players) for players in self.selected_players.values())
    
    def get_total_database_players(self):
        return sum(len(players) for players in self.all_players.values())
    
    def create_teams(self, num_teams: int):
        total_players = self.get_total_selected_players()
        if total_players == 0 or num_teams == 0:
            return []
        
        # Initialize teams
        teams = [{'name': self._get_team_name(i), 'players': [], 'total_rating': 0,
                  'batsman_rating': 0, 'bowler_rating': 0, 'allrounder_rating': 0} 
                 for i in range(num_teams)]
        
        # Process each category separately for balanced distribution
        for cat in ['Batsman', 'Bowler', 'All-rounder']:
            # Get players from this category with ratings
            category_players = []
            for player in self.selected_players[cat]:
                rating = self.all_players[cat].get(player, 0)
                category_players.append({
                    'name': player,
                    'category': cat,
                    'rating': rating
                })
            
            # Sort by rating (highest first)
            category_players.sort(key=lambda x: x['rating'], reverse=True)
            
            # Add randomization within same rating groups
            rating_groups = {}
            for player in category_players:
                rating = player['rating']
                if rating not in rating_groups:
                    rating_groups[rating] = []
                rating_groups[rating].append(player)
            
            # Shuffle within each rating group
            for rating in rating_groups:
                random.shuffle(rating_groups[rating])
            
            # Rebuild sorted list with shuffled groups
            category_players = []
            for rating in sorted(rating_groups.keys(), reverse=True):
                category_players.extend(rating_groups[rating])
            
            # Distribute using snake draft for this category
            team_order = []
            num_rounds = (len(category_players) + num_teams - 1) // num_teams
            for round_num in range(num_rounds):
                if round_num % 2 == 0:
                    team_order.extend(range(num_teams))
                else:
                    team_order.extend(range(num_teams - 1, -1, -1))
            
            # Assign players from this category
            for idx, player_data in enumerate(category_players):
                if idx < len(team_order):
                    team_idx = team_order[idx]
                    teams[team_idx]['players'].append(player_data['name'])
                    teams[team_idx]['total_rating'] += player_data['rating']
                    
                    # Track category-specific ratings
                    if cat == 'Batsman':
                        teams[team_idx]['batsman_rating'] += player_data['rating']
                    elif cat == 'Bowler':
                        teams[team_idx]['bowler_rating'] += player_data['rating']
                    else:
                        teams[team_idx]['allrounder_rating'] += player_data['rating']
        
        self.teams = teams
        return teams
    
    def _get_team_name(self, index: int):
        return f"Team-{chr(65 + index)}"  # Team-A, Team-B, etc.
    
    def move_player(self, player: str, from_team_idx: int, to_team_idx: int):
        if 0 <= from_team_idx < len(self.teams) and 0 <= to_team_idx < len(self.teams):
            if player in self.teams[from_team_idx]['players']:
                self.teams[from_team_idx]['players'].remove(player)
                self.teams[to_team_idx]['players'].append(player)
    
    def remove_player_from_team(self, player: str, team_idx: int):
        """Remove a player from a team"""
        if 0 <= team_idx < len(self.teams):
            if player in self.teams[team_idx]['players']:
                self.teams[team_idx]['players'].remove(player)
                return True
        return False
    
    def update_team_name(self, team_idx: int, new_name: str):
        if 0 <= team_idx < len(self.teams):
            self.teams[team_idx]['name'] = new_name

    def clear_selection(self):
        self.selected_players = {
            'Batsman': [],
            'Bowler': [],
            'All-rounder': []
        }
