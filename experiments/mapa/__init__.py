"""
Sistema de Mapa Global - Last Adventurer

Este módulo implementa el sistema de mapa mundial con:
- Tiles globales (1 km² cada uno)
- Chunks para gestión eficiente
- Sub-tiles para ubicaciones
- Rutas entre ubicaciones
- Generación procedural
- Sistema de cartografía

Integración con sistema de zonas existente.
"""

from tile import Tile, SubTile, EstadoVisibilidad, TipoTerreno, calcular_costo_movimiento
from chunk import Chunk, GestorChunks
from mapa import MapaMundo
from ubicacion import Ubicacion, UbicacionGenerator, TipoUbicacion
from ruta import Ruta, RutaGenerator, TipoRuta
from cartografia import (
    HabilidadCartografia, 
    MapaItem, 
    SistemaCartografia,
    CalidadMapa, 
    TipoMapa
)

__all__ = [
    # Tiles
    "Tile",
    "SubTile", 
    "EstadoVisibilidad",
    "TipoTerreno",
    "calcular_costo_movimiento",
    # Chunks
    "Chunk",
    "GestorChunks",
    # Mapa
    "MapaMundo",
    # Ubicaciones
    "Ubicacion",
    "UbicacionGenerator",
    "TipoUbicacion",
    # Rutas
    "Ruta",
    "RutaGenerator",
    "TipoRuta",
    # Cartografía
    "HabilidadCartografia",
    "MapaItem",
    "SistemaCartografia",
    "CalidadMapa",
    "TipoMapa",
]