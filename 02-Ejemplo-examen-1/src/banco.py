from .cuenta_ahorro import CuentaAhorro
from .cuenta_corriente import CuentaCorriente

class Banco:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuentas = []

    def crear_cuenta(self, titular, tipo="ahorros") -> list:
        if tipo == "ahorros":
            cuenta = CuentaAhorro(titular)
        else:
            cuenta = CuentaCorriente(titular)
        self.cuentas.append(cuenta)
        print(f"cuenta bancaria {self.nombre}")
        return self.cuentas
    
    def mostrar_cuentas(self):
        if not self.cuentas:
            print("No tengo cuentas registradas")
        else:
            for i, cuenta in enumerate(self.cuentas, 1):
                print(f"{i}. {cuenta}")