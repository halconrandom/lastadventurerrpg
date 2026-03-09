# Sistema de Mapa - Last Adventurer

## Visión General

El sistema de mapa gestiona el mundo del juego: tiles con coordenadas X/Y, generación procedural, biomas, ubicaciones y rutas. Es la base para exploración, viajes y el sistema de tiempo.

---

## Decisiones Tomadas (Iteración 1)

| Aspecto | Decisión | Notas |
|---------|----------|-------|
| Escala de tiles | 1 km de lado | Tile = 1 km² |
| Mundo | Infinito con chunks | 1 chunk = 9 tiles (3x3), 30 chunks cargados |
| Transiciones | Suaves | Perlin noise |
| Ubicaciones | Opción B | 10-20 pueblos, 3-5 ciudades, 1-2 capitales, 20-40 mazmorras, 30-50 POIs |
| Distancias | Pathfinding A* | Considerando terreno |
| Revelado | 3 tiles alrededor | Radio de visión base |
| Spawn | Ubicación aleatoria | Cualquier pueblo/ciudad |

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
    
    # Conectividad
    rutas: list               # Rutas que pasan por este tile
```

---

### 2. Sistema de Chunks

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

### 3. Generación Procedural

El mundo se genera proceduralmente al crear una nueva partida.

#### Semilla del Mundo

```python
class SemillaMundo:
    seed: int                 # Semilla base para RNG
    bioma_seed: int           # Semilla para distribución de biomas
    ubicaciones_seed: int     # Semilla para ubicaciones
    rutas_seed: int           # Semilla para rutas
```

#### Proceso de Generación

1. **Generar biomas**: Usar Perlin noise para distribución natural con transiciones suaves
2. **Generar ubicaciones**: Pueblos, ciudades, puntos de interés
3. **Generar rutas**: Conexiones entre ubicaciones usando A*
4. **Generar contenido**: Recursos, enemigos, eventos por tile

---

### 4. Biomas

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

### 5. Ubicaciones

Las ubicaciones son puntos de interés en el mapa.

#### Cantidad de Ubicaciones (Opción B)

| Tipo | Cantidad | NPCs | Servicios |
|------|----------|------|-----------|
| Pueblos | 10-20 | 10-50 | Básicos (tienda, posada) |
| Ciudades | 3-5 | 50-200 | Completos (tienda, herrero, posada, templo) |
| Capitales | 1-2 | 200+ | Especiales + servicios completos |
| Mazmorras | 20-40 | 0 | Combate, tesoros |
| POIs | 30-50 | 0-5 | Eventos especiales |

#### Estructura de Ubicación

```python
class Ubicacion:
    id: str                   # Identificador único
    nombre: str               # Nombre generado
    tipo: str                 # pueblo/ciudad/capital/mazmorra/poi
    x: int                    # Coordenada X
    y: int                    # Coordenada Y
    bioma: str                # Bioma donde está ubicada
    npcs: list                # NPCs en la ubicación
    servicios: list           # Tiendas, herreros, etc.
    eventos: list             # Eventos disponibles
    rutas: list               # Rutas hacia otras ubicaciones
```

---

### 6. Mapa de Ubicación (Pregunta Pendiente)

**Pregunta 8**: ¿Cómo funciona el mapa DENTRO de una ubicación?

Si un tile del mapa mundial = 1 km², ¿cómo se mueve el jugador dentro de una ciudad?

#### Opciones

| Opción | Descripción | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| **A) Mapa de ubicación** | Cada ubicación tiene su propio mapa con tiles pequeños (10m/tile) | Exploración detallada | Doble sistema de mapas |
| **B) Sub-tiles** | Un tile mundial se subdivide en 100 sub-tiles (10x10) | Sistema unificado | Complejo |
| **C) Instancias** | Ubicaciones son escenas separadas, sin tiles | Simple | Menos inmersión |
| **D) Escala variable** | Dentro de ubicaciones, tiempo por acción sin mapa visual | Muy simple | Sin exploración visual |

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
    "posicion_actual": {"x": 5, "y": 3}
  }
}
```

---

## Preguntas para la Segunda Iteración

### Pregunta 8: Mapa dentro de Ubicaciones
¿Cómo funciona el mapa DENTRO de una ubicación (ciudad, pueblo)?

| Opción | Descripción |
|--------|-------------|
| A | Mapa de ubicación con tiles pequeños (10m/tile) |
| B | Sub-tiles (1 tile mundial = 100 sub-tiles) |
| C | Instancias separadas sin tiles |
| D | Sin mapa visual, solo menús/diálogos |

---

## Estructura de Archivos

```
backend/src/systems/
├── mapa.py                # Sistema principal de mapa
├── chunks.py              # Gestión de chunks
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
| **Tiempo** | Consume distancias para calcular viajes |
| Clima | Recibe bioma para clima base |
| NPCs | Recibe ubicación para spawn |
| Exploración | Consume tiles y visibilidad |
| Combate | Recibe enemigos por tile |

---

## Próximos Pasos

1. ✅ Primera iteración completada
2. ⏳ Segunda iteración (pregunta 8)
3. 🔜 Implementación en `experiments/mapa/`
4. 🔜 Tests de validación
5. 🔜 Integración al backend principal