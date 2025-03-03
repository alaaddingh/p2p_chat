import socket
import threading

connected_clients = []  # list of tuples: (client_id, ip, port)

def handle_client(conn, addr):
    """
    Each new client connection (for registration/bridge/info) is handled in this thread.
    After processing the request, we close the connection.
    """
    data = conn.recv(1024)
    if not data:
        conn.close()
        return

    lines = data.decode().splitlines()
    if not lines:
        conn.close()
        return

    request_type = lines[0].strip()
    headers = lines[1:]  # everything after the first line

    if request_type == "REGISTER":
        client_id = None
        ip = None
        port = None
        for line in headers:
            if line.startswith("clientID: "):
                client_id = line.split(": ", 1)[1].strip()
            elif line.startswith("IP: "):
                ip = line.split(": ", 1)[1].strip()
            elif line.startswith("Port: "):
                port = line.split(": ", 1)[1].strip()

        if client_id and ip and port:
            connected_clients.append((client_id, ip, port))
            print(f"[Server] Registered {client_id} at {ip}:{port}")
            response = (
                f"REGACK\r\n"
                f"clientID: {client_id}\r\n"
                f"IP: {ip}\r\n"
                f"Port: {port}\r\n"
                f"Status: registered\r\n\r\n"
            )
            conn.sendall(response.encode())

    elif request_type == "BRIDGE":
        # Parse which client is requesting bridging
        requesting_id = None
        for line in headers:
            if line.startswith("clientID: "):
                requesting_id = line.split(": ", 1)[1].strip()

        # Find *another* client to connect to
        # (in real usage, we'd have a more direct or user-chosen approach)
        found_client = None
        for (c_id, c_ip, c_port) in connected_clients:
            if c_id != requesting_id:
                found_client = (c_id, c_ip, c_port)
                break

        if found_client:
            c_id, c_ip, c_port = found_client
            print(f"[Server] BRIDGE request from {requesting_id}, returning {c_id} {c_ip}:{c_port}")
            response = (
                f"BRIDGEACK\r\n"
                f"clientID: {c_id}\r\n"
                f"IP: {c_ip}\r\n"
                f"Port: {c_port}\r\n\r\n"
            )
            conn.sendall(response.encode())
        else:
            # No other client found, respond with empty
            print(f"[Server] BRIDGE request from {requesting_id}, but no other clients found.")
            response = (
                "BRIDGEACK\r\n"
                "clientID: \r\n"
                "IP: \r\n"
                "Port: \r\n\r\n"
            )
            conn.sendall(response.encode())

    elif request_type == "INFO":
        print("[Server] INFO request received.")
        # Build a list of all connected clients
        response = "INFOACK\r\n"
        for (c_id, c_ip, c_port) in connected_clients:
            response += f"{c_id} {c_ip}:{c_port}\r\n"
        response += "\r\n"
        conn.sendall(response.encode())

    conn.close()

def main():
    HOST = '127.0.0.1'
    PORT = 5555

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[Server] Listening on {HOST}:{PORT}")

    try:
        while True:
            client_conn, client_addr = server_sock.accept()
            thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
