# Configuración de Base de Datos

## Problema Identificado

El error `column productos.id_producto does not exist` indica que las tablas no se han creado correctamente en la base de datos.

## Solución

### 1. Crear archivo .env

Crea un archivo `.env` en la carpeta `03-Introduccion-ORM con fastAPI/` con el siguiente contenido:

```env
# Configuración de la base de datos
DATABASE_URL=postgresql://usuario:password@host:puerto/nombre_base_datos

# Ejemplo para PostgreSQL local:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/sistema_gestion

# Ejemplo para Neon (PostgreSQL en la nube):
# DATABASE_URL=postgresql://usuario:password@ep-xxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 2. Instalar dependencias

```bash
cd "03-Introduccion-ORM con fastAPI"
pip install -r requirements.txt
```

### 3. Configurar la base de datos

Ejecuta el script de configuración:

```bash
python setup_database.py
```

### 4. Verificar la configuración

El script creará todas las tablas necesarias:
- `categorias`
- `tbl_usuarios` 
- `productos`

### 5. Ejecutar el servidor

```bash
python main.py
```

## Estructura de Tablas

### Categorias
- `id_categoria` (UUID, PK)
- `nombre` (String)
- `descripcion` (Text)
- `activa` (Boolean)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)

### Usuarios (tbl_usuarios)
- `id` (UUID, PK)
- `nombre` (String)
- `email` (String)
- `telefono` (String)
- `activo` (Boolean)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)
- `nombre_usuario` (String)
- `contrasena_hash` (String)
- `es_admin` (Boolean)

### Productos
- `id_producto` (UUID, PK)
- `nombre` (String)
- `descripcion` (Text)
- `precio` (Numeric)
- `stock` (Integer)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)
- `categoria_id` (UUID, FK)
- `usuario_id` (UUID, FK)
- `id_usuario_crea` (UUID, FK)
- `id_usuario_edita` (UUID, FK)

## Solución de Problemas

### Error: "DATABASE_URL no está configurada"
- Asegúrate de crear el archivo `.env` con la URL correcta
- Verifica que la URL de conexión sea válida

### Error: "No se puede conectar a la base de datos"
- Verifica que el servidor de base de datos esté ejecutándose
- Confirma que las credenciales sean correctas
- Para Neon, asegúrate de que la URL incluya `?sslmode=require`

### Error: "Tabla ya existe"
- Esto es normal si ya ejecutaste el script anteriormente
- El script es idempotente (se puede ejecutar múltiples veces)

## Próximos Pasos

1. Configura la base de datos siguiendo los pasos anteriores
2. Ejecuta el backend: `python main.py`
3. Ejecuta el frontend: `npm start` (en la carpeta 04-Frontend-angular)
4. Prueba el login con las credenciales de prueba

