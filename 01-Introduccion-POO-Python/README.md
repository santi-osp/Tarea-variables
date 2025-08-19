# Módulo 1: Introducción a la Programación Orientada a Objetos (POO) en Python

## Objetivos
- Comprender los fundamentos de POO
- Aprender a crear clases y objetos en Python
- Entender encapsulación, herencia y polimorfismo

## Contenido

### 1. ¿Qué es la POO?
La Programación Orientada a Objetos es un paradigma de programación que organiza el código en objetos, los cuales representan entidades del mundo real o conceptos abstractos. En lugar de escribir código como una serie de instrucciones lineales, organizamos nuestro programa en "cosas" (objetos) que tienen características (atributos) y pueden hacer acciones (métodos).

**Imagina que estás diseñando un videojuego:**
- En lugar de tener variables separadas para `nombre_jugador`, `vida_jugador`, `posicion_x`, `posicion_y`
- Creas un objeto `Jugador` que contiene toda esa información y puede `moverse()`, `atacar()`, `curarse()`

**La POO nos permite:**
- **Modelar problemas de forma natural**: Pensar en el mundo real como objetos que interactúan
- **Reutilizar código**: Crear una clase `Vehiculo` y usarla para `Carro`, `Moto`, `Bicicleta`
- **Mantener código ordenado y modular**: Cada clase tiene una responsabilidad específica
- **Aplicar herencia, polimorfismo, encapsulación**: Principios que hacen el código más robusto

### 2. Conceptos Básicos

**Piensa en una clase como un molde o plantilla, y en un objeto como algo creado con ese molde.**

| Concepto | Descripción | Ejemplo del Mundo Real |
|----------|-------------|------------------------|
| **Clase** | Plantilla que define atributos y métodos | `Molde de Galleta` - define qué forma y sabor tendrán todas las galletas |
| **Objeto** | Instancia de una clase | `Galleta específica` - una galleta real creada con el molde |
| **Atributos** | Variables asociadas a un objeto | `Color`, `sabor`, `tamaño` de la galleta |
| **Métodos** | Funciones que definen comportamiento | `comer()`, `partir()`, `hornear()` |
| **self** | Referencia al propio objeto | Como decir "yo mismo" - la galleta sabe que es ella misma |

**Ejemplo práctico:**
- **Clase**: `Molde de Casa` (define que todas las casas tengan paredes, techo, puerta)
- **Objeto**: `Mi Casa` (una casa específica con paredes blancas, techo rojo, puerta de madera)
- **Atributos**: `color_paredes = "blanco"`, `color_techo = "rojo"`, `material_puerta = "madera"`
- **Métodos**: `abrir_puerta()`, `cerrar_ventana()`, `encender_luz()`

### 3. Creación de Clases y Objetos

**Vamos a crear nuestra primera clase paso a paso. Piensa en crear un "molde" para personas.**

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        return f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años."

# Crear objetos
persona1 = Persona("Alejandro", 25)
persona2 = Persona("Laura", 30)

