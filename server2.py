import socket
import threading

#hiff
class Server:

    def __init__(self):
        self.server_socket = None
        self.clients = []
        self.client_lock = threading.Lock()
        self.users = {}

    def start(self):
        ip = '127.0.0.1'
        print(f"Server IP address: {ip}")
        port = 8080

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()

        print(f"Server listening on {ip}:{port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client connected from {client_address[0]}:{client_address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def broadcast(self, message, users, sender_username=None):
        """
        Send a message to all connected clients except for the sender.
        """
        for username, conn in users.items():
            if username != sender_username:
                conn.send(message.encode())

    def handle_client(self, conn, addr):
        """
        Handle a client connection.
        """
        username = None
        try:
            # Receive the client's username
            username = conn.recv(1024).decode()
            self.users[username] = conn

            # Notify all clients that a new user has joined
            message = f"{username} has joined the chat.\n"
            self.broadcast(message, self.users)
            print(message.strip())

            # Send a message to the new client confirming their connection
            conn.send("You have connected to the server.\n".encode())

            # Receive and broadcast messages
            while True:
                message = conn.recv(1024).decode()
                if message.lower() == "/quit":
                    # User has disconnected
                    break
                elif message.startswith("PRIVATE"):
                    # Split the private message by spaces and extract the recipient and message
                    parts = message.split(" ", 2)
                    if len(parts) == 3:
                        recipient_username = parts[1][1:]
                        message = parts[2]
                        recipient_socket = self.users.get(recipient_username)
                        if recipient_socket:
                            recipient_socket.send(f"{username} (private): {message}".encode())
                            conn.send(f"To {recipient_username} (private): {message}".encode())
                        else:
                            conn.send(f"User @{recipient_username} not found.".encode())
                    else:
                        conn.send("Invalid private message format.".encode())
                else:
                    self.broadcast(f"{username}: {message}", self.users, sender_username=username)

        except:
            print(f"Error handling connection from {addr}")
        finally:
            # Remove the user from the dictionary of connected clients
            if username in self.users:
                del self.users[username]
                # Notify all clients that the user has left the chat
                message = f"{username} has left the chat.\n"
                self.broadcast(message, self.users)
                print(message.strip())
            conn.close()


    def get_username(self, conn):
        for username, user_conn in self.users.items():
            if user_conn == conn:
                return username
        return None


server = Server()
server.start()
