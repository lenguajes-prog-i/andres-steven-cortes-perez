import threading
import time
inicio = time.perf_counter()

def tarea(letra):
    for i in range(4):
        print(letra)

letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]

hilos = []


for letra in letras:
    hilo = threading.Thread(target= tarea, args=(letra,))
    hilos.append(hilo)
    hilo.start()


for hilo in hilos:
    hilo.join()


fin = time.perf_counter()

tiempo = fin - inicio
print(tiempo)
