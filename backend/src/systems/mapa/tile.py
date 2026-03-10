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
    Sub-tile para exploración local dentro de un tile mundial.
    
    Cada sub-tile representa 10m x 10m (100 m²).
    1 Tile mundial = 10x10 = 100 SubTiles.
    
    Tiempo de viaje: 1 minuto entre sub-tiles adyacentes.
    
    El descubrimiento de sub-tiles es INDEPENDIENTE del mapa mundial.
    """
    x: int                          # Coordenada X dentro del tile (0-9)
    y: int                          # Coordenada Y dentro del tile (0-9)
    tipo: str = "vacio"             # calle, edificio, plaza, muro, etc.
    contenido: Dict[str, Any] = field(default_factory=dict)
    transitivo: bool = True         # Si se puede caminar sobre él
    descubierto: bool = False       # Estado de descubrimiento LOCAL
    veces_explorado: int = 0        # Cuántas veces se ha explorado
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "transitivo": self.transitivo,
            "descubierto": self.descubierto,
            "veces_explorado": self.veces_explorado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SubTile':
        return cls(
            x=data["x"],
            y=data["y"],
            tipo=data.get("tipo", "vacio"),
            contenido=data.get("contenido", {}),
            transitivo=data.get("transitivo", True),
            descubierto=data.get("descubierto", False),
            veces_explorado=data.get("veces_explorado", 0)
        )
    
    def coordenada_global(self, tile_x: int, tile_y: int) -> tuple:
        """Retorna la coordenada global del sub-tile."""
        return (tile_x * 10 + self.x, tile_y * 10 + self.y)
    
    def explorar(self) -> None:
        """Marca el sub-tile como descubierto y aumenta el contador."""
        self.descubierto = True
        self.veces_explorado += 1


@dataclass
class Tile:
    """
    Tile del mapa mundial.
    
    Cada tile representa 1 km².
    Tiempo de viaje: 1 hora entre tiles adyacentes.
    
    IMPORTANTE: El descubrimiento de tiles es INDEPENDIENTE de los sub-tiles.
    - Descubrir un tile mundial NO descubre sus sub-tiles automáticamente.
    - Moverse en sub-tiles NO descubre tiles mundiales adyacentes.
    
    Contiene:
    - 10x10 sub-tiles para exploración local (cada uno 10m x 10m)
    - Posible ubicación (pueblo, ciudad, mazmorra, POI)
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
    
    # POI Dinámico (✨)
    tiene_poi: bool = False
    poi_completado: bool = False
    poi_tipo: Optional[str] = None              # combate, npc, tesoro, descubrimiento, mistico, comercio
    poi_data: Dict[str, Any] = field(default_factory=dict)
    poi_fecha_regeneracion: Optional[int] = None # Tick en el que se regenera
    
    # Sub-tiles SIEMPRE existen (10x10 = 100 subtiles de 10m cada uno)
    # Se generan lazy cuando el jugador entra al tile por primera vez
    sub_tiles: List[List[SubTile]] = field(default_factory=list)
    sub_tiles_generados: bool = False           # Flag para saber si ya se generaron
    
    # Conectividad
    rutas: List[str] = field(default_factory=list)  # IDs de rutas que pasan por aquí
    
    # Costo de movimiento
    costo_movimiento: float = 1.0               # Multiplicador (1.0 = normal)
    
    def tiene_ubicacion(self) -> bool:
        """Verifica si el tile tiene una ubicación."""
        return self.ubicacion_id is not None
    
    def generar_sub_tiles(self) -> None:
        """
        Genera la grilla de 10x10 sub-tiles para exploración local.
        
        Cada sub-tile representa 10m x 10m.
        Se genera lazy cuando el jugador entra al tile.
        """
        if self.sub_tiles_generados:
            return
        
        self.sub_tiles = []
        for y in range(10):
            fila = []
            for x in range(10):
                sub_tile = SubTile(x=x, y=y, tipo=self._determinar_tipo_subtile(x, y))
                fila.append(sub_tile)
            self.sub_tiles.append(fila)
        
        self.sub_tiles_generados = True
    
    def _determinar_tipo_subtile(self, x: int, y: int) -> str:
        """Determina el tipo de sub-tile basado en el bioma y posición."""
        # Tipos base por bioma
        tipos_por_bioma = {
            "bosque_ancestral": ["bosque_denso", "claro", "arbol_grande", "arbustos"],
            "paramo_marchito": ["tierra_yerma", "roca", "hierba_seca", "ruinas"],
            "pantano_sombrio": ["cienaga", "tierra_firme", "niebla", "agua_estancada"],
            "montanas_heladas": ["roca", "nieve", "cueva", "pico"],
            "desierto_ceniza": ["arena", "duna", "oasis", "ruinas"],
            "pradera": ["hierba", "flores", "arbol", "rio"],
            "costa": ["playa", "acantilado", "roca", "agua"],
        }
        
        import random
        tipos = tipos_por_bioma.get(self.bioma, ["terreno", "terreno", "terreno", "especial"])
        return random.choice(tipos[:3])  # 75% terreno normal, 25% especial
    
    def get_sub_tile(self, x: int, y: int) -> Optional[SubTile]:
        """Obtiene un sub-tile específico."""
        if not self.sub_tiles_generados:
            self.generar_sub_tiles()
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
            "tiene_poi": self.tiene_poi,
            "poi_completado": self.poi_completado,
            "poi_tipo": self.poi_tipo,
            "poi_data": self.poi_data,
            "poi_fecha_regeneracion": self.poi_fecha_regeneracion,
            "sub_tiles": [[st.to_dict() for st in fila] for fila in self.sub_tiles] if self.sub_tiles else [],
            "sub_tiles_generados": self.sub_tiles_generados,
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
            tiene_poi=data.get("tiene_poi", False),
            poi_completado=data.get("poi_completado", False),
            poi_tipo=data.get("poi_tipo"),
            poi_data=data.get("poi_data", {}),
            poi_fecha_regeneracion=data.get("poi_fecha_regeneracion"),
            rutas=data.get("rutas", []),
            costo_movimiento=data.get("costo_movimiento", 1.0),
            sub_tiles_generados=data.get("sub_tiles_generados", False)
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