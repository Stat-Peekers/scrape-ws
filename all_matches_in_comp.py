# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:28:34 2020
@title: Scrape match, team, player and event level data for all matches not in current data in local data directory
Modified on Sun Aug 14 12:00:00 2022
@modified: Sushant Rao / twitter: @StatPeekers
"""

"""
NOTE: I would advise you to not run this code for the entire season. Chances are you might be detected as a bot and be blocked.
Modify the code (for loop at the end) and run it for maybe 20 games (2 GWs) at a time
"""

import os
import re
import time

from main import get_league_urls, get_match_urls
from single_match_scrape import single_match_data


if __name__ == "__main__":

    # getting competition urls
    league_urls = get_league_urls()

    # Select comp and season:
    tournaments_list = list(league_urls.keys())
    # tournaments_list = [
    #     "Premier League",
    #     "Champions League",
    #     "Ligue 1",
    #     "LaLiga",
    #     "Bundesliga",
    #     "2. Bundesliga",
    #     "Serie A",
    #     "Eredivisie"
    # ]
    season_list = [
        "2020/2021",
        "2021/2022",
        "2022/2023",
        "2023/2024"
    ]
    # NOTE: You can add tournaments and seasons above as you want according to the WS website

    # Get input for tournament details:
    i = 0
    for i, text_output in enumerate(tournaments_list, start=1):
        print("{}. {}".format(i, text_output))
    while True:
        try:
            selected = int(input('Select one of the below (1-{}): '.format(i)))
            comp_name = tournaments_list[selected - 1]
            print('Selected Tournament is {}'.format(comp_name))
            break
        except(ValueError, IndexError):
            print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

    for i, text_output in enumerate(season_list, start=1):
        print("{}. {}".format(i, text_output))
    while True:
        try:
            selected = int(input('Select one of the below (1-{}): '.format(i)))
            season_name = season_list[selected - 1]
            print('Selected Season is {}'.format(season_name))
            break
        except(ValueError, IndexError):
            print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

    # getting match urls for that competition and season
    match_urls = get_match_urls(comp_urls=league_urls, competition=comp_name, season=season_name)

    # setting dir path to check for existing matches
    # (This step is to avoid re-scraping of matches. If you need to re-scrape a match, simply delete the file from the respective folder)
    data_dir = "data/" + str(comp_name) + "/" + str(season_name.replace("/", "-")) + "/all_match_data/"
    if not os.path.exists(data_dir):
        existing_match_ids = []
    else:
        existing_match_ids = os.listdir(data_dir)
        existing_match_ids = [i.replace(".json", "") for i in existing_match_ids]

    main_url = 'https://1xbet.whoscored.com/'

    for m_url in match_urls[0:]:
        match_url = m_url["url"]
        m_id = re.findall('[0-9]+', match_url)[0]
        if m_id not in existing_match_ids:
            try:
                print("Scraping for", m_url["home"], "vs", m_url["away"])
                # recommended to avoid getting blocked by incapsula/imperva bots
                time.sleep(7)
                single_match_data(main_url + match_url)
            except Exception as e:
                print(e)
                try:
                    # recommended to avoid getting blocked by incapsula/imperva bots
                    time.sleep(7)
                    single_match_data(main_url + match_url)
                except Exception:
                    print("Some problem in this match! Try again later...")
                    continue
