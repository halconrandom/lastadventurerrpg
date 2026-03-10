# Sistema de Combate - Last Adventurer

> **Estado:** Actualizado - Consistente con sistemas actuales
> **Última actualización:** 2026-03-09
> **Dependencias:** SISTEMA_STATS.md, CATALOGO_ENEMIGOS_COMPLETO.md, SISTEMA_INVENTARIO.md

## Concepto

Combate por turnos con **grupo completo** (múltiples aliados y enemigos). El orden de turnos se determina por velocidad. El jugador puede atacar, usar habilidades, usar items, bloquear, evadir activamente, o huir.

---

## Flujo de Combate

```
1. Inicio del combate
   - Generar participantes (jugador + aliados vs enemigos)
   - Calcular orden de turnos por velocidad
   - Determinar turnos extra por diferencia de velocidad

2. Turno de cada participante (en orden de velocidad)
   - Jugador/Aliado: Elige acción
   - Enemigo: IA elige acción
   - Ejecutar acción
   - Verificar efectos (estados alterados, muerte)

3. Fin de turno
   - Resetear bloqueos
   - Aplicar efectos de tiempo (veneno, sangrado, etc.)
   - Regenerar stamina

4. Verificar fin de combate
   - Victoria: Todos los enemigos muertos
   - Derrota: Todos los aliados muertos
   - Huida: Jugador escapa con éxito

5. Repetir hasta fin del combate
```

---

## Acciones del Jugador

### Atacar
- Usa el arma equipada
- Cálculo: `Daño = (ATK Personaje + Daño Arma) × Multiplicador Habilidad`
- Costo: 10 Stamina
- Da experiencia a la habilidad del arma

### Usar Habilidad (Perk Activo)
- Consume Mana o Stamina según el perk
- Efecto variable según el perk
- Da experiencia a la habilidad relacionada

### Usar Item
- Consume una poción del inventario
- Costo: 5 Stamina
- **Consume turno** (según decisión del usuario)

### Bloquear
- Reduce daño recibido en 50%
- Da experiencia a Defensa
- Costo: 5 Stamina
- **Chance de contraataque:** 10% base + (Nivel Defensa × 1%)
- Si contraataca: Ataque básico automático sin costo adicional

### Evadir Activamente
- Evade 100% del daño del próximo ataque
- Costo: 5 Stamina
- No ataca en este turno

### Huir
- Probabilidad basada en nivel del enemigo vs jugador
- Fórmula: `Probabilidad = 50% + (Nivel Jugador - Nivel Enemigo) × 5%`
- Rango: 10% - 90%
- Si falla, el enemigo ataca con ventaja

---

## Sistema de Stamina

La stamina es el **recurso de acción por turno**. Se regenera completamente al inicio de cada turno.

### Costos de Acción

| Acción | Costo de Stamina | Efecto |
|--------|-----------------|--------|
| Ataque básico | 10 puntos | Daño normal |
| Usar habilidad | Variable (10-30 puntos) | Efecto según habilidad |
| Usar item | 5 puntos | Cura HP/Mana |
| Bloquear | 5 puntos | Reduce daño 50% + chance contraataque |
| Evadir activamente | 5 puntos | Evade 100% del daño |

### Ejemplo de Turno

```
Stamina disponible: 20

Opción 1: Ataque básico (10) → Turno terminado
Opción 2: Tomar poción (5) + Bloquear (5) → Turno terminado
Opción 3: Usar habilidad fuerte (15) → Turno terminado
Opción 4: Ataque básico (10) + Bloquear (5) → Necesitas más stamina
```

### Perks que Afectan Stamina

- Reducen costo de acciones específicas
- Aumentan stamina máxima
- Permiten recuperar stamina parcial en combate

---

## Sistema de Turnos Extra por Velocidad

La velocidad determina no solo el orden de ataque, sino también **cuántas veces atacas por turno**.

### Cálculo de Turnos Extra

```
Diferencia = (Velocidad Atacante - Velocidad Objetivo) / Velocidad Objetivo × 100
Turnos Extra = floor(Diferencia / 50)
Ataques Totales = 1 + Turnos Extra
```

### Tabla de Turnos Extra

| Diferencia de Velocidad | Ataques por Turno |
|------------------------|-------------------|
| 0-49% superior | 1 ataque |
| 50-99% superior | 2 ataques |
| 100-149% superior | 3 ataques |
| 150-199% superior | 4 ataques |
| ... | +1 por cada 50% |

### Ejemplos

```
Tu velocidad: 100
Enemigo velocidad: 50
Diferencia: 100% superior → Atacas 3 veces (1 base + 2 extra)

Tu velocidad: 100
Enemigo velocidad: 60
Diferencia: 66% superior → Atacas 2 veces (1 base + 1 extra)
```

