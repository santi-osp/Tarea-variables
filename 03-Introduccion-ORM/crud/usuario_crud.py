"""
Operaciones CRUD para Usuario
<<<<<<< HEAD
=============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Usuario.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from ..database.database import get_session_context

class UsuarioCRUD:
    """Clase para operaciones CRUD de Usuario"""
    
    @staticmethod
    def crear_usuario(usuario_data: UsuarioCreate) -> Usuario:
        """
        Crea un nuevo usuario
        
        Args:
            usuario_data: Datos del usuario a crear
            
        Returns:
            Usuario: Usuario creado
            
        Raises:
            ValueError: Si el email ya existe
        """
        with get_session_context() as session:
            # Verificar si el email ya existe
            if UsuarioCRUD.obtener_por_email(session, usuario_data.email):
                raise ValueError(f"El email {usuario_data.email} ya está registrado")
            
            # Crear el usuario
            usuario = Usuario(
                nombre=usuario_data.nombre,
                email=usuario_data.email,
                telefono=usuario_data.telefono,
                activo=usuario_data.activo
            )
            
            session.add(usuario)
            session.flush()  # Para obtener el ID
            session.refresh(usuario)
            
            return usuario
    
    @staticmethod
    def obtener_por_id(session: Session, usuario_id: int) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID
        
        Args:
            session: Sesión de base de datos
            usuario_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return session.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def obtener_por_email(session: Session, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email
        
        Args:
            session: Sesión de base de datos
            email: Email del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return session.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def obtener_todos(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> List[Usuario]:
        """
        Obtiene todos los usuarios con paginación
        
        Args:
            session: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            activo: Filtrar por estado activo/inactivo
            
        Returns:
            Lista de usuarios
        """
        query = session.query(Usuario)
        
        if activo is not None:
            query = query.filter(Usuario.activo == activo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_usuarios(
        session: Session,
        termino_busqueda: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Usuario]:
        """
        Busca usuarios por nombre o email
        
        Args:
            session: Sesión de base de datos
            termino_busqueda: Término a buscar
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de usuarios que coinciden
        """
        termino = f"%{termino_busqueda}%"
        return session.query(Usuario).filter(
            or_(
                Usuario.nombre.ilike(termino),
                Usuario.email.ilike(termino)
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        """
        Actualiza un usuario existente
        
        Args:
            usuario_id: ID del usuario a actualizar
            usuario_data: Datos a actualizar
            
        Returns:
            Usuario actualizado o None si no existe
            
        Raises:
            ValueError: Si el email ya existe en otro usuario
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return None
            
            # Verificar si el email ya existe en otro usuario
            if usuario_data.email and usuario_data.email != usuario.email:
                usuario_existente = UsuarioCRUD.obtener_por_email(session, usuario_data.email)
                if usuario_existente:
                    raise ValueError(f"El email {usuario_data.email} ya está registrado")
            
            # Actualizar campos
            update_data = usuario_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(usuario, field, value)
            
            usuario.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(usuario)
            
            return usuario
    
    @staticmethod
    def eliminar_usuario(usuario_id: int) -> bool:
        """
        Elimina un usuario (soft delete - lo marca como inactivo)
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return False
            
            usuario.activo = False
            usuario.fecha_actualizacion = datetime.now()
            
            return True
    
    @staticmethod
    def eliminar_usuario_permanente(usuario_id: int) -> bool:
        """
        Elimina permanentemente un usuario de la base de datos
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return False
            
            session.delete(usuario)
            return True
    
    @staticmethod
    def contar_usuarios(session: Session, activo: Optional[bool] = None) -> int:
        """
        Cuenta el total de usuarios
        
        Args:
            session: Sesión de base de datos
            activo: Filtrar por estado activo/inactivo
            
        Returns:
            Número total de usuarios
        """
        query = session.query(Usuario)
        
        if activo is not None:
            query = query.filter(Usuario.activo == activo)
        
        return query.count()
    
    @staticmethod
    def obtener_estadisticas(session: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas de usuarios
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = UsuarioCRUD.contar_usuarios(session)
        activos = UsuarioCRUD.contar_usuarios(session, activo=True)
        inactivos = UsuarioCRUD.contar_usuarios(session, activo=False)
        
        return {
            'total_usuarios': total,
            'usuarios_activos': activos,
            'usuarios_inactivos': inactivos,
            'porcentaje_activos': (activos / total * 100) if total > 0 else 0
        }
=======
"""

import re
from typing import List, Optional, Tuple
from uuid import UUID

from auth.security import PasswordManager
from entities.usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    #
    def _validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono"""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """Validar formato de nombre de usuario"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

    def crear_usuario(
        self,
        nombre: str,
        nombre_usuario: str,
        email: str,
        contraseña: str,
        telefono: str = None,
        es_admin: bool = False,
    ) -> Usuario:
        """
        Crear un nuevo usuario con validaciones

        Args:
            nombre: Nombre del usuario (máximo 100 caracteres)
            nombre_usuario: Nombre de usuario único (3-20 caracteres, alfanumérico y _)
            email: Email válido y único
            contraseña: Contraseña segura
            telefono: Teléfono opcional (formato internacional)
            es_admin: Si es administrador

        Returns:
            Usuario creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
            raise ValueError(
                "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
            )

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        if not contraseña:
            raise ValueError("La contraseña es obligatoria")

        es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
        if not es_valida:
            raise ValueError(f"Contraseña inválida: {mensaje}")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        contraseña_hash = PasswordManager.hash_password(contraseña)

        usuario = Usuario(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.lower().strip(),
            contraseña_hash=contraseña_hash,
            telefono=telefono.strip() if telefono else None,
            es_admin=es_admin,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """
        Obtener un usuario por ID

        Args:
            usuario_id: UUID del usuario

        Returns:
            Usuario encontrado o None
        """
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtener un usuario por email

        Args:
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        """
        Obtener un usuario por nombre de usuario

        Args:
            nombre_usuario: Nombre de usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def autenticar_usuario(
        self, nombre_usuario: str, contraseña: str
    ) -> Optional[Usuario]:
        """
        Autenticar un usuario con nombre de usuario y contraseña

        Args:
            nombre_usuario: Nombre de usuario o email
            contraseña: Contraseña en texto plano

        Returns:
            Usuario autenticado o None si las credenciales son inválidas
        """
        # Buscar por nombre de usuario o email
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        if PasswordManager.verify_password(contraseña, usuario.contraseña_hash):
            return usuario

        return None

    def cambiar_contraseña(
        self, usuario_id: UUID, contraseña_actual: str, nueva_contraseña: str
    ) -> bool:
        """
        Cambiar la contraseña de un usuario

        Args:
            usuario_id: UUID del usuario
            contraseña_actual: Contraseña actual
            nueva_contraseña: Nueva contraseña

        Returns:
            True si se cambió exitosamente, False en caso contrario

        Raises:
            ValueError: Si la contraseña actual es incorrecta o la nueva es inválida
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not PasswordManager.verify_password(
            contraseña_actual, usuario.contraseña_hash
        ):
            raise ValueError("La contraseña actual es incorrecta")

        es_valida, mensaje = PasswordManager.validate_password_strength(
            nueva_contraseña
        )
        if not es_valida:
            raise ValueError(f"Nueva contraseña inválida: {mensaje}")

        usuario.contraseña_hash = PasswordManager.hash_password(nueva_contraseña)
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Obtener lista de usuarios con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de usuarios
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        """
        Actualizar un usuario con validaciones

        Args:
            usuario_id: UUID del usuario
            **kwargs: Campos a actualizar

        Returns:
            Usuario actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_por_email(email)
                and self.obtener_usuario_por_email(email).id != usuario_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self._validar_telefono(kwargs["telefono"]):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "nombre_usuario" in kwargs:
            nombre_usuario = kwargs["nombre_usuario"]
            if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
                raise ValueError(
                    "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
                )
            if (
                self.obtener_usuario_por_nombre_usuario(nombre_usuario)
                and self.obtener_usuario_por_nombre_usuario(nombre_usuario).id
                != usuario_id
            ):
                raise ValueError("El nombre de usuario ya está registrado")
            kwargs["nombre_usuario"] = nombre_usuario.strip().lower()

        if "contraseña" in kwargs:
            contraseña = kwargs["contraseña"]
            es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
            if not es_valida:
                raise ValueError(f"Contraseña inválida: {mensaje}")
            kwargs["contraseña_hash"] = PasswordManager.hash_password(contraseña)
            del kwargs["contraseña"]  # Eliminar la contraseña en texto plano

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """
        Eliminar un usuario

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si se eliminó, False si no existe
        """
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """
        Desactivar un usuario (soft delete)

        Args:
            usuario_id: UUID del usuario

        Returns:
            Usuario desactivado o None
        """
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """
        Obtener todos los usuarios administradores

        Returns:
            Lista de usuarios administradores
        """
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        """
        Verificar si un usuario es administrador

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si es administrador, False en caso contrario
        """
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """
        Obtener el usuario administrador por defecto

        Returns:
            Usuario administrador por defecto o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
