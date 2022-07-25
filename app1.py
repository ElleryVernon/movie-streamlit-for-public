import streamlit as st
from time import sleep
from config import config

from components.components import (
    movie_info_component,
    poster_component,
    review_component,
    summary_component,
)

from model.model import load_tokenizer, load_model, prediction
from utils.movie import get_movie_info
from utils.utils import make_year_arr


def app():
    API_CONFIG = config.NaverOpenAPIConfig
    tokenizer = load_tokenizer()
    model = load_model()

    st.title("네이버 영화 리뷰 분석")
    title = st.text_input("정확한 영화 제목을 입력하고 Enter를 눌러주세요. (시리즈 물은 번호를 포함해주세요.)")
    year = st.selectbox("개봉연도", make_year_arr(), index=0)

    st.write("""---""")

    placeholder = st.empty()
    movie_aria = st.empty()

    st.write("""---""")
    rating_area = st.empty()
    tab_area = st.empty()

    placeholder.success("입력을 기다리고 있어요... ")

    if title:
        try:
            placeholder.empty()
            rating_area.empty()
            movie_aria.empty()
            tab_area.empty()

            placeholder.info("영화 내용을 최대한 빨리 요약하는 중... ")

            if year == "전체":
                movie_info = get_movie_info(title, API_CONFIG)
            else:
                movie_info = get_movie_info(title, API_CONFIG, year)

            placeholder.warning("열심히 리뷰를 읽고 분류 하는 중...")

            reviews = prediction(movie_info["reviews"], model, tokenizer)

            placeholder.success("완료!")
            sleep(0.5)
            placeholder.empty()

            col1, col2 = movie_aria.columns([0.8, 1.5])
            with col1:
                poster_component(movie_info["image"])
            with col2:
                movie_info_component(movie_info)

            summary_component(rating_area, reviews, movie_info)
            review_component(tab_area, reviews, movie_info)

        except Exception:
            placeholder.error("영화를 찾을 수 없습니다. 제목 혹은 개봉연도를 다시 확인해주세요.")
