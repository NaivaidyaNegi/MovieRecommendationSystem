import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.title("🎬 Movie Recommendation System")

@st.cache(allow_output_mutation=True)
def load_data():
    movie_df = pickle.load(open("Required/movie_recm.pkl", "rb"))
    similarity = pickle.load(open("Required/similarity.pkl", "rb"))
    return movie_df, similarity

def get_recommendations(movie_df, similarity, movie):
    index = movie_df[movie_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [movie_df.iloc[i[0]].title for i in distances[1:6]]
    recommended_urls = [movie_df.iloc[i[0]].urls for i in distances[1:6]]
    return recommended_movies, recommended_urls

movie_df, similarity = load_data()

list_movie = np.array(movie_df["title"])
option = st.selectbox("🍿 Select a Movie", list_movie)

if st.button('🔍 Search') and option:
    st.write('Movies Recommended for you are:')
    recommended_movies, recommended_urls = get_recommendations(movie_df, similarity, option)
    df = pd.DataFrame({
        'Movie Recommended': recommended_movies,
        'Movie Url': recommended_urls
    })
    st.table(df)

import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('Required/back.jpg')
