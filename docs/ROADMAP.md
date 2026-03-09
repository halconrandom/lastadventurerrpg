# Last Adventurer - Roadmap

## Visión del Proyecto
RPG para navegador con narrativa procedural generada por LLM local, mundo persistente y simulación profunda.

---

## Estado Actual: Fase 2 - Implementación Backend

### Progreso General
```
[████████░░░░░░░░░░░░] 40%
```

---

## Sistemas Documentados (Completados)

| Sistema | Archivo | Estado | Descripción |
|---------|---------|--------|-------------|
| Combate | `SISTEMA_COMBATE.md` | ✅ Documentado | Sistema de combate por turnos con habilidades y perks |
| Enemigos | `SISTEMA_ENEMIGOS.md` | ✅ Documentado | Generación procedural de enemigos con modificadores |
| Items | `SISTEMA_ITEMS.md` | ✅ Documentado | Sistema de items con rareza y stats |
| Inventario | `SISTEMA_INVENTARIO.md` | ✅ Documentado | Gestión de inventario con límites y equipamiento |
| Stats | `SISTEMA_STATS.md` | ✅ Documentado | Sistema de estadísticas del personaje |
| Experiencia | `SISTEMA_EXPERIENCIA.md` | ✅ Documentado | Sistema de nivel y progresión |
| Perks | `SISTEMA_PERKS.md` | ✅ Documentado | Habilidades pasivas y activas |
| Creación Personaje | `SISTEMA_CREACION_PERSONAJE.md` | ✅ Documentado | Sistema de creación de personaje |
| Durabilidad | `SISTEMA_DURABILIDAD.md` | ✅ Documentado | Sistema de desgaste de items |
| Rareza | `SISTEMA_RAREZA.md` | ✅ Documentado | Sistema de rareza de items |
| Crafteo | `SISTEMA_CRAFTEO.md` | ✅ Documentado | Sistema de crafteo de items |
| Misiones | `SISTEMA_MISIONES.md` | ✅ Documentado | Sistema de misiones |
| Guardado | `SISTEMA_GUARDADO.md` | ✅ Documentado | Sistema de guardado en JSON |
| Exploración | `SISTEMA_EXPLORACION.md` | ✅ Documentado | Sistema de exploración procedural |
| Historia | `SISTEMA_HISTORIA.md` | ✅ Documentado | Sistema de narrativa persistente |
| Mapa | `SISTEMA_MAPA.md` | ✅ Documentado | Sistema de mapa procedural |
| Tiempo | `SISTEMA_TIEMPO.md` | ✅ Documentado | Sistema de tiempo y clima |
| LLM | `SISTEMA_LLM.md` | ✅ Documentado | Integración con Llama 3.2 3B |
| Relaciones | `SISTEMA_RELACIONES.md` | ✅ Documentado | Sistema de relaciones y reputación |

---

## Sistemas Pendientes (Por Documentar)

### Alta Prioridad

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 1 | **SISTEMA_NPCS.md** | NPCs con memoria total, personalidad, comportamiento, rutinas | Tiempo, Mapa |

### Media Prioridad

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 2 | **SISTEMA_MUNDO.md** | Eventos globales que avanzan sin el jugador | Mapa, Tiempo, NPCs |
| 3 | **SISTEMA_PROPAGACION.md** | Propagación de información por rutas y proximidad | Mapa, NPCs, Relaciones |
| 4 | **SISTEMA_CONSECUENCIAS.md** | Cadenas de consecuencias, eventos retardados | Historia, Mundo |

### Baja Prioridad

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 5 | **SISTEMA_CONSTRUCCION.md** | Construir/comprar casas, mejoras | Mapa, Inventario |
| 6 | **SISTEMA_FACCIONES.md** | Facciones con relaciones dinámicas | Relaciones, Mundo |
| 7 | **SISTEMA_ECONOMIA.md** | Economía dinámica, precios variables | Mapa, Tiempo |

---

## Implementación Backend (En Progreso)

### Completado

