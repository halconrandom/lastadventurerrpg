"""
Modulo API para el backend de Last Adventurer.
"""

from .exploracion import exploracion_bp, registrar_blueprint as registrar_exploracion
from .mapa import mapa_bp, registrar_blueprint as registrar_mapa

__all__ = [
    'exploracion_bp', 
    'mapa_bp',
    'registrar_exploracion',
    'registrar_mapa'
]
