import socket
import threading
from datetime import datetime

# 0.0.0.0 means the server accepts connections from any computer on the network
HOST = "0.0.0.0"
PORT = 5000

# Stores all connected clients as {socket: username}
clients = {}

# Lock is used because many threads access the clients dictionary at the same time
lock = threading.Lock()


# Returns the current time in [HH:MM:SS] format
def get_time():
    return datetime.now().strftime("[%H:%M:%S]")


# Sends a message to every connected client except the sender
def broadcast(message, sender=None):
    with lock:
        for c in list(clients):
            if c != sender:
                try:
                    c.sendall(message.encode())
                except Exception:
                    pass


# Handles one client. A separate thread runs this function for each client.
def handle_client(conn, addr):
    username = None
    print(get_time(), "Connection from", addr[0])

    try:
        conn.sendall("Enter your username: ".encode())

        # Keep asking until the client gives a valid and unique username
        while True:
            data = conn.recv(1024)
            if not data:
                return
            name = data.decode().strip()

            if not name:
                conn.sendall("Username cannot be empty. Try again: ".encode())
                continue

            with lock:
                if name in clients.values():
                    conn.sendall("Username already taken. Try another: ".encode())
                else:
                    clients[conn] = name
                    username = name
                    break

        conn.sendall(f"Welcome, {username}!\n".encode())
        print(get_time(), username, "joined")

        # Tell the other users that a new user has joined
        broadcast(f"{get_time()} {username} joined the chat.\n", conn)

        # Receive messages from this client, add time and username, and send to others
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            if msg:
                full_msg = f"{get_time()} {username}: {msg}\n"
                print(full_msg, end="")
                broadcast(full_msg, conn)

    except Exception:
        pass
    finally:
        # Runs when the client leaves: remove it from the list and close the connection
        with lock:
            if conn in clients:
                del clients[conn]
        conn.close()
        if username:
            print(get_time(), username, "left")
            broadcast(f"{get_time()} {username} left the chat.\n")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allows the server to restart quickly without a "port already in use" error
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()
    print("Server started on port", PORT)

    try:
        while True:
            conn, addr = server.accept()
            # Start a new thread so multiple clients can chat at the same time
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.close()


main()