import socket
import threading


class ChatServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.host = host
        self.port = port

        self.rooms = {"general": []}
        self.client_rooms = {}
        self.nicknames = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def broadcast(self, message, room, sender_conn=None):
        for client in self.rooms.get(room, []):
            if client != sender_conn:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)

    def handle_client(self, client_conn):
        nickname = None

        while True:
            try:
                message = client_conn.recv(1024)
                if not message:
                    raise Exception()

                decoded = message.decode("utf-8")

                # Primer mensaje = nickname
                if nickname is None:
                    nickname = decoded
                    self.nicknames[client_conn] = nickname

                    # entra a sala general
                    self.rooms["general"].append(client_conn)
                    self.client_rooms[client_conn] = "general"

                    print(f"[+] {nickname} conectado")
                    self.broadcast(
                        f"{nickname} se unió a general".encode("utf-8"),
                        "general",
                        client_conn,
                    )
                    continue

                # Comando para cambiar de sala
                if decoded.startswith("/join "):
                    new_room = decoded.split(" ", 1)[1]

                    current_room = self.client_rooms[client_conn]

                    # salir de sala actual
                    self.rooms[current_room].remove(client_conn)
                    self.broadcast(
                        f"{nickname} salió de la sala".encode("utf-8"),
                        current_room,
                        client_conn,
                    )

                    # crear sala si no existe
                    if new_room not in self.rooms:
                        self.rooms[new_room] = []

                    # entrar a nueva sala
                    self.rooms[new_room].append(client_conn)
                    self.client_rooms[client_conn] = new_room

                    client_conn.send(f"Entraste a {new_room}".encode("utf-8"))

                    self.broadcast(
                        f"{nickname} se unió a la sala".encode("utf-8"),
                        new_room,
                        client_conn,
                    )
                    continue

                # mensaje normal
                room = self.client_rooms[client_conn]
                full_msg = f"{nickname}: {decoded}".encode("utf-8")
                self.broadcast(full_msg, room, client_conn)

            except:
                self.remove_client(client_conn)
                break

    def remove_client(self, client_conn):
        nickname = self.nicknames.get(client_conn, "Unknown")
        room = self.client_rooms.get(client_conn)

        if room and client_conn in self.rooms.get(room, []):
            self.rooms[room].remove(client_conn)
            self.broadcast(
                f"{nickname} se desconectó".encode("utf-8"),
                room,
                client_conn,
            )

        if client_conn in self.nicknames:
            del self.nicknames[client_conn]

        if client_conn in self.client_rooms:
            del self.client_rooms[client_conn]

        client_conn.close()

    def start(self):
        self.server.listen()
        print(f"[INFO] Servidor en {self.host}:{self.port}")

        while True:
            client_conn, addr = self.server.accept()
            print(f"[INFO] Conexión desde {addr}")

            thread = threading.Thread(
                target=self.handle_client, args=(client_conn,)
            )
            thread.start()


if __name__ == "__main__":
    server = ChatServer()
    server.start()