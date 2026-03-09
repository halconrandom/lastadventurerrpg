# Sistema de Historia Persistente y Narrativa Procedural

Este sistema tiene como objetivo generar una narrativa coherente, dinámica y persistente donde las acciones del jugador (exploración, combate, diálogos) dejen una huella real en el mundo y en la memoria del personaje.

## Pilares del Sistema

1. **Memoria del Personaje (Bitácora)**: Un registro estructurado de eventos clave que el sistema puede consultar para dar contexto a futuros encuentros.
2. **Contexto Regional y Pre-existente**: La narrativa se adapta a la zona actual. Además, existen "historias previas" en cada región antes de la llegada del jugador, permitiendo diálogos y decisiones basadas en eventos que ya estaban ocurriendo.
3. **Decisiones con Impacto**: Estados lógicos que se activan según las elecciones del jugador, afectando diálogos y eventos futuros.
4. **Inicio Seguro (The Hearth)**: El personaje comienza en un lugar "seguro" (estilo Minecraft), sin exposición inmediata a combate ni situado en un pueblo masificado. Un punto de partida neutral y equilibrado.

## Arquitectura de Datos

### 1. El Registro Histórico (Log de Eventos)
Cada evento relevante se guardará en el `save_game` con la siguiente estructura:
```json
{
  "id": "ev_001",
  "timestamp": 12345678,
  "tipo": "decision | combate | descubrimiento",
  "descripcion": "Derrotó al Jefe de las Ruinas",
  "impacto": {
    "faccion_x": -10,
    "rumor_activado": "heroe_de_ruinas"
  }
}
```

### 2. Generador de Contexto (Context Engine)
Antes de generar un texto descriptivo, el sistema evaluará:
- **Estado Vital**: ¿Está el jugador herido o tiene hambre/sed?
- **Pasado Reciente**: ¿Qué hizo en las últimas 5 exploraciones?
- **Entorno**: Clima actual y peligros detectados.

## Implementación Propuesta

### Fase 1: Estructura de Datos (Backend)
- [ ] Crear clase `NarrativaManager` en `backend/src/systems/narrativa.py`.
- [ ] Añadir `historial` al objeto `DatosJuego` en el SaveManager.
- [ ] Implementar un sistema de "Tags" (Etiquetas) para el personaje (ej: "Matabestias", "Fugitivo").

### Fase 2: Narrativa de Inicio (Prólogo)
- [ ] Crear un set de plantillas de inicio que dependan de la dificultad y el género.
- [ ] Implementar el endpoint `/api/narrativa/prologo` para obtener una introducción coherente.

### Fase 3: Integración en Exploración
- [ ] Modificar el endpoint de exploración para que los eventos no sean solo "aleatorios", sino que consulten el historial.
- [ ] Ejemplo: Si el jugador huyó de un combate antes, el texto de exploración podría decir: *"Vuelves a este lugar con cautela, recordando la sombra que casi te arrebata la vida."*

## Decisiones Procedurales
Se introducirán "Eventos de Decisión" durante la exploración:
- **A** (Riesgo alto, recompensa alta)
- **B** (Cautela, información)
- **C** (Ignorar, preservación de recursos)


## Preguntas para Definir la Estructura

### Preguntas Originales

1. **El Inicio Seguro**: ¿Visualizas este lugar como un campamento base inicial, una cabaña abandonada o simplemente un claro en el bosque que sirva de "hub" permanente para el jugador?
   > [RESPUESTA]: Un lugar aleatorio que el sistema decida. 

2. **Historia de Zona**: ¿Preferirías que la historia previa de una zona se descubra mediante "hallazgos" (notas, restos) o que haya NPCs neutrales que te pongan al día?
   > [RESPUESTA]: De todas las formas posibles, notas, investigando uno mismo, hablando con NPC si hay en el area, etc. Hagamos esto un sistema muy inmerisovo

3. **Persistencia**: ¿Qué tan granular debe ser la memoria? ¿Debe recordar cada acción menor o solo hitos importantes (muerte de jefes, rutas elegidas)?
   > [RESPUESTA]: Debemos asegurarnos de que recuerde todo. Hagamos un sistema que permita que dependiendo de las decisiones del jugador, este haga contraste en el mundo... ¿Recomendaste a un npc hacer un segundo piso en su casa? eventualmente lo verás. ¿mataste al tabernero? la taberna del lugar cierra y eventualmente verás que hay un cartel de "se vende". Juguemos con eso.

