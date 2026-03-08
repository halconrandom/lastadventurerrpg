# Sistema de Experiencia - Last Adventurer

## Filosofía del Sistema

Sistema híbrido inspirado en **Diablo** + **Skyrim**:
- Crecimiento por uso de habilidades (Skyrim)
- Curva de experiencia progresiva (Diablo)
- Libertad total: el jugador se define mediante sus acciones

---

## Arquitectura del Personaje

```
Personaje
├── Stats (componente central)
│   ├── Nivel (1-100)
│   ├── Experiencia acumulada
│   ├── Puntos disponibles para distribuir
│   ├── HP, ATK, DEF, Velocidad, Crítico, Evasión, Mana, Stamina
│   └── Métodos: ganar_experiencia(), subir_nivel(), asignar_X()
│
├── SistemaHabilidades
│   ├── Espada      → nivel (1-100), exp, perks
│   ├── Espadón     → nivel (1-100), exp, perks
│   ├── Arco        → nivel (1-100), exp, perks
│   ├── Magia       → nivel (1-100), exp, perks
│   ├── Dagas       → nivel (1-100), exp, perks
│   ├── Defensa     → nivel (1-100), exp (ESPECIAL: suma a Stats.DEF)
│   └── [extensible] → futuras armas/habilidades
│
└── Perks (implementar después)
    ├── Pasivos (siempre activos)
    └── Activos (consumen recursos)
```

---

## Relación con Sistema de Stats

**IMPORTANTE:** Stats es el componente central que maneja TODO:

| Sistema | Responsabilidad |
|---------|-----------------|
| **Stats** | Nivel, Experiencia, HP, ATK, DEF, Velocidad, Crítico, Evasión, Mana, Stamina y puntos distribuibles |
| **SistemaHabilidades** | Habilidades de combate (Espada, Arco, etc.) con su nivel/exp independiente |
| **Perks** | Se implementarán después (placeholder por ahora) |

**Flujo de puntos:**
```
1. Stats.ganar_experiencia(cantidad) → suma exp
2. Si sube de nivel → Stats.subir_nivel() → +puntos_disponibles
3. Jugador distribuye puntos via Stats.asignar_X()
```

---

## Decisiones de Integración (Definidas)

- [x] **¿Puntos por nivel van a Stats o se manejan por separado?**
  - ✅ Respuesta: **Todo en Stats** - Nivel, experiencia y puntos viven en Stats

- [x] **¿La habilidad Defensa afecta Stats.DEF o es separado?**
  - ✅ Respuesta: **Suma a la reducción total** - Nivel Habilidad Defensa suma a Stats.get_def()

- [x] **¿Dónde se guardan los puntos asignados?**
  - ✅ Respuesta: **Solo en Stats** - No duplicar

- [x] **¿ExperienciaPersonaje se elimina y se usa solo Stats?**
  - ✅ Respuesta: **Sí, se elimina** - Stats maneja nivel y experiencia del personaje

---

## Sistema de Experiencia

### Experiencia de Personaje (Nivel General)

| Acción | Experiencia ganada |
|--------|-------------------|
| Atacar con cualquier arma | +exp Personaje |
| Matar enemigo | +exp Personaje (bonus) |
| Completar misión | +exp Personaje (variable) |
| Bloquear ataque | +exp Personaje + exp Defensa |

### Experiencia de Habilidad

| Acción | Experiencia ganada |
|--------|-------------------|
| Atacar con Espada | +exp Espada |
| Atacar con Arco | +exp Arco |
| Usar Magia | +exp Magia |
| Bloquear ataque | +exp Defensa |

---

## Cálculo de Daño

**Integración con Stats:**
- `Stats.get_atk()` proporciona el ATK base
- `Habilidad.obtener_multiplicador()` proporciona el multiplicador por nivel

```
Daño Total = (Stats.get_atk() + Daño Arma) × Habilidad.obtener_multiplicador()
```

### Ejemplo:
```
Stats ATK: 20 (10 base + 10 por puntos)
Arma: Espada de Hierro (+5 ATK)
Nivel Espada: 10 (multiplicador: 1 + 10 × 0.05 = 1.5)

Daño = (20 + 5) × 1.5 = 37.5 → 37
```

### Daño Crítico:
```
Si Stats.get_critico() se activa:
Daño Crítico = Daño Total × 1.5
```

---

## Sistema de Defensa

### Cómo subir Defensa:
- **Bloquear ataques** → +exp Defensa
- **NO** recibir daño (evitamos farmeo intenso)

### Cálculo de reducción (integrado con Stats):
```
Reducción Total = Stats.get_def() + (Nivel Habilidad Defensa × 1%)
Cap: 80%
```

### Ejemplo:
```
Stats DEF: 15% (0 base + 15 puntos)
Nivel Habilidad Defensa: 10

Reducción Total = 15% + 10% = 25%
Enemigo ataca con 50 de daño
Daño Recibido = 50 × (1 - 0.25) = 37.5 → 37
```

### Contraataque tras Bloqueo:
```
Chance = 10% + (Nivel Habilidad Defensa × 1%)
```

Ver más detalles en `SISTEMA_STATS.md`

---

## Sistema de Nivel y Puntos

