# Progreso del Sistema de Combate

## Estado Actual

### ✅ Completado
- [x] Modelo Enemigo (`backend/src/models/enemigo.py`)
- [x] Datos de enemigos (`backend/src/data/enemigos.json`)

### 🔄 En Progreso
- [ ] Sistema de combate (`backend/src/systems/combate.py`) - **INCOMPLETO**

### ⏳ Pendiente
- [ ] API de combate (`backend/src/api/combate.py`)
- [ ] Registrar blueprint en `main.py`
- [ ] Tipos frontend (`frontend/src/lib/types.ts`)
- [ ] Funciones API frontend (`frontend/src/lib/api.ts`)
- [ ] GameContext con estado de combate
- [ ] Hook useCombate
- [ ] Componentes de combate
- [ ] CombatePanel funcional
- [ ] Testing

---

## Notas
- El archivo `combate.py` se cortó en la función `_ejecutar_bloqueo`
- Falta completar: bloqueo, huida, resolver turno enemigo, verificar fin, get_estado