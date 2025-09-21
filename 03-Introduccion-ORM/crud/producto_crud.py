"""
Operaciones CRUD para Producto
<<<<<<< HEAD
==============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Producto.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from ..entities.producto import Producto, ProductoCreate, ProductoUpdate
from ..database.database import get_session_context

class ProductoCRUD:
    """Clase para operaciones CRUD de Producto"""
    
    @staticmethod
    def crear_producto(producto_data: ProductoCreate) -> Producto:
        """
        Crea un nuevo producto
        
        Args:
            producto_data: Datos del producto a crear
            
        Returns:
            Producto: Producto creado
            
        Raises:
            ValueError: Si la categoría o usuario no existen
        """
        with get_session_context() as session:
            # Verificar que la categoría existe
            from .categoria_crud import CategoriaCRUD
            from .usuario_crud import UsuarioCRUD
            
            categoria = CategoriaCRUD.obtener_por_id(session, producto_data.categoria_id)
            if not categoria:
                raise ValueError(f"La categoría con ID {producto_data.categoria_id} no existe")
            
            usuario = UsuarioCRUD.obtener_por_id(session, producto_data.usuario_id)
            if not usuario:
                raise ValueError(f"El usuario con ID {producto_data.usuario_id} no existe")
            
            # Crear el producto
            producto = Producto(
                nombre=producto_data.nombre,
                descripcion=producto_data.descripcion,
                precio=producto_data.precio,
                stock=producto_data.stock,
                activo=producto_data.activo,
                categoria_id=producto_data.categoria_id,
                usuario_id=producto_data.usuario_id
            )
            
            session.add(producto)
            session.flush()  # Para obtener el ID
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def obtener_por_id(session: Session, producto_id: int, incluir_relaciones: bool = False) -> Optional[Producto]:
        """
        Obtiene un producto por su ID
        
        Args:
            session: Sesión de base de datos
            producto_id: ID del producto
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Producto o None si no existe
        """
        query = session.query(Producto).filter(Producto.id == producto_id)
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.first()
    
    @staticmethod
    def obtener_todos(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None,
        categoria_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        incluir_relaciones: bool = False
    ) -> List[Producto]:
        """
        Obtiene todos los productos con paginación y filtros
        
        Args:
            session: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            activo: Filtrar por estado activo/inactivo
            categoria_id: Filtrar por categoría
            usuario_id: Filtrar por usuario
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Lista de productos
        """
        query = session.query(Producto)
        
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        
        if categoria_id is not None:
            query = query.filter(Producto.categoria_id == categoria_id)
        
        if usuario_id is not None:
            query = query.filter(Producto.usuario_id == usuario_id)
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_productos(
        session: Session,
        termino_busqueda: str,
        skip: int = 0,
        limit: int = 100,
        incluir_relaciones: bool = False
    ) -> List[Producto]:
        """
        Busca productos por nombre o descripción
        
        Args:
            session: Sesión de base de datos
            termino_busqueda: Término a buscar
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Lista de productos que coinciden
        """
        termino = f"%{termino_busqueda}%"
        query = session.query(Producto).filter(
            or_(
                Producto.nombre.ilike(termino),
                Producto.descripcion.ilike(termino)
            )
        )
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_por_rango_precio(
        session: Session,
        precio_min: float,
        precio_max: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Producto]:
        """
        Busca productos por rango de precio
        
        Args:
            session: Sesión de base de datos
            precio_min: Precio mínimo
            precio_max: Precio máximo
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de productos en el rango de precio
        """
        return session.query(Producto).filter(
            and_(
                Producto.precio >= precio_min,
                Producto.precio <= precio_max
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_producto(producto_id: int, producto_data: ProductoUpdate) -> Optional[Producto]:
        """
        Actualiza un producto existente
        
        Args:
            producto_id: ID del producto a actualizar
            producto_data: Datos a actualizar
            
        Returns:
            Producto actualizado o None si no existe
            
        Raises:
            ValueError: Si la categoría o usuario no existen
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return None
            
            # Verificar que la categoría existe si se está actualizando
            if producto_data.categoria_id and producto_data.categoria_id != producto.categoria_id:
                from .categoria_crud import CategoriaCRUD
                categoria = CategoriaCRUD.obtener_por_id(session, producto_data.categoria_id)
                if not categoria:
                    raise ValueError(f"La categoría con ID {producto_data.categoria_id} no existe")
            
            # Verificar que el usuario existe si se está actualizando
            if producto_data.usuario_id and producto_data.usuario_id != producto.usuario_id:
                from .usuario_crud import UsuarioCRUD
                usuario = UsuarioCRUD.obtener_por_id(session, producto_data.usuario_id)
                if not usuario:
                    raise ValueError(f"El usuario con ID {producto_data.usuario_id} no existe")
            
            # Actualizar campos
            update_data = producto_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(producto, field, value)
            
            producto.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def actualizar_stock(producto_id: int, nueva_cantidad: int) -> Optional[Producto]:
        """
        Actualiza el stock de un producto
        
        Args:
            producto_id: ID del producto
            nueva_cantidad: Nueva cantidad en stock
            
        Returns:
            Producto actualizado o None si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return None
            
            producto.stock = nueva_cantidad
            producto.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def eliminar_producto(producto_id: int) -> bool:
        """
        Elimina un producto (soft delete - lo marca como inactivo)
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return False
            
            producto.activo = False
            producto.fecha_actualizacion = datetime.now()
            
            return True
    
    @staticmethod
    def eliminar_producto_permanente(producto_id: int) -> bool:
        """
        Elimina permanentemente un producto de la base de datos
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return False
            
            session.delete(producto)
            return True
    
    @staticmethod
    def contar_productos(
        session: Session,
        activo: Optional[bool] = None,
        categoria_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> int:
        """
        Cuenta el total de productos
        
        Args:
            session: Sesión de base de datos
            activo: Filtrar por estado activo/inactivo
            categoria_id: Filtrar por categoría
            usuario_id: Filtrar por usuario
            
        Returns:
            Número total de productos
        """
        query = session.query(Producto)
        
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        
        if categoria_id is not None:
            query = query.filter(Producto.categoria_id == categoria_id)
        
        if usuario_id is not None:
            query = query.filter(Producto.usuario_id == usuario_id)
        
        return query.count()
    
    @staticmethod
    def obtener_productos_bajo_stock(session: Session, stock_minimo: int = 10) -> List[Producto]:
        """
        Obtiene productos con stock bajo
        
        Args:
            session: Sesión de base de datos
            stock_minimo: Stock mínimo considerado como bajo
            
        Returns:
            Lista de productos con stock bajo
        """
        return session.query(Producto).filter(
            and_(
                Producto.stock <= stock_minimo,
                Producto.activo == True
            )
        ).all()
    
    @staticmethod
    def obtener_estadisticas(session: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas de productos
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = ProductoCRUD.contar_productos(session)
        activos = ProductoCRUD.contar_productos(session, activo=True)
        inactivos = ProductoCRUD.contar_productos(session, activo=False)
        bajo_stock = len(ProductoCRUD.obtener_productos_bajo_stock(session))
        
        # Estadísticas de precios
        precio_stats = session.query(
            func.min(Producto.precio).label('precio_min'),
            func.max(Producto.precio).label('precio_max'),
            func.avg(Producto.precio).label('precio_promedio')
        ).filter(Producto.activo == True).first()
        
        return {
            'total_productos': total,
            'productos_activos': activos,
            'productos_inactivos': inactivos,
            'productos_bajo_stock': bajo_stock,
            'precio_minimo': float(precio_stats.precio_min) if precio_stats.precio_min else 0,
            'precio_maximo': float(precio_stats.precio_max) if precio_stats.precio_max else 0,
            'precio_promedio': float(precio_stats.precio_promedio) if precio_stats.precio_promedio else 0,
            'porcentaje_activos': (activos / total * 100) if total > 0 else 0
        }
=======
"""

