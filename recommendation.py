import pandas as pd
import random


# This function lists some books of a specific genre or lists some random books
def book_recommendation(count: int, genre: str):
    # Build new dataframe from two
    def build_chart(genre):
        df = available_genres_books[available_genres_books["genre"] == genre.lower()]
        new_df = books.set_index("book_id").loc[df.goodreads_book_id]
        return new_df

    # Lists some books from given dataframe
    def random_recommendation(df):
        list_of_books = []
        indexes = random.sample(range(len(df)), count)
        for ind in indexes:
            book = df.loc[ind]
            book_author = book.authors
            book_title = book.original_title
            list_of_books.append([book_author, book_title])
        return list_of_books

    genres = [
        "Art",
        "Biography",
        "Business",
        "Chick Lit",
        "Children's",
        "Christian",
        "Classics",
        "Comics",
        "Contemporary",
        "Cookbooks",
        "Crime",
        "Ebooks",
        "Fantasy",
        "Fiction",
        "Gay and Lesbian",
        "Graphic Novels",
        "Historical Fiction",
        "History",
        "Horror",
        "Humor and Comedy",
        "Manga",
        "Memoir",
        "Music",
        "Mystery",
        "Nonfiction",
        "Paranormal",
        "Philosophy",
        "Poetry",
        "Psychology",
        "Religion",
        "Romance",
        "Science",
        "Science Fiction",
        "Self Help",
        "Suspense",
        "Spirituality",
        "Sports",
        "Thriller",
        "Travel",
        "Young Adult",
    ]

    genres = list(map(str.lower, genres))
    if genre.lower() not in genres and genre.lower() != "random":
        return None
    else:
        # Some dataframes from https://www.kaggle.com/
        books = pd.read_csv("data/books.csv")
        book_tags = pd.read_csv("data/book_tags.csv")
        tags = pd.read_csv("data/tags.csv")

        cols = [
            "original_title",
            "authors",
            "original_publication_year",
            "average_rating",
            "ratings_count",
            "work_text_reviews_count",
        ]

        available_genres = tags.loc[tags.tag_name.str.lower().isin(genres)]
        available_genres_books = book_tags[
            book_tags.tag_id.isin(available_genres.tag_id)
        ]
        available_genres_books["genre"] = available_genres.tag_name.loc[
            available_genres_books.tag_id
        ].values

        if genre.lower() == "random":
            result = random_recommendation(books)
        else:
            genre_books = build_chart(genre)[cols]
            genre_books.to_csv("genre_books.csv", encoding="utf-8", index=False)
            genre_books = pd.read_csv("genre_books.csv")
            result = random_recommendation(genre_books)

        return result