print(persona1.saludar())  # Hola, mi nombre es Alejandro y tengo 25 años.
print(persona2.saludar())  # Hola, mi nombre es Laura y tengo 30 años.
```

**Explicación detallada:**

1. **`class Persona:`** - Estamos creando un molde llamado "Persona"
2. **`def __init__(self, nombre, edad):`** - Este es el constructor, se ejecuta automáticamente cuando creamos una persona
3. **`self.nombre = nombre`** - Guardamos el nombre que recibimos en el atributo `nombre` del objeto
4. **`self`** - Siempre es el primer parámetro y representa al objeto que se está creando
5. **`def saludar(self):`** - Un método que la persona puede hacer

**Analogía del mundo real:**
- **Clase**: Es como un formulario en blanco para registrar empleados
- **Constructor**: Es como llenar el formulario con datos específicos
- **Objeto**: Es el formulario ya llenado con información de una persona específica
- **Método**: Es como una acción que esa persona puede realizar

**Otros ejemplos de clases que podrías crear:**
- `Producto` (nombre, precio, stock)
- `Libro` (titulo, autor, año, paginas)
- `Cuenta` (usuario, contraseña, email)

### 4. Encapsulación

**La encapsulación es como poner información importante en una caja fuerte. Solo se puede acceder a ella a través de métodos específicos y seguros.**

**¿Por qué es importante?**
Imagina que tienes una cuenta bancaria. No quieres que cualquiera pueda cambiar tu saldo directamente. Solo quieres que se pueda modificar a través de operaciones controladas como depositar o retirar.

```python
class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.__saldo = saldo  # Atributo privado (doble guión bajo)

    def depositar(self, cantidad):
        if cantidad > 0:  # Validación
            self.__saldo += cantidad
            return f"Depósito exitoso. Saldo: ${self.__saldo}"
        else:
            return "Cantidad inválida"

    def retirar(self, cantidad):
        if cantidad > 0 and cantidad <= self.__saldo:
            self.__saldo -= cantidad
            return f"Retiro exitoso. Saldo: ${self.__saldo}"
        else:
            return "Fondos insuficientes o cantidad inválida"

    def mostrar_saldo(self):
        return f"Saldo actual: ${self.__saldo}"

# Uso de la clase
cuenta = CuentaBancaria("Alejandro", 1000)
print(cuenta.depositar(500))    # Depósito exitoso. Saldo: $1500
print(cuenta.retirar(200))      # Retiro exitoso. Saldo: $1300
print(cuenta.mostrar_saldo())   # Saldo actual: $1300

# Esto NO funcionaría (atributo privado):
# cuenta.__saldo = 10000  # Error!
```

**Explicación de la encapsulación:**

1. **`self.__saldo`** - El doble guión bajo hace que `__saldo` sea privado
2. **No se puede acceder directamente** - Solo a través de métodos controlados
3. **Validaciones** - Los métodos verifican que las operaciones sean válidas
4. **Control total** - Tú decides cómo se puede modificar el saldo

**Analogías del mundo real:**
- **Caja fuerte**: Solo se abre con la combinación correcta (métodos)
- **Cápsula de medicina**: Protege el contenido y solo se libera cuando debe
- **Control remoto del carro**: Solo puedes hacer ciertas acciones, no puedes modificar el motor directamente

**Otros ejemplos de encapsulación:**
- **Clase `Estudiante`**: `__promedio` solo se modifica a través de `agregar_nota()`
- **Clase `Producto`**: `__stock` solo se modifica a través de `vender()` o `reponer()`
- **Clase `Usuario`**: `__contraseña` solo se modifica a través de `cambiar_contraseña()`

### 5. Herencia

**La herencia es como crear una familia de clases. Una clase "hija" hereda todo de su clase "padre" y puede agregar o modificar comportamientos.**

**¿Por qué usar herencia?**
Imagina que estás creando un juego con diferentes tipos de vehículos. Todos tienen características comunes (marca, modelo, velocidad) pero cada uno tiene comportamientos específicos. En lugar de repetir código, creas una clase base y las demás heredan de ella.

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.energia = 100

    def hacer_sonido(self):
        return "Hace un sonido."

    def comer(self):
        self.energia += 20
        return f"{self.nombre} come y recupera energía. Energía: {self.energia}"

class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre)  # Llamar al constructor del padre
        self.raza = raza

    def hacer_sonido(self):
        return "Guau"

    def jugar(self):
        if self.energia >= 20:
            self.energia -= 20
            return f"{self.nombre} juega felizmente. Energía: {self.energia}"
        else:
            return f"{self.nombre} está muy cansado para jugar"

class Gato(Animal):
    def __init__(self, nombre, color):
        super().__init__(nombre)
        self.color = color

    def hacer_sonido(self):
        return "Miau"

    def ronronear(self):
        return f"{self.nombre} ronronea suavemente"

# Crear instancias
perro = Perro("Firulais", "Labrador")
gato = Gato("Mishito", "Naranja")

print(f"{perro.nombre} ({perro.raza}): {perro.hacer_sonido()}")
print(f"{gato.nombre} ({gato.color}): {gato.hacer_sonido()}")

# Usar métodos heredados
print(perro.comer())  # Método heredado de Animal
print(gato.comer())   # Método heredado de Animal

# Usar métodos específicos
print(perro.jugar())
print(gato.ronronear())
```

