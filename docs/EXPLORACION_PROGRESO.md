# Progreso: Sistema de Exploración Procedural

## Estado General: `EN PROGRESO`

---

## Sistemas a Implementar

| # | Sistema | Estado | Archivos |
|---|---------|--------|----------|
| 1 | Semillas (Seed) | ✅ COMPLETADO | `backend/src/systems/seed.py`, `backend/tests/test_seed.py` |
| 2 | Biomas | ✅ COMPLETADO | `backend/src/systems/biomas.py`, `backend/tests/test_biomas.py` |
| 3 | Zonas y Tiles | ✅ COMPLETADO | `backend/src/systems/zonas.py`, `backend/tests/test_zonas.py` |
| 4 | Generador de Nombres | ✅ COMPLETADO | `backend/src/systems/nombres.py`, `backend/tests/test_nombres.py` |
| 5 | Eventos de Exploración | ✅ COMPLETADO | `backend/src/systems/eventos.py`, `backend/tests/test_eventos.py` |
| 6 | Clima Dinámico | ✅ COMPLETADO | `backend/src/systems/clima.py`, `backend/tests/test_clima.py` |
| 7 | API Endpoints | ✅ COMPLETADO | `backend/src/api/exploracion.py`, `backend/tests/test_api_exploracion.py` |
| 8 | Frontend Panel | ✅ COMPLETADO | `frontend/src/components/juego/panels/ExplorarPanel.tsx`, `frontend/src/hooks/useExploracion.ts` |
| 9 | Persistencia | ⏳ PENDIENTE | - |

---

## Decisiones Tomadas

| Aspecto | Decisión |
|---------|----------|
| Visualización | Solo texto descriptivo |
| Encuentros hostiles | Esperar a sistema de combate |
| Persistencia | Semilla + zonas descubiertas + cambios |
| Nombres | Únicos siempre (procedurales) |

---

## Sistema 1: Semillas (Seed)

### Objetivo
Crear un sistema determinista donde misma semilla = mismo mundo.

### Archivos creados
- `backend/src/systems/seed.py` - Clase WorldSeed
- `backend/tests/test_seed.py` - Tests del sistema (9 tests, todos pasan)

### Funcionalidades implementadas
- [x] Generar semilla aleatoria
- [x] Crear semilla desde string
- [x] Generar sub-seeds para diferentes sistemas
- [x] RNG independiente por contexto
- [x] Helpers: get_int, get_choice, get_float, get_weighted_choice
- [x] Serializacion (to_dict / from_dict)
- [x] Semilla global (init_global_seed, get_global_seed, set_global_seed)

### Tests
```
[OK] Semillas aleatorias son unicas
[OK] Semilla desde string funciona
[OK] Determinismo verificado
[OK] Contextos son independientes
[OK] Sub-seeds unicas
[OK] Helpers funcionan correctamente
[OK] Serializacion funciona correctamente
[OK] Semilla global funciona correctamente
[OK] Partida reproducible
```

### Estado: `✅ COMPLETADO`

---

## Sistema 2: Biomas

### Objetivo
Crear sistema de biomas procedurales con variaciones unicas.

### Archivos creados
- `backend/src/systems/biomas.py` - Clase BiomaGenerator y Bioma
- `backend/tests/test_biomas.py` - Tests del sistema (10 tests, todos pasan)

### Funcionalidades implementadas
- [x] 6 biomas base definidos
- [x] Variaciones unicas por bioma (encantado, corrupto, maldito, etc.)
- [x] Clima, recursos, fauna, peligros, eventos
- [x] Nombres procedurales unicos
- [x] Descripciones dinamicas
- [x] Serializacion

### Tests
```
[OK] Bioma generado: Aquellos Bosques Marchitos
[OK] Determinismo verificado
[OK] Generados 9 biomas con variedad
[OK] Bioma tiene contenido completo
[OK] Variaciones encontradas: infernal, sagrado, maldito, olvidado...
[OK] Nombre unico: Las Pantanos Ardientes
[OK] Descripcion generada correctamente
[OK] Serializacion correcta
[OK] Coordenadas correctas
[OK] Todos los biomas disponibles
```

