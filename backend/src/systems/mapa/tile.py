"""
Sistema de Tiles y Sub-Tiles para el mapa global.

Cada Tile representa 1 km² del mapa mundial.
Cada SubTile representa 100m x 100m dentro de una ubicación.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TipoTerreno(Enum):
    """Tipos de terreno posibles en un tile."""
    BOSQUE = "bosque"
    DESIERTO = "desierto"
    TUNDRA = "tundra"
    JUNGLA = "jungla"
    PANTANO = "pantano"
    MONTANA = "montana"
    COSTA = "costa"
    PRADERA = "pradera"
    AGUA = "agua"
    NIEVE = "nieve"


class EstadoVisibilidad(Enum):
    """Estados de visibilidad de un tile."""
    NO_DESCUBIERTO = "no_descubierto"
    DESCUBIERTO = "descubierto"
    EXPLORADO = "explorado"
    ACTUAL = "actual"


@dataclass
class SubTile:
    """
    Sub-tile para ubicaciones (ciudades, pueblos, mazmorras).
    
    Cada sub-tile representa 100m x 100m (10,000 m²).
    Tiempo de viaje: 10 minutos entre sub-tiles adyacentes.
    """
    x: int                          # Coordenada X dentro del tile (0-9)
    y: int                          # Coordenada Y dentro del tile (0-9)
    tipo: str = "vacio"             # calle, edificio, plaza, muro, etc.
    contenido: Dict[str, Any] = field(default_factory=dict)
    transitivo: bool = True         # Si se puede caminar sobre él
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "transitivo": self.transitivo
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SubTile':
        return cls(**data)
    
    def coordenada_global(self, tile_x: int, tile_y: int) -> tuple:
        """Retorna la coordenada global del sub-tile."""
        return (tile_x * 10 + self.x, tile_y * 10 + self.y)


@dataclass
class Tile:
    """
    Tile del mapa mundial.
    
    Cada tile representa 1 km².
    Tiempo de viaje: 1 hora entre tiles adyacentes.
    
    Puede contener:
    - Una ubicación (pueblo, ciudad, mazmorra, POI)
    - Recursos naturales
    - Enemigos potenciales
    - Eventos
    """
    x: int                                      # Coordenada X global
    y: int                                      # Coordenada Y global
    bioma: str = "desconocido"                  # Tipo de bioma
    terreno: str = "normal"                     # Tipo de terreno específico
    visibilidad: EstadoVisibilidad = EstadoVisibilidad.NO_DESCUBIERTO
    
    # Contenido
    ubicacion_id: Optional[str] = None          # ID de ubicación si hay
    recursos: List[str] = field(default_factory=list)
    enemigos_potenciales: List[str] = field(default_factory=list)
    eventos: List[str] = field(default_factory=list)
    
    # Sub-tiles (solo si tiene ubicación)
    sub_tiles: List[List[SubTile]] = field(default_factory=list)
    
    # Conectividad
    rutas: List[str] = field(default_factory=list)  # IDs de rutas que pasan por aquí
    
    # Costo de movimiento
    costo_movimiento: float = 1.0               # Multiplicador (1.0 = normal)
    
    def tiene_ubicacion(self) -> bool:
        """Verifica si el tile tiene una ubicación."""
        return self.ubicacion_id is not None
    
    def generar_sub_tiles(self, tipo_ubicacion: str) -> None:
        """
        Genera la grilla de sub-tiles para una ubicación.
        
        Args:
            tipo_ubicacion: Tipo de ubicación (pueblo, ciudad, capital, etc.)
        """
        # Tamaño según tipo de ubicación
        tamanos = {
            "pueblo": (5, 5),
            "ciudad": (8, 8),
            "capital": (10, 10),
            "mazmorra": (10, 10),
            "poi": (3, 3)
        }
        
        ancho, alto = tamanos.get(tipo_ubicacion, (5, 5))
        
        self.sub_tiles = []
        for y in range(alto):
            fila = []
            for x in range(ancho):
                sub_tile = SubTile(x=x, y=y, tipo="vacio")
                fila.append(sub_tile)
            self.sub_tiles.append(fila)
    
    def get_sub_tile(self, x: int, y: int) -> Optional[SubTile]:
        """Obtiene un sub-tile específico."""
        if 0 <= y < len(self.sub_tiles) and 0 <= x < len(self.sub_tiles[0]):
            return self.sub_tiles[y][x]
        return None
    
    def explorar(self) -> None:
        """Marca el tile como explorado."""
        self.visibilidad = EstadoVisibilidad.EXPLORADO
    
    def descubrir(self) -> None:
        """Marca el tile como descubierto."""
        if self.visibilidad == EstadoVisibilidad.NO_DESCUBIERTO:
            self.visibilidad = EstadoVisibilidad.DESCUBIERTO
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "bioma": self.bioma,
            "terreno": self.terreno,
            "visibilidad": self.visibilidad.value,
            "ubicacion_id": self.ubicacion_id,
            "recursos": self.recursos,
            "enemigos_potenciales": self.enemigos_potenciales,
            "eventos": self.eventos,
            "sub_tiles": [[st.to_dict() for st in fila] for fila in self.sub_tiles] if self.sub_tiles else [],
            "rutas": self.rutas,
            "costo_movimiento": self.costo_movimiento
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tile':
        tile = cls(
            x=data["x"],
            y=data["y"],
            bioma=data.get("bioma", "desconocido"),
            terreno=data.get("terreno", "normal"),
            visibilidad=EstadoVisibilidad(data.get("visibilidad", "no_descubierto")),
            ubicacion_id=data.get("ubicacion_id"),
            recursos=data.get("recursos", []),
            enemigos_potenciales=data.get("enemigos_potenciales", []),
            eventos=data.get("eventos", []),
            rutas=data.get("rutas", []),
            costo_movimiento=data.get("costo_movimiento", 1.0)
        )
        
        # Reconstruir sub-tiles
        if data.get("sub_tiles"):
            tile.sub_tiles = [
                [SubTile.from_dict(st) for st in fila]
                for fila in data["sub_tiles"]
            ]
        
        return tile
    
    def __repr__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.bioma}, {self.visibilidad.value})"


# Multiplicadores de costo de movimiento por terreno
COSTOS_TERRENO = {
    "carretera": 0.8,      # Más rápido
    "pradera": 1.0,        # Normal
    "bosque": 1.5,         # Más lento
    "pantano": 2.0,        # Mucho más lento
    "montana": 2.5,        # Muy lento
    "desierto": 1.8,       # Lento
    "tundra": 2.0,         # Lento
    "jungla": 1.8,         # Lento
    "costa": 1.2,          # Ligeramente lento
    "agua": 3.0,           # Muy lento (necesita barco)
    "nieve": 2.2,          # Lento
}


def calcular_costo_movimiento(bioma: str, terreno: str) -> float:
    """
    Calcula el costo de movimiento para un tile.
    
    Returns:
        Multiplicador de tiempo (1.0 = 1 hora base)
    """
    # Primero verificar terreno específico
    if terreno in COSTOS_TERRENO:
        return COSTOS_TERRENO[terreno]
    
    # Luego bioma
    costo_bioma = {
        "bosque_ancestral": 1.5,
        "paramo_marchito": 1.2,
        "pantano_sombrio": 2.0,
        "montanas_heladas": 2.5,
        "desierto_ceniza": 1.8,
        "ruinas_subterraneas": 1.3,
        "pradera": 1.0,
        "costa": 1.2,
    }
    
    return costo_bioma.get(bioma, 1.0)