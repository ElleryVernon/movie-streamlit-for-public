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
from utils.movie import get_movie_info, get_movie_list


def app():
    API_CONFIG = config.NaverOpenAPIConfig
    tokenizer = load_tokenizer()
    model = load_model()

    st.title("네이버 영화 리뷰 분석")
    title = st.text_input("정확한 영화 제목을 입력하고 Enter를 눌러주세요. (시리즈 물은 번호를 포함해주세요.)")
    select_area = st.empty()

    st.write("""---""")

    placeholder = st.empty()
    movie_aria = st.empty()

    st.write("""---""")
    rating_area = st.empty()
    tab_area = st.empty()

    if not title:
        return placeholder.success("입력을 기다리고 있어요... ")

    options = get_movie_list(title, API_CONFIG)

    if not options:
        return placeholder.error("영화를 찾을 수 없습니다. 제목을 다시 확인해주세요.")

    movie = select_area.selectbox("영화를 선택해주세요. 👇", get_movie_list(title, API_CONFIG))

    if "발견했어요!" in movie:
        return placeholder.success("영화를 선택하시는동안 기다리고 있어요.")

    placeholder.info("영화 내용을 최대한 빨리 요약하고 있어요... ")
    title, year = movie.rstrip(")").split(" (")
    movie_info = get_movie_info(title, API_CONFIG, year)

    placeholder.warning("열심히 리뷰를 읽고 분류 하고 있어요...")
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
