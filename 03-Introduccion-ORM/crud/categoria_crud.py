"""
<<<<<<< HEAD
Operaciones CRUD para Categoria
===============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Categoria.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from ..database.database import get_session_context

class CategoriaCRUD:
    """Clase para operaciones CRUD de Categoria"""
    
    @staticmethod
    def crear_categoria(categoria_data: CategoriaCreate) -> Categoria:
        """
        Crea una nueva categoría
        
        Args:
            categoria_data: Datos de la categoría a crear
            
        Returns:
            Categoria: Categoría creada
            
        Raises:
            ValueError: Si el nombre ya existe
        """
        with get_session_context() as session:
            # Verificar si el nombre ya existe
            if CategoriaCRUD.obtener_por_nombre(session, categoria_data.nombre):
                raise ValueError(f"La categoría '{categoria_data.nombre}' ya existe")
            
            # Crear la categoría
            categoria = Categoria(
                nombre=categoria_data.nombre,
                descripcion=categoria_data.descripcion,
                activa=categoria_data.activa
            )
            
            session.add(categoria)
            session.flush()  # Para obtener el ID
            session.refresh(categoria)
            
            return categoria
    
    @staticmethod
    def obtener_por_id(session: Session, categoria_id: int) -> Optional[Categoria]:
        """
        Obtiene una categoría por su ID
        
        Args:
            session: Sesión de base de datos
            categoria_id: ID de la categoría
            
        Returns:
            Categoria o None si no existe
        """
        return session.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    @staticmethod
    def obtener_por_nombre(session: Session, nombre: str) -> Optional[Categoria]:
        """
        Obtiene una categoría por su nombre
        
        Args:
            session: Sesión de base de datos
            nombre: Nombre de la categoría
            
        Returns:
            Categoria o None si no existe
        """
        return session.query(Categoria).filter(Categoria.nombre == nombre).first()
    
    @staticmethod
    def obtener_todas(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        activa: Optional[bool] = None
    ) -> List[Categoria]:
        """
        Obtiene todas las categorías con paginación
        
        Args:
            session: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            activa: Filtrar por estado activa/inactiva
            
        Returns:
            Lista de categorías
        """
        query = session.query(Categoria)
        
        if activa is not None:
            query = query.filter(Categoria.activa == activa)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_categorias(
        session: Session,
        termino_busqueda: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Categoria]:
        """
        Busca categorías por nombre o descripción
        
        Args:
            session: Sesión de base de datos
            termino_busqueda: Término a buscar
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de categorías que coinciden
        """
        termino = f"%{termino_busqueda}%"
        return session.query(Categoria).filter(
            or_(
                Categoria.nombre.ilike(termino),
                Categoria.descripcion.ilike(termino)
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_categoria(categoria_id: int, categoria_data: CategoriaUpdate) -> Optional[Categoria]:
        """
        Actualiza una categoría existente
        
        Args:
            categoria_id: ID de la categoría a actualizar
            categoria_data: Datos a actualizar
            
        Returns:
            Categoría actualizada o None si no existe
            
        Raises:
            ValueError: Si el nombre ya existe en otra categoría
        """
        with get_session_context() as session:
            categoria = CategoriaCRUD.obtener_por_id(session, categoria_id)
            
            if not categoria:
                return None
            
            # Verificar si el nombre ya existe en otra categoría
            if categoria_data.nombre and categoria_data.nombre != categoria.nombre:
                categoria_existente = CategoriaCRUD.obtener_por_nombre(session, categoria_data.nombre)
                if categoria_existente:
                    raise ValueError(f"La categoría '{categoria_data.nombre}' ya existe")
            
            # Actualizar campos
            update_data = categoria_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(categoria, field, value)
            
            categoria.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(categoria)
            
            return categoria
    
    @staticmethod
    def eliminar_categoria(categoria_id: int) -> bool:
        """
        Elimina una categoría (soft delete - la marca como inactiva)
        
        Args:
            categoria_id: ID de la categoría a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            categoria = CategoriaCRUD.obtener_por_id(session, categoria_id)
            
            if not categoria:
                return False
            
            categoria.activa = False
            categoria.fecha_actualizacion = datetime.now()
            
            return True
    
    @staticmethod
    def eliminar_categoria_permanente(categoria_id: int) -> bool:
        """
        Elimina permanentemente una categoría de la base de datos
        
        Args:
            categoria_id: ID de la categoría a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            categoria = CategoriaCRUD.obtener_por_id(session, categoria_id)
            
            if not categoria:
                return False
            
            session.delete(categoria)
            return True
    
    @staticmethod
    def contar_categorias(session: Session, activa: Optional[bool] = None) -> int:
        """
        Cuenta el total de categorías
        
        Args:
            session: Sesión de base de datos
            activa: Filtrar por estado activa/inactiva
            
        Returns:
            Número total de categorías
        """
        query = session.query(Categoria)
        
        if activa is not None:
            query = query.filter(Categoria.activa == activa)
        
        return query.count()
    
    @staticmethod
    def obtener_categorias_con_productos(session: Session) -> List[Categoria]:
        """
        Obtiene categorías que tienen productos asociados
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Lista de categorías con productos
        """
        return session.query(Categoria).filter(
            Categoria.productos.any()
        ).all()
    
    @staticmethod
    def obtener_estadisticas(session: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas de categorías
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = CategoriaCRUD.contar_categorias(session)
        activas = CategoriaCRUD.contar_categorias(session, activa=True)
        inactivas = CategoriaCRUD.contar_categorias(session, activa=False)
        con_productos = len(CategoriaCRUD.obtener_categorias_con_productos(session))
        
        return {
            'total_categorias': total,
            'categorias_activas': activas,
            'categorias_inactivas': inactivas,
            'categorias_con_productos': con_productos,
            'porcentaje_activas': (activas / total * 100) if total > 0 else 0
        }
=======
Operaciones CRUD para Categoría
"""

