
```markdown
# Client-Server Local Chat

A simple local chat application built with Python sockets. This project allows multiple users on the same local network to chat in real time via a central server.

## How it Works

- A **server** runs and listens for client connections.
- **Clients** connect to the server and send messages.
- Messages are broadcasted to all connected clients.

## Requirements

- Python 3.x

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/SummerBoi718/client-server-localchat.git
   cd client-server-localchat
   ```

2. Start the app:

   ```bash
   python cli_menu.py
   ```

3. Use the menu to:
   - Start the server
   - Join as a client
   - Resolve server IP and port using `ipport_resolver.py`

> All users must be connected to the same local network for the chat to work.

## File Overview

- `cli_menu.py` – Main menu for starting the server or client
- `server.py` – Handles incoming connections and message broadcasting
- `client.py` – Connects to the server and sends/receives messages
- `ipport_resolver.py` – Helps retrieve local IP address and choose a port
```