| Componente | Archivo | Estado | Descripción |
|------------|---------|--------|-------------|
| Servidor Flask | `main.py` | ✅ Implementado | API REST con CORS |
| Save Manager | `systems/save_manager.py` | ✅ Implementado | 5 slots de guardado en JSON |
| Modelo Personaje | `models/personaje.py` | ✅ Implementado | Stats, nivel, experiencia |
| Modelo Enemigo | `models/enemigo.py` | ✅ Implementado | Stats, habilidades, drops |
| Modelo Stats | `models/stats.py` | ✅ Implementado | HP, ATK, DEF, velocidad, etc. |
| Sistema Combate | `systems/combate.py` | ✅ Implementado | Combate por turnos completo |
| Sistema Exploración | `api/exploracion.py` | ✅ Implementado | Exploración procedural |
| Generador Biomas | `systems/biomas.py` | ✅ Implementado | Biomas procedurales |
| Generador Zonas | `systems/zonas.py` | ✅ Implementado | Zonas con POIs |
| Generador Clima | `systems/clima.py` | ✅ Implementado | Clima dinámico |
| Generador Eventos | `systems/eventos.py` | ✅ Implementado | Eventos de exploración |
| Semilla Mundial | `systems/seed.py` | ✅ Implementado | Mundo reproducible |
| API Combate | `api/combate.py` | ✅ Implementado | Endpoints de combate |
| API Exploración | `api/exploracion.py` | ✅ Implementado | Endpoints de exploración |
| API Mapa | `api/mapa.py` | ✅ Implementado | Endpoints de mapa |

### Pendiente

| Componente | Descripción | Prioridad |
|------------|-------------|-----------|
| Sistema NPCs | Gestión de NPCs y memoria | Alta |
| Sistema Relaciones | Reputación y relaciones | Alta |
| Sistema LLM | Integración con Ollama | Media |
| Sistema Misiones | Misiones procedurales | Media |
| Sistema Items | Items y drops | Media |
| Sistema Inventario | Gestión de inventario | Media |

---

## Implementación Frontend (En Progreso)

### Completado

| Componente | Archivo | Estado | Descripción |
|------------|---------|--------|-------------|
| Next.js Setup | `package.json` | ✅ Configurado | Next.js 16 + React 19 |
| Tailwind CSS | `package.json` | ✅ Configurado | Tailwind v4 |
| shadcn/ui | `package.json` | ✅ Configurado | Componentes UI |
| Framer Motion | `package.json` | ✅ Configurado | Animaciones |
| Página Inicio | `app/page.tsx` | ✅ Implementado | Menú principal |
| Página Nueva Partida | `app/nueva-partida/` | ✅ Implementado | Creación de personaje |
| Página Juego | `app/juego/` | ✅ Implementado | Interfaz de juego |
| Providers | `app/providers.tsx` | ✅ Implementado | Context providers |
| Layout | `app/layout.tsx` | ✅ Implementado | Layout principal |

### Pendiente

| Componente | Descripción | Prioridad |
|------------|-------------|-----------|
| UI Combate | Interfaz de combate | Alta |
| UI Exploración | Interfaz de exploración | Alta |
| UI Inventario | Gestión de inventario | Media |
| UI Personaje | Stats y equipamiento | Media |
| UI NPCs | Diálogos y relaciones | Baja |
| UI Mapa | Visualización del mundo | Baja |

---

## Datos del Juego

### Completado

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `enemigos.json` | ✅ 140 enemigos | Catálogo completo de enemigos |
| `arquetipos.json` | ✅ Implementado | Arquetipos de personaje |
| `items.json` | ✅ Implementado | Catálogo de items |

### Pendiente

| Archivo | Descripción | Prioridad |
|---------|-------------|-----------|
| `npcs.json` | Datos de NPCs | Alta |
| `facciones.json` | Datos de facciones | Media |
| `misiones.json` | Misiones base | Media |
| `habilidades.json` | Habilidades y perks | Media |

---

## Decisiones Clave del Proyecto

