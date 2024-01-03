from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: str = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Aditya karan',
                'Description': 'this is a book',
                'rating': 5,
                'published_date': 2021
            }
        }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_title(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='ID not found')

@app.get("/book/by_author/", status_code= status.HTTP_200_OK)
async def get_by_author(author: str):
    author_lst = []
    for book in BOOKS:
        if book.author.casefold() == author.casefold():
            author_lst.append(book)
    return author_lst

@app.get("/book/{category}/")
async def get_by_category(category: str):
    category_lst = []
    for book in BOOKS:
        if book.description.casefold() == category.casefold():
            category_lst.append(book)
    return category_lst

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookReques):
    new_book = Book(**book_request.dict())
    
