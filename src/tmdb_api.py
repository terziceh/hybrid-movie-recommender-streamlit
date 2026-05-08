import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
}

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def clean_movie_title(title):
    return re.sub(r"\s*\(\d{4}\)", "", title).strip()


def extract_year(title):
    match = re.search(r"\((\d{4})\)", title)

    if match:
        return match.group(1)

    return None


def get_movie_poster(title):
    clean_title = clean_movie_title(title)
    year = extract_year(title)

    params = {
        "query": clean_title
    }

    if year:
        params["year"] = year

    try:
        response = requests.get(
            SEARCH_URL,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        data = response.json()

        if not data["results"]:
            return None

        movie = data["results"][0]

        poster_path = movie.get("poster_path")

        if not poster_path:
            return None

        return f"{IMAGE_BASE_URL}{poster_path}"

    except Exception as e:
        print(e)
        return None