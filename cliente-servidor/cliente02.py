import socket
import sys
import threading


class ChatClient:
    def __init__(self, host="127.0.0.1", port=5555, nickname="Cliente2"):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def receive_messages(self):
        while self.connected:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if msg:
                    print(f"\n[SERVIDOR] {msg}")
            except:
                print("\n[ERROR] Comunicación con el servidor perdida.")
                self.connected = False
                break

    def start(self):
        try:
            self.client.connect((self.host, self.port))
            self.connected = True
            print(f"[INFO] Conectado al servidor {self.host}:{self.port}")

            self.client.send(self.nickname.encode("utf-8"))

            thread = threading.Thread(target=self.receive_messages)
            thread.daemon = True
            thread.start()

            while self.connected:
                try:
                    msg = input(f"{self.nickname} > ")
                    if msg.lower() == "salir":
                        self.connected = False
                        self.client.close()
                        print("[INFO] Desconexión del servidor.")
                        break
                    else:
                        self.client.send(msg.encode("utf-8"))
                except:
                    self.connected = False
                    self.client.close()
                    print("\n[ERROR] Error al enviar mensaje.")
                    break

        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        client = ChatClient(host=sys.argv[1], nickname="Cliente2")
    else:
        client = ChatClient(nickname="Cliente2")
    client.start()