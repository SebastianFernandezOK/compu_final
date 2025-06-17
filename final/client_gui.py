"""


En este proyecto, se detecta automáticamente el tipo de dirección IP (IPv4 o IPv6) y se crea el socket adecuado, permitiendo que el chat funcione en cualquier red moderna.
"""
"""
Cliente de chat tipo Discord (interfaz gráfica).
Permite conectarse a un servidor, crear y unirse a grupos, y enviar mensajes a los miembros del grupo usando una GUI con Tkinter.
Comandos disponibles:
  /crear <grupo>   - Crea y se une a un grupo
  /unir <grupo>    - Se une a un grupo existente
  /listar          - Lista los grupos disponibles
  /salir           - Sale del grupo actual
  /ayuda           - Muestra esta ayuda
  (Los mensajes normales se reenvían solo a los miembros del grupo)
"""
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import argparse
import ipaddress  # <--- Import para detectar tipo de IP

class ChatClientGUI:
    """
    Clase principal para la interfaz gráfica del cliente de chat.
    Gestiona la conexión, la recepción y el envío de mensajes, y la interacción con el usuario.
    """
    def __init__(self, master, host, port, usuario):
        """
        Inicializa la ventana principal, conecta al servidor (IPv4 o IPv6) y configura los widgets.
        Args:
            master (tk.Tk): Ventana raíz de Tkinter.
            host (str): IP del servidor.
            port (int): Puerto del servidor.
            usuario (str): Nombre de usuario.
        """
        self.master = master
        self.master.title(f"Chat - Usuario: {usuario}")
        self.host = host
        self.port = port
        self.usuario = usuario
        # Detecta si la IP es IPv4 o IPv6
        try:
            ip_obj = ipaddress.ip_address(self.host)
            if ip_obj.version == 6:
                family = socket.AF_INET6
            else:
                family = socket.AF_INET
        except ValueError:
            # Si no es una IP válida, asume IPv4 (por ejemplo, 'localhost')
            family = socket.AF_INET
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            self.master.destroy()
            return
        # Área de texto para mostrar mensajes
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        # Entrada de texto para escribir mensajes
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.entry.bind('<Return>', self.enviar_mensaje)
        # Botón para enviar mensajes
        self.boton = tk.Button(master, text="Enviar", command=self.enviar_mensaje)
        self.boton.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))
        # Maneja el cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.running = True
        # Hilo para recibir mensajes del servidor
        threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        self.mostrar_ayuda()

    def mostrar_ayuda(self):
        """
        Muestra los comandos disponibles en el área de mensajes.
        """
        ayuda = ("Comandos disponibles:\n"
                 "/crear <grupo>   - Crea y se une a un grupo\n"
                 "/unir <grupo>    - Se une a un grupo existente\n"
                 "/listar          - Lista los grupos disponibles\n"
                 "/salir           - Sale del grupo actual\n"
                 "/ayuda           - Muestra esta ayuda\n"
                 "(Escribe un mensaje para enviarlo al grupo)\n")
        self.mostrar_mensaje(ayuda)

    def mostrar_mensaje(self, mensaje):
        """
        Inserta un mensaje en el área de texto y hace scroll automático.
        Args:
            mensaje (str): Mensaje a mostrar.
        """
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, mensaje + '\n')
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def enviar_mensaje(self, event=None):
        """
        Envía el mensaje escrito al servidor y lo muestra en la interfaz si es propio.
        """
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
        """
        Hilo que recibe mensajes del servidor y los muestra en la interfaz.
        """
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
        """
        Cierra la conexión y la ventana de la aplicación.
        """
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

def main():
    """
    Parsea argumentos de línea de comandos y lanza la interfaz gráfica del cliente.
    """
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
