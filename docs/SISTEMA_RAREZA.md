# Sistema de Rareza y Forja - Last Adventurer

## Estado del Proyecto

**Última actualización:** 10 de marzo de 2026

**Contexto actual:**
- Backend en Flask con API REST funcionando
- Frontend en Next.js 16 (en desarrollo)
- Sistema de combate implementado
- Sistema de exploración implementado
- Sistema de guardado implementado
- Items básicos definidos en `backend/src/data/items.json` (sin rareza aún)

---

## Rareza de Items

### Niveles de Rareza

| Rareza | Color | Probabilidad | Bonus Stats | Perks | Notas |
|--------|-------|--------------|-------------|-------|-------|
| Común | Gris (#9CA3AF) | 60% | x1.0 | 0 | Item base |
| Raro | Verde (#22C55E) | 25% | x1.1 | 0-1 | - |
| Épico | Púrpura (#A855F7) | 10% | x1.25 | 1-2 | - |
| Legendario | Naranja (#F97316) | 4% | x1.5 | 2-3 | + perk especial único |
| Único | Rojo (#EF4444) | 1% | x2.0 | 3-4 | Solo 1 en el mundo |

### Propiedades por Rareza

| Rareza | Rango Daño | Stats Adicionales | Perks Positivos | Perks Negativos |
|--------|-----------|-------------------|-----------------|-----------------|
| Común | 100% | 0 | 0 | 0 |
| Raro | 110% | +1-2 stats | 1 | 0-1 |
| Épico | 125% | +2-3 stats | 1-2 | 0-1 |
| Legendario | 150% | +3-4 stats | 2-3 | 0 |
| Único | 200% | +4-5 stats | 3-4 | 0 |

---

## Sistema de Forja

### Concepto

Permite crear armas personalizadas con:
- Nombre personalizado (generado o elegido)
- Stats aleatorios dentro de un rango basado en materiales
- Rareza variable según materiales y probabilidad
- Perks aleatorios (positivos y negativos)
- Durabilidad inicial

### Proceso de Forja

```
1. Seleccionar tipo de arma (espada, arco, daga, etc.)
2. Seleccionar materiales (afectan stats, rareza y perks)
3. Forjar → Genera stats aleatorios basados en materiales
4. Determinar rareza según materiales usados
5. Añadir perks (probabilidad basada en rareza)
6. Nombrar el arma (opcional - si no, nombre aleatorio)
```

### Materiales

#### Materiales Básicos

| Material | Rareza Base | Efecto | Dificultad |
|----------|-------------|--------|------------|
| Hierro | Común | Stats base | Baja |
| Acero | Raro | +10% daño, +20% durabilidad | Media |
| Bronce | Raro | +5% defensa | Media |

#### Materiales Especiales

| Material | Rareza Base | Efecto | Fuente |
|----------|-------------|--------|--------|
| Mithril | Épico | +25% daño, -10% peso | Minas profundas |
| Escama de Dragón | Legendario | +50% daño, perk fuego | Jefes dragón |
| Cristal de Hielo | Legendario | +40% daño, perk hielo | Zonas frías |
| Essence Void | Único | +100% daño, perk especial | Mazmorras finales |
| Plata Bendita | Épico | +30% daño vs no-muertos | Templos |

#### Materiales de Perk

| Material | Perk Posible | Rareza del Perk |
|----------|--------------|-----------------|
| Ruby ígneo | Fuego | Épico |
| Zafiro glacial | Hielo | Épico |
| Esmeralda venenosa | Veneno | Raro |
| Topacio eléctrico | Trueno | Raro |
| Amatista mística | Mana | Legendario |
| Onyx infernal | Vida | Único |

---

## Generación Aleatoria

### Fórmula de Rareza

```
probabilidad_base = 60% (común)
bonificacion_material = sum(rareza_materiales) / count(materiales)
rareza_final = random() < (probabilidad_base + bonificacion_material)
```

### Fórmula de Stats

```
stat_base = stat_base_tipoarma
bonus_rareza = multiplicador_tabla_rareza
modificador_material = sum(modificadores_materiales)
varianza = random(0.9, 1.1)

stat_final = floor(stat_base × bonus_rareza × modificador_material × varianza)
```

### Rango de Daño por Tipo de Arma

| Tipo | Daño Mín | Daño Máx | Multiplicador Rareza |
|------|----------|----------|---------------------|
| Espada | 5 | 15 | 1.0 |
| Espadón | 8 | 22 | 1.2 |
| Arco | 4 | 12 | 0.9 |
| Ballesta | 6 | 16 | 1.0 |
| Dagas | 3 | 10 | 0.8 |
| Catalizador | 2 | 8 | 0.7 |
| Bastón | 3 | 9 | 0.75 |
| Hacha | 7 | 18 | 1.1 |

### Probabilidad de Perks

| Rareza | Sin Perk | 1 Perk | 2 Perks | 3 Perks | 4 Perks |
|--------|----------|--------|---------|---------|---------|
| Común | 100% | 0% | 0% | 0% | 0% |
| Raro | 50% | 40% | 10% | 0% | 0% |
| Épico | 20% | 45% | 30% | 5% | 0% |
| Legendario | 0% | 20% | 45% | 30% | 5% |
| Único | 0% | 0% | 20% | 50% | 30% |

### Perks Disponibles

#### Perks Positivos

| Perk | Efecto | Rareza | Tipo Arma |
|------|--------|--------|-----------|
| Filo Duradero | +15% durabilidad | Común | Todas |
| Balance Perfecto | +10% velocidad ataque | Raro | Espadas, Arcos |
| Golpe Crítico | +5% crit chance | Raro | Todas |
| Impacto Pesado | +20% daño | Épico | Espadones, Hachas |
| Ligero como el Viento | -15% peso | Épico | Dagas, Arcos |
| Toque de Fuego | +25% daño fuego | Legendario | Todas |
| Toque de Hielo | +25% daño hielo | Legendario | Todas |
| Toque de Trueno | +25% daño eléctrico | Legendario | Todas |
| Vampirismo | +10% robo de vida | Único | Dagas, Espadas |
| Destrucción | +50% daño a escudos | Épico | Todas |

#### Perks Negativos

| Perk | Efecto | Frecuencia |
|------|--------|------------|
| Oxidado | -10% durabilidad | 30% |
| Desbalanceado | -10% velocidad | 25% |
| Pesado | +10% peso | 20% |
| Frágil | -20% durabilidad | 15% |
| Maldito | -5% todos los stats | 10% |

---

## Sistema de Herrería

### Habilidad de Herrero

El mejorar su habilidad de her jugador puederero:

| Nivel | Nombre | Bonus |
|-------|--------|-------|
| 1 | Aprendiz | Sin bonus |
| 2 | Herrador | +5% probabilidad rareza |
| 3 | Herrero | +10% probabilidad rareza |
| 4 | Maestro Herrero | +15% probabilidad rareza, -1 perk negativo máx |
| 5 | Gran Maestro | +20% probabilidad rareza, perks negativos 50% menos |

### Estaciones de Forja

| Estación | Ubicación | Bonus |
|----------|-----------|-------|
| Yunque Básico | Cualquier sitio | Sin bonus |
| Yunque de Villa | Pueblos | +5% calidad |
| Yunque de Ciudad | Ciudades | +10% calidad |
| Yunque de Mazmorra | Mazmorras especiales | +15% calidad + chance único |

### Proceso de Mejora (Reforge)

```
1. Seleccionar item a mejorar
2. Seleccionar materiales adicionales
3. Forjar de nuevo (puede mejorar o empeorar)
4. Si mejora → nuevos stats/perks
5. Si falla → item destruido o stats reducidos
```

---

## Integración con Otros Sistemas

### Drops de Enemigos

- Enemigos comunes: 80% común, 15% raro, 4% épico, 1% legendarios
- Enemigos elite: 40% raro, 40% épico, 15% legendarios, 5% único
- Jefes: 30% épico, 50% legendarios, 20% único
- La rareza del drop depende del nivel del enemigo vs nivel del jugador

### Tiendas

- Tiendas básicas: Solo comunes y raros
- Tiendas avanzadas: Hasta épicos
- Tiendas especializadas: Legendarios (raras)
- Precios basados en rareza: común x1, raro x2, épico x5, legendarios x20

### Crafteo

- Recetas producen items de rareza basada en materiales
- Mayor calidad de materiales = mayor probabilidad de rareza
- Skills de crafteo influyen en el resultado

---

## Estructura JSON

### Template de Arma Base

```json
{
  "id": "espada_hierro",
  "tipo": "arma",
  "subtipo": "espada",
  "nombre_base": "Espada de {material}",
  "materiales_compatibles": ["hierro", "acero", "mithril", "dragon"],
  "stats_base": {
    "daño_min": 5,
    "daño_max": 15,
    "durabilidad": 100,
    "peso": 3
  },
  "perks_disponibles": ["filo_duradero", "balance_perfecto", "golpe_critico"],
  "requisitos": {
    "fuerza": 10,
    "nivel": 1
  }
}
```

### Item Forjado (Instancia)

```json
{
  "id": "item_instancia_001",
  "id_template": "espada_hierro",
  "nombre": "Espada del Amanecer",
  "tipo": "arma",
  "rareza": "epico",
  "stats": {
    "daño": 18,
    "durabilidad": 120,
    "velocidad": 1.1
  },
  "perks": [
    {"id": "filo_duradero", "nombre": "Filo Duradero", "tipo": "positivo", "efecto": "+15% durabilidad"},
    {"id": "toque_fuego", "nombre": "Toque de Fuego", "tipo": "positivo", "efecto": "+25% daño fuego"}
  ],
  "perks_negativos": [],
  "materiales": ["acero", "mithril"],
  "forjado_por": "Hernán el Herrero",
  "fecha_creacion": "2026-03-10",
  "durabilidad_actual": 120,
  "enhancements": 0
}
```

## Respuestas Definidas

- **Forja:** Ambos (NPC herrero + jugador puede aprender herrería)
- **Nombrar:** Nombre libre
- **Reforjar:** Sí, se puede mejorar items existentes
- **Fallo reforja:** No mejora pero se pierden los materiales
- **Skill herrería:** Sí, requerido para forjar
- **Nivel herrería:** Por receta (no por nivel de skill)
- **Costo forja:** Solo materiales
- **Perks negativos:** Sí, a veces
- **Rareza Único:** Sí, implementar
- **Mejora skill:** XP por forjar + quests/NPCs
- **Materiales reforja:** Materiales especiales
- **Límite mejora:** Por tier de rareza
- **Merchants:** Hasta raro (intermedia)
- **Fuente materiales:** Todas (enemigos, recolección, tiendas)

---

## Sistema de Herrería del Jugador

### Skill de Herrería

El jugador puede mejorar su habilidad de herrería:

| Nivel | Nombre | Bonus | Recetas Desbloqueadas |
|-------|--------|-------|----------------------|
| 1 | Aprendiz | - | Común |
| 2 | Herrador | +5% probabilidad rareza | Raro |
| 3 | Herrero | +10% probabilidad rareza | Épico |
| 4 | Maestro Herrero | +15% probabilidad rareza | Legendario |
| 5 | Gran Maestro | +20% probabilidad rareza | Único |

### Cómo Subir de Nivel

- **XP por forjar:** Cada forja da XP
- **Quests/NPCs:** Misiones específicas de herrería

### Recetas

| Receta | Rareza Resultado | Materiales | Requiere Nivel |
|--------|-----------------|------------|----------------|
| Espada Hierro | Común | Hierro x3, Madera x1 | 1 |
| Espada Acero | Raro | Acero x3, Carbón x2 | 2 |
| Espada Mithril | Épico | Mithril x3, Gema x1 | 3 |
| Espada Dragón | Legendario | Escama x2, Mithril x2 | 4 |
| Espada Void | Único | Essence Void x1, Mithril x3 | 5 |

---

## Sistema de Reforja (Mejora de Items)

### Proceso

```
1. Seleccionar item a mejorar
2. Seleccionar materiales especiales de mejora
3. Forjar de nuevo
4. Si tiene éxito → mejora stats/perks
5. Si falla → no mejora pero se pierden materiales
```

### Límite por Rareza

| Rareza | Mejoras Máximas |
|--------|-----------------|
| Común | 1 |
| Raro | 2 |
| Épico | 3 |
| Legendario | 4 |
| Único | 5 |

### Materiales de Mejora

| Material | Efecto | Rareza del Item |
|----------|--------|-----------------|
| Aceite de Afilar | +5% daño | Común-Raro |
| Escencia de Forja | +10% stats | Raro-Épico |
| Fragmento Estelar | +15% stats + chance perk | Épico-Legendario |
| Alma de Herrero | +20% stats + nuevo perk | Legendario-Único |

---

## Preguntas a Definir

### Rareza y Probabilidades

- [x] **¿Las probabilidades de rareza son correctas?**
  - 60% común, 25% raro, 10% épico, 4% legendarios, 1% único
  - **Ajustar:**

- [x] **¿Los bonus de stats por rareza son adecuados?**
  - Raro +10%, Épico +25%, Legendario +50%, Único +100%
  - **Ajustar:**

- [x] **¿Añadimos una rareza "Único" para items single-player (solo 1 en el mundo)?**
  - **Sí** → Implementar

### Sistema de Forja

- [x] **¿Quién forja los items?**
  - **Ambos** → NPC herrero + jugador puede aprender

- [x] **¿El jugador puede nombrar sus armas forjadas?**
  - **Nombre libre**

- [x] **¿Se puede mejorar (reforjar) un item existente?**
  - **Sí, mejora items**

- [x] **¿Qué pasa si falla una mejora?**
  - **Simplemente no mejora pero se pierden los items de mejora.**

### Materiales y Economía

- [x] **¿Cómo se consigue cada material?**
  - **Todas las fuentes** → Drops, Recolección, Tiendas

- [x] **¿Los materiales se pueden comprar en tiendas?**
  - **Respuesta:** Básico en tiendas, especial por otras fuentes

- [x] **¿Costo de forja?**
  - **Solo materiales**

### Perks

- [x] **¿Los perks negativos siempre aparecen?**
  - **Sí, a veces**

- [x] **¿Se pueden eliminar perks negativos?**
  - **Sí, con purificación** → Material especial

- [x] **¿Sistema de durabilidad implementado?**
  - **No implementado** → Pendiente de definir

- [x] **¿Los perks afectan el gameplay significativamente?**
  - **Sí, perks deben cambiar cómo juegas**

### Herrería del Jugador

- [x] **¿El jugador puede aprender a forjar?**
  - **Sí, skill requerido**

- [x] **¿Nivel de herrería afecta qué puede crear?**
  - **Por receta** → Depende de la receta, no del nivel

### Integración

- [x] **¿Los enemies droppean items con rareza?**
  - **Sí, siempre**

- [x] **¿Los merchants venden items de qué rareza?**
  - **Intermedia** → Hasta raro

- [ ] **¿Sistema de durabilidad implementado?**
  - Ya está en otro documento
  - Lo definimos aquí
  - No implementado aún
  - Respuesta:

- [ ] **¿El jugador puede nombrar sus armas forjadas?**
  - Solo nombre aleatorio
  - Elegir de lista de prefijos
  - Nombre completamente libre
  - Respuesta:

- [ ] **¿Se puede mejorar (reforjar) un item existente?**
  - Sí, añadir materiales para mejorar stats/perks
  - No, solo crear nuevos
  - Respuesta:

- [ ] **¿Qué pasa si falla una mejora?**
  - Item destruido
  - Item pierde stats
  - Item pierde perk
  - Nada (solo no mejora)
  - Respuesta:

### Materiales y Economía

- [ ] **¿Cómo se consigue cada material?**
  - Hierro:
  - Acero:
  - Mithril:
  - Escama de Dragón:
  - Essence Void:
  - (Drops / Minas / Tiendas / Misiones)

- [ ] **¿Los materiales tienen durabilidad/rotura?**
  - Sí / No

- [ ] **¿Los materiales se pueden comprar en tiendas?**
  - Solo básicos / Todos / Ninguno
  - Respuesta:

- [ ] **¿Costo de forja?**
  - Solo materiales
  - Oro + materiales
  - Solo oro (materiales de drops)
  - Respuesta:

### Perks

- [ ] **¿Los perks negativos siempre aparecen?**
  - Solo en raro y épico (ver tabla)
  - Nunca
  - Siempre tienen perks negativos
  - Respuesta:

- [ ] **¿Se pueden eliminar perks negativos?**
  - Sí, con material especial
  - No, son permanentes
  - Sí, con forja de "purificación"
  - Respuesta:

- [ ] **¿Los perks afectan el gameplay significativamente?**
  - Sí, perks deben cambiar cómo juegas
  - No, son solo bonus menores
  - Respuesta:

### Herrería del Jugador

- [ ] **¿El jugador puede aprender a forjar?**
  - Sí, skill de herrería
  - No, siempre NPCs
  - Respuesta:

- [ ] **¿Nivel de herrería afecta qué puede crear?**
  - Nivel 1: común
  - Nivel 2: común + raro
  - Nivel 3: común + raro + épico
  - Nivel 4: común + raro + épico + legendarios
  - Nivel 5: todo
  - Respuesta:

### Integración

- [ ] **¿Los enemies droppean items con rareza?**
  - Sí, siempre
  - Solo enemies específicos
  - Solo bosses
  - Respuesta:

- [ ] **¿Los merchants venden items de qué rareza?**
  - Básica (común/raro)
  - Intermedia (hasta épico)
  - Avanzada (hasta legendarios)
  - Respuesta:

- [ ] **¿Sistema de durabilidad implementado?**
  - Ya está en otro documento
  - Lo definimos aquí
  - No implementado aún
  - Respuesta:---

## Sistema de Purificación (Eliminar Perks Negativos)

### Proceso

```
1. Seleccionar item con perk negativo
2. Añadir material de purificación
3. Forjar para eliminar perk negativo
4. El perk negativo se elimina (no se puede elegir cuál)
```

### Materiales de Purificación

| Material | Efecto | Fuente |
|----------|--------|--------|
| Agua Bendita | Elimina 1 perk negativo | Templos |
| Luz Solar | Elimina hasta 2 perks negativos | Eventos especiales |
| Ritual Ancestral | Elimina todos los perks negativos | Quest épica |

---

## Sistema de Durabilidad

### Estados del Item

| Estado | Color | Efecto |
|--------|-------|--------|
| Perfecto | Verde | Sin penalización |
| Usado | Amarillo | Sin penalización |
| Gastado | Naranja | -10% stats |
|赵易 | Rojo | -25% stats |
| Roto | Gris | No usable (0% stats) |

### Reparación

- **NPC Herrero:** Costo en gold
- **Materiales:** Kit de reparación
- **Self repair:** Si tiene skill de herrería

### Desgaste por Uso

| Acción | Pérdida Durabilidad |
|--------|---------------------|
| Golpe en combate | -1 por golpe |
| Recibir daño (armadura) | -2 por golpe |
| Bloqueo exitoso | -3 por bloqueo |
| Usar habilidad especial | -5 por uso |

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de rareza y forja -->
