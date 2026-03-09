"""
Sistema de Chunks para gestión eficiente del mapa infinito.

Un chunk es un grupo de 3x3 tiles (9 km²).
Solo se cargan los chunks cercanos al jugador (30 chunks de radio).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
import math

from tile import Tile, EstadoVisibilidad


@dataclass
class Chunk:
    """
    Un chunk contiene 9 tiles (3x3).
    
    Cada tile = 1 km²
    Cada chunk = 9 km²
    
    Coordenadas de chunk:
    - Chunk (0,0) contiene tiles (0,0) a (2,2)
    - Chunk (1,0) contiene tiles (3,0) a (5,2)
    """
    x: int                              # Coordenada X del chunk
    y: int                              # Coordenada Y del chunk
    tiles: List[List[Tile]] = field(default_factory=list)
    generado: bool = False
    
    def __post_init__(self):
        """Inicializa la grilla de tiles si está vacía."""
        if not self.tiles:
            self.tiles = [[None for _ in range(3)] for _ in range(3)]
    
    def get_tile(self, local_x: int, local_y: int) -> Optional[Tile]:
        """Obtiene un tile dentro del chunk."""
        if 0 <= local_x < 3 and 0 <= local_y < 3:
            return self.tiles[local_y][local_x]
        return None
    
    def set_tile(self, local_x: int, local_y: int, tile: Tile) -> None:
        """Establece un tile dentro del chunk."""
        if 0 <= local_x < 3 and 0 <= local_y < 3:
            self.tiles[local_y][local_x] = tile
    
    def get_tiles_explorados(self) -> List[Tile]:
        """Retorna todos los tiles explorados del chunk."""
        explorados = []
        for fila in self.tiles:
            for tile in fila:
                if tile and tile.visibilidad == EstadoVisibilidad.EXPLORADO:
                    explorados.append(tile)
        return explorados
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "tiles": [[tile.to_dict() if tile else None for tile in fila] for fila in self.tiles],
            "generado": self.generado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Chunk':
        chunk = cls(x=data["x"], y=data["y"])
        chunk.tiles = [
            [Tile.from_dict(tile) if tile else None for tile in fila]
            for fila in data["tiles"]
        ]
        chunk.generado = data.get("generado", False)
        return chunk


class GestorChunks:
    """
    Gestiona la carga y descarga de chunks.
    
    Mantiene solo los chunks cercanos al jugador en memoria.
    """
    
    RADIO_CARGA = 30  # Chunks cargados alrededor del jugador
    
    def __init__(self):
        self.chunks: Dict[Tuple[int, int], Chunk] = {}
        self.posicion_jugador: Tuple[int, int] = (0, 0)
    
    @staticmethod
    def tile_a_chunk(x: int, y: int) -> Tuple[int, int]:
        """Convierte coordenadas de tile a coordenadas de chunk.
        
        Cada chunk contiene 3x3 tiles.
        Chunk (0,0) contiene tiles (0,1,2) en cada dimensión.
        Chunk (-1,0) contiene tiles (-3,-2,-1) en X y (0,1,2) en Y.
        """
        # Python's floor division maneja correctamente los negativos
        # -3 // 3 = -1, -2 // 3 = -1, -1 // 3 = -1
        # 0 // 3 = 0, 1 // 3 = 0, 2 // 3 = 0, 3 // 3 = 1
        chunk_x = x // 3
        chunk_y = y // 3
        return (chunk_x, chunk_y)
    
    @staticmethod
    def chunk_a_tile_base(chunk_x: int, chunk_y: int) -> Tuple[int, int]:
        """Retorna las coordenadas del tile base (esquina superior izquierda) de un chunk."""
        return (chunk_x * 3, chunk_y * 3)
    
    @staticmethod
    def tile_a_local(x: int, y: int) -> Tuple[int, int]:
        """Convierte coordenadas globales de tile a coordenadas locales dentro del chunk."""
        local_x = x % 3 if x >= 0 else (x % 3 + 3) % 3
        local_y = y % 3 if y >= 0 else (y % 3 + 3) % 3
        return (local_x, local_y)
    
    def get_chunk(self, chunk_x: int, chunk_y: int) -> Optional[Chunk]:
        """Obtiene un chunk por sus coordenadas."""
        return self.chunks.get((chunk_x, chunk_y))
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Obtiene un tile por sus coordenadas globales."""
        chunk_x, chunk_y = self.tile_a_chunk(x, y)
        chunk = self.get_chunk(chunk_x, chunk_y)
        
        if chunk:
            local_x, local_y = self.tile_a_local(x, y)
            return chunk.get_tile(local_x, local_y)
        
        return None
    
    def set_tile(self, tile: Tile) -> None:
        """Establece un tile en su chunk correspondiente."""
        chunk_x, chunk_y = self.tile_a_chunk(tile.x, tile.y)
        chunk = self.get_chunk(chunk_x, chunk_y)
        
        if not chunk:
            chunk = Chunk(x=chunk_x, y=chunk_y)
            self.chunks[(chunk_x, chunk_y)] = chunk
        
        local_x, local_y = self.tile_a_local(tile.x, tile.y)
        chunk.set_tile(local_x, local_y, tile)
    
    def actualizar_posicion_jugador(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Actualiza la posición del jugador y retorna los chunks que deben cargarse.
        
        Returns:
            Lista de coordenadas de chunks a cargar
        """
        self.posicion_jugador = (x, y)
        
        chunk_x, chunk_y = self.tile_a_chunk(x, y)
        
        # Chunks necesarios
        chunks_necesarios = set()
        for dx in range(-self.RADIO_CARGA, self.RADIO_CARGA + 1):
            for dy in range(-self.RADIO_CARGA, self.RADIO_CARGA + 1):
                # Distancia Manhattan (más eficiente)
                if abs(dx) + abs(dy) <= self.RADIO_CARGA:
                    chunks_necesarios.add((chunk_x + dx, chunk_y + dy))
        
        # Chunks a cargar
        chunks_a_cargar = []
        for cx, cy in chunks_necesarios:
            if (cx, cy) not in self.chunks:
                chunks_a_cargar.append((cx, cy))
        
        # Chunks a descargar
        chunks_a_descargar = []
        for cx, cy in list(self.chunks.keys()):
            if (cx, cy) not in chunks_necesarios:
                chunks_a_descargar.append((cx, cy))
        
        # Descargar chunks lejanos
        for cx, cy in chunks_a_descargar:
            del self.chunks[(cx, cy)]
        
        return chunks_a_cargar
    
    def get_chunks_a_cargar(self) -> List[Tuple[int, int]]:
        """Retorna los chunks que necesitan ser cargados."""
        return self.actualizar_posicion_jugador(*self.posicion_jugador)
    
    def agregar_chunk(self, chunk: Chunk) -> None:
        """Agrega un chunk al gestor."""
        self.chunks[(chunk.x, chunk.y)] = chunk
    
    def get_tiles_visibles(self, radio: int = 3) -> List[Tile]:
        """
        Retorna los tiles visibles desde la posición del jugador.
        
        Args:
            radio: Radio de visión en tiles (default 3)
        
        Returns:
            Lista de tiles visibles
        """
        px, py = self.posicion_jugador
        tiles_visibles = []
        
        for dx in range(-radio, radio + 1):
            for dy in range(-radio, radio + 1):
                # Distancia Manhattan
                if abs(dx) + abs(dy) <= radio:
                    tile = self.get_tile(px + dx, py + dy)
                    if tile:
                        tiles_visibles.append(tile)
        
        return tiles_visibles
    
    def get_tiles_explorados(self) -> List[Tile]:
        """Retorna todos los tiles explorados en los chunks cargados."""
        explorados = []
        for chunk in self.chunks.values():
            explorados.extend(chunk.get_tiles_explorados())
        return explorados
    
    def contar_tiles_explorados(self) -> int:
        """Cuenta el total de tiles explorados."""
        return len(self.get_tiles_explorados())
    
    def to_dict(self) -> dict:
        """Serializa el gestor de chunks."""
        return {
            "chunks": {f"{cx},{cy}": chunk.to_dict() for (cx, cy), chunk in self.chunks.items()},
            "posicion_jugador": list(self.posicion_jugador)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GestorChunks':
        """Deserializa el gestor de chunks."""
        gestor = cls()
        gestor.posicion_jugador = tuple(data.get("posicion_jugador", [0, 0]))
        
        for key, chunk_data in data.get("chunks", {}).items():
            chunk = Chunk.from_dict(chunk_data)
            cx, cy = map(int, key.split(","))
            gestor.chunks[(cx, cy)] = chunk
        
        return gestor
    
    def __repr__(self) -> str:
        return f"GestorChunks(chunks={len(self.chunks)}, posicion={self.posicion_jugador})"