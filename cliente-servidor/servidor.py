import socket
import threading

class ChatServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.host = host
        self.port = port
        self.clients = []          # lista de conexiones de clientes
        self.nicknames = []        # lista de nicknames correspondientes
        self.rooms = {}            # diccionario: nickname -> sala_actual
        self.all_rooms = set(["general"])  # conjunto de salas existentes
        self.lock = threading.Lock()       # para proteger estructuras compartidas

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def broadcast_to_room(self, message, room, sender_conn=None):
        """Envía mensaje a todos los clientes en una sala, excepto al remitente."""
        with self.lock:
            # Hacemos una copia para evitar modificar mientras iteramos
            clients_copy = list(self.clients)
            nicknames_copy = list(self.nicknames)
            rooms_copy = dict(self.rooms)

        for i, client in enumerate(clients_copy):
            if client != sender_conn and rooms_copy.get(nicknames_copy[i]) == room:
                try:
                    client.send(message)
                except:
                    # Si falla el envío, eliminamos el cliente de forma segura
                    self.remove_client(client)

    def send_to_client(self, client, message):
        """Envía un mensaje privado a un cliente."""
        try:
            client.send(message)
        except:
            self.remove_client(client)

    def handle_client(self, client_conn):
        """Atiende a un cliente específico en un hilo."""
        nickname = None
        try:
            # Recibir nickname
            nickname = client_conn.recv(1024).decode("utf-8").strip()
            if not nickname:
                return

            with self.lock:
                self.nicknames.append(nickname)
                self.clients.append(client_conn)
                current_room = "general"
                self.rooms[nickname] = current_room

            print(f"[+] {nickname} conectado, unido a sala '{current_room}'")
            self.broadcast_to_room(
                f"{nickname} se ha unido al chat".encode("utf-8"),
                current_room,
                client_conn
            )

            # Bucle de recepción de mensajes
            while True:
                msg = client_conn.recv(1024).decode("utf-8")
                if not msg:
                    break

                if msg.startswith('/'):
                    self.process_command(client_conn, nickname, msg)
                else:
                    with self.lock:
                        room = self.rooms[nickname]
                    full_msg = f"{nickname}: {msg}".encode("utf-8")
                    self.broadcast_to_room(full_msg, room, client_conn)

        except Exception as e:
            print(f"Error con {nickname}: {e}")
        finally:
            if nickname:
                print(f"[-] {nickname} desconectado")
                with self.lock:
                    room = self.rooms.get(nickname, "general")
                self.broadcast_to_room(
                    f"{nickname} ha salido del chat".encode("utf-8"),
                    room,
                    client_conn
                )
                self.remove_client(client_conn, nickname)

    def process_command(self, client_conn, nickname, command):
        """Procesa comandos del cliente."""
        parts = command.strip().split()
        cmd = parts[0].lower()

        if cmd == "/join":
            if len(parts) < 2:
                self.send_to_client(client_conn, b"Uso: /join <nombre_sala>")
                return
            room = parts[1]
            with self.lock:
                current_room = self.rooms[nickname]
                if room == current_room:
                    self.send_to_client(client_conn, f"Ya estás en la sala '{room}'.".encode())
                    return
                # Abandonar sala anterior
                self.rooms[nickname] = room
                self.all_rooms.add(room)

            self.send_to_client(client_conn, f"Te has unido a la sala '{room}'.".encode())
            self.broadcast_to_room(
                f"{nickname} ha abandonado la sala '{current_room}'".encode(),
                current_room,
                client_conn
            )
            self.broadcast_to_room(
                f"{nickname} se ha unido a la sala '{room}'".encode(),
                room,
                client_conn
            )

        elif cmd == "/leave":
            with self.lock:
                current_room = self.rooms[nickname]
                if current_room == "general":
                    self.send_to_client(client_conn, b"No puedes salir de la sala 'general'.")
                    return
                self.rooms[nickname] = "general"

            self.send_to_client(client_conn, b"Has abandonado la sala actual y te has unido a 'general'.")
            self.broadcast_to_room(
                f"{nickname} ha abandonado la sala '{current_room}'".encode(),
                current_room,
                client_conn
            )
            self.broadcast_to_room(
                f"{nickname} se ha unido a la sala 'general'".encode(),
                "general",
                client_conn
            )

        elif cmd == "/rooms":
            with self.lock:
                rooms_list = ", ".join(self.all_rooms)
            self.send_to_client(client_conn, f"Salas disponibles: {rooms_list}".encode())

        elif cmd == "/quit":
            self.send_to_client(client_conn, b"Desconectando...")
            client_conn.close()
            self.remove_client(client_conn, nickname)

        else:
            self.send_to_client(client_conn, b"Comando no reconocido. Usa: /join, /leave, /rooms, /quit")

    def remove_client(self, client_conn, nickname=None):
        """Elimina un cliente de las listas y cierra conexión."""
        with self.lock:
            if client_conn in self.clients:
                idx = self.clients.index(client_conn)
                self.clients.pop(idx)
                if nickname is None:
                    nickname = self.nicknames.pop(idx)
                else:
                    self.nicknames.remove(nickname)
                if nickname in self.rooms:
                    del self.rooms[nickname]
        client_conn.close()

    def start(self):
        self.server.listen()
        print(f"[INFO] Servidor de chat con salas escuchando en {self.host}:{self.port}")
        try:
            while True:
                client_conn, addr = self.server.accept()
                print(f"[INFO] Conexión entrante desde {addr}")
                thread = threading.Thread(target=self.handle_client, args=(client_conn,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\n[INFO] Servidor detenido por el usuario.")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()