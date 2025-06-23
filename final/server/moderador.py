def moderador(queue_in, queue_out):
    """
    Proceso moderador: revisa mensajes y detecta palabras prohibidas.
    Args:
        queue_in (multiprocessing.Queue): Cola para recibir mensajes del servidor.
        queue_out (multiprocessing.Queue): Cola para enviar la respuesta al servidor.
    """
    palabras_prohibidas = ["prohibido", "ban", "bloquear"]  # Lista de palabras prohibidas
    while True:
        item = queue_in.get()  # Espera un mensaje del servidor (bloqueante)
        if item == "__salir__":
            break  # Si recibe la señal de salir, termina el proceso
        mensaje, conn = item[0], item[1]  # Extrae el mensaje y la conexión
        id_mensaje = item[2] if len(item) > 2 else None  # Extrae el id único del mensaje
        if any(palabra in mensaje.lower() for palabra in palabras_prohibidas):  # Si el mensaje contiene palabra prohibida
            print(f"[MODERADOR] Mensaje bloqueado: '{mensaje}'")  # Muestra en consola que fue bloqueado
            try:
                conn.sendall("Mensaje bloqueado por contener palabras prohibidas.".encode())  # Avisa al usuario
            except:
                pass  # Si falla el envío, lo ignora
            queue_out.put((False, id_mensaje))  # Informa al servidor que el mensaje está bloqueado
        else:
            queue_out.put((True, id_mensaje))  # Informa al servidor que el mensaje está permitido
