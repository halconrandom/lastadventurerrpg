# Sistema de Mapa - Last Adventurer

## Visión General

El sistema de mapa gestiona el mundo del juego: tiles con coordenadas X/Y, generación procedural, biomas, ubicaciones y rutas. Es la base para exploración, viajes y el sistema de tiempo.

---

## Decisiones Finales

| Aspecto | Decisión | Notas |
|---------|----------|-------|
| Escala de tiles | 1 km de lado | Tile = 1 km² |
| Mundo | Infinito con chunks | 1 chunk = 9 tiles (3x3), 30 chunks cargados |
| Transiciones | Suaves | Perlin noise |
| Ubicaciones | Opción B | 10-20 pueblos, 3-5 ciudades, 1-2 capitales, 20-40 mazmorras, 30-50 POIs |
| Distancias | Pathfinding A* | Considerando terreno |
| Revelado | 3 tiles alrededor | Radio de visión base |
| Spawn | Ubicación aleatoria | Cualquier pueblo/ciudad |
| Mapa de ubicaciones | Sub-tiles | 1 tile = 100 sub-tiles (10x10) |

---

## Componentes del Sistema

### 1. Estructura del Mundo

#### Tiles y Coordenadas

El mundo se divide en tiles (celdas) con coordenadas X/Y. Cada tile = 1 km².

```
        X →
   ┌───┬───┬───┬───┬───┐
 Y │0,0│1,0│2,0│3,0│4,0│
 ↓ ├───┼───┼───┼───┼───┤
   │0,1│1,1│2,1│3,1│4,1│
   ├───┼───┼───┼───┼───┤
   │0,2│1,2│2,2│3,2│4,2│
   └───┴───┴───┴───┴───┘
```

#### Datos por Tile

```python
class Tile:
    x: int                    # Coordenada X
    y: int                    # Coordenada Y
    bioma: str                # Tipo de bioma
    terreno: str              # Tipo de terreno específico
    explorado: bool           # Si el jugador lo ha visitado
    visible: bool             # Si el jugador lo ve actualmente
    
    # Contenido
    ubicacion_id: str         # ID de ubicación (pueblo, ciudad, etc.) o None
    recursos: list            # Recursos disponibles
    enemigos: list            # Enemigos potenciales
    eventos: list             # Eventos disponibles
    
    # Sub-tiles (si tiene ubicación)
    sub_tiles: list           # 100 sub-tiles (10x10) si hay ubicación
    
    # Conectividad
    rutas: list               # Rutas que pasan por este tile
```

---

### 2. Sistema de Sub-Tiles

Cada tile del mapa mundial puede contener **100 sub-tiles** (10x10) para ubicaciones.

#### Escala de Sub-Tiles

| Nivel | Escala | Tiempo de Viaje |
|-------|--------|-----------------|
| Tile macro | 1 km | 1 hora |
| Sub-tile | 100 m | 10 minutos |

#### Estructura de Sub-Tiles

```python
class SubTile:
    x: int                    # Coordenada X dentro del tile (0-9)
    y: int                    # Coordenada Y dentro del tile (0-9)
    tipo: str                 # calle/edificio/plaza/muro/etc
    contenido: dict           # NPCs, objetos, eventos
    
    # Coordenada global
    @property
    def coordenada_global(self) -> tuple:
        return (self.tile_x * 10 + self.x, self.tile_y * 10 + self.y)
```

#### Visualización

```
Tile Macro (1 km²):
┌─────────────────────────────┐
│  Sub-tiles 10x10            │
│  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│  │  │  │  │  │  │  │  │  │  │  │  Cada sub-tile
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤  = 100m x 100m
│  │  │  │  │  │  │  │  │  │  │  │  = 10 min viaje
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│  │  │  │  │  │  │  │  │  │  │  │
│  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
└─────────────────────────────┘
```

#### Tiempos de Viaje Unificados

| Acción | Distancia | Tiempo |
|--------|-----------|--------|
| Mover 1 tile macro | 1 km | 1 hora |
| Mover 1 sub-tile | 100 m | 10 minutos |
| Cruzar ciudad pequeña | ~5 sub-tiles | ~50 minutos |
| Cruzar ciudad grande | ~10 sub-tiles | ~1.5 horas |

---

### 3. Sistema de Chunks

El mundo es infinito pero se gestiona por chunks para optimizar rendimiento.

#### Estructura de Chunks

```python
class Chunk:
    x: int                    # Coordenada X del chunk
    y: int                    # Coordenada Y del chunk
    tiles: list               # 9 tiles (3x3)
    generado: bool            # Si ya fue generado
```

#### Gestión de Chunks

