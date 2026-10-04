# Distributed Chat Application

A client-server chat application built in Python using TCP sockets and threading. Multiple users connect to one central server and chat with each other in real time. The project demonstrates basic Distributed Computing concepts: several clients on different machines communicating through a central server over a network.

**Current version:** 1.0

## Features

- Central server that handles multiple clients at the same time
- Unique username for every user
- Messages are delivered to all other users with the time and sender's username
- Join and leave notifications
- Two client interfaces: Tkinter GUI (default) and terminal (CMD)
- Works on the same computer and across computers on a LAN/Wi-Fi network

## Project Files

- `server.py` - the chat server
- `client.py` - starts the client and lets the user choose GUI or CMD
- `client_gui.py` - the Tkinter GUI client
- `README.md` - project documentation

## Requirements

- Python 3
- No external packages are needed, only standard libraries
- On Linux, the GUI may need Tkinter installed: `sudo apt install python3-tk`

## How to Run

1. Start the server first:
```
python3 server.py
```

2. Open another terminal and start a client:
```
python3 client.py
```

3. Choose the interface:
```
1 = GUI (Tkinter)
2 = CMD (Terminal)
```
Press Enter or type 1 for the GUI, or type 2 for the terminal. Run `client.py` again in more terminals to add more users.

- **GUI mode:** Enter the Server IP, Port and Username, then click Connect. Type a message and press Enter or click Send.
- **CMD mode:** Enter the server IP and a username, then type your messages. Press Ctrl+C to leave the chat.

## Using on LAN / Wi-Fi

1. Run `server.py` on one computer and find its IP address (`ipconfig` on Windows, `hostname -I` on Linux).
2. On the other computers, run `client.py` and enter that IP address.

All computers must be on the same network. If a client cannot connect, check that the firewall allows port 5000.

## How It Works

The server listens on port 5000 and creates a new thread for every client that connects. The client sends a username, and the server checks that no one else is using it. After that, when the server receives a message, it adds the time and username and sends it to all the other clients. The server also informs everyone when a user joins or leaves.

The client has a separate thread for receiving messages, so a user can receive messages while typing.

## Technologies Used

- Python 3
- TCP sockets
- Threading
- Tkinter

## Limitations

- Messages are sent as plain text (no encryption)
- There is only one server, so if it stops, all clients are disconnected
- Chat history is not saved

## Future Scope

These are not part of version 1.0, but the project can be extended with:

- Private messages between two users
- A list of online users
- Saving chat history
- Encrypted communication
- Handling multiple chat rooms