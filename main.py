# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:20:02 2020
@author: aliha
@twitter: rockingAli5

Modified on Sun Aug 14 12:00:00 2022
@modified: Sushant Rao / twitter: @StatPeekers
"""
import os
import re
import json
import time
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None
from bs4 import BeautifulSoup as soup
from collections import OrderedDict
from datetime import datetime as dt
from selenium.webdriver.common.by import By

try:
    from tqdm import trange
except ModuleNotFoundError:
    pass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

TRANSLATE_DICT = {'Jan': 'Jan',
                  'Feb': 'Feb',
                  'Mac': 'Mar',
                  'Apr': 'Apr',
                  'Mei': 'May',
                  'Jun': 'Jun',
                  'Jul': 'Jul',
                  'Ago': 'Aug',
                  'Sep': 'Sep',
                  'Okt': 'Oct',
                  'Nov': 'Nov',
                  'Des': 'Dec',
                  'Mar': 'Mar',
                  'May': 'May',
                  'Aug': 'Aug',
                  'Oct': 'Oct',
                  'Dec': 'Dec'}

main_url = 'https://1xbet.whoscored.com/'


def get_league_urls(minimize_window=True):
    driver = webdriver.Chrome('chromedriver.exe')
    # driver = webdriver.Firefox()

    if minimize_window:
        driver.minimize_window()

    driver.get(main_url)
    league_names = []
    league_urls = []
    for i in range(21):
        league_name = driver.find_element("xpath", '//*[@id="popular-tournaments-list"]/li[' + str(i + 1) + ']/a').text
        league_link = driver.find_element("xpath", '//*[@id="popular-tournaments-list"]/li[' + str(i + 1) + ']/a').get_attribute('href')
        league_names.append(league_name)
        league_urls.append(league_link)

    for link in league_urls:
        if 'Russia' in link:
            r_index = league_urls.index(link)
            league_names[r_index] = 'Russian Premier League'
            break

    # leagues = {}
    # for name, link in zip(league_names, league_urls):
    #     leagues[name] = link
    # Code execution will be faster with dict comprehension than a traditional for loop
    leagues = {
        name: link for name, link in zip(league_names, league_urls)
    }

    driver.close()
    return leagues


def get_match_urls(comp_urls, competition, season, maximize_window=True):
    driver = webdriver.Chrome('chromedriver.exe')
    # driver = webdriver.Firefox()

    if maximize_window:
        driver.maximize_window()

    comp_url = comp_urls[competition]
    driver.get(comp_url)
    time.sleep(5)

    seasons = driver.find_element("xpath", '//*[@id="seasons"]').get_attribute('innerHTML').split(sep='\n')
    seasons = [i for i in seasons if i]

    for j in range(1, len(seasons) + 1):
        if driver.find_element("xpath", '//*[@id="seasons"]/option[' + str(j) + ']').text == season:
            driver.find_element("xpath", '//*[@id="seasons"]/option[' + str(j) + ']').click()

            time.sleep(5)
            try:
                stages = driver.find_element("xpath", '//*[@id="stages"]').get_attribute('innerHTML').split(sep='\n')
                stages = [i for i in stages if i]

                all_urls = []

                for i in range(1, len(stages) + 1):
                    if competition == 'Champions League' or competition == 'Europa League':
                        if 'Group Stages' in driver.find_element("xpath",
                                                                 '//*[@id="stages"]/option[' + str(
                                                                     i) + ']').text or 'Final Stage' in driver.find_element("xpath",
                                                                                                                            '//*[@id="stages"]/option[' + str(
                                                                                                                                i) + ']').text:
                            driver.find_element("xpath", '//*[@id="stages"]/option[' + str(i) + ']').click()
                            time.sleep(5)

                            driver.execute_script("window.scrollTo(0, 400)")

                            match_urls = get_fixture_data(driver)

                            match_urls = get_sorted_data(match_urls)

                            match_urls2 = [url for url in match_urls if '?' not in url['date'] and '\n' not in url['date']]

                            all_urls += match_urls2
                        else:
                            continue

                    elif competition == 'Major League Soccer':
                        if 'Grp. ' not in driver.find_element("xpath", '//*[@id="stages"]/option[' + str(i) + ']').text:
                            driver.find_element("xpath", '//*[@id="stages"]/option[' + str(i) + ']').click()
                            time.sleep(5)

                            driver.execute_script("window.scrollTo(0, 400)")

                            match_urls = get_fixture_data(driver)

                            match_urls = get_sorted_data(match_urls)

                            match_urls2 = [url for url in match_urls if '?' not in url['date'] and '\n' not in url['date']]

                            all_urls += match_urls2
                        else:
                            continue

                    else:
                        driver.find_element("xpath", '//*[@id="stages"]/option[' + str(i) + ']').click()
                        time.sleep(5)

                        driver.execute_script("window.scrollTo(0, 400)")

                        match_urls = get_fixture_data(driver)

                        match_urls = get_sorted_data(match_urls)

                        match_urls2 = [url for url in match_urls if '?' not in url['date'] and '\n' not in url['date']]

                        all_urls += match_urls2

            except NoSuchElementException:
                all_urls = []

                driver.execute_script("window.scrollTo(0, 400)")
                try:
                    driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
                except:
                    pass
                match_urls = get_fixture_data(driver)

                match_urls = get_sorted_data(match_urls)

                match_urls2 = [url for url in match_urls if '?' not in url['date'] and '\n' not in url['date']]

                all_urls += match_urls2

            remove_dup = [dict(t) for t in {tuple(sorted(d.items())) for d in all_urls}]
            all_urls = get_sorted_data(remove_dup)

            driver.close()

            return all_urls

    season_names = [re.search(r'>(.*?)<', season).group(1) for season in seasons]
    driver.close()
    print('Seasons available: {}'.format(season_names))
    raise 'Season Not Found.'


def get_fixture_data(driver):
    matches_ls = []
    while True:
        table_rows = driver.find_elements(By.CLASS_NAME, 'divtable-row')
        if len(table_rows) == 0:
            break
        for row in table_rows:
            match_dict = {}
            element = soup(row.get_attribute('innerHTML'), features='html.parser')
            link_tag = element.find("a", {"class": "result-1 rc"})
            # if type(link_tag) is type(None):
            if isinstance(link_tag, type(None)):
                if isinstance(element.find('span', {'class': 'status-1 rc'}), type(None)):
                    date = row.text.split(', ')[-1]
            # if type(link_tag) is not type(None):
            else:
                match_dict['date'] = date
                match_dict['time'] = element.find('div', {'class': 'col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 time divtable-data'}).text
                match_dict['home'] = element.find_all("a", {"class": "team-link"})[0].text
                match_dict['away'] = element.find_all("a", {"class": "team-link"})[1].text
                match_dict['score'] = element.find("a", {"class": "result-1 rc"}).text
                match_dict['url'] = link_tag.get("href")
            matches_ls.append(match_dict)
        try:
            driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        except NoSuchElementException:
            pass
        _ = driver.find_element("xpath", '//*[@id="date-controller"]/a[1]').click()
        time.sleep(2)
        if driver.find_element("xpath", '//*[@id="date-controller"]/a[1]').get_attribute('title') == 'No data for previous week':
            table_rows = driver.find_elements(By.CLASS_NAME, 'divtable-row')
            for row in table_rows:
                match_dict = {}
                element = soup(row.get_attribute('innerHTML'), features='html.parser')
                link_tag = element.find("a", {"class": "result-1 rc"})
                if isinstance(link_tag, type(None)):
                    if isinstance(element.find('span', {'class': 'status-1 rc'}), type(None)):
                        date = row.text.split(', ')[-1]
                # if type(link_tag) is not type(None):
                else:
                    match_dict['date'] = date
                    match_dict['time'] = element.find('div', {'class': 'col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 time divtable-data'}).text
                    match_dict['home'] = element.find_all("a", {"class": "team-link"})[0].text
                    match_dict['away'] = element.find_all("a", {"class": "team-link"})[1].text
                    match_dict['score'] = element.find("a", {"class": "result-1 rc"}).text
                    match_dict['url'] = link_tag.get("href")
                matches_ls.append(match_dict)
            break

    matches_ls = list(filter(None, matches_ls))

    return matches_ls


def translate_date(data):
    for match in data:
        date = match['date'].split()
        match['date'] = ' '.join([TRANSLATE_DICT[date[0]], date[1], date[2]])

    return data


def get_sorted_data(data):
    try:
        data = sorted(data, key=lambda i: dt.strptime(i['date'], '%b %d %Y'))
        return data
    except ValueError:
        data = translate_date(data)
        data = sorted(data, key=lambda i: dt.strptime(i['date'], '%b %d %Y'))
        return data


def get_match_data(driver, url, display=True, close_window=True):
    driver.get(url)

    # get script data from page source
    script_content = driver.find_element("xpath", '//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')

    # clean script content
    script_content = re.sub(r"[\n\t]*", "", script_content)
    script_content = script_content[script_content.index("matchId"):script_content.rindex("}")]

    # this will give script content in list form
    script_content_list = list(filter(None, script_content.strip().split(',            ')))
    metadata = script_content_list.pop(1)

    # string format to json format
    match_data = json.loads(metadata[metadata.index('{'):])
    keys = [item[:item.index(':')].strip() for item in script_content_list]
    values = [item[item.index(':') + 1:].strip() for item in script_content_list]
    for key, val in zip(keys, values):
        match_data[key] = json.loads(val)

    # get other details about the match
    region = driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/span[1]').text
    league = driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[0]
    season = driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[1]
    if len(driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 2:
        competition_type = 'League'
        competition_stage = ''
    elif len(driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 3:
        competition_type = 'Knock Out'
        competition_stage = driver.find_element("xpath", '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[-1]
    else:
        print('Getting more than 3 types of information about the competition.')
        competition_type = ''
        competition_stage = ''

    match_data['region'] = region
    match_data['league'] = league
    match_data['season'] = season
    match_data['competitionType'] = competition_type
    match_data['competitionStage'] = competition_stage

    # sort match_data dictionary alphabetically
    match_data = OrderedDict(sorted(match_data.items()))
    match_data = dict(match_data)
    if display:
        print('Region: {}, League: {}, Season: {}, Match ID: {}'.format(region, league, season, match_data['matchId']))

    if close_window:
        driver.close()

    return match_data


def create_team_json(data):
    return {"home": data["home"], "away": data["away"]}


def create_player_json(data):
    return data["home"]["players"] + data["away"]["players"]


def create_events_json(data):
    return data["events"]


def create_player_id_name_map(data):
    data_dir = "data/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    json_filename = data_dir + "playerIdNameMap.json"
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as f:
            player_id_name_map = json.load(f)
        return player_id_name_map.update(data["playerIdNameDictionary"])
    else:
        return data["playerIdNameDictionary"]


def create_matches_json(data):
    keys_list = [
        'attendance',
        'commonEvents',
        'competitionStage',
        'competitionType',
        'elapsed',
        'etScore',
        'expandedMaxMinute',
        'expandedMinutes',
        'ftScore',
        'htScore',
        'league',
        'matchId',
        'maxMinute',
        'maxPeriod',
        'minuteExpanded',
        'periodCode',
        'periodEndMinutes',
        'periodMinuteLimits',
        'pkScore',
        'referee',
        'region',
        'score',
        'season',
        'startDate',
        'startTime',
        'statusCode',
        'timeStamp',
        'timeoutInSeconds',
        'venueName',
        'weatherCode'
    ]
    match_json = {
        key: value for key, value in data.items() if key in keys_list
    }

    return match_json
