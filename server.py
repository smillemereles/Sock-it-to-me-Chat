import socket
import select

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 12345

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    # Lista de sockets que serán monitoreados
    sockets_list = [server_socket]

    while True:
        readable, _, _ = select.select(sockets_list, [], [])

        for notified_socket in readable:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)
                print(f"Cliente {client_address} conectado")
            else:
                message = notified_socket.recv(1024).decode('utf-8')
                if not message:
                    sockets_list.remove(notified_socket)
                    notified_socket.close()
                    print(f"Cliente {notified_socket.getpeername()} desconectado")
                    continue

                print(f"Mensaje recibido: {message}")
                for sock in sockets_list:
                    if sock != server_socket and sock != notified_socket:
                        try:
                            sock.send(message.encode('utf-8'))
                        except BrokenPipeError:
                            sockets_list.remove(sock)
                            sock.close()

if __name__ == "__main__":
    main()