```python
class GestorChunks:
    radio_carga: int = 30     # Chunks cargados alrededor del jugador
    
    def cargar_chunks_around(self, x: int, y: int) -> list:
        # Carga chunks en radio de 30 alrededor de la posición
        pass
    
    def descargar_chunks_lejanos(self, x: int, y: int) -> list:
        # Descarga chunks fuera del radio
        pass
    
    def generar_chunk(self, x: int, y: int) -> Chunk:
        # Genera un chunk nuevo proceduralmente
        pass
```

#### Visualización

```
Chunk 3x3 tiles:
┌───┬───┬───┐
│0,0│1,0│2,0│  ← 1 chunk = 9 tiles
├───┼───┼───┤     = 9 km²
│0,1│1,1│2,1│
├───┼───┼───┤
│0,2│1,2│2,2│
└───┴───┴───┘

30 chunks de radio = ~2700 tiles cargados máximo
```

---

### 4. Generación Procedural

El mundo se genera proceduralmente al crear una nueva partida.

#### Semilla del Mundo

```python
class SemillaMundo:
    seed: int                 # Semilla base para RNG
    bioma_seed: int           # Semilla para distribución de biomas
    ubicaciones_seed: int     # Semilla para ubicaciones
    rutas_seed: int           # Semilla para rutas
    sub_tiles_seed: int       # Semilla para sub-tiles de ubicaciones
```

#### Proceso de Generación

1. **Generar biomas**: Usar Perlin noise para distribución natural con transiciones suaves
2. **Generar ubicaciones**: Pueblos, ciudades, puntos de interés
3. **Generar sub-tiles**: Mapa interno de cada ubicación
4. **Generar rutas**: Conexiones entre ubicaciones usando A*
5. **Generar contenido**: Recursos, enemigos, eventos por tile

---

### 5. Biomas

Los biomas definen el tipo de terreno y afectan clima, recursos y enemigos.

#### Biomas Base

| Bioma | Terrenos | Clima Base | Recursos | Enemigos |
|-------|----------|------------|----------|----------|
| Bosque | Denso, Claro, Ancestral | Templado | Madera, Plantas | Lobos, Bandidos |
| Desierto | Dunas, Oasis, Ruinas | Árido/Caliente | Cactus, Minerales | Escorpiones, Nómadas |
| Tundra | Hielo, Nieve, Glaciares | Frío eterno | Hielo, Pieles | Osos, Tribus |
| Jungla | Denso, Pantanoso, Ruinas | Húmedo/Caliente | Plantas raras, Madera | Serpientes, Bestias |
| Pantano | Ciénaga, Fango, Niebla | Húmedo | Hongos, Plantas | Criaturas, No-muertos |
| Montaña | Picos, Valles, Cavernas | Frío | Minerales, Piedra | Gigantes, Dragones |
| Costa | Playa, Acantilados, Puertos | Moderado | Pescado, Sal | Piratas, Sirenas |
| Pradera | Campos, Colinas, Granjas | Templado | Cultivos, Ganado | Bandidos, Animales |

#### Transiciones Suaves

Los biomas usan Perlin noise para transiciones naturales sin bordes abruptos.

---

### 6. Ubicaciones

Las ubicaciones son puntos de interés en el mapa.

#### Cantidad de Ubicaciones (Opción B)

| Tipo | Cantidad | NPCs | Servicios | Sub-tiles |
|------|----------|------|-----------|-----------|
| Pueblos | 10-20 | 10-50 | Básicos | 5x5 - 8x8 |
| Ciudades | 3-5 | 50-200 | Completos | 8x8 - 10x10 |
| Capitales | 1-2 | 200+ | Especiales | 10x10 (usa múltiples tiles) |
| Mazmorras | 20-40 | 0 | Combate | Variable |
| POIs | 30-50 | 0-5 | Eventos | 3x3 - 5x5 |

#### Estructura de Ubicación

```python
class Ubicacion:
    id: str                   # Identificador único
    nombre: str               # Nombre generado
    tipo: str                 # pueblo/ciudad/capital/mazmorra/poi
    x: int                    # Coordenada X del tile
    y: int                    # Coordenada Y del tile
    bioma: str                # Bioma donde está ubicada
    
    # Sub-tiles
    sub_tiles: list           # Matriz de sub-tiles
    
    # Contenido
    npcs: list                # NPCs en la ubicación
    servicios: list           # Tiendas, herreros, etc.
    eventos: list             # Eventos disponibles
    
    # Conexiones
    rutas: list               # Rutas hacia otras ubicaciones
```

---

### 7. Sistema de Rutas y Distancias

Las rutas conectan ubicaciones y definen el tiempo de viaje.

#### Estructura de Rutas

