import pdfplumber
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class RatingSystem:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.rating_history_file = os.path.join(data_dir, 'rating_history.json')
        self.name_mapping_file = os.path.join(data_dir, 'name_mapping.json')
        self.rating_history = self._load_rating_history()
        self.name_mapping = self._load_name_mapping()
    
    def _load_rating_history(self):
        if os.path.exists(self.rating_history_file):
            with open(self.rating_history_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_rating_history(self):
        with open(self.rating_history_file, 'w') as f:
            json.dump(self.rating_history, f, indent=2)
    
    def _load_name_mapping(self):
        """Load name mapping: PDF name -> Database name"""
        if os.path.exists(self.name_mapping_file):
            with open(self.name_mapping_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_name_mapping(self):
        with open(self.name_mapping_file, 'w') as f:
            json.dump(self.name_mapping, f, indent=2)
    
    def save_latest_leaderboard(self, batting_df: pd.DataFrame, bowling_df: pd.DataFrame, mvp_df: pd.DataFrame, date: str):
        """Save the latest match leaderboard data"""
        leaderboard_file = os.path.join(self.data_dir, 'latest_leaderboard.json')
        
        leaderboard_data = {
            'date': date,
            'batting': batting_df.to_dict('records') if not batting_df.empty else [],
            'bowling': bowling_df.to_dict('records') if not bowling_df.empty else [],
            'mvp': mvp_df.to_dict('records') if not mvp_df.empty else []
        }
        
        with open(leaderboard_file, 'w') as f:
            json.dump(leaderboard_data, f, indent=2)
    
    def get_latest_leaderboard(self):
        """Get the latest match leaderboard data"""
        leaderboard_file = os.path.join(self.data_dir, 'latest_leaderboard.json')
        
        if os.path.exists(leaderboard_file):
            with open(leaderboard_file, 'r') as f:
                return json.load(f)
        return None
    
    def add_name_mapping(self, pdf_name: str, db_name: str):
        """Map a PDF name to database name"""
        self.name_mapping[pdf_name] = db_name
        self._save_name_mapping()
    
    def remove_name_mapping(self, pdf_name: str):
        """Remove a name mapping"""
        if pdf_name in self.name_mapping:
            del self.name_mapping[pdf_name]
            self._save_name_mapping()
            return True
        return False
    
    def get_mapped_name(self, pdf_name: str) -> str:
        """Get database name from PDF name (or return original if no mapping)"""
        return self.name_mapping.get(pdf_name, pdf_name)
    
    def parse_batting_pdf(self, pdf_file) -> pd.DataFrame:
        """Parse batting leaderboard PDF"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page = pdf.pages[0]
                tables = page.extract_tables()
                
                if tables:
                    df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                    # Clean and convert data types
                    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce').fillna(0)
                    df['SR'] = pd.to_numeric(df['SR'], errors='coerce').fillna(0)
                    df['4s'] = pd.to_numeric(df['4s'], errors='coerce').fillna(0)
                    df['6s'] = pd.to_numeric(df['6s'], errors='coerce').fillna(0)
                    return df
        except Exception as e:
            print(f"Error parsing batting PDF: {e}")
        return pd.DataFrame()
    
    def parse_bowling_pdf(self, pdf_file) -> pd.DataFrame:
        """Parse bowling leaderboard PDF"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page = pdf.pages[0]
                tables = page.extract_tables()
                
                if tables:
                    df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                    # Clean and convert data types
                    df['Wickets'] = pd.to_numeric(df['Wickets'], errors='coerce').fillna(0)
                    df['Econ'] = pd.to_numeric(df['Econ'], errors='coerce').fillna(0)
                    df['Overs'] = pd.to_numeric(df['Overs'], errors='coerce').fillna(0)
                    return df
        except Exception as e:
            print(f"Error parsing bowling PDF: {e}")
        return pd.DataFrame()
    
    def parse_mvp_pdf(self, pdf_file) -> pd.DataFrame:
        """Parse MVP leaderboard PDF"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page = pdf.pages[0]
                tables = page.extract_tables()
                
                if tables:
                    df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                    # Clean and convert data types
                    df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)
                    df['Batting'] = pd.to_numeric(df['Batting'], errors='coerce').fillna(0)
                    df['Bowling'] = pd.to_numeric(df['Bowling'], errors='coerce').fillna(0)
                    return df
        except Exception as e:
            print(f"Error parsing MVP PDF: {e}")
        return pd.DataFrame()
    
    def calculate_batting_rating(self, df: pd.DataFrame, player_name: str) -> Tuple[float, Dict]:
        """Calculate batting rating for a player based on absolute performance benchmarks"""
        if df.empty or player_name not in df['Player Name'].values:
            return 0, {}
        
        player_row = df[df['Player Name'] == player_name].iloc[0]
        
        # Absolute benchmarks (not comparing with others)
        # These are "excellent" performance targets
        EXCELLENT_RUNS = 60      # 60+ runs = excellent
        EXCELLENT_SR = 200       # 200+ SR = excellent
        EXCELLENT_SIXES = 6      # 6+ sixes = excellent
        EXCELLENT_FOURS = 8      # 8+ fours = excellent
        
        # Calculate scores (capped at 1.0)
        runs_score = min(player_row['Runs'] / EXCELLENT_RUNS, 1.0) if EXCELLENT_RUNS > 0 else 0
        sr_score = min(player_row['SR'] / EXCELLENT_SR, 1.0) if EXCELLENT_SR > 0 else 0
        sixes_score = min(player_row['6s'] / EXCELLENT_SIXES, 1.0) if EXCELLENT_SIXES > 0 else 0
        fours_score = min(player_row['4s'] / EXCELLENT_FOURS, 1.0) if EXCELLENT_FOURS > 0 else 0
        
        # Calculate weighted rating
        rating = (
            runs_score * 0.30 +
            sr_score * 0.25 +
            sixes_score * 0.30 +
            fours_score * 0.15
        ) * 5
        
        stats = {
            'runs': int(player_row['Runs']),
            'sr': float(player_row['SR']),
            'sixes': int(player_row['6s']),
            'fours': int(player_row['4s'])
        }
        
        return round(rating, 2), stats
    
    def calculate_bowling_rating(self, df: pd.DataFrame, player_name: str) -> Tuple[float, Dict]:
        """Calculate bowling rating for a player based on absolute performance benchmarks"""
        if df.empty or player_name not in df['Player Name'].values:
            return 0, {}
        
        player_row = df[df['Player Name'] == player_name].iloc[0]
        
        # Absolute benchmarks (not comparing with others)
        EXCELLENT_WICKETS = 4    # 4+ wickets = excellent
        EXCELLENT_ECON = 6.0     # 6.0 or lower economy = excellent
        EXCELLENT_OVERS = 4.0    # 4+ overs = excellent
        
        # Calculate scores (capped at 1.0)
        wickets_score = min(player_row['Wickets'] / EXCELLENT_WICKETS, 1.0) if EXCELLENT_WICKETS > 0 else 0
        
        # Economy: lower is better, so invert the score
        if player_row['Econ'] > 0:
            econ_score = min(EXCELLENT_ECON / player_row['Econ'], 1.0)
        else:
            econ_score = 1.0
        
        overs_score = min(player_row['Overs'] / EXCELLENT_OVERS, 1.0) if EXCELLENT_OVERS > 0 else 0
        
        # Calculate weighted rating
        rating = (
            wickets_score * 0.50 +
            econ_score * 0.30 +
            overs_score * 0.20
        ) * 5
        
        stats = {
            'wickets': int(player_row['Wickets']),
            'economy': float(player_row['Econ']),
            'overs': float(player_row['Overs'])
        }
        
        return round(rating, 2), stats
    
    def calculate_overall_rating(self, batting_rating: float, bowling_rating: float, 
                                 mvp_score: float, category: str) -> float:
        """Calculate overall rating based on player category"""
        if category == 'Batsman':
            return round(batting_rating, 1)
        elif category == 'Bowler':
            return round(bowling_rating, 1)
        else:  # All-rounder
            return round((batting_rating * 0.40 + bowling_rating * 0.40 + mvp_score * 0.20), 1)
    
    def add_rating_entry(self, player_name: str, category: str, date: str, 
                        batting_rating: float, bowling_rating: float, 
                        overall_rating: float, stats: Dict):
        """Add a new rating entry for a player"""
        if player_name not in self.rating_history:
            self.rating_history[player_name] = {
                'category': category,
                'entries': []
            }
        
        entry = {
            'date': date,
            'batting_rating': batting_rating,
            'bowling_rating': bowling_rating,
            'overall_rating': overall_rating,
            'stats': stats
        }
        
        self.rating_history[player_name]['entries'].append(entry)
        self._save_rating_history()
    
    def get_cumulative_rating(self, player_name: str) -> float:
        """Calculate cumulative rating from all entries, ignoring absent matches (0 rating with no stats)"""
        if player_name not in self.rating_history:
            return 0
        
        entries = self.rating_history[player_name]['entries']
        if not entries:
            return 0
        
        # Filter out absent matches (0 rating with empty stats)
        played_entries = [e for e in entries if e.get('stats') or e.get('overall_rating', 0) > 0]
        if not played_entries:
            return 0
        
        # Weight recent performances higher
        total_weight = 0
        weighted_sum = 0
        
        for idx, entry in enumerate(reversed(played_entries)):
            weight = 1.0 / (idx + 1)  # Recent entries get higher weight
            weighted_sum += entry['overall_rating'] * weight
            total_weight += weight
        
        cumulative = weighted_sum / total_weight if total_weight > 0 else 0
        return round(min(cumulative, 5.0), 1)  # Cap at 5.0
    
    def get_player_history(self, player_name: str) -> List[Dict]:
        """Get rating history for a player"""
        if player_name in self.rating_history:
            return self.rating_history[player_name]['entries']
        return []
    
    def update_rating_entry(self, player_name: str, entry_index: int, new_rating: float):
        """Manually update a rating entry"""
        if player_name in self.rating_history:
            entries = self.rating_history[player_name]['entries']
            if 0 <= entry_index < len(entries):
                entries[entry_index]['overall_rating'] = new_rating
                self._save_rating_history()
                return True
        return False
    
    def delete_rating_entry(self, player_name: str, entry_index: int):
        """Delete a rating entry"""
        if player_name in self.rating_history:
            entries = self.rating_history[player_name]['entries']
            if 0 <= entry_index < len(entries):
                entries.pop(entry_index)
                self._save_rating_history()
                return True
        return False
