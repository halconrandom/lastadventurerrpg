# Sistema de NPCs - Last Adventurer

## VisiÃ³n General

El **Sistema de NPCs** es el nÃºcleo de simulaciÃ³n social del juego. Define cÃ³mo se generan, viven, recuerdan, se relacionan, viajan y cambian el mundo. Debe permitir:

- **Persistencia total**: todo lo que ocurre queda guardado.
- **Memoria total**: cada NPC recuerda todo (directo o por rumor), pero con mecanismos para *resumir sin perder el detalle*.
- **Mundo dinÃ¡mico**: NPCs actÃºan aunque el jugador no estÃ© presente.
- **PropagaciÃ³n de informaciÃ³n**: las noticias se mueven por proximidad y rutas.
- **IntegraciÃ³n con LLM**: la LLM genera narrativa, diÃ¡logos, reacciones y eventos usando contexto consistente.

> **Importante**: Last Adventurer es **text-based**. Este sistema genera *estado* y *texto*, no IA visual ni comportamiento 3D.

---

## Dependencias (Sistemas Relacionados)

Este documento conecta directamente con:

- `SISTEMA_HISTORIA.md`: bitÃ¡cora global, consecuencias encadenadas, persistencia.
- `STORYTELLER_SYSTEM.md`: world lore estÃ¡tico + historia procedural + live history + context builder.
- `SISTEMA_RELACIONES.md`: reputaciÃ³n hÃ­brida, opiniones (confianza/respeto/miedo), red social, propagaciÃ³n.
- `SISTEMA_TIEMPO.md`: rutinas por hora, avance por acciÃ³n, eventos temporales.
- `SISTEMA_MAPA.md`: ubicaciones, rutas, distancias, movimiento/visibilidad.
- `SISTEMA_LLM.md`: cliente LLM, prompt templates, fallback.

---

## Objetivos de DiseÃ±o

1. **Determinismo por semilla**: con la misma seed, el mundo y los NPCs â€œbaseâ€ deben ser reproducibles.
2. **Estado vivo**: ademÃ¡s de lo procedural inicial, el mundo se *desvÃ­a* por acciones del jugador y por eventos del mundo.
3. **Escalabilidad**: miles de NPCs teÃ³ricos, pero solo un subconjunto activo/cargado segÃºn regiÃ³n.
4. **No perder memoria**: todo se guarda; para contexto LLM se usa un Ã­ndice/resumen, pero el histÃ³rico crudo permanece.

---

## Conceptos Clave

### NPC vs Persona
- **NPC**: entidad persistente con ID, estado, relaciones, inventario, agenda, memoria.
- **Persona**: â€œcapa narrativaâ€ del NPC (voz, valores, rasgos), usada para coherencia textual y decisiones.

### Estados del NPC
- `vivo`
- `muerto`
- `desaparecido`
- `preso`
- `herido`
- `enfermo`

> El estado afecta rutinas, diÃ¡logos, disponibilidad de servicios y consecuencias (ej. taberna cerrada).

---

## Arquitectura del Sistema

### Componentes (Backend)

1. **NPCManager**
   - Crea/carga NPCs
   - Mantiene cachÃ© de NPCs activos por regiÃ³n/ubicaciÃ³n
   - Expone operaciones de interacciÃ³n (hablar, comerciar, atacar, ayudar, etc.)

2. **Scheduler / Time Reactor**
   - Cuando avanza el tiempo (por acciÃ³n), actualiza:
     - rutinas
     - viajes
     - eventos programados
     - consecuencias con delay

3. **RumorEngine**
   - Gestiona hechos/noticias como â€œrumoresâ€
   - Propaga por proximidad y por rutas

4. **MemoryIndex / Context Indexer**
   - Mantiene un Ã­ndice para construir contexto LLM:
     - Ãºltimas interacciones
     - eventos relevantes
     - â€œresÃºmenes por temaâ€

5. **Storyteller Bridge**
   - Integra NPCs con eventos histÃ³ricos (procedural history) y live history

---

## Modelo de Datos

### 1. Estructura Base de NPC (JSON)

