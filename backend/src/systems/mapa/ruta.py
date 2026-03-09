"""
Sistema de Rutas para conectar ubicaciones.

Las rutas definen caminos entre ubicaciones y calculan
el tiempo de viaje basado en el terreno atravesado.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import math


class TipoRuta(Enum):
    """Tipos de rutas."""
    CAMINO = "camino"           # Ruta básica
    SENDER0 = "sendero"         # Ruta estrecha
    CARRETERA = "carretera"     # Ruta principal
    RIO = "rio"                 # Ruta fluvial
    MARITIMA = "maritima"       # Ruta marítima
    SECRETA = "secreta"         # Ruta oculta


# Multiplicadores de velocidad por tipo de ruta
MULTIPLICADORES_RUTA = {
    TipoRuta.CARRETERA: 0.8,    # Más rápido
    TipoRuta.CAMINO: 1.0,       # Normal
    TipoRuta.SENDER0: 1.3,      # Más lento
    TipoRuta.RIO: 1.5,          # Lento
    TipoRuta.MARITIMA: 2.0,     # Muy lento
    TipoRuta.SECRETA: 1.5,      # Lento pero con ventajas
}


@dataclass
class Ruta:
    """
    Una ruta conecta dos ubicaciones.
    
    Define el camino, tiempo de viaje y dificultad.
    """
    id: str                              # Identificador único
    origen: str                          # ID de ubicación origen
    destino: str                         # ID de ubicación destino
    tipo: TipoRuta = TipoRuta.CAMINO     # Tipo de ruta
    
    # Propiedades
    distancia: float = 0.0              # Distancia en km
    tiempo_base: int = 0                # Tiempo base en horas
    dificultad: int = 1                 # 1-10 (afecta eventos negativos)
    
    # Camino
    tiles: List[Tuple[int, int]] = field(default_factory=list)  # Tiles por los que pasa
    
    # Eventos
    eventos_posibles: List[str] = field(default_factory=list)
    
    # Estado
    descubierta: bool = False           # Si el jugador la ha descubierto
    
    def calcular_tiempo(self, modificador_terreno: float = 1.0) -> int:
        """
        Calcula el tiempo de viaje real.
        
        Args:
            modificador_terreno: Multiplicador por terreno (promedio)
        
        Returns:
            Tiempo en horas
        """
        base = self.tiempo_base * MULTIPLICADORES_RUTA.get(self.tipo, 1.0)
        return int(base * modificador_terreno)
    
    def calcular_distancia(self) -> float:
        """
        Calcula la distancia real basada en los tiles.
        
        Returns:
            Distancia en km
        """
        if not self.tiles:
            return self.distancia
        
        distancia = 0.0
        for i in range(len(self.tiles) - 1):
            x1, y1 = self.tiles[i]
            x2, y2 = self.tiles[i + 1]
            # Distancia Manhattan (cada tile = 1 km)
            distancia += abs(x2 - x1) + abs(y2 - y1)
        
        return distancia
    
    def get_descripcion(self) -> str:
        """Genera una descripción de la ruta."""
        tipo_nombres = {
            TipoRuta.CARRETERA: "carretera",
            TipoRuta.CAMINO: "camino",
            TipoRuta.SENDER0: "sendero",
            TipoRuta.RIO: "ruta fluvial",
            TipoRuta.MARITIMA: "ruta marítima",
            TipoRuta.SECRETA: "ruta secreta",
        }
        
        dificultad_desc = {
            1: "fácil",
            2: "sencillo",
            3: "moderado",
            4: "algo difícil",
            5: "desafiante",
            6: "difícil",
            7: "peligroso",
            8: "muy peligroso",
            9: "extremo",
            10: "mortal",
        }
        
        return f"{tipo_nombres.get(self.tipo, 'camino')} {dificultad_desc.get(self.dificultad, 'normal')}"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "origen": self.origen,
            "destino": self.destino,
            "tipo": self.tipo.value,
            "distancia": self.distancia,
            "tiempo_base": self.tiempo_base,
            "dificultad": self.dificultad,
            "tiles": [list(t) for t in self.tiles],
            "eventos_posibles": self.eventos_posibles,
            "descubierta": self.descubierta
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ruta':
        return cls(
            id=data["id"],
            origen=data["origen"],
            destino=data["destino"],
            tipo=TipoRuta(data.get("tipo", "camino")),
            distancia=data.get("distancia", 0.0),
            tiempo_base=data.get("tiempo_base", 0),
            dificultad=data.get("dificultad", 1),
            tiles=[tuple(t) for t in data.get("tiles", [])],
            eventos_posibles=data.get("eventos_posibles", []),
            descubierta=data.get("descubierta", False)
        )
    
    def __repr__(self) -> str:
        return f"Ruta({self.origen} -> {self.destino}, {self.tipo.value})"


class RutaGenerator:
    """Generador de rutas procedurales."""
    
    def __init__(self, seed):
        """
        Inicializa el generador.
        
        Args:
            seed: Instancia de WorldSeed para determinismo
        """
        self.seed = seed
    
    def calcular_ruta(
        self,
        origen: Tuple[int, int],
        destino: Tuple[int, int],
        mapa_tiles: callable = None  # Función para obtener tile (x, y) -> Tile
    ) -> List[Tuple[int, int]]:
        """
        Calcula el camino entre dos puntos usando A*.
        
        Args:
            origen: Coordenadas (x, y) de origen
            destino: Coordenadas (x, y) de destino
            mapa_tiles: Función que retorna un tile dado (x, y)
        
        Returns:
            Lista de coordenadas del camino
        """
        # Implementación simplificada de A*
        # Por ahora, usamos línea recta con variaciones
        
        x1, y1 = origen
        x2, y2 = destino
        
        camino = []
        x, y = x1, y1
        
        # Distancia Manhattan
        dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
        
        # Avanzar hacia el destino
        while x != x2 or y != y2:
            camino.append((x, y))
            
            # Decidir dirección (priorizar la más lejana)
            if abs(x2 - x) > abs(y2 - y):
                x += dx
            elif y != y2:
                y += dy
            else:
                x += dx
        
        camino.append((x2, y2))
        
        return camino
    
    def generar_ruta(
        self,
        id: str,
        origen_id: str,
        destino_id: str,
        origen_coords: Tuple[int, int],
        destino_coords: Tuple[int, int],
        mapa_tiles: callable = None
    ) -> Ruta:
        """
        Genera una ruta completa entre dos ubicaciones.
        
        Args:
            id: Identificador único
            origen_id: ID de ubicación origen
            destino_id: ID de ubicación destino
            origen_coords: Coordenadas (x, y) del origen
            destino_coords: Coordenadas (x, y) del destino
            mapa_tiles: Función para obtener tiles
        
        Returns:
            Instancia de Ruta
        """
        contexto = f"ruta_{id}"
        rng = self.seed.get_rng(contexto)
        
        # Calcular camino
        tiles = self.calcular_ruta(origen_coords, destino_coords, mapa_tiles)
        
        # Calcular distancia
        distancia = len(tiles) - 1  # Cada tile = 1 km
        
        # Tiempo base (1 hora por km)
        tiempo_base = distancia
        
        # Tipo de ruta aleatorio
        tipo = rng.choice(list(TipoRuta))
        
        # Dificultad basada en distancia y tipo
        dificultad = min(10, max(1, distancia // 10 + rng.randint(0, 2)))
        
        # Eventos posibles (se llenarán después)
        eventos_posibles = []
        
        return Ruta(
            id=id,
            origen=origen_id,
            destino=destino_id,
            tipo=tipo,
            distancia=distancia,
            tiempo_base=tiempo_base,
            dificultad=dificultad,
            tiles=tiles,
            eventos_posibles=eventos_posibles
        )
    
    def generar_rutas_ubicaciones(
        self,
        ubicaciones: List,  # Lista de Ubicacion
        mapa_tiles: callable = None
    ) -> List[Ruta]:
        """
        Genera rutas entre ubicaciones cercanas.
        
        Args:
            ubicaciones: Lista de ubicaciones
            mapa_tiles: Función para obtener tiles
        
        Returns:
            Lista de rutas generadas
        """
        rutas = []
        rng = self.seed.get_rng("rutas")
        
        # Crear índice de ubicaciones
        ubicaciones_dict = {u.id: u for u in ubicaciones}
        
        # Conectar cada ubicación con las más cercanas
        for ubicacion in ubicaciones:
            # Encontrar ubicaciones cercanas (dentro de 50 tiles)
            cercanas = []
            for otra in ubicaciones:
                if otra.id == ubicacion.id:
                    continue
                
                distancia = abs(otra.x - ubicacion.x) + abs(otra.y - ubicacion.y)
                if distancia <= 50:
                    cercanas.append((otra, distancia))
            
            # Ordenar por distancia
            cercanas.sort(key=lambda x: x[1])
            
            # Crear rutas a las 3 más cercanas
            for i, (otra, distancia) in enumerate(cercanas[:3]):
                # Verificar si ya existe la ruta
                id_ruta = f"ruta_{ubicacion.id}_{otra.id}"
                id_ruta_inversa = f"ruta_{otra.id}_{ubicacion.id}"
                
                existe = any(r.id == id_ruta or r.id == id_ruta_inversa for r in rutas)
                
                if not existe:
                    ruta = self.generar_ruta(
                        id=id_ruta,
                        origen_id=ubicacion.id,
                        destino_id=otra.id,
                        origen_coords=(ubicacion.x, ubicacion.y),
                        destino_coords=(otra.x, otra.y),
                        mapa_tiles=mapa_tiles
                    )
                    rutas.append(ruta)
        
        return rutas