# Sistema de Tiempo - Last Adventurer

## Visión General

El sistema de tiempo gestiona el ciclo día/noche, las estaciones y el tiempo transcurrido en el mundo del juego. Es fundamental para la inmersion y afecta otros sistemas como clima, NPCs, eventos y exploración.

---

## Componentes del Sistema

### 1. Ciclo Día/Noche

El tiempo del mundo avanza de forma continua, afectando:

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

#### Escala de Tiempo

**Pregunta 1**: ¿Cuál debería ser la relación tiempo real vs tiempo de juego?

| Opción | Tiempo Real | Tiempo Juego | Descripción |
|--------|-------------|--------------|-------------|
| A | 1 minuto | 1 hora | 1 día = 24 minutos reales |
| B | 2 minutos | 1 hora | 1 día = 48 minutos reales |
| C | 5 minutos | 1 hora | 1 día = 2 horas reales |
| D | Configurable | Variable | El jugador ajusta la velocidad |

**Mi recomendación**: Opción B (2 min = 1 hora). Un día completo en 48 minutos es suficiente para experimentar el ciclo sin que se sienta eterno.

---

### 2. Sistema de Estaciones

Las estaciones afectan el clima, disponibilidad de recursos y eventos disponibles.

#### Estaciones del Año

| Estación | Duración | Efectos Principales |
|----------|----------|---------------------|
| Primavera | 30 días | Lluvias frecuentes, flora activa, animales jóvenes |
| Verano | 30 días | Calor, sequía posible, días más largos |
| Otoño | 30 días | Cosecha, clima variable, migraciones |
| Invierno | 30 días | Frío extremo, recursos escasos, noches largas |

**Pregunta 2**: ¿El año del juego debe tener 4 estaciones iguales o algo diferente?

- A) 4 estaciones de 30 días cada una (120 días/año)
- B) Estaciones de duración variable según bioma
- C) Sistema de lunas/meses diferente (ej: 13 meses de 28 días)
- D) Otra idea

---

### 3. Tiempo Transcurrido

El juego lleva cuenta del tiempo total transcurrido desde el inicio de la partida.

#### Datos Almacenados

```python
class TiempoMundo:
    # Tiempo absoluto
    tick_actual: int          # Ticks totales desde inicio
    hora_actual: int          # 0-23
    dia_actual: int           # Día desde inicio
    estacion_actual: str      # primavera/verano/otonno/invierno
    año_actual: int           # Año desde inicio
    
    # Configuración
    ticks_por_hora: int       # Velocidad del tiempo
    dias_por_estacion: int    # Duración de estaciones
    estaciones: list          # Orden de estaciones
    
    # Estado
    pausado: bool             # Tiempo pausado
    multiplicador: float      # Velocidad actual (1x, 2x, etc.)
```

**Pregunta 3**: ¿El tiempo debe avanzar solo o solo cuando el jugador hace acciones?

- A) **Tiempo continuo**: Avanza automáticamente en tiempo real
- B) **Tiempo por acción**: Avanza con cada acción del jugador (explorar, combatir, etc.)
- C) **Híbrido**: Tiempo real en zonas seguras, por acción en exploración/combate
- D) **Configurable**: El jugador elige el modo

---

### 4. Eventos Temporales

Algunos eventos están ligados al tiempo:

#### Tipos de Eventos Temporales

| Tipo | Ejemplo | Trigger |
|------|---------|---------|
| Horarios | Tienda abre 8:00-20:00 | Hora específica |
| Diarios | Mercado cada día 10 | Cada día a X hora |
| Semanales | Festival cada 7 días | Cada X días |
| Estacionales | Cosecha en otoño | Estación específica |
| Únicos | Eclipse solar año 1 | Fecha exacta |

**Pregunta 4**: ¿Qué eventos temporales debería haber desde el inicio?

---

### 5. Persistencia del Tiempo

El tiempo debe guardarse y cargarse correctamente.

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

### 6. Integración con Otros Sistemas

#### Clima

El sistema de tiempo afecta el clima:

- **Hora**: Algunos climas son más probables de noche
- **Estación**: Invierno = más nieve, Verano = más calor

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

---

## Preguntas para la Primera Iteración

### Pregunta 1: Escala de Tiempo
¿Cuál debería ser la relación tiempo real vs tiempo de juego?

### Pregunta 2: Estaciones
¿El año del juego debe tener 4 estaciones iguales o algo diferente?

### Pregunta 3: Avance del Tiempo
¿El tiempo debe avanzar solo o solo cuando el jugador hace acciones?

### Pregunta 4: Eventos Temporales
¿Qué eventos temporales debería haber desde el inicio?

### Pregunta 5: Tiempo Inicial
¿El jugador empieza en un momento específico (ej: mañana del día 1) o es aleatorio?

### Pregunta 6: Pausas
¿El tiempo se pausa durante combate, diálogos, menús? ¿O sigue avanzando?

---

## Estructura de Archivos Propuesta

```
backend/src/systems/
├── tiempo.py           # Sistema principal de tiempo
├── eventos_temporales.py  # Eventos programados
└── ...

backend/src/api/
├── tiempo.py           # Endpoints de tiempo
└── ...

frontend/src/hooks/
├── useTiempo.ts        # Hook para tiempo
└── ...
```

---

## Próximos Pasos

1. Responder las preguntas de esta iteración
2. Segunda iteración con más detalle técnico
3. Implementación en `experiments/tiempo/`
4. Tests de validación
5. Integración al backend principal