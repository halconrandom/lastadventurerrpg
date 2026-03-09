# Last Adventurer - Roadmap

## Visión del Proyecto
RPG para navegador con narrativa procedural generada por LLM local, mundo persistente y simulación profunda.

---

## Estado Actual: Fase 1 - Fundamentos

### Progreso General
```
[████░░░░░░░░░░░░░░░░] 20%
```

---

## Sistemas Documentados (Completados)

| Sistema | Archivo | Estado | Descripción |
|---------|---------|--------|-------------|
| Combate | `SISTEMA_COMBATE.md` | Documentado | Sistema de combate por turnos con habilidades y perks |
| Enemigos | `SISTEMA_ENEMIGOS.md` | Documentado | Generación procedural de enemigos con modificadores |
| Items | `SISTEMA_ITEMS.md` | Documentado | Sistema de items con rareza y stats |
| Inventario | `SISTEMA_INVENTARIO.md` | Documentado | Gestión de inventario con límites y equipamiento |
| Stats | `SISTEMA_STATS.md` | Documentado | Sistema de estadísticas del personaje |
| Experiencia | `SISTEMA_EXPERIENCIA.md` | Documentado | Sistema de nivel y progresión |
| Perks | `SISTEMA_PERKS.md` | Documentado | Habilidades pasivas y activas |
| Creación Personaje | `SISTEMA_CREACION_PERSONAJE.md` | Documentado | Sistema de creación de personaje |
| Durabilidad | `SISTEMA_DURABILIDAD.md` | Documentado | Sistema de desgaste de items |
| Rareza | `SISTEMA_RAREZA.md` | Documentado | Sistema de rareza de items |
| Crafteo | `SISTEMA_CRAFTEO.md` | Documentado | Sistema de crafteo de items |
| Misiones | `SISTEMA_MISIONES.md` | Documentado | Sistema de misiones |
| Guardado | `SISTEMA_GUARDADO.md` | Documentado | Sistema de guardado en JSON |
| Exploración | `SISTEMA_EXPLORACION.md` | Documentado | Sistema de exploración procedural |
| Historia | `SISTEMA_HISTORIA.md` | Documentado | Sistema de narrativa persistente |

---

## Sistemas Pendientes (Por Documentar)

### Alta Prioridad - Fundamentos del Mundo

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 1 | **SISTEMA_MAPA.md** | Tiles con coordenadas X/Y, mundo infinito, generación procedural, biomas | Ninguna |
| 2 | **SISTEMA_TIEMPO.md** | Día/noche, estaciones, tiempo transcurrido, configuración inicial aleatoria | Ninguna |
| 3 | **SISTEMA_NPCS.md** | NPCs con memoria total, personalidad, comportamiento, rutinas | Tiempo, Mapa |
| 4 | **SISTEMA_RELACIONES.md** | Reputación numérica (-100 a +100), estados (Enemigo/Neutral/Aliado), red de relaciones entre NPCs, relaciones complejas (familia, romance, rivalidad) | NPCs |
| 5 | **SISTEMA_LLM.md** | Llama 3.2 3B con LoRA, fine-tuning para RPG, fallback con error | Ninguna |

### Media Prioridad - Simulación

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 6 | **SISTEMA_MUNDO.md** | Eventos globales que avanzan sin el jugador (guerras, facciones, cambios), consecuencias retardadas | Mapa, Tiempo, NPCs |
| 7 | **SISTEMA_PROPAGACION.md** | Propagación de información por rutas y proximidad, sistema de rumores | Mapa, NPCs, Relaciones |
| 8 | **SISTEMA_CONSECUENCIAS.md** | Cadenas de consecuencias, eventos retardados, cambios en el mundo | Historia, Mundo |

### Baja Prioridad - Expansión

| # | Sistema | Descripción | Dependencias |
|---|---------|-------------|--------------|
| 9 | **SISTEMA_CONSTRUCCION.md** | Construir/comprar casas, mejoras, ubicación libre | Mapa, Inventario |
| 10 | **SISTEMA_FACCIONES.md** | Facciones con relaciones dinámicas, guerras, alianzas | Relaciones, Mundo |
| 11 | **SISTEMA_ECONOMIA.md** | Economía dinámica, precios variables, oferta/demanda | Mapa, Tiempo |

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

### Fase 1: Fundamentos (Actual)
- [x] Documentar sistemas base (combate, items, stats)
- [x] Documentar sistema de historia
- [ ] Crear SISTEMA_MAPA.md
- [ ] Crear SISTEMA_TIEMPO.md
- [ ] Crear SISTEMA_NPCS.md
- [ ] Crear SISTEMA_RELACIONES.md
- [ ] Crear SISTEMA_LLM.md

### Fase 2: Implementación Backend
- [ ] Configurar entorno Python/FastAPI
- [ ] Implementar sistema de guardado
- [ ] Implementar sistema de mapa
- [ ] Implementar sistema de NPCs
- [ ] Implementar sistema de relaciones
- [ ] Integrar LLM

### Fase 3: Implementación Frontend
- [ ] Configurar React/Next.js
- [ ] Implementar UI de exploración
- [ ] Implementar UI de combate
- [ ] Implementar UI de inventario
- [ ] Implementar UI de NPCs/relaciones

### Fase 4: Integración y Polish
- [ ] Conectar frontend con backend
- [ ] Implementar sistema de historia
- [ ] Testing y balanceo
- [ ] Optimización

---

## Stack Tecnológico Decidido

### Backend
- **Lenguaje**: Python 3.11+
- **Framework**: FastAPI
- **Base de datos**: JSON files (para prototipo) → SQLite/PostgreSQL (producción)
- **LLM**: Llama 3.2 3B con Ollama/vLLM

### Frontend
- **Framework**: Next.js 16
- **Estilos**: Tailwind CSS
- **Estado**: React Context / Zustand

### Infraestructura
- **Hosting**: VPS propia
- **LLM**: Hosteada en VPS

---

## Próximos Pasos Inmediatos

1. **Crear SISTEMA_LLM.md** - Guía de instalación de Llama 3.2 3B
2. **Crear SISTEMA_MAPA.md** - Estructura del mundo
3. **Crear SISTEMA_TIEMPO.md** - Reloj del mundo
4. **Crear SISTEMA_NPCS.md** - NPCs y su comportamiento
5. **Crear SISTEMA_RELACIONES.md** - Sistema de relaciones complejas

---

## Notas de Desarrollo

- Cada sistema debe ser documentado antes de implementarse
- Los commits deben ser frecuentes
- Testing manual en cada paso
- El usuario escribe el código con guía