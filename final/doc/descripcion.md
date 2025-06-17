# Descripción del sistema

La aplicación es un sistema de chat cliente-servidor inspirado en Discord, donde los usuarios pueden crear y unirse a grupos (canales) para comunicarse en tiempo real. El servidor gestiona múltiples clientes de manera concurrente, permitiendo la interacción fluida entre usuarios y grupos. La comunicación se realiza mediante sockets TCP, y se emplean mecanismos de concurrencia y asincronismo para el manejo eficiente de múltiples conexiones y mensajes.

## Características principales
- Usuarios pueden autenticarse, crear y unirse a grupos de chat.
- Envío y recepción de mensajes en tiempo real dentro de los grupos.
- El servidor maneja múltiples clientes concurrentemente.
- Uso de sockets y mecanismos de IPC para la comunicación y sincronización.
- Posibilidad de extender funcionalidades como persistencia de mensajes, administración de usuarios, etc.
