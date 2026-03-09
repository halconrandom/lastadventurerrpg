# Changelog - 8 de Marzo de 2026

## Sesión: Corrección de API de Exploración

### Problema Identificado
Error CORS en `/api/exploracion/explorar` causado por Error 500 interno en el backend.

### Causas Raíz
1. **Frontend (`useExploracion.ts`)**: Extraía coordenadas de `bioma.key` (ej: "bosque_ancestral") en lugar de usar coordenadas reales. `parseInt("bosque")` retornaba `NaN`.
2. **Backend (`api/exploracion.py`)**: Sin manejo de errores, cualquier excepción causaba Error 500 silencioso.
3. **Import incorrecto (`src/main.py`)**: Función `crear_personaje` no existía, era `crear_nuevo_personaje`.

### Cambios Realizados

#### Frontend
- **Archivo**: `frontend/src/hooks/useExploracion.ts`
- **Cambios**:
  - Agregado estado `coordenadas: { x: number; y: number }` al hook
  - `iniciarExploracion(x, y)` ahora guarda las coordenadas en el estado
  - `explorar()` usa `state.coordenadas` en lugar de parsear `bioma.key`

#### Backend
- **Archivo**: `backend/src/api/exploracion.py`
- **Cambios**:
  - Agregado `import traceback` y `logging`
  - Endpoints `iniciar_exploracion`, `ejecutar_exploracion`, `obtener_evento`, `resolver_evento` ahora tienen bloques try/except
  - Errores se loguean y devuelven mensajes claros (status 500 con mensaje descriptivo)

- **Archivo**: `backend/src/main.py`
- **Cambios**:
  - Corregido import: `crear_personaje` → `crear_nuevo_personaje`

### Verificación
```
Testing /api/exploracion/iniciar...
Status: 200
Success: True
Zona: Los Paramos Perdidos
Bioma: Ruinas Subterraneas

Testing /api/exploracion/explorar...
Status: 200
Success: True
Zona: Los Paramos Perdidos
Tiles descubiertos: 5
```

### Archivos Modificados
- `frontend/src/hooks/useExploracion.ts`
- `backend/src/api/exploracion.py`
- `backend/src/main.py`

### Estado del Proyecto
- Exploración: ✅ Funcional
- Combate: ✅ Funcional
- Guardado: ✅ Funcional
- Personaje: ✅ Funcional

### Próximos Pasos Discutidos
- Crear carpeta `experiments/` como playground para nuevos sistemas
- Sistemas pendientes: Mapa, Tiempo, NPCs, Relaciones, LLM

---

## Sesión: Documentación de Sistemas (Tiempo y Mapa)

### SISTEMA_TIEMPO.md - Completado

**Decisiones finales:**
- Escala: 2 min real = 1 hora juego (48 min = 1 día)
- Estaciones: 4 estaciones de 30 días con variación por bioma
- Avance: Por acción (no tiempo real)
- Tiempo inicial: Aleatorio (safe start, siempre de día)
- Pausas: Total (combate, diálogos, menús)
- Costos de tiempo: 5 min moverse, 15 min explorar, 1-8 horas viajes
- Dependencia: Requiere sistema de mapa para distancias

### SISTEMA_MAPA.md - Completado

**Decisiones finales:**
- Escala: 1 tile = 1 km² = 1 hora de viaje
- Mundo: Infinito con chunks (1 chunk = 9 tiles, 30 chunks cargados)
- Transiciones: Suaves (Perlin noise)
- Ubicaciones: 10-20 pueblos, 3-5 ciudades, 1-2 capitales, 20-40 mazmorras, 30-50 POIs
- Distancias: Pathfinding A* considerando terreno
- Revelado: 3 tiles alrededor
- Spawn: Ubicación aleatoria (pueblo/ciudad)
- **Sub-tiles**: 1 tile = 100 sub-tiles (10x10), cada sub-tile = 100m = 10 min viaje

### Integración Tiempo + Mapa

| Nivel | Escala | Tiempo de Viaje |
|-------|--------|-----------------|
| Tile macro | 1 km | 1 hora |
| Sub-tile | 100 m | 10 minutos |

