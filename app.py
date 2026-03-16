import streamlit as st
import streamlit.components.v1 as components
from team_builder import TeamBuilder
from auction import AuctionManager

from scouting import ScoutingManager

# Initialize session state
if 'team_builder' not in st.session_state:
    st.session_state.team_builder = TeamBuilder()
if 'teams_created' not in st.session_state:
    st.session_state.teams_created = False
if 'rating_system' not in st.session_state:
    from rating_system import RatingSystem
    st.session_state.rating_system = RatingSystem()
if 'auction_manager' not in st.session_state:
    st.session_state.auction_manager = AuctionManager()
if 'scouting_manager' not in st.session_state:
    st.session_state.scouting_manager = ScoutingManager()
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'team_builder'

st.set_page_config(page_title="Cricket Team Builder", page_icon="🏏", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown("""
    <style>
    .main {background: #f8f9fa; padding: 0 !important;}
    .stApp {background: #ffffff;}
    div[data-testid="stSidebar"] {background: linear-gradient(180deg, #0f766e 0%, #0d9488 100%);}
    div[data-testid="stSidebar"] * {color: white !important;}
    h1 {color: #1e293b; text-align: center; font-size: 2.8rem !important; font-weight: 700 !important; padding: 20px 0; margin: 0 0 20px 0 !important;}
    h2 {color: #334155; font-weight: 600 !important; padding: 12px 0; margin: 16px 0 !important; border-bottom: 2px solid #e2e8f0; font-size: 1.8rem !important;}
    h3 {color: #475569; font-weight: 600 !important; font-size: 1.3rem !important;}
    .stButton>button {background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); color: white; border: none; border-radius: 8px; padding: 12px 24px; font-weight: 600; font-size: 1.1rem; transition: all 0.3s; box-shadow: 0 2px 4px rgba(20, 184, 166, 0.3);}
    .stButton>button:hover {transform: translateY(-1px); box-shadow: 0 3px 6px rgba(20, 184, 166, 0.4); background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);}
    div[data-testid="stExpander"] {background-color: rgba(255,255,255,0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);}
    .stTabs [data-baseweb="tab-list"] {gap: 4px; background-color: #f1f5f9; padding: 4px; border-radius: 8px;}
    .stTabs [data-baseweb="tab"] {background-color: white; border-radius: 8px; padding: 10px 20px; font-weight: 600; font-size: 1.1rem; color: #64748b; border: 2px solid transparent;}
    .stTabs [aria-selected="true"] {background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); color: white !important; border-color: #14b8a6;}
    .stCheckbox {background: white; padding: 8px 12px; border-radius: 8px; margin: 6px 0; border: 1px solid #e2e8f0; transition: all 0.2s;}
    .stCheckbox:hover {border-color: #14b8a6; box-shadow: 0 2px 4px rgba(20, 184, 166, 0.1);}
    .stCheckbox label {font-size: 1.1rem !important;}
    .stTextInput>div>div>input {border-radius: 8px; border: 2px solid #e2e8f0; padding: 10px 16px; font-size: 1.1rem;}
    .stTextInput>div>div>input:focus {border-color: #14b8a6;}
    .block-container {padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 100% !important;}
    section[data-testid="stSidebar"] .block-container {padding-top: 2rem !important;}
    .team-card {height: 450px; overflow-y: auto; padding-right: 8px; margin-top: 8px;}
    .team-card::-webkit-scrollbar {width: 5px;}
    .team-card::-webkit-scrollbar-track {background: #f1f5f9; border-radius: 10px;}
    .team-card::-webkit-scrollbar-thumb {background: #14b8a6; border-radius: 10px;}
    hr {margin: 6px 0 !important;}
    .stNumberInput {margin-bottom: 0 !important;}
    .stNumberInput > div {margin-bottom: 0 !important;}
    .element-container {margin-bottom: 0 !important;}
    div[data-testid="column"] {padding: 0 0.75rem !important;}
    .stTabs [data-baseweb="tab-panel"] {padding-top: 1rem !important;}
    div[data-testid="column"] > div {margin-top: 0 !important;}
    .block-container > div:first-child {margin-top: 0 !important;}
    .stMarkdown p {font-size: 1.1rem !important;}
    .stMarkdown li {font-size: 1.1rem !important;}
    .stSelectbox label {font-size: 1.1rem !important;}
    .stNumberInput label {font-size: 1.1rem !important;}
    div[data-baseweb="select"] {font-size: 1.1rem !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏏 Cricket Team Builder</h1>", unsafe_allow_html=True)

# Navigation
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    if st.button("🏏 Team Builder", use_container_width=True, type="primary" if st.session_state.current_view == 'team_builder' else "secondary"):
        st.session_state.current_view = 'team_builder'
        st.rerun()
with col2:
    if st.button("📊 Rating Manager", use_container_width=True, type="primary" if st.session_state.current_view == 'rating_manager' else "secondary"):
        st.session_state.current_view = 'rating_manager'
        st.rerun()
with col3:
    if st.button("🏆 Leaderboard", use_container_width=True, type="primary" if st.session_state.current_view == 'leaderboard' else "secondary"):
        st.session_state.current_view = 'leaderboard'
        st.rerun()
with col4:
    if st.button("🔨 Auction", use_container_width=True, type="primary" if st.session_state.current_view == 'auction' else "secondary"):
        st.session_state.current_view = 'auction'
        st.rerun()
with col5:
    if st.button("📰 Scouting", use_container_width=True, type="primary" if st.session_state.current_view == 'scouting' else "secondary"):
        st.session_state.current_view = 'scouting'
        st.rerun()

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Player Database")
    with st.expander("➕ Add New Player", expanded=False):
        category = st.selectbox("Category", ["Batsman", "Bowler", "All-rounder"], key="add_category")
        player_name = st.text_input("Player Name", key="add_player_name")
        if st.button("Add to Database", use_container_width=True):
            if player_name:
                if st.session_state.team_builder.add_player_to_database(player_name, category):
                    st.success(f"✅ Added {player_name}")
                    st.rerun()
                else:
                    st.warning("⚠️ Player already exists")
    st.divider()
    st.markdown("### 👥 All Players")
    total_db = st.session_state.team_builder.get_total_database_players()
    st.markdown(f"**Total: {total_db}**")
    
    # Manual cumulative rating override
    with st.expander("✏️ Edit Cumulative Rating", expanded=False):
        st.caption("Manually override cumulative rating (bypasses history calculation)")
        edit_cat = st.selectbox("Category", ["Batsman", "Bowler", "All-rounder"], key="edit_cum_cat")
        edit_players = list(st.session_state.team_builder.all_players[edit_cat].keys())
        if edit_players:
            edit_player = st.selectbox("Player", edit_players, key="edit_cum_player")
            current_rating = st.session_state.team_builder.all_players[edit_cat][edit_player]
            new_cum_rating = st.number_input("New Rating", min_value=0, max_value=5, value=current_rating, step=1, key="edit_cum_rating")
            if st.button("💾 Update Rating", use_container_width=True):
                st.session_state.team_builder.update_player_rating(edit_player, edit_cat, new_cum_rating)
                st.success(f"Updated {edit_player} to {new_cum_rating}")
                st.rerun()
        else:
            st.info("No players in this category")
    
    category_icons = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐"}
    rating_labels = {0: "⚪ 0", 1: "⭐ 1", 2: "⭐ 2", 3: "⭐ 3", 4: "⭐ 4", 5: "⭐ 5"}
    for cat in ["Batsman", "Bowler", "All-rounder"]:
        players = st.session_state.team_builder.all_players[cat]
        if players:
            with st.expander(f"{category_icons[cat]} {cat} ({len(players)})", expanded=False):
                for player, rating in players.items():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{player}**")
                    with col2:
                        # Ensure rating is within valid range
                        safe_rating = max(0, min(5, int(rating)))
                        new_rating = st.selectbox("Rating", options=[0, 1, 2, 3, 4, 5], index=safe_rating, format_func=lambda x: rating_labels[x], key=f"rating_{cat}_{player}", label_visibility="collapsed")
                        if new_rating != rating:
                            st.session_state.team_builder.update_player_rating(player, cat, new_rating)
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"delete_{cat}_{player}"):
                            st.session_state.team_builder.remove_player_from_database(player, cat)
                            st.session_state.team_builder.deselect_player(player, cat)
                            st.rerun()

# Main content based on current view
if st.session_state.current_view == 'rating_manager':
    # Import rating manager dependencies
    from datetime import datetime
    import pandas as pd
    
    st.markdown("## 📊 Player Rating Manager")
    
    # Top action bar
    col_info, col_clear1, col_clear2 = st.columns([4, 1, 1])
    with col_info:
        st.info("Upload match reports to automatically calculate and update player ratings")
    with col_clear1:
        if st.button("🗑️ Clear All Ratings", type="secondary", use_container_width=True):
            st.session_state.show_clear_confirm = True
    with col_clear2:
        if st.session_state.get('show_clear_confirm', False):
            if st.button("⚠️ Confirm", type="primary", use_container_width=True):
                # Clear rating history
                st.session_state.rating_system.rating_history = {}
                st.session_state.rating_system._save_rating_history()
                # Reset all player ratings to 0
                for category in ['Batsman', 'Bowler', 'All-rounder']:
                    for player_name in st.session_state.team_builder.all_players[category].keys():
                        st.session_state.team_builder.update_player_rating(player_name, category, 0)
                st.session_state.show_clear_confirm = False
                # Clear parsed data
                if 'parsed_data' in st.session_state:
                    del st.session_state.parsed_data
                st.success("✅ All rating history cleared!")
                st.rerun()
    
    # Upload section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Match Reports")
        match_date = st.date_input("Match Date", value=datetime.now())
        
        batting_pdf = st.file_uploader("Batting Leaderboard PDF", type=['pdf'], key="batting_pdf")
        bowling_pdf = st.file_uploader("Bowling Leaderboard PDF", type=['pdf'], key="bowling_pdf")
        mvp_pdf = st.file_uploader("MVP Leaderboard PDF", type=['pdf'], key="mvp_pdf")
        
        if st.button("🔍 Parse & Calculate Ratings", type="primary", use_container_width=True):
            if batting_pdf and bowling_pdf and mvp_pdf:
                with st.spinner("Parsing PDFs..."):
                    batting_df = st.session_state.rating_system.parse_batting_pdf(batting_pdf)
                    bowling_df = st.session_state.rating_system.parse_bowling_pdf(bowling_pdf)
                    mvp_df = st.session_state.rating_system.parse_mvp_pdf(mvp_pdf)
                    
                    if not batting_df.empty and not bowling_df.empty and not mvp_df.empty:
                        st.session_state.parsed_data = {
                            'date': match_date.strftime('%Y-%m-%d'),
                            'batting': batting_df,
                            'bowling': bowling_df,
                            'mvp': mvp_df
                        }
                        # Save as latest leaderboard
                        st.session_state.rating_system.save_latest_leaderboard(
                            batting_df, bowling_df, mvp_df, match_date.strftime('%Y-%m-%d')
                        )
                        st.success("✅ PDFs parsed successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to parse PDFs")
            else:
                st.warning("Please upload all 3 PDF files")
    
    with col2:
        if 'parsed_data' in st.session_state:
            st.markdown("### 📋 All Parsed Data")
            
            # Show all three tables
            st.markdown("**Batting Stats**")
            st.dataframe(st.session_state.parsed_data['batting'][['Player Name', 'Runs', 'SR', '4s', '6s']], 
                        use_container_width=True, height=200)
            
            st.markdown("**Bowling Stats**")
            st.dataframe(st.session_state.parsed_data['bowling'][['Player Name', 'Wickets', 'Econ', 'Overs']], 
                        use_container_width=True, height=200)
            
            st.markdown("**MVP Stats**")
            st.dataframe(st.session_state.parsed_data['mvp'][['Player Name', 'Total', 'Batting', 'Bowling']], 
                        use_container_width=True, height=200)
    
    # Player mapping section
    if 'parsed_data' in st.session_state:
        st.markdown("---")
        st.markdown("### 🔗 Player Name Mapping")
        
        # Check for unmatched players
        all_pdf_players = set()
        all_pdf_players.update(st.session_state.parsed_data['batting']['Player Name'].tolist())
        all_pdf_players.update(st.session_state.parsed_data['bowling']['Player Name'].tolist())
        all_pdf_players.update(st.session_state.parsed_data['mvp']['Player Name'].tolist())
        
        existing_players = set()
        for cat in ['Batsman', 'Bowler', 'All-rounder']:
            existing_players.update(st.session_state.team_builder.all_players[cat].keys())
        
        unmatched_players = all_pdf_players - existing_players
        unmapped_players = []
        
        # Check which unmatched players need mapping vs adding
        for pdf_name in unmatched_players:
            mapped_name = st.session_state.rating_system.get_mapped_name(pdf_name)
            if mapped_name not in existing_players:
                unmapped_players.append(pdf_name)
        
        if unmapped_players:
            st.warning(f"⚠️ Found {len(unmapped_players)} unmatched player(s) - Map them to existing players or add as new")
            
            for pdf_name in sorted(unmapped_players):
                col_a, col_b, col_c, col_d = st.columns([2, 2, 1, 1])
                with col_a:
                    st.markdown(f"**PDF Name: {pdf_name}**")
                with col_b:
                    # Option to map to existing player
                    all_db_players = []
                    for cat in ['Batsman', 'Bowler', 'All-rounder']:
                        all_db_players.extend(st.session_state.team_builder.all_players[cat].keys())
                    
                    map_option = st.selectbox(
                        "Map to existing or add new",
                        ["-- Add as New Player --"] + sorted(all_db_players),
                        key=f"map_{pdf_name}",
                        label_visibility="collapsed"
                    )
                with col_c:
                    if map_option != "-- Add as New Player --":
                        if st.button("🔗 Map", key=f"mapbtn_{pdf_name}"):
                            st.session_state.rating_system.add_name_mapping(pdf_name, map_option)
                            st.success(f"Mapped!")
                            st.rerun()
                with col_d:
                    if map_option == "-- Add as New Player --":
                        category = st.selectbox("Category",
                                               ["Batsman", "Bowler", "All-rounder"],
                                               key=f"cat_{pdf_name}",
                                               label_visibility="collapsed")
                        if st.button("➕ Add", key=f"add_{pdf_name}"):
                            if st.session_state.team_builder.add_player_to_database(pdf_name, category, 0):
                                st.success(f"Added!")
                                st.rerun()
        else:
            st.success("✅ All players matched!")
        
        # Show existing mappings
        if st.session_state.rating_system.name_mapping:
            st.markdown("---")
            st.markdown("**Current Name Mappings:**")
            for pdf_name, db_name in st.session_state.rating_system.name_mapping.items():
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.markdown(f"📄 **{pdf_name}**")
                with col2:
                    st.markdown(f"→ 💾 **{db_name}**")
                with col3:
                    if st.button("🗑️", key=f"delmap_{pdf_name}"):
                        st.session_state.rating_system.remove_name_mapping(pdf_name)
                        st.success("Removed!")
                        st.rerun()
    
    # Apply ratings section
    if 'parsed_data' in st.session_state:
        st.markdown("---")
        st.markdown("### ⭐ Apply Ratings")
        
        all_players = st.session_state.team_builder.all_players
        parsed_data = st.session_state.parsed_data
        
        rating_updates = []
        
        for category in ['Batsman', 'Bowler', 'All-rounder']:
            if all_players[category]:
                st.markdown(f"#### {category}s")
                
                for player_name in all_players[category].keys():
                    # Get PDF name for this player
                    pdf_name = player_name
                    for pdf_n, db_n in st.session_state.rating_system.name_mapping.items():
                        if db_n == player_name:
                            pdf_name = pdf_n
                            break
                    
                    batting_rating, bat_stats = st.session_state.rating_system.calculate_batting_rating(
                        parsed_data['batting'], pdf_name
                    )
                    bowling_rating, bowl_stats = st.session_state.rating_system.calculate_bowling_rating(
                        parsed_data['bowling'], pdf_name
                    )
                    
                    # Get MVP score
                    mvp_score = 0
                    if pdf_name in parsed_data['mvp']['Player Name'].values:
                        mvp_row = parsed_data['mvp'][parsed_data['mvp']['Player Name'] == pdf_name].iloc[0]
                        mvp_score = (float(mvp_row['Total']) / parsed_data['mvp']['Total'].max()) * 5
                    
                    new_rating = st.session_state.rating_system.calculate_overall_rating(
                        batting_rating, bowling_rating, mvp_score, category
                    )
                    
                    cumulative_rating = st.session_state.rating_system.get_cumulative_rating(player_name)
                    current_rating = all_players[category][player_name]
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{player_name}**")
                        # Show rating breakdown
                        if category == 'Batsman':
                            details = f"🏏 Bat: {batting_rating} | R:{bat_stats.get('runs',0)} SR:{bat_stats.get('sr',0):.1f} 6s:{bat_stats.get('sixes',0)}"
                        elif category == 'Bowler':
                            details = f"⚾ Bowl: {bowling_rating} | W:{bowl_stats.get('wickets',0)} Econ:{bowl_stats.get('economy',0):.1f}"
                        else:  # All-rounder
                            details = f"🏏 {batting_rating} ⚾ {bowling_rating} ⭐ {mvp_score:.1f} | R:{bat_stats.get('runs',0)} W:{bowl_stats.get('wickets',0)}"
                        st.caption(details)
                    with col2:
                        st.markdown(f"Current: **{current_rating}**")
                    with col3:
                        st.markdown(f"New: **{new_rating}**")
                    with col4:
                        # Edit option for new rating
                        edited_rating = st.number_input(
                            "Edit",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(new_rating),
                            step=0.1,
                            key=f"edit_rating_{category}_{player_name}",
                            label_visibility="collapsed"
                        )
                    with col5:
                        st.markdown(f"Cumulative: **{cumulative_rating}**")
                    with col6:
                        if st.button("Apply", key=f"apply_{category}_{player_name}"):
                            # Add to history with edited rating
                            st.session_state.rating_system.add_rating_entry(
                                player_name, category, parsed_data['date'],
                                batting_rating, bowling_rating, edited_rating,
                                {**bat_stats, **bowl_stats}
                            )
                            # Update player rating with cumulative
                            new_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                            st.session_state.team_builder.update_player_rating(
                                player_name, category, int(round(new_cumulative))
                            )
                            # Redirect to Team Builder
                            st.session_state.current_view = 'team_builder'
                            st.success(f"✅ Updated {player_name} - Redirecting to Team Builder...")
                            st.rerun()
                    
                    rating_updates.append({
                        'player': player_name,
                        'category': category,
                        'pdf_name': pdf_name,
                        'edited_rating': edited_rating
                    })
        
        # Apply all button
        st.markdown("---")
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("✅ Apply All Ratings", type="primary", use_container_width=True):
                for update in rating_updates:
                    # Skip players not in the PDF (absent on match day)
                    pdf_name = update['pdf_name']
                    in_batting = pdf_name in parsed_data['batting']['Player Name'].values
                    in_bowling = pdf_name in parsed_data['bowling']['Player Name'].values
                    in_mvp = pdf_name in parsed_data['mvp']['Player Name'].values
                    if not in_batting and not in_bowling and not in_mvp:
                        continue

                    batting_rating, bat_stats = st.session_state.rating_system.calculate_batting_rating(
                        parsed_data['batting'], update['pdf_name']
                    )
                    bowling_rating, bowl_stats = st.session_state.rating_system.calculate_bowling_rating(
                        parsed_data['bowling'], update['pdf_name']
                    )
                    
                    # Use edited rating
                    st.session_state.rating_system.add_rating_entry(
                        update['player'], update['category'], parsed_data['date'],
                        batting_rating, bowling_rating, update['edited_rating'],
                        {**bat_stats, **bowl_stats}
                    )
                    
                    new_cumulative = st.session_state.rating_system.get_cumulative_rating(update['player'])
                    st.session_state.team_builder.update_player_rating(
                        update['player'], update['category'], int(round(new_cumulative))
                    )
                
                # Redirect to Team Builder
                st.session_state.current_view = 'team_builder'
                st.success("✅ All ratings updated! Redirecting to Team Builder...")
                st.rerun()
    
    # Manual Rating Edit Section
    st.markdown("---")
    st.markdown("### ✏️ Manual Rating Override")
    st.info("Directly set a player's final rating (this overrides automatic calculation from match history)")
    
    all_players = st.session_state.team_builder.all_players
    
    # Create a table-like view for all players
    for category in ['Batsman', 'Bowler', 'All-rounder']:
        if all_players[category]:
            st.markdown(f"#### {category}s")
            
            for player_name in all_players[category].keys():
                current_rating = all_players[category][player_name]
                cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                history = st.session_state.rating_system.get_player_history(player_name)
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{player_name}**")
                    if history:
                        st.caption(f"📊 {len(history)} matches | Auto-calculated: {cumulative}")
                    else:
                        st.caption(f"No match history")
                with col2:
                    st.markdown(f"Current: **{current_rating}**")
                with col3:
                    manual_rating = st.number_input(
                        "Set Rating",
                        min_value=0,
                        max_value=5,
                        value=int(current_rating),
                        step=1,
                        key=f"manual_{category}_{player_name}",
                        label_visibility="collapsed"
                    )
                with col4:
                    if manual_rating != current_rating:
                        if st.button("💾 Save", key=f"save_manual_{category}_{player_name}"):
                            st.session_state.team_builder.update_player_rating(player_name, category, manual_rating)
                            st.success(f"✅ Updated {player_name} to {manual_rating}")
                            st.rerun()
                    else:
                        # Show button to sync with cumulative
                        if history and cumulative != current_rating:
                            if st.button("🔄 Auto", key=f"auto_{category}_{player_name}", help="Use auto-calculated rating from history"):
                                st.session_state.team_builder.update_player_rating(player_name, category, int(round(cumulative)))
                                st.success(f"✅ Set to auto-calculated: {int(round(cumulative))}")
                                st.rerun()
    
    # Rating History Section
    st.markdown("---")
    st.markdown("### 📜 Rating History")
    
    # Show rating history for all players
    all_players = st.session_state.team_builder.all_players
    has_history = False
    
    for category in ['Batsman', 'Bowler', 'All-rounder']:
        if all_players[category]:
            for player_name in all_players[category].keys():
                history = st.session_state.rating_system.get_player_history(player_name)
                if history:
                    has_history = True
                    break
            if has_history:
                break
    
    if has_history:
        for category in ['Batsman', 'Bowler', 'All-rounder']:
            if all_players[category]:
                players_with_history = []
                for player_name in all_players[category].keys():
                    history = st.session_state.rating_system.get_player_history(player_name)
                    if history:
                        players_with_history.append(player_name)
                
                if players_with_history:
                    st.markdown(f"#### {category}s")
                    
                    for player_name in players_with_history:
                        history = st.session_state.rating_system.get_player_history(player_name)
                        current_rating = all_players[category][player_name]
                        cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                        
                        with st.expander(f"{player_name} - Current: {current_rating} | Cumulative: {cumulative} | History: {len(history)} matches"):
                            for idx, entry in enumerate(history):
                                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                                
                                with col1:
                                    st.markdown(f"**📅 {entry['date']}**")
                                with col2:
                                    st.markdown(f"Rating: **{entry['overall_rating']}**")
                                with col3:
                                    if entry.get('stats'):
                                        stats = entry['stats']
                                        st.caption(f"R:{stats.get('runs',0)} 6s:{stats.get('sixes',0)}")
                                with col4:
                                    if entry.get('stats'):
                                        stats = entry['stats']
                                        st.caption(f"W:{stats.get('wickets',0)} Econ:{stats.get('economy',0):.1f}")
                                with col5:
                                    if st.button("🗑️", key=f"del_history_{player_name}_{idx}"):
                                        st.session_state.rating_system.delete_rating_entry(player_name, idx)
                                        # Recalculate cumulative
                                        new_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                                        st.session_state.team_builder.update_player_rating(
                                            player_name, category, int(round(new_cumulative))
                                        )
                                        st.success("Deleted!")
                                        st.rerun()
    else:
        st.info("No rating history yet. Upload PDFs and apply ratings to build history.")

elif st.session_state.current_view == 'leaderboard':
    # Leaderboard Dashboard View - Compact Design
    leaderboard_data = st.session_state.rating_system.get_latest_leaderboard()
    
    if leaderboard_data:
        # Compact header
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); 
                 padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                <h2 style="color: white; margin: 0; font-size: 1.5rem;">🏆 Latest Match Leaderboard</h2>
                <p style="color: rgba(255,255,255,0.9); margin: 3px 0 0 0; font-size: 0.9rem;">📅 {leaderboard_data['date']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Three columns for compact view
        col1, col2, col3 = st.columns(3)
        
        # Top 5 Batsmen (Compact)
        with col1:
            st.markdown("### 🏏 Top Batsmen")
            if leaderboard_data['batting']:
                batting_data = leaderboard_data['batting']
                batting_sorted = sorted(batting_data, key=lambda x: x.get('Runs', 0), reverse=True)[:5]
                
                for idx, player in enumerate(batting_sorted, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    
                    st.markdown(f"""
                        <div style="background: white; padding: 10px; border-radius: 8px; margin: 5px 0; 
                             box-shadow: 0 2px 4px rgba(0,0,0,0.08); border-left: 4px solid #14b8a6;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 1.5rem;">{medal}</span>
                                <div style="flex: 1;">
                                    <strong style="color: #1e293b; font-size: 0.95rem;">{player.get('Player Name', 'Unknown')}</strong>
                                    <div style="color: #64748b; font-size: 0.75rem; margin-top: 3px;">
                                        {player.get('Runs', 0)}R • SR:{player.get('SR', 0):.0f} • 6s:{player.get('6s', 0)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data")
        
        # Top 5 Bowlers (Compact)
        with col2:
            st.markdown("### ⚡ Top Bowlers")
            if leaderboard_data['bowling']:
                bowling_data = leaderboard_data['bowling']
                bowling_sorted = sorted(bowling_data, key=lambda x: x.get('Wickets', 0), reverse=True)[:5]
                
                for idx, player in enumerate(bowling_sorted, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    
                    st.markdown(f"""
                        <div style="background: white; padding: 10px; border-radius: 8px; margin: 5px 0; 
                             box-shadow: 0 2px 4px rgba(0,0,0,0.08); border-left: 4px solid #3b82f6;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 1.5rem;">{medal}</span>
                                <div style="flex: 1;">
                                    <strong style="color: #1e293b; font-size: 0.95rem;">{player.get('Player Name', 'Unknown')}</strong>
                                    <div style="color: #64748b; font-size: 0.75rem; margin-top: 3px;">
                                        {player.get('Wickets', 0)}W • Econ:{player.get('Econ', 0):.1f} • {player.get('Overs', 0):.1f}Ov
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data")
        
        # Top 5 MVP (Compact)
        with col3:
            st.markdown("### ⭐ Top MVP")
            if leaderboard_data['mvp']:
                mvp_data = leaderboard_data['mvp']
                mvp_sorted = sorted(mvp_data, key=lambda x: x.get('Total', 0), reverse=True)[:5]
                
                for idx, player in enumerate(mvp_sorted, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    
                    st.markdown(f"""
                        <div style="background: white; padding: 10px; border-radius: 8px; margin: 5px 0; 
                             box-shadow: 0 2px 4px rgba(0,0,0,0.08); border-left: 4px solid #f59e0b;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 1.5rem;">{medal}</span>
                                <div style="flex: 1;">
                                    <strong style="color: #1e293b; font-size: 0.95rem;">{player.get('Player Name', 'Unknown')}</strong>
                                    <div style="color: #64748b; font-size: 0.75rem; margin-top: 3px;">
                                        Total:{player.get('Total', 0)} • Bat:{player.get('Batting', 0)} • Bowl:{player.get('Bowling', 0)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data")
    else:
        st.markdown("""
            <div style="text-align: center; padding: 80px 20px;">
                <div style="font-size: 4rem; margin-bottom: 15px;">📤</div>
                <h2 style="color: #64748b; margin-bottom: 8px;">No Leaderboard Data Yet</h2>
                <p style="color: #94a3b8; font-size: 1rem;">Upload match reports in Rating Manager to see top performers!</p>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 'auction':
    am = st.session_state.auction_manager
    all_db_players = st.session_state.team_builder.all_players

    if not am.is_active():
        # ===== AUCTION SETUP =====
        st.markdown("""
            <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
                 padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <h2 style="color: white; margin: 0; font-size: 1.8rem;">🔨 Auction Setup</h2>
                <p style="color: rgba(255,255,255,0.85); margin: 5px 0 0 0;">Configure teams, budgets, and auction rounds</p>
            </div>
        """, unsafe_allow_html=True)

        # Team & Budget Config
        st.markdown("### ⚙️ Configuration")
        cfg_col1, cfg_col2, cfg_col3, cfg_col4 = st.columns(4)
        with cfg_col1:
            num_teams = st.number_input("Number of Teams", min_value=2, max_value=10,
                                        value=am.data["config"]["num_teams"], key="auc_num_teams")
        with cfg_col2:
            squad_size = st.number_input("Squad Size per Team", min_value=2, max_value=20,
                                         value=am.data["config"]["squad_size"], key="auc_squad_size")
        with cfg_col3:
            budget = st.number_input("Budget per Team (points)", min_value=100, max_value=1000000,
                                     value=am.data["config"]["budget_per_team"], step=1000, key="auc_budget")
        with cfg_col4:
            bid_increment = st.number_input("Bid Increment (points)", min_value=10, max_value=10000,
                                            value=am.data["config"].get("bid_increment", 50), step=10, key="auc_bid_inc")

        # Team Names & Captains
        st.markdown("### 🏷️ Teams & Captains")
        current_teams = am.data["config"]["teams"]
        current_captains = am.get_captains()
        while len(current_teams) < num_teams:
            current_teams.append(f"Team {len(current_teams) + 1}")
        team_names = []
        captain_names = {}
        t_cols = st.columns(min(num_teams, 4))
        for i in range(num_teams):
            with t_cols[i % 4]:
                default_name = current_teams[i] if i < len(current_teams) else f"Team {i+1}"
                name = st.text_input(f"Team {i+1}", value=default_name, key=f"auc_team_name_{i}")
                team_names.append(name)
                cap_default = current_captains.get(default_name, "")
                cap = st.text_input(f"👑 Captain", value=cap_default, key=f"auc_captain_{i}",
                                    placeholder="Captain name")
                if cap.strip():
                    captain_names[name] = cap.strip()

        if st.button("💾 Save Configuration", type="primary", key="save_auc_config"):
            am.update_config(num_teams, squad_size, budget, bid_increment, team_names)
            for team, cap in captain_names.items():
                am.set_captain(team, cap)
            # Clear captains for teams without one
            for team in team_names:
                if team not in captain_names:
                    am.set_captain(team, "")
            st.success("Configuration saved!")
            st.rerun()

        st.markdown("---")

        # Auction Rounds
        st.markdown("### 🎯 Auction Rounds")
        st.caption("Create rounds and assign players. All players in a round are shown on screen together. Any team can buy multiple players per round.")

        # Get all players from database (flat list)
        all_players_flat = []
        for cat in ["Batsman", "Bowler", "All-rounder"]:
            for player in all_db_players[cat].keys():
                all_players_flat.append({"name": player, "category": cat})

        already_assigned = am.get_all_assigned_players()

        # Show existing rounds
        rounds = am.get_rounds()
        for r_idx, r in enumerate(rounds):
            max_cap = r.get('max_bid_per_player', 0)
            cap_text = f" | Max Bid: {max_cap:,}" if max_cap > 0 else " | No cap"
            with st.expander(f"Round {r_idx + 1}: {r['name']} — Base: {r['base_price']:,}{cap_text} — {len(r['players'])} players", expanded=False):
                st.markdown(f"**Players in this round:**")
                for p in r["players"]:
                    st.markdown(f"- {p['name']} ({p['category']})")
                if st.button(f"🗑️ Delete Round", key=f"del_round_{r_idx}"):
                    am.delete_round(r_idx)
                    st.rerun()

        # Add new round
        st.markdown("#### ➕ Add New Round")
        ar_col1, ar_col2, ar_col3 = st.columns(3)
        with ar_col1:
            round_name = st.text_input("Round Name", value="", placeholder="e.g. Elite All-rounders", key="new_round_name")
        with ar_col2:
            base_price = st.number_input("Base Price (points)", min_value=0, max_value=100000,
                                         value=1000, step=100, key="new_round_base")
        with ar_col3:
            max_bid_player = st.number_input("Max Bid per Player", min_value=0, max_value=1000000,
                                              value=51000, step=1000, key="new_round_max_bid",
                                              help="Maximum amount any team can bid on a single player in this round. Set 0 for no limit.")

        # Player selection for this round — show available (not yet assigned)
        available_for_round = [p for p in all_players_flat if p["name"] not in already_assigned]
        if available_for_round:
            player_options = [f"{p['name']} ({p['category']})" for p in available_for_round]
            selected_display = st.multiselect("Select Players for this Round", player_options, key="new_round_players")
            selected_players = [available_for_round[player_options.index(d)] for d in selected_display]
        else:
            selected_players = []
            st.info("All players are assigned to rounds")

        if st.button("➕ Add Round", type="primary", key="add_round_btn"):
            if round_name and selected_players:
                am.add_round(round_name, base_price, max_bid_player, selected_players)
                st.success(f"Added round: {round_name} with {len(selected_players)} players")
                st.rerun()
            else:
                st.warning("Enter a round name and select at least one player")

        # Start Auction button
        st.markdown("---")
        total_round_players = sum(len(r["players"]) for r in am.get_rounds())
        st.markdown(f"**Total players in rounds: {total_round_players}** | **Rounds: {len(am.get_rounds())}**")

        col_start, col_reset = st.columns(2)
        with col_start:
            if st.button("🚀 Start Auction", type="primary", use_container_width=True, key="start_auction_btn"):
                if am.get_rounds():
                    am.start_auction()
                    st.rerun()
                else:
                    st.warning("Add at least one round before starting")
        with col_reset:
            if st.button("🔄 Reset All Rounds", use_container_width=True, key="reset_rounds_btn"):
                am.data["config"]["rounds"] = []
                am._save()
                st.rerun()

    else:
        # ===== LIVE AUCTION =====
        current_round = am.get_current_round()
        rounds = am.get_rounds()
        round_idx = am.get_current_round_idx()
        teams = am.get_teams()
        budget = am.get_budget()

        if round_idx >= len(rounds):
            # Auction complete
            st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                     padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                    <h2 style="color: white; margin: 0;">🎉 Auction Complete!</h2>
                </div>
            """, unsafe_allow_html=True)

            summary = am.get_auction_summary()
            team_colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6"]

            s_cols = st.columns(len(teams))
            for idx, team in enumerate(teams):
                info = summary[team]
                color = team_colors[idx % len(team_colors)]
                with s_cols[idx]:
                    st.markdown(f"""
                        <div style="background: white; border-radius: 12px; padding: 16px;
                             border-top: 4px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                            <h3 style="color: {color}; text-align: center; margin: 0 0 8px 0;">{team}</h3>
                            <p style="text-align: center; color: #64748b; margin: 0;">
                                {info['count']} players | Spent: {info['spent']} | Left: {info['remaining']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    for p in info["squad"]:
                        cat_icon = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐", "Captain": "👑"}.get(p["category"], "")
                        bid_text = f"{p['bid']:,} pts" if p["bid"] > 0 else "Captain"
                        st.markdown(f"""
                            <div style="background: #f8fafc; padding: 8px 12px; border-radius: 8px;
                                 margin: 4px 0; border-left: 3px solid {color}; font-size: 0.95rem;">
                                {cat_icon} {p['name']} — <span style="color: {color}; font-weight: 600;">{bid_text}</span>
                            </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                if st.button("💾 Save & Finish Auction", type="primary", use_container_width=True, key="finish_auc"):
                    am.finish_auction()
                    st.success("Auction saved to history!")
                    st.rerun()
            with fc2:
                if st.button("↩️ Undo Last Sale", use_container_width=True, key="undo_final"):
                    ok, msg = am.undo_last_sale()
                    if ok:
                        st.success(msg)
                    else:
                        st.warning(msg)
                    st.rerun()
            with fc3:
                if st.button("🔄 Reset Auction", use_container_width=True, key="reset_auc"):
                    am.reset_auction()
                    st.rerun()

        else:
            # Active round
            r = current_round
            round_max_cap = r.get('max_bid_per_player', 0)
            cap_display = f" | Max Bid: {round_max_cap:,}" if round_max_cap > 0 else ""
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
                     padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                    <h2 style="color: white; margin: 0; font-size: 1.6rem;">🔨 Live Auction</h2>
                    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 1.1rem;">
                        Round {round_idx + 1} of {len(rounds)}: <strong>{r['name']}</strong> — Base: {r['base_price']:,} pts{cap_display}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Team budget dashboard with max bid indicator
            team_colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6"]
            round_cap = r.get("max_bid_per_player", 0)
            round_cap_text = f" | Round Cap: {round_cap:,}" if round_cap > 0 else ""
            b_cols = st.columns(len(teams))
            for idx, team in enumerate(teams):
                remaining = am.get_team_budget_remaining(team)
                spent = am.data["state"]["team_spent"].get(team, 0)
                squad_count = len(am.get_team_squad(team))
                slots_left = am.get_remaining_slots(team)
                max_bid = am.get_max_bid(team, round_idx)
                bid_status = am.get_team_bid_status(team, round_idx)
                color = team_colors[idx % len(team_colors)]
                pct = (remaining / budget * 100) if budget > 0 else 0
                # Status message
                if bid_status["status"] == "no_budget":
                    status_html = f'<p style="margin:4px 0 0 0;background:#fef2f2;color:#dc2626;padding:4px 8px;border-radius:6px;font-size:0.8rem;font-weight:700;">❌ No budget remaining</p>'
                elif bid_status["status"] == "base_only":
                    status_html = f'<p style="margin:4px 0 0 0;background:#fffbeb;color:#d97706;padding:4px 8px;border-radius:6px;font-size:0.8rem;font-weight:700;">⚠️ Can only bid at base price</p>'
                else:
                    status_html = f'<p style="margin:4px 0 0 0;font-size:0.8rem;"><span style="color:#059669;font-weight:700;">Max bid: {max_bid:,}</span></p>'
                with b_cols[idx]:
                    st.markdown(f"""
                        <div style="background: white; border-radius: 10px; padding: 12px;
                             border-top: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;">
                            <h4 style="color: {color}; margin: 0 0 6px 0; font-size: 1rem;">{team}</h4>
                            <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #1e293b;">{remaining:,} pts</p>
                            <div style="background: #e2e8f0; border-radius: 4px; height: 6px; margin: 6px 0;">
                                <div style="background: {color}; width: {pct}%; height: 100%; border-radius: 4px;"></div>
                            </div>
                            <p style="margin: 0; color: #64748b; font-size: 0.8rem;">{squad_count} players | Spent: {spent:,}</p>
                            <p style="margin: 2px 0 0 0; color: #ef4444; font-size: 0.8rem; font-weight: 600;">Need {slots_left} more</p>
                            {status_html}
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("")

            # === SPINNER SECTION ===
            import random, json as json_mod

            # Collect rounds with unsold players
            rounds_with_unsold = []
            for ri, rd in enumerate(rounds):
                unsold_count = len([p for p in rd["players"] if not am.get_player_sold_info(p["name"])])
                if unsold_count > 0:
                    rounds_with_unsold.append({"idx": ri, "name": rd["name"], "unsold": unsold_count})

            # Spinner wheel HTML/JS generator
            def make_wheel_html(items, wheel_id, title, size=360):
                if not items:
                    return f"<p style='text-align:center;color:#94a3b8;'>No items to spin</p>"
                # If only 1 item, duplicate it so wheel looks proper (result is always that item)
                display_items = items if len(items) > 1 else items + items
                colors = ["#ef4444","#3b82f6","#10b981","#f59e0b","#8b5cf6","#06b6d4","#ec4899","#14b8a6",
                          "#f97316","#84cc16","#a855f7","#22d3ee"]
                segments = json_mod.dumps(display_items)
                original_items = json_mod.dumps(items)
                seg_colors = json_mod.dumps([colors[i % len(colors)] for i in range(len(display_items))])
                font_size = max(11, min(16, 180 // len(display_items)))
                max_chars = max(12, min(20, 200 // len(display_items)))
                return f"""
                <div id="{wheel_id}_container" style="text-align:center;padding:8px 0;">
                    <div style="background:linear-gradient(135deg,#1e293b,#334155);border-radius:12px;
                         padding:16px;display:inline-block;">
                        <h3 style="color:white;margin:0 0 12px 0;font-size:1.1rem;">{title}</h3>
                        <canvas id="{wheel_id}" width="{size}" height="{size}" style="display:block;margin:0 auto;"></canvas>
                        <button id="{wheel_id}_btn" onclick="spin_{wheel_id}()"
                            style="background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border:none;
                            border-radius:25px;padding:12px 40px;font-size:1.15rem;font-weight:700;cursor:pointer;
                            margin:14px 0 6px 0;box-shadow:0 4px 12px rgba(245,158,11,0.4);letter-spacing:1px;">
                            🎰 SPIN!
                        </button>
                        <div id="{wheel_id}_result" style="font-size:1.3rem;font-weight:800;color:#f59e0b;
                             margin-top:8px;min-height:36px;"></div>
                    </div>
                </div>
                <script>
                (function() {{
                    const canvas = document.getElementById('{wheel_id}');
                    const ctx = canvas.getContext('2d');
                    const items = {segments};
                    const origItems = {original_items};
                    const colors = {seg_colors};
                    const n = items.length;
                    const arc = 2 * Math.PI / n;
                    const size = {size};
                    const center = size / 2;
                    const radius = center - 8;
                    let angle = 0;
                    let spinning = false;

                    function drawWheel(a) {{
                        ctx.clearRect(0, 0, size, size);
                        // Outer ring shadow
                        ctx.beginPath();
                        ctx.arc(center, center, radius + 4, 0, 2 * Math.PI);
                        ctx.fillStyle = 'rgba(0,0,0,0.15)';
                        ctx.fill();
                        for (let i = 0; i < n; i++) {{
                            const startAngle = a + i * arc;
                            ctx.beginPath();
                            ctx.moveTo(center, center);
                            ctx.arc(center, center, radius, startAngle, startAngle + arc);
                            ctx.fillStyle = colors[i];
                            ctx.fill();
                            ctx.strokeStyle = 'rgba(255,255,255,0.6)';
                            ctx.lineWidth = 2;
                            ctx.stroke();
                            // Text
                            ctx.save();
                            ctx.translate(center, center);
                            ctx.rotate(startAngle + arc / 2);
                            ctx.fillStyle = '#fff';
                            ctx.font = 'bold {font_size}px sans-serif';
                            ctx.textAlign = 'right';
                            ctx.shadowColor = 'rgba(0,0,0,0.3)';
                            ctx.shadowBlur = 2;
                            const label = items[i].length > {max_chars} ? items[i].substring(0,{max_chars - 1})+'..' : items[i];
                            ctx.fillText(label, radius - 14, 5);
                            ctx.restore();
                        }}
                        // Arrow pointer (top)
                        ctx.save();
                        ctx.shadowColor = 'rgba(0,0,0,0.3)';
                        ctx.shadowBlur = 4;
                        ctx.beginPath();
                        ctx.moveTo(center - 14, 2);
                        ctx.lineTo(center + 14, 2);
                        ctx.lineTo(center, 28);
                        ctx.fillStyle = '#ef4444';
                        ctx.fill();
                        ctx.restore();
                        // Center circle
                        ctx.beginPath();
                        ctx.arc(center, center, 22, 0, 2 * Math.PI);
                        ctx.fillStyle = '#1e293b';
                        ctx.fill();
                        ctx.strokeStyle = '#f59e0b';
                        ctx.lineWidth = 3;
                        ctx.stroke();
                        ctx.fillStyle = '#f59e0b';
                        ctx.font = 'bold 14px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🎯', center, center);
                    }}

                    drawWheel(angle);

                    window.spin_{wheel_id} = function() {{
                        if (spinning) return;
                        spinning = true;
                        document.getElementById('{wheel_id}_btn').disabled = true;
                        document.getElementById('{wheel_id}_btn').style.opacity = '0.5';
                        document.getElementById('{wheel_id}_result').textContent = '🎰 Spinning...';
                        const totalRotation = Math.random() * 360 + 1800;
                        const duration = 5000;
                        const start = performance.now();
                        const startAngle = angle;
                        function animate(now) {{
                            const elapsed = now - start;
                            const progress = Math.min(elapsed / duration, 1);
                            const ease = 1 - Math.pow(1 - progress, 4);
                            angle = startAngle + (totalRotation * Math.PI / 180) * ease;
                            drawWheel(angle);
                            if (progress < 1) {{
                                requestAnimationFrame(animate);
                            }} else {{
                                spinning = false;
                                document.getElementById('{wheel_id}_btn').disabled = false;
                                document.getElementById('{wheel_id}_btn').style.opacity = '1';
                                // Arrow is at top (270 deg = 3π/2)
                                const norm = ((3 * Math.PI / 2) - (angle % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
                                const winnerIdx = Math.floor(norm / arc) % n;
                                const winner = origItems.length === 1 ? origItems[0] : items[winnerIdx];
                                document.getElementById('{wheel_id}_result').innerHTML =
                                    '🎯 <span style="color:#10b981;font-size:1.4rem;">' + winner + '</span>';
                            }}
                        }}
                        requestAnimationFrame(animate);
                    }};
                }})();
                </script>
                """

            # Spinner UI
            st.markdown("---")
            spin_col1, spin_col2 = st.columns(2)

            with spin_col1:
                st.markdown("#### 🎰 Spin for Round")
                if rounds_with_unsold:
                    # Let user pick which rounds to include in the spin
                    all_round_labels = [f"{rd['name']} ({rd['unsold']} left)" for rd in rounds_with_unsold]
                    selected_round_labels = st.multiselect(
                        "Select rounds to include in spin:",
                        all_round_labels, default=all_round_labels, key="spin_round_filter"
                    )
                    if selected_round_labels:
                        wheel_html = make_wheel_html(selected_round_labels, "round_wheel", "🎯 Which Round?", 340)
                        components.html(wheel_html, height=520)
                    else:
                        st.warning("Select at least one round to spin")

                    # Manual override
                    round_display_opts = [f"{rd['name']}" for rd in rounds_with_unsold]
                    manual_round = st.selectbox("Or pick round manually:", round_display_opts, key="manual_round_pick")
                    picked_round_data = rounds_with_unsold[round_display_opts.index(manual_round)]
                    if st.button("✅ Use this Round", key="use_round_btn"):
                        am.data["state"]["current_round"] = picked_round_data["idx"]
                        am._save()
                        st.rerun()
                else:
                    st.success("All rounds complete!")

            with spin_col2:
                st.markdown("#### 🎰 Spin for Player")
                unsold_in_current = [p for p in r["players"] if not am.get_player_sold_info(p["name"])]
                if unsold_in_current:
                    player_labels = [f"{p['name']}" for p in unsold_in_current]
                    wheel_html = make_wheel_html(player_labels, "player_wheel", "🎯 Which Player?", 340)
                    components.html(wheel_html, height=520)
                else:
                    st.success("All players in this round are sold!")

            st.markdown("---")

            # Show all players in this round as cards
            st.markdown("#### 🎴 Players in this Round")
            cat_icons = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐"}
            cat_colors = {"Batsman": "#14b8a6", "Bowler": "#3b82f6", "All-rounder": "#f59e0b"}

            p_cols = st.columns(max(len(r["players"]), 1))
            for p_idx, player in enumerate(r["players"]):
                sold_info = am.get_player_sold_info(player["name"])
                cat_color = cat_colors.get(player["category"], "#64748b")
                cat_icon = cat_icons.get(player["category"], "")
                with p_cols[p_idx]:
                    if sold_info:
                        buyer_idx = teams.index(sold_info["team"]) if sold_info["team"] in teams else 0
                        buyer_color = team_colors[buyer_idx % len(team_colors)]
                        st.markdown(f"""
                            <div style="background: #f0fdf4; border-radius: 12px; padding: 16px;
                                 border: 2px solid #10b981; text-align: center; min-height: 160px;">
                                <p style="font-size: 1.3rem; font-weight: 700; color: #1e293b; margin: 0 0 4px 0;">
                                    {cat_icon} {player['name']}
                                </p>
                                <p style="color: {cat_color}; font-weight: 600; margin: 0 0 10px 0; font-size: 0.9rem;">
                                    {player['category']}
                                </p>
                                <p style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px;
                                   display: inline-block; font-weight: 700; font-size: 0.9rem; margin: 0 0 6px 0;">
                                    ✅ SOLD — {sold_info['bid']:,} pts
                                </p>
                                <p style="color: {buyer_color}; font-weight: 700; margin: 0; font-size: 1rem;">
                                    → {sold_info['team']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="background: white; border-radius: 12px; padding: 16px;
                                 border: 2px solid {cat_color}; text-align: center; min-height: 160px;
                                 box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                                <p style="font-size: 1.3rem; font-weight: 700; color: #1e293b; margin: 0 0 4px 0;">
                                    {cat_icon} {player['name']}
                                </p>
                                <p style="color: {cat_color}; font-weight: 600; margin: 0 0 10px 0; font-size: 0.9rem;">
                                    {player['category']}
                                </p>
                                <p style="background: {cat_color}; color: white; padding: 4px 12px; border-radius: 20px;
                                   display: inline-block; font-weight: 600; font-size: 0.85rem; margin: 0;">
                                    Base: {r['base_price']:,} pts
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

            # Bidding section — incremental bidding
            st.markdown("---")
            st.markdown("#### 💰 Bidding")

            # Live bid increment control
            inc_col1, inc_col2, inc_col3 = st.columns([2, 1, 1])
            with inc_col1:
                live_increment = st.number_input(
                    "Bid Increment (pts)", min_value=10, max_value=100000,
                    value=am.get_bid_increment(), step=10,
                    key=f"live_bid_inc_{round_idx}",
                    help="Change the bid raise amount on the fly"
                )
            with inc_col2:
                # Quick preset buttons
                preset_col_a, preset_col_b, preset_col_c = st.columns(3)
                with preset_col_a:
                    if st.button("500", key=f"inc_500_{round_idx}", use_container_width=True):
                        am.set_bid_increment(500)
                        st.rerun()
                with preset_col_b:
                    if st.button("1000", key=f"inc_1000_{round_idx}", use_container_width=True):
                        am.set_bid_increment(1000)
                        st.rerun()
                with preset_col_c:
                    if st.button("2000", key=f"inc_2000_{round_idx}", use_container_width=True):
                        am.set_bid_increment(2000)
                        st.rerun()
            with inc_col3:
                if st.button("✅ Set Increment", key=f"set_inc_{round_idx}", use_container_width=True):
                    am.set_bid_increment(live_increment)
                    st.success(f"Increment set to {live_increment:,} pts")
                    st.rerun()

            increment = am.get_bid_increment()

            unsold_in_round = [p for p in r["players"] if not am.get_player_sold_info(p["name"])]

            if unsold_in_round:
                # Select player to bid on
                player_opts = [f"{p['name']} ({p['category']})" for p in unsold_in_round]
                sel_player_display = st.selectbox("Select Player for Bidding", player_opts, key=f"bid_player_{round_idx}")
                sel_player = unsold_in_round[player_opts.index(sel_player_display)]

                # Initialize bidding state for this player
                bid_key = f"current_bid_{sel_player['name']}"
                bidder_key = f"current_bidder_{sel_player['name']}"
                if bid_key not in st.session_state:
                    st.session_state[bid_key] = r["base_price"]
                if bidder_key not in st.session_state:
                    st.session_state[bidder_key] = ""

                current_bid = st.session_state[bid_key]
                current_bidder = st.session_state[bidder_key]

                # Current bid display
                bidder_display = current_bidder if current_bidder else "No bids yet"
                bid_color = "#f59e0b" if current_bidder else "#94a3b8"
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e293b, #334155); border-radius: 12px;
                         padding: 16px; text-align: center; margin: 10px 0;">
                        <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">Current Bid</p>
                        <p style="color: #f59e0b; margin: 4px 0; font-size: 2rem; font-weight: 800;">{current_bid:,} pts</p>
                        <p style="color: {bid_color}; margin: 0; font-size: 1.1rem; font-weight: 600;">
                            🏷️ {bidder_display}
                        </p>
                        <p style="color: #64748b; margin: 6px 0 0 0; font-size: 0.8rem;">
                            Increment: +{increment} pts | Base: {r['base_price']:,} pts
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                # Team raise buttons with inline budget info
                st.markdown("**🖐️ Raise Hand — click team to bid:**")
                raise_cols = st.columns(len(teams))
                next_bid = current_bid + increment if current_bidder else current_bid
                for t_idx, team in enumerate(teams):
                    color = team_colors[t_idx % len(team_colors)]
                    team_max = am.get_max_bid(team, round_idx)
                    remaining = am.get_team_budget_remaining(team)
                    bid_status = am.get_team_bid_status(team, round_idx)
                    can_bid = next_bid <= team_max and am.get_remaining_slots(team) > 0
                    with raise_cols[t_idx]:
                        # Compact budget info above button
                        if bid_status["status"] == "no_budget":
                            st.markdown(f"""
                                <div style="background:#fef2f2;border-radius:8px;padding:6px;text-align:center;margin-bottom:4px;border:1px solid #fecaca;">
                                    <p style="margin:0;font-size:0.75rem;color:#1e293b;font-weight:600;">{team}</p>
                                    <p style="margin:0;font-size:0.7rem;color:#dc2626;font-weight:700;">❌ No budget</p>
                                </div>
                            """, unsafe_allow_html=True)
                            st.button(f"❌ {team}", key=f"raise_{team}_{round_idx}",
                                     use_container_width=True, disabled=True)
                        elif not can_bid:
                            st.markdown(f"""
                                <div style="background:#fffbeb;border-radius:8px;padding:6px;text-align:center;margin-bottom:4px;border:1px solid #fde68a;">
                                    <p style="margin:0;font-size:0.75rem;color:#1e293b;font-weight:600;">{team} — {remaining:,} pts</p>
                                    <p style="margin:0;font-size:0.7rem;color:#d97706;font-weight:700;">Max: {team_max:,} | 🚫 Limit</p>
                                </div>
                            """, unsafe_allow_html=True)
                            st.button(f"🚫 Limit reached", key=f"raise_{team}_{round_idx}",
                                     use_container_width=True, disabled=True)
                        else:
                            st.markdown(f"""
                                <div style="background:#f0fdf4;border-radius:8px;padding:6px;text-align:center;margin-bottom:4px;border:1px solid #bbf7d0;">
                                    <p style="margin:0;font-size:0.75rem;color:#1e293b;font-weight:600;">{team} — {remaining:,} pts</p>
                                    <p style="margin:0;font-size:0.7rem;color:#059669;font-weight:700;">Max bid: {team_max:,}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"🖐️ {team} ({next_bid:,} pts)", key=f"raise_{team}_{round_idx}",
                                        use_container_width=True):
                                st.session_state[bid_key] = next_bid
                                st.session_state[bidder_key] = team
                                st.rerun()

                # Sell and Reset buttons
                sell_col1, sell_col2, sell_col3 = st.columns([2, 1, 1])
                with sell_col1:
                    if current_bidder:
                        if st.button(f"🔨 SOLD to {current_bidder} for {current_bid:,} pts!", type="primary",
                                    use_container_width=True, key=f"sell_btn_{round_idx}"):
                            ok, msg = am.sell_player(sel_player["name"], sel_player["category"],
                                                     current_bidder, current_bid, round_idx)
                            if ok:
                                # Clear bid state
                                del st.session_state[bid_key]
                                del st.session_state[bidder_key]
                                st.success(f"🎉 {sel_player['name']} sold to {current_bidder} for {current_bid:,} pts!")
                            else:
                                st.error(msg)
                            st.rerun()
                    else:
                        st.button("🔨 SOLD (select a bidder first)", disabled=True,
                                 use_container_width=True, key=f"sell_btn_{round_idx}")
                with sell_col2:
                    if st.button("🔄 Reset Bid", use_container_width=True, key=f"reset_bid_{round_idx}"):
                        st.session_state[bid_key] = r["base_price"]
                        st.session_state[bidder_key] = ""
                        st.rerun()
                with sell_col3:
                    if st.button("⏭️ Unsold / Skip", use_container_width=True, key=f"skip_bid_{round_idx}"):
                        if bid_key in st.session_state:
                            del st.session_state[bid_key]
                        if bidder_key in st.session_state:
                            del st.session_state[bidder_key]
                        st.info(f"{sel_player['name']} marked unsold")
                        st.rerun()
            else:
                st.success("✅ All players in this round are sold!")

            # Live Team Formation
            st.markdown("---")
            st.markdown("#### 🏆 Team Formation (Live)")
            captains = am.get_captains()
            tf_cols = st.columns(len(teams))
            for t_idx, team in enumerate(teams):
                color = team_colors[t_idx % len(team_colors)]
                squad = am.get_team_squad(team)
                remaining = am.get_team_budget_remaining(team)
                spent = am.data["state"]["team_spent"].get(team, 0)
                # Check if captain is already in squad
                captain_name = captains.get(team, "")
                captain_in_squad = any(p.get("category") == "Captain" for p in squad)
                with tf_cols[t_idx]:
                    st.markdown(f"""
                        <div style="background: white; border-radius: 12px; padding: 14px;
                             border-top: 4px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                             margin-bottom: 8px;">
                            <h4 style="color: {color}; text-align: center; margin: 0 0 6px 0;">{team}</h4>
                            <p style="text-align: center; color: #64748b; margin: 0; font-size: 0.85rem;">
                                {len(squad) + (1 if captain_name and not captain_in_squad else 0)} players | Spent: {spent:,} | Left: {remaining:,}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Show captain first (even if not in squad data)
                    if captain_name and not captain_in_squad:
                        st.markdown(f"""
                            <div style="background: #fef3c7; padding: 8px 12px; border-radius: 8px;
                                 margin: 4px 0; border-left: 3px solid {color}; font-size: 0.9rem;">
                                👑 {captain_name}<span style="color: {color}; font-weight: 600;"> — Captain</span>
                            </div>
                        """, unsafe_allow_html=True)
                    if squad:
                        for p in squad:
                            ci = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐", "Captain": "👑"}.get(p["category"], "")
                            if p.get("category") == "Captain":
                                st.markdown(f"""
                                    <div style="background: #fef3c7; padding: 8px 12px; border-radius: 8px;
                                         margin: 4px 0; border-left: 3px solid {color}; font-size: 0.9rem;">
                                        {ci} {p['name']}<span style="color: {color}; font-weight: 600;"> — Captain</span>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                    <div style="background: #f8fafc; padding: 8px 12px; border-radius: 8px;
                                         margin: 4px 0; border-left: 3px solid {color}; font-size: 0.9rem;">
                                        {ci} {p['name']}<span style="color: {color}; font-weight: 600;"> — {p['bid']:,} pts</span>
                                    </div>
                                """, unsafe_allow_html=True)
                    elif not captain_name:
                        st.markdown(f"""
                            <div style="text-align: center; color: #94a3b8; padding: 12px; font-size: 0.9rem;">
                                No players yet
                            </div>
                        """, unsafe_allow_html=True)

            # Round navigation
            st.markdown("---")
            nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
            with nav_col1:
                if round_idx > 0:
                    if st.button("⬅️ Previous Round", use_container_width=True, key="prev_round"):
                        am.prev_round()
                        st.rerun()
            with nav_col2:
                if st.button("➡️ Next Round", use_container_width=True, type="primary", key="next_round"):
                    am.next_round()
                    st.rerun()
            with nav_col3:
                if st.button("↩️ Undo Last Sale", use_container_width=True, key="undo_sale"):
                    ok, msg = am.undo_last_sale()
                    if ok:
                        st.success(msg)
                    else:
                        st.warning(msg)
                    st.rerun()
            with nav_col4:
                if st.button("🛑 Cancel Auction", use_container_width=True, key="cancel_auc"):
                    am.reset_auction()
                    st.rerun()

    # Auction History
    history = am.get_history()
    if history:
        st.markdown("---")
        st.markdown("## 📜 Auction History")
        for h_idx, entry in enumerate(history):
            with st.expander(f"🗓️ {entry['date']}", expanded=False):
                results = entry["results"]
                h_teams = list(results["team_squads"].keys())
                h_cols = st.columns(len(h_teams))
                team_colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"]
                for t_idx, team in enumerate(h_teams):
                    color = team_colors[t_idx % len(team_colors)]
                    squad = results["team_squads"][team]
                    spent = results["team_spent"].get(team, 0)
                    with h_cols[t_idx]:
                        st.markdown(f"""
                            <div style="background: white; border-radius: 10px; padding: 12px;
                                 border-top: 3px solid {color}; text-align: center; margin-bottom: 8px;">
                                <h4 style="color: {color}; margin: 0;">{team}</h4>
                                <p style="color: #64748b; margin: 4px 0 0 0; font-size: 0.85rem;">
                                    {len(squad)} players | Spent: {spent}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        for p in squad:
                            cat_icon = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐"}.get(p["category"], "")
                            st.markdown(f"""
                                <div style="background: #f8fafc; padding: 6px 10px; border-radius: 6px;
                                     margin: 3px 0; border-left: 3px solid {color}; font-size: 0.9rem;">
                                    {cat_icon} {p['name']} — {p['bid']} pts
                                </div>
                            """, unsafe_allow_html=True)
                if st.button("🗑️ Delete", key=f"del_auc_hist_{h_idx}"):
                    am.delete_history_entry(h_idx)
                    st.rerun()

elif st.session_state.current_view == 'team_builder':
    # Team Builder View (original content)
    # Main dashboard layout
    st.markdown("## 🎯 Select Players & Generate Teams")

    # Top control bar
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    with col1:
        total_selected = st.session_state.team_builder.get_total_selected_players()
        st.markdown(f"**📋 Selected: {total_selected} players**")
    with col2:
        if st.button("✅ All", use_container_width=True, key="select_all_btn"):
            for cat in ["Batsman", "Bowler", "All-rounder"]:
                for player in st.session_state.team_builder.all_players[cat].keys():
                    if player not in st.session_state.team_builder.selected_players[cat]:
                        st.session_state.team_builder.select_player(player, cat)
            st.rerun()
    with col3:
        if st.button("❌ Clear", use_container_width=True, key="clear_all_btn"):
            st.session_state.team_builder.clear_selection()
            st.rerun()
    with col4:
        num_teams = st.number_input("Teams", min_value=2, max_value=10, value=2, key="num_teams_input", label_visibility="collapsed")
    with col5:
        if st.button("🔀 Generate Teams", type="primary", use_container_width=True, key="generate_btn"):
            if total_selected > 0:
                st.session_state.team_builder.create_teams(num_teams)
                st.session_state.teams_created = True
                st.rerun()
            else:
                st.warning("Select players first!")

    # Unified player search and selection
    category_icons = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐"}
    category_colors = {"Batsman": "#14b8a6", "Bowler": "#3b82f6", "All-rounder": "#f59e0b"}
    rating_icons = {0: "⚪", 1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "🔵"}

    # Build player list for selectbox (instant search as you type)
    all_player_list = []
    for cat in ["Batsman", "Bowler", "All-rounder"]:
        for player, rating in st.session_state.team_builder.all_players[cat].items():
            is_sel = "✅" if player in st.session_state.team_builder.selected_players[cat] else "⬜"
            safe_rating = max(0, min(5, int(rating)))
            rating_icon = rating_icons.get(safe_rating, "⚪")
            cat_icon = category_icons[cat]
            all_player_list.append((f"{is_sel} {rating_icon}{cat_icon} {player} ({cat})", player, cat))

    if all_player_list:
        player_options = ["🔍 Type to search & select/deselect player..."] + [p[0] for p in all_player_list]
        picked = st.selectbox("🔍 Search & Select Player", player_options, key="quick_player_pick")
        if picked != "🔍 Type to search & select/deselect player...":
            for display, name, cat in all_player_list:
                if display == picked:
                    if name in st.session_state.team_builder.selected_players[cat]:
                        st.session_state.team_builder.deselect_player(name, cat)
                    else:
                        st.session_state.team_builder.select_player(name, cat)
                    st.rerun()

    # Category summary cards
    sum_cols = st.columns(3)
    for col_idx, cat in enumerate(["Batsman", "Bowler", "All-rounder"]):
        sel = len(st.session_state.team_builder.selected_players[cat])
        total = len(st.session_state.team_builder.all_players[cat])
        color = category_colors[cat]
        icon = category_icons[cat]
        with sum_cols[col_idx]:
            st.markdown(f"""
                <div style="background: white; border-radius: 10px; padding: 12px 16px; 
                     border-left: 4px solid {color}; box-shadow: 0 2px 6px rgba(0,0,0,0.06); 
                     text-align: center; margin-bottom: 10px;">
                    <span style="font-size: 1.4rem;">{icon}</span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #1e293b; margin-left: 6px;">{cat}s</span>
                    <span style="font-size: 1rem; color: {color}; font-weight: 600; margin-left: 8px;">{sel} / {total}</span>
                </div>
            """, unsafe_allow_html=True)

    # Player cards grouped by category
    for cat in ["Batsman", "Bowler", "All-rounder"]:
        available_players = st.session_state.team_builder.all_players[cat]
        selected_players = st.session_state.team_builder.selected_players[cat]
        if not available_players:
            continue
        color = category_colors[cat]
        icon = category_icons[cat]
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}15, {color}08); border-radius: 10px; 
                 padding: 10px 16px 4px 16px; margin: 8px 0 4px 0; border-left: 4px solid {color};">
                <span style="font-size: 1.15rem; font-weight: 700; color: {color};">{icon} {cat}s</span>
                <span style="font-size: 0.9rem; color: #64748b; margin-left: 10px;">
                    {len(selected_players)} of {len(available_players)} selected
                </span>
            </div>
        """, unsafe_allow_html=True)
        cols = st.columns(6)
        for idx, (player, rating) in enumerate(available_players.items()):
            with cols[idx % 6]:
                is_selected = player in selected_players
                safe_rating = max(0, min(5, int(rating)))
                rating_icon = rating_icons.get(safe_rating, "⚪")
                if st.checkbox(f"{rating_icon} {player}", value=is_selected, key=f"select_{cat}_{player}"):
                    if not is_selected:
                        st.session_state.team_builder.select_player(player, cat)
                else:
                    if is_selected:
                        st.session_state.team_builder.deselect_player(player, cat)

    # Generated teams section
    if st.session_state.teams_created and st.session_state.team_builder.teams:
        st.markdown("---")
        st.markdown("## 🏆 Generated Teams")
    
        teams = st.session_state.team_builder.teams
        team_colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4"]
    
        # Finalize and reshuffle buttons
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"**{len(teams)} teams created | Adjust if needed, then finalize to save**")
        with col2:
            if st.button("🔄 Reshuffle", use_container_width=True, key="reshuffle_btn"):
                st.session_state.team_builder.create_teams(len(teams))
                st.rerun()
        with col3:
            if st.button("✅ Finalize", use_container_width=True, key="finalize_btn", type="primary"):
                if st.session_state.team_builder.finalize_teams():
                    st.success("Saved to history!")
                    st.rerun()
    
        # Display teams in table format
        st.markdown("### Teams Overview")
    
        # Create header row with dividers
        header_html = '<div style="display: flex; gap: 0; margin-bottom: 10px;">'
        for idx, team in enumerate(teams):
            team_color = team_colors[idx % len(team_colors)]
            team_rating = team.get('total_rating', 0)
            bat_rating = team.get('batsman_rating', 0)
            bowl_rating = team.get('bowler_rating', 0)
            ar_rating = team.get('allrounder_rating', 0)
        
            header_html += f'''
                <div style="flex: 1; background: white; border-radius: 8px; padding: 10px 12px; 
                     box-shadow: 0 2px 4px rgba(0,0,0,0.06); border-left: 3px solid {team_color}; 
                     margin: 0 5px;">
                    <h3 style="color: {team_color}; margin: 0 0 8px 0; font-size: 1.1rem; text-align: center;">{team['name']}</h3>
                    <p style="color: #64748b; margin: 0; font-weight: 600; font-size: 0.75rem; text-align: center;">
                        {len(team['players'])} players | Total: {team_rating}
                    </p>
                    <p style="color: #64748b; margin: 3px 0 0 0; font-weight: 600; font-size: 0.75rem; text-align: center;">
                        🏏 {bat_rating} | ⚡ {bowl_rating} | ⭐ {ar_rating}
                    </p>
                </div>
            '''
            if idx < len(teams) - 1:
                header_html += '<div style="width: 2px; background: linear-gradient(to bottom, #e2e8f0, #cbd5e1, #e2e8f0); margin: 0 5px;"></div>'
    
        header_html += '</div>'
        st.markdown(header_html, unsafe_allow_html=True)
    
        # Team name inputs (hidden but functional)
        input_cols = st.columns(len(teams))
        for idx, (col, team) in enumerate(zip(input_cols, teams)):
            with col:
                new_name = st.text_input("Team Name", value=team['name'], key=f"team_name_{idx}", label_visibility="collapsed")
                if new_name != team['name']:
                    st.session_state.team_builder.update_team_name(idx, new_name)
    
        # Find max players in any team
        max_players = max(len(team['players']) for team in teams)
    
        # Create table rows with dividers
        for player_idx in range(max_players):
            row_html = '<div style="display: flex; gap: 0; margin: 3px 0;">'
            for team_idx, team in enumerate(teams):
                team_color = team_colors[team_idx % len(team_colors)]
                if player_idx < len(team['players']):
                    player = team['players'][player_idx]
                    row_html += f'''
                        <div style="flex: 1; background: #f8fafc; color: #334155; padding: 6px 10px; 
                             border-radius: 6px; margin: 0 5px; font-weight: 500; font-size: 0.85rem; 
                             border-left: 3px solid {team_color}; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                            • {player}
                        </div>
                    '''
                else:
                    row_html += '<div style="flex: 1; margin: 0 5px;"></div>'
            
                if team_idx < len(teams) - 1:
                    row_html += '<div style="width: 2px; background: #e2e8f0; margin: 0 5px;"></div>'
        
            row_html += '</div>'
            st.markdown(row_html, unsafe_allow_html=True)
    
        # Manual adjustments
        st.markdown("---")
        st.markdown("### ⚙️ Manual Adjustments")
        
        col1, col2 = st.columns([3, 2])
        with col1:
            all_team_players = []
            for idx, team in enumerate(teams):
                for player in team['players']:
                    all_team_players.append((player, idx))
            if all_team_players:
                player_options = [f"{p[0]} (from {teams[p[1]]['name']})" for p in all_team_players]
                selected_player_idx = st.selectbox("Select Player", range(len(player_options)), format_func=lambda x: player_options[x], key="move_player_select")
                selected_player, from_team = all_team_players[selected_player_idx]
        with col2:
            team_names = [team['name'] for team in teams]
            to_team = st.selectbox("Move to Team", range(len(teams)), format_func=lambda x: team_names[x], key="move_to_team")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("↔️ Move Player", use_container_width=True, key="move_player_btn", type="primary"):
                st.session_state.team_builder.move_player(selected_player, from_team, to_team)
                st.rerun()
        with col_btn2:
            if st.button("🗑️ Remove Player", use_container_width=True, key="remove_player_btn", type="secondary"):
                st.session_state.team_builder.remove_player_from_team(selected_player, from_team)
                st.success(f"Removed {selected_player}")
                st.rerun()
    
        # Match Scheduler
        st.markdown("---")
        st.markdown("## 📅 Match Schedule Generator")
    
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            ground_hours = st.number_input("Ground Hours", min_value=1.0, max_value=8.0, value=2.0, step=0.5, key="ground_hours")
        with col2:
            match_duration = st.number_input("Match Duration (mins)", min_value=15, max_value=60, value=20, step=5, key="match_duration")
        with col3:
            start_time = st.text_input("Start Time", value="07:00 AM", key="start_time")
        with col4:
            st.write("")
            st.write("")
            if st.button("🎲 Generate Schedule", use_container_width=True, key="generate_schedule_btn", type="primary"):
                schedule = st.session_state.team_builder.generate_match_schedule(ground_hours, match_duration, start_time)
                if schedule:
                    st.session_state.match_schedule = schedule
                    st.rerun()
    
        # Display match schedule
        if 'match_schedule' in st.session_state and st.session_state.match_schedule:
            schedule = st.session_state.match_schedule
        
            st.markdown(f"### 🏏 Match Schedule ({schedule['total_matches']} matches)")
        
            # Display matches in grid (3 per row)
            matches_list = schedule['matches']
            for row_start in range(0, len(matches_list), 3):
                cols = st.columns(3)
                for col_idx, match in enumerate(matches_list[row_start:row_start+3]):
                    with cols[col_idx]:
                        officials_html = ""
                        if match['resting_teams']:
                            officials_html = f"""
                                <div style="background: #f8fafc; border-radius: 8px; padding: 12px; margin: 12px 0; border: 1px solid #e2e8f0;">
                                    <h4 style="color: #475569; margin: 0 0 10px 0; text-align: center; font-size: 0.9rem; font-weight: 600;">
                                        Match Officials
                                    </h4>
                                    <div style="display: flex; justify-content: space-around; gap: 10px;">
                                        <div style="text-align: center;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Umpire</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #1e293b; font-weight: 600;">{match.get('main_umpire', 'N/A')}</p>
                                        </div>
                                        <div style="text-align: center;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Leg Umpire</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #1e293b; font-weight: 600;">{match.get('leg_umpire', 'N/A')}</p>
                                        </div>
                                        <div style="text-align: center;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Scorer</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #1e293b; font-weight: 600;">{match.get('scorer', 'N/A')}</p>
                                        </div>
                                    </div>
                                    <p style="color: #64748b; margin: 10px 0 0 0; text-align: center; font-size: 0.75rem;">
                                        Resting: <strong>{', '.join(match['resting_teams'])}</strong>
                                    </p>
                                </div>
                            """
                    
                        card_html = f"""
                            <div style="background: white; border-radius: 12px; padding: 16px; margin: 5px 0; 
                                 box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;">
                            
                                <div style="text-align: center; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 2px solid #f1f5f9;">
                                    <h3 style="color: #1e293b; margin: 0; font-size: 1.2rem; font-weight: 700;">
                                        Match {match['match_num']}
                                    </h3>
                                    <p style="color: #64748b; margin: 4px 0 0 0; font-size: 0.8rem;">
                                        {match['time_slot']}
                                    </p>
                                </div>
                            
                                <div style="display: flex; gap: 12px; margin-bottom: 12px;">
                                    <div style="flex: 1; background: #f8fafc; border-radius: 8px; padding: 12px; border: 1px solid #e2e8f0;">
                                        <div style="background: #3b82f6; color: white; padding: 10px; border-radius: 6px; margin-bottom: 8px; text-align: center;">
                                            <strong style="font-size: 0.95rem;">{match['team1']}</strong>
                                        </div>
                                        <div style="background: #1e293b; color: white; padding: 6px; 
                                             border-radius: 50%; text-align: center; margin: 8px auto; width: 45px; font-size: 0.8rem; font-weight: 700;">
                                            VS
                                        </div>
                                        <div style="background: #10b981; color: white; padding: 10px; border-radius: 6px; text-align: center;">
                                            <strong style="font-size: 0.95rem;">{match['team2']}</strong>
                                        </div>
                                    </div>
                                    <div style="flex: 1; background: #f8fafc; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: center; border: 1px solid #e2e8f0;">
                                        <div style="margin-bottom: 8px;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Toss Winner</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.9rem; color: #14b8a6; font-weight: 700;">{match['toss_winner']}</p>
                                        </div>
                                        <div style="margin-bottom: 4px;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Batting First</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #1e293b; font-weight: 600;">{match['bats_first']}</p>
                                        </div>
                                        <div>
                                            <p style="margin: 0; font-size: 0.7rem; color: #94a3b8;">Bowling First</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #1e293b; font-weight: 600;">{match['bowls_first']}</p>
                                        </div>
                                    </div>
                                </div>
                            
                                {officials_html}
                            </div>
                        """
                        components.html(card_html, height=360, scrolling=False)

    # Team history section
    else:
        history = st.session_state.team_builder.get_recent_history(5)
        if history:
            st.markdown("---")
            st.markdown("## 📜 Recent Team History")
            for idx, entry in enumerate(history):
                with st.expander(f"🗓️ {entry['date']}", expanded=False):
                    # Create header row with dividers
                    header_html = '<div style="display: flex; gap: 0; margin-bottom: 10px;">'
                    for team_idx, team in enumerate(entry['teams']):
                        header_html += f'''
                            <div style="flex: 1; background: white; border-radius: 8px; padding: 10px 12px; 
                                 box-shadow: 0 2px 4px rgba(0,0,0,0.06); border-left: 3px solid #3b82f6; 
                                 margin: 0 5px;">
                                <p style="color: #64748b; margin: 0 0 5px 0; font-weight: 600; font-size: 0.75rem; text-align: center;">
                                    {len(team['players'])} players | Total: {team['total_rating']}
                                </p>
                                <p style="color: #64748b; margin: 0 0 8px 0; font-weight: 600; font-size: 0.75rem; text-align: center;">
                                    🏏 {team['batsman_rating']} | ⚡ {team['bowler_rating']} | ⭐ {team['allrounder_rating']}
                                </p>
                                <h4 style="color: #3b82f6; margin: 0; font-size: 1rem; text-align: center; padding-top: 8px; border-top: 1px solid #e2e8f0;">{team['name']}</h4>
                            </div>
                        '''
                        if team_idx < len(entry['teams']) - 1:
                            header_html += '<div style="width: 2px; background: linear-gradient(to bottom, #e2e8f0, #cbd5e1, #e2e8f0); margin: 0 5px;"></div>'
                
                    header_html += '</div>'
                    st.markdown(header_html, unsafe_allow_html=True)
                
                    # Find max players
                    max_players = max(len(team['players']) for team in entry['teams'])
                
                    # Create player rows with dividers
                    for player_idx in range(max_players):
                        row_html = '<div style="display: flex; gap: 0; margin: 3px 0;">'
                        for team_idx, team in enumerate(entry['teams']):
                            if player_idx < len(team['players']):
                                player = team['players'][player_idx]
                                row_html += f'''
                                    <div style="flex: 1; background: #f8fafc; color: #334155; padding: 6px 10px; 
                                         border-radius: 6px; margin: 0 5px; font-weight: 500; font-size: 0.85rem; 
                                         border-left: 3px solid #3b82f6; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                                        • {player}
                                    </div>
                                '''
                            else:
                                row_html += '<div style="flex: 1; margin: 0 5px;"></div>'
                        
                            if team_idx < len(entry['teams']) - 1:
                                row_html += '<div style="width: 2px; background: #e2e8f0; margin: 0 5px;"></div>'
                    
                        row_html += '</div>'
                        st.markdown(row_html, unsafe_allow_html=True)
                
                    col1, col2 = st.columns([5, 1])
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_history_{idx}"):
                            st.session_state.team_builder.delete_history_entry(idx)
                            st.rerun()

elif st.session_state.current_view == 'scouting':
    sm = st.session_state.scouting_manager

    st.markdown("## 📰 Pre-Tournament Scouting Report")

    scout_tab1, scout_tab2, scout_tab3, scout_tab4 = st.tabs(["⚙️ Team Config", "📊 Scouting Report", "⚔️ Compare", "🎯 Strategy"])

    # --- TAB 1: Team Configuration ---
    with scout_tab1:
        st.markdown("### ⚙️ Configure Tournament Teams")
        st.info("Set up the 4 tournament teams and assign players to each team")

        all_db_players = []
        for cat in ['Batsman', 'Bowler', 'All-rounder']:
            for p in st.session_state.team_builder.all_players[cat].keys():
                all_db_players.append(p)

        existing_teams = sm.get_teams()
        num_teams = 4

        # Collect already-assigned players to prevent duplicates
        assigned_players = set()
        team_configs = {}

        for i in range(num_teams):
            default_name = list(existing_teams.keys())[i] if i < len(existing_teams) else f"Team {i+1}"
            existing_team_data = existing_teams.get(default_name, {})
            existing_players = existing_team_data.get("players", [])
            existing_captain = existing_team_data.get("captain", "")

            st.markdown(f"---")
            tc1, tc2 = st.columns([1, 3])
            with tc1:
                team_name = st.text_input(f"Team {i+1} Name", value=default_name, key=f"scout_team_name_{i}")
            with tc2:
                # Filter out players already assigned to other teams
                available = [p for p in all_db_players if p not in assigned_players or p in existing_players]
                default_sel = [p for p in existing_players if p in available]
                selected = st.multiselect(
                    f"Players for {team_name}",
                    options=available,
                    default=default_sel,
                    key=f"scout_team_players_{i}"
                )
                for p in selected:
                    assigned_players.add(p)

            cap_options = ["-- No Captain --"] + selected
            cap_default = 0
            if existing_captain in selected:
                cap_default = cap_options.index(existing_captain)
            captain = st.selectbox(f"Captain of {team_name}", cap_options, index=cap_default, key=f"scout_captain_{i}")

            team_configs[team_name] = {
                "captain": captain if captain != "-- No Captain --" else "",
                "players": selected
            }

        if st.button("💾 Save Team Configuration", type="primary", key="save_scout_teams"):
            sm.save_teams(team_configs)
            st.success("✅ Tournament teams saved!")
            st.rerun()


    # --- TAB 2: Scouting Report ---
    with scout_tab2:
        teams = sm.get_teams()
        total_matches = sm.get_total_matches()

        if not teams:
            st.warning("⚠️ Configure tournament teams first in the Team Config tab")
        elif total_matches == 0:
            st.warning("⚠️ No match data found. Upload match reports in Rating Manager first.")
        else:
            st.markdown("### 📊 Team Scouting Report")
            st.caption(f"Based on {total_matches} match day(s) from Rating History")

            team_names = sm.get_team_names()
            selected_team = st.selectbox("🔍 Select Team to Scout", team_names, key="scout_select_team")

            if selected_team:
                team_players = sm.get_team_players(selected_team)
                team_captain = sm.get_team_captain(selected_team)

                # Team header
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e293b, #334155); border-radius: 12px;
                         padding: 20px; margin: 10px 0;">
                        <h2 style="color: white; margin: 0; text-align: center;">{selected_team}</h2>
                        <p style="color: #94a3b8; text-align: center; margin: 4px 0;">
                            👑 Captain: {team_captain if team_captain else 'Not set'} | 👥 {len(team_players)} Players | 📊 {total_matches} Matches Analyzed
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                # Team summary stats
                team_total_runs = 0
                team_total_wickets = 0
                team_total_6s = 0
                best_batter = ("", 0)
                best_bowler = ("", 0)

                for p in team_players:
                    bat = sm.get_player_batting_stats(p)
                    bowl = sm.get_player_bowling_stats(p)
                    team_total_runs += bat["total_runs"]
                    team_total_wickets += bowl["total_wickets"]
                    team_total_6s += bat["total_6s"]
                    if bat["total_runs"] > best_batter[1]:
                        best_batter = (p, bat["total_runs"])
                    if bowl["total_wickets"] > best_bowler[1]:
                        best_bowler = (p, bowl["total_wickets"])

                sum_cols = st.columns(5)
                with sum_cols[0]:
                    st.metric("Total Runs", f"{int(team_total_runs)}")
                with sum_cols[1]:
                    st.metric("Total Wickets", f"{int(team_total_wickets)}")
                with sum_cols[2]:
                    st.metric("Total 6s", f"{team_total_6s}")
                with sum_cols[3]:
                    st.metric("Top Batter", f"{best_batter[0]}", f"{int(best_batter[1])} runs")
                with sum_cols[4]:
                    st.metric("Top Bowler", f"{best_bowler[0]}", f"{int(best_bowler[1])} wkts")

                st.markdown("---")

                # Player-wise scouting cards
                st.markdown("### 👤 Player Scouting Cards")

                for p_name in team_players:
                    bat = sm.get_player_batting_stats(p_name)
                    bowl = sm.get_player_bowling_stats(p_name)
                    form_emoji, form_text = sm.get_player_form_tag(p_name)
                    strengths = sm.get_player_strengths(p_name)
                    is_captain = (p_name == team_captain)

                    # Find player category
                    p_cat = ""
                    for cat in ['Batsman', 'Bowler', 'All-rounder']:
                        if p_name in st.session_state.team_builder.all_players[cat]:
                            p_cat = cat
                            break

                    cat_icon = {"Batsman": "🏏", "Bowler": "⚡", "All-rounder": "⭐"}.get(p_cat, "🏏")
                    captain_badge = " 👑" if is_captain else ""

                    with st.expander(f"{cat_icon} {p_name}{captain_badge} — {form_emoji} {form_text}", expanded=False):
                        # Top row: key stats
                        st.markdown(f"**Role:** {p_cat} | **Form:** {form_emoji} {form_text}")

                        # Strengths
                        strength_text = " • ".join(strengths)
                        st.markdown(f"""
                            <div style="background: #f0fdf4; border-radius: 8px; padding: 10px; margin: 8px 0;
                                 border-left: 4px solid #22c55e;">
                                <p style="margin: 0; font-size: 0.9rem; color: #166534;">
                                    💪 <strong>Strengths:</strong> {strength_text}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                        # Batting stats
                        if bat["total_runs"] > 0 or bat["matches_batted"] > 0:
                            st.markdown("**🏏 Batting**")
                            bc1, bc2, bc3, bc4, bc5, bc6 = st.columns(6)
                            with bc1:
                                st.metric("Runs", int(bat["total_runs"]))
                            with bc2:
                                st.metric("Avg", bat["avg_runs"])
                            with bc3:
                                st.metric("SR", bat["avg_sr"])
                            with bc4:
                                st.metric("6s", bat["total_6s"])
                            with bc5:
                                st.metric("4s", bat["total_4s"])
                            with bc6:
                                st.metric("Highest", int(bat["highest"]))

                            # Match-by-match batting
                            if bat["match_scores"]:
                                st.markdown("**Match-by-match batting:**")
                                for ms in bat["match_scores"]:
                                    bar_width = min(int(ms["runs"] / 1.2), 100) if ms["runs"] > 0 else 2
                                    bar_color = "#22c55e" if ms["runs"] >= 30 else "#f59e0b" if ms["runs"] >= 15 else "#94a3b8"
                                    st.markdown(f"""
                                        <div style="display: flex; align-items: center; margin: 3px 0;">
                                            <span style="width: 140px; font-size: 0.8rem; color: #64748b;">{ms['date']}</span>
                                            <div style="background: {bar_color}; height: 20px; width: {bar_width}%;
                                                 border-radius: 4px; margin: 0 8px; min-width: 4px;"></div>
                                            <span style="font-size: 0.85rem; font-weight: 600;">{int(ms['runs'])} ({ms['sr']:.0f} SR)</span>
                                        </div>
                                    """, unsafe_allow_html=True)

                        # Bowling stats
                        if bowl["total_wickets"] > 0 or bowl["matches_bowled"] > 0:
                            st.markdown("**⚡ Bowling**")
                            bw1, bw2, bw3, bw4 = st.columns(4)
                            with bw1:
                                st.metric("Wickets", bowl["total_wickets"])
                            with bw2:
                                st.metric("Economy", bowl["avg_econ"])
                            with bw3:
                                st.metric("Overs", bowl["total_overs"])
                            with bw4:
                                st.metric("Best", f"{bowl['best_wickets']}W")

                            # Match-by-match bowling
                            if bowl["match_figures"]:
                                st.markdown("**Match-by-match bowling:**")
                                for mf in bowl["match_figures"]:
                                    wkt_dots = "🔴" * int(mf["wickets"])
                                    econ_color = "#22c55e" if mf["econ"] < 9 else "#f59e0b" if mf["econ"] < 14 else "#ef4444"
                                    st.markdown(f"""
                                        <div style="display: flex; align-items: center; margin: 3px 0;">
                                            <span style="width: 140px; font-size: 0.8rem; color: #64748b;">{mf['date']}</span>
                                            <span style="font-size: 0.85rem; margin: 0 8px;">{wkt_dots if wkt_dots else '—'}</span>
                                            <span style="font-size: 0.85rem; font-weight: 600;">{int(mf['wickets'])}W</span>
                                            <span style="font-size: 0.8rem; color: {econ_color}; margin-left: 12px;">Econ: {mf['econ']:.1f}</span>
                                        </div>
                                    """, unsafe_allow_html=True)



    # --- TAB 3: Compare ---
    with scout_tab3:
        teams = sm.get_teams()
        total_matches = sm.get_total_matches()

        if not teams:
            st.warning("⚠️ Configure tournament teams first in the Team Config tab")
        elif total_matches == 0:
            st.warning("⚠️ No match data found. Upload match reports in Rating Manager first.")
        else:
            st.markdown("### ⚔️ Team & Player Comparison")
            team_names = sm.get_team_names()

            compare_mode = st.radio("Compare Mode", ["🏏 Team vs Team", "👤 Player vs Player"], horizontal=True, key="compare_mode")

            if compare_mode == "🏏 Team vs Team":
                tc1, tc2 = st.columns(2)
                with tc1:
                    team_a = st.selectbox("Team A", team_names, key="compare_team_a")
                with tc2:
                    other_teams = [t for t in team_names if t != team_a]
                    team_b = st.selectbox("Team B", other_teams, key="compare_team_b")

                if team_a and team_b:
                    # Team summary comparison
                    st.markdown("---")
                    st.markdown("#### 📊 Team Overview")

                    def get_team_totals(tn):
                        players = sm.get_team_players(tn)
                        t_runs, t_wkts, t_6s, t_sr_list = 0, 0, 0, []
                        for p in players:
                            b = sm.get_player_batting_stats(p)
                            w = sm.get_player_bowling_stats(p)
                            t_runs += b["total_runs"]
                            t_wkts += w["total_wickets"]
                            t_6s += b["total_6s"]
                            if b["avg_sr"] > 0:
                                t_sr_list.append(b["avg_sr"])
                        avg_sr = sum(t_sr_list) / len(t_sr_list) if t_sr_list else 0
                        return {"runs": t_runs, "wickets": t_wkts, "6s": t_6s, "avg_sr": round(avg_sr, 1)}

                    ta = get_team_totals(team_a)
                    tb = get_team_totals(team_b)

                    # Side by side comparison bars
                    stats_to_compare = [
                        ("Total Runs", ta["runs"], tb["runs"], "🏏"),
                        ("Total Wickets", ta["wickets"], tb["wickets"], "⚡"),
                        ("Total 6s", ta["6s"], tb["6s"], "💥"),
                        ("Avg Strike Rate", ta["avg_sr"], tb["avg_sr"], "📈"),
                    ]

                    for label, val_a, val_b, icon in stats_to_compare:
                        max_val = max(val_a, val_b, 1)
                        pct_a = int(val_a / max_val * 100)
                        pct_b = int(val_b / max_val * 100)
                        color_a = "#14b8a6" if val_a >= val_b else "#94a3b8"
                        color_b = "#14b8a6" if val_b >= val_a else "#94a3b8"
                        st.markdown(f"""
                            <div style="margin: 8px 0;">
                                <p style="text-align: center; margin: 0 0 4px 0; font-weight: 600; font-size: 0.9rem; color: #475569;">
                                    {icon} {label}
                                </p>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="width: 80px; text-align: right; font-weight: 700; color: {color_a};">{val_a}</span>
                                    <div style="flex: 1; display: flex; height: 24px; border-radius: 6px; overflow: hidden; background: #f1f5f9;">
                                        <div style="width: {pct_a}%; background: {color_a}; border-radius: 6px 0 0 6px;"></div>
                                    </div>
                                    <div style="flex: 1; display: flex; height: 24px; border-radius: 6px; overflow: hidden; background: #f1f5f9; direction: rtl;">
                                        <div style="width: {pct_b}%; background: {color_b}; border-radius: 0 6px 6px 0;"></div>
                                    </div>
                                    <span style="width: 80px; font-weight: 700; color: {color_b};">{val_b}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-top: 2px;">
                                    <span style="font-size: 0.75rem; color: #64748b; margin-left: 88px;">{team_a}</span>
                                    <span style="font-size: 0.75rem; color: #64748b; margin-right: 88px;">{team_b}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    # Best player face-offs
                    st.markdown("---")
                    st.markdown("#### 🏆 Best Player Face-offs")

                    for role, role_label, role_icon in [("batsman", "Batsman", "🏏"), ("bowler", "Bowler", "⚡"), ("allrounder", "All-rounder", "⭐")]:
                        name_a, stats_a = sm.get_best_in_team(team_a, role)
                        name_b, stats_b = sm.get_best_in_team(team_b, role)

                        if name_a and name_b:
                            bat_a = stats_a["bat"]
                            bat_b = stats_b["bat"]
                            bowl_a = stats_a["bowl"]
                            bowl_b = stats_b["bowl"]
                            form_a = stats_a["form"]
                            form_b = stats_b["form"]

                            st.markdown(f"**{role_icon} Best {role_label}**")
                            fc1, fc2, fc3 = st.columns([2, 1, 2])
                            with fc1:
                                st.markdown(f"""
                                    <div style="background: white; border-radius: 10px; padding: 12px; border-left: 4px solid #14b8a6;
                                         box-shadow: 0 2px 6px rgba(0,0,0,0.06);">
                                        <p style="margin: 0; font-weight: 700; font-size: 1.1rem; color: #1e293b;">{name_a}</p>
                                        <p style="margin: 2px 0; font-size: 0.8rem; color: #64748b;">{team_a} | {form_a[0]} {form_a[1]}</p>
                                        <p style="margin: 4px 0 0 0; font-size: 0.9rem;">
                                            🏏 {int(bat_a['total_runs'])} runs (SR {bat_a['avg_sr']}) | 💥 {bat_a['total_6s']} sixes<br>
                                            ⚡ {bowl_a['total_wickets']}W (Econ {bowl_a['avg_econ']})
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)
                            with fc2:
                                st.markdown("""
                                    <div style="text-align: center; padding-top: 20px;">
                                        <p style="font-size: 1.5rem; font-weight: 800; color: #f59e0b;">VS</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            with fc3:
                                st.markdown(f"""
                                    <div style="background: white; border-radius: 10px; padding: 12px; border-right: 4px solid #f59e0b;
                                         box-shadow: 0 2px 6px rgba(0,0,0,0.06);">
                                        <p style="margin: 0; font-weight: 700; font-size: 1.1rem; color: #1e293b;">{name_b}</p>
                                        <p style="margin: 2px 0; font-size: 0.8rem; color: #64748b;">{team_b} | {form_b[0]} {form_b[1]}</p>
                                        <p style="margin: 4px 0 0 0; font-size: 0.9rem;">
                                            🏏 {int(bat_b['total_runs'])} runs (SR {bat_b['avg_sr']}) | 💥 {bat_b['total_6s']} sixes<br>
                                            ⚡ {bowl_b['total_wickets']}W (Econ {bowl_b['avg_econ']})
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)

            else:
                # Player vs Player mode
                st.markdown("---")
                st.markdown("#### 👤 Head-to-Head Player Comparison")

                ptc1, ptc2 = st.columns(2)
                with ptc1:
                    p_team_a = st.selectbox("Team A", team_names, key="p2p_team_a")
                with ptc2:
                    p_other_teams = [t for t in team_names if t != p_team_a]
                    p_team_b = st.selectbox("Team B", p_other_teams, key="p2p_team_b")

                players_a = sm.get_team_players(p_team_a)
                players_b = sm.get_team_players(p_team_b)

                pc1, pc2 = st.columns(2)
                with pc1:
                    player_a = st.selectbox(f"Player from {p_team_a}", players_a, key="compare_player_a")
                with pc2:
                    player_b = st.selectbox(f"Player from {p_team_b}", players_b, key="compare_player_b")

                p_a = player_a
                p_b = player_b

                if p_a and p_b:
                    bat_a = sm.get_player_batting_stats(p_a)
                    bat_b = sm.get_player_batting_stats(p_b)
                    bowl_a = sm.get_player_bowling_stats(p_a)
                    bowl_b = sm.get_player_bowling_stats(p_b)
                    form_a = sm.get_player_form_tag(p_a)
                    form_b = sm.get_player_form_tag(p_b)
                    str_a = sm.get_player_strengths(p_a)
                    str_b = sm.get_player_strengths(p_b)

                    # Player cards side by side
                    h2h1, h2h_mid, h2h2 = st.columns([2, 1, 2])
                    with h2h1:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #0f766e, #14b8a6); border-radius: 12px;
                                 padding: 16px; text-align: center;">
                                <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 0;">{p_a}</p>
                                <p style="color: #a7f3d0; margin: 4px 0; font-size: 0.9rem;">{form_a[0]} {form_a[1]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with h2h_mid:
                        st.markdown("""
                            <div style="text-align: center; padding-top: 10px;">
                                <p style="font-size: 2rem; font-weight: 800; color: #f59e0b;">⚔️</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with h2h2:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #b45309, #f59e0b); border-radius: 12px;
                                 padding: 16px; text-align: center;">
                                <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 0;">{p_b}</p>
                                <p style="color: #fef3c7; margin: 4px 0; font-size: 0.9rem;">{form_b[0]} {form_b[1]}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    # Stat-by-stat comparison
                    st.markdown("---")
                    h2h_stats = [
                        ("Total Runs", int(bat_a["total_runs"]), int(bat_b["total_runs"])),
                        ("Avg Runs", bat_a["avg_runs"], bat_b["avg_runs"]),
                        ("Strike Rate", bat_a["avg_sr"], bat_b["avg_sr"]),
                        ("Sixes", bat_a["total_6s"], bat_b["total_6s"]),
                        ("Fours", bat_a["total_4s"], bat_b["total_4s"]),
                        ("Highest Score", int(bat_a["highest"]), int(bat_b["highest"])),
                        ("Wickets", bowl_a["total_wickets"], bowl_b["total_wickets"]),
                        ("Economy", bowl_a["avg_econ"], bowl_b["avg_econ"]),
                        ("Overs Bowled", bowl_a["total_overs"], bowl_b["total_overs"]),
                        ("Best Bowling", bowl_a["best_wickets"], bowl_b["best_wickets"]),
                    ]

                    for stat_label, va, vb in h2h_stats:
                        # For economy, lower is better
                        if stat_label == "Economy":
                            better_a = va < vb if va > 0 and vb > 0 else va > 0
                            better_b = vb < va if va > 0 and vb > 0 else vb > 0
                        else:
                            better_a = va > vb
                            better_b = vb > va

                        color_a = "#14b8a6" if better_a else "#94a3b8"
                        color_b = "#f59e0b" if better_b else "#94a3b8"
                        weight_a = "700" if better_a else "400"
                        weight_b = "700" if better_b else "400"

                        st.markdown(f"""
                            <div style="display: flex; align-items: center; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
                                <span style="flex: 1; text-align: right; font-size: 1rem; font-weight: {weight_a}; color: {color_a};">
                                    {va}
                                </span>
                                <span style="width: 160px; text-align: center; font-size: 0.85rem; color: #64748b; font-weight: 600;">
                                    {stat_label}
                                </span>
                                <span style="flex: 1; text-align: left; font-size: 1rem; font-weight: {weight_b}; color: {color_b};">
                                    {vb}
                                </span>
                            </div>
                        """, unsafe_allow_html=True)

                    # Strengths comparison
                    st.markdown("---")
                    st.markdown("#### 💪 Strengths")
                    str_c1, str_c2 = st.columns(2)
                    with str_c1:
                        for s in str_a:
                            st.markdown(f"✅ {s}")
                    with str_c2:
                        for s in str_b:
                            st.markdown(f"✅ {s}")

    # --- TAB 4: Strategy ---
    with scout_tab4:
        teams = sm.get_teams()
        total_matches = sm.get_total_matches()

        if not teams:
            st.warning("⚠️ Configure tournament teams first in the Team Config tab")
        elif total_matches == 0:
            st.warning("⚠️ No match data found. Upload match reports in Rating Manager first.")
        else:
            st.markdown("### 🎯 Match Strategy Generator")
            st.caption("Get data-driven winning strategies against any opponent")

            team_names = sm.get_team_names()

            strat_c1, strat_c2 = st.columns(2)
            with strat_c1:
                my_team = st.selectbox("🏏 My Team", team_names, key="strat_my_team")
            with strat_c2:
                opp_options = [t for t in team_names if t != my_team]
                opponent_team = st.selectbox("⚔️ Opponent Team", opp_options, key="strat_opp_team")

            if my_team and opponent_team:
                strategy = sm.generate_strategy(my_team, opponent_team)

                # Summary card
                if strategy["summary"]:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1e293b, #334155); border-radius: 12px;
                             padding: 20px; margin: 16px 0;">
                            <p style="color: #fbbf24; font-size: 0.85rem; font-weight: 600; margin: 0 0 6px 0; text-transform: uppercase;">
                                🎯 Game Plan
                            </p>
                            <p style="color: white; font-size: 1.15rem; font-weight: 700; margin: 0;">
                                {strategy['summary']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                # Key Matchups
                if strategy["matchups"]:
                    st.markdown("#### ⚔️ Key Match-ups")
                    for mu in strategy["matchups"]:
                        st.markdown(f"""
                            <div style="background: white; border-radius: 10px; padding: 14px; margin: 8px 0;
                                 box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                                <p style="text-align: center; color: #64748b; font-size: 0.8rem; margin: 0 0 8px 0;">
                                    {mu['label']}
                                </p>
                                <div style="display: flex; align-items: center; justify-content: space-between;">
                                    <div style="flex: 1; text-align: center;">
                                        <p style="margin: 0; font-weight: 700; color: #14b8a6; font-size: 1.05rem;">{mu['my']}</p>
                                        <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #64748b;">{mu['my_stat']}</p>
                                    </div>
                                    <div style="padding: 0 12px;">
                                        <span style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">VS</span>
                                    </div>
                                    <div style="flex: 1; text-align: center;">
                                        <p style="margin: 0; font-weight: 700; color: #ef4444; font-size: 1.05rem;">{mu['opp']}</p>
                                        <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #64748b;">{mu['opp_stat']}</p>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

                strat_left, strat_right = st.columns(2)

                # Batting Strategy
                with strat_left:
                    st.markdown("#### 🏏 Batting Strategy")
                    if strategy["batting_tips"]:
                        for tip in strategy["batting_tips"]:
                            st.markdown(f"""
                                <div style="background: #f0fdf4; border-radius: 8px; padding: 10px; margin: 6px 0;
                                     border-left: 4px solid #22c55e;">
                                    <p style="margin: 0; font-size: 0.9rem; color: #166534;">{tip}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific batting tips — not enough opponent bowling data")

                    # Target bowlers
                    if strategy["target_bowlers"]:
                        st.markdown("##### 🎯 Target These Bowlers")
                        for tb in strategy["target_bowlers"]:
                            st.markdown(f"""
                                <div style="background: #fef3c7; border-radius: 8px; padding: 8px 12px; margin: 4px 0;
                                     border-left: 4px solid #f59e0b;">
                                    <p style="margin: 0; font-size: 0.9rem; color: #92400e;">
                                        🎯 {tb['name']} — Econ: {tb['bowl']['avg_econ']} | {tb['bowl']['total_wickets']}W in {tb['bowl']['total_overs']} ov
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)

                    # Careful against
                    if strategy["careful_bowlers"]:
                        st.markdown("##### 🛡️ Be Careful Against")
                        for cb in strategy["careful_bowlers"]:
                            st.markdown(f"""
                                <div style="background: #fef2f2; border-radius: 8px; padding: 8px 12px; margin: 4px 0;
                                     border-left: 4px solid #ef4444;">
                                    <p style="margin: 0; font-size: 0.9rem; color: #991b1b;">
                                        ⚠️ {cb['name']} — Econ: {cb['bowl']['avg_econ']} | {cb['bowl']['total_wickets']}W
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)

                # Bowling Strategy
                with strat_right:
                    st.markdown("#### ⚡ Bowling Strategy")
                    if strategy["bowling_tips"]:
                        for tip in strategy["bowling_tips"]:
                            st.markdown(f"""
                                <div style="background: #eff6ff; border-radius: 8px; padding: 10px; margin: 6px 0;
                                     border-left: 4px solid #3b82f6;">
                                    <p style="margin: 0; font-size: 0.9rem; color: #1e40af;">{tip}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific bowling tips — not enough opponent batting data")

                    # Danger batsmen
                    if strategy["danger_batsmen"]:
                        st.markdown("##### 🔥 Danger Batsmen")
                        for db in strategy["danger_batsmen"][:4]:
                            form_emoji, form_text = db["form"]
                            runs = int(db["bat"]["total_runs"])
                            sr = db["bat"]["avg_sr"]
                            sixes = db["bat"]["total_6s"]
                            threat_color = "#ef4444" if runs > 50 else "#f59e0b" if runs > 20 else "#94a3b8"
                            st.markdown(f"""
                                <div style="background: white; border-radius: 8px; padding: 8px 12px; margin: 4px 0;
                                     border-left: 4px solid {threat_color}; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                    <p style="margin: 0; font-size: 0.9rem; color: #1e293b; font-weight: 600;">
                                        {db['name']} {form_emoji}
                                    </p>
                                    <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #64748b;">
                                        {runs} runs | SR {sr} | {sixes} sixes | {form_text}
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
