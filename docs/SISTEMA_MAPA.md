# Sistema de Mapa - Last Adventurer

## Filosofía de Diseño

> *"El mundo es infinito, pero cada paso tiene significado. No hay fast travel porque el viaje ES el juego."*

### Principios Core

1. **Mundo Infinito** - Generación procedural sin límites artificiales
2. **Coordenadas X/Y** - Sistema de tiles con posición exacta
3. **Sin Fast Travel** - Exploración a pie obligatoria
4. **Spawn Aleatorio** - No hay hub fijo, cada partida comienza en un lugar único
5. **Continuidad** - Zonas adyacentes son coherentes entre sí
6. **Persistencia Total** - Todo cambio en el mapa se guarda permanentemente

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        WORLD MANAGER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    SEED      │  │    TIME      │  │    GLOBAL STATE      │  │
│  │  (Semilla)   │  │   (Ticks)    │  │  (Historia/Mundo)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CHUNK MANAGER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ CHUNK CACHE  │  │ NOISE MAP    │  │ BIOME MAP            │  │
│  │ (Zonas Act.) │  │ (Perlin)     │  │ (Distribución)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CHUNK (Zona)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    TILES     │  │  ENTIDADES   │  │      POI             │  │
│  │  (32x32)     │  │ (NPCs/Enem.) │  │  (Puntos Interés)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          TILE                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   TERRENO    │  │   OBJETO     │  │     ENTIDAD          │  │
│  │ (Tipo/Color) │  │ (Item/Estruct)│  │  (NPC/Enemigo)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Sistema de Coordenadas

### Estructura del Mundo

```
MUNDO (Infinito)
│
├── CHUNKS (Zonas de 32x32 tiles)
│   ├── Chunk (-1,-1)    Chunk (0,-1)    Chunk (1,-1)
│   ├── Chunk (-1,0)     Chunk (0,0)     Chunk (1,0)   ← Spawn inicial
│   ├── Chunk (-1,1)    Chunk (0,1)     Chunk (1,1)
│   └── ... (infinito en todas direcciones)
│
└── TILES (Celdas individuales de 1x1)
    └── Cada tile tiene coordenadas globales (x, y)
```

### Tipos de Coordenadas

```python
# Coordenadas Globales (World Coordinates)
# - Rango: Infinito (integers)
# - Formato: (x, y) donde x e y pueden ser negativos
# - Ejemplo: (1542, -893)

# Coordenadas de Chunk
# - Rango: Infinito (integers)
# - Formato: (chunk_x, chunk_y)
# - Conversión: chunk_x = world_x // CHUNK_SIZE

# Coordenadas Locales (dentro de un chunk)
# - Rango: 0 a CHUNK_SIZE-1
# - Formato: (local_x, local_y)
# - Conversión: local_x = world_x % CHUNK_SIZE
```

### Implementación

```python
from dataclasses import dataclass
from typing import Tuple, Optional
import math

CHUNK_SIZE = 32  # 32x32 tiles por chunk
WORLD_SEED = None  # Se define al crear el mundo

@dataclass
class Coordenadas:
    """Sistema de coordenadas del mundo"""
    x: int
    y: int
    
    def to_chunk(self) -> Tuple[int, int]:
        """Convierte a coordenadas de chunk"""
        chunk_x = self.x // CHUNK_SIZE if self.x >= 0 else (self.x + 1) // CHUNK_SIZE - 1
        chunk_y = self.y // CHUNK_SIZE if self.y >= 0 else (self.y + 1) // CHUNK_SIZE - 1
        return (chunk_x, chunk_y)
    
    def to_local(self) -> Tuple[int, int]:
        """Convierte a coordenadas locales del chunk"""
        local_x = self.x % CHUNK_SIZE if self.x >= 0 else (self.x % CHUNK_SIZE + CHUNK_SIZE) % CHUNK_SIZE
        local_y = self.y % CHUNK_SIZE if self.y >= 0 else (self.y % CHUNK_SIZE + CHUNK_SIZE) % CHUNK_SIZE
        return (local_x, local_y)
    
    def distancia(self, other: 'Coordenadas') -> float:
        """Calcula distancia euclidiana"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def distancia_manhattan(self, other: 'Coordenadas') -> int:
        """Calcula distancia Manhattan (para pathfinding)"""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def adyacentes(self) -> list:
        """Retorna coordenadas adyacentes (4 direcciones)"""
        return [
            Coordenadas(self.x, self.y - 1),      # Norte
            Coordenadas(self.x, self.y + 1),      # Sur
            Coordenadas(self.x + 1, self.y),      # Este
            Coordenadas(self.x - 1, self.y),      # Oeste
        ]
    
    def vecinos(self) -> list:
        """Retorna todos los vecinos (8 direcciones)"""
        vecinos = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    vecinos.append(Coordenadas(self.x + dx, self.y + dy))
        return vecinos
    
    def direccion_hacia(self, other: 'Coordenadas') -> str:
        """Retorna dirección cardinal hacia otro punto"""
        dx = other.x - self.x
        dy = other.y - self.y
        
        if abs(dx) > abs(dy):
            return "este" if dx > 0 else "oeste"
        else:
            return "sur" if dy > 0 else "norte"
```

