import streamlit as st


def render_pack_reveal(recommendations):
    st.header("🎬 Your Movie Pack Reveal")

    if recommendations.empty:
        st.warning("No recommendations found.")
        return

    for _, movie in recommendations.iterrows():

        with st.container(border=True):

            st.subheader(movie["title"])

            st.write(f"🎭 Genres: {movie['genres']}")

            st.write(
                f"⭐ Average Rating: {round(movie['avg_rating'], 2)}"
            )

            st.write(
                f"👥 Ratings Count: {int(movie['rating_count'])}"
            )

            reveal = st.button(
                f"Reveal Recommendation: {movie['title']}",
                key=f"reveal_{movie['movieId']}",
            )

            if reveal:
                st.success(
                    f"You unlocked: {movie['title']} 🍿"
                )

                st.balloons()