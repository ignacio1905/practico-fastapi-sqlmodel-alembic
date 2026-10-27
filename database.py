from sqlalchemy import event
from sqlmodel import Session, create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# check_same_thread=False: FastAPI puede atender una conexión desde distintos hilos.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def activar_foreign_keys(dbapi_connection, _connection_record):
    """SQLite ignora las Foreign Keys por defecto: hay que activarlas en cada conexión."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_session():
    """Dependencia de FastAPI: una sesión por request, se cierra sola al terminar."""
    with Session(engine) as session:
        yield session
