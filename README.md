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

- Python 3.8 or newer
- No external packages are needed, only the standard library
- Tkinter for the GUI client (the terminal client works without it)

## Setup

Linux (Fedora) is the primary platform. Windows is also supported.

### Linux (Fedora)

Clone the project and open the folder:

```bash
git clone https://github.com/spiyush09/distributedChatApplication.git
cd distributedChatApplication
```

Check Python (Fedora includes it) and install Tkinter for the GUI:

```bash
python3 --version
sudo dnf install python3-tkinter
```

Verify that Tkinter works (no output means it is fine):

```bash
python3 -c "import tkinter"
```

### Windows

Install Python from <https://www.python.org/downloads/> (Tkinter is included; tick **Add Python to PATH** during installation).

Open PowerShell and run:

```powershell
git clone https://github.com/spiyush09/distributedChatApplication.git
cd distributedChatApplication
py --version
```

Verify that Tkinter works (no output means it is fine):

```powershell
py -c "import tkinter"
```

## How to Run

Start the **server first**, then start one client for each user. Every command is run from the project folder.

### Linux (Fedora)

Terminal 1: the server

```bash
python3 server.py
```

Terminal 2 (and 3, 4, ... for more users): a client

```bash
python3 client.py
```

### Windows

PowerShell window 1: the server

```powershell
py server.py
```

PowerShell window 2 (and 3, 4, ... for more users): a client

```powershell
py client.py
```

### Choosing the interface

When a client starts, choose the interface:

```
1 = GUI (Tkinter)
2 = CMD (Terminal)
```

Press Enter or type 1 for the GUI, or type 2 for the terminal.

- **GUI mode:** Enter the Server IP, Port and Username, then click Connect. Type a message and press Enter or click Send.
- **CMD mode:** Enter the server IP and a username, then type your messages. Press Ctrl+C to leave the chat.

**Quick test on one computer:** run the server in one terminal, then open two or three more terminals and run `client.py` in each. Use `127.0.0.1` as the server IP.

## Using on LAN / Wi-Fi

All computers must be on the same network.

**1. Run the server on one computer and find its IP address.**

| System | Command |
| ------ | ------- |
| Linux (Fedora) | `hostname -I` |
| Windows | `ipconfig` (look for "IPv4 Address") |

**2. Allow port 5000 (TCP) through the server computer's firewall.** This is the most common reason a client on another computer cannot connect.

Linux (Fedora):

```bash
sudo firewall-cmd --add-port=5000/tcp
```

This is temporary and resets on reboot. To keep it permanently:

```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

Windows: click **Allow access** when Windows Defender Firewall asks about Python. Or open PowerShell **as Administrator** and run:

```powershell
New-NetFirewallRule -DisplayName "Chat Server 5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

**3. On the other computers, run `client.py` and enter the server's IP address.**

## How It Works

The server listens on port 5000 and creates a new thread for every client that connects. The client sends a username, and the server checks that no one else is using it. After that, when the server receives a message, it adds the time and username and sends it to all the other clients. The server also informs everyone when a user joins or leaves.

The client has a separate thread for receiving messages, so a user can receive messages while typing.

```
Client A ----\
Client B ------>  Server (port 5000, one thread per client)  ---> forwards to all other clients
Client C ----/
```

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `ModuleNotFoundError: No module named 'tkinter'` | Fedora: `sudo dnf install python3-tkinter`. Windows: reinstall Python and keep the tcl/tk option ticked. Or choose the terminal client (option 2). |
| `Connection refused` | The server is not running, or the IP or port is wrong. Start the server first. |
| Connection times out from another computer | Allow port 5000 in the firewall (see [Using on LAN / Wi-Fi](#using-on-lan--wi-fi)) and check that both computers are on the same network. |
| `Address already in use` when starting the server | An old server is still running, or another program is using port 5000. Close it and try again. |
| Username is rejected | Another user already has that name. Choose a different one. |
| `python3` / `py` is not recognized | Linux: install Python with `sudo dnf install python3`. Windows: reinstall Python and tick **Add Python to PATH**. |

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
- Running more than one server so the chat keeps working if one server fails