```json
{
  "id": "npc_000123",
  "nombre": "Mira",
  "alias": ["La Tabernera"],
  "genero": "femenino",
  "raza": "humano",

  "origen": {
    "nacimiento": {"aÃ±o": 67, "region_id": "region_valle_umbrio", "ubicacion_id": "pueblo_roble"},
    "linaje": {"padre": "npc_000021", "madre": "npc_000022", "familia": ["npc_000021", "npc_000022"]}
  },

  "rol": {
    "tipo": "comerciante",
    "subtipo": "tabernero",
    "faccion_id": "faccion_gremio_mercaderes",
    "servicios": ["posada", "comida", "rumores"]
  },

  "personalidad": {
    "rasgos": ["desconfiada", "pragmÃ¡tica"],
    "valores": ["lealtad", "orden"],
    "sliders": {
      "agresividad": 0.2,
      "empatÃ­a": 0.5,
      "codicia": 0.6,
      "chisme": 0.8,
      "valentÃ­a": 0.3,
      "honor": 0.4
    },
    "voz": {
      "tono": "seco",
      "muletillas": ["ajÃ¡", "mira tÃº"],
      "registro": "coloquial"
    }
  },

  "estado": {
    "vital": "vivo",
    "salud": {"hp": 30, "hp_max": 30, "heridas": []},
    "riqueza": {"oro": 120, "deudas": []},
    "emocion": {"estado": "neutral", "intensidad": 0.2}
  },

  "ubicacion": {
    "modo": "mundial",
    "tile": [12, 45],
    "subtile": [4, 7],
    "ubicacion_id": "pueblo_roble",
    "interior_id": "taberna_roble"
  },

  "rutina": {
    "zona_base_id": "pueblo_roble",
    "agenda_diaria": [
      {"desde": "06:00", "hasta": "10:00", "actividad": "abrir_taberna"},
      {"desde": "10:00", "hasta": "18:00", "actividad": "atender_clientes"},
      {"desde": "18:00", "hasta": "22:00", "actividad": "cierre_y_cuentas"},
      {"desde": "22:00", "hasta": "06:00", "actividad": "dormir"}
    ],
    "excepciones": []
  },

  "relaciones": {
    "jugador": {
      "reputacion": {"valor": 0, "estado": "neutral"},
      "opiniones": {"confianza": 50, "respeto": 50, "miedo": 0, "deuda": 0, "romance": 0},
      "eventos": []
    },
    "npcs": {
      "npc_000124": {"tipo": "familia", "subtipo": "hermano", "afecto": 75}
    }
  },

  "inventario": {
    "tipo": "tienda",
    "stock": [{"item_id": "comida_pan", "cantidad": 12}],
    "tabla_precios": {"multiplicador": 1.0}
  },

  "memoria": {
    "eventos": [],
    "rumores": [],
    "indice": {
      "resumen_general": "...",
      "resumen_jugador": "...",
      "ultimas_interacciones": []
    }
  },

  "flags": {
    "conocido_por_jugador": false,
    "importante": false,
    "es_unico": false
  }
}
```

---

## Personalidad (Sistema de Rasgos)

### Rasgos (tags)
Ejemplos:
- `generoso`, `tacaÃ±o`, `valiente`, `cobarde`, `curioso`, `fanÃ¡tico`, `paranoico`, `honorable`, `mentiroso`, `ambicioso`

### Sliders (0.0 - 1.0)
Estos valores son usados para:
- modificar reacciones
- sesgar diÃ¡logos generados por LLM
- probabilidad de propagar rumores

Sliders recomendados:
- agresividad
- empatÃ­a
- codicia
- chisme
- valentÃ­a
- honor
- paciencia
- supersticion

---

## Rutinas y Agenda (IntegraciÃ³n con Tiempo)

Basado en `SISTEMA_TIEMPO.md` (tiempo avanza por acciÃ³n). Cuando el tiempo avanza:

1. Se evalÃºa en quÃ© bloque horario cae el NPC.
2. Se ejecuta el cambio de actividad.
3. Si la actividad implica movimiento, se crea un **Plan de Viaje**.

### Actividades estÃ¡ndar
- `dormir`
- `trabajar`
- `viajar`
- `comer`
- `patrullar`
- `atender_tienda`
- `reunirse`
- `rezar`
- `ocultarse`

### Excepciones
Eventos que rompen la rutina:
- guerra/plaga/incendio
- muerte de un familiar
- persecuciÃ³n
- misiÃ³n activa

---

## Movimiento y Viajes (IntegraciÃ³n con Mapa)

### Plan de Viaje
Un viaje se modela como:

