from typing import Annotated, Optional

from fastapi import Body, FastAPI, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str | None = None
    rating: int
    published_date: int

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str | None = None,
        rating: int = 0,
        published_date: int = 0,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


# Modelo de entrada con validaciones automáticas usando Pydantic
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="No necesitamos el id", default=None)
    title: str = Field(description="El título del libro", min_length=3, max_length=150)
    author: str = Field(description="El autor del libro", min_length=1)
    description: str | None = Field(default=None, description="La descripción del libro")
    rating: int = Field(description="La calificación del libro", gt=0, le=5)
    published_date: int = Field(gt=1999, le=2031)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Mi libro",
                    "author": "Autor 1",
                    "rating": 4,
                    "published_date": 2020,
                },
                {
                    "title": "Mi libro",
                    "author": "Autor 2",
                    "description": "Descripción del libro",
                    "rating": 5,
                    "published_date": 2021,
                },
            ]
        }
    }


# ============= Endpoints =============


# Leer todos los libros
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# Buscar por rating desde la query
@app.get("/books-rating", status_code=status.HTTP_200_OK)
async def read_books_by_rating_v1(rating: int = Query(gt=0, le=5)):
    books_filtered = [book for book in BOOKS if book.rating == rating]
    return books_filtered


@app.get("/books-rating/annotated", status_code=status.HTTP_200_OK)
async def read_books_by_rating_v2(rating: Annotated[int, Query(gt=0, le=5)]):
    books_filtered = [book for book in BOOKS if book.rating == rating]
    return books_filtered


# Crear un libro
@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_request: Annotated[BookRequest, Body(..., embed=True, description="The book to create")],
):
    """
    Endpoint para crear un nuevo libro en la lista de libros.

    Args:
        book_request (BookRequest): Objeto que contiene los datos del libro a crear.
            Se recibe en el body de la petición con embed=True o embed=False.

            Con embed=True (default):
            {"book_request": {"title": "Mi libro", "author": "Autor", "rating": 5}}

            Con embed=False:
            {"title": "Mi libro", "author": "Autor", "rating": 5}

    Returns:
        Book: El libro creado y agregado a la lista global de libros

    Status Codes:
        201: Libro creado exitosamente
    """
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return {"message": "Book created successfully"}


# Actualizar un libro
@app.put("/books/update-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
    book_id: Annotated[int, Path(..., gt=0, description="The ID of the book to update")],
    book: Annotated[BookRequest, Body(...)],
):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            update_book = Book(**book.model_dump())
            update_book.id = book_id
            BOOKS[i] = update_book
            return
    raise HTTPException(status_code=404, detail="Book not found")


# Eliminar un libro
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: Annotated[int, Path(..., gt=0, description="The ID of the book to delete")],
):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
    raise HTTPException(status_code=404, detail="Book not found")
