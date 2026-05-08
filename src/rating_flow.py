import streamlit as st


def render_rating_flow(movies_to_rate):
    st.subheader("Rate 5 movies")

    user_ratings = []

    if movies_to_rate.empty:
        st.warning("No movies found for those genres. Try selecting different genres.")
        return user_ratings

    for _, movie in movies_to_rate.iterrows():
        st.markdown(f"### {movie['title']}")
        st.caption(f"Genres: {movie['genres']}")

        rating = st.slider(
            f"Your rating for {movie['title']}",
            min_value=0.5,
            max_value=5.0,
            value=3.0,
            step=0.5,
            key=f"rating_{movie['movieId']}",
        )

        skip = st.checkbox(
            f"Skip {movie['title']}",
            key=f"skip_{movie['movieId']}",
        )

        if not skip:
            user_ratings.append(
                {
                    "movieId": movie["movieId"],
                    "title": movie["title"],
                    "genres": movie["genres"],
                    "user_rating": rating,
                }
            )

        st.divider()

    return user_ratings