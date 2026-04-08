import threading
import time

contador = 0
lock = threading.Lock()

def incrementador():
    global contador
    for _ in range(100):
        with lock:
            contador += 1




hilo1 = threading.Thread(target=incrementador, args=())
hilo1.start()
hilo2 = threading.Thread(target=incrementador, args=())
hilo2.start()
hilo3 = threading.Thread(target=incrementador, args=())
hilo3.start()



hilo1.join()
hilo2.join()
hilo3.join()




print(contador)