from typing import List, Optional
from uuid import UUID

from entities.categoria import Categoria
from sqlalchemy.orm import Session


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self, nombre: str, descripcion: str = None, id_usuario_crea: UUID = None
    ) -> Categoria:
        """
        Crear una nueva categoría con validaciones

        Args:
            nombre: Nombre de la categoría (único, máximo 100 caracteres)
            descripcion: Descripción opcional
            id_usuario_crea: UUID del usuario que crea la categoría

        Returns:
            Categoría creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_categoria_por_nombre(nombre):
            raise ValueError("Ya existe una categoría con ese nombre")

        if id_usuario_crea is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la categoría"
                )
            id_usuario_crea = admin.id_usuario

        categoria = Categoria(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, categoria_id: UUID) -> Optional[Categoria]:
        """
        Obtener una categoría por ID

        Args:
            categoria_id: UUID de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )

    def obtener_categoria_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """
        Obtener una categoría por nombre

        Args:
            nombre: Nombre de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria).filter(Categoria.nombre == nombre.strip()).first()
        )

    def obtener_categorias(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """
        Obtener lista de categorías con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de categorías
        """
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def actualizar_categoria(
        self, categoria_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Categoria]:
        """
        Actualizar una categoría con validaciones

        Args:
            categoria_id: UUID de la categoría
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Categoría actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la categoría es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            if (
                self.obtener_categoria_por_nombre(nombre)
                and self.obtener_categoria_por_nombre(nombre).id_categoria
                != categoria_id
            ):
                raise ValueError("Ya existe una categoría con ese nombre")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs and kwargs["descripcion"]:
            kwargs["descripcion"] = kwargs["descripcion"].strip()

        if id_usuario_edita is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la categoría"
                )
            id_usuario_edita = admin.id_usuario

        categoria.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, categoria_id: UUID) -> bool:
        """
        Eliminar una categoría

        Args:
            categoria_id: UUID de la categoría

        Returns:
            True si se eliminó, False si no existe
        """
        categoria = self.obtener_categoria(categoria_id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
