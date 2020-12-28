from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup as Bs


class Scraper:
    URL = None

    def fetch_content(self):
        page = requests.get(self.URL)
        soup = Bs(page.content, 'html.parser')
        return soup

    def get_time(self):
        t = datetime.now(timezone.utc).astimezone()
        t_str = t.strftime('%d-%m-%Y %H:%M:%S %Z').replace('Standard Time', '').replace('  ', ' ')
        return t_str

    def fetch_player_stats(self, soup):
        return ()

    def get_stats(self):
        page_soup = self.fetch_content()
        player_stats = self.fetch_player_stats(page_soup)
        update_time = self.get_time()
        return player_stats + (update_time,)


class OWScraper(Scraper):
    REGION = 'en-us'
    PLATFORM = 'pc'
    NAME = 'LetsGo-21230'
    URL = f'https://playoverwatch.com/{REGION}/career/{PLATFORM}/{NAME}/'

    def fetch_player_stats(self, soup):
        comp_roles = soup.findAll('div', class_='competitive-rank-tier')
        comp_SRs = soup.findAll('div', class_='competitive-rank-level')
        role_names = [role['data-ow-tooltip-text'][:role['data-ow-tooltip-text'].find('Skill') - 1] for role in
                      comp_roles]
        role_SRs = [sr.text for sr in comp_SRs]

        comp = soup.findAll('div', {'data-category-id': '0x0860000000000021'})
        hero_name_data = comp[1].findAll('div', class_='ProgressBar-title')
        hero_time_data = comp[1].findAll('div', class_='ProgressBar-description')
        hero_names = [name.text for name in hero_name_data[:5]]
        hero_times = [time.text for time in hero_time_data[:5]]
        for i, time in enumerate(hero_times):
            segments = time.split(':')
            if len(segments) == 3:
                continue
            elif len(segments) == 2:
                hero_times[i] = f'00:{segments[0]}:{segments[1]}'
            elif len(segments) == 1:
                hero_times[i] = f'00:00:{segments[0]}'

        half_length = int(len(role_names) / 2)
        role_names, role_SRs = role_names[:half_length], role_SRs[:half_length]  # removes duplicates from lists
        return role_names, role_SRs, hero_names, hero_times


class SmiteScraper(Scraper):
    NAME = '4172839-Ioan'
    URL = f'https://smite.guru/profile/{NAME}'

    def fetch_player_stats(self, soup):
        player = soup.find(id='cw')
        rawLevel = player.find('div', class_='profile-header__level')
        rawPlaytime = player.find('div', class_='ptw__val')
        rawWinLoss = player.findAll(class_='ptw__val')
        rawKDA = player.findAll(class_='tsw__grid')
        rawMatchesPlayed = player.find('div', class_='tsw__grid')

        level = rawLevel.text.strip()
        playtime = rawPlaytime.text.strip()
        playtime = playtime[:playtime.find('h') + 1]
        win_loss = rawWinLoss[1].text.strip()
        kda = rawKDA[1].find('div', class_='tsw__grid__stat').text.strip()
        matches_played = rawMatchesPlayed.find('div', class_='tsw__grid__stat').text.strip()
        return level, playtime, win_loss, kda, matches_played
