from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Data models
class Book(BaseModel):
    title: str
    author: str
    publication_year: int


class Review(BaseModel):
    book_title: str
    text: str
    rating: int


# In-memory storage for books and reviews (replace with a database in a real-world scenario)
books_db = []
reviews_db = []


# Endpoints

@app.post("/books/", response_model=Book, status_code=201)
def add_book(book: Book):
    """
    Add a new book to the system.
    """
    books_db.append(book)
    return book


@app.post("/reviews/", response_model=Review, status_code=201)
def submit_review(review: Review):
    """
    Submit a review for a book.
    """
    # Check if the book exists
    for book in books_db:
        if book.title == review.book_title:
            reviews_db.append(review)
            return review
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", response_model=List[Book])
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    """
    Retrieve all books with optional filters for author and publication year.
    """
    filtered_books = books_db
    if author:
        filtered_books = [book for book in filtered_books if book.author == author]
    if publication_year:
        filtered_books = [book for book in filtered_books if book.publication_year == publication_year]
    return filtered_books


@app.get("/reviews/{book_title}", response_model=List[Review])
def get_reviews(book_title: str):
    """
    Retrieve all reviews for a specific book.
    """
    book_reviews = [review for review in reviews_db if review.book_title == book_title]
    if not book_reviews:
        raise HTTPException(status_code=404, detail="No reviews found for the book")
    return book_reviews


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
