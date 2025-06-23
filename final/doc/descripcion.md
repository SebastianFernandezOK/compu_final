# Descripción del sistema

La aplicación es un sistema de chat cliente-servidor inspirado en Discord, donde los usuarios pueden crear y unirse a grupos (canales) para comunicarse en tiempo real. El servidor gestiona múltiples clientes de manera concurrente, permitiendo la interacción fluida entre usuarios y grupos. La comunicación se realiza mediante sockets TCP, y se emplean mecanismos de concurrencia y asincronismo para el manejo eficiente de múltiples conexiones y mensajes.

**Nota sobre concurrencia:** En este sistema, el servidor utiliza hilos (threads) para manejar a cada usuario de forma concurrente dentro de un mismo proceso. Todos los hilos comparten el mismo espacio de memoria, lo que permite que accedan y modifiquen variables y estructuras de datos globales. Esto facilita el intercambio de información entre usuarios, pero requiere mecanismos de sincronización para evitar conflictos cuando varios hilos acceden a los mismos datos al mismo tiempo.

> En otras palabras, como el proceso corresponde al archivo `server.py` en ejecución, todas las funciones y variables definidas en ese archivo pueden ser utilizadas y compartidas por los distintos hilos, lo que constituye la "información" compartida entre ellos.

## Características principales
- Usuarios pueden autenticarse, crear y unirse a grupos de chat.
- Envío y recepción de mensajes en tiempo real dentro de los grupos.
- El servidor maneja múltiples clientes concurrentemente.
- Uso de sockets y mecanismos de IPC para la comunicación y sincronización.
- Posibilidad de extender funcionalidades como persistencia de mensajes, administración de usuarios, etc.
