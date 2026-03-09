# Sistema de Tiempo - Last Adventurer

## Visión General

El sistema de tiempo gestiona el ciclo día/noche, las estaciones y el tiempo transcurrido en el mundo del juego. Es fundamental para la inmersión y afecta otros sistemas como clima, NPCs, eventos y exploración.

---

## Decisiones Tomadas (Iteración 1)

| Aspecto | Decisión | Notas |
|---------|----------|-------|
| Escala de tiempo | 2 min real = 1 hora juego | 48 min = 1 día completo |
| Estaciones | 4 estaciones de 30 días | Variación por bioma |
| Avance del tiempo | Por acción | No es tiempo real |
| Eventos | Todos los tipos | Generados por LLM según NPC |

---

## Componentes del Sistema

### 1. Ciclo Día/Noche

El tiempo del mundo avanza **por acción del jugador**, afectando:

- **Iluminación**: Afecta visibilidad y exploración
- **Comportamiento de NPCs**: Horarios de sueño, trabajo, etc.
- **Eventos**: Algunos eventos solo ocurren de noche/día
- **Clima**: Algunos climas son más probables en ciertas horas

#### Fases del Día

| Fase | Horas | Luz | Descripción |
|------|-------|-----|-------------|
| Madrugada | 0-5 | 10% | Oscuridad total, peligros aumentan |
| Amanecer | 6-7 | 30% | Transición, NPCs despiertan |
| Día | 8-17 | 100% | Luz plena, actividad normal |
| Atardecer | 18-19 | 60% | Transición, NPCs se retiran |
| Anochecer | 20-21 | 30% | Oscuridad creciente |
| Noche | 22-23 | 10% | Oscuridad, peligros aumentan |

---

### 2. Tiempo por Acción (Detalle Técnico)

**Problema identificado**: Si el tiempo avanza por acción, ¿cuánto tiempo pasa por cada tipo de acción?

#### Propuesta de Costos de Tiempo por Acción

| Acción | Tiempo que Avanza | Justificación |
|--------|-------------------|----------------|
| **Exploración** | | |
| Moverse a tile adyacente | 15 min | Caminar un tile |
| Explorar tile (revelar) | 30 min | Buscar, investigar |
| Descansar corto | 1 hora | Recuperar stamina |
| Descansar largo | 8 horas | Dormir hasta mañana |
| **Combate** | | |
| Iniciar combate | 5 min | Preparativos |
| Cada turno de combate | 10 seg | Acción rápida |
| Combate completo (promedio) | 5-15 min | Dependiendo duración |
| **Interacción** | | |
| Hablar con NPC | 15 min | Conversación corta |
| Negociar/Comerciar | 30 min | Intercambio |
| Leer libro/documento | 30 min | Estudiar información |
| **Viaje** | | |
| Viaje corto (misma zona) | 1-2 horas | Dentro de un área |
| Viaje largo (otra zona) | 4-8 horas | Entre zonas |
| Viaje muy largo (otra región) | 1-3 días | Entre regiones |

**Pregunta 7**: ¿Estos tiempos te parecen correctos? ¿Quieres ajustar alguno?

---

### 3. Sistema de Estaciones por Bioma

**Decisión**: 4 estaciones base de 30 días, pero variación según bioma.

#### Tabla de Estaciones por Bioma

| Bioma | Estaciones | Duración | Efectos |
|-------|------------|----------|---------|
| **Bosque** | Primavera, Verano, Otoño, Invierno | 30 días c/u | Normal |
| **Desierto** | Temporada Fría, Temporada Caliente | 60 días c/u | Extremos |
| **Tundra** | Invierno Eterno | 120 días | Siempre frío |
| **Jungla** | Lluvias, Sequía | 60 días c/u | Humedad extrema |
| **Pantano** | Húmedo, Más Húmedo | 60 días c/u | Siempre húmedo |
| **Montaña** | Las 4 estaciones | 30 días c/u | Invierno más largo |
| **Costa** | Las 4 estaciones | 30 días c/u | Clima moderado |

**Pregunta 8**: ¿Quieres añadir más biomas o modificar los existentes?

---

### 4. Tiempo Inicial del Jugador

**Pregunta 5 (pendiente)**: ¿Cuándo empieza el jugador?

#### Opciones

| Opción | Descripción | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| A | Mañana del día 1, primavera, año 1 | Predecible, tutorial amigable | Menos variedad |
| B | Aleatorio (hora, día, estación) | Cada partida es única | Puede empezar de noche (difícil) |
| C | Según zona de spawn | Coherencia con el mundo | Requiere sistema de spawn |
| D | Configurable al crear partida | El jugador elige | Más complejo |

**Pregunta 9**: ¿Cuál prefieres?

---

### 5. Pausas del Tiempo

**Pregunta 6 (pendiente)**: ¿El tiempo se pausa?

