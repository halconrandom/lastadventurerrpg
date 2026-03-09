# Storyteller System

## Visión General

El **Storyteller System** es el motor narrativo de Last Adventurer. Genera y mantiene la historia del mundo, proporcionando contexto al LLM para crear eventos dinámicos y coherentes.

**Inspiración**: Dwarf Fortress - Historia procedural profunda que afecta el gameplay actual.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORYTELLER SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    WORLD LORE (Estático)                │   │
│  │  Historia base del mundo - definida manualmente         │   │
│  │  - Cosmología y creación                                │   │
│  │  - Facciones principales                                │   │
│  │  - Geografía histórica                                  │   │
│  │  - Conflictos eternos                                   │   │
│  │  - Dioses y entidades superiores                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              PROCEDURAL HISTORY (100 años)               │   │
│  │  Generada al crear el mundo - determinista por semilla  │   │
│  │  - Año 1-100: Eventos históricos                        │   │
│  │  - Ascenso y caída de reinos                            │   │
│  │  - Héroes y villanos                                    │   │
│  │  - Guerras y tratados                                   │   │
│  │  - Artefactos legendarios                               │   │
│  │  - Linajes de NPCs                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LIVE HISTORY (Tiempo real)                  │   │
│  │  Generada durante el gameplay                           │   │
│  │  - Acciones del jugador                                 │   │
│  │  - Eventos dinámicos (LLM)                               │   │
│  │  - Cambios en ubicaciones                               │   │
│  │  - Relaciones con NPCs                                  │   │
│  │  - Consecuencias de decisiones                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  CONTEXT BUILDER                         │   │
│  │  Construye el contexto para el LLM                      │   │
│  │  - Historia relevante cercana                           │   │
│  │  - Estado de NPCs involucrados                          │   │
│  │  - Historia de la ubicación                             │   │
│  │  - Eventos recientes del jugador                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tipos de Información

### 1. World Lore (Estático)

Información base del mundo, definida manualmente. No cambia entre partidas.

| Categoría | Contenido | Ejemplo |
|-----------|-----------|---------|
| **Cosmología** | Origen del mundo, dioses, planos | "Los Antiguos crearon el mundo hace 10,000 años" |
| **Facciones** | Organizaciones principales | Reino de Valdris, El Círculo Arcano, Los Errantes |
| **Geografía** | Lugares importantes | La Gran Muralla, El Mar de Cenizas, Monte Espectral |
| **Conflictos** | Tensiones eternas | La Guerra de las Sombras (500 años) |
| **Artefactos** | Objetos legendarios | La Espada del Alba, El Ojo de Obsidiana |
| **Razas** | Pueblos del mundo | Humanos, Elfos Nocturnos, Enanos del Vacío |

### 2. Procedural History (100 años)

Generada al crear el mundo. Determinista por semilla.

| Tipo de Evento | Descripción | Afecta a |
|----------------|-------------|----------|
| **Guerras** | Conflictos entre facciones | Fronteras, relaciones, NPCs hostiles |
| **Ascensos** | Nuevos líderes, reinos | Quests, NPCs importantes |
| **Caídas** | Reinos destruidos, ciudades perdidas | Ruinas, tesoros, fantasmas |
| **Plagas** | Enfermedades, maldiciones | Zonas peligrosas, NPCs afectados |
| **Descubrimientos** | Nuevas tierras, recursos | Mapa, comercio |
| **Artefactos** | Creación/pérdida de items legendarios | Quests, tesoros únicos |
| **Linajes** | Nacimientos, muertes, herencias | NPCs, herederos, títulos |
| **Desastres** | Terremotos, erupciones, inundaciones | Geografía, ruinas |

### 3. Live History (Tiempo Real)

Generada durante el gameplay por acciones del jugador y eventos LLM.

| Tipo | Contenido | Persistencia |
|------|-----------|--------------|
| **Acciones del jugador** | Decisiones, combates, exploración | Permanente |
| **Eventos LLM** | Narrativa generada dinámicamente | Permanente |
| **Relaciones NPC** | Afinidad, memoria, diálogos | Por NPC |
| **Cambios de ubicación** | Estado de zonas, modificaciones | Por ubicación |
| **Consecuencias** | Efectos de decisiones pasadas | Permanente |

---

## Estructura de Datos

### Evento Histórico

