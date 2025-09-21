<<<<<<< HEAD
"""
Módulo de entidades
==================

Este módulo contiene todas las entidades del sistema usando SQLAlchemy
y sus esquemas de validación con Pydantic.
"""

from .usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from .categoria import Categoria, CategoriaCreate, CategoriaUpdate, CategoriaResponse
from .producto import Producto, ProductoCreate, ProductoUpdate, ProductoResponse

__all__ = [
    # Usuario
    'Usuario', 'UsuarioCreate', 'UsuarioUpdate', 'UsuarioResponse',
    # Categoria
    'Categoria', 'CategoriaCreate', 'CategoriaUpdate', 'CategoriaResponse',
    # Producto
    'Producto', 'ProductoCreate', 'ProductoUpdate', 'ProductoResponse'
]
=======
# Módulo de entidades del modelo de datos

>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
