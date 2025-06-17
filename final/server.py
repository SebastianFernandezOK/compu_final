import socket  # Módulo para comunicación de red
import threading  # Módulo para concurrencia con hilos
import argparse   # Módulo para parseo de argumentos

HOST = '127.0.0.1'  # Dirección IP local donde el servidor escuchará
PORT = 12345        # Puerto donde el servidor aceptará conexiones

clients = []  # Lista global para guardar los sockets de los clientes conectados
client_groups = {}  # Diccionario: socket -> nombre de grupo
chat_groups = {}    # Diccionario: nombre de grupo -> lista de sockets

def broadcast(message, group, sender_conn):
    """
    Envía el mensaje a todos los clientes del grupo excepto al remitente.
    """
    for client in chat_groups.get(group, []):
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                pass  # Si falla, ignora ese cliente

def handle_client(conn, addr):
    """
    Atiende a un cliente conectado.
    Procesa comandos para crear/unirse/listar/salir de grupos y reenvía mensajes solo a miembros del grupo.
    """
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    grupo_actual = None
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            if msg.startswith('/crear '):
                nombre_grupo = msg[7:].strip()
                if nombre_grupo in chat_groups:
                    conn.sendall(f"El grupo '{nombre_grupo}' ya existe.".encode())
                else:
                    chat_groups[nombre_grupo] = [conn]
                    client_groups[conn] = nombre_grupo
                    grupo_actual = nombre_grupo
                    conn.sendall(f"Grupo '{nombre_grupo}' creado y unido.".encode())
            elif msg.startswith('/unir '):
                nombre_grupo = msg[6:].strip()
                if nombre_grupo not in chat_groups:
                    conn.sendall(f"El grupo '{nombre_grupo}' no existe.".encode())
                else:
                    if conn not in chat_groups[nombre_grupo]:
                        chat_groups[nombre_grupo].append(conn)
                    client_groups[conn] = nombre_grupo
                    grupo_actual = nombre_grupo
                    conn.sendall(f"Unido al grupo '{nombre_grupo}'.".encode())
            elif msg.startswith('/listar'):
                if chat_groups:
                    lista = ', '.join(chat_groups.keys())
                    conn.sendall(f"Grupos disponibles: {lista}".encode())
                else:
                    conn.sendall("No hay grupos disponibles.".encode())
            elif msg.startswith('/salir'):
                if grupo_actual and grupo_actual in chat_groups and conn in chat_groups[grupo_actual]:
                    chat_groups[grupo_actual].remove(conn)
                    conn.sendall(f"Saliste del grupo '{grupo_actual}'.".encode())
                    del client_groups[conn]
                    grupo_actual = None
                else:
                    conn.sendall("No estás en ningún grupo.".encode())
            else:
                # Mensaje normal: solo se reenvía si está en un grupo
                if grupo_actual and grupo_actual in chat_groups:
                    print(f"[{addr}][{grupo_actual}] {msg}")
                    broadcast(f"[{addr}][{grupo_actual}] {msg}".encode(), grupo_actual, conn)
                else:
                    conn.sendall("Debes crear o unirte a un grupo para enviar mensajes.".encode())
        except:
            break
    print(f"[DESCONECTADO] {addr}")
    # Elimina al cliente de los grupos y listas
    if conn in clients:
        clients.remove(conn)
    if conn in client_groups:
        grupo = client_groups[conn]
        if grupo in chat_groups and conn in chat_groups[grupo]:
            chat_groups[grupo].remove(conn)
        del client_groups[conn]
    conn.close()

def main():
    """
    Función principal del servidor.
    Parsea argumentos, crea el socket, lo enlaza a la IP y puerto, y acepta conexiones entrantes.
    Por cada cliente, crea un hilo para atenderlo.
    """
    parser = argparse.ArgumentParser(description='Servidor de chat tipo Discord')
    parser.add_argument('--host', default='127.0.0.1', help='Dirección IP para escuchar (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=12345, help='Puerto para escuchar (default: 12345)')
    args = parser.parse_args()
    host = args.host
    port = args.port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea el socket TCP
    server.bind((host, port))  # Asocia el socket a la IP y puerto
    server.listen()  # Comienza a escuchar conexiones entrantes
    print(f"[ESCUCHANDO] Servidor en {host}:{port}")
    while True:
        conn, addr = server.accept()  # Espera una nueva conexión de cliente
        clients.append(conn)  # Agrega el socket del cliente a la lista global
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()  # Inicia el hilo
        print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")  # Muestra cantidad de clientes conectados

if __name__ == "__main__":
    main()  # Ejecuta la función principal si el archivo se corre directamente
