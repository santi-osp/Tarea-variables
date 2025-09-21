<<<<<<< HEAD
from .cuenta import CuentaBancaria

class CuentaAhorro(CuentaBancaria):
    def __init__(self, titular, saldo: float = 0, interes: float = 0.02) -> None:
        super().__init__(titular, saldo)
=======
from .cuenta import Cuenta

class CuentaAhorro(Cuenta):
    def __init__(self, numero, saldo=0, interes=0.02):
        super().__init__(numero, saldo)
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
        self._interes = interes

    def aplicar_interes(self) -> None:
        self._saldo += self._saldo * self._interes
<<<<<<< HEAD

    def __str__(self):
        return f"Cuenta de Ahorros - {super().__str__()}, Interés: {self._interes}"
=======
>>>>>>> 5381fc36d68ac5f3de2d1cfa959718de1599f369
