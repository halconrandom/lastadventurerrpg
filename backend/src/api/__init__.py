"""
Modulo API para el backend de Last Adventurer.
"""

from .exploracion import exploracion_bp, registrar_blueprint as registrar_exploracion
from .mapa import mapa_bp, registrar_blueprint as registrar_mapa
from .inventario import inventario_bp, registrar_blueprint as registrar_inventario
from .crafteo import crafteo_bp, registrar_blueprint as registrar_crafteo

__all__ = [
    "exploracion_bp",
    "mapa_bp",
    "inventario_bp",
    "crafteo_bp",
    "registrar_exploracion",
    "registrar_mapa",
    "registrar_inventario",
    "registrar_crafteo",
]