### Archivos Creados/Modificados
- `docs/SISTEMA_TIEMPO.md` - Documento finalizado
- `docs/SISTEMA_MAPA.md` - Documento finalizado
- `experiments/README.md` - Playground para prototipos

### Commits Realizados
- `63a39ca` - SISTEMA_TIEMPO.md finalizado
- `4dd345c` - SISTEMA_MAPA.md primera iteración
- `1b464ea` - SISTEMA_MAPA.md segunda iteración
- `37d7034` - SISTEMA_MAPA.md finalizado con sub-tiles

### Próximos Pasos
1. ~~Implementar sistema de mapa en `experiments/mapa/`~~ ✅ Completado
2. Implementar sistema de tiempo en `experiments/tiempo/`
3. Documentar sistema de NPCs
4. Documentar sistema de Relaciones
5. Documentar sistema de LLM

---

## Sesión: Implementación del Sistema de Mapa

### Resumen
Implementación completa del sistema de mapa global en `experiments/mapa/` siguiendo la documentación de `SISTEMA_MAPA.md`.

### Archivos Creados

| Archivo | Descripción |
|---------|-------------|
| `experiments/mapa/__init__.py` | Exports del módulo |
| `experiments/mapa/tile.py` | Sistema de tiles (1 km²) y sub-tiles (100m) |
| `experiments/mapa/chunk.py` | Gestión de chunks (3x3 tiles) con carga/descarga |
| `experiments/mapa/ubicacion.py` | Ubicaciones: pueblos, ciudades, capitales, mazmorras, POIs |
| `experiments/mapa/ruta.py` | Rutas entre ubicaciones con A* pathfinding |
| `experiments/mapa/mapa.py` | Clase principal `MapaMundo` que integra todo |
| `experiments/mapa/cartografia.py` | Habilidad de cartografía y mapas como items |
| `experiments/mapa/demo.py` | Demo interactivo para probar el sistema |
| `experiments/mapa/tests/test_mapa.py` | Tests completos (7/7 pasados) |

### Características Implementadas

**Sistema de Tiles:**
- Tiles de 1 km² con biomas y tipos de terreno
- Estados de visibilidad: no_descubierto, descubierto, explorado, actual
- Costos de movimiento por terreno (carretera: 0.8x, montaña: 2.5x)
- Sub-tiles 10x10 para ubicaciones (100m cada uno)

**Sistema de Chunks:**
- Chunks de 3x3 tiles (9 km²)
- Carga dinámica de chunks cercanos al jugador (radio 30)
- Descarga de chunks lejanos para optimizar memoria

**Sistema de Ubicaciones:**
- 5 tipos: pueblo, ciudad, capital, mazmorra, poi
- Generación procedural de nombres únicos
- Tamaños variables según tipo (pueblo: 5x5, capital: 10x10)
- Servicios y NPCs configurables

**Sistema de Rutas:**
- 6 tipos: camino, sendero, carretera, río, marítima, secreta
- Cálculo de tiempo de viaje basado en distancia y terreno
- Dificultad variable (1-10) para eventos de viaje

**Sistema de Cartografía:**
- 8 niveles de habilidad (Novato → Legendario)
- Mapas como items con tipos y calidades
- Experiencia por explorar y descubrir
- Revelado progresivo del mapa

### Tests Ejecutados
```
Total: 7/7 tests pasados
- Tiles: ✅
- Chunks: ✅
- Ubicaciones: ✅
- Rutas: ✅
- Mapa Mundial: ✅
- Cartografía: ✅
- Integración: ✅
```

### Demo Interactivo
```bash
python experiments/mapa/demo.py
```
Comandos: WASD (mover), E (explorar), M (mapa), U (ubicaciones), I (inventario), C (crear mapa), V (usar mapa), T (teleportar)

### Integración Pendiente
El sistema usa `MockSeed` para tests. Para integrar con el backend:
```python
from backend.src.systems.seed import WorldSeed
from experiments.mapa import MapaMundo

seed = WorldSeed(semilla=12345)
mapa = MapaMundo(seed=seed)
mapa.generar_mundo_inicial()
```

### Commit
- `6e0200f` - feat: Implementar sistema de mapa global en experiments/mapa/