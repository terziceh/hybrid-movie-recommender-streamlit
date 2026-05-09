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

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:10px;
            margin-bottom:20px;
        ">
            <p style="
                font-size:18px;
                color:#b8b8b8;
                margin-top:0px;
            ">
                Select 3–5 genres to build your movie pack.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_genres = st.multiselect(
        label="Choose your movie taste profile:",
        options=GENRES,
        max_selections=5,
        placeholder="Select genres...",
    )

    if selected_genres:

        genre_text = " • ".join(selected_genres)

        st.markdown(
            f"""
            <div style="
                text-align:center;
                margin-top:15px;
                margin-bottom:10px;
                padding:14px;
                border-radius:14px;
                background:rgba(255,255,255,0.05);
                border:1px solid rgba(255,255,255,0.08);
                font-size:16px;
                color:#f3f4f6;
            ">
                🎬 Current Taste Profile:
                <strong>{genre_text}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_genres