### Estado: `✅ COMPLETADO`

---

## Sistema 3: Zonas y Tiles

### Objetivo
Crear sistema de zonas explorables con tiles procedurales.

### Archivos creados
- `backend/src/systems/zonas.py` - Clases Zona, Tile, Entidad, PuntoInteres
- `backend/tests/test_zonas.py` - Tests del sistema (12 tests, todos pasan)

### Funcionalidades implementadas
- [x] Zonas con tamaño variable (15-30 tiles)
- [x] Tiles con terreno y propiedades
- [x] Tiles especiales (tesoro, trampa, secreto, evento, rareza)
- [x] Entidades hostiles y neutrales
- [x] Nivel de entidades por distancia al centro
- [x] Puntos de interes (POI) por bioma
- [x] Sistema de exploracion con descubrimientos
- [x] Estados de zona (inexplorada, explorando, agotada)
- [x] Serializacion completa

### Tests
```
[OK] Zona generada con tamaño variable
[OK] Tiles generados correctamente
[OK] Entidades hostiles y neutrales
[OK] POIs por bioma
[OK] Determinismo verificado
[OK] Exploracion descubre tiles
[OK] Estados de zona funcionan
[OK] Serializacion correcta
[OK] Tiles especiales encontrados
[OK] Niveles escalan con distancia
[OK] POIs se descubren al explorar
[OK] Encuentros generados
```

### Estado: `✅ COMPLETADO`

---

## Sistema 4: Generador de Nombres

### Objetivo
Crear sistema de nombres procedurales para NPCs, lugares y objetos.

### Archivos creados
- `backend/src/systems/nombres.py` - Clase NombreGenerator
- `backend/tests/test_nombres.py` - Tests del sistema (13 tests, todos pasan)

### Funcionalidades implementadas
- [x] Nombres para NPCs (masculino/femenino)
- [x] Apellidos procedurales
- [x] Titulos y apodos (positivos/negativos)
- [x] Nombres para lugares (4 estructuras diferentes)
- [x] Nombres para objetos (con tipo y adjetivo)
- [x] Nombres para enemigos (con prefijos)
- [x] Nombres por silabas (procedural puro)
- [x] Determinismo garantizado

### Tests
```
[OK] NPC masculino: Garrick Kingsley
[OK] NPC femenino: Penelope Lockwood
[OK] Con titulo positivo: Percival Mercer, el Piadoso
[OK] Con titulo negativo: Valentina Ashford, el Despiadado
[OK] Lugar: Valle Sagrado del Fin
[OK] Objeto: Casco Antiguo
[OK] Enemigo con prefijo: Guardian Troll
[OK] Determinismo verificado
[OK] 20 nombres unicos generados
```

### Estado: `✅ COMPLETADO`

---

## Sistema 5: Eventos de Exploracion

### Objetivo
Crear sistema de eventos aleatorios durante la exploracion.

### Archivos creados
- `backend/src/systems/eventos.py` - Clase EventoGenerator y Evento
- `backend/tests/test_eventos.py` - Tests del sistema (12 tests, todos pasan)

### Funcionalidades implementadas
- [x] 10 eventos base definidos
- [x] Tipos: encuentro_npc, descubrimiento, peligro, mistico, tesoro
- [x] Eventos con 3 opciones cada uno
- [x] Recompensas y consecuencias
- [x] Rarezas: comun, raro, epico, legendario
- [x] Filtrado por bioma
- [x] Sistema de resolucion de eventos
- [x] Serializacion

### Tests
```
[OK] Evento generado: Ruinas Antiguas
[OK] Evento tiene 3 opciones validas
[OK] Evento resuelto: exito
[OK] Eventos por bioma funcionan
[OK] Eventos por tipo funcionan
[OK] Determinismo verificado
[OK] Rarezas: comun, raro, epico, legendario
[OK] Recompensas y consecuencias funcionan
```

### Estado: `✅ COMPLETADO`

---

## Sistema 6: Clima Dinamico

### Objetivo
Crear sistema de clima dinamico que afecta la exploracion.

