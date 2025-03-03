import socket
import threading
import sys

def listen_for_inbound_chat(listen_sock):
    while True:
        try:
            conn, addr = listen_sock.accept()
            thread = threading.Thread(target=chat_receiver, args=(conn, addr))
            thread.start()
        except:
            break

def chat_receiver(conn, addr):
    print(f"\n[Chat] Incoming connection from {addr}.")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[Chat] Disconnected from {addr}")
                break
            message = data.decode()
            print(f"\n[From {addr}] {message}")
            print("> ", end="", flush=True)
    except:
        pass
    finally:
        conn.close()

def chat_sender(peer_ip, peer_port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((peer_ip, peer_port))
    print(f"[Chat] Connected to peer at {peer_ip}:{peer_port}")

    thread = threading.Thread(target=chat_receiver, args=(s, (peer_ip, peer_port)))
    thread.start()

    return s

def main():
    if len(sys.argv) < 4:
        print(f"Usage: python {sys.argv[0]} <clientID> <listenPort> <serverIP:serverPort>")
        sys.exit(1)

    client_id = sys.argv[1]
    listen_port = int(sys.argv[2])
    server_str = sys.argv[3]
    server_ip, server_port = server_str.split(':')
    server_port = int(server_port)
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(('127.0.0.1', listen_port))
    listen_sock.listen(5)

    # start background thread for inbound chat
    listen_thread = threading.Thread(target=listen_for_inbound_chat, args=(listen_sock,), daemon=True)
    listen_thread.start()

    outbound_chat_socket = None

    print(f"[Client] {client_id} running on 127.0.0.1:{listen_port}, server = {server_ip}:{server_port}")

    def send_to_server(payload):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall(payload.encode())
            s.settimeout(5)
            try:
                return s.recv(1024).decode()
            except socket.timeout:
                return "[timeout from server]"

    while True:
        try:
            cmd = input("> ").strip()
        except EOFError:
            break
        if not cmd:
            continue

        # command parser:
        if cmd == "/quit":
            print("[Client] Quitting.")
            # Close any outbound chat
            if outbound_chat_socket:
                outbound_chat_socket.close()
            listen_sock.close()
            break

        elif cmd == "/register":
            # Send REGISTER to server
            payload = (
                "REGISTER\r\n"
                f"clientID: {client_id}\r\n"
                "IP: 127.0.0.1\r\n"
                f"Port: {listen_port}\r\n"
                "\r\n"
            )
            resp = send_to_server(payload)
            print("[Server Response]\n", resp)

        elif cmd == "/info":
            # Send INFO to server
            payload = "INFO\r\nRequesting clients\r\n\r\n"
            resp = send_to_server(payload)
            print("[Server Response]\n", resp)

        elif cmd == "/bridge":
            # Attempt to get bridging info from server
            payload = (
                "BRIDGE\r\n"
                f"clientID: {client_id}\r\n"
                "\r\n"
            )
            resp = send_to_server(payload)
            print("[Server Response]\n", resp)

            # Attempt to parse out ip/port from the response
            lines = resp.splitlines()
            if "BRIDGEACK" in lines[0]:
                found_ip = None
                found_port = None
                for line in lines[1:]:
                    if line.startswith("IP: "):
                        found_ip = line.split(": ", 1)[1]
                    elif line.startswith("Port: "):
                        found_port = line.split(": ", 1)[1]
                if found_ip and found_port:
                    if found_ip.strip() != "" and found_port.strip() != "":
                        print(f"[Client] Bridge found peer {found_ip}:{found_port}")
                    else:
                        print("[Client] No peer found, you might wait for inbound chat.")
                else:
                    print("[Client] Could not parse bridging info.")
            else:
                print("[Client] Bridge request failed or had no data.")

        elif cmd.startswith("/chat "):
            # /chat <IP>:<PORT>
            try:
                _, peer = cmd.split()
                peer_ip, peer_port = peer.split(":")
                peer_port = int(peer_port)

                outbound_chat_socket = chat_sender(peer_ip, peer_port)
                print("[Client] You can now type messages to send them to the peer.")
            except Exception as e:
                print("[Client] Usage: /chat IP:PORT. Error:", e)

        elif cmd.startswith("/msg "):
            if not outbound_chat_socket:
                print("[Client] No outbound chat connection. Use /chat first or wait for inbound.")
            else:
                message = cmd[5:]  # everything after '/msg '
                try:
                    outbound_chat_socket.sendall(message.encode())
                except OSError:
                    print("[Client] Connection error. The peer may have closed.")
                    outbound_chat_socket = None

        else:
            print("[Client] Available commands:")
            print("  /register       Register with server")
            print("  /info           Get list of known clients from server")
            print("  /bridge         Request bridging info from server")
            print("  /chat IP:PORT   Connect to a peer's chat socket")
            print("  /msg <text>     Send a message to the peer (outbound connection)")
            print("  /quit           Quit client")

    print("[Client] Exited.")

if __name__ == "__main__":
    main()