```json
{
  "viaje": {
    "origen_tile": [12, 45],
    "destino_tile": [15, 47],
    "ruta_id": "ruta_00123",
    "inicio_tick": 15234,
    "fin_tick": 15310,
    "estado": "en_curso",
    "eventos": []
  }
}
```

- Se usa el sistema de rutas del mapa cuando exista `ruta_id`.
- Si no hay ruta conocida, se puede hacer viaje â€œcampo traviesaâ€ con mÃ¡s riesgo.

---

## Memoria Total (sin perder rendimiento)

La memoria *cruda* se guarda siempre.

### Estructura de evento de memoria

```json
{
  "id": "mem_000001",
  "timestamp": {"tick": 15234, "dia": 3, "hora": 14},
  "tipo": "interaccion|rumor|evento|combate|decision",
  "fuente": "observado|oido|inferido",
  "descripcion": "El jugador ayudÃ³ a reparar la puerta de la taberna.",
  "entidades": {"jugador": true, "npcs": ["npc_000123"], "ubicacion_id": "pueblo_roble"},
  "impacto_emocional": 0.6,
  "etiquetas": ["ayuda", "trabajo", "positivo"],
  "datos": {}
}
```

### Ãndice / Resumen (para el Context Builder)
Para no mandar 5000 eventos al LLM:
- `resumen_general` (actualizable)
- `resumen_jugador` (quÃ© piensa del jugador)
- `ultimas_interacciones` (N Ãºltimas)
- `memoria_por_etiqueta` (opcional: top-N por tema)

> **Regla**: resumir â‰  borrar. El histÃ³rico queda intacto.

---

## Conocimiento y Rumores (PropagaciÃ³n)

Basado en `SISTEMA_RELACIONES.md` y `SISTEMA_HISTORIA.md`.

### Rumor (estructura)

```json
{
  "id": "rumor_000045",
  "hecho_id": "ev_tabernero_muerto",
  "contenido": "Dicen que el tabernero de Roble muriÃ³...",
  "origen": {"tile": [12, 45], "npc_id": "npc_000777"},
  "timestamp": {"tick": 16000},
  "fidelidad": 0.7,
  "alcance": {
    "tipo": "proximidad|rutas",
    "radio_tiles": 3,
    "velocidad": 2
  },
  "sesgo": {
    "npc_id": "npc_000777",
    "emocion": "miedo",
    "intensidad": 0.5
  }
}
```

### Reglas de propagaciÃ³n
- **Proximidad**: NPCs en el mismo asentamiento lo saben â€œrÃ¡pidoâ€.
- **Rutas**: comerciantes/viajeros lo llevan entre ubicaciones.
- **Personalidad**: alto `chisme` = mÃ¡s transmisiÃ³n.
- **RelaciÃ³n**: familia/amigos transmiten mÃ¡s y distorsionan menos.

---

## IntegraciÃ³n con Historia y Consecuencias

### Evento Global (Live History)
Toda interacciÃ³n relevante produce un evento en el historial global y en memoria NPC:

- jugador mata a NPC â†’ evento `muerte_npc`
- eso encola consecuencias:
  - `cierre_negocio` (1 dÃ­a)
  - `cartel_se_vende` (7 dÃ­as)
  - `nuevo_dueÃ±o` (14 dÃ­as)

Este encadenamiento se gestiona por un sistema de consecuencias (ver `SISTEMA_HISTORIA.md`).

---

## IntegraciÃ³n con LLM

### Tipos de generaciÃ³n
- `npc_dialogo_saludo`
- `npc_dialogo_reaccion`
- `npc_dialogo_negociacion`
- `rumor_redaccion`
- `descripcion_escena_social`
- `evento_mundo`

### Context Builder (mÃ­nimo viable)
Cuando se llame al LLM para un NPC:

**Inputs mÃ­nimos**
- NPC: personalidad + estado + rol + ubicaciÃ³n
- Jugador: estado (hp, nivel) + tags + reputaciÃ³n con NPC
- Tiempo: hora/dÃ­a/estaciÃ³n
- Entorno: ubicaciÃ³n/bioma
- Memoria: Ãºltimas interacciones + resumen_jugador
- Rumores locales (top 3)

**Constraints**
- No spoilear cosas no descubiertas.
- Voz omnisciente limitada.
- 150 palabras (o lÃ­mite definido).

