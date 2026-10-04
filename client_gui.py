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
        self.root.geometry("420x500")

        # Close the socket properly when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.login_screen()

    # First screen: the user enters server IP, port and username
    def login_screen(self):
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Distributed Chat", font=("Arial", 14, "bold")).pack(pady=10)

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
        self.user_entry.focus()

        # Pressing Enter in the username box also connects
        self.user_entry.bind("<Return>", lambda e: self.connect())

        tk.Button(self.login_frame, text="Connect", width=15, command=self.connect).pack(pady=10)

    # Connects to the server and sends the username
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
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Timeout so the window does not freeze if the IP is wrong
            self.sock.settimeout(5)
            self.sock.connect((host, port))
            self.sock.settimeout(None)

            self.sock.recv(1024)  # read the username prompt sent by the server
            self.sock.sendall(username.encode())
            reply = self.sock.recv(1024).decode()

            # If the reply is not Welcome, the username was rejected (for example, already taken)
            if "Welcome" not in reply:
                messagebox.showwarning("Error", reply.strip() or "Server closed the connection")
                self.sock.close()
                return
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return

        self.username = username
        self.connected = True

        # Remove the login screen and show the chat screen
        self.login_frame.destroy()
        self.chat_screen()

        # Start the thread that receives messages
        threading.Thread(target=self.receive, daemon=True).start()

    # Second screen: chat display, message box and Send button
    def chat_screen(self):
        self.root.title("Chat - " + self.username)

        # The chat box is disabled so the user cannot type in it directly
        self.chat_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_box.pack(expand=True, fill="both", padx=10, pady=10)

        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        self.msg_entry = tk.Entry(bottom)
        self.msg_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", lambda e: self.send())

        tk.Button(bottom, text="Send", width=8, command=self.send).pack(side="right")

        self.show("Connected as " + self.username + "\n")

    # Adds a line of text to the chat box and scrolls down
    def show(self, text):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, text)
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    # Sends the typed message to the server and shows it in our own chat box
    def send(self):
        text = self.msg_entry.get().strip()
        if not text or not self.connected:
            return
        self.msg_entry.delete(0, tk.END)

        try:
            self.sock.sendall(text.encode())
            time = datetime.now().strftime("[%H:%M:%S]")
            self.show(f"{time} You: {text}\n")
        except Exception:
            self.show("Could not send message.\n")

    # Runs in a background thread and shows messages received from the server
    def receive(self):
        while self.connected:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                # after() is used because Tkinter should only be updated from the main thread
                self.root.after(0, self.show, data.decode())
            except Exception:
                break

        if self.connected:
            self.connected = False
            self.root.after(0, self.show, "Disconnected from server.\n")

    # Called when the user closes the window
    def on_close(self):
        self.connected = False
        if self.sock:
            self.sock.close()
        self.root.destroy()


# Called from client.py to start the GUI
def run_gui():
    app = ChatGUI()
    app.root.mainloop()