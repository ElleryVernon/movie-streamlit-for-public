import streamlit as st

from io import BytesIO
from urllib import request
from PIL import Image


def movie_info_component(movie_info):
    st.subheader(f"{movie_info['title']} ({movie_info['date']})")
    st.caption(
        f"부제: {movie_info['subtitle'] if movie_info['subtitle'] else '정보가 없습니다.'}"
    )
    st.write(
        f"**감독**: {movie_info['director'] if movie_info['director'] else '정보가 없습니다.'}"
    )
    st.write(f"**배우**: {movie_info['actor'] if movie_info['actor'] else '정보가 없습니다.'}")
    st.write(f"**줄거리**:")
    st.info(movie_info["story"])
    st.write(f"\n**영화 정보 더보기**:")
    st.info(
        f"https://movie.naver.com/movie/bi/mi/basic.naver?code={movie_info['code']}"
    )


def poster_component(link):
    poster = Image.open(BytesIO(request.urlopen(link).read()), mode="r")
    st.image(poster)


def review_component(area, reviews, movie_info):
    tab1, tab2, tab3 = area.tabs(["✅ 전체 평가", "😆 긍정 평가", "😡 부정 평가"])

    if not float(movie_info["rating"]) or isinstance(reviews, str):
        tab1.info(f"유저리뷰가 존재하지 않는 영화입니다.")
        tab2.info(f"유저리뷰가 존재하지 않는 영화입니다.")
        tab3.info(f"유저리뷰가 존재하지 않는 영화입니다.")
    else:
        tab1.subheader(f"전체 리뷰 ({len(reviews['all'])}개)")
        for review in reviews["all"]:
            tab1.code(review)

        tab2.subheader(f"긍정 리뷰 ({len(reviews['positive'])}개)")
        for review in reviews["positive"]:
            tab2.success(review)

        tab3.subheader(f"부정 리뷰 ({len(reviews['negative'])}개)")
        for review in reviews["negative"]:
            tab3.error(review)


def summary_component(area, reviews, movie_info):
    col3, col4, col5 = area.columns(3)
    rating = movie_info["rating"]
    if not float(rating) or not isinstance(reviews, dict):
        col3.metric("평점", "0.00", "없음", delta_color="off")
        col4.metric("평가비율", "0%", "+ 긍정")
        col5.metric("평가비율", "0", "- 부정")
    else:
        if float(rating) < 6:
            col3.metric("평점", f"{rating}", "- 부정", delta_color="normal")
        elif float(rating) < 7.5:
            col3.metric("평점", f"{rating}", "중립", delta_color="off")
        else:
            col3.metric("평점", f"{rating}", "+ 긍정", delta_color="normal")
        col4.metric(
            "평가비율",
            f"{round(len(reviews['positive']) / len(reviews['all']) * 100)}%",
            "+ 긍정",
        )
        col5.metric(
            "평가비율",
            f"{round(len(reviews['negative']) / len(reviews['all']) * 100)}%",
            "- 부정",
        )
