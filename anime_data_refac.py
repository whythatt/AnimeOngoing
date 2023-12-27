# дальше нужно спарсить второй сайт, сложить все в один список и в отдельной \
# функции записать все в json файл

from bs4 import BeautifulSoup
import requests
import re


# https://animeschedule.net/shows?mt=all&airing-statuses=Ongoing
class WebsiteParser:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_page(self, html):
        response = requests.get(html, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"[FAIL] status code = {response.status_code}"

    def animeScheduleParser(self, html):
        soup = BeautifulSoup(html, "lxml")

        all_anime = soup.find_all("div", class_="anime-tile lozad")
        for anime in all_anime:
            anime_link = "https://animeschedule.net/" + anime["itemid"]
            soup = BeautifulSoup(self.fetch_page(anime_link), "lxml")

            first_block = soup.find(id="release-times-section")
            next_episode_count = first_block.find(
                "span", class_="release-time-episode-number"
            )

            title = anime.find("h2", class_="anime-tile-title")
            release_date = anime.find(
                class_="anime-tile-bottom-item anime-tile-datetime"
            )  # .text.split("\n")[1]

            episode_duration = anime["duration"]
            total_episodes = anime["episodes"]
            rating = anime["score"]
            print(next_episode_count.text)

    def run(self):
        html = self.fetch_page(self.url)
        self.animeScheduleParser(html)


# вызываю парсер для AnimeSchedule
animeschedule = WebsiteParser(
    "https://animeschedule.net/shows?mt=all&airing-statuses-exclude=Finished"
)

animeschedule.run()
