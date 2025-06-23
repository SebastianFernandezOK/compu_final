import socket  # Para comunicación de red
import threading  # Para manejo de hilos
import argparse  # Para parseo de argumentos de línea de comandos
import ipaddress  # Para detectar tipo de IP
import multiprocessing  # Para procesos y colas entre procesos
from server.core import accept_connections  # Importa la función para aceptar conexiones
from server.moderador import moderador  # Importa el proceso moderador

def main():
    """
    Punto de entrada principal del servidor de chat.
    Configura argumentos, crea sockets IPv4/IPv6 en puertos diferentes, lanza el proceso moderador y los hilos de escucha.
    """
    parser = argparse.ArgumentParser(description='Servidor de chat tipo Discord')  # Parser de argumentos
    parser.add_argument('--host', default='127.0.0.1', help='Dirección IP para escuchar (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Puerto para IPv4 (default: 5000)')
    parser.add_argument('--port6', type=int, default=5001, help='Puerto para IPv6 (default: 5001)')
    args = parser.parse_args()  # Parsea los argumentos
    host = args.host
    port = args.port
    port6 = args.port6

    queue_in = multiprocessing.Queue()   # Queue de entrada para mensajes al moderador
    queue_out = multiprocessing.Queue()  # Queue de salida para respuestas del moderador
    mod_proc = multiprocessing.Process(target=moderador, args=(queue_in, queue_out))  # Crea proceso moderador
    mod_proc.start()  # Inicia el proceso moderador

    # Socket IPv4
    ipv4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket IPv4
    ipv4_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar dirección IPv4
    ipv4_socket.bind(('0.0.0.0', port))  # Enlaza socket IPv4 a todas las interfaces
    ipv4_socket.listen()  # Escucha conexiones IPv4
    print(f"[ESCUCHANDO] Servidor IPv4 en 0.0.0.0:{port}")  # Mensaje de escucha IPv4
    threading.Thread(target=accept_connections, args=(ipv4_socket, queue_in, queue_out), daemon=True).start()  # Hilo para IPv4

    # Socket IPv6 en puerto diferente
    ipv6_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # Socket IPv6
    ipv6_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar dirección IPv6
    ipv6_socket.bind(('::', port6))  # Enlaza socket IPv6 a todas las interfaces en otro puerto
    ipv6_socket.listen()  # Escucha conexiones IPv6
    print(f"[ESCUCHANDO] Servidor IPv6 en [::]:{port6}")  # Mensaje de escucha IPv6
    threading.Thread(target=accept_connections, args=(ipv6_socket, queue_in, queue_out), daemon=True).start()  # Hilo para IPv6

    while True:
        threading.Event().wait(1)  # Mantiene el hilo principal vivo

if __name__ == "__main__":
    main()  # Ejecuta el servidor si el archivo se corre directamente
