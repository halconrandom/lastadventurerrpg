# Sistema de Mapa - Last Adventurer

## Visión General

El sistema de mapa gestiona el mundo del juego: tiles con coordenadas X/Y, generación procedural, biomas, ubicaciones y rutas. Es la base para exploración, viajes y el sistema de tiempo.

---

## Componentes del Sistema

### 1. Estructura del Mundo

#### Tiles y Coordenadas

El mundo se divide en tiles (celdas) con coordenadas X/Y.

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

**Pregunta 1**: ¿Cuál debería ser el tamaño de un tile en términos de "escala"?

| Opción | Escala | Descripción |
|--------|--------|-------------|
| A | 1 km² | Un tile = 1 km de lado |
| B | 5 km² | Un tile = 5 km de lado |
| C | 10 km² | Un tile = 10 km de lado |
| D | Abstracto | No tiene escala real, es una unidad de juego |

---

### 2. Generación Procedural

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

1. **Generar biomas**: Usar Perlin noise para distribución natural
2. **Generar ubicaciones**: Pueblos, ciudades, puntos de interés
3. **Generar rutas**: Conexiones entre ubicaciones
4. **Generar contenido**: Recursos, enemigos, eventos por tile

**Pregunta 2**: ¿El mundo debe ser infinito o tener límites?

| Opción | Descripción | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| A | Infinito | Exploración sin límites | Dificulta persistencia |
| B | Limitado (ej: 1000x1000) | Mundo finito, manejable | Límite artificial |
| C | Expande dinámicamente | Crece según el jugador explora | Complejo de implementar |

---

### 3. Biomas

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

**Pregunta 3**: ¿Los biomas deben tener transiciones suaves o bordes definidos?

| Opción | Descripción |
|--------|-------------|
| A | Transiciones suaves (Perlin noise) |
| B | Bordes definidos (cambio abrupto) |
| C | Zonas de transición (tiles mixtos) |

---

### 4. Ubicaciones

Las ubicaciones son puntos de interés en el mapa: pueblos, ciudades, mazmorras, etc.

#### Tipos de Ubicaciones

| Tipo | Tamaño | Descripción | Ejemplos |
|------|--------|-------------|----------|
| Pueblo | Pequeño | 10-50 NPCs, servicios básicos | Aldea, Campamento |
| Ciudad | Mediano | 50-200 NPCs, servicios completos | Puerto, Fortaleza |
| Capital | Grande | 200+ NPCs, servicios especiales | Ciudad principal |
| Mazmorra | Variable | Exploración, combate, tesoros | Cueva, Ruinas |
| Punto de Interés | Pequeño | Sin NPCs, eventos especiales | Santuario, Monolito |

#### Generación de Ubicaciones

```python
class Ubicacion:
    id: str                   # Identificador único
    nombre: str               # Nombre generado
    tipo: str                 # pueblo/ciudad/capital/mazmorra/poi
    x: int                    # Coordenada X
    y: int                    # Coordenada Y
    bioma: str                # Bioma donde está ubicada
    
    # Contenido
    npcs: list                # NPCs en la ubicación
    servicios: list           # Tiendas, herreros, etc.
    eventos: list             # Eventos disponibles
    
    # Conexiones
    rutas: list               # Rutas hacia otras ubicaciones
```

**Pregunta 4**: ¿Cuántas ubicaciones debería generar el mundo inicial?

| Opción | Pueblos | Ciudades | Capitales | Mazmorras | POIs |
|--------|---------|----------|-----------|-----------|------|
| A | 5-10 | 2-3 | 1 | 10-20 | 20-30 |
| B | 10-20 | 3-5 | 1-2 | 20-40 | 30-50 |
| C | 20-40 | 5-10 | 2-3 | 40-80 | 50-100 |

---

### 5. Sistema de Rutas y Distancias

Las rutas conectan ubicaciones y definen el tiempo de viaje.

#### Estructura de Rutas