---

## Sistema de Evasión

### Evasión Pasiva
- Ocurre automáticamente si decides atacar
- Chance base: 10% + puntos de evasión
- Cap: 50%
- No consume recursos

### Evasión Activa
- Decides evadir conscientemente
- Siempre evade (100% éxito)
- Costo: 5 Stamina
- No atacas en este turno

### Bloqueo vs Evasión

| Tipo | Descripción | Efecto |
|------|-------------|--------|
| **Pasiva** | Ocurre automáticamente si decides atacar | Chance base de evadir (10% + puntos) |
| **Activa** | Decides evadir conscientemente | Siempre evade (100% éxito) |
| **Bloqueo** | Decides bloquear | Reduce daño + da exp a Defensa + chance contraataque |

### Contraataque tras Bloqueo

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

---

## Cálculo de Daño

### Fórmula de Daño Físico
```
Daño Base = ATK Personaje + Daño Arma
Multiplicador = 1 + (Nivel Habilidad × 0.05)
Daño Final = Daño Base × Multiplicador
```

### Fórmula de Crítico
```
Probabilidad Crítico = Crítico Base + Puntos Crítico
Daño Crítico = Daño Final × 1.5
```

### Fórmula de Reducción de Daño
```
Reducción = DEF % + (Nivel Defensa × 1%)
Reducción Máxima = 80%
Daño Recibido = Daño Enemigo × (1 - Reducción)
```

### Fórmula de Bloqueo
```
Daño Bloqueado = Daño Recibido × 0.5
Experiencia Defensa = Nivel Enemigo × 2
```

---

## Tipos de Daño

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Físico | Daño normal | Espada, Arco, Dagas |
| Mágico | Daño de hechizos | Bola de Fuego |
| Fuego | Daño elemental, puede quemar | Espada del Infierno |
| Hielo | Daño elemental, puede congelar | Espadón de Escarcha |
| Rayo | Daño elemental, puede aturdir | Bastón de Tormenta |
| Veneno | Daño por tiempo | Daga Ensangrentada |
| Sangrado | Daño por tiempo | Hacha de Carnicero |
| Oscuridad | Daño mágico oscuro | Orbe de Sombra |

---

## Estados Alterados

Los estados alterados son efectos que persisten durante varios turnos.

### Estados de Daño por Tiempo

| Estado | Efecto | Duración | Cómo se cura |
|--------|--------|----------|--------------|
| **Quemadura** | 5-10 daño/turno | 3 turnos | Agua, Poción de Curación |
| **Veneno** | 5-15 daño/turno | 3-5 turnos | Antídoto, Poción de Curación |
| **Sangrado** | 3-8 daño/turno | 2-4 turnos | Vendas, Poción de Curación |
| **Congelación** | -20% velocidad, 50% chance de saltar turno | 2 turnos | Fuego, Poción de Calor |
| **Enfermedad** | -20% stats, -50% curación | 4 turnos | Poción de Curación, Descanso largo |

### Estados de Control

| Estado | Efecto | Duración | Cómo se cura |
|--------|--------|----------|--------------|
| **Aturdir** | No puede actuar | 1 turno | Pasa automáticamente |
| **Inmovilizar** | No puede moverse, -50% evasión | 1-2 turnos | Pasa automáticamente |
| **Ceguera** | -50% precisión, -30% crítico | 2-3 turnos | Poción de Visión |
| **Miedo** | -20% ATK, 20% chance de huir | 2 turnos | Pasa automáticamente |
| **Confusión** | 50% chance de atacar aliado | 2 turnos | Pasa automáticamente |
| **Silencio** | No puede usar habilidades mágicas | 2 turnos | Pasa automáticamente |

### Estados de Buff

| Estado | Efecto | Duración | Fuente |
|--------|--------|----------|--------|
| **Furia** | +30% ATK, -20% DEF | 3 turnos | Habilidad, Item |
| **Escudo** | +50% DEF | 2 turnos | Habilidad, Item |
| **Velocidad** | +30% velocidad | 2 turnos | Habilidad, Item |
| **Invisibilidad** | 100% evasión | 1 turno | Habilidad, Item |
| **Regeneración** | +10 HP/turno | 3 turnos | Habilidad, Item |

---

## Combate en Grupo

El combate soporta **múltiples participantes** en ambos bandos.

### Estructura de Grupo

```
Bando del Jugador:
├── Jugador (siempre presente)
├── Aliado 1 (opcional)
├── Aliado 2 (opcional)
└── Aliado 3 (opcional)

Bando Enemigo:
├── Enemigo 1
├── Enemigo 2
├── Enemigo 3
└── Enemigo 4
```

