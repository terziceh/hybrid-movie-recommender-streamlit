# 🎬 CineMatch – Hybrid Movie Recommender System

## Live App
🚀 https://cinematching.streamlit.app/

---

## Overview

CineMatch is a deployed hybrid movie recommendation system built using Python, machine learning, Streamlit, and the TMDB API.  

The idea started as wanting to build something that felt more interactive than a normal recommendation list. Instead of typing random searches, users select genres, rate 5 movies, and then reveal recommendations through a “pack reveal” style interface inspired by sports card and MyTeam pack openings.

This project became a full applied data science project involving:
- recommendation systems
- collaborative filtering
- machine learning
- API integration
- feature engineering
- model deployment
- user interaction design
- inference pipelines
- lightweight production deployment

---

# 🎥 Live Demo

*(MP4/GIF demo will be added here later)*

---

# Features

- Genre-based onboarding flow
- Randomized movie rating system
- Hybrid recommendation engine
- SVD collaborative filtering
- XGBoost prediction model
- TMDB movie poster integration
- Interactive “Click to Reveal” recommendation cards
- Streamlit cloud deployment
- Lightweight deploy-ready ML pipeline

---

# Data Science Concepts Used

## Hybrid Recommendation System

The recommendation engine combines multiple approaches instead of relying on a single model.

### 1. Collaborative Filtering (SVD)

Singular Value Decomposition (SVD) was used to learn hidden relationships between users and movies from historical rating behavior.

This allows the model to recommend movies based on latent taste similarities rather than just genres.

Topics learned:
- matrix factorization
- sparse matrices
- latent feature embeddings
- recommendation ranking systems

---

### 2. XGBoost Regression Model

An XGBoost regressor was trained on engineered movie features to predict expected user ratings.

Features included:
- genre indicators
- average movie rating
- popularity signals
- rating counts

Topics learned:
- feature engineering
- supervised learning
- regression pipelines
- model persistence with joblib
- inference workflows

---

### 3. Hybrid Scoring System

Final recommendations are generated using weighted scoring:

- SVD collaborative filtering score
- XGBoost predicted score
- genre similarity score
- popularity weighting

This creates more balanced recommendations that combine:
- personalization
- movie quality
- genre alignment
- popularity confidence

---

# Recommendation Pipeline

User Flow:
1. Select genres
2. Rate 5 movies
3. Build temporary user profile
4. Generate hybrid recommendation scores
5. Rank candidate movies
6. Reveal recommendations interactively

---

# Technologies Used

## Languages
- Python

## Machine Learning
- Scikit-learn
- XGBoost
- Collaborative Filtering (SVD)

## Data Processing
- pandas
- numpy

## Frontend / Deployment
- Streamlit
- Streamlit Community Cloud

## APIs
- TMDB API

## Model Persistence
- joblib

---

# Dataset

This project uses the MovieLens dataset for movie ratings and recommendation modeling.

For deployment optimization:
- a lightweight sampled dataset was created
- deploy-ready CSVs were separated from raw datasets
- processed model data was prebuilt before deployment

This reduced deployment overhead and allowed the app to run efficiently on Streamlit Cloud.

---

# Challenges & Lessons Learned

Some of the biggest things learned during this project:

- handling sparse recommendation data
- balancing collaborative filtering with ML scoring
- debugging deployment issues
- reducing dataset size for cloud deployment
- managing model artifacts safely
- handling API failures gracefully
- designing recommendation logic that feels interactive instead of static

A lot of time was also spent learning:
- project structuring
- model pipelines
- deployment preparation
- inference optimization
- how production ML apps differ from notebook experiments

---

# Future Improvements

## Planned V2
- Full hybrid SVD + XGBoost optimization
- Better recommendation diversity
- Match confidence explanations
- Recommendation reasoning ("Because you liked...")
- Databricks + Spark pipeline rebuild
- Larger production-scale datasets
- User accounts and persistence

## Planned V3
- “Movie Night” prediction game
- Friend-based rating predictions
- Probability/odds system inspired by PrizePicks
- Social leaderboards
- Cloud-native deployment architecture

---

# Project Structure

```text
app.py
data/
    deploy/
models/
src/
requirements.txt