from typing import List, Optional
from uuid import UUID

from entities.producto import Producto
from sqlalchemy.orm import Session


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria_id: UUID,
        usuario_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Producto:
        """
        Crear un nuevo producto con validaciones

        Args:
            nombre: Nombre del producto (máximo 200 caracteres)
            descripcion: Descripción del producto
            precio: Precio del producto (debe ser positivo)
            stock: Cantidad en stock (no puede ser negativo)
            categoria_id: UUID de la categoría
            usuario_id: UUID del usuario propietario
            id_usuario_crea: UUID del usuario que crea el producto

        Returns:
            Producto creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio")

        if len(nombre) > 200:
            raise ValueError("El nombre no puede exceder 200 caracteres")

        if not descripcion or len(descripcion.strip()) == 0:
            raise ValueError("La descripción del producto es obligatoria")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        from entities.categoria import Categoria

        categoria = (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )
        if not categoria:
            raise ValueError("La categoría especificada no existe")

        from entities.usuario import Usuario

        usuario = (
            self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        )
        if not usuario:
            raise ValueError("El usuario especificado no existe")

        if id_usuario_crea is None:
            id_usuario_crea = usuario_id

        producto = Producto(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            usuario_id=usuario_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: UUID) -> Optional[Producto]:
        """
        Obtener un producto por ID

        Args:
            producto_id: UUID del producto

        Returns:
            Producto encontrado o None
        """
        return (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Obtener lista de productos con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de productos
        """
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def obtener_productos_por_categoria(self, categoria_id: UUID) -> List[Producto]:
        """
        Obtener productos por categoría

        Args:
            categoria_id: UUID de la categoría

        Returns:
            Lista de productos de la categoría
        """
        return (
            self.db.query(Producto).filter(Producto.categoria_id == categoria_id).all()
        )

    def obtener_productos_por_usuario(self, usuario_id: UUID) -> List[Producto]:
        """
        Obtener productos por usuario

        Args:
            usuario_id: UUID del usuario

        Returns:
            Lista de productos del usuario
        """
        return self.db.query(Producto).filter(Producto.usuario_id == usuario_id).all()

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Buscar productos por nombre (búsqueda parcial)

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de productos que coinciden
        """
        return self.db.query(Producto).filter(Producto.nombre.contains(nombre)).all()

    def actualizar_producto(
        self, producto_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Producto]:
        """
        Actualizar un producto con validaciones

        Args:
            producto_id: UUID del producto
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Producto actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del producto es obligatorio")
            if len(nombre) > 200:
                raise ValueError("El nombre no puede exceder 200 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs:
            descripcion = kwargs["descripcion"]
            if not descripcion or len(descripcion.strip()) == 0:
                raise ValueError("La descripción del producto es obligatoria")
            kwargs["descripcion"] = descripcion.strip()

        if "precio" in kwargs:
            precio = kwargs["precio"]
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")

        if "stock" in kwargs:
            stock = kwargs["stock"]
            if stock < 0:
                raise ValueError("El stock no puede ser negativo")

        if "categoria_id" in kwargs:
            from entities.categoria import Categoria

            categoria = (
                self.db.query(Categoria)
                .filter(Categoria.id_categoria == kwargs["categoria_id"])
                .first()
            )
            if not categoria:
                raise ValueError("La categoría especificada no existe")

        if "usuario_id" in kwargs:
            from entities.usuario import Usuario

            usuario = (
                self.db.query(Usuario)
                .filter(Usuario.id_usuario == kwargs["usuario_id"])
                .first()
            )
            if not usuario:
                raise ValueError("El usuario especificado no existe")

        if id_usuario_edita is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el producto"
                )
            id_usuario_edita = admin.id_usuario

        producto.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_stock(
        self, producto_id: UUID, nuevo_stock: int
    ) -> Optional[Producto]:
        """
        Actualizar el stock de un producto

        Args:
            producto_id: UUID del producto
            nuevo_stock: Nueva cantidad en stock

        Returns:
            Producto actualizado o None
        """
        return self.actualizar_producto(producto_id, stock=nuevo_stock)

    def eliminar_producto(self, producto_id: UUID) -> bool:
        """
        Eliminar un producto

        Args:
            producto_id: UUID del producto

        Returns:
            True si se eliminó, False si no existe
        """
        producto = self.obtener_producto(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