4. **Consecuencias**: ¿Quieres que las decisiones afecten estadísticas del personaje (alineamiento) o principalmente el contenido de los textos y encuentros?
   > [RESPUESTA]: Depende. Puede ocurrir que las decisiones provoquen cosas que nos afecten. Siempre puede ocurrir.

---

### Preguntas Adicionales - Memoria y Persistencia

5. **Caducidad de eventos**: ¿Los eventos "menores" deberían expirar después de X tiempo o exploraciones? Ejemplo: "Encontraste una seta" es irrelevante después de 50 movimientos, pero "Mataste al Aldeano X" debería persistir permanentemente.
   > [RESPUESTA]: No, siempre se debe guardar todo.

6. **Memoria de NPCs**: ¿Los NPCs también recuerdan al jugador? Si el jugador robó en una tienda, ¿el tendero lo recuerda en futuras visitas? ¿Se propaga ese "rumor" a NPCs cercanos?
   > [RESPUESTA]: Si, los NPCs deben recordar todo.

7. **Memoria del mundo**: ¿El mundo cambia sin intervención del jugador? Ejemplo: Si hay una guerra entre facciones, ¿avanza aunque el jugador no participe?
   > [RESPUESTA]: Si, el mundo debe cambiar sin intervención del jugador.

---

### Preguntas Adicionales - Decisiones y Consecuencias

8. **Sistema de reputación**: ¿Quieres un sistema numérico (reputación: -100 a +100) o basado en "estados" (Aliado/Neutral/Enemigo)? Los estados son más narrativos, los números más "gamificables".
   > [RESPUESTA]: Ambos. Depende de la situación. Es decir, por lo general seran numericas, pero cada cierta cantidad podrá definir realmente como alguien o algo nos defina a nosotros. Por ejemplo -50 como enemigo, 0 neutral y +50 como aliado. Pero incluso podemos trabajarlo más profundamente, como por ejemplo, que un enemigo se nos vuelva aliado por temas del mundo, o que hayan relaciones amorosas. ¿me hago entender?

9. **Consecuencias retardadas**: ¿Las decisiones pueden tener efectos horas/juegos después? Ejemplo: Salvas a un NPC en el inicio → 10 horas después aparece para ayudarte en un combate.
   > [RESPUESTA]: Si, por supuesto, pero tampoco puede ser algo constante. Tampoco es que salvar un niño de 10 años, luego se te vuelve tu aliado. Debe ser consistente pero tampoco asi.

10. **Decisiones irreversibles**: ¿Debe haber decisiones que cambien permanentemente el mundo? (matar un NPC importante, destruir un lugar)
    > [RESPUESTA]: Exactamente.

---

### Preguntas Adicionales - Narrativa Procedural

11. **Voz narrativa**: ¿El narrador es:
    - Omnisciente (3ra persona clásica RPG)
    - Limitado (solo lo que el personaje percibe)
    - Subjetivo (con opiniones/bias según el personaje)
    > [RESPUESTA]: Omnisciente, pero tampoco liberando demasiada informacion al personaje para que este decida que descubrir o que hacer.

12. **Tono**: ¿El tono es:
    - Oscuro/sombrío (Dark Souls)
    - Aventurero clásico (D&D)
    - Misterioso/lore-heavy (Elder Scrolls)
    > [RESPUESTA]: D&D pero con toques oscuros. Es decir, no todo es color de rosa, pero tampoco es todo negro y a su vez con un heavy lore.

---

### Preguntas Adicionales - "The Hearth" (Inicio Seguro)

13. **Evolución del hub**: ¿El lugar seguro puede mejorar/expandirse? ¿El jugador puede construir/mejorar su base inicial?
    > [RESPUESTA]: Hay que entender que el hub no es donde el personaje vive, es donde spawnea. Podemos hacer que eventualmente pueda comprar o construir una casa donde el se le de la gana.

14. **Fast travel**: ¿El inicio seguro sirve como punto de teletransporte? ¿Hay múltiples "hogares" o solo uno?
    > [RESPUESTA]: No, nada de eso. El jugador debe caminar para llegar a todos lados.

---

### Pregunta Clave

15. **Balance simulación vs narrativa**: ¿Cuál es el balance deseado?
    - Más simulación = el mundo reacciona lógicamente a todo (complejo de implementar)
    - Más narrativa = el sistema "finge" consecuencias para contar una mejor historia (más manejable)
    > [RESPUESTA]: Más simulación, pero con toques narrativos.

---

