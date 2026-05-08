import streamlit as st
import pandas as pd

from src.data_loader import build_or_load_model_df
from src.genre_selector import render_genre_selector
from src.movie_pool import create_movie_pool, get_random_movies
from src.rating_flow import render_rating_flow
from src.recommender import generate_recommendations
from src.pack_reveal import render_pack_reveal


st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
)


def init_session_state():
    defaults = {
        "page": "genres",
        "selected_genres": [],
        "movies_to_rate": None,
        "user_ratings": [],
        "rating_index": 0,
        "recommendations": None,
        "revealed_cards": set(),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header():
    st.markdown(
        """
        <div style="text-align:center; padding-top:10px; padding-bottom:20px;">
            <h1 style="font-size:48px; margin-bottom:8px; font-weight:800; letter-spacing:-1px;">
                🎬 CineMatch
            </h1>
            <div style="font-size:18px; color:#9ca3af; margin-top:0px;">
                Discover your next favorite movie.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top, #211636 0%, #0e1117 45%, #090b10 100%);
        }

        div[data-testid="stButton"] button {
            border-radius: 18px;
            font-weight: 700;
            min-height: 52px;
        }

        div[data-testid="stButton"] button:hover {
            transform: scale(1.02);
            transition: 0.15s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_empty_movies_to_rate(movies_to_rate):
    if movies_to_rate is None:
        return True

    if isinstance(movies_to_rate, pd.DataFrame):
        return movies_to_rate.empty

    if isinstance(movies_to_rate, list):
        return len(movies_to_rate) == 0

    return False


def reset_rating_flow():
    st.session_state["user_ratings"] = []
    st.session_state["rating_index"] = 0
    st.session_state["recommendations"] = None
    st.session_state["revealed_cards"] = set()


def render_genre_page(movie_df):
    selected_genres = render_genre_selector()
    st.session_state["selected_genres"] = selected_genres

    if len(selected_genres) < 3:
        st.info("Select at least 3 genres to start.")
        return

    if st.button("Continue to Movie Ratings"):
        movie_pool = create_movie_pool(movie_df, selected_genres)

        st.session_state["movies_to_rate"] = get_random_movies(movie_pool, n=20)
        reset_rating_flow()
        st.session_state["page"] = "ratings"

        st.rerun()


def render_ratings_page(movie_df):
    movies_to_rate = st.session_state.get("movies_to_rate")

    if is_empty_movies_to_rate(movies_to_rate):
        st.warning("No movies loaded. Go back and select genres again.")

        if st.button("Back to Genres"):
            st.session_state["page"] = "genres"
            st.rerun()

        return

    user_ratings = render_rating_flow(movies_to_rate)
    st.session_state["user_ratings"] = user_ratings

    if len(user_ratings) >= 5 and st.session_state["recommendations"] is None:
        recommendations = generate_recommendations(
            movie_df=movie_df,
            selected_genres=st.session_state["selected_genres"],
            user_ratings=user_ratings,
            top_n=5,
        )

        st.session_state["recommendations"] = recommendations
        st.session_state["revealed_cards"] = set()
        st.session_state["page"] = "reveal"
        st.rerun()


def render_reveal_page():
    if st.session_state["recommendations"] is not None:
        render_pack_reveal(st.session_state["recommendations"])
    else:
        st.warning("No recommendations found yet.")


def main():
    init_session_state()
    add_custom_css()
    render_header()

    movie_df = build_or_load_model_df()

    if st.session_state["page"] == "genres":
        render_genre_page(movie_df)

    elif st.session_state["page"] == "ratings":
        render_ratings_page(movie_df)

    elif st.session_state["page"] == "reveal":
        render_reveal_page()


if __name__ == "__main__":
    main()