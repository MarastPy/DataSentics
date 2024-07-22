import streamlit as st
import pandas as pd
import numpy as np
from numpy.linalg import norm

# Sample data (you can replace this with your dataset)

# Function to recommend books
def recommend_books(title, books_df, num_recommendations=5):
    vocab = build_vocab(books_df['description'])
    book_vectors = books_df['description'].apply(lambda x: vectorize(x, vocab))

    book_idx = books_df[books_df['title'] == title].index[0]
    book_vector = book_vectors[book_idx]

    similarities = book_vectors.apply(lambda x: cosine_similarity(book_vector, x))
    similar_books = similarities.sort_values(ascending=False).index[1:num_recommendations + 1]

    return books_df['title'].iloc[similar_books]


# Streamlit UI
st.title("Book Recommendation System")
st.write("Enter your favorite book and get a list of recommended books.")

favorite_book = st.text_input("Favorite Book")
if st.button("Recommend"):
    if favorite_book in books['title'].values:
        recommendations = recommend_books(favorite_book, books)
        st.write("Recommended Books:")
        for book in recommendations:
            st.write(book)
    else:
        st.write("Book not found in our dataset. Please try another book.")

# streamlit run streamlitapp.py
