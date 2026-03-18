import threading
import time

def tarea(numero):
    print(f"numero de Hilo {numero}")

hilos = []

inicio = time.perf_counter()

for i in range (1,101):
    hilo = threading.Thread(target= tarea, args=(i,))
    hilos.append(hilo)
    hilo.start()


for hilo in hilos:
    hilo.join()


fin = time.perf_counter()

tiempo = fin - inicio
print(tiempo)

