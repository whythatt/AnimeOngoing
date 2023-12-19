# название
# рейтинг
# эпизодов вышло
# сколько ждать 5 day 23 hours

# продолжительность серии
# дата выхода november 9, 2023

from bs4 import BeautifulSoup
import requests


class WebsiteParser:
    """собирает ссылки на аниме с сайта AnimeGo"""

    def __init__(self, start_url):
        self.start_url = start_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.links = []

    def fetch_page(self, my_url):
        """получает html страницу сайта и отдает его"""
        response = requests.get(my_url, headers=self.headers)

        if response.status_code == 200:
            return response.text
        else:
            return f"[FAIL] status code = {response.status_code}"

    def parse_links(self, html):
        """собирает ссылки на аниме (с полученной от функции fetch_page) html страницы"""
        soup = BeautifulSoup(html, "lxml")

        # parsing block
        links = soup.find_all("a", class_="poster-item")
        for link in links:
            link = f"https://animego.online/{link.get('href')}"
            self.links.append(link)

    def data_parser(self, anime_html):
        soup = BeautifulSoup(anime_html, "lxml")

        # parsing block
        title = soup.find("header", class_="page__header").find("h1")
        rating = soup.find("div", class_="page__rating-item--audience").find("div")
        episodes_relised = (
            soup.find(class_="page__poster")
            .find(class_="poster-item__label")
            .find("span")
        )
        episode_duration = (
            soup.find("ul", class_="page__details-list")
            .find_all("li")[2]
            .find_all("span")[1]
        )
        print(episode_duration.text)

    def run(self):
        """запускает парсер"""
        html = self.fetch_page(self.start_url)
        self.parse_links(html)

        for link in self.links:
            anime_html = self.fetch_page(link)
            self.data_parser(anime_html)


title = WebsiteParser("https://animego.online/ongoing/")
title.run()
