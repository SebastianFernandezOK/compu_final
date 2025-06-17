import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import argparse

class ChatClientGUI:
    def __init__(self, master, host, port, usuario):
        self.master = master
        self.master.title(f"Chat - Usuario: {usuario}")
        self.host = host
        self.port = port
        self.usuario = usuario
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            self.master.destroy()
            return
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.entry.bind('<Return>', self.enviar_mensaje)
        self.boton = tk.Button(master, text="Enviar", command=self.enviar_mensaje)
        self.boton.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.running = True
        threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        self.mostrar_ayuda()

    def mostrar_ayuda(self):
        ayuda = ("Comandos disponibles:\n"
                 "/crear <grupo>   - Crea y se une a un grupo\n"
                 "/unir <grupo>    - Se une a un grupo existente\n"
                 "/listar          - Lista los grupos disponibles\n"
                 "/salir           - Sale del grupo actual\n"
                 "/ayuda           - Muestra esta ayuda\n"
                 "(Escribe un mensaje para enviarlo al grupo)\n")
        self.mostrar_mensaje(ayuda)

    def mostrar_mensaje(self, mensaje):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, mensaje + '\n')
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def enviar_mensaje(self, event=None):
        msg = self.entry.get()
        if not msg:
            return
        if msg == '/ayuda':
            self.mostrar_ayuda()
        elif msg.startswith('/'):
            self.sock.sendall(msg.encode())
        else:
            mensaje_formateado = f'{self.usuario}: {msg}'
            self.sock.sendall(mensaje_formateado.encode())
            self.mostrar_mensaje(mensaje_formateado)  # Mostrar el mensaje propio inmediatamente
        self.entry.delete(0, tk.END)

    def recibir_mensajes(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.mostrar_mensaje(data.decode())
            except:
                break
        self.mostrar_mensaje("[Desconectado del servidor]")

    def cerrar(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

def main():
    parser = argparse.ArgumentParser(description='Cliente de chat tipo Discord (GUI)')
    parser.add_argument('--host', default='127.0.0.1', help='IP del servidor (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12345, help='Puerto del servidor (default: 12345)')
    parser.add_argument('--usuario', default='anonimo', help='Nombre de usuario (default: anonimo)')
    args = parser.parse_args()
    root = tk.Tk()
    app = ChatClientGUI(root, args.host, args.port, args.usuario)
    root.mainloop()

if __name__ == "__main__":
    main()
