# Práctico FastAPI 5: SQLModel y Alembic

API de biblioteca con **autores** y **libros** (relación 1 a N con Foreign Key),
usando FastAPI, SQLModel (en lugar de SQLAlchemy puro) y Alembic para migraciones.

## Estructura

- `database.py`: engine, activación de foreign keys en SQLite y dependencia `get_session`
- `schemas.py`: clases de SQLModel que no son tablas (Create / Update / Public) y los schemas anidados
  (`AutorPublicConLibros`, `LibroPublicConAutor`)
- `models.py`: tablas `Autor` y `Libro` (`table=True`), con `Libro.autor_id` como Foreign Key
- `main.py`: endpoints CRUD de autores y libros
- `alembic/` y `alembic.ini`: configuración de migraciones; `alembic/versions/` tiene la migración inicial

## Cómo correrlo

```bash
python -m venv .venv
.venv\Scripts\activate          # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head            # crea biblioteca.db con las tablas
uvicorn main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

## Migraciones con Alembic

```bash
alembic upgrade head                                   # aplicar migraciones
alembic downgrade -1                                   # deshacer la última
alembic current                                        # ver en qué versión está la base
alembic history                                        # listar migraciones
alembic revision --autogenerate -m "describir cambio"  # generar una nueva tras tocar los modelos
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/autores` | Crear autor |
| GET | `/autores` | Listar autores |
| GET | `/autores/{id}` | Autor **con sus libros anidados** |
| PATCH | `/autores/{id}` | Actualizar autor |
| DELETE | `/autores/{id}` | Eliminar autor (409 si tiene libros) |
| POST | `/libros` | Crear libro (requiere `autor_id` existente) |
| GET | `/libros` | Listar (filtros `?leido=` y `?autor_id=`) |
| GET | `/libros/{id}` | Libro **con su autor anidado** |
| PATCH | `/libros/{id}` | Actualizar libro |
| DELETE | `/libros/{id}` | Eliminar libro |
