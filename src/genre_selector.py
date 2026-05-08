import streamlit as st


GENRES = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
]


def render_genre_selector():
    st.subheader("Pick 3–5 genres you like")

    selected_genres = st.multiselect(
        "Choose your movie taste profile:",
        GENRES,
        max_selections=5,
    )

    return selected_genres