### Preguntas Adicionales - Generación y Mundo

16. **Generación de texto narrativo**: ¿Cómo se genera el texto descriptivo y de eventos?
    - Plantillas predefinidas con variables (ej: "El [ENEMIGO] aparece desde [DIRECCION]")
    - Fragmentos combinables tipo "mad libs"
    - LLM externo via API
    - Sistema híbrido (plantillas + LLM para momentos clave)
    > [RESPUESTA]: LLM hosteada en VPS propia, especializada en RPG con fine-tuning suave (LoRA).

17. **Estructura del mapa**: ¿Cómo se organiza el mundo?
    - Grid de tiles (cada movimiento es un tile)
    - Zonas grandes con puntos de interés (estilo mapa de región)
    - Mundo abierto con coordenadas X/Y
    - Otra estructura
    > [RESPUESTA]: Diria que por tiles pero con coordenadas X/Y. Es decir, que el mundo sea infinito pero que tenga coordenadas. 

18. **Sistema de tiempo**: ¿Existe un reloj del mundo?
    - Día/noche que afecta gameplay
    - Estaciones del año
    - Tiempo transcurrido desde el inicio
    - Sin sistema de tiempo
    > [RESPUESTA]: Si, tendremos que tener un sistema dia, noche, estaciones del año y tiempo transcurrido desde el inicio. Podremos setear estos parametros aleatorios para el inicio de la partida

19. **Sistema de relaciones NPCs**: ¿Qué tan profundo es el sistema de relaciones?
    - Solo reputación numérica
    - Estados simples (Aliado/Neutral/Enemigo)
    - Relaciones complejas (familia, amistad, romance, rivalidad)
    - Red de relaciones entre NPCs (A es enemigo de B, si ayudas a A, B te odia)
    > [RESPUESTA]: Reputacion numero con estados simples, desarrollado a una red de relaciones entre NPC y relaciones complejas. osea muy muy trabajado.

20. **Propagación de información**: ¿Cómo se propaga la información entre NPCs?
    - Instantáneo (todos saben todo inmediatamente)
    - Por proximidad (NPCs cercanos saben primero)
    - Por rutas (comerciantes viajan y cuentan historias)
    - Por tiempo (la noticia tarda X días en llegar)
    > [RESPUESTA]: Por rutas y proximidad.

---

### Preguntas Adicionales - LLM y Narrativa

21. **Modelo base para LLM**: ¿Qué modelo prefieres como base?
    - Llama 3.2 3B (muy ligero, rápido)
    - Phi-3 Mini 3.8B (buen balance)
    - Mistral 7B (más calidad, más recursos)
    - Otro modelo específico
    > [RESPUESTA]: Llama 3.2 3B

22. **Especialización del modelo**: ¿Qué tipo de contenido debe generar principalmente?
    - Descripciones de lugares y ambientes
    - Diálogos de NPCs
    - Eventos y encuentros
    - Todo lo anterior (modelo generalista RPG)
    > [RESPUESTA]: Todo lo anterior.

23. **Dataset de entrenamiento**: ¿Cómo conseguimos datos para el fine-tuning?
    - Crear dataset manual con ejemplos propios
    - Usar datasets públicos de RPG (si existen)
    - Mezcla de ambos
    > [RESPUESTA]: usar datasets y manualmente

24. **Fallback sin LLM**: ¿Qué pasa si la LLM no está disponible?
    - Usar plantillas predefinidas como respaldo
    - Mostrar error al jugador
    - Pausar el juego hasta que vuelva
    > [RESPUESTA]: mostrar error y pausar el juego.

25. **Temperatura y creatividad**: ¿Qué nivel de variabilidad deseas?
    - Baja (0.3-0.5): Narrativa consistente y predecible
    - Media (0.6-0.7): Balance entre consistencia y sorpresa
    - Alta (0.8-1.0): Narrativa muy variada, menos predecible
    > [RESPUESTA]: media.

---

## Sugerencias de Expansión

### G. Arquitectura LLM para Narrativa (NUEVO)