```python
class Ruta:
    id: str                   # Identificador único
    origen: str               # ID de ubicación origen
    destino: str              # ID de ubicación destino
    tipo: str                 # camino/sendero/carretera/rio
    distancia: float          # Distancia en km
    tiempo_base: int          # Tiempo base en horas
    dificultad: int           # 1-10 (afecta eventos negativos)
    tiles: list               # Lista de coordenadas [(x,y), ...]
    eventos_posibles: list    # Eventos que pueden ocurrir en la ruta
```

#### Modificadores de Tiempo por Terreno

| Terreno | Multiplicador |
|---------|---------------|
| Carretera | 1.0x |
| Pradera | 1.2x |
| Bosque | 1.5x |
| Pantano | 2.0x |
| Montaña | 2.5x |
| Desierto | 1.8x |
| Tundra | 2.0x |

---

### 8. Exploración y Revelado

#### Estados de Visibilidad

| Estado | Descripción |
|--------|-------------|
| No descubierto | Tile completamente oculto |
| Descubierto | Tile visible pero sin detalles |
| Explorado | Tile visitado, todos los detalles visibles |
| Actual | Tile donde está el jugador ahora |

#### Radio de Visión (3 tiles)

```python
class VisionJugador:
    radio_base: int = 3       # Tiles visibles alrededor
    
    def calcular_visibles(self, x: int, y: int) -> list:
        visibles = []
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if abs(dx) + abs(dy) <= 3:  # Distancia Manhattan
                    visibles.append((x + dx, y + dy))
        return visibles
```

---

### 9. Spawn del Jugador

El jugador aparece en una ubicación aleatoria al inicio.

```python
def generar_spawn_aleatorio(ubicaciones: list) -> Ubicacion:
    # Filtrar ubicaciones seguras (pueblos y ciudades)
    ubicaciones_seguras = [u for u in ubicaciones if u.tipo in ["pueblo", "ciudad"]]
    
    # Seleccionar aleatoriamente
    return random.choice(ubicaciones_seguras)
```

---

### 10. Persistencia del Mapa

#### Datos a Persistir

```json
{
  "mapa": {
    "seed": 12345,
    "chunks_generados": [
      {"x": 0, "y": 0, "tiles": [...]},
      {"x": 1, "y": 0, "tiles": [...]}
    ],
    "tiles_explorados": [
      {"x": 0, "y": 0, "bioma": "bosque", "explorado": true}
    ],
    "ubicaciones_conocidas": ["pueblo_1", "ciudad_1"],
    "rutas_conocidas": ["ruta_1", "ruta_2"],
    "posicion_actual": {"x": 5, "y": 3, "sub_x": 2, "sub_y": 5}
  }
}
```

---

## Estructura de Archivos

```
backend/src/systems/
├── mapa.py                # Sistema principal de mapa
├── chunks.py              # Gestión de chunks
├── sub_tiles.py           # Sistema de sub-tiles
├── generacion_mundo.py    # Generación procedural
├── biomas.py              # Definición de biomas
├── ubicaciones.py         # Gestión de ubicaciones
├── rutas.py               # Sistema de rutas
└── ...

backend/src/api/
├── mapa.py                # Endpoints de mapa
└── ...

frontend/src/hooks/
├── useMapa.ts             # Hook para mapa
└── ...

frontend/src/components/
├── MapDisplay.tsx         # Componente de mapa
└── ...
```

---

## Dependencias

| Sistema | Relación |
|---------|----------|
| **Tiempo** | Consume distancias para calcular viajes (1 tile = 1 hora, 1 sub-tile = 10 min) |
| Clima | Recibe bioma para clima base |
| NPCs | Recibe ubicación para spawn |
| Exploración | Consume tiles y visibilidad |
| Combate | Recibe enemigos por tile |

---

---

## 11. Sistema de Mapa Progresivo (Cartografía)

El mapa no está disponible desde el inicio. El jugador debe obtenerlo y mejorarlo.

### Fases del Mapa

| Fase | Cómo obtener | Funcionalidad |
|------|--------------|---------------|
| **Sin Mapa** | Inicio del juego | Solo descripciones textuales |
| **Mapa Básico** | Comprar (100 oro) o encontrar | Muestra tiles explorados como símbolos |
| **Mapa Detallado** | Cartógrafo (500 oro) | Muestra biomas, rutas, nombres |
| **Mapa Maestro** | Quest especial | Muestra POIs, enemigos, recursos |

### Interfaz del Mapa

#### Sin Mapa (Fase 1)

El jugador solo ve descripciones direccionales:

