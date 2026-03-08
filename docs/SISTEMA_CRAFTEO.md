# Sistema de Crafteo - Last Adventurer

## Concepto

Sistema para crear y mejorar items mediante recetas y materiales.

---

## Tipos de Crafteo

| Tipo | Descripción |
|------|-------------|
| Herrería | Armas y armaduras metálicas |
| Alquimia | Pociones y consumibles |
| Encantamiento | Añadir perks a items |

---

## Recetas

### Estructura de Receta

```json
{
  "id": "receta_espada_hierro",
  "nombre": "Espada de Hierro",
  "tipo": "herreria",
  "materiales": [
    {"id": "hierro", "cantidad": 3},
    {"id": "madera", "cantidad": 1}
  ],
  "resultado": {
    "id": "espada_hierro",
    "cantidad": 1
  },
  "tiempo": 5,
  "requisitos": {
    "nivel_herreria": 1
  }
}
```

---

## Materiales

### Materiales Base

| Material | Fuente | Uso |
|----------|--------|-----|
| Hierro | Minas, Enemigos | Armas, Armaduras |
| Acero | Forja (Hierro + Carbon) | Armas mejoradas |
| Madera | Bosques | Armas, Construcción |
| Cuero | Animales | Armaduras ligeras |
| Tela | Plantas | Ropa, Pociones |
| Gemas | Minas, Jefes | Encantamientos |

### Materiales Especiales

| Material | Fuente | Uso |
|----------|--------|-----|
| Escama de Dragón | Dragones | Armas de fuego |
| Cristal de Hielo | Zonas frías | Armas de hielo |
| Veneno | Serpientes | Armas de sangrado |

---

## Creación de Pociones

### Recetas de Alquimia

| Poción | Ingredientes | Efecto |
|--------|--------------|--------|
| Poción Pequeña | Hierba + Agua | +20 HP |
| Poción Grande | Hierba x2 + Agua | +50 HP |
| Poción de Fuerza | Hierba + Cristal Rojo | +10 ATK por 30s |
| Poción de Mana | Cristal Azul + Agua | +30 Mana |

---

## Encantamiento

### Añadir Perks a Items

| Encantamiento | Material | Efecto |
|---------------|----------|--------|
| Fuego | Escama de Dragón | +5% daño fuego |
| Hielo | Cristal de Hielo | 5% probabilidad congelar |
| Sangrado | Veneno | 10% probabilidad sangrado |

---

## Preguntas a Definir

- [ ] **¿Dónde se craftea?**
  - En cualquier lugar
  - En estaciones específicas (Yunque, Mesa de Alquimia)
  - Respuesta:

- [ ] **¿Tiempo de crafteo?**
  - Instantáneo
  - Tiempo de espera
  - Respuesta:

- [ ] **¿Probabilidad de fallo?**
  - Siempre éxito
  - Posibilidad de fallar
  - Respuesta:

- [ ] **¿Aprender recetas?**
  - Todas disponibles desde el inicio
  - Se aprenden con NPCs o libros
  - Respuesta:

- [ ] **¿Crafteo personalizado?**
  - Solo recetas predefinidas
  - Combinación libre de materiales
  - Respuesta:

---

## Estructura JSON Propuesta

### Inventario de Materiales
```json
{
  "materiales": [
    {"id": "hierro", "nombre": "Hierro", "cantidad": 15},
    {"id": "madera", "nombre": "Madera", "cantidad": 8},
    {"id": "cuero", "nombre": "Cuero", "cantidad": 5}
  ]
}
```

### Recetas Desbloqueadas
```json
{
  "recetas": [
    "receta_espada_hierro",
    "receta_pocion_pequena",
    "receta_arco_madera"
  ]
}
```

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de crafteo -->