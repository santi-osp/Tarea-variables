"""
Sistema de gestion de productos con ORM SQLAlchemy y Neon PostgreSQL
Incluye sistema de autenticacion con login
"""

import getpass
from typing import Optional

from auth.security import PasswordManager
from crud.categoria_crud import CategoriaCRUD
from crud.producto_crud import ProductoCRUD
from crud.usuario_crud import UsuarioCRUD
from database.config import SessionLocal, create_tables
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario


class SistemaGestion:
    """Sistema de gestión por consola (menu)"""

    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.categoriaCRUD = CategoriaCRUD(self.db)
        self.productoCRUD = ProductoCRUD(self.db)
        self.usuarioCRUD = UsuarioCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

    def login(self) -> bool:
        """Mostrar el Login por consola y autentificar usuario"""
        print("°" * 50)
        print("Bienvenido a Supermercado Murcigato")
        while True:
            print("\n--- Menú de acceso ---")
            print("1. Iniciar sesión")
            print("2. Registrar usuario")
            print("0. Salir")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                intentos: int = 0
                max_intentos: int = 4

                while intentos < max_intentos:
                    try:
                        print(f"\nIntento {intentos + 1} de {max_intentos}")
                        nombre_usuario = input("Usuario o correo: ").strip()

                        if not nombre_usuario:
                            print("El campo nombre de usuario es obligatorio")
                            intentos += 1
                            continue

                        password = input("Contraseña: ")

                        if not password:
                            print("La contraseña es obligatoria")
                            intentos += 1
                            continue

                        usuario = self.usuarioCRUD.autenticar_usuario(
                            nombre_usuario, password
                        )

                        if usuario:
                            self.usuario_actual = usuario
                            print(f"\nBienvenido {usuario.nombre}")
                            if self.usuarioCRUD.es_admin(self.usuario_actual.id):
                                print("Tienes privilegios de administrador")
                            return True
                        else:
                            print("Error: información incorrecta o perfil inactivo")
                            intentos += 1

                    except KeyboardInterrupt:
                        print("\nOperación cancelada por el usuario")
                        return False
                    except Exception as e:
                        print(f"\nError durante la ejecución: {e}")
                        intentos += 1

                print("\nSe ha llegado al máximo de intentos, acceso denegado")
                return False

            elif opcion == "2":
                try:
                    print("\n--- Registro de Usuario ---")
                    nombre = input("Nombre completo: ").strip()
                    nombre_usuario = input("Nombre de usuario: ").strip()
                    email = input("Correo electrónico: ").strip()
                    telefono = input("Teléfono (opcional): ").strip() or None
                    password = input("Contraseña: ")

                    nuevo_usuario = self.usuarioCRUD.crear_usuario(
                        nombre=nombre,
                        nombre_usuario=nombre_usuario,
                        email=email,
                        telefono=telefono,
                        contraseña=password,
                    )

                    print(f"\nUsuario {nuevo_usuario.nombre} registrado con éxito!\n")

                except Exception as e:
                    print(f"\nError al registrar usuario: {e}\n")

            elif opcion == "0":
                print("\n👋 Hasta luego!\n")
                return False

            else:
                print("Opción inválida, intente de nuevo.")

    def menu_principal(self) -> None:
        """Mostrar menu principal a usuario después de iniciar sesión"""
        print("°" * 50)
        print("Menú principal")
        print("°" * 50)
        print(f"Email: {self.usuario_actual.email}")

        if self.usuarioCRUD.es_admin(self.usuario_actual.id):
            print("Administrador")
            print("°" * 50)
            print("1. Gestion de Usuarios")
            print("2. Gestion de Categorias")
            print("3. Gestion de Productos")
            print("0. Cerrar Sesion")
            print("°" * 50)

    def menu_perfil(self) -> None:
        """Mostrar el menu de perfil del usuario"""

        while True:
            print("\n" + "-_" * 40)
            print("Perfil")
            print("--" * 40)
            print("1. Ver Informacion Personal")
            print("2. Actualizar Informacion")
            print("3. Cambiar Contrasena")
            print("0. Volver al menu principal")

            op_perfil = input("\nSeleccione una opcion: ").strip()

            if op_perfil == "1":
                self.ver_informacion_personal()
            elif op_perfil == "2":
                self.actualizar_informacion_personal()
            elif op_perfil == "3":
                self.cambiar_password()
            elif op_perfil == "0":
                break
            else:
                print("Opción invalida, intente de nuevo")

    def ver_informacion_personal(self) -> None:
        """Ver informacion personal del usuario"""
        try:
            print(f"\n°^°^°^° Información del usuario °^°^°^°")
            print(f"Nombre: {self.usuario_actual.nombre}")
            print(f"Email: {self.usuario_actual.email}")
            print(f"Telefono: {self.usuario_actual.telefono}")
            print(f"Estado: {'Activo' if self.usuario_actual.activo else 'Inactivo'}")
            print(
                f"Rol: {'Administrador' if self.usuario_actual.es_admin else 'Usuario'}"
            )
            print(f"Fecha de creacion: {self.usuario_actual.fecha_creacion}")

        except Exception as e:
            print(f"Error durante la ejecución: {e}")

    def actualizar_informacion_personal(self) -> None:
        """Actualizar la informacion personal del usuario"""
        try:
            print(f"\n°^°^°^° Actualizar información personal del usuario °^°^°^°")
            print("Deje en blanco para mantener el valor actual")

            nuevo_email = input(
                f"Email actual: ({self.usuario_actual.email}): "
            ).strip()
            nuevo_telefono = input(
                f"Telefono actual: ({self.usuario_actual.telefono}): "
            ).strip()

            cambios = {}
            if nuevo_email:
                cambios["email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono

            if cambios:
                usuario_actualizado = self.usuarioCRUD.actualizar_usuario(
                    self.usuario_actual.id, **cambios
                )
                if usuario_actualizado:
                    self.usuario_actual = usuario_actualizado
                    print(f"Información actualizada exitosamente")
                else:
                    print("Error al actualizar la información")
            else:
                print("Info: No se realizaron cambios")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def cambiar_password(self) -> None:
        """Cambiar la contrasena del usuario"""

        try:
            print(f"°^°^°^° Cambiar contraseña °^°^°^°")

            password_actual = input("Contraseña actual: ")
            if not password_actual:
                print("El ingreso de la contraseña actual es obligatorio")
                return

            password_nueva = input("Nueva contraseña: ")
            if not password_nueva:
                print("El ingreso de una nueva contraseña es obligatorio")

            confirmar_password = input("Confirme la nueva contraseña: ")
            if password_nueva != confirmar_password:
                print("Las contraseñas no coinciden")
                return

            if self.usuarioCRUD.cambiar_contraseña(
                self.usuario_actual.id, password_actual, password_nueva
            ):
                print("Contraseña modificada existosamente")
            else:
                print("Error al cambiar la contraseña")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def menu_usuarios(self) -> None:
        """Mostrar menu de usuarios"""

        while True:
            print("\n" + "-_" * 40)
            print("Menú de usuarios")
            print("-_" * 30)
            print("1. Crear Usuario")
            print("2. Listar Usuarios")
            print("3. Buscar Usuario por Email")
            print("4. Actualizar Usuario")
            print("5. Crear Usuario Administrador")
            print("0. Volver al menu principal")

            op_usuario = input("\nSeleccione la opción deseada: ").strip()

            if op_usuario == "1":
                self.crear_usuario()
            elif op_usuario == "2":
                self.listar_usuarios()
            elif op_usuario == "3":
                self.buscar_usuario_por_email()
            elif op_usuario == "4":
                self.actualizar_usuario()
            elif op_usuario == "5":
                self.crear_usuario_admin()
            elif op_usuario == "0":
                break
            else:
                print("Opcion invalida, intente de nuevo")

    def crear_usuario(self) -> None:
        """Crear un nuevo usuario"""

        try:
            print("\n°^°^°^° Crear usuario °^°^°^°")
            nombre = input("Ingrese su nombre completo: ").strip()
            nombre_usuario = input("Ingrese su nombre de usuario: ").strip()
            email = input("Ingrese su correo electrónico: ").strip()
            telefono = input("Ingrese su telefono: ").strip() or None
            password = input("Ingrese una contraseña: ")
            es_admin = input("¿Es administrador? (S/N): ").strip().lower() == "s"

            usuario = self.usuarioCRUD.crear_usuario(
                nombre=nombre,
                nombre_usuario=nombre_usuario,
                email=email,
                telefono=telefono,
                contraseña=password,
                es_admin=es_admin,
            )

            print("Usuario creado de manera exitosa: {usuario}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def listar_usuarios(self) -> None:
        """Listar todos los usuarios"""
        try:
            usuarios = self.usuarioCRUD.obtener_usuarios()
            if not usuarios:
                print("No hay usuarios registrados")
                return

            print(f"\n °^°^°^° Usuarios ({len(usuarios)}) °^°^°^°")
            for i, usuario in enumerate(usuarios, 1):
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                print(
                    f"{i}. {usuario.nombre} - {usuario.email} - {activo_text}{admin_text}"
                )

        except Exception as e:
            print(f"Error: {e}")

    def buscar_usuario_por_email(self) -> None:
        """Buscar usuario por email"""
        try:
            email = input("\nIngrese el email a buscar: ").strip()
            usuario = self.usuarioCRUD.obtener_usuario_por_email(email)

            if usuario:
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                print(f"Usuario encontrado con éxito:")
                print(f"Nombre: {usuario.nombre}")
                print(f"Email: {usuario.email}")
                print(f"Telefono: {usuario.telefono or 'No especificado'}")
                print(f"Estado: {activo_text}{admin_text}")
            else:
                print("Usuario no encontrado")

        except Exception as e:
            print(f"Error: {e}")

    def actualizar_usuario(self) -> None:
        """Actualizar un usuario"""
        try:
            email = input("\nIngrese el email del usuario a actualizar: ").strip()
            usuario = self.usuarioCRUD.obtener_usuario_por_email(email)

            if not usuario:
                print("Usuario no encontrado")
                return

            print(f"\nActualizando usuario: {usuario.email}")
            print("Deje en blanco para mantener el valor actual")

            nuevo_email = input(f"Email actual ({usuario.email}): ").strip()
            nuevo_telefono = input(
                f"Telefono actual ({usuario.telefono or 'No especificado'}): "
            ).strip()

            cambios = {}
            if nuevo_email:
                cambios["email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono

            if cambios:
                usuario_actualizado = self.usuarioCRUD.actualizar_usuario(
                    usuario.id, **cambios
                )
                print(f"Usuario actualizado: {usuario_actualizado}")
            else:
                print("No se realizaron cambios")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def crear_usuario_admin(self) -> None:
        """Crear usuario administrador por defecto"""
        try:
            admin = self.usuarioCRUD.obtener_usuarios_admin()
            if admin:
                print("Ya existe un usuario administrador por defecto")
                return

            password_admin = PasswordManager.generate_secure_password(12)
            admin = self.usuarioCRUD.crear_usuario(
                nombre="Administrador del sistema",
                nombre_usuario="admin",
                email="admin@sysrem.com",
                contraseña=password_admin,
                telefono=None,
                es_admin=True,
            )
            print(f"Usuario administrador creado: {admin}")
            print(f"Contrasena temporal: {password_admin}")
            print("ADVERTENCIA: Cambie esta contrasena en su primer inicio de sesion")

        except Exception as e:
            print(f"Error: {e}")

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticacion"""
        try:
            print("Iniciando Sistema de Gestion de Productos Supermercado Murcigato...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            if not self.login():
                print("°°° Acceso denegado. Hasta luego °°°")
                return

            while True:
                self.menu_principal()
                opcion = input("\nSeleccione una opcion: ").strip()

                if opcion == "1":
                    self.menu_usuarios()
                elif opcion == "2":
                    self.menu_categorias()
                elif opcion == "3":
                    self.menu_productos()
                elif opcion == "0":
                    print("\n¡Hasta luego!")
                    break
                else:
                    print("ERROR: Opcion invalida. Intente nuevamente.")

        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario")
        except Exception as e:
            print(f"\nError critico: {e}")
        finally:
            self.db.close()

    def menu_categorias(self) -> None:
        print("\n°^°^°^° Menú categorias °^°^°^°")
        while True:
            print("1. Crear categoría")
            print("2. Ver categorías")
            print("3. Actualizar categoría")
            print("0. Volver al menu principal")

            op_cat = input("\nSeleccione una opcion: ").strip()

            if op_cat == "1":
                nombre_categoria = input("Ingrese el nombre de la categoría: ").strip()
                descripcion_categoria = input(
                    "Ingrese una descripción para la categoría: "
                ).strip()
                self.categoriaCRUD.crear_categoria(
                    nombre_categoria, descripcion_categoria
                )
            elif op_cat == "2":
                categorias = self.categoriaCRUD.obtener_categorias()
                for cat in categorias:
                    print(f"- {cat.nombre}: {cat.descripcion}")
            elif op_cat == "3":
                id_categoria = input(
                    "Ingrese el id de la categoría a actualizar: "
                ).strip()
                # Implementation for updating category
                print("Funcionalidad de actualización pendiente")
            elif op_cat == "0":
                break
            else:
                print("Opción invalida, intente de nuevo")

    def menu_productos(self) -> None:
        print("\n°^°^°^° Menú productos °^°^°^°")
        while True:
            print("1. Crear producto")
            print("2. Ver productos")
            print("3. Ver producto por id")
            print("4. Ver producto por nombre")
            print("5. Ver productos por categoría")
            print("6. Actualizar stock del producto")
            print("0. Volver al menu principal")

            op_prod = input("\nSeleccione una opcion: ").strip()

            if op_prod == "1":
                nombre_producto = input("Ingrese el nombre del producto: ").strip()
                descripcion_producto = input("Ingrese la descripción: ").strip()
                precio_producto = float(input("Ingrese el precio del producto: "))
                stock_producto = int(input("Ingrese el stock del producto: "))
                id_categoria = input(
                    "Ingrese el id de la categoría a la que pertenece el producto: "
                ).strip()
                self.productoCRUD.crear_producto(
                    nombre_producto,
                    descripcion_producto,
                    precio_producto,
                    stock_producto,
                    id_categoria,
                    self.usuario_actual.id,
                )
            elif op_prod == "2":
                productos = self.productoCRUD.obtener_productos()
                for prod in productos:
                    print(f"- {prod.nombre}: ${prod.precio} (Stock: {prod.stock})")
            elif op_prod == "3":
                id_producto = input("Ingrese el id del producto: ").strip()
                producto = self.productoCRUD.obtener_producto(id_producto)
                if producto:
                    print(f"Producto: {producto.nombre} - ${producto.precio}")
                else:
                    print("Producto no encontrado")
            elif op_prod == "4":
                nombre_producto = input("Ingrese el nombre del producto: ").strip()
                productos = self.productoCRUD.buscar_productos_por_nombre(
                    nombre_producto
                )
                for prod in productos:
                    print(f"- {prod.nombre}: ${prod.precio}")
            elif op_prod == "5":
                id_categoria = input("Ingrese el id de la categoría: ").strip()
                productos = self.productoCRUD.obtener_productos_por_categoria(
                    id_categoria
                )
                for prod in productos:
                    print(f"- {prod.nombre}: ${prod.precio}")
            elif op_prod == "6":
                id_producto = input("Ingrese el id del producto: ").strip()
                nuevo_stock = int(input("Ingrese el nuevo stock: "))
                # Implementation for updating stock
                print("Funcionalidad de actualización de stock pendiente")
            elif op_prod == "0":
                break
            else:
                print("Opción invalida, intente de nuevo")


def main():
    """Funcion principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
