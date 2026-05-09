import os
import re
import time
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def clean_movie_title(title):
    title = str(title)
    title = re.sub(r"\s*\(\d{4}\)", "", title).strip()

    article_patterns = {
        ", The": "The ",
        ", A": "A ",
        ", An": "An ",
    }

    for suffix, prefix in article_patterns.items():
        if title.endswith(suffix):
            title = prefix + title[: -len(suffix)]
            break

    title = title.replace("&", "and")
    title = title.replace("·", "")
    title = re.sub(r"\s+", " ", title)

    return title.strip()


def extract_year(title):
    match = re.search(r"\((\d{4})\)", str(title))
    return match.group(1) if match else None


def request_tmdb(params, headers, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(
                SEARCH_URL,
                headers=headers,
                params=params,
                timeout=10,
            )

            if response.status_code == 200:
                return response

            print("TMDB status error:", response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            print(f"TMDB request failed attempt {attempt + 1}: {e}")
            time.sleep(1)

    return None


@st.cache_data(show_spinner=False)
def get_movie_poster(title):
    if not TMDB_BEARER_TOKEN:
        print("ERROR: TMDB_BEARER_TOKEN is missing")
        return None

    clean_title = clean_movie_title(title)
    year = extract_year(title)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    }

    search_attempts = []

    if year:
        search_attempts.append(
            {
                "query": clean_title,
                "year": year,
                "include_adult": False,
            }
        )

    search_attempts.append(
        {
            "query": clean_title,
            "include_adult": False,
        }
    )

    for params in search_attempts:
        response = request_tmdb(params, headers)

        if response is None:
            continue

        data = response.json()
        results = data.get("results", [])

        print("Searching:", clean_title, year)
        print("Status:", response.status_code)
        print("Results found:", len(results))

        if not results:
            continue

        if year:
            for movie in results:
                poster_path = movie.get("poster_path")
                release_date = movie.get("release_date", "")

                if poster_path and release_date.startswith(year):
                    poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    print("Poster found:", poster_url)
                    return poster_url

        for movie in results:
            poster_path = movie.get("poster_path")

            if poster_path:
                poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                print("Poster found:", poster_url)
                return poster_url

    print("No poster found for:", title)
    return None