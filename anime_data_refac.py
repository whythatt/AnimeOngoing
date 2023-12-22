from bs4 import BeautifulSoup
import requests


# https://animeschedule.net/shows?mt=all&airing-statuses=Ongoing
class Website:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_page(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"[FAIL] status code = {response.status_code}"


class Animego(Website):
    base_url = "https://animego.online/ongoing/"

    def __init__(self):
        super().__init__()

    def parser(self, html):
        soup = BeautifulSoup(html, "lxml")
        # собираю все блоки с данными об аниме
        anime_links = soup.find(id="dle-content").find_all(
            "a", class_="poster-item grid-item"
        )
        # собираю название
        anime_titles = [
            title.find(class_="poster-item__title").text for title in anime_links
        ]

        # собираю число эпизодов которые вышли
        anime_episodes = []
        for eps in anime_links:
            eps = eps.find(
                class_="poster-item__img img-fit-cover img-responsive img-responsive--portrait"
            ).find(class_="poster-item__label")
            # если есть число вышелших серий, то я добавляю в список, если нет, то пропускаю
            try:
                if "серия" in eps.text:
                    eps = eps.text.replace("серия", "episodes")
                elif "серий" in eps.text:
                    eps = eps.text.replace("серий", "episodes")
                elif "серии" in eps.text:
                    eps = eps.text.replace("серии", "episodes")

                anime_episodes.append(eps)
            except AttributeError:
                anime_episodes.append("Not episodes")

        # собираю рейтинг
        anime_rating = [
            rating.find(class_="poster-item__rating").text.strip()
            for rating in anime_links
        ]

        print(anime_episodes)


html = Animego().fetch_page()
parser = Animego().parser(html)
print(parser)
