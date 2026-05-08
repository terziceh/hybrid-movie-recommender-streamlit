import streamlit as st

from src.data_loader import build_or_load_model_df
from src.genre_selector import render_genre_selector
from src.movie_pool import create_movie_pool, get_random_movies
from src.rating_flow import render_rating_flow
from src.recommender import generate_recommendations
from src.pack_reveal import render_pack_reveal


st.set_page_config(
    page_title="Movie Recommender MVP",
    page_icon="🎬",
    layout="wide",
)


def main():
    st.title("🎬 Movie Recommender MVP")
    st.write("Pick your genres, rate 5 movies, then reveal your recommendation pack.")

    movie_df = build_or_load_model_df()

    selected_genres = render_genre_selector()

    if len(selected_genres) >= 3:
        movie_pool = create_movie_pool(movie_df, selected_genres)

        if st.button("Generate 5 Movies to Rate"):
            st.session_state["movies_to_rate"] = get_random_movies(movie_pool, n=5)

        if "movies_to_rate" in st.session_state:
            user_ratings = render_rating_flow(st.session_state["movies_to_rate"])

            if len(user_ratings) > 0:
                if st.button("Reveal My Movie Pack"):
                    recommendations = generate_recommendations(
                        movie_df=movie_df,
                        selected_genres=selected_genres,
                        user_ratings=user_ratings,
                        top_n=5,
                    )

                    st.session_state["recommendations"] = recommendations

        if "recommendations" in st.session_state:
            render_pack_reveal(st.session_state["recommendations"])

    else:
        st.info("Select at least 3 genres to start.")


if __name__ == "__main__":
    main()