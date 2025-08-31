from .cuenta import CuentaBancaria

class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular, saldo: float = 0, sobregiro: float = 500) -> None:
        super().__init__(titular, saldo)
        self._sobregiro = sobregiro

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo + self._sobregiro:
            self._saldo -= monto
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")
    
    def __str__(self):
        return f"Cuenta Corriente - {super().__str__()}, Límite de sobregiro: {self._sobregiro}"
