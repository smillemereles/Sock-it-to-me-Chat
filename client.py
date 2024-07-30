import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente de Chat")
        
        # Configuración de la interfaz gráfica
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled')
        self.chat_display.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # Conexión al servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Hilo para recibir mensajes
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_display.config(state='normal')
                    self.chat_display.insert(tk.END, message + '\n')
                    self.chat_display.config(state='disabled')
                    self.chat_display.yview(tk.END)
            except ConnectionAbortedError:
                break

    def send_message(self, event):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
