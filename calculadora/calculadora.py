print("1.Suma")
print("2.Resta")
print("3.Multiplicacion")
print("4.Division")

operacion =int(input("Ingrese la operacion requerida : "))

num1=int(input("Ingrese Numero 1: "))
num2=int(input("Ingrese Numero 2: "))

if operacion == 1:
    resul= num1 + num2

elif operacion == 2:
    resul= num1 - num2

elif operacion == 3:
   resul= num1 * num2

elif operacion == 4:
    resul= num1 / num2

else:
    print("operacion incorrecta")

print(resul)