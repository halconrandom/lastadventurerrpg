"""
Sistema de Ubicaciones para el mapa global.

Las ubicaciones son puntos de interés en el mapa:
- Pueblos
- Ciudades
- Capitales
- Mazmorras
- Puntos de interés (POIs)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import random


class TipoUbicacion(Enum):
    """Tipos de ubicaciones."""

    PUEBLO = "pueblo"
    CIUDAD = "ciudad"
    CAPITAL = "capital"
    MAZMORRA = "mazmorra"
    POI = "poi"


# Configuración por tipo de ubicación
CONFIG_UBICACION = {
    TipoUbicacion.PUEBLO: {
        "tamanos_sub_tiles": (5, 8),  # 5x5 a 8x8 sub-tiles
        "npcs_min": 10,
        "npcs_max": 50,
        "servicios": ["tienda", "posada"],
        "segura": True,
    },
    TipoUbicacion.CIUDAD: {
        "tamanos_sub_tiles": (8, 10),  # 8x8 a 10x10 sub-tiles
        "npcs_min": 50,
        "npcs_max": 200,
        "servicios": ["tienda", "herrero", "posada", "templo", "banco"],
        "segura": True,
    },
    TipoUbicacion.CAPITAL: {
        "tamanos_sub_tiles": (10, 10),  # 10x10 sub-tiles (máximo)
        "npcs_min": 200,
        "npcs_max": 500,
        "servicios": [
            "tienda",
            "herrero",
            "posada",
            "templo",
            "banco",
            "gremio",
            "palacio",
        ],
        "segura": True,
    },
    TipoUbicacion.MAZMORRA: {
        "tamanos_sub_tiles": (10, 20),  # 10x10 a 20x20 sub-tiles
        "npcs_min": 0,
        "npcs_max": 5,
        "servicios": [],
        "segura": False,
    },
    TipoUbicacion.POI: {
        "tamanos_sub_tiles": (3, 5),  # 3x3 a 5x5 sub-tiles
        "npcs_min": 0,
        "npcs_max": 5,
        "servicios": [],
        "segura": False,
    },
}


@dataclass
class Ubicacion:
    """
    Una ubicación en el mapa mundial.

    Puede ser un pueblo, ciudad, capital, mazmorra o punto de interés.
    Cada ubicación tiene su propio mapa de sub-tiles.
    """

    id: str  # Identificador único
    nombre: str  # Nombre generado
    tipo: TipoUbicacion  # Tipo de ubicación
    x: int  # Coordenada X del tile
    y: int  # Coordenada Y del tile
    bioma: str  # Bioma donde está ubicada

    # Contenido
    npcs: List[str] = field(default_factory=list)  # IDs de NPCs
    servicios: List[str] = field(default_factory=list)  # Servicios disponibles
    eventos: List[str] = field(default_factory=list)  # Eventos disponibles

    # Conexiones
    rutas: List[str] = field(default_factory=list)  # IDs de rutas

    # Estado
    descubierta: bool = False  # Si el jugador la ha descubierto
    visitada: bool = False  # Si el jugador la ha visitado

    # Propiedades
    segura: bool = True  # Si es una zona segura
    tamanio: Tuple[int, int] = (5, 5)  # Tamaño en sub-tiles (ancho, alto)

    def __post_init__(self):
        """Configura la ubicación según su tipo."""
        config = CONFIG_UBICACION.get(self.tipo, {})

        if not self.servicios:
            self.servicios = config.get("servicios", []).copy()

        self.segura = config.get("segura", True)

        if self.tamanio == (5, 5):
            min_tam, max_tam = config.get("tamanos_sub_tiles", (5, 5))
            self.tamanio = (min_tam, min_tam)  # Se puede hacer aleatorio

    def get_tiempo_exploracion(self) -> int:
        """
        Retorna el tiempo base para explorar la ubicación.

        Returns:
            Tiempo en minutos
        """
        # Base: 10 minutos por sub-tile
        area = self.tamanio[0] * self.tamanio[1]

        # Modificadores por tipo
        modificadores = {
            TipoUbicacion.PUEBLO: 1.0,
            TipoUbicacion.CIUDAD: 1.5,
            TipoUbicacion.CAPITAL: 2.0,
            TipoUbicacion.MAZMORRA: 2.0,
            TipoUbicacion.POI: 0.5,
        }

        return int(area * 10 * modificadores.get(self.tipo, 1.0))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "x": self.x,
            "y": self.y,
            "bioma": self.bioma,
            "npcs": self.npcs,
            "servicios": self.servicios,
            "eventos": self.eventos,
            "rutas": self.rutas,
            "descubierta": self.descubierta,
            "visitada": self.visitada,
            "segura": self.segura,
            "tamanio": list(self.tamanio),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ubicacion":
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=TipoUbicacion(data["tipo"]),
            x=data["x"],
            y=data["y"],
            bioma=data["bioma"],
            npcs=data.get("npcs", []),
            servicios=data.get("servicios", []),
            eventos=data.get("eventos", []),
            rutas=data.get("rutas", []),
            descubierta=data.get("descubierta", False),
            visitada=data.get("visitada", False),
            segura=data.get("segura", True),
            tamanio=tuple(data.get("tamanio", [5, 5])),
        )

    def __repr__(self) -> str:
        return f"Ubicacion('{self.nombre}', {self.tipo.value}, ({self.x}, {self.y}))"


class UbicacionGenerator:
    """Generador de ubicaciones procedurales."""

    # Prefijos y sufijos para nombres
    PREFIJOS = {
        TipoUbicacion.PUEBLO: [
            "Aldea",
            "Pueblo",
            "Caserío",
            "Hamlet",
            "Villa",
            "Villorrio",
            "Poblado",
            "Refugio",
            "Coto",
            "Aldean",
            "Lugar",
            "Paraje",
            "Cruz",
            "Río",
            "Collado",
        ],
        TipoUbicacion.CIUDAD: [
            "Ciudad",
            "Fortaleza",
            "Puerto",
            "Villa",
            "Bastión",
            "Cidadela",
            "Metrópolis",
            "Urbe",
            "Plaza",
            "Torre",
            "Muralla",
            "Recinto",
            "Arrabal",
        ],
        TipoUbicacion.CAPITAL: [
            "Capital",
            "Metrópolis",
            "Ciudadela",
            "Imperial",
            "Sede",
            "Trono",
            "Reino",
            "Dominio",
            "Sededel",
            "Corona",
            "Majestad",
        ],
        TipoUbicacion.MAZMORRA: [
            "Cueva",
            "Ruinas",
            "Mazmorra",
            "Cripta",
            "Templo",
            "Sótano",
            "Abismo",
            "Pozo",
            "Laberinto",
            "Sala",
            "Cámara",
            "Túmulo",
            "Pirámide",
            "Torre",
            "Fortaleza",
            "Isla",
            "Volcán",
        ],
        TipoUbicacion.POI: [
            "Santuario",
            "Monolito",
            "Fuente",
            "Árbol",
            "Piedra",
            "Estatua",
            "Altar",
            "Pozo",
            "Túmulo",
            "Cruz",
            "Mojón",
            "Marca",
            "Hito",
            "Lago",
            "Cascada",
            "Cañón",
            "Colina",
            "Cumbre",
            "Valle",
        ],
    }

    ADJETIVOS = [
        "Antiguo",
        "Olvidado",
        "Sagrado",
        "Maldito",
        "Eterno",
        "Sombrío",
        "Luminoso",
        "Helado",
        "Ardiente",
        "Verde",
        "Dorado",
        "Plateado",
        "Carmesí",
        "Azul",
        "Negro",
        "Blanco",
        "Gris",
        "Púrpura",
        "Esmeralda",
        "Rubí",
        "Perdido",
        "Abandonado",
        "Encantado",
        "Embrujado",
        "Protegido",
        "Oculto",
        "Secreto",
        "Misterioso",
        "Legendario",
        "Fantasmal",
        "Silencioso",
        "Trágico",
        "Santo",
        "Profano",
        "Divino",
        "Salvaje",
        "Fértil",
        "Árido",
        "Bosco",
        "Selvático",
        "Costero",
        "Montañés",
        "Real",
        "Noble",
        "Pobre",
        "Fortificado",
        "Destruido",
        "Renacido",
        "Olvidadizo",
        "Bendito",
    ]

    SUSTANTIVOS = {
        TipoUbicacion.PUEBLO: [
            "del Roble",
            "del Río",
            "de la Colina",
            "del Bosque",
            "del Valle",
            "de la Ladera",
            "del Prado",
            "de las Flores",
            "del Viento",
            "de la Lluvia",
            "de la Montaña",
            "del Mar",
            "del Lago",
            "del Puerto",
            "de la Frontera",
            "del Paso",
            "del Collado",
            "de la Fuente",
            "del Manantial",
            "de las Minas",
        ],
        TipoUbicacion.CIUDAD: [
            "de Plata",
            "del Hierro",
            "de la Luz",
            "de las Tormentas",
            "del Mar",
            "del Sol",
            "de la Luna",
            "de las Estrellas",
            "del Trueno",
            "de la Aurora",
            "del Crepúsculo",
            "de la Noche",
            "del Día",
            "del Horizonte",
            "de los Mares",
            "de las Montañas",
            "del Valle",
            "del Río",
            "del Puerto",
            "de la Costa",
        ],
        TipoUbicacion.CAPITAL: [
            "de los Reyes",
            "Imperial",
            "del Trono",
            "Eterna",
            "de la Corona",
            "del Reino",
            "de los Cielos",
            "de la Victoria",
            "del Destino",
            "Eterna",
            "de la Gloria",
            "del Poder",
            "de la Sabiduría",
            "de la Justicia",
            "del Orden",
        ],
        TipoUbicacion.MAZMORRA: [
            "de los Caídos",
            "del Destino",
            "de las Sombras",
            "del Dragón",
            "del Terror",
            "de la Muerte",
            "del Vacío",
            "de la Locura",
            "del Infierno",
            "de los Milagros",
            "del Abismo",
            "de la Perdición",
            "del Colapso",
            "de la Ruina",
            "del Olvido",
            "de las Almas",
            "de los Condenados",
            "de la Escalera",
            "del Espejo",
            "del Tiempo",
        ],
        TipoUbicacion.POI: [
            "de los Deseos",
            "del Viento",
            "de la Luna",
            "del Sol",
            "de las Estrellas",
            "del Silencio",
            "de la Verdad",
            "de la Vida",
            "de la Muerte",
            "del Tiempo",
            "Eterno",
            "Primordial",
            "Ancestral",
            "de los Espíritus",
            "de los Dioses",
            "de la Bendición",
            "de la Maldición",
            "del Pact",
            "de la Promesa",
            "del Recuerdo",
        ],
    }

    def __init__(self, seed):
        """
        Inicializa el generador.

        Args:
            seed: Instancia de WorldSeed para determinismo
        """
        self.seed = seed

    def generar_nombre(self, tipo: TipoUbicacion, bioma: str, rng) -> str:
        """Genera un nombre único para la ubicación."""
        prefijos = self.PREFIJOS.get(tipo, ["Lugar"])
        sustantivos = self.SUSTANTIVOS.get(tipo, ["Misterioso"])

        # 50% con adjetivo
        if rng.random() < 0.5:
            prefijo = rng.choice(prefijos)
            adjetivo = rng.choice(self.ADJETIVOS)
            return f"{prefijo} {adjetivo}"
        else:
            prefijo = rng.choice(prefijos)
            sustantivo = rng.choice(sustantivos)
            return f"{prefijo} {sustantivo}"

    def generar_ubicacion(
        self, id: str, tipo: TipoUbicacion, x: int, y: int, bioma: str
    ) -> Ubicacion:
        """
        Genera una ubicación completa.

        Args:
            id: Identificador único
            tipo: Tipo de ubicación
            x: Coordenada X
            y: Coordenada Y
            bioma: Bioma donde está ubicada

        Returns:
            Instancia de Ubicacion
        """
        contexto = f"ubicacion_{id}"
        rng = self.seed.get_rng(contexto)

        # Generar nombre
        nombre = self.generar_nombre(tipo, bioma, rng)

        # Configuración
        config = CONFIG_UBICACION.get(tipo, {})

        # Tamaño aleatorio
        min_tam, max_tam = config.get("tamanos_sub_tiles", (5, 5))
        ancho = rng.randint(min_tam, max_tam)
        alto = rng.randint(min_tam, max_tam)

        # Crear ubicación
        ubicacion = Ubicacion(
            id=id,
            nombre=nombre,
            tipo=tipo,
            x=x,
            y=y,
            bioma=bioma,
            tamanio=(ancho, alto),
        )

        return ubicacion

    def generar_ubicaciones_iniciales(
        self,
        cantidad_pueblos: Tuple[int, int] = (10, 20),
        cantidad_ciudades: Tuple[int, int] = (3, 5),
        cantidad_capitales: Tuple[int, int] = (1, 2),
        cantidad_mazmorras: Tuple[int, int] = (20, 40),
        cantidad_pois: Tuple[int, int] = (30, 50),
        radio_mundo: int = 100,
    ) -> List[Ubicacion]:
        """
        Genera las ubicaciones iniciales del mundo.

        Args:
            cantidad_*: Tuplas (min, max) para cada tipo
            radio_mundo: Radio del mundo en tiles

        Returns:
            Lista de ubicaciones generadas
        """
        ubicaciones = []
        rng = self.seed.get_rng("ubicaciones_iniciales")

        # Contadores por tipo
        contadores = {
            TipoUbicacion.PUEBLO: rng.randint(*cantidad_pueblos),
            TipoUbicacion.CIUDAD: rng.randint(*cantidad_ciudades),
            TipoUbicacion.CAPITAL: rng.randint(*cantidad_capitales),
            TipoUbicacion.MAZMORRA: rng.randint(*cantidad_mazmorras),
            TipoUbicacion.POI: rng.randint(*cantidad_pois),
        }

        # Generar cada tipo
        for tipo, cantidad in contadores.items():
            for i in range(cantidad):
                # Posición aleatoria
                x = rng.randint(-radio_mundo, radio_mundo)
                y = rng.randint(-radio_mundo, radio_mundo)

                # Bioma aleatorio (se determinará después)
                bioma = "desconocido"

                # ID único
                id = f"{tipo.value}_{i}"

                ubicacion = self.generar_ubicacion(id, tipo, x, y, bioma)
                ubicaciones.append(ubicacion)

        return ubicaciones
