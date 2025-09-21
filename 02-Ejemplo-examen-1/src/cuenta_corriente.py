<<<<<<< HEAD
from .cuenta import CuentaBancaria

class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular, saldo: float = 0, sobregiro: float = 500) -> None:
        super().__init__(titular, saldo)
=======
from .cuenta import Cuenta

class CuentaCorriente(Cuenta):
    def __init__(self, numero, saldo=0, sobregiro=500):
        super().__init__(numero, saldo)
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
        self._sobregiro = sobregiro

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo + self._sobregiro:
            self._saldo -= monto
<<<<<<< HEAD
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")
    
    def __str__(self):
        return f"Cuenta Corriente - {super().__str__()}, Límite de sobregiro: {self._sobregiro}"
=======
        else:
            print("Límite de sobregiro excedido")
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
