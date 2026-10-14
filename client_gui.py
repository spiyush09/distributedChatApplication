import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime


class ChatGUI:
    def __init__(self):
        self.sock = None
        self.username = ""
        self.connected = False

        self.root = tk.Tk()
        self.root.title("Chat Application")

        # Slightly larger default window and minimum size
        self.root.geometry("460x560")
        self.root.minsize(420, 500)

        # Close the socket properly when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.login_screen()

    # First screen: server IP, port and username
    def login_screen(self):
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack(expand=True)

        tk.Label(
            self.login_frame,
            text="Distributed Chat",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(self.login_frame, text="Server IP:").pack(anchor="w")

        self.ip_entry = tk.Entry(self.login_frame, width=25)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Port:").pack(anchor="w")

        self.port_entry = tk.Entry(self.login_frame, width=25)
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Username:").pack(anchor="w")

        self.user_entry = tk.Entry(self.login_frame, width=25)
        self.user_entry.pack(pady=5)
        self.user_entry.focus_set()

        # Pressing Enter connects to the server
        self.user_entry.bind("<Return>", lambda event: self.connect())

        tk.Button(
            self.login_frame,
            text="Connect",
            width=15,
            command=self.connect
        ).pack(pady=10)

    # Connect to the server and send the username
    def connect(self):
        host = self.ip_entry.get().strip()
        username = self.user_entry.get().strip()

        if not username:
            messagebox.showwarning("Error", "Enter a username")
            return

        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return

        try:
            self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            # Prevent the GUI from freezing on connection timeout
            self.sock.settimeout(5)
            self.sock.connect((host, port))
            self.sock.settimeout(None)

            self.sock.recv(1024)  # Read server username prompt
            self.sock.sendall(username.encode())

            reply = self.sock.recv(1024).decode()

            # Reject usernames that the server does not accept
            if "Welcome" not in reply:
                messagebox.showwarning(
                    "Error",
                    reply.strip() or "Server closed the connection"
                )
                self.sock.close()
                self.sock = None
                return

        except Exception as error:
            if self.sock:
                self.sock.close()
                self.sock = None

            messagebox.showerror("Connection Error", str(error))
            return

        self.username = username
        self.connected = True

        # Replace login screen with chat screen
        self.login_frame.destroy()
        self.chat_screen()

        # Receive messages in the background
        threading.Thread(
            target=self.receive,
            daemon=True
        ).start()

    # Second screen: chat history, input and Send button
    def chat_screen(self):
        self.root.title("Chat - " + self.username)

        # Chat history occupies the available space
        self.chat_box = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state=tk.DISABLED
        )

        self.chat_box.pack(
            side="top",
            expand=True,
            fill="both",
            padx=10,
            pady=(10, 5)
        )

        # Dedicated bottom row for message input and Send button
        bottom = tk.Frame(self.root)
        bottom.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=(5, 12)
        )

        self.msg_entry = tk.Entry(bottom)
        self.msg_entry.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 8)
        )

        self.send_button = tk.Button(
            bottom,
            text="Send",
            width=10,
            command=self.send
        )
        self.send_button.pack(side="right")

        # Enter sends the message
        self.msg_entry.bind(
            "<Return>",
            lambda event: self.send()
        )

        self.msg_entry.focus_set()

        self.show("Connected as " + self.username + "\n")

    # Display a message in the chat history
    def show(self, text):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, text)
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    # Send a message to the server
    def send(self):
        text = self.msg_entry.get().strip()

        if not text or not self.connected:
            return

        self.msg_entry.delete(0, tk.END)

        try:
            self.sock.sendall(text.encode())

            timestamp = datetime.now().strftime("[%H:%M:%S]")
            self.show(f"{timestamp} You: {text}\n")

        except Exception:
            self.show("Could not send message.\n")

    # Receive messages from the server
    def receive(self):
        while self.connected:
            try:
                data = self.sock.recv(1024)

                if not data:
                    break

                # Update Tkinter widgets on the main thread
                self.root.after(
                    0,
                    self.show,
                    data.decode()
                )

            except Exception:
                break

        if self.connected:
            self.connected = False
            self.root.after(
                0,
                self.show,
                "Disconnected from server.\n"
            )

    # Close the socket when the window closes
    def on_close(self):
        self.connected = False

        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                self.sock.close()
            except OSError:
                pass

        self.root.destroy()


# Called from client.py to start the GUI
def run_gui():
    app = ChatGUI()
    app.root.mainloop()
