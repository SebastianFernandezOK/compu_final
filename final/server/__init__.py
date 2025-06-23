# server/__init__.py
# Este archivo permite que la carpeta server sea tratada como un paquete de Python.
# Expone las funciones principales del servidor como API del paquete.

from .core import broadcast, handle_client, accept_connections  # Funciones de lógica de chat
from .moderador import moderador  # Proceso moderador
from .main import main  # Punto de entrada principal