### Orden de Turnos

1. Calcular velocidad de todos los participantes
2. Ordenar de mayor a menor velocidad
3. Cada participante actúa en su orden
4. Aplicar turnos extra por diferencia de velocidad

### IA de Enemigos

Los enemigos tienen comportamientos predefinidos según su tipo:

| Tipo de Enemigo | Comportamiento |
|----------------|----------------|
| **Agresivo** | Ataca siempre, prioriza HP bajo |
| **Defensivo** | Bloquea frecuentemente, protege aliados |
| **Mágico** | Usa habilidades, mantiene distancia |
| **Sigiloso** | Ataca primero, huye si HP bajo |
| **Líder** | Ordena a aliados, invoca refuerzos |
| **Jefe** | Múltiples fases, habilidades especiales |

### Ejemplo de Combate en Grupo

```
Orden de turnos (por velocidad):
1. Águila Real (VEL: 28) - Enemigo
2. Asesino Sombra (VEL: 28) - Enemigo
3. Jugador (VEL: 20) - Aliado
4. Guerrero Caballero (VEL: 12) - Aliado
5. Oso Pardo (VEL: 8) - Enemigo

Turno 1:
- Águila Real ataca a Guerrero Caballero
- Asesino Sombra ataca a Jugador
- Jugador ataca a Águila Real
- Guerrero Caballero bloquea
- Oso Pardo ataca a Jugador

Fin de turno 1:
- Resetear bloqueos
- Aplicar efectos de tiempo
- Regenerar stamina
```

---

## Preguntas a Definir

- [ ] **¿Usar item consume turno?**
  - Sí
  - No
  - Respuesta: Si

- [ ] **¿Orden de turnos?**
  - Por velocidad
  - Jugador siempre primero
  - Aleatorio
  - Respuesta: Por velocidad

- [ ] **¿Combate en grupo?**
  - Solo 1v1
  - Múltiples enemigos
  - Respuesta: Grupo completo

- [ ] **¿Críticos?**
  - Probabilidad fija (5%)
  - Basado en habilidad
  - Respuesta: Basado en habilidad

- [ ] **¿Esvasión?**
  - Probabilidad de esquivar
  - Basado en armadura ligera
  - Respuesta: Probabilidad de esquivar ataque completo (basado en stat evasion)

---

## Estructura JSON Propuesta

### Estado de Combate
```json
{
  "turno": 5,
  "jugador": {
    "hp_actual": 85,
    "hp_maximo": 100,
    "mana_actual": 30,
    "mana_maximo": 50,
    "stamina_actual": 40,
    "stamina_maximo": 50
  },
  "enemigo": {
    "nombre": "Orco",
    "hp_actual": 20,
    "hp_maximo": 50
  },
  "acciones_disponibles": ["atacar", "habilidad", "item", "bloquear", "huir"]
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de combate -->  

Preguntas de Diseño

  Antes de implementar, necesito que definas:

  1. ¿Usar item consume turno?
   - A) Sí, consume turno
   - B) No, es acción gratuita
   - C) Solo pociones de curación son gratuitas

  Respuesta: Consumen un turno.

  2. ¿Orden de turnos?
   - A) Jugador siempre primero
   - B) Por velocidad (stat existente)
   - C) Aleatorio cada turno
Respuesta: por velocidad

  3. ¿Combate en grupo?
   - A) Solo 1v1 (jugador vs 1 enemigo)
   - B) 1 vs múltiples enemigos (el jugador ataca a uno por turno)
   - C) Grupo completo (múltiples aliados y enemigos)

Respuesta:  Grupo completo

  4. ¿Cómo funcionan los críticos?
   - A) Probabilidad fija 5%
   - B) Basado en stat critico (ya existe en Stats)
   - C) Ambos: base 5% + stat crítico

Respuesta:  basado en stat critico

  5. ¿Cómo funciona la evasión?
   - A) No hay evasión
   - B) Probabilidad de esquivar ataque completo (basado en stat evasion)
   - C) Reduce daño en lugar de esquivar

Respuesta:  Probabilidad de esquivar ataque completo (basado en stat evasion)

  6. ¿Qué pasa al huir?
   - A) Probabilidad basada en nivel (jugador vs enemigo)
   - B) Siempre funciona pero pierdes oro/experiencia
   - C) Solo funciona si el enemigo está por debajo de 50% HP

Respuesta:  Probabilidad basada en nivel (jugador vs enemigo)

  7. ¿Recompensas al ganar?
   - A) Solo experiencia
   - B) Experiencia + oro
   - C) Experiencia + oro + posible drop de item

Respuesta: Depende del tipo de monstruo, su nivel y demas, pero seria la C