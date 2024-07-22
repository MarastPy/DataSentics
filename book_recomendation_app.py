import pandas as pd
from difflib import get_close_matches

# Load the data from csvs
df_ratings = pd.read_csv(r'Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
df_books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)

# Data preprocessing
# Merge ratings and books on ISBNs
df = pd.merge(df_ratings, df_books, on='ISBN')
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

# Function to get book recommendations based on user ratings
def get_recommendations(book_title, user_book_ratings):
    if book_title not in user_book_ratings:
        return "Book not found. Please try another title."

    book_ratings = user_book_ratings[book_title]
    similar_books = user_book_ratings.corrwith(book_ratings)

    # Remove NaN values and books with no valid correlation
    similar_books = similar_books.dropna()
    if similar_books.empty:
        return "No recommendations available."

    similar_books = similar_books.sort_values(ascending=False)
    recommendations = similar_books.head(10).index
    return recommendations

# Function to find the closest match for a given book title
def find_closest_match(book_title, book_titles):
    matches = get_close_matches(book_title, book_titles, n=1, cutoff=0.1)
    if matches:
        return matches[0]
    return None

print("Insert book for recommendation:")

book_title = input().strip()

if book_title:
    closest_match = find_closest_match(book_title, user_book_ratings.columns)
    if closest_match:
        recommendations = get_recommendations(closest_match, user_book_ratings)
        print(f'Did you mean: {closest_match}?')
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print('Here are some books you might like:')
            for title in recommendations:
                book_info = df_books[df_books['Book-Title'] == title].iloc[0]
                print(f"{book_info['Book-Title']} by {book_info['Book-Author']} ({book_info['Year-Of-Publication']})")
    else:
        print('No close match found. Please try another title.')
else:
    print('No book title entered.')