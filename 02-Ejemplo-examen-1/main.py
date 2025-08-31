from src.banco import Banco
from src.cliente import Persona
from src.cuenta_ahorro import CuentaAhorro

def menu():
    print("\n--- BANCO ---")
    print("1. Crear cuenta")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Aplicar interés")
    print("5. Mostrar cuentas")
    print("6. Salir")

def main() -> None:
    banco = Banco("Banco ITM")

    while True:
        menu()

        #FORMA 1 DE VALIDACION
        opcion = input("Elige una opción: ")
        if opcion.isdigit(): #isdigit es un metodo que verifica si el input es un numero entero postivio
            opcion = int(opcion)
            if opcion < 1 or opcion > 6:
                print("Debes ingresar un número entre 1 y 6.")
                print("Opcion no valida")
                continue
        else:
            print("Debes ingresar un número entero.")
            print("Opcion no valida")
            continue
        
        #FORMA 2 DE VALIDACION
        #opcion = int(input("Elige una opción: "))

        if opcion == 1:
            nombre = input("Ingrese el nombre de la persona ")
            documento = input("ingrese el documento de la persona ")
            persona = Persona(nombre=nombre,documento=documento)

            print("\nQue tipo de cuenta quiere crear")
            #Validar tipo de dato entre str ahorro o corriente
            tipo = input("Escriba ahorros o corriente ").lower()
            banco.crear_cuenta(persona,tipo)
        
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
                        cuenta.aplicar_interes()
                    else:
                        print("Solo se puede aplicar interés a cuentas de ahorros.")
                else:
                    print("Cuenta inválida.")

        elif opcion == 5:
            banco.mostrar_cuentas()

        elif opcion == 6:
            print("Gracias por usar nuestra aplicacion")
            break

if __name__ == "__main__":
    main()