---

## 2. Sistema de Tiles

### Tipos de Terreno

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class TipoTerreno(Enum):
    """Tipos básicos de terreno"""
    # Naturales
    PASTO = "pasto"
    TIERRA = "tierra"
    PIEDRA = "piedra"
    AGUA = "agua"
    ARENA = "arena"
    NIEVE = "nieve"
    HIELO = "hielo"
    LAVA = "lava"
    CENIZA = "ceniza"
    
    # Vegetación
    BOSQUE_DENSO = "bosque_denso"
    BOSQUE_CLARO = "bosque_claro"
    JUNGLA = "jungla"
    PANTANO = "pantano"
    
    # Construidos
    CAMINO = "camino"
    PUENTE = "puente"
    RUINAS = "ruinas"
    PISO_PIEDRA = "piso_piedra"
    
    # Especiales
    VACIO = "vacio"          # No explorado
    FRONTERA = "frontera"    # Límite del mundo conocido

class TipoObjeto(Enum):
    """Objetos que pueden estar en un tile"""
    NINGUNO = "ninguno"
    
    # Naturales
    ARBOL = "arbol"
    ROCA = "roca"
    FLOR = "flor"
    HIERBA = "hierba"
    SETO = "seto"
    
    # Recursos
    MINERAL = "mineral"
    VEGETAL = "vegetal"
    CADAVER = "cadaver"
    
    # Construcciones
    PUERTA = "puerta"
    COFRE = "cofre"
    TRAMPA = "trampa"
    ALTAR = "altar"
    
    # Items en suelo
    ITEM_SUELO = "item_suelo"
    ORO_SUELO = "oro_suelo"

