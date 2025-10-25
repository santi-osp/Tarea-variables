#!/usr/bin/env python3
"""
Script para crear tablas importando explicitamente todos los modelos
"""

import os
import sys
from database.config import Base, engine
from dotenv import load_dotenv
from sqlalchemy import text

# Importar todos los modelos explicitamente
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario

def crear_tablas():
    """Crear todas las tablas"""
    try:
        print("Creando tablas con modelos explicitos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("Tablas creadas exitosamente")
        
        # Verificar que las tablas se crearon
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"Tablas creadas: {', '.join(tables)}")
            
            # Verificar estructura de categorias
            print("\n=== ESTRUCTURA CATEGORIAS ===")
            try:
                result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns 
                    WHERE table_name = 'categorias'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                for col in columns:
                    print(f"  {col[0]}: {col[1]}")
            except Exception as e:
                print(f"  Error: {e}")
            
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        return False
    
    return True

def main():
    """Funcion principal"""
    print("Creando tablas con importaciones explicitas...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar que DATABASE_URL este configurada
    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL no esta configurada")
        return False
    
    # Crear tablas
    if crear_tablas():
        print("Tablas creadas exitosamente")
        return True
    else:
        print("Error al crear tablas")
        return False

if __name__ == "__main__":
    crear_tablas()