**Fallback**
- Si el LLM no estÃ¡ disponible: mostrar error y pausar juego (decisiÃ³n ya tomada).

---

## Persistencia en Save

### Propuesta de estructura en el save

```json
{
  "npcs": {
    "version": "1.0",
    "activos": ["npc_000123", "npc_000124"],
    "por_id": {
      "npc_000123": {"...": "..."}
    },
    "rumores": [
      {"id": "rumor_000045", "...": "..."}
    ]
  }
}
```

> Nota: para performance, NPCs no activos pueden guardarse de forma â€œcompactaâ€ pero **sin perder memoria cruda**.

---

## Endpoints API (Propuestos)

> No se implementan aÃºn; sirven para planear la uniÃ³n backendâ†”frontend.

- `GET /api/npcs?slot=1&ubicacion_id=...` â†’ lista NPCs visibles/alcanzables
- `GET /api/npcs/<npc_id>?slot=1` â†’ detalle NPC (con privacidad: no revelar secretos)
- `POST /api/npcs/<npc_id>/hablar` â†’ genera diÃ¡logo (LLM) con contexto
- `POST /api/npcs/<npc_id>/accion` â†’ ayudar/amenazar/atacar/comprar/etc.
- `GET /api/npcs/rumores?slot=1&ubicacion_id=...` â†’ rumores locales
- `POST /api/npcs/tiempo/avanzar` â†’ para simular avance (si hace falta)

---

## UI (Frontend) - Propuesta

- Panel â€œNPCsâ€ en la pantalla principal:
  - lista de NPCs cercanos (por ubicaciÃ³n)
  - al seleccionar, muestra:
    - descripciÃ³n
    - reputaciÃ³n/estado
    - opciones (hablar, comerciar, preguntar rumores)

- Panel â€œRumoresâ€ (subpanel):
  - feed de rumores por ubicaciÃ³n

---

## Checklist de ImplementaciÃ³n (cuando pasemos a cÃ³digo)

### Backend
- [ ] `backend/src/systems/npcs/` con:
  - `npc.py` (modelo y utilidades)
  - `npc_manager.py` (carga/creaciÃ³n/cachÃ© por regiÃ³n)
  - `scheduler.py` (rutinas + viajes + ejecuciÃ³n por avance de tiempo)
  - `rumors.py` (RumorEngine)
  - `memory_index.py` (resÃºmenes e indexado para prompts)
- [ ] Integrar con `SaveManager` (migraciÃ³n de versiÃ³n y estructura `npcs` en el save)
- [ ] Endpoints `/api/npcs/*` (listado, detalle, hablar, acciÃ³n, rumores)
- [ ] IntegraciÃ³n con `tiempo` (TimeManager: avance por acciÃ³n, triggers de rutina)
- [ ] IntegraciÃ³n con `llm/client.py` (si el LLM estÃ¡ habilitado)

### Frontend
- [ ] Panel â€œNPCsâ€ (lista + detalle + acciones)
- [ ] UI de diÃ¡logo (feed + respuestas)
- [ ] UI de rumores (por ubicaciÃ³n)
- [ ] Manejo de fallback: â€œLLM no disponible â†’ PAUSEâ€

### Testing
- [ ] Unit: generaciÃ³n determinista por seed
- [ ] Unit: transiciÃ³n de rutinas por hora y excepciones
- [ ] Unit: propagaciÃ³n de rumores (proximidad + rutas + personalidad)
- [ ] Unit: persistencia (save/load) sin perder memoria cruda
- [ ] Functional: simular 1-3 dÃ­as y verificar cambios de mundo (negocio cierra, cambia dueÃ±o, etc.)

---

## Preguntas para Definir (respÃ³ndeme en este mismo documento o en chat)

### A. Escala y densidad
1. Â¿CuÃ¡ntos NPCs â€œglobalesâ€ quieres generar por regiÃ³n/ubicaciÃ³n? (Ej: 10 por pueblo, 200 por regiÃ³n): Realmente me gustaria que los pueblos y regiones tengan vida y que sea vida propia.
2. Â¿Hay NPCs â€œÃºnicosâ€ fijos (handcrafted) ademÃ¡s de los procedurales? Â¿CuÃ¡ntos?: No 

