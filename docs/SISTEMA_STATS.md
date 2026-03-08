# Sistema de Stats - Last Adventurer

## Concepto

Los stats son los atributos base del personaje que determinan su capacidad en combate, exploración y otras mecánicas del juego.

---

## Stats Principales

### HP (Puntos de Vida)
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Cantidad de daño que puede recibir antes de morir |
| **Base** | 100 HP |
| **Por punto** | +10 HP por punto asignado (se suma al base) |
| **Regeneración** | Solo con descanso largo o pociones |

**Nota:** Los puntos se suman directamente al valor base.

### ATK (Ataque)
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Daño base que inflige el personaje |
| **Base** | 10 ATK inicial |
| **Por punto** | +2 ATK por punto asignado (se suma al base) |
| **Cálculo** | `Daño = (ATK Total + Daño Arma) × Multiplicador Habilidad` |

**Ejemplo de asignación:**
```
ATK Base inicial: 10
Asignas 5 puntos a ATK: +10 ATK (5 puntos × 2)
ATK Total nuevo: 20 (el base ahora es 20, no 10)
```

**Nota:** Los puntos se suman directamente al valor base. No se calculan por separado.

### DEF (Defensa)
| Aspecto | Descripción |
|---------|-------------|
| **Función | Reducción porcentual del daño recibido |
| **Base** | 0% reducción |
| **Por punto** | +1% reducción por punto asignado |
| **Máximo** | 80% reducción (cap) |
| **Cálculo** | `Daño Recibido = Daño Enemigo × (1 - DEF%)` |

---

## Stats Secundarios

### Velocidad
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Determina orden de turnos y cantidad de ataques por turno |
| **Base** | 10 |
| **Por punto** | +1 velocidad por punto asignado |

**Sistema de Turnos:**
1. **Orden de ataque:** Quien tenga mayor velocidad ataca primero
2. **Turnos extra:** Si tu velocidad supera al enemigo por 50% o más, ganas turnos extra

| Diferencia de Velocidad | Ataques por Turno |
|------------------------|-------------------|
| 0-49% superior | 1 ataque |
| 50-99% superior | 2 ataques |
| 100-149% superior | 3 ataques |
| 150-199% superior | 4 ataques |
| ... | +1 por cada 50% |

**Ejemplo:**
```
Tu velocidad: 100
Enemigo velocidad: 50
Diferencia: 100% superior → Atacas 3 veces (1 base + 2 extra)

Tu velocidad: 100
Enemigo velocidad: 60
Diferencia: 66% superior → Atacas 2 veces (1 base + 1 extra)
```

### Crítico
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Probabilidad de hacer más daño |
| **Base** | ¿5% base? |
| **Por punto** | ¿+1% probabilidad? |
| **Daño crítico** | ¿x1.5? ¿x2? |

EDIT: 1.5

### Evasión
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Probabilidad de esquivar un ataque completamente |
| **Base** | 10% |
| **Por punto** | +1% probabilidad |
| **Máximo** | 50% |

**Sistema de Evasión:**

| Tipo | Descripción | Efecto |
|------|-------------|--------|
| **Pasiva** | Ocurre automáticamente si decides atacar | Chance base de evadir (10% + puntos) |
| **Activa** | Decides evadir conscientemente | Siempre evade (100% éxito) |
| **Bloqueo** | Decides bloquear | Reduce daño + da exp a Defensa |

**Sistema de Bloqueo:**

| Aspecto | Descripción |
|---------|-------------|
| **Reducción de daño** | 50% del daño recibido |
| **Experiencia** | +exp a habilidad Defensa |
| **Costo** | 5 stamina |
| **Contraataque** | Chance de atacar tras bloquear exitosamente |

**Contraataque tras Bloqueo:**
- Chance base: 10%
- Se calcula: `Contraataque Base + (Nivel Defensa × 1%)`
- Si activa: Realizas un ataque básico automático tras bloquear
- No consume stamina adicional

**Ejemplo:**
```
Nivel Defensa: 15
Chance de contraataque: 10% + 15% = 25%

Enemigo ataca con 40 de daño
Bloqueas → Recibes 20 de daño (50% reducido)
Sistema calcula contraataque: 25% chance
Si activa → Atacas automáticamente al enemigo
```

**Decisiones por turno:**
- Si atacas → Evasión pasiva (chance de evadir si el enemigo contraataca)
- Si evades activamente → No recibes daño, pero no atacas
- Si bloqueas → Reduces daño, ganas exp, chance de contraatacar

### Mana
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Recurso para habilidades mágicas |
| **Base** | 100 |
| **Por punto** | +10 mana por punto asignado (se suma al base) |
| **Regeneración** | Solo con pociones o descanso largo |

**Nota:** Los puntos se suman directamente al valor base.

### Stamina
| Aspecto | Descripción |
|---------|-------------|
| **Función** | Puntos de acción por turno |
| **Base** | 10 |
| **Por punto** | +2 stamina por punto asignado |
| **Regeneración** | Se refresca completamente cada turno |

**Sistema de Acciones por Turno:**

| Acción | Costo de Stamina | Efecto |
|--------|-----------------|--------|
| Ataque básico | 10 puntos | Daño normal |
| Tomar poción | 5 puntos | Cura HP/Mana |
| Usar habilidad | Variable (10-30 puntos) | Efecto según habilidad |
| Bloquear | 5 puntos | Reduce daño 50% + chance contraataque |
| Evadir activamente | 5 puntos | Evade 100% del daño |