```python
@dataclass
class EventoHistorico:
    # Identificación
    id: str                    # "guerra_sombras_23"
    año: int                   # Año del evento (1-100 para procedural)
    tipo: str                  # "guerra", "ascenso", "caida", etc.
    
    # Ubicación
    ubicacion: Tuple[int, int] # Coordenadas
    region: str                 # "Valle de Sombras"
    
    # Narrativa
    titulo: str                # "La Caída de Aranthor"
    descripcion: str           # Texto generado por LLM o procedural
    importancia: int           # 1-10 (afecta probabilidad de mención)
    
    # Entidades involucradas
    facciones: List[str]       # ["Reino de Valdris", "Hordas Oscuras"]
    npcs: List[str]            # ["Rey Aldric", "General Vex"]
    artefactos: List[str]      # Items legendarios involucrados
    
    # Consecuencias
    cambios: Dict              # {"faccion": {"relacion": -50}, {"zona": {"estado": "destruido"}}
    
    # Metadata
    generado_por: str          # "procedural" o "llm"
    semilla: str               # Para reproducibilidad
```

### NPC Memory

```python
@dataclass
class NPCMemory:
    # Identificación
    id: str                    # "npc_001"
    nombre: str                # "Elena la Curandera"
    tipo: str                  # "comerciante", "aldeano", "guardia"
    
    # Origen (procedural)
    año_nacimiento: int        # Año en que nació (procedural)
    lugar_nacimiento: str      # Ciudad o región
    linaje: List[str]          # IDs de ancestros
    
    # Estado actual
    ubicacion: Tuple[int, int] # Dónde está ahora
    estado: str                # "vivo", "muerto", "desaparecido"
    
    # Relaciones
    relaciones: Dict[str, int] # {"jugador": 50, "npc_002": -20}
    
    # Memoria
    eventos_presenciados: List[str]  # IDs de eventos
    interacciones_jugador: List[Dict] # Historial con el jugador
    
    # Personalidad dinámica
    rasgos: List[str]          # ["desconfiado", "generoso"]
    estado_emocional: str      # "neutral", "feliz", "asustado"
    
    # Comercio (si aplica)
    inventario: List[str]      # Items disponibles
    precios_modificador: float # 1.0 = normal, 0.8 = descuento
```

### Location State

```python
@dataclass
class LocationState:
    # Identificación
    x: int
    y: int
    bioma: str
    
    # Historia procedural
    eventos_historicos: List[str]  # IDs de eventos del pasado
    
    # Estado actual
    estado: str                # "normal", "alterado", "destruido"
    poblacion: int             # Habitantes actuales
    recursos: Dict             # {"madera": 100, "mineral": 50}
    
    # NPCs presentes
    npcs: List[str]            # IDs de NPCs en esta ubicación
    
    # Modificaciones del jugador
    cambios_jugador: List[Dict] # Acciones que modificaron el lugar
    
    # Puntos de interés
    pois: List[Dict]           # Lugares especiales
```

---

## Flujo de Generación

### Al Crear el Mundo (Nueva Partida)

```
1. Generar semilla del mundo
2. Cargar World Lore (estático)
3. Generar Historia Procedural (100 años):
   └─ Para cada año (1-100):
      ├─ Determinar eventos principales (guerras, ascensos, caídas)
      ├─ Generar NPCs importantes
      ├─ Crear artefactos legendarios
      ├─ Establecer relaciones entre facciones
      └─ Modificar geografía según desastres
4. Inicializar Live History (vacío)
5. Guardar todo en save file
```

### Durante el Gameplay

```
1. Jugador explora → Solicita evento
2. Context Builder construye contexto:
   ├─ Últimos 5 eventos del jugador
   ├─ Historia de la ubicación (eventos procedurales)
   ├─ NPCs cercanos y su estado
   └─ Lore relevante (facciones, conflictos)
3. LLM genera evento con contexto
4. Storyteller guarda evento en Live History
5. Actualizar estados afectados (NPCs, ubicaciones)
```

---

## Contexto para el LLM

El Context Builder genera un prompt estructurado:

```
CONTEXTO DEL MUNDO:
- Año actual: 101 (100 años después de la fundación)
- Ubicación: Bosque Ancestral (coordenadas 12, -5)
- Región: Valle de Sombras

HISTORIA DE LA UBICACIÓN:
- Año 23: Batalla de los Susurros - Los elfos nocturnos defendieron este bosque de las hordas oscuras.
- Año 67: Un druida llamado Aldric encontró un manantial sagrado aquí.
- Año 89: La plaga del norte mató a muchos de los habitantes originales.

NPCS CERCANOS:
- Elena (comerciante): Afinidad 45/100. Te vendió pociones la semana pasada.
- Guardia Marcus: Afinidad 10/100. Desconfía de los forasteros.

EVENTOS RECIENTES DEL JUGADOR:
- Ayer: Derrotaste a un lobo salvaje cerca de aquí.
- Hace 3 días: Ayudaste a un viajero perdido en el camino.
- Hace 1 semana: Encontraste ruinas antiguas al este.

LORE RELEVANTE:
- Los elfos nocturnos protegían este bosque hace siglos.
- Se dice que un artefacto antiguo está oculto en algún lugar del bosque.
- Las hadas son comunes pero esquivas en esta región.

TIPO DE EVENTO SOLICITADO: encuentro_npc
RARITY: raro

GENERA UN EVENTO COHERENTE CON ESTE CONTEXTO.
```

