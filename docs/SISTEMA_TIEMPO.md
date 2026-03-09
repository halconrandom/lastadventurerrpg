# Sistema de Tiempo - Last Adventurer

## Visión General

El sistema de tiempo gestiona el ciclo día/noche, las estaciones y el tiempo transcurrido en el mundo del juego. Es fundamental para la inmersión y afecta otros sistemas como clima, NPCs, eventos y exploración.

---

## Decisiones Finales

| Aspecto | Decisión | Notas |
|---------|----------|-------|
| Escala de tiempo | 2 min real = 1 hora juego | 48 min = 1 día completo |
| Estaciones | 4 estaciones de 30 días | Variación por bioma |
| Avance del tiempo | Por acción | No es tiempo real |
| Eventos | Todos los tipos | Generados por LLM dinámicamente |
| Tiempo inicial | Aleatorio (safe start) | Siempre de día, hora aleatoria |
| Pausas | Pausa total | Combate, diálogos, menús |
| Dependencia | Requiere sistema de mapa | Para distancias entre lugares |

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

### 2. Tiempo por Acción

El tiempo avanza según la acción que realice el jugador.

#### Costos de Tiempo por Acción

| Acción | Tiempo que Avanza | Justificación |
|--------|-------------------|----------------|
| **Exploración** | | |
| Moverse a tile adyacente | 5 min | Caminar un tile |
| Explorar tile (revelar) | 15 min | Buscar, investigar |
| **Descanso** | | |
| Descanso corto | 1 hora | Recuperar stamina (+20%) |
| Dormir | 8 horas | Recuperar todo (+100% stamina, +salud) |
| **Viaje** | | |
| Viaje corto | 1-2 horas | Dentro de un área |
| Viaje largo | 4-8 horas | Entre zonas |
| Viaje muy largo | 1-3 días | Entre regiones |

**Nota**: Los tiempos de viaje se calculan proceduralmente según distancias y rutas definidas por el sistema de mapa.

> Ejemplo: *"De pueblo A a B son 2 días por Bosque X, pero 4 días por Colinas X"*

#### Sistema de Descanso

El jugador puede dormir a cualquier hora:

- **Dormir siempre avanza 8 horas** de tiempo
- Si te acuestas a las 2 PM, despiertas a las 10 PM (de noche)
- No hay penalizaciones por dormir de día, pero el tiempo avanza igual
- El jugador decide cuándo descansar según su estrategia

---

### 3. Sistema de Estaciones por Bioma

**Estructura**: 4 estaciones base de 30 días, con variación según bioma.

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

---

### 4. Tiempo Inicial del Jugador

**Decisión**: Safe start con hora aleatoria.

| Aspecto | Valor |
|---------|-------|
| Hora inicial | Aleatoria entre 8:00 y 17:00 (siempre de día) |
| Día inicial | 1 |
| Estación inicial | Primavera |
| Año inicial | 1 |

**Justificación**: El jugador siempre empieza con luz, pero la hora varía para dar variedad a cada partida.

---

### 5. Pausas del Tiempo

**Decisión**: Pausa total.

| Situación | Tiempo |
|-----------|--------|
| Combate | Pausado |
| Diálogos | Pausado |
| Menús | Pausado |
| Exploración | Avanza por acción |

**Justificación**: Si el tiempo avanza por acción, pausar en menús/diálogos es natural y consistente.

---

### 6. Eventos Temporales

**Decisión**: Generados dinámicamente por el LLM.

#### Estructura de Eventos Temporales

```python
class EventoTemporal:
    id: str                    # Identificador único
    nombre: str                # Nombre del evento
    tipo: str                  # horario/diario/semanal/estacional/unico
    trigger: dict              # Condiciones de activación
    duracion: int              # Duración en minutos (0 = instantáneo)
    efectos: list              # Efectos al activarse
    repite: bool               # Si se repite
    intervalo: int             # Intervalo de repetición (días)
```

#### Generación por LLM

El LLM genera eventos dinámicamente basándose en:

1. **NPC**: Personalidad, trabajo, relaciones
2. **Ubicación**: Zona, bioma, tipo de asentamiento
3. **Tiempo actual**: Hora, día, estación
4. **Historia**: Eventos pasados, relaciones previas

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

#### Sistema de Mapa (Dependencia)

El sistema de mapa define:
- Distancias entre ubicaciones
- Rutas disponibles
- Tiempos de viaje

El sistema de tiempo consume estos datos para calcular el tiempo de viaje.

#### Clima

- **Hora**: Algunos climas son más probables de noche
- **Estación**: Invierno = más nieve, Verano = más calor
- **Bioma**: Cada bioma tiene sus propias reglas

#### NPCs

- **Sueño**: Horas de descanso
- **Trabajo**: Horas de actividad
- **Comida**: Horarios de comida
- **Festividades**: Días especiales

#### Exploración

- **Visibilidad**: Reducida de noche
- **Peligros**: Aumentan de noche
- **POIs**: Algunos solo accesibles de día/noche

#### Combate

- **Costo de tiempo**: Cada combate avanza el reloj (5 min inicio + turnos)
- **Condiciones**: Noche = más peligros, menos visibilidad

---

## Estructura de Archivos

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

## Dependencias

| Sistema | Relación |
|---------|----------|
| **Mapa** | Requerido para distancias y rutas |
| Clima | Recibe hora y estación |
| NPCs | Recibe hora para horarios |
| Exploración | Recibe hora para visibilidad |
| Combate | Recibe hora para condiciones |
| LLM | Genera eventos dinámicos |

---

## Próximos Pasos

1. ✅ Documento completado
2. 🔜 Implementar sistema de mapa primero
3. 🔜 Implementar sistema de tiempo en `experiments/tiempo/`
4. 🔜 Tests de validación
5. 🔜 Integración al backend principal