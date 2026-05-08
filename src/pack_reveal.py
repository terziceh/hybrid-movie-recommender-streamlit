import streamlit as st

from src.tmdb_api import get_movie_poster


def render_pack_reveal(recommendations):
    if "revealed_cards" not in st.session_state:
        st.session_state["revealed_cards"] = set()

    st.markdown("## 🎬 Your Movie Pack Reveal")

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            width: 100%;
            height: 420px;
            border-radius: 24px;
            font-weight: 800;
            font-size: 22px;
            background: linear-gradient(145deg, #202026, #09090c);
            border: 2px solid rgba(255,255,255,0.18);
            box-shadow: 0 15px 35px rgba(0,0,0,0.45);
            transition: 0.2s ease-in-out;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 0 35px rgba(155, 92, 255, 0.75);
            border: 2px solid rgba(155, 92, 255, 1);
        }

        .movie-title {
            font-size: 16px;
            font-weight: 800;
            margin-top: 10px;
            text-align: center;
            line-height: 1.2;
        }

        .movie-meta {
            color: #b8b8b8;
            font-size: 12px;
            text-align: center;
            line-height: 1.2;
            margin-top: 6px;
        }

        img {
            border-radius: 22px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.45);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5)

    for i, (_, movie) in enumerate(recommendations.head(5).iterrows()):
        movie_title = movie["title"]
        movie_genres = movie.get("genres", "Unknown")
        avg_rating = movie.get("avg_rating", movie.get("average_rating", None))
        rating_count = movie.get("rating_count", movie.get("ratings_count", None))

        with cols[i]:
            if i in st.session_state["revealed_cards"]:
                poster_url = get_movie_poster(movie_title)

                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.markdown("### 🎬 No Poster Found")

                st.markdown(
                    f'<div class="movie-title">{movie_title}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="movie-meta">🎭 {movie_genres}</div>',
                    unsafe_allow_html=True,
                )

                if avg_rating is not None:
                    st.markdown(
                        f'<div class="movie-meta">⭐ {avg_rating:.2f}</div>',
                        unsafe_allow_html=True,
                    )

                if rating_count is not None:
                    st.markdown(
                        f'<div class="movie-meta">👥 {int(rating_count)} ratings</div>',
                        unsafe_allow_html=True,
                    )

            else:
                if st.button(
                    "🎞️\n\nClick to Reveal",
                    key=f"reveal_card_{i}",
                    use_container_width=True,
                ):
                    st.session_state["revealed_cards"].add(i)
                    st.rerun()