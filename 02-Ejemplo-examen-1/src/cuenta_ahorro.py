from .cuenta import CuentaBancaria

class CuentaAhorro(CuentaBancaria):
    def __init__(self, titular, saldo: float = 0, interes: float = 0.02) -> None:
        super().__init__(titular, saldo)
        self._interes = interes

    def aplicar_interes(self) -> None:
        self._saldo += self._saldo * self._interes

    def __str__(self):
        return f"Cuenta de Ahorros - {super().__str__()}, Interés: {self._interes}"