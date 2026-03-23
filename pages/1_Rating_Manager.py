import streamlit as st
import sys
sys.path.append('..')
from rating_system import RatingSystem
from team_builder import TeamBuilder
from datetime import datetime

st.set_page_config(page_title="Rating Manager", page_icon="📊", layout="wide")

# Initialize
if 'rating_system' not in st.session_state:
    st.session_state.rating_system = RatingSystem()
if 'team_builder' not in st.session_state:
    st.session_state.team_builder = TeamBuilder()

st.title("📊 Player Rating Manager")

# Tab navigation
tab1, tab2, tab3 = st.tabs(["📤 Upload Reports", "⭐ View Ratings", "📈 Rating History"])

# Tab 1: Upload Reports
with tab1:
    st.markdown("## 📤 Upload Match Reports")
    st.info("Upload batting, bowling, and MVP leaderboard PDFs to automatically calculate player ratings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        match_date = st.date_input("Match Date", value=datetime.now())
        
        st.markdown("### Upload PDFs")
        batting_pdf = st.file_uploader("Batting Leaderboard PDF", type=['pdf'], key="batting_pdf")
        bowling_pdf = st.file_uploader("Bowling Leaderboard PDF", type=['pdf'], key="bowling_pdf")
        mvp_pdf = st.file_uploader("MVP Leaderboard PDF", type=['pdf'], key="mvp_pdf")
        
        if st.button("🔍 Parse & Calculate Ratings", type="primary", width="stretch"):
            if batting_pdf and bowling_pdf and mvp_pdf:
                with st.spinner("Parsing PDFs..."):
                    # Parse PDFs
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
                        st.success("✅ PDFs parsed successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to parse PDFs. Please check the format.")
            else:
                st.warning("Please upload all 3 PDF files")
    
    with col2:
        if 'parsed_data' in st.session_state:
            st.markdown("### 📋 Parsed Data Preview")
            
            with st.expander("Batting Stats", expanded=True):
                st.dataframe(st.session_state.parsed_data['batting'][['Player Name', 'Runs', 'SR', '4s', '6s']].head(10))
            
            with st.expander("Bowling Stats"):
                st.dataframe(st.session_state.parsed_data['bowling'][['Player Name', 'Wickets', 'Econ', 'Overs']].head(10))
            
            with st.expander("MVP Stats"):
                st.dataframe(st.session_state.parsed_data['mvp'][['Player Name', 'Total', 'Batting', 'Bowling']].head(10))
            
            # Check for unmatched players
            all_pdf_players = set()
            all_pdf_players.update(st.session_state.parsed_data['batting']['Player Name'].tolist())
            all_pdf_players.update(st.session_state.parsed_data['bowling']['Player Name'].tolist())
            all_pdf_players.update(st.session_state.parsed_data['mvp']['Player Name'].tolist())
            
            existing_players = set()
            for cat in ['Batsman', 'Bowler', 'All-rounder']:
                existing_players.update(st.session_state.team_builder.all_players[cat].keys())
            
            unmatched_players = all_pdf_players - existing_players
            
            if unmatched_players:
                st.markdown("---")
                st.warning(f"⚠️ Found {len(unmatched_players)} player(s) not in database")
                
                with st.expander("➕ Add New Players", expanded=True):
                    for player in sorted(unmatched_players):
                        col_a, col_b, col_c = st.columns([3, 2, 1])
                        with col_a:
                            st.markdown(f"**{player}**")
                        with col_b:
                            category = st.selectbox("Category", 
                                                   ["Batsman", "Bowler", "All-rounder"],
                                                   key=f"cat_{player}",
                                                   label_visibility="collapsed")
                        with col_c:
                            if st.button("Add", key=f"add_{player}"):
                                if st.session_state.team_builder.add_player_to_database(player, category, 0):
                                    st.success(f"Added {player}")
                                    st.rerun()
                    
                    st.markdown("---")
                    if st.button("🔄 Refresh After Adding", type="primary", width="stretch"):
                        st.rerun()

# Tab 2: View & Apply Ratings
with tab2:
    st.markdown("## ⭐ Calculate & Apply Ratings")
    
    if 'parsed_data' in st.session_state:
        all_players = st.session_state.team_builder.all_players
        parsed_data = st.session_state.parsed_data
        
        st.markdown(f"### Match Date: {parsed_data['date']}")
        
        # Calculate ratings for all players
        rating_updates = []
        
        for category in ['Batsman', 'Bowler', 'All-rounder']:
            if all_players[category]:
                st.markdown(f"### {category}s")
                
                for player_name in all_players[category].keys():
                    # Calculate new rating
                    batting_rating, bat_stats = st.session_state.rating_system.calculate_batting_rating(
                        parsed_data['batting'], player_name
                    )
                    bowling_rating, bowl_stats = st.session_state.rating_system.calculate_bowling_rating(
                        parsed_data['bowling'], player_name
                    )
                    
                    # Get MVP score
                    mvp_score = 0
                    if player_name in parsed_data['mvp']['Player Name'].values:
                        mvp_row = parsed_data['mvp'][parsed_data['mvp']['Player Name'] == player_name].iloc[0]
                        mvp_score = (float(mvp_row['Total']) / parsed_data['mvp']['Total'].max()) * 5
                    
                    new_rating = st.session_state.rating_system.calculate_overall_rating(
                        batting_rating, bowling_rating, mvp_score, category
                    )
                    
                    # Get current cumulative rating (from history only)
                    old_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                    
                    # Calculate what cumulative WILL BE after adding this new rating
                    # Simulate adding the new entry temporarily
                    history = st.session_state.rating_system.get_player_history(player_name)
                    temp_entries = history + [{'overall_rating': new_rating}]
                    
                    # Calculate new cumulative with the new rating included
                    total_weight = 0
                    weighted_sum = 0
                    for idx, entry in enumerate(reversed(temp_entries)):
                        weight = 1.0 / (idx + 1)
                        weighted_sum += entry['overall_rating'] * weight
                        total_weight += weight
                    
                    new_cumulative = round(min(weighted_sum / total_weight if total_weight > 0 else new_rating, 5.0), 1)
                    
                    current_rating = all_players[category][player_name]
                    
                    # Debug info
                    debug_info = f"Hist:{len(history)} New:{new_rating} Weights:{weighted_sum:.2f}/{total_weight:.2f}"
                    
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{player_name}**")
                        st.caption(debug_info)
                    with col2:
                        st.markdown(f"Current: **{current_rating}**")
                    with col3:
                        st.markdown(f"New: **{new_rating}**")
                    with col4:
                        st.markdown(f"Cumulative: **{new_cumulative}**")
                    with col5:
                        if st.button("Apply", key=f"apply_{category}_{player_name}"):
                            # Add to history
                            st.session_state.rating_system.add_rating_entry(
                                player_name, category, parsed_data['date'],
                                batting_rating, bowling_rating, new_rating,
                                {**bat_stats, **bowl_stats}
                            )
                            # Update player rating with new cumulative
                            final_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                            st.session_state.team_builder.update_player_rating(
                                player_name, category, int(round(final_cumulative))
                            )
                            st.success(f"Updated {player_name}")
                            st.rerun()
                    
                    rating_updates.append({
                        'player': player_name,
                        'category': category,
                        'current': current_rating,
                        'new': new_rating,
                        'cumulative': new_cumulative
                    })
        
        st.markdown("---")
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("✅ Apply All", type="primary", width="stretch"):
                for update in rating_updates:
                    # Add to history
                    batting_rating, bat_stats = st.session_state.rating_system.calculate_batting_rating(
                        parsed_data['batting'], update['player']
                    )
                    bowling_rating, bowl_stats = st.session_state.rating_system.calculate_bowling_rating(
                        parsed_data['bowling'], update['player']
                    )
                    st.session_state.rating_system.add_rating_entry(
                        update['player'], update['category'], parsed_data['date'],
                        batting_rating, bowling_rating, update['new'],
                        {**bat_stats, **bowl_stats}
                    )
                    # Update with cumulative
                    new_cumulative = st.session_state.rating_system.get_cumulative_rating(update['player'])
                    st.session_state.team_builder.update_player_rating(
                        update['player'], update['category'], int(round(new_cumulative))
                    )
                st.success("All ratings updated!")
                st.rerun()
    else:
        st.info("👆 Upload PDFs in the 'Upload Reports' tab to calculate ratings")

# Tab 3: Rating History
with tab3:
    st.markdown("## 📈 Rating History")
    
    all_players = st.session_state.team_builder.all_players
    
    for category in ['Batsman', 'Bowler', 'All-rounder']:
        if all_players[category]:
            st.markdown(f"### {category}s")
            
            for player_name in all_players[category].keys():
                history = st.session_state.rating_system.get_player_history(player_name)
                current_rating = all_players[category][player_name]
                cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                
                with st.expander(f"{player_name} - Current: {current_rating} | Cumulative: {cumulative}"):
                    if history:
                        for idx, entry in enumerate(history):
                            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{entry['date']}**")
                            with col2:
                                st.markdown(f"Rating: **{entry['overall_rating']}**")
                            with col3:
                                new_rating = st.number_input("Edit", value=entry['overall_rating'], 
                                                            min_value=0.0, max_value=5.0, step=0.1,
                                                            key=f"edit_{player_name}_{idx}",
                                                            label_visibility="collapsed")
                            with col4:
                                if new_rating != entry['overall_rating']:
                                    if st.button("💾", key=f"save_{player_name}_{idx}"):
                                        st.session_state.rating_system.update_rating_entry(player_name, idx, new_rating)
                                        # Recalculate and update cumulative
                                        new_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                                        st.session_state.team_builder.update_player_rating(
                                            player_name, category, int(round(new_cumulative))
                                        )
                                        st.success("Updated!")
                                        st.rerun()
                            with col5:
                                if st.button("🗑️", key=f"del_{player_name}_{idx}"):
                                    st.session_state.rating_system.delete_rating_entry(player_name, idx)
                                    # Recalculate and update cumulative
                                    new_cumulative = st.session_state.rating_system.get_cumulative_rating(player_name)
                                    st.session_state.team_builder.update_player_rating(
                                        player_name, category, int(round(new_cumulative))
                                    )
                                    st.success("Deleted!")
                                    st.rerun()
                            with col6:
                                if entry.get('stats'):
                                    stats = entry['stats']
                                    st.caption(f"R:{stats.get('runs',0)} 6s:{stats.get('sixes',0)} W:{stats.get('wickets',0)}")
                    else:
                        st.info("No rating history yet")