### Archivos creados
- `backend/src/systems/clima.py` - Clase ClimaGenerator, EstadoClima, CicloDiaNoche
- `backend/tests/test_clima.py` - Tests del sistema (12 tests, todos pasan)

### Funcionalidades implementadas
- [x] Clima por bioma (6 biomas con climas unicos)
- [x] 30+ tipos de clima definidos
- [x] Intensidades: leve, moderado, intenso, extremo
- [x] Efectos del clima (visibilidad, movimiento)
- [x] Ciclo dia/noche (6 fases)
- [x] Efectos combinados clima + ciclo
- [x] Transiciones de clima
- [x] Serializacion

### Tests
```
[OK] Clima generado: soleado (moderado)
[OK] Clima por bioma funciona
[OK] Ciclo dia/noche: madrugada, dia, noche
[OK] Avanzar hora funciona
[OK] Efectos combinados calculados
[OK] Efectos de noche agregados
[OK] Determinismo verificado
[OK] Intensidades: leve, moderado, intenso, extremo
[OK] Transiciones de clima
```

### Estado: `✅ COMPLETADO`

---

## Sistema 7: API Endpoints

### Objetivo
Crear endpoints de API para conectar frontend con sistemas de exploracion.

### Archivos creados
- `backend/src/api/exploracion.py` - Blueprint Flask con endpoints
- `backend/src/api/__init__.py` - Modulo API
- `backend/tests/test_api_exploracion.py` - Tests de API (10 tests, todos pasan)

### Funcionalidades implementadas
- [x] POST /api/exploracion/iniciar - Inicia exploracion en zona
- [x] GET /api/exploracion/zona/<x>/<y> - Obtiene info de zona
- [x] POST /api/exploracion/explorar - Ejecuta accion de exploracion
- [x] GET /api/exploracion/clima/<x>/<y> - Obtiene clima actual
- [x] GET /api/exploracion/evento - Obtiene evento aleatorio
- [x] POST /api/exploracion/evento/resolver - Resuelve evento
- [x] POST /api/exploracion/seed - Establece semilla
- [x] GET /api/exploracion/seed - Obtiene semilla actual
- [x] Cache de zonas en memoria
- [x] Determinismo garantizado

### Tests
```
[OK] Endpoint iniciar: Exploracion iniciada
[OK] Endpoint zona: zona obtenida
[OK] Endpoint explorar: tiles descubiertos
[OK] Endpoint clima: clima obtenido
[OK] Endpoint evento: evento generado
[OK] Endpoint resolver: evento resuelto
[OK] Endpoint seed POST/GET
[OK] Determinismo API verificado
```

### Estado: `✅ COMPLETADO`

---

## Sistema 8: Frontend Panel

### Objetivo
Crear panel de exploracion en el frontend para mostrar zona, clima y eventos.

### Archivos creados
- `frontend/src/components/juego/panels/ExplorarPanel.tsx` - Panel actualizado
- `frontend/src/hooks/useExploracion.ts` - Hook para API
- `frontend/src/hooks/index.ts` - Export del hook

### Funcionalidades implementadas
- [x] Mostrar zona actual con nombre y bioma
- [x] Mostrar clima y ciclo dia/noche con iconos
- [x] Boton de explorar con estados
- [x] Modal de eventos con opciones
- [x] Modal de resultado de evento
- [x] Log de exploracion
- [x] Integracion con API de exploracion
- [x] Tipos TypeScript para zona, clima, evento

### Tests
```
[OK] Frontend compila sin errores
[OK] Hook useExploracion implementado
[OK] Panel conectado a API
[OK] Modales de eventos funcionales
```

### Estado: `✅ COMPLETADO`

---

## Sistema 9: Persistencia

### Objetivo
Guardar estado de exploracion en el save del jugador.

### Archivos a crear/modificar
- `backend/src/systems/save_manager.py` - Modificar para incluir exploracion
- `backend/src/systems/exploracion_state.py` - Estado de exploracion

### Funcionalidades
- [ ] Guardar semilla del mundo
- [ ] Guardar zonas descubiertas
- [ ] Guardar estado de zonas (veces exploradas)
- [ ] Cargar estado al iniciar partida

### Estado: `⏳ PENDIENTE`
