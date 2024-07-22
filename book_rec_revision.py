import pandas as pd
import numpy as np

'''
1.Načítání dat a zpracování chyb:

Parametr error_bad_lines=False v pd.read_csv je zastaralý. Mělo by se použít on_bad_lines='skip'.

books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='s

2.Filtr hodnocení:

Místo filtrování nula hodnocení by se mohlo použít query pro lepší čitelnost.

ratings = ratings.query('Book-Rating != 0')

3. Efektivnější normalizace textu:

Použití str.lower() přímo na sloupce typu object může být rychlejší.

dataset_lowercase = dataset.applymap(lambda x: x.lower() if isinstance(x, str) else x)
'''

# load ratings
ratings = pd.read_csv('Downloads/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings.query('Book-Rating != 0')

# load books
books = pd.read_csv('Downloads/BX-Books.csv', encoding='cp1251', sep=';', on_bad_lines='skip')

# merge datasets
dataset = pd.merge(ratings, books, on='ISBN')
dataset_lowercase = dataset.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# find Tolkien readers
tolkien_readers = dataset_lowercase['User-ID'][
    (dataset_lowercase['Book-Title'] == 'the fellowship of the ring (the lord of the rings, part 1)') &
    (dataset_lowercase['Book-Author'].str.contains('tolkien'))
    ]
tolkien_readers = np.unique(tolkien_readers)

# books read by Tolkien readers
books_of_tolkien_readers = dataset_lowercase[dataset_lowercase['User-ID'].isin(tolkien_readers)]

# number of ratings per book
number_of_rating_per_book = books_of_tolkien_readers.groupby('Book-Title').size().reset_index(name='count')
books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['count'] >= 8]

# ratings data for correlation
ratings_data_raw = books_of_tolkien_readers[
    books_of_tolkien_readers['Book-Title'].isin(books_to_compare)
][['User-ID', 'Book-Rating', 'Book-Title']]

# average ratings per user-book pair
ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'], as_index=False).mean()

# pivot to create user-book matrix
dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')

LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']

result_list = []
worst_list = []

# compute correlations
for LoR_book in LoR_list:
    dataset_of_other_books = dataset_for_corr.drop(columns=[LoR_book])

    book_titles = []
    correlations = []
    avgrating = []

    for book_title in dataset_of_other_books.columns:
        book_titles.append(book_title)
        correlation = dataset_for_corr[LoR_book].corr(dataset_of_other_books[book_title])
        correlations.append(correlation if not np.isnan(correlation) else 0)
        avgrating.append(ratings_data_raw.query(f'`Book-Title` == "{book_title}"')['Book-Rating'].mean())

    corr_fellowship = pd.DataFrame({
        'book': book_titles,
        'corr': correlations,
        'avg_rating': avgrating
    }).sort_values('corr', ascending=False)

    result_list.append(corr_fellowship.head(10))
    worst_list.append(corr_fellowship.tail(10))

print("Correlation for book:", LoR_list[0])
rslt = result_list[0]
print(rslt)
