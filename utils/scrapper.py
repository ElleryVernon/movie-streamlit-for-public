import re
import requests
from bs4 import BeautifulSoup as bs
from utils.status_code import STATUS


class NaverReviewScrapper:
    def __init__(self):
        self.base_url = "https://movie.naver.com/movie"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == STATUS["OK"]:
            return bs(response.content, "html.parser")

    def get_movie_code(self, title):
        url = f"{self.base_url}/search/result.naver?query={title}&section=all&ie=utf8"
        movies = self.get_page(url).find("p", class_="result_thumb").find("a")
        code = None
        if movies:
            code = movies["href"].split("=")[1]

        return code

    def get_reviews(self, code, page=1):
        # ratings = [article.find("em").text for article in articles]
        url = f"{self.base_url}/point/af/list.naver?st=mcode&sword={code}&target=after&page={page}"
        articles = self.get_page(url).find_all(class_="title")
        reviews = [article.text.split("\n")[5].strip() for article in articles]
        result = {
            "comments": [review for review in reviews if review],
            "size": len(reviews),
        }
        return result

    def get_review_by_num(self, title, code="", max_count=50):
        if not code:
            code = self.get_movie_code(title)

        result = []
        page_num = 1
        is_progress = True
        while is_progress:
            comments, size = self.get_reviews(code, page_num).values()
            result += comments

            if len(result) > max_count or size < 10:
                result = result[:max_count]
                is_progress = False

            result = list(set(result))
            page_num += 1

        return result

    def get_story(self, code):
        url = f"{self.base_url}/bi/mi/basic.naver?code={code}"
        story_area = self.get_page(url).find("div", class_="story_area")
        story = "줄거리가 존재하지 않습니다."

        if story_area:
            story = re.sub("\r\xa0", " ", story_area.find("p", class_="con_tx").text)

        return story