**Explicación de la herencia:**

1. **`class Perro(Animal):`** - `Perro` hereda de `Animal` (todo lo que tiene Animal, lo tiene Perro)
2. **`super().__init__(nombre)`** - Llama al constructor del padre para inicializar atributos comunes
3. **Métodos heredados** - `Perro` y `Gato` pueden usar `comer()` sin definirlo
4. **Métodos específicos** - Cada clase puede tener métodos únicos como `jugar()` o `ronronear()`

**Analogías del mundo real:**
- **Clase padre**: Es como un "plan maestro" de construcción
- **Clase hija**: Es como una versión específica que agrega detalles
- **Herencia**: Es como heredar genes de tus padres y agregar características propias

**Otros ejemplos de herencia:**
- **`Vehiculo`** → `Carro`, `Moto`, `Bicicleta` (todos tienen motor, ruedas, pero diferentes comportamientos)
- **`Empleado`** → `Gerente`, `Vendedor`, `Contador` (todos tienen nombre, salario, pero diferentes responsabilidades)
- **`Forma`** → `Circulo`, `Rectangulo`, `Triangulo` (todos tienen área, pero se calcula diferente)

### 6. Polimorfismo

**El polimorfismo significa "muchas formas". Es la capacidad de que diferentes objetos respondan de manera diferente al mismo método, dependiendo de su tipo específico.**

**¿Por qué es útil?**
Imagina que tienes una lista de diferentes tipos de animales y quieres que todos hagan sonido. Cada uno responde de forma diferente, pero puedes tratarlos a todos igual. Es como tener un control universal que funciona con diferentes dispositivos.

```python
# Usando las clases de Animal, Perro y Gato del ejemplo anterior

def hacer_animal_hablar(animal):
    """Esta función funciona con CUALQUIER tipo de animal"""
    return f"{animal.nombre} dice: {animal.hacer_sonido()}"

# Crear diferentes tipos de animales
animales = [
    Perro("Boby", "Pastor Alemán"),
    Gato("Luna", "Siames"),
    Animal("Criatura Misteriosa")
]

print("Demostrando polimorfismo:")
for animal in animales:
    print(hacer_animal_hablar(animal))

# También funciona con listas mixtas
vehiculos = [
    Carro("Toyota", "Corolla"),
    Moto("Yamaha", "MT-07"),
    Bicicleta("Trek", "Mountain")
]

print("\nDescripción de vehículos:")
for vehiculo in vehiculos:
    print(f"  {vehiculo.descripcion()}")
```

**Explicación del polimorfismo:**

1. **Mismo método, diferentes respuestas**: `hacer_sonido()` devuelve "Guau" para perros, "Miau" para gatos
2. **Función genérica**: `hacer_animal_hablar()` funciona con cualquier animal sin importar su tipo
3. **Flexibilidad**: Puedes agregar nuevos tipos de animales sin cambiar el código existente

**Analogías del mundo real:**
- **Control remoto universal**: Funciona con TV, DVD, aire acondicionado (cada uno responde diferente)
- **Enchufe eléctrico**: Diferentes dispositivos se conectan al mismo enchufe pero funcionan de manera distinta
- **Lenguaje humano**: La palabra "correr" significa algo diferente para un atleta, un niño o un animal

