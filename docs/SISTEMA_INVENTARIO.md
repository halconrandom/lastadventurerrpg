# Sistema de Inventario - Last Adventurer

## Concepto

El inventario tiene **10 slots base**, ampliables mediante mejoras. Los items se apilan en stacks de 10.

---

## Mecánica Base

### Slots

| Tipo | Slots Base | Ampliable hasta |
|------|------------|-----------------|
| Inventario General | 10 | 20 (con mejoras) |
| Equipamiento | 4 | 4 (fijo) |

### Equipamiento

| Slot | Descripción |
|------|-------------|
| Arma | Espada, Arco, Dagas, etc. |
| Casco | Protección de cabeza |
| Peto | Protección de torso |
| Botas | Protección de pies |

### Stack de Items

| Tipo de Item | Stack Máximo |
|---------------|--------------|
| Pociones | 10 |
| Materiales | 50 |
| Armas | 1 (no se apilan) |
| Armaduras | 1 (no se apilan) |

---

## Tipos de Items

### Consumibles
- Pociones de HP, Mana, Stamina
- Pociones de Buff
- Se usan y desaparecen

### Equipables
- Armas
- Armaduras (piezas)
- Se equipan en slots específicos

### Materiales
- Para crafteo y forja
- Se apilan en grandes cantidades

---

## Preguntas a Definir

- [ ] **¿Cómo se amplía el inventario?**
  - Misiones
  - Tiendas
  - Subir de nivel
  - Respuesta:

- [ ] **¿Límite de peso?**
  - Sin límite de peso
  - Límite por peso
  - Respuesta:

- [ ] **¿Inventario compartido?**
  - Si hay sistema de stash/baúl
  - Respuesta:

- [ ] **¿Items favoritos?**
  - Sistema para marcar items importantes
  - Respuesta:

- [ ] **¿Ordenamiento automático?**
  - Por tipo
  - Por rareza
  - Manual
  - Respuesta:

---

## Estructura JSON Propuesta

### Inventario del Jugador
```json
{
  "slots_maximos": 10,
  "items": [
    {
      "id": "espada_hierro_001",
      "nombre": "Espada de Hierro",
      "tipo": "arma",
      "cantidad": 1,
      "slot": 0
    },
    {
      "id": "pocion_hp_001",
      "nombre": "Poción Pequeña",
      "tipo": "consumible",
      "cantidad": 10,
      "slot": 1
    }
  ],
  "equipado": {
    "arma": "espada_hierro_001",
    "casco": null,
    "peto": null,
    "botas": null
  }
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de inventario -->