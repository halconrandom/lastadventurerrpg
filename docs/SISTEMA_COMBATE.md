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

> **Nota:** Las preguntas sobre enemigos están en [SISTEMA_ENEMIGOS.md](./SISTEMA_ENEMIGOS.md)

### Mecánicas de Combate

- [ ] **¿Usar item consume turno?**
  - Sí
  - No
  - Respuesta:

- [ ] **¿Orden de turnos?**
  - Por velocidad
  - Jugador siempre primero
  - Aleatorio
  - Respuesta:

- [ ] **¿Combate en grupo?**
  - Solo 1v1
  - Múltiples enemigos
  - Respuesta:

- [ ] **¿Críticos?**
  - Probabilidad fija (5%)
  - Basado en habilidad
  - Respuesta:

- [ ] **¿Evasión?**
  - Probabilidad de esquivar
  - Basado en armadura ligera
  - Respuesta:

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