### Narrativa y Mundo
- **Tono**: D&D con toques oscuros y lore profundo
- **Voz narrativa**: Omnisciente pero limitada en información
- **Generación de texto**: LLM local (Llama 3.2 3B) con LoRA
- **Temperatura LLM**: Media (0.6-0.7)
- **Fallback LLM**: Mostrar error y pausar el juego

### Mundo y Exploración
- **Mapa**: Tiles con coordenadas X/Y, mundo infinito
- **Fast travel**: No, exploración a pie obligatoria
- **Inicio**: Spawn aleatorio, no hub fijo
- **Tiempo**: Día/noche + estaciones + tiempo transcurrido

### Persistencia y Memoria
- **Persistencia**: TODO se guarda permanentemente
- **Memoria de NPCs**: Total, recuerdan todo
- **Mundo dinámico**: Sí, cambia sin intervención del jugador
- **Consecuencias**: Retardadas pero consistentes, irreversibles

### Relaciones
- **Reputación**: Sistema híbrido (numérico + estados)
- **Relaciones NPCs**: Muy profundo (familia, amistad, romance, rivalidad)
- **Red de NPCs**: A es enemigo de B → si ayudas a A, B te odia
- **Propagación**: Por rutas y proximidad

---

## Fases de Desarrollo

### Fase 1: Fundamentos ✅ COMPLETADA
- [x] Documentar sistemas base (combate, items, stats)
- [x] Documentar sistema de historia
- [x] Crear SISTEMA_MAPA.md
- [x] Crear SISTEMA_TIEMPO.md
- [x] Crear SISTEMA_LLM.md
- [x] Crear SISTEMA_RELACIONES.md

### Fase 2: Implementación Backend 🔄 EN PROGRESO
- [x] Configurar entorno Python/Flask
- [x] Implementar sistema de guardado
- [x] Implementar sistema de mapa procedural
- [x] Implementar sistema de combate
- [x] Implementar sistema de exploración
- [ ] Implementar sistema de NPCs
- [ ] Implementar sistema de relaciones
- [ ] Integrar LLM
- [ ] Implementar sistema de items/inventario

### Fase 3: Implementación Frontend 🔄 EN PROGRESO
- [x] Configurar React/Next.js
- [x] Implementar página de inicio
- [x] Implementar creación de personaje
- [x] Implementar layout base del juego
- [ ] Implementar UI de exploración
- [ ] Implementar UI de combate
- [ ] Implementar UI de inventario
- [ ] Implementar UI de NPCs/relaciones

### Fase 4: Integración y Polish ⏳ PENDIENTE
- [ ] Conectar frontend con backend
- [ ] Implementar sistema de historia
- [ ] Testing y balanceo
- [ ] Optimización

---

## Stack Tecnológico

### Backend
- **Lenguaje**: Python 3.11+
- **Framework**: Flask
- **Base de datos**: JSON files (prototipo) → SQLite/PostgreSQL (producción)
- **LLM**: Llama 3.2 3B con Ollama/vLLM

### Frontend
- **Framework**: Next.js 16
- **React**: 19.2.3
- **Estilos**: Tailwind CSS v4
- **Componentes**: shadcn/ui
- **Animaciones**: Framer Motion
- **Estado**: React Context

### Infraestructura
- **Hosting**: VPS propia
- **LLM**: Hosteada en VPS

---

## Próximos Pasos Inmediatos

1. **Crear SISTEMA_NPCS.md** - Último sistema de alta prioridad pendiente
2. **Implementar NPCs en backend** - Clases y API
3. **Implementar sistema de relaciones** - Conectar con NPCs
4. **Integrar LLM** - Conectar con Ollama
5. **Completar UI de juego** - Exploración y combate

---

## Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| Sistemas documentados | 19/26 (73%) |
| Backend implementado | ~60% |
| Frontend implementado | ~40% |
| Enemigos en catálogo | 140 |
| Progreso general | ~40% |

---

*Roadmap actualizado - 9 de marzo de 2026*
