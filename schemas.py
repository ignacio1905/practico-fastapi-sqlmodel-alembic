"""Clases de SQLModel que NO son tablas: se usan como schemas de entrada/salida de la API."""
from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------- Autor
class AutorBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=100, index=True)
    nacionalidad: str | None = Field(default=None, max_length=50)


class AutorCreate(AutorBase):
    pass


class AutorUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    nacionalidad: str | None = Field(default=None, max_length=50)


class AutorPublic(AutorBase):
    id: int


# ---------------------------------------------------------------- Libro
class LibroBase(SQLModel):
    titulo: str = Field(min_length=1, max_length=200, index=True)
    anio: int | None = Field(default=None, ge=0, le=2100)
    genero: str | None = Field(default=None, max_length=50)
    leido: bool = False


class LibroCreate(LibroBase):
    autor_id: int


class LibroUpdate(SQLModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    anio: int | None = Field(default=None, ge=0, le=2100)
    genero: str | None = Field(default=None, max_length=50)
    leido: bool | None = None
    autor_id: int | None = None


class LibroPublic(LibroBase):
    id: int
    autor_id: int


# ------------------------------------------------- Schemas con datos anidados
class AutorPublicConLibros(AutorPublic):
    """Un autor con la lista de sus libros adentro."""

    libros: list[LibroPublic] = []


class LibroPublicConAutor(LibroPublic):
    """Un libro con los datos completos de su autor adentro."""

    autor: AutorPublic | None = None
