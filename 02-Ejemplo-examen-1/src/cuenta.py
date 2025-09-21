<<<<<<< HEAD
from .cliente import Persona

class CuentaBancaria:
    def __init__(self, titular: Persona, saldo: float = 0):
        self.titular = titular
        self._saldo = saldo
    
    def saldo(self) -> int:
        return self._saldo
    
    def depositar(self, monto: float) -> None:
        if monto > 0:
            self._saldo += monto
            print(f"Se depósito un monto de {monto} y mi saldo actual {self._saldo}")
        else:
            print("El monto debe ser positivo")
=======
class Cuenta:
    def __init__(self, numero: int, saldo: float = 0):
        self._numero = numero
        self._saldo = saldo

    def depositar(self, monto: float) -> None:
        self._saldo += monto
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo:
            self._saldo -= monto
<<<<<<< HEAD
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")
    
    def __str__(self):
        return f"Titular: {self.titular.nombre}, Saldo: {self._saldo}"
=======
        else:
            print("Fondos insuficientes")

    def mostrar_saldo(self) -> str:
        return f"Cuenta {self._numero} - Saldo: {self._saldo}"
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