**Otros ejemplos de polimorfismo:**
- **`calcular_area()`**: Diferente para círculo, rectángulo, triángulo
- **`reproducir()`**: Diferente para video, audio, imagen
- **`guardar()`**: Diferente para documento, imagen, base de datos

**Ventajas del polimorfismo:**
- **Código más limpio**: No necesitas verificar el tipo de cada objeto
- **Fácil de extender**: Agregar nuevos tipos no rompe el código existente
- **Mantenimiento**: Cambios en un tipo no afectan a otros

### 7. Ejemplo Completo - Sistema de Vehículos

**Ahora vamos a crear un sistema completo que combine todos los conceptos que hemos aprendido: clases, objetos, herencia, encapsulación y polimorfismo.**

**¿Qué vamos a crear?**
Un sistema de gestión de vehículos para una empresa de alquiler. Todos los vehículos tienen características comunes pero comportamientos específicos.

```python
class Vehiculo:
    def __init__(self, marca, modelo, año):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.__kilometraje = 0  # Atributo privado
        self.disponible = True

    def obtener_info(self):
        return f"{self.marca} {self.modelo} ({self.año})"

    def alquilar(self):
        if self.disponible:
            self.disponible = False
            return f"{self.obtener_info()} ha sido alquilado"
        else:
            return f"{self.obtener_info()} no está disponible"

    def devolver(self, km_recorridos):
        if not self.disponible:
            self.disponible = True
            self.__kilometraje += km_recorridos
            return f"{self.obtener_info()} devuelto. KM totales: {self.__kilometraje}"
        else:
            return f"{self.obtener_info()} ya está disponible"

    def mostrar_estado(self):
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"{self.obtener_info()} - Estado: {estado} - KM: {self.__kilometraje}"

class Carro(Vehiculo):
    def __init__(self, marca, modelo, año, num_puertas):
        super().__init__(marca, modelo, año)
        self.num_puertas = num_puertas
        self.tipo_combustible = "Gasolina"

    def obtener_info(self):
        return f"Carro: {self.marca} {self.modelo} ({self.año}) - {self.num_puertas} puertas"

    def cargar_combustible(self):
        return f"{self.obtener_info()} está cargando {self.tipo_combustible}"

class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, cilindrada):
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada
        self.tipo_combustible = "Gasolina"

    def obtener_info(self):
        return f"Moto: {self.marca} {self.modelo} ({self.año}) - {self.cilindrada}cc"

    def cargar_combustible(self):
        return f"{self.obtener_info()} está cargando {self.tipo_combustible}"

class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, año, tipo):
        super().__init__(marca, modelo, año)
        self.tipo = tipo  # "Montaña", "Ruta", "Urbana"
        self.tipo_combustible = "Humano"

    def obtener_info(self):
        return f"Bicicleta: {self.marca} {self.modelo} ({self.año}) - {self.tipo}"

    def cargar_combustible(self):
        return f"{self.obtener_info()} necesita que el ciclista coma para tener energía"

# Crear flota de vehículos
flota = [
    Carro("Toyota", "Corolla", 2023, 4),
    Carro("Honda", "Civic", 2022, 4),
    Moto("Yamaha", "MT-07", 2023, 700),
    Moto("Kawasaki", "Ninja", 2022, 600),
    Bicicleta("Trek", "Mountain", 2023, "Montaña"),
    Bicicleta("Specialized", "Ruta", 2023, "Ruta")
]

# Simular operaciones de alquiler
print("=== SISTEMA DE ALQUILER DE VEHÍCULOS ===\n")

# Mostrar estado inicial
print("Estado inicial de la flota:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")

print("\n" + "="*50)

# Alquilar algunos vehículos
print("\nAlquilando vehículos:")
print(flota[0].alquilar())  # Alquilar primer carro
print(flota[2].alquilar())  # Alquilar primera moto
print(flota[4].alquilar())  # Alquilar primera bicicleta

print("\n" + "="*50)

# Mostrar estado después de alquileres
print("\nEstado después de alquileres:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")

print("\n" + "="*50)

# Devolver vehículos
print("\nDevolviendo vehículos:")
print(flota[0].devolver(150))  # Devolver carro con 150km
print(flota[2].devolver(80))   # Devolver moto con 80km
print(flota[4].devolver(25))   # Devolver bicicleta con 25km

print("\n" + "="*50)

# Demostrar polimorfismo
print("\nDemostrando polimorfismo - Cargar combustible:")
for vehiculo in flota:
    print(f"  {vehiculo.cargar_combustible()}")

print("\n" + "="*50)

# Estado final
print("\nEstado final de la flota:")
for vehiculo in flota:
    print(f"  {vehiculo.mostrar_estado()}")
```

