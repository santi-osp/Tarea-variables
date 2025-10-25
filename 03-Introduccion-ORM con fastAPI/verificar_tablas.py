#!/usr/bin/env python3
"""
Script para verificar la estructura de las tablas
"""

import os
from database.config import engine
from dotenv import load_dotenv
from sqlalchemy import text

def verificar_tablas():
    """Verificar la estructura de las tablas"""
    try:
        print("Verificando estructura de las tablas...")
        
        with engine.connect() as conn:
            # Verificar tabla categorias
            print("\n=== TABLA CATEGORIAS ===")
            try:
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'categorias'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                if columns:
                    for col in columns:
                        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
                else:
                    print("  No se encontraron columnas")
            except Exception as e:
                print(f"  Error al verificar categorias: {e}")
            
            # Verificar tabla productos
            print("\n=== TABLA PRODUCTOS ===")
            try:
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'productos'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                if columns:
                    for col in columns:
                        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
                else:
                    print("  No se encontraron columnas")
            except Exception as e:
                print(f"  Error al verificar productos: {e}")
            
            # Verificar tabla usuarios
            print("\n=== TABLA USUARIOS ===")
            try:
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'tbl_usuarios'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                if columns:
                    for col in columns:
                        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
                else:
                    print("  No se encontraron columnas")
            except Exception as e:
                print(f"  Error al verificar usuarios: {e}")
            
    except Exception as e:
        print(f"Error general: {e}")
        return False
    
    return True

def main():
    """Funcion principal"""
    print("Verificando estructura de base de datos...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar que DATABASE_URL este configurada
    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL no esta configurada")
        return False
    
    # Verificar tablas
    if verificar_tablas():
        print("\nVerificacion completada")
        return True
    else:
        print("\nError en la verificacion")
        return False

if __name__ == "__main__":
    verificar_tablas()
