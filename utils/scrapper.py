import re
import requests
from bs4 import BeautifulSoup as bs


class NaverReviewScrapper:
    def __init__(self):
        self.base_url = "https://movie.naver.com/movie"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return bs(response.content, "html.parser")

    def get_movie_code(self, title):
        url = f"{self.base_url}/search/result.naver?query={title}&section=all&ie=utf8"
        movies = self.get_page(url).find("p", class_="result_thumb").find("a")

        if not movies:
            raise ValueError(f"잘못된 인자값입니다.({title})")

        return movies["href"].split("=")[1]

    def get_reviews(self, code, with_rating, page=1):
        url = f"{self.base_url}/point/af/list.naver?st=mcode&sword={code}&target=after&page={page}"
        articles = self.get_page(url).find_all(class_="title")
        reviews = [article.text.split("\n")[5].strip() for article in articles]
        ratings = [article.find("em").text for article in articles]
        if not with_rating:
            return list(set([review for review in reviews if review]))
        if ratings:
            return list(
                set(
                    [
                        [rating, review]
                        for rating, review in zip(ratings, reviews)
                        if review
                    ]
                )
            )

    def get_review_by_num(self, title, code="", with_rating=False, max_count=50):
        reviews = []
        page_num = 1
        prev_len = 0
        while len(reviews) < max_count:
            if not code:
                reviews += self.get_reviews(
                    self.get_movie_code(title), with_rating, page_num
                )
            else:
                reviews += self.get_reviews(code, with_rating, page_num)
            if prev_len == len(reviews):
                return reviews
            prev_len = len(reviews)
            page_num += 1

        return reviews[:max_count]

    def get_story(self, code):
        url = f"{self.base_url}/bi/mi/basic.naver?code={code}"
        story_area = self.get_page(url).find("div", class_="story_area")
        if not story_area:
            return "줄거리가 존재하지 않습니다."
        return re.sub("\r\xa0", " ", story_area.find("p", class_="con_tx").text)