### Subir de Nivel:
- Cada nivel requiere más experiencia (curva tipo Diablo)
- Al subir, recibes **Puntos de Atributo** que van a `Stats.puntos_disponibles`

### Puntos por Nivel (escalan):
| Rango de Nivel | Puntos por Nivel |
|----------------|------------------|
| 1-10 | 5 puntos |
| 11-20 | 7 puntos |
| 21-50 | 10 puntos |
| 51-100 | 15 puntos |

### Distribución de Puntos:
Los puntos se asignan a través de `Stats.asignar_X()`:

| Método | Efecto |
|--------|--------|
| `Stats.asignar_hp()` | +10 HP |
| `Stats.asignar_atk()` | +2 ATK |
| `Stats.asignar_def()` | +1% reducción |
| `Stats.asignar_velocidad()` | +1 Velocidad |
| `Stats.asignar_critico()` | +1% crítico |
| `Stats.asignar_evasion()` | +1% evasión |
| `Stats.asignar_mana()` | +10 Mana |
| `Stats.asignar_stamina()` | +2 Stamina |

### Fórmula de experiencia por nivel:
```
Exp necesaria = Nivel × 100 × (1 + Nivel × 0.1)

Ejemplos:
- Nivel 1 → 110 exp
- Nivel 2 → 240 exp
- Nivel 10 → 2000 exp
- Nivel 50 → 30000 exp
```

---

## Sistema de Perks

### Desbloqueo:
- Variable según habilidad
- Se desbloquean al alcanzar ciertos niveles de habilidad

### Tipos:

#### Pasivos (siempre activos):
| Habilidad | Nivel | Perk | Efecto |
|-----------|-------|------|--------|
| Espada | 5 | Filo Afilado | +10% daño con espadas |
| Espada | 15 | Contraataque | 5% probabilidad de ataque doble |
| Defensa | 10 | Piel Dura | +5% reducción de daño |
| Magia | 20 | Mana Expandido | +20 mana máximo |

#### Activos (consumen recursos):
| Habilidad | Nivel | Perk | Efecto | Costo |
|-----------|-------|------|--------|-------|
| Espada | 10 | Golpe Giratorio | Daño en área | 15 stamina |
| Arco | 12 | Disparo Múltiple | 3 flechas a la vez | 20 stamina |
| Magia | 15 | Bola de Fuego | Daño mágico en área | 30 mana |
| Defensa | 20 | Escudo de Hierro | Inmune 3 segundos | 50 stamina |

---

## Niveles Máximos

| Sistema | Nivel Máximo |
|---------|--------------|
| Personaje | 100 |
| Habilidades de Combate | 100 |
| Defensa | 100 |

---

## Flujo de Combate (Ejemplo)

```
1. Jugador ataca con Espada
   → +exp Espada
   → +exp Personaje
   → Cálculo de daño

2. Enemigo ataca
   → Jugador puede: Esquivar, Bloquear, Recibir

3. Si Bloquea:
   → +exp Defensa
   → +exp Personaje
   → Daño reducido

4. Si Recibe:
   → Sin exp
   → Daño completo aplicado
```

---

## Archivos a Crear/Modificar

| Archivo | Estado | Propósito |
|---------|--------|-----------|
| `models/stats.py` | ⚠️ Modificar | Agregar nivel, experiencia, métodos ganar_experiencia(), subir_nivel() |
| `models/experiencia.py` | ⚠️ Modificar | Eliminar ExperienciaPersonaje, mantener Habilidad y SistemaHabilidades |
| `models/personaje.py` | ⚠️ Modificar | Agregar SistemaHabilidades como atributo |
| `models/perk.py` | ❌ Después | Clase para perks (placeholder) |
| `data/habilidades.json` | ❌ Después | Datos de habilidades |
| `data/perks.json` | ❌ Después | Datos de perks |

---

## Preguntas de Implementación

### Integración Stats-Experiencia
- [x] **¿ExperienciaPersonaje se mantiene o se elimina?**
  - ✅ Respuesta: **Se elimina** - Stats maneja todo

- [x] **¿Dónde va el nivel del personaje?**
  - ✅ Respuesta: **En Stats** - Stats.nivel y Stats.experiencia

- [x] **¿Cómo se conectan al guardar/cargar?**
  - ✅ Respuesta: **Stats.to_dict() y Stats.from_dict()** - Serialización directa

### Habilidades
- [x] **¿Las habilidades se guardan en el JSON de experiencia o separado?**
  - ✅ Respuesta: **En el JSON principal** - Sección "habilidades" en el save

- [x] **¿La habilidad Defensa es especial o igual que las demás?**
  - ✅ Respuesta: **Especial** - No es un arma, afecta stats de defensa (suma a reducción)

### Perks
- [x] **¿Los perks se implementan ahora o después?**
  - ✅ Respuesta: **Después** - Placeholder por ahora, sistema completo más adelante

---

## Notas de Diseño

- **Sin clases definidas**: El jugador empieza con stats base y se define por sus acciones
- **Extensible**: Fácil agregar nuevas armas/habilidades
- **Balance**: Evitar farmeo intenso (no dar exp por recibir daño)
- **Libertad**: Puntos distribuibles al subir de nivel