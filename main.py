from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import logging
import uuid
from prometheus_client import Counter, generate_latest
from fastapi import Response

app = FastAPI(title="Book Library API")

# Metrics & Logging
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("api")

# Data Model
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool = True

# Database
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949, "available": True},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "available": True},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "available": False},
    {"id": 4, "title": "Harry Potter", "author": "J.K. Rowling", "year": 1997, "available": True},
    {"id": 5, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "available": False}
]
book_id = 6

# Middleware
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    REQUEST_COUNT.inc()
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info(f"[{request_id}] Response: {response.status_code}")
    return response

# Endpoints
@app.get("/")
def home():
    return {"message": "Book Library API", "total_books": len(books)}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.post("/books", status_code=201)
def add_book(title: str, author: str, year: int):
    global book_id
    book = {"id": book_id, "title": title, "author": author, "year": year, "available": True}
    books.append(book)
    logger.info(f"Added book: {title}")
    book_id += 1
    return book

@app.get("/books", response_model=List[Book])
def get_books(available: Optional[bool] = None):
    if available is not None:
        return [b for b in books if b["available"] == available]
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return {"message": "Book deleted"}

@app.get("/stats")
def get_stats():
    total = len(books)
    available = len([b for b in books if b["available"]])
    borrowed = total - available
    return {"total": total, "available": available, "borrowed": borrowed}