@dataclass
class Tile:
    """Un tile individual del mapa"""
    coordenadas: Coordenadas
    terreno: TipoTerreno
    objeto: Optional[TipoObjeto] = None
    entidad_id: Optional[str] = None      # ID de NPC/Enemigo en el tile
    item_suelo: Optional[Dict] = None     # Items tirados en el tile
    
    # Estado
    explorado: bool = False
    visible: bool = False
    
    # Metadatos
    variacion: int = 0          # Variación visual (0-15)
    humedad: float = 0.5        # 0-1, afecta vegetación
    fertilidad: float = 0.5     # 0-1, afecta recursos
    
    # Propiedades derivadas
    @property
    def transitable(self) -> bool:
        """Si el jugador puede caminar sobre este tile"""
        NO_TRANSITABLES = {
            TipoTerreno.AGUA, TipoTerreno.LAVA, TipoTerreno.VACIO,
            TipoTerreno.FRONTERA
        }
        OBJETOS_BLOQUEANTES = {
            TipoObjeto.ARBOL, TipoObjeto.ROCA, TipoObjeto.PUERTA
        }
        
        if self.terreno in NO_TRANSITABLES:
            return False
        if self.objeto in OBJETOS_BLOQUEANTES:
            return False
        if self.entidad_id is not None:
            return False
        return True
    
    @property
    def velocidad_movimiento(self) -> float:
        """Multiplicador de velocidad al moverse (1.0 = normal)"""
        modificadores = {
            TipoTerreno.PASTO: 1.0,
            TipoTerreno.CAMINO: 1.2,
            TipoTerreno.BOSQUE_DENSO: 0.7,
            TipoTerreno.PANTANO: 0.5,
            TipoTerreno.NIEVE: 0.8,
            TipoTerreno.ARENA: 0.9,
            TipoTerreno.HIELO: 0.6,
        }
        return modificadores.get(self.terreno, 1.0)
    
    @property
    def vision_bonus(self) -> float:
        """Bonus/malus de visión en este tile"""
        bonus = {
            TipoTerreno.BOSQUE_DENSO: -0.3,
            TipoTerreno.BOSQUE_CLARO: -0.1,
            TipoTerreno.PANTANO: -0.2,
            TipoTerreno.JUNGLA: -0.4,
        }
        return bonus.get(self.terreno, 0.0)
    
    @property
    def sigilo_bonus(self) -> float:
        """Bonus de sigilo en este tile"""
        bonus = {
            TipoTerreno.BOSQUE_DENSO: 0.2,
            TipoTerreno.PANTANO: 0.1,
            TipoTerreno.CAMINO: -0.2,
        }
        return bonus.get(self.terreno, 0.0)
    
    def to_dict(self) -> dict:
        """Serializa el tile para guardar"""
        return {
            "x": self.coordenadas.x,
            "y": self.coordenadas.y,
            "terreno": self.terreno.value,
            "objeto": self.objeto.value if self.objeto else None,
            "entidad_id": self.entidad_id,
            "item_suelo": self.item_suelo,
            "explorado": self.explorado,
            "variacion": self.variacion,
            "humedad": self.humedad,
            "fertilidad": self.fertilidad
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tile':
        """Deserializa un tile"""
        return cls(
            coordenadas=Coordenadas(data["x"], data["y"]),
            terreno=TipoTerreno(data["terreno"]),
            objeto=TipoObjeto(data["objeto"]) if data.get("objeto") else None,
            entidad_id=data.get("entidad_id"),
            item_suelo=data.get("item_suelo"),
            explorado=data.get("explorado", False),
            variacion=data.get("variacion", 0),
            humedad=data.get("humedad", 0.5),
            fertilidad=data.get("fertilidad", 0.5)
        )
```

---

## 3. Sistema de Chunks (Zonas)

### Estructura del Chunk

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random

@dataclass
class Chunk:
    """Un chunk de 32x32 tiles"""
    coordenadas: Tuple[int, int]          # Coordenadas del chunk
    bioma: str                            # Tipo de bioma
    nombre: str                           # Nombre único de la zona
    
    # Contenido
    tiles: Dict[Tuple[int, int], Tile] = field(default_factory=dict)
    entidades: List[str] = field(default_factory=list)      # IDs de entidades
    poi: List[Dict] = field(default_factory=list)           # Puntos de interés
    
    # Estado
    generado: bool = False
    visitado: bool = False
    veces_explorado: int = 0
    
    # Metadatos
    nivel_zona: int = 1
    clima_actual: str = "despejado"
    variacion_bioma: str = "normal"
    
    # Constantes
    SIZE = CHUNK_SIZE
    
    def generar(self, seed: 'WorldSeed', noise_map: dict) -> None:
        """Genera el chunk proceduralmente"""
        if self.generado:
            return
        
        rng = seed.get_rng(f"chunk_{self.coordenadas}")
        
        # Generar tiles
        for local_y in range(self.SIZE):
            for local_x in range(self.SIZE):
                world_x = self.coordenadas[0] * self.SIZE + local_x
                world_y = self.coordenadas[1] * self.SIZE + local_y
                
                tile = self._generar_tile(
                    rng, local_x, local_y, 
                    world_x, world_y, noise_map
                )
                self.tiles[(local_x, local_y)] = tile
        
        # Generar entidades
        self._generar_entidades(rng)
        
        # Generar POIs
        self._generar_poi(rng)
        
        self.generado = True
    
    def _generar_tile(self, rng: random.Random, local_x: int, local_y: int,
                      world_x: int, world_y: int, noise_map: dict) -> Tile:
        """Genera un tile individual"""
        # Obtener terreno base del bioma
        terreno = self._determinar_terreno(rng, local_x, local_y, noise_map)
        
        # Determinar objeto (árbol, roca, etc.)
        objeto = self._determinar_objeto(rng, terreno)
        
        # Calcular propiedades
        humedad = noise_map.get("humedad", (world_x, world_y), 0.5)
        fertilidad = noise_map.get("fertilidad", (world_x, world_y), 0.5)
        
        return Tile(
            coordenadas=Coordenadas(world_x, world_y),
            terreno=terreno,
            objeto=objeto,
            variacion=rng.randint(0, 15),
            humedad=humedad,
            fertilidad=fertilidad
        )
    
    def _determinar_terreno(self, rng: random.Random, x: int, y: int, 
                           noise_map: dict) -> TipoTerreno:
        """Determina el tipo de terreno basado en bioma y noise"""
        # Mapeo de biomas a terrenos posibles
        terrenos_bioma = {
            "bosque_ancestral": [
                (TipoTerreno.PASTO, 0.6),
                (TipoTerreno.BOSQUE_CLARO, 0.25),
                (TipoTerreno.BOSQUE_DENSO, 0.15)
            ],
            "paramo_marchito": [
                (TipoTerreno.T