from fastapi import Body, FastAPI


app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/book")
async def read_all_book():
    return BOOKS

@app.get("/books/{book_category}")
async def read_book(book_category:str):
    for book in BOOKS:
        if book.get('category').casefold() == book_category.casefold():
            return book

@app.get("/books/")
async def read_book_by_query(category:str):
    book_lst = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            book_lst.append(book)
    return book_lst

@app.get("/book/byauthor/")
async def read_by_author(author:str):
    book_lst = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            book_lst.append(book)
    return book_lst








