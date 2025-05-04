# Importamos las clases necesarias de SQLAlchemy
from sqlalchemy import create_engine  # Para crear el motor de la base de datos
from sqlalchemy.ext.declarative import (
    declarative_base,  # Para crear modelos declarativos
)
from sqlalchemy.orm import sessionmaker  # Para crear sesiones de base de datos

# Definimos la URL de conexión a la base de datos SQLite
# El archivo se creará en el directorio actual con nombre todoapp.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todoapp.db"

# Creamos el motor de SQLAlchemy
# check_same_thread=False permite que SQLite sea accedido por múltiples hilos
# Esto es necesario para FastAPI que trabaja con múltiples hilos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creamos una clase de sesión local
# autocommit=False: Los cambios no se guardan automáticamente
# autoflush=False: Los cambios no se sincronizan automáticamente con la BD
# bind=engine: Vinculamos la sesión con nuestro motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos una clase base para los modelos declarativos
# Esta clase será la base para todas nuestras clases de modelo
Base = declarative_base()
