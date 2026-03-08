# Sistema de Rareza y Forja - Last Adventurer

## Rareza de Items

### Niveles de Rareza

| Rareza | Color | Descripción | Bonus |
|--------|-------|-------------|-------|
| Común | Gris | Item básico | Stats base |
| Raro | Verde | Item mejorado | +10% stats |
| Épico | Púrpura | Item poderoso | +25% stats |
| Legendario | Naranja | Item único | +50% stats + perk especial |

---

## Sistema de Forja

### Concepto
Permite crear armas personalizadas con:
- Nombre personalizado
- Stats aleatorios dentro de un rango
- Perks aleatorios (positivos y/o negativos)
- Rareza variable

### Proceso de Forja

```
1. Elegir tipo de arma (Espada, Arco, etc.)
2. Elegir materiales (afectan stats y rareza)
3. Forjar → Genera stats aleatorios
4. Posibilidad de añadir perk (aleatorio)
5. Nombrar el arma
```

### Materiales

| Material | Afecta | Rareza posible |
|----------|--------|----------------|
| Hierro | Daño base | Común, Raro |
| Acero | Daño + durabilidad | Raro, Épico |
| Mithril | Daño + ligereza | Épico, Legendario |
| Dragón | Daño + perk de fuego | Legendario |

---

## Generación Aleatoria

### Stats Base por Tipo de Arma

| Tipo | Daño Mínimo | Daño Máximo |
|------|-------------|-------------|
| Espada | 5 | 15 |
| Espadón | 8 | 20 |
| Arco | 4 | 12 |
| Dagas | 3 | 10 |
| Catalizador | 2 | 8 |

### Fórmula de Generación

```
Daño final = Daño base × (1 + Bonus rareza) × Aleatorio(0.9, 1.1)
```

### Perks Aleatorios

| Rareza | Perks Positivos | Perks Negativos |
|--------|-----------------|-----------------|
| Común | 0 | 0 |
| Raro | 1 | 0-1 |
| Épico | 1-2 | 0-1 |
| Legendario | 2-3 | 0 |

---

## Preguntas a Definir

- [ ] **¿Cómo se consiguen los materiales?**
  - Drops de enemigos
  - Misiones
  - Tiendas
  - Respuesta:

- [ ] **¿Quién forja?**
  - NPC herrero
  - El jugador puede aprender
  - Respuesta:

- [ ] **¿Costo de forja?**
  - Oro
  - Materiales
  - Ambos
  - Respuesta:

- [ ] **¿Se puede mejorar un item existente?**
  - Sí, añadir materiales
  - No, solo crear nuevos
  - Respuesta:

- [ ] **¿Límite de forjas por día?**
  - Sin límite
  - Limitado por materiales
  - Respuesta:

---

## Estructura JSON Propuesta

### Template de Arma Base
```json
{
  "tipo": "espada",
  "nombre_base": "Espada de {material}",
  "materiales": ["hierro", "acero", "mithril", "dragon"],
  "stats_base": {
    "daño_min": 5,
    "daño_max": 15
  },
  "perks_posibles": ["fuego", "hielo", "sangrado", "critico"]
}
```

### Arma Forjada (Resultado)
```json
{
  "nombre": "Destelladora",
  "tipo": "espada",
  "rareza": "epico",
  "daño": 18,
  "perks": [
    {"nombre": "Filo Afilado", "tipo": "positivo", "efecto": "+10% daño"},
    {"nombre": "Maldición", "tipo": "negativo", "efecto": "-5% velocidad"}
  ],
  "material": "acero",
  "forjador": "Jugador",
  "fecha_creacion": "2024-01-15"
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de rareza y forja -->