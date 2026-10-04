import socket
import threading

PORT = 5000


# Runs in a background thread and prints every message sent by the server.
# This way the user can receive messages while typing.
def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
        except Exception:
            break
    print("Disconnected from server.")


# Terminal (CMD) version of the client
def cmd_client():
    host = input("Server IP [127.0.0.1]: ").strip() or "127.0.0.1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Timeout so the program does not wait forever if the IP is wrong
    sock.settimeout(5)
    try:
        sock.connect((host, PORT))
    except Exception as e:
        print("Could not connect:", e)
        return
    sock.settimeout(None)

    try:
        # The server sends the username prompt only once, so we read it here
        print(sock.recv(1024).decode(), end="")

        # Keep sending usernames until the server accepts one (replies with Welcome)
        while True:
            sock.sendall(input().encode())
            reply = sock.recv(1024).decode()
            print(reply, end="")
            if "Welcome" in reply:
                break

        # Start the thread that receives messages
        threading.Thread(target=receive, args=(sock,), daemon=True).start()

        # Main thread reads what the user types and sends it. Ctrl+C to leave.
        while True:
            msg = input()
            if msg.strip():
                sock.sendall(msg.encode())
    except (KeyboardInterrupt, EOFError):
        print("\nYou left the chat.")
    except OSError:
        print("\nConnection lost.")
    finally:
        sock.close()


# Ask the user which interface they want to use
print("Choose interface:")
print("1 = GUI (Tkinter)")
print("2 = CMD (Terminal)")
choice = input("Enter choice [1]: ").strip()

if choice == "2":
    cmd_client()
else:
    # GUI is the default, so anything other than 2 opens the GUI
    from client_gui import run_gui
    run_gui()