```
┌─────────────────────────────────────────────────────────┐
│                    BACKEND PYTHON                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │              NarrativaManager                    │    │
│  │  ┌─────────────┐  ┌─────────────────────────┐   │    │
│  │  │ Context     │  │    LLM Client          │   │    │
│  │  │ Builder     │──►│ (Ollama / vLLM / LM Studio)│   │    │
│  │  └─────────────┘  └─────────────────────────┘   │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      VPS - LLM                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Modelo Base: Llama 3.2 3B / Phi-3 Mini         │    │
│  │  +                                               │    │
│  │  Adaptador LoRA: rpg_narrator.pt                │    │
│  │  +                                               │    │
│  │  Contexto del juego (historial reciente)         │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Stack recomendado**:
- **Ollama** o **vLLM** para servir el modelo
- **LoRA adapters** para especialización
- **Contexto dinámico**: últimos 5-10 eventos + estado actual

**Prompt structure**:
```
System: Eres el narrador de un RPG de fantasía oscura...
Context: {historial_reciente}, {estado_jugador}, {zona_actual}
Task: Genera una descripción de {tipo_evento}
Constraints: Máximo 150 palabras, tono D&D oscuro...
```

### H. Dataset para Fine-Tuning (NUEVO)

Estructura sugerida para entrenar el modelo:

```json
{
  "instruction": "Genera una descripción de exploración para un bosque oscuro donde el jugador encuentra restos de un campamento.",
  "input": {
    "zona": "bosque_somrio",
    "estado_jugador": "herido_leve",
    "historial_reciente": ["huyo_combate", "encontro_setas"],
    "tono": "oscuro"
  },
  "output": "Entre los árboles retorcidos, los restos de un campamento abandonado aparecen ante ti. Una fogola apagada, restos de comida podrida y... marcas de garras en los árboles cercanos. Algo ocurrió aquí, y no fue hace mucho."
}
```

**Categorías de entrenamiento**:
1. Descripciones de zonas
2. Eventos de exploración
3. Diálogos de NPCs
4. Combates (inicio, desarrollo, final)
5. Hallazgos y descubrimientos
6. Transiciones entre zonas

---

### A. Sistema de "Rumores y Propagación"
```json
rumor = {
  "id": "rumor_001",
  "contenido": "Un extraño derrotó al Jefe de las Ruinas",
  "origen": "ruinas_norte",
  "propagacion": {
    "tipo": "proximidad",  // proximidad | rutas_comerciales | tiempo
    "radio": 3,            // zonas de alcance
    "velocidad": 2         // zonas por día de juego
  },
  "modificadores": {
    "combate": 0.05,
    "descuentos_tienda": -0.10
  },
  "caducidad": null        // null = permanente según respuesta del usuario
}
```
Los rumores se propagan entre zonas y afectan cómo los NPCs reaccionan.

### B. Sistema de "Ecos del Pasado"
En lugar de solo historia previa escrita, permitir que el jugador encuentre **vestigios**:
- Diarios de aventureros caídos
- Restos de campamentos
- Inscripciones en ruinas
- NPCs que cuentan historias de otros lugares

### C. Tags Dinámicos vs Estáticos
```json
{
  "tags_estaticos": ["Valiente", "Explorador"],
  "tags_dinamicos": ["Asesino de X", "Salvador de Y"]
}
```
- `tags_estaticos`: El jugador los elige durante la creación
- `tags_dinamicos`: El sistema los asigna según acciones

### D. Sistema de Relaciones Complejas (NUEVO - basado en respuesta 8)
```json
relacion = {
  "npc_id": "tabernero_001",
  "jugador_id": "player",
  "tipo": "neutral",        // enemigo | neutral | aliado | amigo | romance | familia
  "valor": 0,                // -100 a +100
  "historial_interacciones": ["ev_001", "ev_045"],
  "modificadores": {
    "confianza": 0,
    "respeto": 0,
    "atraccion": 0
  }
}
```
Permite relaciones matizadas: un NPC puede ser enemigo (-50) pero tener respeto (+30) por el jugador.

### E. Sistema de Eventos del Mundo (NUEVO - basado en respuesta 7)
```json
evento_mundo = {
  "id": "guerra_facciones_001",
  "tipo": "conflicto",
  "estado": "activo",
  "partes": ["faccion_norte", "faccion_sur"],
  "progreso": 0.35,          // 0-1, avanza sin intervención
  "consecuencias": {
    "faccion_norte_gana": ["faccion_sur_destruida", "refugiados_en_zona_central"],
    "faccion_sur_gana": ["faccion_norte_debilitada", "nuevas_rutas_comerciales"]
  },
  "intervencion_jugador": null  // se actualiza si el jugador participa
}
```
El mundo cambia dinámicamente. El jugador puede intervenir o ignorar.

### F. Sistema de Consecuencias Encadenadas (NUEVO - basado en respuesta 3)
```json
cadena_consecuencias = {
  "evento_origen": "ev_045",
  "tipo": "muerte_npc",
  "npc_afectado": "tabernero_001",
  "consecuencias": [
    {
      "tipo": "cierre_negocio",
      "ubicacion": "taberna_central",
      "delay": 1,            // días de juego
      "estado": "pendiente"
    },
    {
      "tipo": "cartel_se_vende",
      "ubicacion": "taberna_central",
      "delay": 7,
      "estado": "pendiente"
    },
    {
      "tipo": "nuevo_dueno",
      "npc_id": "comerciante_002",
      "delay": 14,
      "estado": "pendiente"
    }
  ]
}
```
Las acciones tienen consecuencias que se ejecutan en cadena, días después.

---

## Resumen de Decisiones Tomadas

| Aspecto | Decisión |
|---------|----------|
| Inicio seguro | Aleatorio, decidido por el sistema |
| Descubrimiento de historia | Múltiples métodos (notas, investigación, NPCs) |
| Persistencia | TODO se guarda permanentemente |
| Consecuencias | Afectan mundo y personaje según contexto |
| Caducidad de eventos | No hay, todo es permanente |
| Memoria de NPCs | Total, recuerdan todo |
| Mundo dinámico | Sí, cambia sin intervención del jugador |
| Reputación | Híbrido: numérico + estados + red de relaciones complejas |
| Consecuencias retardadas | Sí, pero consistentes y no constantes |
| Decisiones irreversibles | Sí, afectan permanentemente |
| Voz narrativa | Omnisciente pero limitada en información |
| Tono | D&D con toques oscuros y lore profundo |
| Hub | Spawn inicial, no hogar. El jugador puede construir donde quiera |
| Fast travel | No, exploración a pie |
| Balance | Simulación pesada con toques narrativos |
| Generación narrativa | LLM local con LoRA especializado en RPG |
| Estructura del mapa | Tiles con coordenadas X/Y, mundo infinito |
| Sistema de tiempo | Día/noche + estaciones + tiempo transcurrido, configurable al inicio |
| Relaciones NPCs | Muy profundo: reputación numérica + estados + red entre NPCs + relaciones complejas |
| Propagación de info | Por rutas y proximidad |
| Modelo LLM | Llama 3.2 3B |
| Contenido LLM | Generalista RPG (descripciones, diálogos, eventos, todo) |
| Dataset | Mezcla: datasets públicos + ejemplos manuales |
| Fallback LLM | Mostrar error y pausar el juego |
| Temperatura LLM | Media (0.6-0.7) |

---

## Sistemas Dependientes Requeridos

Para implementar el Sistema de Historia, primero se necesitan estos sistemas:

| # | Sistema | Descripción | Prioridad |
|---|---------|-------------|-----------|
| 1 | **SISTEMA_MAPA.md** | Tiles con coordenadas X/Y, mundo infinito, generación procedural | Alta |
| 2 | **SISTEMA_TIEMPO.md** | Día/noche, estaciones, tiempo transcurrido, configuración inicial | Alta |
| 3 | **SISTEMA_NPCS.md** | NPCs con memoria, personalidad, comportamiento | Alta |
| 4 | **SISTEMA_RELACIONES.md** | Sistema híbrido complejo de relaciones | Alta |
| 5 | **SISTEMA_MUNDO.md** | Eventos globales que avanzan sin el jugador | Media |
| 6 | **SISTEMA_PROPAGACION.md** | Propagación de información por rutas y proximidad | Media |
| 7 | **SISTEMA_LLM.md** | Arquitectura LLM con Llama 3.2 3B | Alta |

---

## Arquitectura Propuesta (Actualizada)

### Capas del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                 │
│         (Generador de texto narrativo - TBD)           │
├─────────────────────────────────────────────────────────┤
│                    CAPA DE LÓGICA                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Narrativa   │  │ Relaciones  │  │ Eventos Mundo  │  │
│  │ Manager     │  │ Manager      │  │ Manager        │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                    CAPA DE DATOS                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Historial   │  │ Estado      │  │ Rumores        │  │
│  │ Eventos     │  │ Mundo       │  │ & Ecos         │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Eventos

```
Acción del Jugador
       │
       ▼
┌──────────────────┐
│ NarrativaManager │ ◄── Consulta historial
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Guardar Evento   │ ◄── Persistencia total
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Propagar Cambios │ ◄── NPCs, rumores, mundo
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Generar Texto    │ ◄── Contexto + plantillas/LLM
└──────────────────┘
```
