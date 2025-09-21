class Persona:
    def __init__(self, nombre:str, documento:str):
        self.nombre =  nombre
        self.documento = documento

    def __str__(self) -> str:
        return f"{self.nombre}, se creo esta persona con el documneto {self.documento}"
    
class CuentaBancaria:
    def __init__(self, titutar: Persona, saldo: int = 0):
        self.titutar = titutar
        self._saldo = saldo
    
    def saldo(self) -> int:
        return self._saldo
    
    def depositar(self, monto: float) -> None:
        if monto > 0:
            self._saldo += monto
            print(f"Se depósito un monto de {monto} y mi saldo actual {self._saldo}")
        else:
            print("El monto debe ser positivo")

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo:
            self._saldo -= monto
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")
<<<<<<< HEAD
    
    def __str__(self):
        return f"Titular: {self.titutar.nombre}, Saldo: {self._saldo}"
=======

        def __str__(self) -> str:
            return f"{self.nombre}, se creo esta persona con el documneto {self.documento}"
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
        
class CuentaAhorro(CuentaBancaria):
    def __init__(self, titular, saldo = 0, interes: float = 0.02):
        super().__init__(titular, saldo)
        self.interes = interes

    def calcular_interes(self):
        ganancia = self._saldo * self.interes
        self._saldo += ganancia
        print(f"interes aplicado y su nuevo saldo es {self._saldo}")

<<<<<<< HEAD
    def __str__(self):
        return f"Cuenta de Ahorros - {super().__str__()}, Interés: {self.interes}"

=======
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369

class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular, saldo = 0, limite_de_sobregiro: float = 500):
        super().__init__(titular, saldo)
        self.limite_de_sobregiro = limite_de_sobregiro

    def retirar(self, monto: float):
        if monto <= self._saldo + self.limite_de_sobregiro:
            self._saldo -= monto 
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")
<<<<<<< HEAD
    
    def __str__(self):
        return f"Cuenta Corriente - {super().__str__()}, Límite de sobregiro: {self.limite_de_sobregiro}"
=======
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369


class Banco:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuentas = []

    def crear_cuentar(self, titular, tipo="ahorros") -> list:
<<<<<<< HEAD
        if tipo == "ahorros":
=======
        if tipo == "ahorro":
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
            cuenta = CuentaAhorro(titular)
        else:
            cuenta = CuentaCorriente(titular)
        self.cuentas.append(cuenta)
        print(f"cuenta brancaria {self.nombre}")
<<<<<<< HEAD
        return self.cuentas
=======
        return cuenta
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
    
    def mostrar_cuentas(self):
        if not self.cuentas:
            print("No tengo cuentas registradas")
        else:
            for i, cuenta in enumerate(self.cuentas, 1):
                print(f"{i}. {cuenta}")



banco = Banco(nombre="Banco ITM")
while True:
    print("\n--- MENU ---")
    print("1. crear una persona y una cuenta")
    print("2. Depositar")
    print("3. Retirar")
<<<<<<< HEAD
    print("4. Aplicar interés a una cuenta de ahorros")
=======
    print("4. APlicar interes a una cuenta de ahorros")
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
    print("5. Mostrar cuentas")
    print("6. Salir")
    # continuar con las demas opciones
    
    
    #Consultar como validar que este input sea un numero del 1 al 6
<<<<<<< HEAD
    opcion = input("Elige una opción: ")
    if opcion.isdigit(): #isdigit es un metodo que verifica si el input es un numero entero postivio
        opcion = int(opcion)
        if opcion < 1 or opcion > 6:
            print("Debes ingresar un número entre 1 y 6.")
        else:
            print("Opcion no valida")
    else:
        print("Debes ingresar un número entero.")
        print("Opcion no valida")

    
    if opcion == 1:
=======
    opcion = input("Elige una opcion: ")
    
    if opcion == "1":
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
        nombre = input("Ingrese el nombre de la persona ")
        documento = input("ingrese el documento de la persona ")
        persona = Persona(nombre=nombre,documento=documento)

        print("\nQue tipo de cuenta quiere crear")
        #Validar tipo de dato entre str ahorro o corriente
        tipo = input("Escriba ahorros o corriente ").lower()
        banco.crear_cuentar(persona,tipo)
<<<<<<< HEAD
    
    elif opcion == 2:
        if not banco.cuentas:
            print("No hay cuentas registradas para depositar.")
        else:
            banco.mostrar_cuentas()
            num = input("Selecciona el número de cuenta para depositar: ")
            if num.isdigit() and 1 <= int(num) <= len(banco.cuentas):
                cuenta = banco.cuentas[int(num)-1]
                monto = input("Monto a depositar: ")
                if monto.replace('.', '', 1).isdigit() and float(monto) > 0:
                    cuenta.depositar(float(monto))
                else:
                    print("Monto inválido.")
            else:
                print("Cuenta inválida.")

    elif opcion == 3:
        if not banco.cuentas:
            print("No hay cuentas registradas para retirar.")
        else:
            banco.mostrar_cuentas()
            num = input("Selecciona el número de cuenta para retirar: ")
            if num.isdigit() and 1 <= int(num) <= len(banco.cuentas):
                cuenta = banco.cuentas[int(num)-1]
                monto = input("Monto a retirar: ")
                if monto.replace('.', '', 1).isdigit() and float(monto) > 0:
                    cuenta.retirar(float(monto))
                else:
                    print("Monto inválido.")
            else:
                print("Cuenta inválida.")

    elif opcion == 4:
        if not banco.cuentas:  
            print("No hay cuentas registradas para aplicar interes.")
        else:
            banco.mostrar_cuentas()
            num = input("Selecciona el número de cuenta para aplicar interés: ")
        if num.isdigit() and 1 <= int(num) <= len(banco.cuentas):
            cuenta = banco.cuentas[int(num)-1]
            if isinstance(cuenta, CuentaAhorro):
                cuenta.calcular_interes()
            else:
                print("Solo se puede aplicar interés a cuentas de ahorros.")
        else:
            print("Cuenta inválida.")

    elif opcion == 5:
        banco.mostrar_cuentas()

    elif opcion == 6:
        print("Gracias por usar nuestra aplicacion")
        break
    
=======

    elif opcion == "5":
        banco.mostrar_cuentas()

    elif opcion == "6":
        print("Gracias por usar nuestra aplicacion")
        break

    else:
        print("Opcion no valida")


# terminar todas las opciones que son 2, 3, 4, ajustar la 5 para que imprima el objeto y no la referencia de memoria
# Validar que todos los input sean del valor deseado, mostrando errores por consola sin try catch
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