**Ejemplo de turno:**
```
Stamina disponible: 10

Opción 1: Ataque básico (10) → Turno terminado
Opción 2: Tomar poción (5) + Bloquear (5) → Turno terminado
Opción 3: Usar habilidad fuerte (15) → Necesitas más stamina o perk
```

**Perks que afectan Stamina:**
- Reducen costo de acciones específicas
- Aumentan stamina máxima
- Permiten recuperar stamina parcial en combate 

---


## Stats Derivados

### Daño Total
```
Daño Total = (ATK Total + Daño Arma) × (1 + Nivel Habilidad × 0.05)
```

### Daño Crítico
```
Daño Crítico = Daño Total × 1.5
```

### Reducción de Daño Total
```
Reducción = DEF Total + (Nivel Defensa × 1%)
Máximo: 80%
```

### Cálculo de Turnos Extra por Velocidad
```
Diferencia = (Velocidad Jugador - Velocidad Enemigo) / Velocidad Enemigo × 100
Turnos Extra = floor(Diferencia / 50)
Ataques Totales = 1 + Turnos Extra
```

### HP Total
```
HP Total = HP Base + (Puntos HP × 10)
```

---

## Distribución de Puntos

### Puntos por Nivel
| Nivel | Puntos Otorgados |
|-------|-----------------|
| 1-10 | 5 puntos |
| 11-20 | 7 puntos |
| 21-50 | 10 puntos |
| 51-100 | 15 puntos |

### Categorías de Asignación
| Categoría | Stats incluidos |
|-----------|----------------|
| **Vitalidad** | HP, Regeneración HP |
| **Ofensiva** | ATK, Crítico, Penetración |
| **Defensiva** | DEF, Evasión, Resistencia |
| **Utilidad** | Velocidad, Mana, Stamina |

---

## Preguntas a Definir

### Stats Principales
- [x] **¿HP base correcto?** → 100 HP
- [x] **¿ATK base correcto?** → 10 ATK
- [x] **¿DEF base correcto?** → 0% reducción
- [x] **¿Cap de DEF?** → 80% máximo

### Stats Secundarios
- [x] **¿Incluir Velocidad?** → Sí, determina orden y turnos extra
- [x] **¿Incluir Crítico?** → Sí, x1.5 daño
- [x] **¿Incluir Evasión?** → Sí, 10% base, sistema pasivo/activo
- [x] **¿Incluir Mana?** → Sí, 100 base
- [x] **¿Incluir Stamina?** → Sí, 10 base, sistema de acciones
- [x] **¿Sistema de dos recursos (Mana + Stamina)?** → Separados

### Regeneración
- [x] **¿HP se regenera solo?** → No, solo pociones o descanso largo
- [x] **¿Mana se regenera?** → No, solo pociones o descanso largo
- [x] **¿Stamina se regenera?** → Sí, cada turno

### Distribución
- [x] **¿Puntos por nivel?** → Escala con nivel
- [x] **¿Límite de puntos por stat?** → Sin límite
- [x] **¿Resetear puntos?** → Solo en lugar específico del juego

---

## Estructura JSON Propuesta

### Stats del Personaje
```json
{
  "stats": {
    "hp_base": 100,
    "hp_actual": 100,
    "puntos_hp": 0,
    "atk_base": 10,
    "puntos_atk": 0,
    "def_base": 0,
    "puntos_def": 0,
    "velocidad_base": 10,
    "puntos_velocidad": 0,
    "critico_base": 5,
    "puntos_critico": 0,
    "evasion_base": 10,
    "puntos_evasion": 0,
    "mana_base": 100,
    "mana_actual": 100,
    "puntos_mana": 0,
    "stamina_base": 10,
    "stamina_actual": 10,
    "puntos_stamina": 0
  },
  "puntos_disponibles": 0
}
```

### Stats Totales (Calculados)
```json
{
  "hp_total": 100,
  "atk_total": 10,
  "def_total": 0,
  "velocidad_total": 10,
  "critico_total": 5,
  "evasion_total": 10,
  "mana_total": 100,
  "stamina_total": 10
}
```

### Ejemplo con Puntos Asignados
```json
{
  "stats": {
    "hp_base": 150,
    "hp_actual": 150,
    "puntos_hp": 5,
    "atk_base": 20,
    "puntos_atk": 5,
    "def_base": 5,
    "puntos_def": 5,
    "velocidad_base": 15,
    "puntos_velocidad": 5,
    "critico_base": 10,
    "puntos_critico": 5,
    "evasion_base": 15,
    "puntos_evasion": 5,
    "mana_base": 150,
    "mana_actual": 150,
    "puntos_mana": 5,
    "stamina_base": 20,
    "stamina_actual": 20,
    "puntos_stamina": 5
  },
  "puntos_disponibles": 0
}
```

---

## Fórmulas de Cálculo

**Nota importante:** Los puntos asignados se suman directamente al valor base. No se calculan por separado.

### HP Total
```
HP Total = HP Base + (Puntos HP × 10)
```

### ATK Total
```
ATK Total = ATK Base + (Puntos ATK × 2)
```

### DEF Total
```
DEF Total = DEF Base + Puntos DEF
Cap: 80%
```

### Velocidad Total
```
Velocidad Total = Velocidad Base + Puntos Velocidad
```

### Crítico Total
```
Crítico Total = Crítico Base + Puntos Crítico
Cap: 50%
Daño Crítico: x1.5
```

### Evasión Total
```
Evasión Total = Evasión Base + Puntos Evasión
Cap: 50%
```

### Mana Total
```
Mana Total = Mana Base + (Puntos Mana × 10)
```

### Stamina Total
```
Stamina Total = Stamina Base + (Puntos Stamina × 2)
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de stats -->