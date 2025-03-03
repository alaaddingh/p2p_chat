P2P Chat with Registration and Bridging

This repository contains a minimal peer-to-peer chat prototype that uses a central server for registration and bridging, then lets clients connect directly to each other for real-time text chat. It demonstrates key socket programming and basic protocol concepts, inspired by typical assignments in networking classes.
Overview

    Server (server.py):
        Maintains a list of connected clients (client ID, IP, port).
        Accepts REGISTER, BRIDGE, and INFO requests from clients.
        Provides bridging info (IP and port) of another client so a direct, peer-to-peer chat can be established.

    Client (client.py):
        Registers itself with the server using /register.
        Requests another client’s IP/port using /bridge.
        Opens a listening socket to accept inbound connections.
        Can initiate an outbound connection to another client, sending and receiving chat messages directly over TCP.

Goal

    Educational Objective:
        Practice socket programming in Python.
        Explore the basic idea of how protocols like SIP (Session Initiation Protocol) can “introduce” endpoints for direct communication.
        Understand multi-threaded or event-based designs necessary for real-time, two-way data exchange.

Instructions

    Setup
        Install Python 3 on your system.
        Clone this repository or download the server.py and client.py files.

    Run the Server
        In one terminal (e.g., PowerShell), run:

    python server.py

    The server listens on 127.0.0.1:5555 by default.

Run a Client

    Open another terminal and run:

python client.py <clientID> <listenPort> 127.0.0.1:5555

For example:

    python client.py alice 5556 127.0.0.1:5555

    The client starts listening on 127.0.0.1:<listenPort> for inbound chat connections.

Commands (enter in the client’s console):

    /register
    Register with the server (sends client ID and listening port).
    /info
    Ask the server to list all known clients.
    /bridge
    Request another client’s IP/Port from the server (if available).
    /chat IP:PORT
    Connect directly (outbound) to a peer’s IP/port for chat.
    /msg <message>
    Send a text message to the currently connected peer.
    /quit
    Quit the client application.

Try Multiple Clients

    In separate terminals, run:

        python client.py bob 5557 127.0.0.1:5555
        python client.py carol 5558 127.0.0.1:5555
        ...

        Each can /register, then use /bridge to find a peer, then /chat <peerIP>:<peerPort> to connect directly.

Learning Outcomes

    Socket Programming: Gained experience with both server and client TCP sockets in Python.
    Multi-Threading: Demonstrated separate threads for listening and sending, avoiding blocking console issues on Windows.
    Custom Protocol Concepts: Implemented minimal message headers (REGISTER, BRIDGE, INFO, etc.) to control session establishment and bridging.
    P2P vs. Centralized: Showed how a lightweight server can facilitate direct client-to-client connections (a simplified model of SIP and similar protocols).

This project is a straightforward example of how clients can register with a central directory service and then communicate peer-to-peer once they receive each other’s contact info, all while respecting Windows’ console I/O limitations