**¿Qué demuestra este ejemplo?**

1. **Herencia**: `Carro`, `Moto` y `Bicicleta` heredan de `Vehiculo`
2. **Encapsulación**: `__kilometraje` es privado, solo se modifica a través de métodos
3. **Polimorfismo**: `cargar_combustible()` funciona diferente para cada tipo
4. **Reutilización**: No repetimos código para características comunes
5. **Extensibilidad**: Fácil agregar nuevos tipos de vehículos

**Casos de uso reales:**
- **Sistema de reservas**: Hoteles, restaurantes, eventos
- **Gestión de inventario**: Tiendas, almacenes, bibliotecas
- **Sistema de usuarios**: Diferentes tipos de cuentas con permisos específicos

## Ejercicios Prácticos

**Ahora es tu turno de practicar. Estos ejercicios te ayudarán a consolidar todos los conceptos aprendidos.**

### Ejercicio 1: Clase Estudiante
**Objetivo**: Crear una clase que represente a un estudiante universitario.

**Requisitos**:
- Atributos: `nombre`, `edad`, `carrera`, `promedio` (inicializado en 0.0), `materias_inscritas` (lista vacía)
- Métodos:
  - `presentarse()`: Devuelve una descripción del estudiante
  - `inscribir_materia(materia)`: Agrega una materia a la lista (sin duplicados)
  - `agregar_nota(materia, nota)`: Agrega una nota y recalcula el promedio
  - `mostrar_materias()`: Muestra todas las materias inscritas

**Ejemplo de uso**:
```python
estudiante = Estudiante("María González", 20, "Ingeniería de Sistemas")
estudiante.inscribir_materia("Programación I")
estudiante.inscribir_materia("Matemáticas")
estudiante.agregar_nota("Programación I", 4.5)
estudiante.agregar_nota("Matemáticas", 4.2)
print(estudiante.presentarse())
print(f"Promedio: {estudiante.promedio}")
```

### Ejercicio 2: Clase Rectángulo
**Objetivo**: Crear una clase que represente un rectángulo geométrico.

**Requisitos**:
- Atributos: `base`, `altura` (ambos deben ser positivos)
- Métodos:
  - `calcular_area()`: Retorna el área del rectángulo
  - `calcular_perimetro()`: Retorna el perímetro
  - `es_cuadrado()`: Retorna True si es un cuadrado
  - `mostrar_info()`: Muestra toda la información del rectángulo

**Validaciones**:
- La base y altura deben ser números positivos
- Si se intenta crear con valores negativos, lanzar una excepción

**Ejemplo de uso**:
```python
try:
    rect1 = Rectangulo(5, 3)
    rect2 = Rectangulo(4, 4)
    
    print(rect1.mostrar_info())
    print(f"¿Es cuadrado? {rect1.es_cuadrado()}")
    print(f"¿Es cuadrado? {rect2.es_cuadrado()}")
    
except ValueError as e:
    print(f"Error: {e}")
```

### Ejercicio 3: Clase Cuenta Bancaria
**Objetivo**: Crear una clase que represente una cuenta bancaria con funcionalidades avanzadas.

