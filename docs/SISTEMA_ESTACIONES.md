# Sistema de Estaciones de Trabajo - Last Adventurer

## Estado: Definido

**Última actualización:** 10 de marzo de 2026

---

## Estaciones Definidas

| Estación | Descripción | Produce |
|----------|-------------|---------|
| Yunque | Herrería básica | Armas y Armaduras |
| Mesa de Trabajo | Fabricación | Items y Mejoras |
| Taller | Herramientas | Herramientas y Utilidad |
| Horno | Procesamiento | Comida y Materiales |
| Banco de Carpintero | Carpintería | Estructuras y Muebles |

---

## Características Comunes

- **Niveles:** Sin niveles
- **Mejoras:** No se pueden mejorar
- **Obtención:** Se pueden craftear y comprar
- **Ubicación:** Estáticas en ubicaciones + colocables por el jugador

---

## Recetas de Estaciones

### 1. Yunque (Herrería)

**Descripción:** Estación para forjar armas y armaduras metálicas.

**Receta para craftear:**
```json
{
  "id": "receta_yunque",
  "estacion": "yunque",
  "materiales": [
    {"id": "piedra", "cantidad": 10},
    {"id": "hierro", "cantidad": 5},
    {"id": "carbon", "cantidad": 3}
  ],
  "herramienta": "martillo_herrero",
  "tiempo": 60
}
```

**Producción:**
- Espadas
- Espadones
- Armaduras
- Escudos
- Cascos
- Guantes
- Botas

---

### 2. Mesa de Trabajo

**Descripción:** Estación multifunción para crear items y mejoras.

**Receta para craftear:**
```json
{
  "id": "receta_mesa_trabajo",
  "estacion": "mesa_trabajo",
  "materiales": [
    {"id": "madera", "cantidad": 15},
    {"id": "hierro", "cantidad": 3},
    {"id": "cuero", "cantidad": 2}
  ],
  "herramienta": "martillo",
  "tiempo": 45
}
```

**Producción:**
- Kits de reparación
- Materiales de mejora
- Encantamientos básicos
- Accesorios

---

### 3. Taller

**Descripción:** Estación para crear herramientas y objetos de utilidad.

**Receta para craftear:**
```json
{
  "id": "receta_taller",
  "estacion": "taller",
  "materiales": [
    {"id": "hierro", "cantidad": 8},
    {"id": "madera", "cantidad": 5},
    {"id": "cuero", "cantidad": 3}
  ],
  "herramienta": "martillo",
  "tiempo": 45
}
```

**Producción:**
- Herramientas de minería
- Herramientas de cosecha
- Trampas
- Items de utilidad

---

### 4. Horno

**Descripción:** Estación para procesar materiales y crear comida.

**Receta para craftear:**
```json
{
  "id": "receta_horno",
  "estacion": "horno",
  "materiales": [
    {"id": "piedra", "cantidad": 15},
    {"id": "arcilla", "cantidad": 5},
    {"id": "carbon", "cantidad": 5}
  ],
  "herramienta": "pala",
  "tiempo": 45
}
```

**Producción:**
- Pan
- Comida cocida
- Bebidas
- Materiales procesados

---

### 5. Banco de Carpintero

**Descripción:** Estación para crear muebles y estructuras de madera.

**Receta para craftear:**
```json
{
  "id": "receta_banco_carpintero",
  "estacion": "banco_carpintero",
  "materiales": [
    {"id": "madera", "cantidad": 20},
    {"id": "hierro", "cantidad": 2},
    {"id": "clavos", "cantidad": 5}
  ],
  "herramienta": "sierra",
  "tiempo": 60
}
```

**Producción:**
- Muebles (sillas, mesas, armarios)
- Estanterías
- Cajones
- Estructuras básicas

---

## Materiales Necesarios para Estaciones

### Materiales Base (por definir en items.json)

| Material | Tipo | Rareza | Uso |
|----------|------|--------|-----|
| Piedra | Material | Común | Yunque, Horno |
| Arcilla | Material | Común | Horno |
| Clavos | Herramienta | Común | Banco |
| Madera | Material | Común | Todas |
| Hierro | Metal | Común | Yunque, Taller, Banco |
| Carbon | Combustible | Común | Yunque, Horno |
| Cuero | Material | Común | Mesa, Taller |

---

## Integración con el Juego

### Obtención de Estaciones

1. **Crafteando:** El jugador puede crear la estación
2. **Comprando:** En tiendas de artesanos
3. **Encontrando:** Como loot en mazmorras
4. **Misiones:** Recompensa de quests

### Uso en el Juego

```
┌─────────────────────────────────────────────────────┐
│              ESTACIÓN DE TRABAJO                    │
├─────────────────────────────────────────────────────┤
│  [Yunque] [Mesa] [Taller] [Horno] [Carpintero]   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Recetas disponibles:                              │
│  ┌─────────────────────────────────────────────┐  │
│  │ Espada de Hierro                            │  │
│  │   Hierro x3 + Madera x1                     │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  [Craftear]                                        │
└─────────────────────────────────────────────────────┘
```

---

## Pendiente

- [ ] Definir items.json con materiales de estaciones
- [ ] Crear recetas de estaciones
- [ ] Implementar lógica de crafteo de estaciones
- [ ] Sistema deubicación de estaciones en el mundo
- [ ] UI para interactuar con estaciones

---

## Notas

<!-- Agregar notas adicionales aquí -->
