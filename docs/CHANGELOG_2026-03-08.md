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