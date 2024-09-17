import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import sys
import io
import logging
import difflib
import requests
from re import findall
from io import StringIO

###################
##### Sidebar #####
###################
st.sidebar.image('ffa_red.png', use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center;'>Read This!</h1>", unsafe_allow_html=True)
st.sidebar.markdown("* Click Fullscreen at the bottom for a better user experience")
st.sidebar.markdown("* This is the simplest version of a trade calculator. It evaluates the trade in a vacuum, not taking into account the strengths and weaknesses of your team.")
st.sidebar.markdown("* If you play on [Sleeper](https://www.thefantasyfootballadvice.com/sleeper-league-trade-calculator) or [ESPN](https://www.thefantasyfootballadvice.com/espn-trade-calculator/) then please use those specific trade calculators, as they're able to access your exact team and will thus be more accurate.")
st.sidebar.markdown("* If you do not play on those platforms, then use this calculator and just think about the strengths and weaknesses of your team.")
st.sidebar.markdown("* The stronger you already are at a position, then the better the trade needs to be for you in order for it to increase the strength of your team.")
st.sidebar.markdown("* Conversely, if you're really weak at a position, then you should be willing to accept a less favorable trade if it means you're getting help where you need it most.")
st.sidebar.markdown("* When in doubt you can always ask about your specific trade in the trades channel of our [FREE Discord](https://www.thefantasyfootballadvice.com/join-the-discord)")

st.markdown("<h3 style='text-align: center;'>Click Fullscreen at the bottom for a better user experience!</h3>", unsafe_allow_html=True)

dynasty = st.toggle("Is this a Dynasty League?")
if dynasty:
    st.write("You've selected the dynasty trade calculator!")

    scoring = st.selectbox(
        "What type of Dynasty League is this?",
        ('1 QB', 'SuperFlex', 'Tight End Premium', 'SuperFlex & Tight End Premium'))

    # GitHub raw URL for the CSV file
    github_csv_url = 'https://raw.githubusercontent.com/nzylakffa/sleepercalc/main/All%20Dynasty%20Rankings.csv'

    # Read the CSV file into a DataFrame
    ros = pd.read_csv(github_csv_url)

    # Rename Columns
    ros = ros.rename(columns={'Player': 'Player Name',
                              'TEP': 'Tight End Premium',
                              'SF TEP': 'SuperFlex & Tight End Premium',
                              'SF': 'SuperFlex',
                              'Position': 'Pos'})

    # Create a df with pick values
    pick_values = ros[ros['Pos'] == 'Draft']
    # st.dataframe(pick_values)

    # Replace defense names
    replace_dict = {'Ravens D/ST': 'BAL D/ST', 'Cowboys D/ST': 'DAL D/ST', 'Bills D/ST': 'BUF D/ST', 'Jets D/ST': 'NYJ D/ST', 'Dolphins D/ST': 'MIA D/ST',
                    'Browns D/ST': 'CLE D/ST', 'Raiders D/ST': 'LVR D/ST', 'Saints D/ST': 'NO D/ST', '49ers D/ST': 'SF D/ST', 'Colts D/ST': 'IND D/ST',
                    'Steelers D/ST': 'PIT D/ST', 'Bucs D/ST': 'TB D/ST', 'Chiefs D/ST': 'KC D/ST', 'Texans D/ST': 'HOU D/ST', 'Giants D/ST': 'NYG D/ST',
                    'Vikings D/ST': 'MIN D/ST', 'Jaguars D/ST': 'JAX D/ST', 'Bengals D/ST': 'CIN D/ST', 'Bears D/ST': 'CHI D/ST', 'Broncos D/ST': 'DEN D/ST',
                    'Packers D/ST': 'GB D/ST', 'Chargers D/ST': 'LAC D/ST', 'Lions D/ST': 'DET D/ST', 'Seahawks D/ST': 'SEA D/ST', 'Patriots D/ST': 'NE D/ST',
                    'Falcons D/ST': 'ATL D/ST', 'Eagles D/ST': 'PHI D/ST', 'Titans D/ST': 'TEN D/ST', 'Rams D/ST': 'LAR D/ST', 'Panthers D/ST': 'NE D/ST',
                    'Cardinals D/ST': 'ARI D/ST', 'Commanders D/ST': 'WAS D/ST'}
    
    ros['Player Name'] = ros['Player Name'].replace(replace_dict)

    ##########################################

    # Make a drop down for what each side is getting
    trading_away = st.multiselect(
        "Player's & Picks You're Trading AWAY",
        ros['Player Name'])

    trading_for = st.multiselect(
        "Player's & Picks You're Trading FOR",
        ros['Player Name'])
    
    value_trading_away = sum(ros[ros['Player Name'].isin(trading_away)][scoring])
    value_trading_for = sum(ros[ros['Player Name'].isin(trading_for)][scoring])
    trade_diff = value_trading_for - value_trading_away
    
    # Is it a good or bad trade?
    if trade_diff == 0:
        st.subheader(f":gray[This is a perfectly even trade!]")
    elif trade_diff > 15:
        st.subheader(f":green[You are winning this trade by a lot!]")
        st.subheader(f"Value Gained in this Trade: +{trade_diff}")
    elif trade_diff > 10:
        st.subheader(f":green[You are winning this trade!]")
        st.subheader(f"Value Gained in this Trade: +{trade_diff}")
    elif trade_diff >  5:
        st.subheader(f":green[You are winning this trade by a small amount!]")
        st.subheader(f"Value Gained in this Trade: +{trade_diff}")
    elif trade_diff > 0:
        st.subheader(f":green[You are winning this trade by a very small amount]")
        st.subheader(f"Value Gained in this Trade: +{trade_diff}")
    elif trade_diff >  -5:
        st.subheader(f":red[You are losing this trade by a very small amount]")
        st.subheader(f"Value Gained in this Trade: {trade_diff}")
    elif trade_diff > - 10:
        st.subheader(f":red[You are losing this trade by a small amount]")
        st.subheader(f"Value Gained in this Trade: {trade_diff}")
    elif trade_diff > - 15:
        st.subheader(f":red[You are losing this trade!]")
        st.subheader(f"Value Gained in this Trade: {trade_diff}")
    else:
        st.subheader(f":red[You are losing this trade by a lot!]")
        st.subheader(f"Value Gained in this Trade: {trade_diff}")
        
        
else:
    st.write("You've selected the redraft trade calculator!")

    scoring = st.selectbox(
        "Input your league's scoring format",
        ('PPR', 'HPPR', 'Std', '1.5 TE', '6 Pt Pass'))
    
    teams = st.number_input("How many teams are in your league?", step=1, value=12)
        
    qbs = st.number_input("How many starting QB spots are there?", step=1, value=1)
    rbs = st.number_input("How many starting RB spots are there?", step=1, value=2)
    wrs = st.number_input("How many starting WR spots are there?", step=1, value=2)
    tes = st.number_input("How many starting TE spots are there?", step=1, value=1)
    dst = st.number_input("How many starting DST spots are there?", step=1, value=1)
    k = st.number_input("How many starting K spots are there?", step=1, value=1)
    flex = st.number_input("How many starting FLEX spots are there (NOT SuperFlex)?", step=1, value=1)
    sf = st.number_input("How many starting SuperFlex spots are there?", step=1, value=0)
    bench = st.number_input("How many bench players are on a roster?", step=1, value=6)

    
    
    # Calculate the factors based on the given formulas
    def get_rank_index(pos, teams, sf, qbs, rbs, wrs, tes, flex):
        if pos == 'QB':
            return round(teams * sf * 0.75 + teams * qbs * 0.75)
        elif pos == 'RB':
            return round(teams * sf * 0.1 + teams * rbs + teams * flex * 0.4)
        elif pos == 'WR':
            return round(teams * sf * 0.1 + teams * wrs + teams * flex * 0.5)
        elif pos == 'TE':
            return round(teams * sf * 0.05 + teams * tes * 0.5 + teams * flex * 0.1)
        else:
            return None  # DST and K don't use the rank index for this calculation
    
    # Function to calculate value
    def calculate_value(row, df, scoring_column, teams, sf, qbs, rbs, wrs, tes, flex):
        pos = row['Pos']
        games = row['Games']
        score = row[scoring]

        # Ensure that rank_index is a valid number
        rank_index = get_rank_index(pos, teams, sf, qbs, rbs, wrs, tes, flex)
        if rank_index is None:
            return np.nan  # Return NaN if rank_index couldn't be determined

        if pos in ['DST', 'K']:
            # For DST and K, factor is calculated differently
            factor_score = 1.2 * df[df['Pos'] == pos][scoring].max()
        else:
            # Sort the scores in descending order and reset index
            sorted_scores = df[df['Pos'] == pos][scoring].sort_values(ascending=False).reset_index(drop=True)
            # Ensure the rank_index does not exceed the number of players
            if rank_index - 1 >= len(sorted_scores):
                # If there are not enough players to get the rank_index score, use the last player's score
                factor_score = sorted_scores.iloc[-1]
            else:
                # Use the score of the player at rank_index position
                factor_score = sorted_scores.iloc[rank_index - 1]  # rank_index is 1-based, while indices are 0-based

        # Calculate the value and return it
        value = (score - factor_score) / games if games else np.nan
        return value

    # GitHub raw URL for the CSV file
    github_csv_url = 'https://raw.githubusercontent.com/nzylakffa/sleepercalc/main/ROS%20Rankings%20for%20trade%20calc.csv'

    # Read the CSV file into a DataFrame
    ros = pd.read_csv(github_csv_url)

    # Keep these columns of ros
    ros = ros[["Player Name", "Team", "Pos", "PPR", "HPPR", "Std", "1.5 TE", "6 Pt Pass", "DK"]]

    # Replace defense names
    replace_dict = {'Ravens D/ST': 'BAL D/ST', 'Cowboys D/ST': 'DAL D/ST', 'Bills D/ST': 'BUF D/ST', 'Jets D/ST': 'NYJ D/ST', 'Dolphins D/ST': 'MIA D/ST',
                    'Browns D/ST': 'CLE D/ST', 'Raiders D/ST': 'LVR D/ST', 'Saints D/ST': 'NO D/ST', '49ers D/ST': 'SF D/ST', 'Colts D/ST': 'IND D/ST',
                    'Steelers D/ST': 'PIT D/ST', 'Bucs D/ST': 'TB D/ST', 'Chiefs D/ST': 'KC D/ST', 'Texans D/ST': 'HOU D/ST', 'Giants D/ST': 'NYG D/ST',
                    'Vikings D/ST': 'MIN D/ST', 'Jaguars D/ST': 'JAX D/ST', 'Bengals D/ST': 'CIN D/ST', 'Bears D/ST': 'CHI D/ST', 'Broncos D/ST': 'DEN D/ST',
                    'Packers D/ST': 'GB D/ST', 'Chargers D/ST': 'LAC D/ST', 'Lions D/ST': 'DET D/ST', 'Seahawks D/ST': 'SEA D/ST', 'Patriots D/ST': 'NE D/ST',
                    'Falcons D/ST': 'ATL D/ST', 'Eagles D/ST': 'PHI D/ST', 'Titans D/ST': 'TEN D/ST', 'Rams D/ST': 'LAR D/ST', 'Panthers D/ST': 'NE D/ST',
                    'Cardinals D/ST': 'ARI D/ST', 'Commanders D/ST': 'WAS D/ST'}
    ros['Player Name'] = ros['Player Name'].replace(replace_dict)    
    

    # Apply the function to create the new 'Value' column
    ros['Value'] = ros.apply(calculate_value, args=(ros, scoring, teams, sf, qbs, rbs, wrs, tes, flex), axis=1)
    ros = ros.sort_values(by = "Value", ascending=False)
    ros['Rank'] = range(1, len(ros) + 1)   
    ros = ros[["Rank", "Player Name", "Pos", scoring, "Value"]]
    
    # Calculate value of top 20 bench players
    fa_rank_1 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams), 'Value'].iloc[0]
    fa_rank_2 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+1, 'Value'].iloc[0] + fa_rank_1
    fa_rank_3 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+2, 'Value'].iloc[0] + fa_rank_2
    fa_rank_4 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+3, 'Value'].iloc[0] + fa_rank_3
    fa_rank_5 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+4, 'Value'].iloc[0] + fa_rank_4
    fa_rank_6 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+5, 'Value'].iloc[0] + fa_rank_5
    fa_rank_7 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+6, 'Value'].iloc[0] + fa_rank_6
    fa_rank_8 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+7, 'Value'].iloc[0] + fa_rank_7
    fa_rank_9 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+8, 'Value'].iloc[0] + fa_rank_8
    fa_rank_10 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+9, 'Value'].iloc[0] + fa_rank_9
    fa_rank_11 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+10, 'Value'].iloc[0] + fa_rank_10
    fa_rank_12 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+11, 'Value'].iloc[0] + fa_rank_11
    fa_rank_13 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+12, 'Value'].iloc[0] + fa_rank_12
    fa_rank_14 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+13, 'Value'].iloc[0] + fa_rank_13
    fa_rank_15 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+14, 'Value'].iloc[0] + fa_rank_14
    fa_rank_16 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+15, 'Value'].iloc[0] + fa_rank_15
    fa_rank_17 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+16, 'Value'].iloc[0] + fa_rank_16
    fa_rank_18 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+17, 'Value'].iloc[0] + fa_rank_17
    fa_rank_19 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+18, 'Value'].iloc[0] + fa_rank_18
    fa_rank_20 = ros.loc[ros['Rank'] == ((qbs + rbs + wrs + tes + dst + k + flex + sf + bench)*teams)+19, 'Value'].iloc[0] + fa_rank_19
    
    # Make a drop down for what each side is getting
    trading_away = st.multiselect(
        "Player's You're Trading AWAY",
        ros['Player Name'])

    trading_for = st.multiselect(
        "Player's You're Trading FOR",
        ros['Player Name'])
    
    acq_diff = len(trading_for) - len(trading_away)
    
    value_trading_away = sum(ros[ros['Player Name'].isin(trading_away)]["Value"])
    value_trading_for = sum(ros[ros['Player Name'].isin(trading_for)]["Value"])
    
    # Calculate what the value difference should be
    if acq_diff == 0:
        trade_diff = value_trading_for - value_trading_away
    elif acq_diff == 1:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_1)
    elif acq_diff == 2:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_2)
    elif acq_diff == 3:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_3)
    elif acq_diff == 4:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_4)
    elif acq_diff == 5:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_5)
    elif acq_diff == 6:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_6)
    elif acq_diff == 7:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_7)
    elif acq_diff == 8:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_8)
    elif acq_diff == 9:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_9)
    elif acq_diff == 10:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_10)
    elif acq_diff == 11:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_11)
    elif acq_diff == 12:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_12)
    elif acq_diff == 13:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_13)
    elif acq_diff == 14:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_14)
    elif acq_diff == 15:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_15)
    elif acq_diff == 16:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_16)
    elif acq_diff == 17:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_17)
    elif acq_diff == 18:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_18)
    elif acq_diff == 19:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_19)
    elif acq_diff == 20:
        trade_diff = value_trading_for - (value_trading_away + fa_rank_20)
    elif acq_diff == -1:
        trade_diff = (value_trading_for + fa_rank_1) - (value_trading_away)
    elif acq_diff == -2:
        trade_diff = (value_trading_for + fa_rank_2) - (value_trading_away)
    elif acq_diff == -3:
        trade_diff = (value_trading_for + fa_rank_3) - (value_trading_away)
    elif acq_diff == -4:
        trade_diff = (value_trading_for + fa_rank_4) - (value_trading_away)
    elif acq_diff == -5:
        trade_diff = (value_trading_for + fa_rank_5) - (value_trading_away)
    elif acq_diff == -6:
        trade_diff = (value_trading_for + fa_rank_6) - (value_trading_away)
    elif acq_diff == -7:
        trade_diff = (value_trading_for + fa_rank_7) - (value_trading_away)
    elif acq_diff == -8:
        trade_diff = (value_trading_for + fa_rank_8) - (value_trading_away)
    elif acq_diff == -9:
        trade_diff = (value_trading_for + fa_rank_9) - (value_trading_away)
    elif acq_diff == -10:
        trade_diff = (value_trading_for + fa_rank_10) - (value_trading_away)
    elif acq_diff == -11:
        trade_diff = (value_trading_for + fa_rank_11) - (value_trading_away)
    elif acq_diff == -12:
        trade_diff = (value_trading_for + fa_rank_12) - (value_trading_away)
    elif acq_diff == -13:
        trade_diff = (value_trading_for + fa_rank_13) - (value_trading_away)
    elif acq_diff == -14:
        trade_diff = (value_trading_for + fa_rank_14) - (value_trading_away)
    elif acq_diff == -15:
        trade_diff = (value_trading_for + fa_rank_15) - (value_trading_away)
    elif acq_diff == -16:
        trade_diff = (value_trading_for + fa_rank_16) - (value_trading_away)
    elif acq_diff == -17:
        trade_diff = (value_trading_for + fa_rank_17) - (value_trading_away)
    elif acq_diff == -18:
        trade_diff = (value_trading_for + fa_rank_18) - (value_trading_away)
    elif acq_diff == -19:
        trade_diff = (value_trading_for + fa_rank_19) - (value_trading_away)
    elif acq_diff == -20:
        trade_diff = (value_trading_for + fa_rank_20) - (value_trading_away)
    
    # Is it a good or bad trade?
    if trade_diff == 0:
        st.subheader(f":gray[This is a perfectly even trade!]")
    elif trade_diff > 10:
        st.subheader(f":green[You are winning this trade by a lot!]")
        st.subheader(f"Value Gained in this Trade: +{round(trade_diff,1)}")
    elif trade_diff > 5:
        st.subheader(f":green[You are winning this trade!]")
        st.subheader(f"Value Gained in this Trade: +{round(trade_diff,1)}")
    elif trade_diff >  2:
        st.subheader(f":green[You are winning this trade by a small amount!]")
        st.subheader(f"Value Gained in this Trade: +{round(trade_diff,1)}")
    elif trade_diff > 0:
        st.subheader(f":green[You are winning this trade by a very small amount]")
        st.subheader(f"Value Gained in this Trade: +{round(trade_diff,1)}")
    elif trade_diff >  -2:
        st.subheader(f":red[You are losing this trade by a very small amount]")
        st.subheader(f"Value Gained in this Trade: {round(trade_diff,1)}")
    elif trade_diff > - 5:
        st.subheader(f":red[You are losing this trade by a small amount]")
        st.subheader(f"Value Gained in this Trade: {round(trade_diff,1)}")
    elif trade_diff > - 10:
        st.subheader(f":red[You are losing this trade!]")
        st.subheader(f"Value Gained in this Trade: {round(trade_diff,1)}")
    else:
        st.subheader(f":red[You are losing this trade by a lot!]")
        st.subheader(f"Value Gained in this Trade: {round(trade_diff,1)}")
