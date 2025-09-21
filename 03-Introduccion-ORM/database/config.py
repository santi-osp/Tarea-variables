"""
<<<<<<< HEAD
Configuración de la base de datos
=================================

Configuraciones centralizadas para la conexión a la base de datos.
"""

import os
from typing import Optional

# URL de la base de datos
# Por defecto usa SQLite, pero puede cambiarse por PostgreSQL, MySQL, etc.
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./ejemplo_orm.db"
)

# Configuraciones adicionales
DB_ECHO: bool = os.getenv("DB_ECHO", "True").lower() == "true"
DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

# Configuraciones específicas para diferentes entornos
class DatabaseConfig:
    """Configuración de base de datos para diferentes entornos"""
    
    @staticmethod
    def get_sqlite_config(db_name: str = "ejemplo_orm.db") -> str:
        """Configuración para SQLite (desarrollo)"""
        return f"sqlite:///./{db_name}"
    
    @staticmethod
    def get_postgresql_config(
        host: str = "localhost",
        port: int = 5432,
        database: str = "ejemplo_orm",
        username: str = "postgres",
        password: str = "password"
    ) -> str:
        """Configuración para PostgreSQL (producción)"""
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def get_mysql_config(
        host: str = "localhost",
        port: int = 3306,
        database: str = "ejemplo_orm",
        username: str = "root",
        password: str = "password"
    ) -> str:
        """Configuración para MySQL"""
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
=======
Configuración de la base de datos PostgreSQL con Neon
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
    connect_args={"sslmode": "require"},  # Requerir SSL para Neon
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
