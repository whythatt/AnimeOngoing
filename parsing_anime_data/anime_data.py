from lxml import etree, html
import requests
from date_formatting import date_form
import timeit
import json


# https://animeschedule.net/shows?mt=all&airing-statuses=Ongoing
class WebsiteParser:
    def __init__(self, url):
        self.parser = etree.HTMLParser()
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_page(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            return f"[FAIL] status code = {response.status_code}"

    def get_anime_links(self, html):
        # HTMLParser нужен для того, чтобы etree мог извлекать данные из html-формата
        # передаю полученный html сюда и форматирую из формата строки в html-файл, и преобразовываю html файл в удобный для etree
        tree = etree.fromstring(html, self.parser)

        all_page_count = tree.xpath('//*[@id="last-page"]/text()')[0]
        all_anime_links = []
        for i in range(1, int(all_page_count) + 1):
            link = f"{self.url}&page={i}"
            tree = etree.fromstring(self.fetch_page(link), self.parser)

            anime_itemid = tree.xpath('//div[@class="anime-tile lozad"]/@itemid')
            anime_links = ["https://animeschedule.net" + i for i in anime_itemid]
            for link in anime_links:
                all_anime_links.append(link)
        return all_anime_links

    def parsing_anime_pages(self, anime_links):
        anime_data_dict = {}
        for link in anime_links:
            anime_page = etree.fromstring(self.fetch_page(link), self.parser)

            title = anime_page.xpath('//*[@id="anime-header-main-title"]/text()')[0]
            # союираю данные из блока с данными об аниме. Все это из одной пременной - data_block_data
            data_block_data = anime_page.xpath(
                '//section[@id="information-section-large"]'
            )[0]

            total_episodes = data_block_data.xpath('.//div/h3[text()="Episodes"]')
            total_episodes = self.check(
                total_episodes, "Episodes", xpath="../div/text()"
            )

            mediatype = data_block_data.xpath('.//div/h3[text()="Type"]')
            mediatype = self.check(mediatype, "Type", xpath="..//a/text()")

            season = data_block_data.xpath('.//div/h3[text()="Season"]')
            season = self.check(season, "Season", xpath="../a/text()")

            release_date = data_block_data.xpath('.//div/h3[text()="Release Date"]')
            release_date = self.check(
                release_date, "Release Date", xpath="../time/text()"
            )

            status = data_block_data.xpath('.//div/h3[text()="Status"]')
            status = self.check(status, "Status", xpath="../div/text()")

            episode_duration = data_block_data.xpath(
                './/div/h3[text()="Episode Length"]'
            )
            episode_duration = self.check(
                episode_duration, "Episode Length", xpath="../div/text()"
            )

            score = data_block_data.xpath('.//div/h3[text()="Score"]')
            score = self.check(score, "Score", xpath="../strong/text()")

            # собираю данные из блока с данными о выходе новой серии
            release_time_block = anime_page.xpath('//*[@id="release-times-section"]')
            if len(release_time_block) > 0:
                release_time_block = release_time_block[0]

                next_episode_count = release_time_block.xpath(
                    '//span[@class="release-time-episode-number"]/text()'
                )[0].split(" ")[1]

                release_date_next_ep = release_time_block.xpath(
                    './/*[@id="release-time-raw"]'
                )[0].get("datetime")
                # форматирую полученную строку времени нужный мне формат
                release_date_next_ep = date_form(release_date_next_ep)
            else:
                next_episode_count = None
                release_date_next_ep = None

            anime_data = {
                "next_episode_count": next_episode_count,
                "release_date_next_ep": release_date_next_ep,
                "mediatype": mediatype,
                "season": season,
                "release_date": release_date,
                "status": status,
                "episode_duration": episode_duration,
                "score": score,
            }
            anime_data_dict.update({title: anime_data})
        return anime_data_dict

    def check(self, block, text, xpath):
        if len(block) > 0:
            if block[0].text == f"{text}":
                return block[0].xpath(xpath)[0]
        else:
            block = None
            return block

    def write_data(self, data_dict):
        with open("anime_data.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)

    def run(self):
        html = self.fetch_page(url=self.url)
        anime_links = self.get_anime_links(html=html)
        anime_data_dict = self.parsing_anime_pages(anime_links=anime_links)
        self.write_data(anime_data_dict)


# вызываю парсер для AnimeSchedule
animeschedule = WebsiteParser(
    "https://animeschedule.net/shows?mt=all&airing-statuses-exclude=Finished"
)
animeschedule.run()

# speed = timeit.timeit(stmt="animeschedule.run()", globals=globals(), number=1)
# print(speed)
