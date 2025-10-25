#!/usr/bin/env python3
"""
Script para configurar la base de datos
"""

import os
import sys

from database.config import Base, engine
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def setup_database():
    """Configurar la base de datos creando todas las tablas"""
    try:
        print("Creando tablas en la base de datos...")

        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)

        print("✅ Tablas creadas exitosamente")

        # Verificar que las tablas se crearon
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
                )
            )

            tables = [row[0] for row in result]
            print(f"📋 Tablas creadas: {', '.join(tables)}")

    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        return False

    return True


def main():
    """Función principal"""
    print("🚀 Configurando base de datos...")

    # Cargar variables de entorno
    load_dotenv()

    # Verificar que DATABASE_URL esté configurada
    if not os.getenv("DATABASE_URL"):
        print("❌ Error: DATABASE_URL no está configurada en las variables de entorno")
        print("   Crea un archivo .env con tu URL de base de datos")
        return False

    # Configurar la base de datos
    if setup_database():
        print("🎉 Base de datos configurada exitosamente")
        return True
    else:
        print("💥 Error al configurar la base de datos")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

