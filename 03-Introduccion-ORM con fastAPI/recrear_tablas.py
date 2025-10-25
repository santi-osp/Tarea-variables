#!/usr/bin/env python3
"""
Script para recrear las tablas con la estructura correcta
"""

import os
from database.config import engine
from dotenv import load_dotenv
from sqlalchemy import text

def recrear_tablas():
    """Recrear las tablas con la estructura correcta"""
    try:
        print("Eliminando tablas existentes...")
        
        with engine.connect() as conn:
            # Eliminar tablas en orden correcto (respetando foreign keys)
            tablas = ['productos', 'categorias', 'tbl_usuarios']
            
            for tabla in tablas:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {tabla} CASCADE;"))
                    print(f"  Tabla {tabla} eliminada")
                except Exception as e:
                    print(f"  Error al eliminar {tabla}: {e}")
            
            # Confirmar cambios
            conn.commit()
            print("Tablas eliminadas exitosamente")
            
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")
        return False
    
    return True

def main():
    """Funcion principal"""
    print("Recreando tablas...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar que DATABASE_URL este configurada
    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL no esta configurada")
        return False
    
    # Recrear tablas
    if recrear_tablas():
        print("Tablas eliminadas. Ahora ejecuta setup_simple.py para recrearlas.")
        return True
    else:
        print("Error al eliminar tablas")
        return False

if __name__ == "__main__":
    recrear_tablas()
