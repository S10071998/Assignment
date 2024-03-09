from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from databases import Database
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Define SQLAlchemy models
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")


Book.reviews = relationship("Review", back_populates="book")


# Configure database URL
DATABASE_URL = "sqlite:///./test.db"

# Create database connection
database = Database(DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    book_id: int
    text: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int

    class Config:
        orm_mode = True


# Routes
@app.post("/books/", response_model=BookOut)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[BookOut])
async def read_books(
    db: Session = Depends(get_db),
    author: Optional[str] = None,
    publication_year: Optional[int] = None,
):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return query.all()


@app.post("/reviews/", response_model=ReviewOut)
async def create_review(review: ReviewCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    background_tasks.add_task(send_confirmation_email, review.text)  # Background task for sending confirmation email
    return db_review


@app.get("/reviews/", response_model=List[ReviewOut])
async def read_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for the book")
    return reviews


# Simulated function for sending confirmation email
def send_confirmation_email(review_text: str):
    print(f"Sending confirmation email for review: {review_text}")


from pydantic import BaseModel, FilePath, DirectoryPath
import os
class ConnectionConfig(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    TEMPLATE_FILE: FilePath
    MAIL_TLS: bool = False
    MAIL_SSL: bool = False

# Initialize a ConnectionConfig instance with valid file paths
conf = ConnectionConfig(
    MAIL_USERNAME="your_username",
    MAIL_PASSWORD="your_password",
    MAIL_SERVER="mail.example.com",
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FILE='text',
    MAIL_TLS=False,
    MAIL_SSL=False
)



@app.post("/test-send-email/")
async def test_send_email(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_confirmation_email, "This is a test email.")
    return {"message": "Test email sent successfully."}
