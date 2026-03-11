user = "admin@uniremington.edu.co"
password= "admin1234"

user_input= input("ingrese el usuario: ")
pass_input= input("ingrese la contraseña: ")

if(user_input == user and pass_input == password):
    print("ingreso correcto")
else: 
    print("ingreso fallido")