### B. Identidad y representaciÃ³n
3. Â¿QuÃ© razas existen en el mundo (lista cerrada) y quÃ© proporciones quieres? Lee el sistema de world lore y entenderÃ¡s.
4. Â¿Quieres edades â€œrealistasâ€ (nacen/mueren) o solo edad como flavor? Edades realistas.
5. Â¿Los NPCs pueden cambiar de rol (ej. campesino â†’ guardia) por eventos? Si, claro.

### C. SimulaciÃ³n vs. costo
6. Â¿Simulamos rutinas de TODOS los NPCs o solo de NPCs activos/cercanos al jugador? Solo los npc en un radio de 500 tiles. Sin embargo, bajo eventos generales o mundiales, se podran dejar prescedentes para que cuando el llm o sistema procedural genere nuevos npc en zonas, tengan esto en cuenta. Por ejmplo, ocurrio un terremoto en otra region hace 20 aÃ±os, que en esa otra region si llegamos a visitarla, npc recuerden eso.
7. Â¿QuÃ© radio define â€œactivoâ€? (tiles, ubicaciones, regiÃ³n): 500 tiles
8. Â¿Se permite teletransporte narrativo para NPCs lejanos (simulaciÃ³n aproximada)? No.

### D. Memoria y privacidad
9. Â¿QuÃ© cosas NO deben revelarse nunca al jugador aunque existan en el estado? (secretos) : Pues nada, todo lo debe descubrir el jugador 
10. Â¿QuÃ© ventana de â€œmemoria recienteâ€ quieres para prompts? (N eventos o N dÃ­as) : Ambos
11. Â¿Quieres un sistema de â€œconfianzaâ€ para que un NPC comparta secretos? : Si

### E. Rumores
12. Â¿Los rumores pueden distorsionarse (fidelidad baja) o siempre veraces? : Pueden distorcionarse entre mas lejos viajen.
13. Â¿QuÃ© velocidad de propagaciÃ³n quieres por rutas? (ej. 1 tile/hora, 1 ubicaciÃ³n/dÃ­a) : Deberemos seguir la logica de distancia y tiempos de los tiles.
14. Â¿QuiÃ©nes son â€œportadoresâ€ fuertes? (comerciantes, bardos, guardias): No implemetemos esto.

### F. Relaciones
15. Â¿ReputaciÃ³n se calcula solo por acciones directas o tambiÃ©n por valores (ej. matar bandidos = +respeto)? : te lo dejo a tu gusto, prefiero por ambos.
16. Â¿Quieres romance como sistema real o solo como opiniÃ³n opcional? : Sistema real

### G. Interacciones mÃ­nimas (MVP)
17. Para la primera implementaciÃ³n: Â¿quÃ© 3 acciones deben existir sÃ­ o sÃ­? (hablar, comerciar, pedir rumor, etc.) : Hablar, Comerciar, Pedir Rumor, Hablar IA
18. Â¿Se permite matar NPCs importantes? Si sÃ­, Â¿cÃ³mo manejamos reemplazos? : Si se pueden matar npcs importantes y sus reemplazos deben ser por logica. Por ejemplo, matamos al gobernador de un pueblo, pues deberÃ¡ asumir cargo eventualmente aquel npc que siempre se ha visto que es importante en el pueblo o asi.

### H. LLM
19. Â¿Proveedor inicial? (Ollama local, API remota, ambos) : ambos
20. Â¿â€œPAUSEâ€ significa bloquear totalmente el gameplay o permitir acciones no narrativas? : **Opcion A - El juego se detiene completamente, muestra error, el jugador no puede hacer nada hasta que el LLM vuelva.**
21. Â¿Longitud objetivo por respuesta NPC? (ej. 2-4 lÃ­neas, 100-150 palabras) : 150 palabras maximo por nuestra parte y 150 palabras maximo por parte del npc.

### I. Guardado
22. Â¿Quieres guardar TODOS los NPCs completos en el save, o â€œcompactarâ€ los no activos (manteniendo memoria cruda en archivo aparte)? Guarda todos los npc completos en el save.
23. Â¿Quieres versionado propio para `npcs.version` independiente del save general? si.

### J. Tono y estilo
24. Â¿Tono del mundo (grimdark, heroico, comedia seca)? | Lee el sistema de world lore.
25. Â¿Nivel de â€œrealismo socialâ€ (racismo/clases/polÃ­tica) permitido? Si

> Cuando respondas estas preguntas, cierro decisiones y puedo proponer el plan de implementaciÃ³n (backend + endpoints + UI) alineado a tus respuestas.


