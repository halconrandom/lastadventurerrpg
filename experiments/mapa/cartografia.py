"""
Sistema de Cartografía - Progresión del mapa.

Gestiona:
- Habilidad de cartografía
- Mapas como items
- Descubrimiento progresivo
- Bonificaciones por exploración
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CalidadMapa(Enum):
    """Calidad de un mapa."""
    BORROSO = "borroso"         # -50% precisión
    NORMAL = "normal"           # Precisión base
    DETALLADO = "detallado"    # +25% precisión
    PRECISO = "preciso"        # +50% precisión
    MAESTRO = "maestro"        # +100% precisión


class TipoMapa(Enum):
    """Tipos de mapas disponibles."""
    REGIONAL = "regional"       # Muestra una región
    LOCAL = "local"             # Muestra un área pequeña
    DUNGEON = "dungeon"         # Mapa de mazmorra
    TESORO = "tesoro"           # Mapa de tesoro
    ANTIGUO = "antiguo"         # Mapa antiguo (revela ubicaciones ocultas)


# Configuración de niveles de cartografía
NIVELES_CARTOGRAFIA = {
    1: {"nombre": "Novato", "radio_base": 5, "precision": 0.5},
    2: {"nombre": "Aprendiz", "radio_base": 7, "precision": 0.6},
    3: {"nombre": "Practicante", "radio_base": 10, "precision": 0.7},
    4: {"nombre": "Competente", "radio_base": 15, "precision": 0.8},
    5: {"nombre": "Experto", "radio_base": 20, "precision": 0.85},
    6: {"nombre": "Maestro", "radio_base": 30, "precision": 0.9},
    7: {"nombre": "Gran Maestro", "radio_base": 50, "precision": 0.95},
    8: {"nombre": "Legendario", "radio_base": 100, "precision": 1.0},
}


@dataclass
class MapaItem:
    """
    Un mapa como item del inventario.
    
    Los mapas revelan información sobre áreas del mundo.
    """
    id: str                              # Identificador único
    nombre: str                          # Nombre del mapa
    tipo: TipoMapa                       # Tipo de mapa
    calidad: CalidadMapa                 # Calidad del mapa
    
    # Área que cubre
    centro_x: int = 0                   # Centro X del área
    centro_y: int = 0                   # Centro Y del área
    radio: int = 10                      # Radio de cobertura en tiles
    
    # Contenido
    ubicaciones_reveladas: List[str] = field(default_factory=list)
    rutas_reveladas: List[str] = field(default_factory=list)
    notas: str = ""                      # Notas del mapa
    
    # Estado
    usado: bool = False                  # Si ya fue usado
    
    def get_precision(self) -> float:
        """Retorna la precisión del mapa."""
        precisiones = {
            CalidadMapa.BORROSO: 0.5,
            CalidadMapa.NORMAL: 1.0,
            CalidadMapa.DETALLADO: 1.25,
            CalidadMapa.PRECISO: 1.5,
            CalidadMapa.MAESTRO: 2.0,
        }
        return precisiones.get(self.calidad, 1.0)
    
    def get_area(self) -> Tuple[int, int, int, int]:
        """Retorna el área que cubre (x_min, y_min, x_max, y_max)."""
        return (
            self.centro_x - self.radio,
            self.centro_y - self.radio,
            self.centro_x + self.radio,
            self.centro_y + self.radio
        )
    
    def contiene_tile(self, x: int, y: int) -> bool:
        """Verifica si un tile está dentro del área del mapa."""
        x_min, y_min, x_max, y_max = self.get_area()
        return x_min <= x <= x_max and y_min <= y <= y_max
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "calidad": self.calidad.value,
            "centro_x": self.centro_x,
            "centro_y": self.centro_y,
            "radio": self.radio,
            "ubicaciones_reveladas": self.ubicaciones_reveladas,
            "rutas_reveladas": self.rutas_reveladas,
            "notas": self.notas,
            "usado": self.usado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MapaItem':
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=TipoMapa(data["tipo"]),
            calidad=CalidadMapa(data["calidad"]),
            centro_x=data.get("centro_x", 0),
            centro_y=data.get("centro_y", 0),
            radio=data.get("radio", 10),
            ubicaciones_reveladas=data.get("ubicaciones_reveladas", []),
            rutas_reveladas=data.get("rutas_reveladas", []),
            notas=data.get("notas", ""),
            usado=data.get("usado", False)
        )


@dataclass
class HabilidadCartografia:
    """
    Habilidad de cartografía del jugador.
    
    Permite:
    - Crear mapas
    - Mejorar precisión de mapas
    - Descubrir ubicaciones ocultas
    - Obtener bonificaciones por exploración
    """
    nivel: int = 1                        # Nivel de la habilidad (1-8)
    experiencia: int = 0                   # Experiencia acumulada
    
    # Estadísticas
    tiles_explorados: int = 0              # Total de tiles explorados
    ubicaciones_descubiertas: int = 0      # Ubicaciones descubiertas
    mapas_creados: int = 0                 # Mapas creados
    
    # Bonificaciones
    bonificaciones: Dict[str, float] = field(default_factory=dict)
    
    def get_config(self) -> dict:
        """Obtiene la configuración del nivel actual."""
        return NIVELES_CARTOGRAFIA.get(self.nivel, NIVELES_CARTOGRAFIA[1])
    
    def get_radio_vision(self) -> int:
        """Obtiene el radio de visión del mapa."""
        return self.get_config()["radio_base"]
    
    def get_precision(self) -> float:
        """Obtiene la precisión del mapa."""
        base = self.get_config()["precision"]
        return min(1.0, base + self.bonificaciones.get("precision", 0))
    
    def get_nombre_nivel(self) -> str:
        """Obtiene el nombre del nivel actual."""
        return self.get_config()["nombre"]
    
    def add_experiencia(self, cantidad: int) -> bool:
        """
        Añade experiencia y verifica subida de nivel.
        
        Args:
            cantidad: Cantidad de experiencia a añadir
        
        Returns:
            True si subió de nivel
        """
        self.experiencia += cantidad
        
        # Experiencia necesaria para siguiente nivel
        exp_necesaria = self.nivel * 100
        
        if self.experiencia >= exp_necesaria and self.nivel < 8:
            self.nivel += 1
            self.experiencia = 0
            return True
        
        return False
    
    def explorar_tile(self) -> int:
        """
        Registra la exploración de un tile.
        
        Returns:
            Experiencia ganada
        """
        self.tiles_explorados += 1
        
        # Experiencia base por tile
        exp = 1
        
        # Bonificación por tiles únicos (cada 10 tiles)
        if self.tiles_explorados % 10 == 0:
            exp += 5
        
        return exp
    
    def descubrir_ubicacion(self) -> int:
        """
        Registra el descubrimiento de una ubicación.
        
        Returns:
            Experiencia ganada
        """
        self.ubicaciones_descubiertas += 1
        
        # Experiencia por ubicación
        exp = 20
        
        # Bonificación por variedad
        if self.ubicaciones_descubiertas % 5 == 0:
            exp += 50
        
        return exp
    
    def crear_mapa(self) -> int:
        """
        Registra la creación de un mapa.
        
        Returns:
            Experiencia ganada
        """
        self.mapas_creados += 1
        
        # Experiencia por crear mapa
        return 10
    
    def to_dict(self) -> dict:
        return {
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "tiles_explorados": self.tiles_explorados,
            "ubicaciones_descubiertas": self.ubicaciones_descubiertas,
            "mapas_creados": self.mapas_creados,
            "bonificaciones": self.bonificaciones
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HabilidadCartografia':
        return cls(
            nivel=data.get("nivel", 1),
            experiencia=data.get("experiencia", 0),
            tiles_explorados=data.get("tiles_explorados", 0),
            ubicaciones_descubiertas=data.get("ubicaciones_descubiertas", 0),
            mapas_creados=data.get("mapas_creados", 0),
            bonificaciones=data.get("bonificaciones", {})
        )


class SistemaCartografia:
    """
    Sistema principal de cartografía.
    
    Gestiona la habilidad, mapas y descubrimientos.
    """
    
    def __init__(self, seed):
        """
        Inicializa el sistema.
        
        Args:
            seed: Instancia de WorldSeed para determinismo
        """
        self.seed = seed
        self.habilidad = HabilidadCartografia()
        self.mapas: Dict[str, MapaItem] = {}
    
    def crear_mapa(
        self,
        tipo: TipoMapa,
        calidad: CalidadMapa,
        centro_x: int,
        centro_y: int,
        radio: int = None
    ) -> MapaItem:
        """
        Crea un nuevo mapa.
        
        Args:
            tipo: Tipo de mapa
            calidad: Calidad del mapa
            centro_x: Centro X del área
            centro_y: Centro Y del área
            radio: Radio de cobertura (opcional)
        
        Returns:
            MapaItem creado
        """
        contexto = f"mapa_{tipo.value}_{centro_x}_{centro_y}"
        rng = self.seed.get_rng(contexto)
        
        # Radio base según tipo
        radios_base = {
            TipoMapa.REGIONAL: 20,
            TipoMapa.LOCAL: 10,
            TipoMapa.DUNGEON: 5,
            TipoMapa.TESORO: 3,
            TipoMapa.ANTIGUO: 15,
        }
        
        if radio is None:
            radio = radios_base.get(tipo, 10)
        
        # Generar ID único
        id = f"mapa_{len(self.mapas)}"
        
        # Generar nombre
        nombres = {
            TipoMapa.REGIONAL: ["Mapa Regional", "Carta de la Zona", "Plano Regional"],
            TipoMapa.LOCAL: ["Mapa Local", "Plano del Área", "Croquis"],
            TipoMapa.DUNGEON: ["Mapa de Mazmorra", "Plano de las Ruinas", "Esquema"],
            TipoMapa.TESORO: ["Mapa del Tesoro", "Carta del Tesoro", "Guía del Tesoro"],
            TipoMapa.ANTIGUO: ["Mapa Antiguo", "Pergamino Viejo", "Carta Ancestral"],
        }
        
        nombre = rng.choice(nombres.get(tipo, ["Mapa"]))
        
        mapa = MapaItem(
            id=id,
            nombre=nombre,
            tipo=tipo,
            calidad=calidad,
            centro_x=centro_x,
            centro_y=centro_y,
            radio=radio
        )
        
        self.mapas[id] = mapa
        self.habilidad.crear_mapa()
        
        return mapa
    
    def usar_mapa(self, mapa_id: str, mapa_mundo) -> Dict:
        """
        Usa un mapa para revelar información.
        
        Args:
            mapa_id: ID del mapa
            mapa_mundo: Instancia de MapaMundo
        
        Returns:
            Diccionario con información revelada
        """
        if mapa_id not in self.mapas:
            return {"error": "Mapa no encontrado"}
        
        mapa = self.mapas[mapa_id]
        
        if mapa.usado:
            return {"error": "Mapa ya usado"}
        
        # Marcar como usado
        mapa.usado = True
        
        # Revelar tiles
        tiles_revelados = []
        x_min, y_min, x_max, y_max = mapa.get_area()
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                tile = mapa_mundo.gestor_chunks.get_tile(x, y)
                if tile:
                    tile.descubrir()
                    tiles_revelados.append((x, y))
        
        # Revelar ubicaciones
        ubicaciones_reveladas = []
        for ubicacion in mapa_mundo.ubicaciones.values():
            if mapa.contiene_tile(ubicacion.x, ubicacion.y):
                ubicacion.descubierta = True
                mapa.ubicaciones_reveladas.append(ubicacion.id)
                ubicaciones_reveladas.append(ubicacion.to_dict())
        
        # Revelar rutas
        rutas_reveladas = []
        for ruta in mapa_mundo.rutas.values():
            origen = mapa_mundo.ubicaciones.get(ruta.origen)
            destino = mapa_mundo.ubicaciones.get(ruta.destino)
            
            if origen and destino:
                if mapa.contiene_tile(origen.x, origen.y) or mapa.contiene_tile(destino.x, destino.y):
                    ruta.descubierta = True
                    mapa.rutas_reveladas.append(ruta.id)
                    rutas_reveladas.append(ruta.to_dict())
        
        # Experiencia
        exp_ganada = len(tiles_revelados) + len(ubicaciones_reveladas) * 10
        self.habilidad.add_experiencia(exp_ganada)
        
        return {
            "mapa": mapa.to_dict(),
            "tiles_revelados": len(tiles_revelados),
            "ubicaciones_reveladas": ubicaciones_reveladas,
            "rutas_reveladas": rutas_reveladas,
            "experiencia_ganada": exp_ganada
        }
    
    def get_mapas_disponibles(self) -> List[MapaItem]:
        """Obtiene los mapas disponibles (no usados)."""
        return [m for m in self.mapas.values() if not m.usado]
    
    def get_estadisticas(self) -> Dict:
        """Obtiene estadísticas de cartografía."""
        return {
            "nivel": self.habilidad.nivel,
            "nombre_nivel": self.habilidad.get_nombre_nivel(),
            "experiencia": self.habilidad.experiencia,
            "tiles_explorados": self.habilidad.tiles_explorados,
            "ubicaciones_descubiertas": self.habilidad.ubicaciones_descubiertas,
            "mapas_creados": self.habilidad.mapas_creados,
            "precision": self.habilidad.get_precision(),
            "radio_vision": self.habilidad.get_radio_vision()
        }
    
    def to_dict(self) -> dict:
        """Serializa el sistema."""
        return {
            "habilidad": self.habilidad.to_dict(),
            "mapas": {id: m.to_dict() for id, m in self.mapas.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict, seed) -> 'SistemaCartografia':
        """Deserializa el sistema."""
        sistema = cls(seed)
        sistema.habilidad = HabilidadCartografia.from_dict(data.get("habilidad", {}))
        sistema.mapas = {
            id: MapaItem.from_dict(m) 
            for id, m in data.get("mapas", {}).items()
        }
        return sistema