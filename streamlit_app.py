import pandas as pd
import streamlit as st
from difflib import get_close_matches

# Load the data from csvs
keggle = 'False'

# Reading Keggle or sd datasets
if keggle == 'True':
    df_ratings = pd.read_csv(r'Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
    df_books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
else:
    df_ratings = pd.read_csv(r'Keggle downloads/Ratings.csv', encoding='cp1251', sep=',')
    df_books = pd.read_csv('Keggle downloads/Books.csv', encoding='cp1251', sep=',', on_bad_lines='skip', low_memory=False)

# Display the title
st.title('Welcome to the Book Recommendation Page')

# Data preprocessing
# REmove 0 ratings
df_ratings = df_ratings[df_ratings['Book-Rating'] != 0]
# Merge ratings and books on ISBNs
df = pd.merge(df_ratings, df_books, on='ISBN')
# Remove duplicates
df = df.drop_duplicates()
# Replace single backslash '\' with an empty string in 'Book-Title' column
df['Book-Title'] = df['Book-Title'].str.replace(r'\\', '', regex=True)

df = df[['User-ID', 'ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Book-Rating']]

# Filter to include only users, and books with a minimum number of ratings
min_book_ratings = 50
min_user_ratings = 50

book_counts = df['Book-Title'].value_counts()
user_counts = df['User-ID'].value_counts()

filtered_books = book_counts[book_counts >= min_book_ratings].index
filtered_users = user_counts[user_counts >= min_user_ratings].index

df_filtered = df[df['Book-Title'].isin(filtered_books) & df['User-ID'].isin(filtered_users)]

# Create a pivot table
user_book_ratings = df_filtered.pivot_table(index='User-ID', columns='Book-Title', values='Book-Rating')

# Get book recommendations based on user ratings
def get_recommendations(book_title, user_book_ratings):
    if book_title not in user_book_ratings:
        return "Book not found. Please try another title."

    book_ratings = user_book_ratings[book_title]
    similar_books = user_book_ratings.corrwith(book_ratings)
    similar_books = similar_books.dropna().sort_values(ascending=False)

    recommendations = similar_books.head(10).index
    return recommendations

# Find the closest match for a given book titl
def find_closest_match(book_title, book_titles):
    matches = get_close_matches(book_title, book_titles, n=1, cutoff=0.1)
    if matches:
        return matches[0]
    return None

# Header
st.header('Find Your Next Book')

# Input for book title
book_title = st.text_input('Enter a book title you like')

# Display recommendations
if book_title:
    closest_match = find_closest_match(book_title, user_book_ratings.columns)
    if closest_match:
        recommendations = get_recommendations(closest_match, user_book_ratings)
        st.write(f'If you mean {closest_match}')
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            st.write('Here are some books you might like:')
            for title in recommendations:
                book_info = df_books[df_books['Book-Title'] == title]
                if not book_info.empty:
                    book_info = book_info.iloc[0]
                    st.write(
                        f"{book_info['Book-Title']} by {book_info['Book-Author']} ({book_info['Year-Of-Publication']})")
                else:
                    st.write(f"Information for the book '{title}' is not available.")
    else:
        st.write('No close match found. Please try another title.')

# To run the app type in terminal: streamlit run streamlit_app.py