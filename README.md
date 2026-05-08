# 🎬 Hybrid Movie Recommender Streamlit MVP

## Overview

This project is an interactive movie recommendation application built with Streamlit using MovieLens data.  

The long-term goal is to evolve this into a hybrid recommendation platform combining:

- Collaborative Filtering (SVD)
- XGBoost reranking
- Recommendation explanations
- Movie poster APIs
- Interactive “movie pack reveal” UX
- Databricks/Spark scalable pipeline architecture

---

# ✅ Current MVP Features

## Interactive User Flow

Users can:

1. Select 3–5 favorite genres
2. Receive 5 random movies to rate
3. Submit ratings
4. Generate personalized recommendations
5. Reveal recommendations in a “pack reveal” style interface

---

# ✅ Current Architecture

## Frontend

- Streamlit

## Data

- MovieLens dataset
- Sampled ratings subset for fast MVP performance

## Current Recommendation Logic

Baseline recommendation engine using:

- Genre filtering
- Average movie rating
- Rating count popularity weighting
- Genre match scoring
- User preference weighting

---

# ✅ Project Structure

app.py
src/
    config.py
    data_loader.py
    genre_selector.py
    movie_pool.py
    rating_flow.py
    recommender.py
    pack_reveal.py
data/
    raw/
    processed/
models/


---

# ✅ Completed Tonight

* Project setup
* Virtual environment setup
* Streamlit app structure
* Modular file architecture
* Data preprocessing pipeline
* Genre selection UI
* Movie rating workflow
* Recommendation pipeline
* Pack reveal interface
* GitHub repository setup
* `.gitignore` cleanup
* Sampled MovieLens processing for MVP speed

---

# 🚧 Next Steps (Tomorrow)

## Recommendation System Upgrades

* Integrate SVD collaborative filtering model
* Integrate XGBoost reranking layer
* Build true hybrid recommendation scoring

---

## UI / UX Improvements

* Add TMDB API movie posters
* Improve recommendation cards
* Add animations and transitions
* Improve “pack reveal” experience
* Add loading states/spinners

---

## Recommendation Intelligence

* “Because you liked...” explanations
* Similar movie reasoning
* Better genre weighting
* Movie embedding similarity
* Recommendation confidence scoring

---

# 🚧 Future Roadmap

## V2

* Databricks + Spark pipeline
* Medallion architecture
* Model artifact storage
* Real-time recommendation serving

## V3

* Movie night prediction game
* Friend recommendation battles
* Probability/odds system
* Social recommendation platform

---

# 🛠 Tech Stack

* Python
* Streamlit
* pandas
* scikit-learn
* XGBoost
* MovieLens dataset

---

# 📌 Notes

The current MVP uses sampled MovieLens data for fast local development.
Full-scale recommendation training and hybrid modeling will be integrated in future versions.

```
```
