<<<<<<< HEAD
"""
Entidad Categoria
=================

Modelo de Categoria con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class Categoria(Base):
    """
    Modelo de Categoria que representa la tabla 'categorias'
    
    Atributos:
        id: Identificador único de la categoría
        nombre: Nombre de la categoría
        descripcion: Descripción detallada de la categoría
        activa: Estado de la categoría (activa/inactiva)
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """
    
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    activa = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Representación en string del objeto Categoria"""
        return f"<Categoria(id={self.id}, nombre='{self.nombre}', activa={self.activa})>"
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

# Esquemas de Pydantic para validación y serialización

class CategoriaBase(BaseModel):
    """Esquema base para Categoria"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    activa: bool = Field(True, description="Estado de la categoría")
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v

class CategoriaCreate(CategoriaBase):
    """Esquema para crear una nueva categoría"""
    pass

class CategoriaUpdate(BaseModel):
    """Esquema para actualizar una categoría existente"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    activa: Optional[bool] = None
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title() if v else v
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v

class CategoriaResponse(CategoriaBase):
    """Esquema para respuesta de categoría"""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CategoriaListResponse(BaseModel):
    """Esquema para lista de categorías"""
    categorias: List[CategoriaResponse]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True
=======
import uuid

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Campos de auditoría
    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    # Relación con productos (una categoría puede tener muchos productos)
    productos = relationship("Producto", back_populates="categoria")

    # Relaciones de auditoría
    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita,productos"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea,productos"
    )

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