#### Opciones

| Opción | Combate | Diálogos | Menús | Descripción |
|--------|---------|----------|-------|-------------|
| A | Pausa | Pausa | Pausa | Tiempo nunca avanza sin input |
| B | No pausa | No pausa | No pausa | Tiempo siempre avanza |
| C | No pausa | Pausa | Pausa | Combate toma tiempo real |
| D | Pausa | No pausa | Pausa | Diálogos toman tiempo |

**Mi recomendación**: Opción A. Si el tiempo avanza por acción, pausar en menús/diálogos es natural. El combate ya tiene su propio costo de tiempo.

**Pregunta 10**: ¿Cuál prefieres?

---

### 6. Eventos Temporales

**Decisión**: Todos los tipos, generados por LLM según NPC.

#### Estructura de Eventos Temporales

```python
class EventoTemporal:
    id: str                    # Identificador único
    nombre: str                 # Nombre del evento
    tipo: str                   # horario/diario/semanal/estacional/unico
    trigger: dict               # Condiciones de activación
    duracion: int               # Duración en minutos (0 = instantáneo)
    efectos: list               # Efectos al activarse
    repite: bool                # Si se repite
    intervalo: int              # Intervalo de repetición (días)
    
    # Ejemplo: Tienda
    # {
    #   "tipo": "horario",
    #   "trigger": {"hora_inicio": 8, "hora_fin": 20},
    #   "duracion": 0,
    #   "efectos": [{"tipo": "tienda_abierta", "npc_id": "comerciante_1"}]
    # }
```

#### Generación por LLM

El LLM generará eventos basándose en:

1. **NPC**: Personalidad, trabajo, relaciones
2. **Ubicación**: Zona, bioma, tipo de asentamiento
3. **Tiempo actual**: Hora, día, estación
4. **Historia**: Eventos pasados, relaciones previas

**Pregunta 11**: ¿El LLM debe generar eventos al crear el NPC o dinámicamente durante el juego?

---

### 7. Persistencia del Tiempo

#### Datos a Persistir

```json
{
  "tiempo": {
    "tick_actual": 15234,
    "hora_actual": 14,
    "dia_actual": 42,
    "estacion_actual": "verano",
    "año_actual": 1,
    "configuracion": {
      "velocidad": 1.0,
      "pausado": false
    },
    "eventos_programados": [
      {
        "id": "festival_primavera",
        "fecha": {"año": 1, "dia": 15},
        "repetir": true,
        "intervalo_dias": 365
      }
    ]
  }
}
```

---

### 8. Integración con Otros Sistemas

#### Clima

El sistema de tiempo afecta el clima:

- **Hora**: Algunos climas son más probables de noche
- **Estación**: Invierno = más nieve, Verano = más calor
- **Bioma**: Cada bioma tiene sus propias reglas

#### NPCs

Los NPCs tienen horarios:

- **Sueño**: Horas de descanso
- **Trabajo**: Horas de actividad
- **Comida**: Horarios de comida
- **Festividades**: Días especiales

#### Exploración

- **Visibilidad**: Reducida de noche
- **Peligros**: Aumentan de noche
- **POIs**: Algunos solo accesibles de día/noche

#### Combate

- **Costo de tiempo**: Cada combate avanza el reloj
- **Condiciones**: Noche = más peligros, menos visibilidad

---

## Preguntas para la Segunda Iteración

### Pregunta 7: Costos de Tiempo por Acción
¿Los tiempos propuestos (15 min moverse, 30 min explorar, etc.) te parecen correctos?

### Pregunta 8: Biomas y Estaciones
¿Quieres añadir más biomas o modificar los existentes?

### Pregunta 9: Tiempo Inicial
¿Cuándo empieza el jugador? (Mañana día 1 / Aleatorio / Según zona / Configurable)

### Pregunta 10: Pausas del Tiempo
¿El tiempo se pausa en combate/diálogos/menús?

### Pregunta 11: Generación de Eventos por LLM
¿El LLM genera eventos al crear el NPC o dinámicamente durante el juego?

---

## Estructura de Archivos Propuesta

```
backend/src/systems/
├── tiempo.py              # Sistema principal de tiempo
├── eventos_temporales.py  # Eventos programados
├── bioma_estaciones.py    # Estaciones por bioma
└── ...

backend/src/api/
├── tiempo.py              # Endpoints de tiempo
└── ...

frontend/src/hooks/
├── useTiempo.ts           # Hook para tiempo
└── ...

frontend/src/components/
├── TimeDisplay.tsx        # Componente de reloj
└── ...
```

---

## Próximos Pasos

1. ✅ Primera iteración completada
2. ⏳ Segunda iteración (preguntas 7-11)
3. 🔜 Implementación en `experiments/tiempo/`
4. 🔜 Tests de validación
5. 🔜 Integración al backend principal