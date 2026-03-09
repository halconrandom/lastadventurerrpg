# Sistema de Enemigos - Last Adventurer

## Concepto

Enemigos con diferentes tipos, stats y drops. La dificultad escala con el nivel del jugador o la zona.

---

## Tipos de Enemigos

### Por Categoría

| Categoría | Descripción | Ejemplos |
|-----------|-------------|----------|
| Bestias | Animales salvajes | Lobo, Oso, Serpiente |
| Humanoides | Seres inteligentes | Bandido, Orco, Goblin |
| No-muertos | Cadáveres reanimados | Esqueleto, Zombi, Espectro |
| Mágicos | Criaturas mágicas | Elemental, Golem, Demonio |
| Jefes | Enemigos únicos y poderosos | Dragón, Rey Demonio |

---

## Stats de Enemigos

### Stats Base

| Stat | Descripción |
|------|-------------|
| HP | Puntos de vida |
| ATK | Daño base |
| DEF | Reducción de daño |
| Velocidad | Determina orden de turnos |
| Experiencia | Exp que da al morir |

### Escalado por Nivel

```
HP = HP Base × (1 + Nivel × 0.1)
ATK = ATK Base × (1 + Nivel × 0.05)
DEF = DEF Base × (1 + Nivel × 0.03)
```

---

## Drops

### Probabilidad de Drop

| Rareza del Item | Probabilidad Base |
|-----------------|-------------------|
| Común | 50% |
| Raro | 20% |
| Épico | 5% |
| Legendario | 1% |

### Tipos de Drops

| Tipo | Descripción |
|------|-------------|
| Oro | Moneda del juego |
| Materiales | Para crafteo/forja |
| Armas | Equipamiento |
| Armaduras | Protección |
| Pociones | Consumibles |

---

## Preguntas a Definir

- [ ] **¿Cómo escala la dificultad?**
  - Por nivel del jugador
  - Por zona del mapa
  - Ambos
  - Respuesta: Ambos

- [ ] **¿Enemigos únicos?**
  - Enemigos que solo aparecen una vez
  - Jefes de zona
  - Respuesta: Si

- [ ] **¿Sistema de agro?**
  - Enemigos te persiguen
  - Zonas seguras
  - Respuesta: Enemigos te persiguen

- [ ] **¿Respawn de enemigos?**
  - Aparecen de nuevo después de un tiempo
  - No reaparecen
  - Respuesta: aparecen de nuevo despues de un tiempo

- [ ] **¿Experiencia por matar?**
  - Fija por tipo de enemigo
  - Escala con nivel del jugador
  - Respuesta: fija por tipo de enemigo, nivel y demas

---

## Estructura JSON Propuesta

### Enemigo Base
```json
{
  "id": "lobo",
  "nombre": "Lobo",
  "categoria": "bestia",
  "stats_base": {
    "hp": 30,
    "atk": 8,
    "def": 2,
    "velocidad": 10
  },
  "experiencia_base": 25,
  "drops": [
    {"item": "colmillo_lobo", "probabilidad": 0.3},
    {"item": "piel_lobo", "probabilidad": 0.2},
    {"item": "oro", "min": 5, "max": 15, "probabilidad": 1.0}
  ],
  "habilidades": [
    {"nombre": "Mordisco", "daño": 1.2, "tipo": "físico"}
  ]
}
```

### Enemigo en Combate
```json
{
  "id": "lobo_001",
  "tipo": "lobo",
  "nivel": 5,
  "hp_actual": 45,
  "hp_maximo": 45,
  "atk": 10,
  "def": 3
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de enemigos -->