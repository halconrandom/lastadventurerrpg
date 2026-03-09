# Sistema de Combate - Last Adventurer

## Concepto

Combate por turnos con acciones estratégicas. El jugador puede atacar, usar habilidades, bloquear, o huir.

---

## Flujo de Combate

```
1. Inicio del combate
2. Turno del jugador
   - Atacar (físico)
   - Usar habilidad (consume mana/stamina)
   - Usar item (pociones)
   - Bloquear (reduce daño y da exp de Defensa)
   - Huir (probabilidad de escape)
3. Turno del enemigo
4. Verificar si alguien murió
5. Repetir hasta fin del combate
```

---

## Acciones del Jugador

### Atacar
- Usa el arma equipada
- Cálculo: `Daño = (ATK base + Daño Arma) × Multiplicador Habilidad`
- Consume: Nada
- Da experiencia a la habilidad del arma

### Usar Habilidad (Perk Activo)
- Consume Mana o Stamina según el perk
- Efecto variable según el perk
- Da experiencia a la habilidad relacionada

### Usar Item
- Consume una poción del inventario
- Sin límite por combate
- No consume turno (o sí, a definir)

### Bloquear
- Reduce daño recibido en 50%
- Da experiencia a Defensa
- No consume recursos

### Huir
- Probabilidad basada en nivel del enemigo vs jugador
- Si falla, el enemigo ataca con ventaja

---

## Cálculo de Daño

### Fórmula de Daño Físico
```
Daño Base = ATK Personaje + Daño Arma
Multiplicador = 1 + (Nivel Habilidad × 0.05)
Daño Final = Daño Base × Multiplicador
```

### Fórmula de Reducción de Daño
```
Reducción = Defensa % + (Nivel Defensa × 1%)
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
| Fuego | Daño elemental | Espada del Infierno |
| Hielo | Posibilidad de congelar | Espadón de Escarcha |
| Sangrado | Daño por tiempo | Daga Ensangrentada |

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