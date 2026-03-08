"""
Estado de exploracion para persistencia.

Guarda:
- Semilla del mundo
- Zonas descubiertas
- Coordenadas actuales
- Historial de exploracion
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json


@dataclass
class ZonaDescubierta:
    """Representa una zona descubierta por el jugador."""
    x: int
    y: int
    nombre: str
    bioma_key: str
    veces_explorada: int = 0
    estado: str = "descubierta"
    tiles_descubiertos: int = 0
    pois_encontrados: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "nombre": self.nombre,
            "bioma_key": self.bioma_key,
            "veces_explorada": self.veces_explorada,
            "estado": self.estado,
            "tiles_descubiertos": self.tiles_descubiertos,
            "pois_encontrados": self.pois_encontrados
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ZonaDescubierta":
        return cls(
            x=data["x"],
            y=data["y"],
            nombre=data["nombre"],
            bioma_key=data["bioma_key"],
            veces_explorada=data.get("veces_explorada", 0),
            estado=data.get("estado", "descubierta"),
            tiles_descubiertos=data.get("tiles_descubiertos", 0),
            pois_encontrados=data.get("pois_encontrados", [])
        )


@dataclass
class ExploracionState:
    """
    Estado completo de exploracion de una partida.
    
    Atributos:
        - seed: Semilla del mundo (string)
        - x, y: Coordenadas actuales del jugador
        - zonas: Diccionario de zonas descubiertas (key: "x_y")
        - eventos_completados: Lista de IDs de eventos completados
        - estadisticas: Estadisticas de exploracion
    """
    seed: str
    x: int = 0
    y: int = 0
    zonas: Dict[str, ZonaDescubierta] = field(default_factory=dict)
    eventos_completados: List[str] = field(default_factory=list)
    estadisticas: Dict[str, int] = field(default_factory=lambda: {
        "total_exploraciones": 0,
        "zonas_descubiertas": 0,
        "eventos_encontrados": 0,
        "pois_descubiertos": 0,
        "encuentros_hostiles": 0
    })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "seed": self.seed,
            "x": self.x,
            "y": self.y,
            "zonas": {k: v.to_dict() for k, v in self.zonas.items()},
            "eventos_completados": self.eventos_completados,
            "estadisticas": self.estadisticas
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExploracionState":
        zonas = {}
        for key, zona_data in data.get("zonas", {}).items():
            zonas[key] = ZonaDescubierta.from_dict(zona_data)
        
        return cls(
            seed=data["seed"],
            x=data.get("x", 0),
            y=data.get("y", 0),
            zonas=zonas,
            eventos_completados=data.get("eventos_completados", []),
            estadisticas=data.get("estadisticas", {
                "total_exploraciones": 0,
                "zonas_descubiertas": 0,
                "eventos_encontrados": 0,
                "pois_descubiertos": 0,
                "encuentros_hostiles": 0
            })
        )
    
    def get_zona_key(self, x: int = None, y: int = None) -> str:
        """Genera la key de una zona."""
        return f"{x if x is not None else self.x}_{y if y is not None else self.y}"
    
    def zona_descubierta(self, x: int = None, y: int = None) -> bool:
        """Verifica si una zona ya fue descubierta."""
        key = self.get_zona_key(x, y)
        return key in self.zonas
    
    def descubrir_zona(self, x: int, y: int, nombre: str, bioma_key: str) -> ZonaDescubierta:
        """Registra una nueva zona descubierta."""
        key = self.get_zona_key(x, y)
        
        if key not in self.zonas:
            zona = ZonaDescubierta(
                x=x,
                y=y,
                nombre=nombre,
                bioma_key=bioma_key
            )
            self.zonas[key] = zona
            self.estadisticas["zonas_descubiertas"] += 1
        else:
            zona = self.zonas[key]
        
        return zona
    
    def explorar_zona(self, x: int, y: int, tiles_descubiertos: int = 1, 
                      poi_encontrado: str = None) -> ZonaDescubierta:
        """Actualiza el estado de una zona tras explorar."""
        key = self.get_zona_key(x, y)
        
        if key not in self.zonas:
            raise ValueError(f"Zona {key} no ha sido descubierta")
        
        zona = self.zonas[key]
        zona.veces_explorada += 1
        zona.tiles_descubiertos += tiles_descubiertos
        
        # Actualizar estado segun veces explorada
        if zona.veces_explorada >= 5:
            zona.estado = "agotada"
        elif zona.veces_explorada >= 3:
            zona.estado = "explorada"
        else:
            zona.estado = "explorando"
        
        if poi_encontrado and poi_encontrado not in zona.pois_encontrados:
            zona.pois_encontrados.append(poi_encontrado)
            self.estadisticas["pois_descubiertos"] += 1
        
        self.estadisticas["total_exploraciones"] += 1
        
        return zona
    
    def mover_jugador(self, nuevo_x: int, nuevo_y: int):
        """Mueve al jugador a nuevas coordenadas."""
        self.x = nuevo_x
        self.y = nuevo_y
    
    def registrar_evento(self, evento_id: str):
        """Registra un evento completado."""
        if evento_id not in self.eventos_completados:
            self.eventos_completados.append(evento_id)
            self.estadisticas["eventos_encontrados"] += 1
    
    def registrar_encuentro_hostil(self):
        """Registra un encuentro hostil."""
        self.estadisticas["encuentros_hostiles"] += 1
    
    def get_zonas_adyacentes(self) -> List[str]:
        """Retorna las keys de zonas adyacentes a la posicion actual."""
        adyacentes = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                key = self.get_zona_key(self.x + dx, self.y + dy)
                if key in self.zonas:
                    adyacentes.append(key)
        return adyacentes
    
    def get_resumen(self) -> Dict[str, Any]:
        """Retorna un resumen del estado de exploracion."""
        return {
            "posicion": {"x": self.x, "y": self.y},
            "zonas_descubiertas": len(self.zonas),
            "eventos_completados": len(self.eventos_completados),
            "estadisticas": self.estadisticas
        }


def crear_exploracion_inicial(seed: str) -> ExploracionState:
    """Crea un estado de exploracion inicial con la semilla dada."""
    state = ExploracionState(seed=seed)
    # La zona inicial (0, 0) se descubre al empezar
    state.descubrir_zona(0, 0, "Pueblo Inicio", "pueblo")
    return state