# Decisiones de diseño y justificación

- **Modelo cliente-servidor:** Permite centralizar la gestión de usuarios, grupos y mensajes, facilitando la concurrencia y el control de acceso.
- **Sockets TCP:** Proveen comunicación eficiente y en tiempo real entre clientes y servidor.
- **Concurrencia/Asincronismo:** El servidor maneja múltiples clientes usando threads o async para garantizar escalabilidad y fluidez.
- **Grupos como entidades lógicas:** Facilita la organización de las conversaciones y la gestión de membresías.
- **(Opcional) Persistencia:** Puede añadirse almacenamiento de mensajes y usuarios para mejorar la experiencia y confiabilidad.

Estas decisiones buscan cumplir con los requisitos de la consigna y asegurar un sistema robusto y extensible.
