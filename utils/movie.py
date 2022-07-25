import re
import requests
from bs4 import BeautifulSoup as bs
from utils.scrapper import NaverReviewScrapper


def get_movie_poster(link):
    response = requests.get(link)
    poster = bs(response.content, "html.parser").find("img")
    if not poster:
        return "https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png"
    return poster["src"]


def get_movie_info(title, config, year=0):
    header_parms = {
        "X-Naver-Client-Id": config.CLIENT_ID,
        "X-Naver-Client-Secret": config.CLIENT_SECRET,
    }

    if year:
        url = f"https://openapi.naver.com/v1/search/movie.json?query={title}&yearfrom={year}&yearto={year}"
    else:
        url = f"https://openapi.naver.com/v1/search/movie.json?query={title}"
    res = requests.get(url, headers=header_parms).json()["items"]
    movie = res[0]
    code = movie["link"].split("=")[-1]
    scrapper = NaverReviewScrapper()
    story = scrapper.get_story(code=code)
    reviews = scrapper.get_review_by_num(title="", code=code)

    movie_info = {
        "years": [movie["pubDate"] for movie in res],
        "title": re.sub("[^가-힣ㅏ-ㅣㄱ-ㅎ1-9\\s]", "", movie["title"]),
        "subtitle": re.sub("[<b>|/]", "", movie["subtitle"]),
        "image": get_movie_poster(
            f"https://movie.naver.com/movie/bi/mi/photoViewPopup.naver?movieCode={code}"
        ),
        "director": movie["director"].split("|")[0],
        "actor": ", ".join(movie["actor"].split("|")[:-1]),
        "rating": movie["userRating"],
        "date": movie["pubDate"],
        "story": story,
        "reviews": reviews,
        "code": code,
    }

    return movie_info
