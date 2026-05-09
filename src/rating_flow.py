import streamlit as st

from src.tmdb_api import get_movie_poster


@st.cache_data(ttl=86400, show_spinner=False)
def safe_get_poster(title):
    try:
        return get_movie_poster(title)
    except Exception:
        return None


def get_movie_genres(movie):
    if "genres" in movie and movie["genres"]:
        return str(movie["genres"]).replace("|", " • ")

    if "genre_list" in movie and movie["genre_list"]:
        return str(movie["genre_list"]).replace("|", " • ")

    return "Genre not listed"


def get_existing_poster_url(movie):
    if "poster_url" in movie and movie["poster_url"]:
        return movie["poster_url"]

    if "poster_path" in movie and movie["poster_path"]:
        return movie["poster_path"]

    return None


def render_rating_flow(movies_to_rate):
    if "rating_index" not in st.session_state:
        st.session_state["rating_index"] = 0

    if "user_ratings" not in st.session_state:
        st.session_state["user_ratings"] = []

    if movies_to_rate.empty:
        st.warning("No movies found for those genres. Try selecting different genres.")
        return st.session_state["user_ratings"]

    rated_count = len(st.session_state["user_ratings"])

    st.markdown(
        """
        <style>
        div[data-testid="stFeedback"] {
            display: flex;
            justify-content: center;
            margin-top: 5px;
            margin-bottom: 28px;
        }

        div[data-testid="stFeedback"] button {
            transform: scale(1.85);
            margin-left: 10px;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:20px;">
            <h2>Rate Movies</h2>
            <p style="font-size:18px; color:#b8b8b8;">Rated {rated_count}/5 movies</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(min(rated_count / 5, 1.0))

    if rated_count >= 5:
        return st.session_state["user_ratings"]

    if st.session_state["rating_index"] >= len(movies_to_rate):
        st.warning("You ran out of movies. Go back and pick different genres.")
        return st.session_state["user_ratings"]

    movie = movies_to_rate.reset_index(drop=True).iloc[
        st.session_state["rating_index"]
    ]

    movie_genres = get_movie_genres(movie)

    poster_url = get_existing_poster_url(movie)

    if not poster_url:
        poster_url = safe_get_poster(movie["title"])

    col_poster, col_info = st.columns([1, 2])

    with col_poster:
        if poster_url:
            st.image(poster_url, width=280)
        else:
            st.markdown(
                """
                <div style="
                    height:420px;
                    width:280px;
                    border-radius:20px;
                    background:rgba(255,255,255,0.08);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    text-align:center;
                    color:#b8b8b8;
                    font-size:18px;
                    border:1px solid rgba(255,255,255,0.14);
                ">
                    No Poster Available
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f"""
            <div style="
                max-width:720px;
                margin:10px auto 30px auto;
                padding:40px;
                border-radius:28px;
                background:linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03));
                border:1px solid rgba(255,255,255,0.14);
                box-shadow:0 20px 50px rgba(0,0,0,0.35);
                text-align:center;
            ">
                <h1 style="font-size:42px; margin-bottom:12px;">{movie['title']}</h1>
                <p style="font-size:18px; color:#b8b8b8;">{movie_genres}</p>
                <p style="font-size:15px; color:#8f8f8f;">Movie {st.session_state['rating_index'] + 1} of {len(movies_to_rate)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        rating_choice = st.feedback(
            "stars",
            key=f"star_rating_{movie['movieId']}_{st.session_state['rating_index']}",
        )

        rating = None

        if rating_choice is not None:
            rating = float(rating_choice + 1)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("⬅ Back"):
                if st.session_state["rating_index"] > 0:
                    st.session_state["rating_index"] -= 1
                    st.rerun()

        with col2:
            if st.button("Skip"):
                st.session_state["rating_index"] += 1
                st.rerun()

        with col3:
            if st.button("Rate Movie"):
                if rating is None:
                    st.warning("Pick a star rating first.")
                else:
                    st.session_state["user_ratings"].append(
                        {
                            "movieId": movie["movieId"],
                            "title": movie["title"],
                            "genres": movie_genres,
                            "user_rating": rating,
                        }
                    )

                    st.session_state["rating_index"] += 1
                    st.rerun()

    return st.session_state["user_ratings"]