```python
class Ruta:
    id: str                   # Identificador único
    origen: str               # ID de ubicación origen
    destino: str              # ID de ubicación destino
    tipo: str                 # camino/sendero/carretera/rio
    
    # Propiedades
    distancia: float          # Distancia en km
    tiempo_base: int          # Tiempo base en horas
    dificultad: int           # 1-10 (afecta eventos negativos)
    
    # Tiles por los que pasa
    tiles: list               # Lista de coordenadas [(x,y), ...]
    
    # Eventos
    eventos_posibles: list    # Eventos que pueden ocurrir en la ruta
```

#### Cálculo de Distancias

El tiempo de viaje depende de:

1. **Distancia base**: Calculada con A* pathfinding
2. **Tipo de ruta**: Carretera = rápido, Sendero = lento
3. **Biomas atravesados**: Montaña = más lento, Pradera = más rápido
4. **Condiciones**: Clima, estación, hora del día

**Pregunta 5**: ¿Cómo se calculan las distancias?

| Opción | Descripción |
|--------|-------------|
| A | Distancia euclidiana simple (línea recta) |
| B | Pathfinding A* considerando terreno |
| C | Predefinido por el sistema de generación |

---

### 6. Exploración y Revelado

El jugador no ve todo el mapa al inicio. Debe explorar.

#### Estados de Visibilidad

| Estado | Descripción |
|--------|-------------|
| No descubierto | Tile completamente oculto |
| Descubierto | Tile visible pero sin detalles |
| Explorado | Tile visitado, todos los detalles visibles |
| Actual | Tile donde está el jugador ahora |

#### Radio de Visión

```python
class VisionJugador:
    radio_base: int = 3       # Tiles visibles alrededor
    modificadores: dict       # Bonos por habilidades, items, etc.
    
    def calcular_visibles(self, x: int, y: int) -> list:
        # Retorna lista de tiles visibles desde (x, y)
        pass
```

**Pregunta 6**: ¿Cómo funciona el revelado del mapa?

| Opción | Descripción |
|--------|-------------|
| A | Solo se revela el tile actual |
| B | Radio de visión (3-5 tiles alrededor) |
| C | Todo el bioma actual se revela al entrar |
| D | Configurable por dificultad |

---

### 7. Spawn del Jugador

¿Dónde aparece el jugador al inicio?

**Pregunta 7**: ¿Dónde hace spawn el jugador?

| Opción | Descripción |
|--------|-------------|
| A | Ubicación aleatoria (cualquier pueblo/ciudad) |
| B | Siempre en un pueblo seguro |
| C | Ubicación configurada por el jugador |
| D | Zona específica según la historia |

---

### 8. Persistencia del Mapa

#### Datos a Persistir

```json
{
  "mapa": {
    "seed": 12345,
    "tiles_explorados": [
      {"x": 0, "y": 0, "bioma": "bosque", "explorado": true},
      {"x": 1, "y": 0, "bioma": "bosque", "explorado": true}
    ],
    "ubicaciones_conocidas": ["pueblo_1", "ciudad_1"],
    "rutas_conocidas": ["ruta_1", "ruta_2"],
    "posicion_actual": {"x": 5, "y": 3}
  }
}
```

---

## Preguntas para la Primera Iteración

### Pregunta 1: Escala de Tiles
¿Cuál debería ser el tamaño de un tile?

### Pregunta 2: Mundo Infinito vs Limitado
¿El mundo debe ser infinito o tener límites?

### Pregunta 3: Transiciones de Biomas
¿Los biomas deben tener transiciones suaves o bordes definidos?

### Pregunta 4: Cantidad de Ubicaciones
¿Cuántas ubicaciones debería generar el mundo inicial?

### Pregunta 5: Cálculo de Distancias
¿Cómo se calculan las distancias entre ubicaciones?

### Pregunta 6: Revelado del Mapa
¿Cómo funciona el revelado del mapa?

### Pregunta 7: Spawn del Jugador
¿Dónde hace spawn el jugador al inicio?

---

## Estructura de Archivos Propuesta

```
backend/src/systems/
├── mapa.py                # Sistema principal de mapa
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

## Próximos Pasos

1. ⏳ Responder preguntas de esta iteración
2. 🔜 Segunda iteración con más detalle técnico
3. 🔜 Implementación en `experiments/mapa/`
4. 🔜 Tests de validación
5. 🔜 Integración al backend principal