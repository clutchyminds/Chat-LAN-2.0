import socket
import threading
import tkinter as tk

def start_server():
    def handle_connection(conn):
        while True:
            try:
                msg = conn.recv(1024).decode()
                chat.insert(tk.END, msg + "\n")
            except:
                conn.close()
                break

    def listen():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', int(my_port.get())))
        server.listen()
        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle_connection, args=(conn,), daemon=True).start()

    threading.Thread(target=listen, daemon=True).start()

def connect_to_peer():
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.connect((peer_ip.get(), int(peer_port.get())))
    connections.append(peer)

def send_message():
    msg = f"{username.get()} : {message_entry.get()}"
    for conn in connections:
        conn.send(msg.encode())
    chat.insert(tk.END, msg + "\n")
    message_entry.delete(0, tk.END)

connections = []

window = tk.Tk()
window.title("Chat P2P")

tk.Label(window, text="Ton pseudo").pack()
username = tk.Entry(window)
username.pack()

tk.Label(window, text="Ton port (à écouter)").pack()
my_port = tk.Entry(window)
my_port.pack()

tk.Button(window, text="Démarrer réception", command=start_server).pack()

tk.Label(window, text="IP de l’autre").pack()
peer_ip = tk.Entry(window)
peer_ip.pack()

tk.Label(window, text="Port de l’autre").pack()
peer_port = tk.Entry(window)
peer_port.pack()

tk.Button(window, text="Se connecter", command=connect_to_peer).pack()

chat = tk.Text(window)
chat.pack()

message_entry = tk.Entry(window)
message_entry.pack()

tk.Button(window, text="Envoyer", command=send_message).pack()

window.mainloop()
