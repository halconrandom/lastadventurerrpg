# Sistema de Durabilidad - Last Adventurer

## Concepto

Las armas y armaduras tienen durabilidad que disminuye con el uso. Cuando llega a 0, el item se rompe y no se puede usar.

---

## Mecánica Base

### Durabilidad por Tipo

| Tipo | Durabilidad Base | Pérdida por Uso |
|------|------------------|-----------------|
| Espada | 100 | -1 por golpe |
| Espadón | 80 | -1 por golpe |
| Arco | 120 | -1 por disparo |
| Dagas | 60 | -1 por golpe |
| Catalizador | 150 | -2 por hechizo |
| Armadura Ligera | 80 | -1 por golpe recibido |
| Armadura Media | 100 | -1 por golpe recibido |
| Armadura Pesada | 150 | -1 por golpe recibido |

### Rareza y Durabilidad

| Rareza | Modificador Durabilidad |
|--------|------------------------|
| Común | x1.0 |
| Raro | x1.25 |
| Épico | x1.5 |
| Legendario | x2.0 |

---

## Sistema de Herrería

### Reparar Items

| Acción | Costo | Efecto |
|--------|-------|--------|
| Reparar | Oro + Materiales | +50 durabilidad |
| Reparar Completo | Más oro | Durabilidad máxima |

### Mejorar Items

| Mejora | Costo | Efecto |
|--------|-------|--------|
| +5 Daño | Materiales + Oro | Aumenta daño |
| +10 Durabilidad | Materiales + Oro | Aumenta durabilidad máxima |
| Añadir Perk | Material especial + Oro | Añade perk aleatorio |

---

## Preguntas a Definir

- [ ] **¿Qué pasa cuando un item llega a 0?**
  - Se rompe y desaparece
  - Se rompe pero se puede reparar
  - Se rompe y pierde todos los stats
  - Respuesta:

- [ ] **¿Dónde se repara?**
  - NPC herrero en ciudades
  - El jugador puede aprender a reparar
  - Ambos
  - Respuesta:

- [ ] **¿Costo de reparación?**
  - Proporcional a la durabilidad perdida
  - Fijo por item
  - Respuesta:

- [ ] **¿Herramientas para reparar?**
  - Se necesitan herramientas especiales
  - Solo materiales
  - Respuesta:

- [ ] **¿Items irreparables?**
  - ¿Hay un límite de veces que se puede reparar?
  - Respuesta:

---

## Estructura JSON Propuesta

```json
{
  "nombre": "Espada de Hierro",
  "tipo": "arma",
  "subtipo": "espada",
  "daño": 5,
  "durabilidad_actual": 85,
  "durabilidad_maxima": 100,
  "rareza": "comun",
  "estado": "buen_estado"
}
```

### Estados de Durabilidad

| Durabilidad | Estado | Efecto Visual |
|-------------|--------|---------------|
| 100-75% | Excelente | Icono brillante |
| 74-50% | Bueno | Icono normal |
| 49-25% | Dañado | Icono con grietas |
| 24-1% | Roto | Icono rojo |
| 0% | Inutilizable | Icono gris |

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de durabilidad -->