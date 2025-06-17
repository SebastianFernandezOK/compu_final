"""
En este proyecto, se detecta automáticamente el tipo de dirección IP (IPv4 o IPv6) y se crea el socket adecuado, permitiendo que el chat funcione en cualquier red moderna.
"""
"""
Cliente de chat tipo Discord (consola).
Permite conectarse a un servidor, crear y unirse a grupos, y enviar mensajes a los miembros del grupo.
Comandos disponibles:
  /crear <grupo>   - Crea y se une a un grupo
  /unir <grupo>    - Se une a un grupo existente
  /listar          - Lista los grupos disponibles
  /salir           - Sale del grupo actual
  /ayuda           - Muestra esta ayuda
  (Los mensajes normales se reenvían solo a los miembros del grupo)
"""
import socket  # Módulo para comunicación de red
import threading  # Módulo para concurrencia
import argparse   # Módulo para parseo de argumentos
import ipaddress  # <--- Import para detectar tipo de IP

# Mensaje de ayuda para mostrar los comandos disponibles
AYUDA = '''\nComandos disponibles:\n  /crear <grupo>   - Crea y se une a un grupo\n  /unir <grupo>    - Se une a un grupo existente\n  /listar          - Lista los grupos disponibles\n  /salir           - Sale del grupo actual\n  /ayuda           - Muestra esta ayuda\n  (Escribe un mensaje para enviarlo al grupo)\n'''

def recibir_mensajes(sock):
    """
    Hilo que recibe mensajes del servidor y los muestra por pantalla.
    Args:
        sock (socket): Socket conectado al servidor.
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
    Parsea argumentos de línea de comandos para host, puerto y usuario.
    Soporta tanto IPv4 como IPv6.
    """
    parser = argparse.ArgumentParser(description='Cliente de chat tipo Discord')
    parser.add_argument('--host', default='127.0.0.1', help='IP del servidor (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12345, help='Puerto del servidor (default: 12345)')
    parser.add_argument('--usuario', default='anonimo', help='Nombre de usuario (default: anonimo)')
    args = parser.parse_args()
    host = args.host
    port = args.port
    usuario = args.usuario

    # Detecta si la IP es IPv4 o IPv6
    try:
        ip_obj = ipaddress.ip_address(host)
        if ip_obj.version == 6:
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
    except ValueError:
        # Si no es una IP válida, asume IPv4 (por ejemplo, 'localhost')
        family = socket.AF_INET

    with socket.socket(family, socket.SOCK_STREAM) as s:
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
