import socket
import sys
import threading


class ChatClient:
    def __init__(self, host="127.0.0.1", port=5555, nickname="steven"):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.current_room = None

    def receive_messages(self):
        while self.connected:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if msg:
                    print(f"\n[SERVIDOR] {msg}")
                    print(f"{self.nickname} ({self.current_room}) > ", end="")
            except:
                print("\n[ERROR] Conexión perdida.")
                self.connected = False
                break

    def start(self):
        try:
            self.client.connect((self.host, self.port))
            self.connected = True

            print(f"[INFO] Conectado a {self.host}:{self.port}")

            # nickname
            self.client.send(self.nickname.encode("utf-8"))

            thread = threading.Thread(target=self.receive_messages)
            thread.daemon = True
            thread.start()

            while self.connected:
                msg = input(f"{self.nickname} ({self.current_room}) > ")

                if msg == "/quit":
                    self.client.send(msg.encode("utf-8"))
                    self.connected = False
                    self.client.close()
                    print("[INFO] Desconectado.")
                    break

                elif msg.startswith("/join "):
                    self.current_room = msg.split(" ", 1)[1]
                    self.client.send(msg.encode("utf-8"))

                elif msg == "/leave":
                    self.current_room = None
                    self.client.send(msg.encode("utf-8"))

                elif msg == "/rooms":
                    self.client.send(msg.encode("utf-8"))

                elif msg.startswith("/msg "):
                    self.client.send(msg.encode("utf-8"))

                else:
                    print("[ERROR] Usa /msg para enviar mensajes")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        client = ChatClient(host=sys.argv[1], nickname="Steven")
    else:
        client = ChatClient(nickname="Steven")

    client.start()