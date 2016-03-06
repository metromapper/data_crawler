# coding: utf8

import json
import mechanize
from bs4 import BeautifulSoup

# access url
SITE_URL = "http://www.homes.co.jp/chintai/tokyo/line/price/"


def access(url):
    # Browser
    br = mechanize.Browser()
    br.set_handle_robots(False)
    r = br.open(url)
    html = r.read()
    return html


soup = BeautifulSoup(access(SITE_URL), "html.parser")

chintai = {}

rosen_list = soup.find('div', class_="mod-rosenList")
# 東京メトロ
metro = rosen_list.find_all('div', class_="rosenType")[1]
company_name = metro.find('p').text

# かぶりありで路線名も入っている
# lines = metro.find_all('li')
# for i in xrange(0, len(lines)):
#     station_name = lines[i].find('a').string
#     chintai[station_name] = {}
#     station_href = lines[i].find('a').get('href')
#     station_soup = BeautifulSoup(access(station_href), "html.parser")
#     stations = station_soup.find("tbody", id="prg-aggregate-graph").find_all("tr")
#     for j in xrange(0, len(stations)):
#         a = stations[j].find("td", class_="station").find('a')
#         station = a.string
#         chintai[station_name][station] = {}
#         chintai_soup = BeautifulSoup(access(a.get('href')), "html.parser")
#         chintaies = chintai_soup.find("tbody", id="prg-aggregate-graph").find_all("tr")
#         for k in xrange(0, len(chintaies)):
#             madori = chintaies[k].find("td", class_="madori").string
#             try:
#                 price = chintaies[k].find("td", class_="price").find("span").string
#             except:
#                 price = None
#             chintai[station_name][station][madori] = price

# 路線名が入っていなくて、駅名にかぶりもない
lines = metro.find_all('li')
for i in xrange(0, len(lines)):
    station_name = lines[i].find('a').string
    # chintai[station_name] = {}
    station_href = lines[i].find('a').get('href')
    station_soup = BeautifulSoup(access(station_href), "html.parser")
    stations = station_soup.find("tbody", id="prg-aggregate-graph").find_all("tr")
    for j in xrange(0, len(stations)):
        a = stations[j].find("td", class_="station").find('a')
        station = a.string
        if station in chintai:
            continue
        chintai[station] = {}
        chintai_soup = BeautifulSoup(access(a.get('href')), "html.parser")
        chintaies = chintai_soup.find("tbody", id="prg-aggregate-graph").find_all("tr")
        for k in xrange(0, len(chintaies)):
            madori = chintaies[k].find("td", class_="madori").string
            try:
                price = chintaies[k].find("td", class_="price").find("span").string
            except:
                price = None
            chintai[station][madori] = price

print chintai
json_data = json.dumps(chintai)
f = open('metro_non_kaburinashi.json', 'w')
f.write(json_data)
f.close()
