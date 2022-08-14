# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:28:34 2020
@title: Module to scrape data for a single match
@author: Sushant Rao
Modified on Sun Aug 14 12:00:00 2022
@modified: Sushant Rao / twitter: @StatPeekers
"""

import os
import json
import main
from selenium import webdriver


def single_match_data(url):
    """
    Get data for a single match
    """
    driver = webdriver.Chrome('chromedriver.exe')

    # Data containing all the info about the match
    all_match_data = main.get_match_data(driver, url, close_window=True)

    # Match data:
    match_data = main.create_matches_json(all_match_data)

    # Team data:
    team_data = main.create_team_json(all_match_data)

    # Player data:
    player_data = main.create_player_json(all_match_data)

    # Player data:
    match_player_id_name_map = main.create_player_id_name_map(all_match_data)

    # Events dataframe
    events_data = main.create_events_json(all_match_data)

    # match Id
    match_id = all_match_data['matchId']

    # saving all data levels as json files

    tour_name = all_match_data["league"]
    season = all_match_data["season"].replace("/", "-")
    season_data_dir = "data/" + str(tour_name) + "/" + str(season) + "/"
    if not os.path.exists(season_data_dir):
        os.makedirs(season_data_dir)

# Save All Match data:
    all_match_data_dir = season_data_dir + "all_match_data/"
    if not os.path.exists(all_match_data_dir):
        os.makedirs(all_match_data_dir)
    with open(all_match_data_dir + str(match_id) + '.json', 'w') as f:
        json.dump(all_match_data, f)
    del all_match_data_dir, all_match_data
    # Save Match data:
    match_data_dir = season_data_dir + "match_info/"
    if not os.path.exists(match_data_dir):
        os.makedirs(match_data_dir)
    with open(match_data_dir + str(match_id) + '.json', 'w') as f:
        json.dump(match_data, f)
    del match_data_dir, match_data
    # Save Team data:
    team_data_dir = season_data_dir + "team_data/"
    if not os.path.exists(team_data_dir):
        os.makedirs(team_data_dir)
    with open(team_data_dir + str(match_id) + '.json', 'w') as f:
        json.dump(team_data, f)
    del team_data_dir, team_data
    # Save Player data:
    player_data_dir = season_data_dir + "player_data/"
    if not os.path.exists(player_data_dir):
        os.makedirs(player_data_dir)
    with open(player_data_dir + str(match_id) + '.json', 'w') as f:
        json.dump(player_data, f)
    del player_data_dir, player_data
    # Save Player ID Name Map:
    id_map_json = season_data_dir + "player_id_name_map.json"
    if os.path.exists(id_map_json):
        with open(id_map_json, 'r') as f:
            player_id_name_map = json.load(f)
        if player_id_name_map is not None:
            player_id_name_map.update(match_player_id_name_map)
    else:
        player_id_name_map = match_player_id_name_map
    with open(season_data_dir + "player_id_name_map.json", 'w') as f:
        json.dump(player_id_name_map, f)
    del player_id_name_map
    # Save Event data:
    event_data_dir = season_data_dir + "event_data/"
    if not os.path.exists(event_data_dir):
        os.makedirs(event_data_dir)
    with open(event_data_dir + str(match_id) + '.json', 'w') as f:
        json.dump(events_data, f)
    del event_data_dir, events_data


if __name__ == "__main__":
    # Insert desired url of the match to obtain data:
    # match_url = "https://1xbet.whoscored.com/Matches/1640674/Live/England-Premier-League-2022-2023-Crystal-Palace-Arsenal"
    match_url = input("Insert url of match here:\n")
    single_match_data(match_url)
