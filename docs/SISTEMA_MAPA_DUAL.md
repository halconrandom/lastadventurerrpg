# Sistema de Mapa Dual: Local vs Mundial

## Concepto General

El sistema de mapa tiene dos modos de visualización que permiten al jugador navegar tanto a nivel macro (viajes largos) como micro (exploración detallada).

---

## Modo Mundial (Macro)

### Escala
- **1 Tile = 1 km²** del mundo
- Grid visible: 13x13 tiles centrados en el jugador
- Cada tile representa una zona general del mundo

### Funcionalidad
- Navegación rápida para viajes largos
- Muestra ubicaciones importantes (pueblos, ciudades, mazmorras, POIs)
- Click en tile adyacente = mover 1 km (consume tiempo/energía)
- Click en ubicación descubierta = viajar automáticamente (si está en rango)

### Visualización
```
? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? · · · ? ? ? ? ? ?
? ? ? · · 🏘️ · · ? ? ? ? ?
? ? ? · · 📍 · · ? ? ? ? ?
? ? ? · · · · · ? ? ? ? ?
? ? ? ? ? ? ? ? ? ? ? ? ?
```

### Leyenda de Iconos
- `📍` - Posición del jugador
- `·` - Tile descubierto
- `?` - Tile no explorado
- `🏘️` - Pueblo
- `🏰` - Ciudad
- `👑` - Capital
- `⚔️` - Mazmorra
- `✨` - Punto de interés (POI)

---

## Modo Local (Micro)

### Escala
- **1 SubTile = 10 metros**
- **1 Tile Mundial = 100 SubTiles (10x10)**
- Grid visible: 13x13 subtiles centrados en el jugador
- Cada subtile representa un área de 10m x 10m

### Funcionalidad
- Exploración detallada de la zona actual
- Búsqueda de recursos, encuentros, secretos
- Cada subtile puede contener:
  - Recursos recolectables
  - Enemigos
  - NPCs
  - Secretos/escondites
  - Puntos de interés menores
  - Entradas a mazmorras

### Generación Procedural
Los 100 subtiles se generan basándose en:
- **Bioma del tile padre** (bosque, desierto, montaña, etc.)
- **Tipo de ubicación** (si hay una ciudad/pueblo)
- **Nivel de peligro** de la zona
- **Recursos disponibles** en el bioma

### Visualización
```
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌲🌿🌿🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌿🌿💎🌿🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌿🌿🌿🌿🌲🌲📍🌲🌲🌲🌲🌲
🌲🌲🌿🌿🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
```

### Leyenda de SubTiles
Por bioma:

**Bosque:**
- `🌲` - Árbol denso
- `🌿` - Vegetación baja
- `🍄` - Hongos/recursos
- `🦌` - Fauna pacífica
- `🐺` - Enemigo

**Desierto:**
- `🏜️` - Arena
- `🌵` - Cactus
- `💀` - Restos
- `💎` - Recursos minerales

**Montaña:**
- `⛰️` - Roca
- `🏔️` - Pico
- `⛏️` - Mina
- `🐉` - Enemigo

**Ciudad/Pueblo:**
- `🏠` - Casa
- `🏪` - Tienda
- `⛪` - Templo
- `🏰` - Edificio importante
- `🚪` - Entrada

---

## Sistema de Navegación

### Controles de Movimiento

#### Modo Mundial
```
    [N]
[W] [·] [E]
    [S]
```
- Botones direccionales para mover 1 tile (1 km)
- Click directo en tile adyacente
- Click en ubicación para viajar

#### Modo Local
```
    [N]
[W] [·] [E]
    [S]
```
- Botones direccionales para mover 1 subtile (10m)
- Click directo en subtile adyacente
- Explorar subtile actual

### Consumo de Recursos
| Acción | Tiempo | Energía |
|--------|--------|---------|
| Mover 1 tile mundial | 1 hora | 5 |
| Mover 1 subtile local | 1 minuto | 1 |
| Viajar a ubicación | Distancia × 1h | Distancia × 3 |
| Explorar subtile | 10 minutos | 2 |

---

## Transición entre Modos

### Toggle Manual
- Botón en el minimapa para cambiar entre Local/Mundial
- Animación de zoom in/out

### Automático
- Al entrar a una ubicación (pueblo, ciudad) → Local
- Al salir de exploración detallada → Mundial
- Al iniciar combate → Local (posicionamiento táctico)

---

## Integración con Exploración

### Flujo de Exploración
1. **Modo Mundial**: Jugador viaja a una zona
2. **Llega al tile**: Puede ver qué hay en general
3. **Cambia a Local**: Explora los 100 subtiles
4. **Encuentra recursos/enemigos**: Interactúa
5. **Agota zona**: Vuelve a Mundial para seguir viaje

### Agotamiento de Zona
- Cada subtile tiene un límite de exploraciones
- Al agotarse, no genera más encuentros
- Se regenera con el tiempo (1 día = 1 exploración recuperada)

---

## Datos Técnicos

### Estructura de Tile Mundial
```python
class Tile:
    x: int
    y: int
    bioma: str
    dificultad: int
    descubierta: bool
    ubicacion_id: Optional[str]
    subtiles: List[List[SubTile]]  # 10x10
```

### Estructura de SubTile
```python
class SubTile:
    x_local: int  # 0-9
    y_local: int  # 0-9
    tipo: str  # terreno, recurso, enemigo, etc.
    explorado: bool
    veces_explorado: int
    contenido: Optional[Dict]
```

### API Endpoints Adicionales
```
GET  /api/mapa/<slot>/local       # Obtener subtiles del tile actual
POST /api/mapa/<slot>/mover-local # Mover dentro de subtiles
GET  /api/mapa/<slot>/subtile     # Info de subtile actual
```

---

## UI del Minimapa

### Layout Propuesto
```
┌─────────────────────────────────┐
│  [Mundial] [Local]    🗺️ Mapa   │
├─────────────────────────────────┤
│                                 │
│      Grid 13x13 (visual)        │
│                                 │
├─────────────────────────────────┤
│         [N]                     │
│      [W] [·] [E]                │
│         [S]                     │
├─────────────────────────────────┤
│  📍 Posición: (X, Y)            │
│  🌲 Bioma: Bosque               │
├─────────────────────────────────┤
│  Ubicaciones Cercanas           │
│  🏘️ Pueblo - 5km               │
│  ⚔️ Mazmorra - 12km            │
└─────────────────────────────────┘
```

### Ancho Recomendado
- **Actual**: 288px (w-72)
- **Propuesto**: 384px (w-96) para mejor visibilidad

---

## Próximos Pasos de Implementación

1. [x] Sistema de tiles mundiales
2. [x] API de mapa mundial
3. [ ] Sistema de subtiles locales
4. [ ] API de mapa local
5. [ ] Toggle Local/Mundial en UI
6. [ ] Botones de movimiento direccional
7. [ ] Generación procedural de subtiles
8. [ ] Integración con sistema de exploración
