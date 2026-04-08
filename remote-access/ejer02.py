import pickle

datos = {
    "nombre": "Andres Steven Cortes Perez",
    "materia": "Lenguaje de Programacion",
    "notas": [5,5,5,4]
}

with open("data.txt", "wb") as archivo:
    pickle.dump(datos, archivo)


with open("data.txt", "rb") as archivo:
    datos_estudiantes = pickle.load(archivo)

print(datos_estudiantes)



