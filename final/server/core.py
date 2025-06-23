import socket  # Importa el módulo para comunicación de red
import threading  # Importa el módulo para manejo de hilos
import uuid  # Para generar identificadores únicos de mensaje

# Lista de sockets de todos los clientes conectados actualmente
clients = []  # Lista global de clientes conectados
# Diccionario que asocia cada socket de cliente con el nombre del grupo al que pertenece
client_groups = {}  # socket -> nombre de grupo
# Diccionario que asocia el nombre de cada grupo con la lista de sockets de los clientes que están en ese grupo
chat_groups = {}  # nombre de grupo -> lista de sockets

def broadcast(message, group, sender_conn):
    """
    Envía el mensaje a todos los clientes del grupo excepto al remitente.
    """
    for client in chat_groups.get(group, []):  # Recorre todos los clientes del grupo
        if client != sender_conn:  # No envía el mensaje al remitente
            try:
                client.sendall(message)  # Envía el mensaje al cliente
            except:
                pass  # Si falla, ignora ese cliente

def handle_client(conn, addr, queue_in, queue_out):
    """
    Atiende a un cliente conectado y procesa comandos.
    """
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")  # Muestra nueva conexión
    grupo_actual = None  # Grupo actual del usuario
    while True:
        try:
            data = conn.recv(1024)  # Recibe datos del cliente
            if not data:
                break  # Si no hay datos, termina el bucle
            msg = data.decode().strip()  # Decodifica el mensaje recibido
            if msg.startswith('/crear '):  # Si el mensaje es para crear grupo
                nombre_grupo = msg[7:].strip()  # Obtiene el nombre del grupo
                if nombre_grupo in chat_groups:
                    conn.sendall(f"El grupo '{nombre_grupo}' ya existe.".encode())  # Grupo ya existe
                else:
                    chat_groups[nombre_grupo] = [conn]  # Crea el grupo y agrega al usuario
                    client_groups[conn] = nombre_grupo  # Asocia el usuario al grupo
                    grupo_actual = nombre_grupo  # Actualiza grupo actual
                    conn.sendall(f"Grupo '{nombre_grupo}' creado y unido.".encode())  # Confirma creación
            elif msg.startswith('/unir '):  # Si el mensaje es para unirse a grupo
                nombre_grupo = msg[6:].strip()  # Obtiene el nombre del grupo
                if nombre_grupo not in chat_groups:
                    conn.sendall(f"El grupo '{nombre_grupo}' no existe.".encode())  # Grupo no existe
                else:
                    if conn not in chat_groups[nombre_grupo]:
                        chat_groups[nombre_grupo].append(conn)  # Agrega usuario al grupo
                    client_groups[conn] = nombre_grupo  # Asocia el usuario al grupo
                    grupo_actual = nombre_grupo  # Actualiza grupo actual
                    conn.sendall(f"Unido al grupo '{nombre_grupo}'.".encode())  # Confirma unión
            elif msg.startswith('/listar'):  # Si el mensaje es para listar grupos
                if chat_groups:
                    lista = ', '.join(chat_groups.keys())  # Lista de grupos
                    conn.sendall(f"Grupos disponibles: {lista}".encode())  # Envía lista
                else:
                    conn.sendall("No hay grupos disponibles.".encode())  # No hay grupos
            elif msg.startswith('/salir'):  # Si el mensaje es para salir del grupo
                if grupo_actual and grupo_actual in chat_groups and conn in chat_groups[grupo_actual]:
                    chat_groups[grupo_actual].remove(conn)  # Quita usuario del grupo
                    conn.sendall(f"Saliste del grupo '{grupo_actual}'.".encode())  # Confirma salida
                    del client_groups[conn]  # Elimina asociación usuario-grupo
                    grupo_actual = None  # Sin grupo actual
                else:
                    conn.sendall("No estás en ningún grupo.".encode())  # No estaba en grupo
            else:
                if grupo_actual and grupo_actual in chat_groups:  # Si está en un grupo
                    print(f"[{addr}][{grupo_actual}] {msg}")  # Muestra mensaje en consola
                    id_mensaje = str(uuid.uuid4())  # Genera un id único para el mensaje
                    queue_in.put((msg, conn, id_mensaje))  # Envía mensaje al moderador
                    permitido = False
                    # Espera la respuesta del moderador
                    while True:
                        resp, resp_id = queue_out.get()
                        if resp_id == id_mensaje:
                            permitido = resp
                            break
                    if permitido:
                        broadcast(f"[{addr}][{grupo_actual}] {msg}".encode(), grupo_actual, conn)  # Reenvía mensaje
                    # Si no está permitido, el moderador ya avisó al usuario
                else:
                    conn.sendall("Debes crear o unirte a un grupo para enviar mensajes.".encode())  # No está en grupo
        except:
            break  # Si hay error, termina el bucle
    print(f"[DESCONECTADO] {addr}")  # Muestra desconexión
    if conn in clients:
        clients.remove(conn)  # Quita usuario de la lista global
    if conn in client_groups:
        grupo = client_groups[conn]  # Obtiene grupo del usuario
        if grupo in chat_groups and conn in chat_groups[grupo]:
            chat_groups[grupo].remove(conn)  # Quita usuario del grupo
        del client_groups[conn]  # Elimina asociación usuario-grupo
    conn.close()  # Cierra la conexión

def accept_connections(server_socket, queue_in, queue_out):
    while True:
        conn, addr = server_socket.accept()  # Acepta nueva conexión
        clients.append(conn)  # Agrega usuario a la lista global
        thread = threading.Thread(target=handle_client, args=(conn, addr, queue_in, queue_out))  # Crea hilo para el usuario
        thread.start()  # Inicia el hilo
        print(f"[USUARIOS CONECTADOS] {len(clients)}")  # Muestra cantidad de usuarios conectados
