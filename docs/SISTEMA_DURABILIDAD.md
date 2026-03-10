# Sistema de Durabilidad - Last Adventurer

## Estado del Proyecto

**Última actualización:** 10 de marzo de 2026

**Contexto:** Este sistema está integrado con el Sistema de Rareza y Forja. Las respuestas definidas ahí aplican aquí.

---

## Mecánica Base

### Durabilidad por Tipo de Item

| Tipo | Durabilidad Base | Pérdida por Uso |
|------|------------------|-----------------|
| Espada | 100 | -1 por golpe |
| Espadón | 80 | -1 por golpe |
| Arco | 120 | -1 por disparo |
| Ballesta | 100 | -1 por disparo |
| Dagas | 60 | -1 por golpe |
| Catalizador | 150 | -2 por hechizo |
| Bastón | 120 | -2 por hechizo |
| Hacha | 90 | -1 por golpe |
| Armadura Ligera | 80 | -1 por golpe recibido |
| Armadura Media | 100 | -2 por golpe recibido |
| Armadura Pesada | 150 | -3 por golpe recibido |
| Escudo | 100 | -2 por bloqueo |
| Casco | 80 | -1 por golpe recibido |
| Guantes | 60 | -1 por golpe recibido |
| Botas | 60 | -1 por uso de habilidad |

### Rareza y Durabilidad

| Rareza | Modificador Durabilidad |
|--------|------------------------|
| Común | x1.0 |
| Raro | x1.25 |
| Épico | x1.5 |
| Legendario | x2.0 |
| Único | x2.5 |

### Estados del Item

| Rango | Estado | Efecto |
|-------|--------|--------|
| 100-76% | Perfecto | Sin penalización |
| 75-51% | Usado | Sin penalización |
| 50-26% | Gastado | -10% stats |
| 25-1% |趙易 | -25% stats |
| 0% | Roto | No usable (0% stats) |

### Pérdida de Durabilidad por Acción

| Acción | Pérdida |
|--------|---------|
| Golpe exitoso (arma) | -1 |
| Golpe recibido (armadura) | -1 a -3 según tipo |
| Bloqueo exitoso (escudo) | -3 |
| Usar habilidad especial | -5 |
| Usar habilidad de arma | -2 |
| Crit recibido | -2 |
| Esquivar fallida | -1 |

---

## Reparación de Items

### Quién Puede Reparar

- **NPC Herrero:** Disponible en pueblos y ciudades
- **Jugador:** Si tiene skill de herrería aprendido

### Métodos de Reparación

| Método | Costo | Efecto |
|--------|-------|--------|
| NPC Herrero | Gold + Materiales | +50 durabilidad |
| NPC Herrero (completo) | Gold + Materiales | Durabilidad máxima |
| Jugador (skill) | Solo materiales | +25 durabilidad |
| Kit de Reparación | 1 uso | +30 durabilidad |

### Costo de Reparación (NPC)

```
costo_gold = (durabilidad_maxima - durabilidad_actual) × 0.5
costo_materiales = tipo_item × 1-3 materiales básicos
```

### Skill de Herrería del Jugador

| Nivel | Bonus Reparación |
|-------|------------------|
| 1 | +10% durabilidad reparada |
| 2 | +20% durabilidad reparada |
| 3 | +30% durabilidad reparada |
| 4 | +40% durabilidad reparada |
| 5 | +50% durabilidad reparada + puede reparar perks |

---

## Integración con Sistema de Rareza

### Perks de Durabilidad

| Perk | Efecto | Rareza |
|------|--------|--------|
| Filo Duradero | +15% durabilidad | Común |
| Acero Endurecido | +25% durabilidad | Raro |
| Forja Perfecta | +50% durabilidad | Épico |
| Eternidad | +100% durabilidad | Legendario |

### Perks Negativos Relacionados

| Perk | Efecto | Frecuencia |
|------|--------|------------|
| Oxidado | -10% durabilidad | 30% |
| Frágil | -20% durabilidad | 15% |
| Quebradizo | -30% durabilidad | 5% |

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de durabilidad -->
