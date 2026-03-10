# Sistema de Crafteo - Last Adventurer

## Estado del Proyecto

**Última actualización:** 10 de marzo de 2026

**Contexto:** Sistema adaptado al estado actual del juego.

---

## Concepto

Sistema para crear y mejorar items mediante recetas en estaciones específicas.

---

## Tipos de Crafteo

| Tipo | Estación | Descripción |
|------|----------|-------------|
| Herrería | Yunque | Armas y armaduras metálicas |
| Forja | Yunque | Crear items base mejorables |
| Reparación | Yunque | Reparar items dañados |

**Nota:** Alquimia separada (no implementada aún).

---

## Estaciones de Crafteo

### Yunque

| Nivel | Nombre | Bonus |
|-------|--------|-------|
| 1 | Yunque Básico | Sin bonus |
| 2 | Yunque de Villa | +5% calidad |
| 3 | Yunque de Ciudad | +10% calidad |
| 4 | Yunque de Mazmorra | +15% calidad |

**Nota:** Por ahora todas las ubicaciones dan igual resultado.

---

## Sistema de Recetas

### Aprendizaje

- **Básicas:** Disponibles desde el inicio
- **Avanzadas:** Se aprenden con NPCs o misiones

### Estructura de Receta

```json
{
  "id": "receta_espada_hierro",
  "nombre": "Espada de Hierro",
  "tipo": "herreria",
  "descripcion": "Forja una espada básica de hierro.",
  "materiales": [
    {"id": "hierro", "cantidad": 3},
    {"id": "madera", "cantidad": 1}
  ],
  "resultado": {
    "id_item": "espada_hierro",
    "cantidad": 1
  },
  "perks": [
    {"id": "filo_duradero", "valor": 15}
  ],
  "tiempo": 5,
  "requisitos": {
    "nivel_herreria": 1
  }
}
```

---

## Sistema de Forja (Items Mejorables)

### Concepto

Los items base se pueden mejorar mediante forja:

```
Item Base + Materiales → Item Mejorado
```

### Mejoras por Tipo

| Mejora | Materiales | Efecto |
|--------|-----------|--------|
| +1 Daño | Hierro x2 | +2 daño |
| +1 Defensa | Hierro x2 | +2 defensa |
| +10 Durabilidad | Material repair x1 | +10 durabilidad |
| +5% Velocidad | Material especial | +5% velocidad |

### Límite de Mejoras

| Rareza | Mejoras Máximas |
|--------|-----------------|
| Común | 3 |
| Raro | 5 |
| Épico | 8 |
| Legendario | 10 |

---

## Sistema de Skill

### Niveles de Herrería

| Nivel | Nombre | Bonus |
|-------|--------|-------|
| 1 | Aprendiz | - |
| 2 | Herrador | +5% chance rareza |
| 3 | Herrero | +10% chance rareza |
| 4 | Maestro | +15% chance rareza |
| 5 | Gran Maestro | +20% chance rareza |

### Subir de Nivel

- **Crafteando:** XP por cada item creado
- **Quests:** Misiones de NPCs herreros

---

## Materiales

### Materiales Base

| Material | Tipo | Rareza | Fuentes |
|----------|------|--------|---------|
| Hierro | Metal | Común | Minas, Enemigos |
| Acero | Metal | Raro | Forja, Tiendas |
| Madera | Material | Común | Bosques |
| Cuero | Material | Común | Caza |
| Tela | Material | Común | Tiendas |
| Mithril | Metal Mágico | Épico | Mazmorras |

### Materiales Especiales

| Material | Rareza | Efecto |
|----------|--------|--------|
| Escama de Dragón | Legendario | +25% daño fuego |
| Cristal de Hielo | Legendario | +25% daño hielo |
| Essence Void | Único | +100% daño |

---

## Integración con Sistemas

### Rareza en Crafteo

| Nivel Skill | Rareza Máxima Posible |
|-------------|----------------------|
| 1-2 | Común, Raro |
| 3 | Raro, Épico |
| 4 | Épico, Legendario |
| 5 | Legendario, Único |

### Probabilidades de Rareza (según skill)

| Nivel | Común | Raro | Épico | Legendario |
|-------|-------|------|-------|------------|
| 1 | 80% | 20% | 0% | 0% |
| 2 | 60% | 35% | 5% | 0% |
| 3 | 40% | 40% | 20% | 0% |
| 4 | 20% | 40% | 35% | 5% |
| 5 | 10% | 30% | 45% | 15% |

---

## Recetas Iniciales (Básicas)

### Herrería

| Receta | Materiales | Nivel Req |
|--------|------------|-----------|
| Espada de Hierro | Hierro x3, Madera x1 | 1 |
| Escudo de Madera | Madera x3 | 1 |
| Espadón | Hierro x5, Madera x2 | 2 |
| Armadura de Cuero | Cuero x4 | 1 |
| Armadura de Placas | Hierro x8, Cuero x3 | 3 |

### Armas

| Receta | Materiales | Nivel Req |
|--------|------------|-----------|
| Arco Corto | Madera x3 | 1 |
| Arco Largo | Madera x4, Hierro x1 | 2 |
| Dagas | Hierro x2, Cuero x1 | 1 |
| Catalizador | Madera x2, Cristal x1 | 3 |

---

## Reparación

### Sistema

- **Siempre exitosa** (sin probabilidad de fallo)
- **Costo:** Materiales base proporcional al daño

### Costos de Reparación

| Durabilidad Perdida | Materiales |
|--------------------|-----------|
| 1-25 | Hierro x1 |
| 26-50 | Hierro x2 |
| 51-75 | Hierro x3 |
| 76-100 | Hierro x4 |

---

## UI Propuesta

```
┌─────────────────────────────────────────────────────────────────┐
│                        CRAFTEO                                   │
├─────────────────────────────────────────────────────────────────┤
│  [Herrería]  [Forja]  [Reparación]                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Recetas Desbloqueadas:                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [+] Espada de Hierro (Nivel 1)                         │   │
│  │     Hierro x3 + Madera x1                               │   │
│  │ [+] Escudo de Madera (Nivel 1)                         │   │
│  │     Madera x3                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Skill: Herrería Nivel 2                                       │
│  [===========            ] 45/100 XP                           │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  [Craftear]                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estructura JSON

### Recetas

```json
{
  "id": "receta_espada_hierro",
  "nombre": "Espada de Hierro",
  "tipo": "herreria",
  "descripcion": "Forja una espada básica de hierro.",
  "materiales": [
    {"id": "hierro", "cantidad": 3},
    {"id": "madera", "cantidad": 1}
  ],
  "resultado": {
    "id_item": "espada_hierro",
    "cantidad": 1,
    "perks": [
      {"id": "filo_duradero", "nombre": "Filo Duradero", "valor": 15}
    ]
  },
  "tiempo": 5,
  "requisitos": {
    "nivel_herreria": 1
  },
  "desbloqueada": true
}
```

### Progreso de Recetas

```json
{
  "recetas_desbloqueadas": [
    "receta_espada_hierro",
    "receta_escudo_madera",
    "receta_armadura_cuero"
  ],
  "skill_herreria": {
    "nivel": 2,
    "xp": 45,
    "xp_proximo_nivel": 100
  }
}
```

---

## Pendiente de Implementar

- [ ] Sistema de recetas (JSON + lógica)
- [ ] Sistema de skill de herrería
- [ ] Integración con inventario
- [ ] UI de crafteo en frontend

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional -->
