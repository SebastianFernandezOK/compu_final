import socket  # Módulo para comunicación de red
import threading  # Módulo para concurrencia
import argparse   # Módulo para parseo de argumentos

HOST = '127.0.0.1'  # IP del servidor al que conectarse
PORT = 12345        # Puerto del servidor

AYUDA = '''\nComandos disponibles:\n  /crear <grupo>   - Crea y se une a un grupo\n  /unir <grupo>    - Se une a un grupo existente\n  /listar          - Lista los grupos disponibles\n  /salir           - Sale del grupo actual\n  /ayuda           - Muestra esta ayuda\n  (Escribe un mensaje para enviarlo al grupo)\n'''

def recibir_mensajes(sock):
    """
    Hilo que recibe mensajes del servidor y los muestra por pantalla.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print('\n' + data.decode())
        except:
            break

def main():
    """
    Cliente que se conecta al servidor, envía mensajes y comandos, y recibe mensajes de otros clientes.
    """
    parser = argparse.ArgumentParser(description='Cliente de chat tipo Discord')
    parser.add_argument('--host', default='127.0.0.1', help='IP del servidor (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12345, help='Puerto del servidor (default: 12345)')
    parser.add_argument('--usuario', default='anonimo', help='Nombre de usuario (default: anonimo)')
    args = parser.parse_args()
    host = args.host
    port = args.port
    usuario = args.usuario

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Conecta al servidor
        print(f"Conectado al servidor {host}:{port}")
        print(AYUDA)
        # Inicia un hilo para recibir mensajes del servidor
        thread = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
        thread.start()
        while True:
            msg = input(f'{usuario}> Mensaje o comando (enter para salir): ')
            if not msg:
                break  # Si el usuario no escribe nada, sale
            if msg == '/ayuda':
                print(AYUDA)
                continue
            # Adjunta el nombre de usuario a los mensajes normales
            if msg.startswith('/'):
                s.sendall(msg.encode())
            else:
                s.sendall(f'{usuario}: {msg}'.encode())
    print("Desconectado.")

if __name__ == "__main__":
    main()