```
┌─────────────────────────────────────────┐
│  📍 Bosque Ancestral                    │
│                                         │
│  "El claro está bañado por luz tenue.  │
│   Un roble centenario te observa."     │
│                                         │
│  🚶 DESTINOS:                          │
│  ↑ Norte → Monte Gris (3 días)         │
│  → Este → Río Plateado (1 día)         │
│  ↓ Sur → Ciudad de Plata (2 días)     │
│  ← Oeste → Bosque Profundo [???]       │
│                                         │
│  [EXPLORAR] [ACAMPAR] [INVENTARIO]     │
└─────────────────────────────────────────┘
```

#### Con Mapa (Fase 2+)

El jugador puede abrir un panel de mapa visual:

```
┌─────────────────────────────────────────────────────────┐
│                    MAPA DEL REINO                       │
├─────────────────────────────────────────────────────────┤
│  ╔═══════════════════════════════════════════════════╗ │
│  ║  ???  ???  🏔️   ???  ???  ???  ???  ???  ???  ??? ║ │
│  ║  ???  ???  ???  ???  ???  ???  ???  ???  ???  ??? ║ │
│  ║  🌲  🌲  🌲  🌲  🌲  🌲  ???  ???  ???  ???  ???  ??? ║ │
│  ║  🌲  🏘️  🛤️  🌲  ???  ???  ???  ???  ???  ???  ??? ║ │
│  ║  🌲  🌲  🌲  🏛️  🌲  ???  ???  ???  ???  ???  ??? ║ │
│  ║  🌊  🌲  🌲  🌲  🌲  ???  ???  ???  ???  ???  ??? ║ │
│  ║  ???  ???  ???  ???  ???  ???  ???  ???  ???  ??? ║ │
│  ╚═══════════════════════════════════════════════════╝ │
│                                                         │
│  📍 Estás aquí: Bosque Ancestral (12, 45)              │
│  🗺️ Explorado: 23% | 📋 Ubicaciones: 3/50              │
│                                                         │
│  [Zoom +] [Zoom -] [Leyenda] [Cerrar]                  │
└─────────────────────────────────────────────────────────┘
```

### Leyenda de Símbolos

| Símbolo | Significado | Se revela con |
|---------|-------------|---------------|
| `???` | No explorado | - |
| `🌲` | Bosque | Explorar tile |
| `🏔️` | Montaña | Explorar tile |
| `🏜️` | Desierto | Explorar tile |
| `🌊` | Agua/Costa | Explorar tile |
| `🏘️` | Pueblo | Explorar tile o Mapa Detallado |
| `🏛️` | Ruinas/POI | Explorar tile o Mapa Maestro |
| `🛤️` | Camino/Ruta | Mapa Detallado |
| `⚠️` | Peligro | Mapa Maestro |
| `💎` | Recurso | Mapa Maestro |

### Skill de Cartografía

```python
class SkillCartografia:
    nivel: int              # 1-5
    experiencia: int        # Acumulada al explorar
    
    beneficios = {
        1: "Mapa básico disponible",
        2: "Revela biomas de tiles adyacentes",
        3: "Revela POIs cercanos",
        4: "Marca enemigos en el mapa",
        5: "Revela rutas ocultas"
    }
    
    def ganar_experiencia(self, tiles_explorados: int):
        # Gana XP por explorar tiles nuevos
        self.experiencia += tiles_explorados * 10
        self._subir_nivel()
```

### Items de Cartografía

| Item | Efecto | Cómo obtener |
|------|--------|--------------|
| **Mapa Básico** | Desbloquea panel de mapa | Comprar (100 oro) |
| **Mapa Detallado** | Muestra biomas y rutas | Cartógrafo (500 oro) |
| **Mapa Maestro** | Muestra todo | Quest especial |
| **Brújula Mágica** | Dirección a ubicaciones conocidas | Encontrar/Comprar |
| **Telescopio** | Revela tiles adyacentes | Encontrar/Comprar |
| **Kit de Cartógrafo** | +50% XP cartografía | Comprar |

### Integración con Exploración

El mapa se revela automáticamente al explorar:

```python
def explorar_tile(jugador, x, y):
    # Revelar tile en el mapa
    if jugador.tiene_mapa:
        jugador.mapa.revelar_tile(x, y)
        
        # Si tiene skill de cartografía
        if jugador.skill_cartografia >= 2:
            # Revelar tiles adyacentes (solo bioma)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                jugador.mapa.revelar_bioma(x+dx, y+dy)
        
        # Ganar experiencia de cartografía
        jugador.skill_cartografia.ganar_experiencia(1)
```

---

## Próximos Pasos

1. ✅ Documento completado
2. ✅ Sistema de mapa progresivo añadido
3. 🔜 Implementación en `experiments/mapa/`
4. 🔜 Tests de validación
5. 🔜 Integración al backend principal