---

## Preguntas para Diseño

### World Lore (Historia Base)

1. **¿Cuál es el nombre del mundo?** Siempre será aleatorio. Pediremos a la LLM que genere varios nombres y luego que haya un sistema que lo elija al azar.
2. **¿Cuál es la cosmología?** Que la LLM genere una cosmología única para cada mundo.
3. **¿Cuáles son las facciones principales?** Que la LLM genere facciones únicas para cada mundo.
4. **¿Cuál es el conflicto central?** hay que fundamentar que han pasado varios milenios, no solo 100 años. El mundo en el que se vive actualmente directamente es un mundo bastante neutral, no existe el mal total pero tampoco la paz mundial. Desde la creación, las entidades cosmologicas dotaron a ciertos seres humanos con la capacidad de exploración, un don unico que permite descubrir cosas en donde otros no la ven. De ahi viene la base del juego, el explorar areas y descubrir. Sin embargo, las guerras y la codicia humana ha provocado que poco a poco el don de las entidades cosmologicas se fuese devaneciendo. Han pasado más de mil años desde el nacimiento del ultimo humano aventurero. Tu eres el primero en mil años en nacer con este don. Ahora esta en tu decisión saber que hacer, que haras con tu vida.
5. **¿Qué razas habitan el mundo?** Usemos las clasicas de la fantasia: Elfos, Orcos, Enanos, etc. Hagamos una lista para esto.
6. **¿Cuál es la geografía importante?** usaremos el sistema del mundo procedural que tenemos.

### Procedural History

1. **¿Qué tan detallada debe ser la historia de 100 años?**
   - Solo eventos mayores (guerras, ascensos)
   - Eventos menores también (NPCs individuales, descubrimientos)

Todo.

2. **¿Cómo afecta la historia al gameplay actual?**
   - NPCs con historias familiares
   - Ruinas de ciudades destruidas
   - Artefactos perdidos
   - Tensiones entre facciones

Todo. 

3. **¿Cuántos eventos por año?**
   - 1-3 eventos mayores por año
   - Eventos menores aleatorios

Algo aleatorio.

### Live History

1. **¿Cuántos eventos del jugador se guardan?**
   - Últimos 50 eventos
   - Todos (con límite de almacenamiento)

Todo.

2. **¿Cómo se relacionan los eventos?**
   - Cadenas de consecuencias
   - Eventos independientes

Cadenas de consecuencias y eventos independientes.
---

## Próximos Pasos

1. **Definir World Lore** - Historia base del mundo
2. **Implementar `WorldLore`** - Modelo de datos estático
3. **Implementar `ProceduralHistoryGenerator`** - Generador de 100 años
4. **Implementar `LiveHistory`** - Sistema de eventos en tiempo real
5. **Implementar `ContextBuilder`** - Constructor de contexto para LLM
6. **Integrar con `EventoGenerator`** - Usar contexto en generación de eventos

---

## Ejemplo: Historia Procedural de 100 Años

```
AÑO 1: Fundación del Reino de Valdris
AÑO 3: Los Enanos del Vacío descubren minas de obsidiana
AÑO 7: Primera Guerra de las Sombras - Valdris vs Hordas Oscuras
AÑO 12: Nace Elena la Curandera (NPC futuro)
AÑO 15: Tratado de Paz del Valle
AÑO 23: Batalla de los Susurros en el Bosque Ancestral
AÑO 30: El Círculo Arcano descubre la magia del vacío
AÑO 35: Plaga del Norte - miles mueren
AÑO 40: Construcción de la Gran Muralla
AÑO 50: Segunda Guerra de las Sombras
AÑO 55: Muere el Rey Aldric I, asciende su hijo Aldric II
AÑO 67: El druida Aldric encuentra el Manantial Sagrado
AÑO 75: Los Errantes se establecen en las tierras salvajes
AÑO 89: Plaga del Norte (segunda ola)
AÑO 95: Descubrimiento de ruinas antiguas al este
AÑO 100: El jugador comienza su aventura
```


Si pero mas descriptivo.
---

## Notas de Implementación

- **Determinismo**: Todo lo procedural debe ser reproducible con la semilla
- **Persistencia**: Guardar en save file, no regenerar al cargar
- **Performance**: Cachear contexto, no regenerar cada vez
- **Fallback**: Si el LLM falla, usar eventos hardcodeados