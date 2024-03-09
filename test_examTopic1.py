import unittest
from fastapi.testclient import TestClient
from examTopic1 import app, books_db, reviews_db

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.book_data = {
            "title": "Sample Book",
            "author": "John Doe",
            "publication_year": 2022
        }
        self.review_data = {
            "book_title": "Sample Book",
            "text": "This is a sample review.",
            "rating": 5
        }
        # Clear the in-memory databases before each test
        books_db.clear()
        reviews_db.clear()

    def test_add_book(self):
        response = self.client.post("/books/", json=self.book_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), self.book_data)
        self.assertEqual(len(books_db), 1)

    def test_submit_review(self):
        # Add a book first
        self.client.post("/books/", json=self.book_data)
        response = self.client.post("/reviews/", json=self.review_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), self.review_data)
        self.assertEqual(len(reviews_db), 1)

    def test_get_books(self):
        # Add a book first
        self.client.post("/books/", json=self.book_data)
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.book_data])

    def test_get_reviews(self):
        # Add a book and its review first
        self.client.post("/books/", json=self.book_data)
        self.client.post("/reviews/", json=self.review_data)
        response = self.client.get(f"/reviews/{self.book_data['title']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.review_data])

if __name__ == "__main__":
    unittest.main()
