"""Modelos de tabla (table=True). Relación: un Autor tiene muchos Libros."""
from typing import List, Optional

from sqlmodel import Field, Relationship

from schemas import AutorBase, LibroBase


class Autor(AutorBase, table=True):
    __tablename__ = "autores"

    id: Optional[int] = Field(default=None, primary_key=True)

    libros: List["Libro"] = Relationship(back_populates="autor")


class Libro(LibroBase, table=True):
    __tablename__ = "libros"

    id: Optional[int] = Field(default=None, primary_key=True)
    autor_id: int = Field(foreign_key="autores.id")

    autor: Optional["Autor"] = Relationship(back_populates="libros")
