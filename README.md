# 💬 ChatPals - Simple Socket Chat Room

A colorful real-time chat room built with Python sockets and threading. This is an **educational project** created to understand networking fundamentals, client-server architecture, and concurrent programming.

## 🎯 Project Status


This project was built to explore:
- Socket programming (TCP/IP)
- Multi-threading for concurrent connections
- Basic client-server architecture
- Console-based colored output with ANSI codes
- Welcome banners and visual enhancements

## ✨ Features

- ✅ Real-time messaging between multiple users
- ✅ Automatic color assignment for each user (8 different colors)
- ✅ Join/leave notifications with emojis
- ✅ Colorful welcome banner with ASCII art
- ✅ Clear screen on connection for better UX
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Console-based interface (lightweight)
- ✅ Supports local network connections

## 🎨 Visual Features

- Color-coded usernames
- Welcome banner with "ChatPals" ASCII art
- Clean screen clearing on connect
- Emoji notifications (✨, 💔)
- Colored server console output

## ❌ Limitations (Not Implemented Yet)

- ❌ No message history (messages disappear when server restarts)
- ❌ No encryption (for local/learning use only)
- ❌ No user authentication (anyone can use any name)
- ❌ No private messaging (only public chat)
- ❌ No file sharing or media support
- ❌ No database storage
- ❌ No GUI interface (console only)
- ❌ No kick/ban functionality for moderators


## 🗺️ Future Plans

- [ ] Add message persistence (SQLite)
- [ ] Implement basic authentication (username/password)
- [ ] Create GUI version (Tkinter/PyQt)
- [ ] Add private messaging (/msg command)
- [ ] Add command system (/help, /users, /clear)
- [ ] Add WebSocket version with Django Channels
- [ ] Docker support for easy deployment

---

> 🤖 **Note:**Some portions were developed with assistance from AI  to help understand concepts, debug issues, and improve code quality. The majority of the logic and understanding comes from personal effort.

## 📋 Prerequisites

- Python 3 or higher
- No external libraries required (uses only standard library)

## 🧪 Run Everything on One Computer (For Testing)

You don't need multiple computers or a network to test ChatPals! Everything can run on your **single laptop/PC**.

or

## Connect with a Friend on the Same Local Network (WiFi)

Want to chat with your friend who is in the **same house, same coffee shop, or same office WiFi**? Follow this:


## 🚀 How to Run

### 1. Start the Server

Open a terminal and run:

```bash
python server.py
```

You'll see:

```text
==================================================
🖥️  CHATPALS SERVER STARTED
==================================================
🏠 Your Local IP: 192.168.1.X
🔌 Port: 8888
✅ Server is running and waiting for connections...
```

### 2. Start Clients (Users)
Open new terminals for each user and run:

```bash
python client.py
```

Then:

Enter your name

See the welcome banner

Start chatting!

### 3. Connect from Different Computers
To chat across a local network:

On Server Computer:

```python
# In server.py - already configured
ip_server = "0.0.0.0"  # Listens on all network interfaces
port_server = 8888
```

On Client Computers:

```python
# In client.py - change to the server's actual IP
ip_server = "192.168.1.X"  # Replace with server's local IP
port_server = 8888
```

To find the server's IP:

- **windows:** Run `ipconfig` in CMD, look for "IPv4 Address"
- **Linux:** Run `ip a` or `ifconfig`, look for "inet" (usually 192.168.x.x)
- **Mac:** Run `ifconfig`, look for "inet" under en0 (usually 192.168.x.x)

### 4. Exit Chat
Type `close` and press Enter.
