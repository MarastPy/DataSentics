# import
import pandas as pd
import numpy as np

# load ratings
ratings = pd.read_csv('Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating'] != 0]
# Good way of filtering to remove zero ratings at the beggining.

# load books
books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip', low_memory=False)
# Allows flexibility with parsing errors in the book dataset.
# Better to use `on_bad_lines='skip'` instead of error_bad_lines=False.

# users_ratigs = pd.merge(ratings, users, on=['User-ID'])
dataset = pd.merge(ratings, books, on=['ISBN'])
dataset_lowercase = dataset.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)
# Merging datasets and normalizing text to lowercase for consistency seems like a good step.


tolkien_readers = dataset_lowercase['User-ID'][
    (dataset_lowercase['Book-Title'] == 'the fellowship of the ring (the lord of the rings, part 1)') & (
        dataset_lowercase['Book-Author'].str.contains("tolkien"))]
tolkien_readers = tolkien_readers.tolist()
tolkien_readers = np.unique(tolkien_readers)
# Good Filtering of users who have read a specific book by the same author, and deduplicating user IDs.


# final dataset
books_of_tolkien_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(tolkien_readers))]
# Good way of filtering the dataset to include only those users who read the specified books.

# Number of ratings per other books in dataset
number_of_rating_per_book = books_of_tolkien_readers.groupby(['Book-Title']).agg('count').reset_index()
# This Calculates the number of ratings for each book, which is useful for filtering.
# Useage of .count() on specific columns seems better to me then `agg('count')`.

# select only books which have actually higher number of ratings than threshold
books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
books_to_compare = books_to_compare.tolist()
# Making parametr out of 8 should be better way.

ratings_data_raw = books_of_tolkien_readers[['User-ID', 'Book-Rating', 'Book-Title']][
    books_of_tolkien_readers['Book-Title'].isin(books_to_compare)]
# Good use of filters of ratings data to include only the books of interest.
# Maybe use `.loc` to filter dataframes for clarity.

# group by User and Book and compute mean
ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
# Good use of aggregation of ratings to get average ratings per user and book.
# Make sure the data is cleaned of duplicates before aggregation.

# reset index to see User-ID in every row
ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
# Its goo that it Reshapes the dataframe to correlate calculations.
# Maybe handling  missing values (NaNs) would help dataset_for_corr.fillna('unknown'/'', inplace=True) if its a string.

LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']

result_list = []
worst_list = []

# for each of the trilogy book compute:
for LoR_book in LoR_list:

    # Take out the Lord of the Rings selected book from correlation dataframe
    dataset_of_other_books = dataset_for_corr.copy(deep=False)
    dataset_of_other_books.drop([LoR_book], axis=1, inplace=True)

    # empty lists
    book_titles = []
    correlations = []
    avgrating = []

    # corr computation
    for book_title in list(dataset_of_other_books.columns.values):
        book_titles.append(book_title)
        correlations.append(dataset_for_corr[LoR_book].corr(dataset_of_other_books[book_title]))
        tab = (ratings_data_raw[ratings_data_raw['Book-Title'] == book_title].groupby(
            ratings_data_raw['Book-Title']).mean())
        avgrating.append(tab['Book-Rating'].min())
    # final dataframe of all correlation of each book
    corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)),
                                   columns=['book', 'corr', 'avg_rating'])
    corr_fellowship.head()

    # top 10 books with highest corr
    result_list.append(corr_fellowship.sort_values('corr', ascending=False).head(10))

    # worst 10 books
    worst_list.append(corr_fellowship.sort_values('corr', ascending=False).tail(10))

print("Correlation for book:", LoR_list[0])
# print("Average rating of LOR:", ratings_data_raw[ratings_data_raw['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1'].groupby(ratings_data_raw['Book-Title']).mean()))
rslt = result_list[0]


# Overall it would be good to add error handling,