**Requisitos**:
- Atributos: `titular`, `__saldo` (privado), `tipo_cuenta`, `activa`
- Métodos:
  - `depositar(cantidad)`: Deposita dinero (validar cantidad positiva)
  - `retirar(cantidad)`: Retira dinero (validar fondos suficientes)
  - `consultar_saldo()`: Muestra el saldo actual
  - `obtener_resumen()`: Muestra un resumen completo de la cuenta

**Validaciones**:
- Solo cuentas activas pueden realizar operaciones
- Las cantidades deben ser positivas
- No se puede retirar más del saldo disponible

**Ejemplo de uso**:
```python
cuenta1 = CuentaBancaria("Alejandro Salgar", 5000, "corriente")
cuenta2 = CuentaBancaria("María López", 2000, "ahorros")

print(cuenta1.obtener_resumen())
print(cuenta1.depositar(1500))
print(cuenta1.retirar(800))
print(cuenta1.consultar_saldo())
```

### Ejercicio Bonus: Sistema de Biblioteca
**Objetivo**: Crear un sistema completo que combine múltiples clases.

**Clases a implementar**:
- `Libro`: título, autor, ISBN, disponible, prestado_a
- `Estudiante`: nombre, ID, libros_prestados
- `Biblioteca`: gestiona libros y estudiantes

**Funcionalidades**:
- Prestar libros a estudiantes
- Devolver libros
- Buscar libros por título o autor
- Mostrar inventario completo

**¿Por qué estos ejercicios?**
- **Estudiante**: Practica atributos, métodos y lógica de negocio
- **Rectángulo**: Practica validaciones y cálculos matemáticos
- **Cuenta Bancaria**: Practica encapsulación y validaciones complejas
- **Biblioteca**: Practica relaciones entre clases y sistemas completos

**Consejos para resolver**:
1. **Empieza simple**: Primero crea la estructura básica
2. **Agrega validaciones**: Una vez que funcione, agrega las validaciones
3. **Prueba casos extremos**: ¿Qué pasa con valores negativos o vacíos?
4. **Documenta tu código**: Comenta qué hace cada método

## Archivos del Módulo

**Este módulo incluye todos los archivos necesarios para aprender POO desde cero:**

- **`README.md`** - Este archivo con toda la teoría, explicaciones y ejemplos
- **`ejemplos_basicos.py`** - Código ejecutable que demuestra cada concepto paso a paso
- **`ejercicios.py`** - Soluciones completas a todos los ejercicios propuestos

## Cómo Usar Este Módulo

### 1. **Leer la Teoría** (README.md)
- Comienza leyendo cada sección del README
- Entiende los conceptos antes de pasar al código
- Usa las analogías del mundo real para comprender mejor

### 2. **Ejecutar los Ejemplos** (ejemplos_basicos.py)
- Ejecuta el archivo completo: `python ejemplos_basicos.py`
- Modifica los valores y observa qué cambia
- Experimenta creando nuevos objetos

### 3. **Practicar con Ejercicios** (ejercicios.py)
- Primero intenta resolver los ejercicios por tu cuenta
- Compara tu solución con la proporcionada
- Modifica los ejercicios para agregar nuevas funcionalidades

## Próximos Pasos

**Una vez que domines este módulo, estarás listo para:**

- **Módulo 2**: Estructuras de datos (listas, pilas, colas, árboles)
- **Módulo 3**: Algoritmos y análisis de complejidad
- **Módulo 4**: Programación funcional (lambda, map, filter, reduce)
- **Módulo 5**: Manejo de excepciones y errores
- **Módulo 6**: Archivos y persistencia de datos

## Recursos Adicionales

- **Documentación oficial de Python**: https://docs.python.org/3/
- **Tutorial de POO en Python**: https://docs.python.org/3/tutorial/classes.html
- **Real Python - OOP**: https://realpython.com/python3-object-oriented-programming/

---

**¡Manos a la obra! El mejor aprendizaje es practicando. Recuerda: la programación se aprende programando, no solo leyendo.**
