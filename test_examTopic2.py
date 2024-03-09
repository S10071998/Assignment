import unittest
from fastapi.testclient import TestClient
from examTopic2 import app, get_db, Book, Review, SessionLocal, engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

# Create a test database session
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestDBSession = SessionTest()

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        # Create test data
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_year": 2022
        }
        self.review_data = {
            "book_id": 1,
            "text": "Test Review",
            "rating": 5
        }

    def test_create_book(self):
        with patch("main.get_db", return_value=TestDBSession):
            response = self.client.post("/books/", json=self.book_data)
            self.assertEqual(response.status_code, 200)
            book = response.json()
            self.assertIn("id", book)
            self.assertEqual(book["title"], self.book_data["title"])

    def test_read_books(self):
        # Insert a book into the test database
        with patch("main.get_db", return_value=TestDBSession):
            TestDBSession.execute(Book.__table__.insert(), self.book_data)
            TestDBSession.commit()

            response = self.client.get("/books/")
            self.assertEqual(response.status_code, 200)
            books = response.json()
            self.assertIsInstance(books, list)
            self.assertEqual(len(books), 1)
            self.assertEqual(books[0]["title"], self.book_data["title"])

    def test_create_review(self):
        # Insert a book into the test database
        with patch("main.get_db", return_value=TestDBSession):
            TestDBSession.execute(Book.__table__.insert(), self.book_data)
            TestDBSession.commit()

            # Update review data with the correct book_id
            self.review_data["book_id"] = TestDBSession.query(Book).first().id

            response = self.client.post("/reviews/", json=self.review_data)
            self.assertEqual(response.status_code, 200)
            review = response.json()
            self.assertIn("id", review)
            self.assertEqual(review["text"], self.review_data["text"])

    def test_read_reviews(self):
        # Insert a review into the test database
        with patch("main.get_db", return_value=TestDBSession):
            TestDBSession.execute(Review.__table__.insert(), self.review_data)
            TestDBSession.commit()

            response = self.client.get(f"/reviews/?book_id={self.review_data['book_id']}")
            self.assertEqual(response.status_code, 200)
            reviews = response.json()
            self.assertIsInstance(reviews, list)
            self.assertEqual(len(reviews), 1)
            self.assertEqual(reviews[0]["text"], self.review_data["text"])

if __name__ == "__main__":
    unittest.main()
