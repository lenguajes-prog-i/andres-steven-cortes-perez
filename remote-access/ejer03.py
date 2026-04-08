import pickle

class Auto:
   def __init__(self, modelo, placa):
      self.modelo = modelo
      self.placa = placa


   def __repr__(self):
        return f"El auto {self.modelo} tiene placa {self.placa}"
   
objeto_auto= Auto("Mazda", "ABC123")
objeto_auto2= Auto("Mercedes", "ACC123")
objeto_auto3= Auto("Ferrari", "BBB123")
objeto_auto4= Auto("toyota", "AAA121")
objeto_auto5= Auto("Nissan", "JJJ987")

#print(objeto_auto)
#print(objeto_auto2)
#print(objeto_auto3)
#print(objeto_auto4)
#print(objeto_auto5)

archivo_auto = open("autos.txt", "wb")
lista_autos = [objeto_auto, objeto_auto2, objeto_auto3, objeto_auto4, objeto_auto5]
pickle.dump(lista_autos, archivo_auto)
archivo_auto.close()




archivo_auto = open("autos.txt", "rb")

for auto in pickle.load(archivo_auto):
    print(auto)
