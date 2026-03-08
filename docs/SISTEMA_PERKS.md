# Sistema de Perks - Last Adventurer

## Definición

Los Perks son habilidades especiales que pueden ser:
- **Pasivos**: Siempre activos
- **Activos**: Se activan manualmente, consumen recursos

---

## Tipos de Perks

### 1. Perks de Habilidad
Se desbloquean al subir de nivel en una habilidad específica.

| Habilidad | Nivel | Perk | Tipo | Efecto |
|-----------|-------|------|------|--------|
| Espada | 5 | Filo Afilado | Pasivo | +10% daño con espadas |
| Espada | 10 | Golpe Giratorio | Activo | Daño en área (15 stamina) |
| Espada | 15 | Contraataque | Pasivo | 5% probabilidad de ataque doble |
| Arco | 5 | Puntería | Pasivo | +5% precisión |
| Arco | 10 | Disparo Múltiple | Activo | 3 flechas a la vez (20 stamina) |
| Arco | 15 | Ojo de Águila | Pasivo | +20% daño a distancia |
| Magia | 5 | Mana Expandido | Pasivo | +20 mana máximo |
| Magia | 10 | Bola de Fuego | Activo | Daño mágico en área (30 mana) |
| Magia | 15 | Regeneración | Pasivo | +1 mana por segundo |
| Dagas | 5 | Sigilo | Pasivo | +10% probabilidad de crítico |
| Dagas | 10 | Apuñalar | Activo | Daño x2 por detrás (10 stamina) |
| Dagas | 15 | Veneno | Pasivo | 5% probabilidad de envenenar |
| Defensa | 5 | Piel Dura | Pasivo | +5% reducción de daño |
| Defensa | 10 | Escudo de Hierro | Activo | Inmune 3 segundos (50 stamina) |
| Defensa | 15 | Bloqueo Perfecto | Pasivo | 10% probabilidad de bloquear todo |

### 2. Perks de Armas
Algunas armas otorgan perks al equiparlas.

| Perk | Tipo | Efecto | Ejemplo de Arma |
|------|------|--------|-----------------|
| Fuego | Pasivo | +5% daño de fuego | Espada del Infierno |
| Hielo | Pasivo | 5% probabilidad de congelar | Espadón de Escarcha |
| Sangrado | Pasivo | 10% probabilidad de sangrado | Daga Ensangrentada |
| Crítico | Pasivo | +15% daño crítico | Arco del Cazador |
| Maldición | Negativo | -10% velocidad | Espada Maldita |

### 3. Perks de Armadura
Bonus por usar set completo.

| Set | Bonus | Efecto |
|-----|-------|--------|
| Cuero | +5% evasión | Más probabilidad de esquivar |
| Hierro | +10% reducción de daño | Defensa adicional |
| Acero | +15% HP | Más vida máxima |
| Dragón | +20% resistencia a fuego | Inmune a daño de fuego |

---

## Preguntas a Definir

- [ ] **¿Cómo se desbloquean los perks de habilidad?**
  - Automáticamente al subir nivel
  - El jugador elige cuál desbloquear
  - Respuesta:

- [ ] **¿Límite de perks activos?**
  - ¿Se pueden tener todos activos?
  - ¿Hay un límite de slots?
  - Respuesta:

- [ ] **¿Perks negativos en armas?**
  - ¿Cómo se balancean?
  - ¿Son más poderosas pero con desventaja?
  - Respuesta:

- [ ] **¿Perks de armadura acumulables?**
  - ¿El bonus de set se suma con otros perks?
  - Respuesta:

---

## Estructura JSON Propuesta

```json
{
  "nombre": "Golpe Giratorio",
  "tipo": "activo",
  "habilidad": "Espada",
  "nivel_requerido": 10,
  "costo": {
    "tipo": "stamina",
    "cantidad": 15
  },
  "efecto": {
    "tipo": "daño_area",
    "multiplicador": 1.5
  },
  "descripcion": "Gira tu espada causando daño a todos los enemigos cercanos"
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de perks -->