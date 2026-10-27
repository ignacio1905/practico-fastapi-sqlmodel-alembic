from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import Autor, Libro
from schemas import (
    AutorCreate,
    AutorPublic,
    AutorPublicConLibros,
    AutorUpdate,
    LibroCreate,
    LibroPublic,
    LibroPublicConAutor,
    LibroUpdate,
)

# OJO: ya no hay create_all(). Las tablas las crea Alembic con `alembic upgrade head`.
app = FastAPI(
    title="API Biblioteca",
    description="Autores y libros con SQLModel + Alembic + SQLite",
)


@app.get("/")
def root():
    return {"mensaje": "API Biblioteca funcionando. Documentación en /docs"}


# =============================================================== AUTORES
@app.post("/autores", response_model=AutorPublic, status_code=status.HTTP_201_CREATED)
def crear_autor(datos: AutorCreate, session: Session = Depends(get_session)):
    autor = Autor.model_validate(datos)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor


@app.get("/autores", response_model=list[AutorPublic])
def listar_autores(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(Autor).offset(skip).limit(limit)).all()


@app.get("/autores/{autor_id}", response_model=AutorPublicConLibros)
def obtener_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@app.patch("/autores/{autor_id}", response_model=AutorPublic)
def actualizar_autor(autor_id: int, datos: AutorUpdate, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor


@app.delete("/autores/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    if autor.libros:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar un autor que tiene libros; eliminá sus libros primero",
        )
    session.delete(autor)
    session.commit()


# =============================================================== LIBROS
@app.post("/libros", response_model=LibroPublic, status_code=status.HTTP_201_CREATED)
def crear_libro(datos: LibroCreate, session: Session = Depends(get_session)):
    if session.get(Autor, datos.autor_id) is None:
        raise HTTPException(status_code=404, detail="El autor indicado no existe")
    libro = Libro.model_validate(datos)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


@app.get("/libros", response_model=list[LibroPublic])
def listar_libros(
    leido: bool | None = None,
    autor_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    consulta = select(Libro)
    if leido is not None:
        consulta = consulta.where(Libro.leido == leido)
    if autor_id is not None:
        consulta = consulta.where(Libro.autor_id == autor_id)
    return session.exec(consulta.offset(skip).limit(limit)).all()


@app.get("/libros/{libro_id}", response_model=LibroPublicConAutor)
def obtener_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@app.patch("/libros/{libro_id}", response_model=LibroPublic)
def actualizar_libro(libro_id: int, datos: LibroUpdate, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    cambios = datos.model_dump(exclude_unset=True)
    nuevo_autor = cambios.get("autor_id")
    if nuevo_autor is not None and session.get(Autor, nuevo_autor) is None:
        raise HTTPException(status_code=404, detail="El autor indicado no existe")
    for campo, valor in cambios.items():
        setattr(libro, campo, valor)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


@app.delete("/libros/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
