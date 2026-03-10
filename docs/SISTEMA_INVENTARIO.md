# Sistema de Inventario - Last Adventurer

## Concepto

El inventario se divide en **3 secciones principales** con funciones diferenciadas:

1. **Alforjas** - Inventario general para items y consumibles
2. **Equipamiento** - Armadura y accesorios equipados
3. **Armas/Herramientas** - Items en mano para uso inmediato

---

## Estructura de la UI

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          INVENTARIO DEL JUGADOR                          │
├─────────────────────┬─────────────────────┬─────────────────────────────┤
│      ALFORJAS       │    EQUIPAMIENTO     │     ARMAS/HERRAMIENTAS      │
│                     │                     │                              │
│  ┌───┐ ┌───┐ ┌───┐ │    ┌───┐ Casco     │   ┌─────┐      ┌─────┐      │
│  │   │ │   │ │   │ │    └───┘           │   │ Mano│      │Mano  │      │
│  └───┘ └───┘ └───┘ │    ┌───┐ Peto      │   │ Izq.│      │Der.  │      │
│  ┌───┐ ┌───┐ ┌───┐ │    └───┘           │   └─────┘      └─────┘      │
│  │   │ │   │ │   │ │    ┌───┐ Guantes   │                              │
│  └───┘ └───┘ └───┘ │    └───┘           │   ┌─────────────────────┐  │
│  ┌───┐ ┌───┐ ┌───┐ │    ┌───┐ Botas     │   │ Herramienta Activa   │  │
│  │   │ │   │ │   │ │    └───┘           │   └─────────────────────┘  │
│  └───┘ └───┘ └───┘ │    ┌───┐ Amuleto   │                              │
│                     │    └───┘           │                              │
│  Capacidad: 10/20   │    ┌───┐ Anillo 1  │   Peso: 45/80 kg           │
│  Peso: 45 kg        │    └───┘           │   Estado: Medio (-10% vel)  │
│                     │    ┌───┐ Anillo 2  │                              │
│                     │    └───┘           │                              │
│                     │  Defensa: 15       │                              │
├─────────────────────┴─────────────────────┴─────────────────────────────┤
│                              INFO ITEM                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Nombre del Item                                                 │  │
│  │  Tipo: Arma | Rareza: Raro | Daño: 15-20                        │  │
│  │  Descripción del item con sus estadísticas...                    │  │
│  │  [Equipar] [Usar] [Tirar] [Favorito ★]                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Sección 1: Alforjas

### Slots Base
- **Capacidad inicial**: 10 slots
- **Capacidad máxima**: 30 slots (con mejoras)
- **Sistema de stacks**: Los items se apilan según su tipo

### Tipos de Items en Alforjas

| Tipo | Stack Máximo | Ejemplos |
|------|--------------|----------|
| Consumibles | 10 | Pociones, Comida, Bombas |
| Materiales | 50 | Hierro, Madera, Cuero |
| Armas | 1 | No se apilan |
| Armaduras | 1 | No se apilan |
| Herramientas | 1 | No se apilan |
| Misceláneos | 5 | Llaves, Documentos |

### Ampliación de Alforjas

El inventario se puede ampliar de múltiples formas:

| Método | Descripción | Aumento |
|--------|-------------|---------|
| **Misiones** | Recompensas de misiones específicas | +2 a +5 slots |
| **Compra** | Tiendas en ciudades y pueblos | +3 slots (precio variable) |
| **Nivel** | Subir de nivel otorga slots | +1 slot cada 5 niveles |
| **Items especiales** | Mochilas, bolsas mágicas, alforjas mejoradas | +5 a +10 slots |

**Concepto simple**: "Las alforjas ahora son más grandes" - no es necesario complicarlo más allá de la narrativa.

**Capacidad base**: 10 slots → **Capacidad máxima**: 30 slots

---

## Sección 2: Equipamiento

### Slots de Equipamiento

| Slot | Descripción | Stat Principal |
|------|-------------|---------------|
| **Casco** | Protección de cabeza | Defensa + Resistencia mágica |
| **Peto** | Protección de torso | Defensa principal |
| **Guantes** | Protección de manos | Defensa + Velocidad ataque |
| **Botas** | Protección de pies | Defensa + Velocidad movimiento |
| **Amuleto** | Accesorio mágico | Stats variables (magia, resistencia, etc.) |
| **Anillo 1** | Primer anillo | Stats variables |
| **Anillo 2** | Segundo anillo | Stats variables |

### Stats de Armadura

```json
{
  "id": "peto_hierro_001",
  "nombre": "Peto de Hierro",
  "tipo": "armadura",
  "slot": "peto",
  "rareza": "comun",
  "stats": {
    "defensa": 15,
    "resistencia": 5,
    "peso": 10
  },
  "requisitos": {
    "nivel": 5,
    "fuerza": 10
  },
  "efectos": [],
  "valor": 100
}
```

### Sets de Equipamiento

**Sistema de Sets**: Inspirado en Baldur's Gate 3, Diablo y WoW. Algunas armaduras forman sets que otorgan bonificaciones al equipar múltiples piezas del mismo set.

| Piezas Equipadas | Bonificación |
|------------------|--------------|
| 2 piezas | +5% stat principal del set |
| 4 piezas | +10% stat principal + efecto menor |
| Set completo (6) | +15% stats + efecto especial del set |

**Ejemplo de Set**:
```
Set del Guerrero de Hierro (6 piezas: casco, peto, guantes, botas, amuleto, anillo)
- 2 piezas: +5% Defensa
- 4 piezas: +10% Defensa, Inmunidad a aturdir
- 6 piezas: +15% Defensa, Inmunidad a aturdir, "Golpe de Hierro" (habilidad especial)
```

**Nota**: No todos los items pertenecen a un set. Los sets son raros y se encuentran en mazmorras, jefes o como recompensas especiales.

---

## Sección 3: Armas/Herramientas en Mano

### Slots de Mano

| Slot | Descripción | Uso |
|------|-------------|-----|
| **Mano Izquierda** | Arma secundaria, escudo, o herramienta | Combate o utilidad |
| **Mano Derecha** | Arma principal o herramienta | Combate o utilidad |

### Tipos de Armas y Herramientas

> **Ver documento separado**: `SISTEMA_OBJETOS.md` - Catálogo completo de armas, herramientas y objetos.

### Sistema de Dos Manos

**Regla**: Si equipas un arma de dos manos, debe ocupar **ambos slots** (izquierda y derecha).

| Situación | Mano Izquierda | Mano Derecha | Resultado |
|-----------|----------------|--------------|-----------|
| Arma 1 mano | Espada | Escudo | ✓ Válido |
| Arma 1 mano | Espada | Espada | ✓ Válido (dual wield) |
| Arma 2 manos | Espada a dos manos | Espada a dos manos | ✓ Válido (misma referencia) |
| Arma 2 manos + escudo | ❌ No permitido | ❌ | No se puede equipar escudo con arma de 2 manos |

**Implementación**:
- Al equipar un arma de dos manos, se asigna automáticamente a ambos slots
- Si hay un item en el slot contrario, se desequipa automáticamente (va a alforjas)
- Si las alforjas están llenas, no se puede equipar el arma de dos manos

---

## Sistema de Rareza

### Colores y Formato de Texto

| Rareza | Color | Formato en Texto |
|--------|-------|-------------------|
| Común | Gris (#9CA3AF) | `Espada de Hierro` |
| Raro | Verde (#22C55E) | `**Espada de Hierro**` |
| Épico | Púrpura (#A855F7) | `***Espada de Hierro***` |
| Legendario | Naranja (#F97316) | `***Espada de Hierro***` |
| Único | Rojo (#EF4444) | `***Espada de Hierro***` |

### Stats por Rareza

| Rareza | Modificador Daño | Perks Positivos | Perks Negativos |
|--------|------------------|-----------------|-----------------|
| Común | x1.0 | 0 | 0 |
| Raro | x1.1 | 0-1 | 0-1 |
| Épico | x1.25 | 1-2 | 0-1 |
| Legendario | x1.5 | 2-3 | 0 |
| Único | x2.0 | 3-4 | 0 |

---

## Sistema de Peso

**Sistema implementado**: El peso tiene límite y afecta al jugador si se excede.

### Capacidad de Peso

| Atributo | Valor Base | Modificadores |
|----------|------------|---------------|
| **Capacidad base** | 50 kg | +5 kg por punto de Fuerza |
| **Capacidad con armadura** | Variable | Algunas armaduras dan +capacidad |
| **Capacidad con mochila** | +10 a +20 kg | Dependiendo de la mochila |

### Penalizaciones por Exceso de Peso

| Carga | Porcentaje | Efecto |
|-------|------------|--------|
| **Ligero** | 0-50% | Sin penalización |
| **Medio** | 51-75% | Velocidad -10% |
| **Pesado** | 76-100% | Velocidad -20%, Stamina regen -15% |
| **Sobrecargado** | >100% | Velocidad -40%, Stamina regen -30%, No puede correr |

### Ejemplo de Cálculo

```json
{
  "peso_total": 65,
  "capacidad_peso": 80,
  "porcentaje": 81.25,
  "estado": "pesado",
  "penalizaciones": {
    "velocidad": -20,
    "stamina_regen": -15
  }
}
```

**Nota**: El peso incluye items en alforjas, equipamiento y armas equipadas.

---

## Sistema de Favoritos

**Sistema implementado**: Los jugadores pueden marcar items como favoritos para evitar perderlos accidentalmente.

### Funciones de Favoritos

| Función | Descripción |
|---------|-------------|
| **Protección** | Los items favoritos no se pueden vender, tirar ni usar como material de crafteo |
| **Visual** | Marcados con un símbolo ★ en la descripción del item |
| **Ordenamiento** | Los favoritos aparecen primero en cualquier ordenamiento automático |
| **Acceso rápido** | Los consumibles favoritos se pueden usar con teclas 1-5 |

### Ejemplo

```json
{
  "id": "espada_leyenda_001",
  "nombre": "Espada de la Leyenda",
  "favorito": true,
  "protegido": ["vender", "tirar", "craftear"]
}
```

**Nota**: Para eliminar un item favorito, primero debe desmarcarse como favorito.

---

## Sistema de Ordenamiento

**Sistema híbrido**: Ordenamiento automático disponible, pero el jugador tiene libertad total para mover items a su gusto.

### Ordenamiento Automático

| Opción | Descripción |
|--------|-------------|
| **Por tipo** | Consumibles → Materiales → Armas → Armaduras → Misc |
| **Por rareza** | Único → Legendario → Épico → Raro → Poco Común → Común |
| **Por valor** | Mayor valor → Menor valor |
| **Por peso** | Más pesado → Más ligero |
| **Por nombre** | A-Z alfabéticamente |

### Ordenamiento Manual

- El jugador puede arrastrar items entre slots libremente
- El orden manual se respeta hasta que se usa ordenamiento automático
- Los items nuevos se añaden al primer slot libre (o al final si hay huecos)

### Prioridad de Ordenamiento

1. **Favoritos** siempre aparecen primero
2. Luego se aplica el criterio seleccionado
3. Los items con misma prioridad se ordenan por nombre

---

## Inventario Compartido (Stash)

**Sistema implementado**: Stash en ubicaciones seguras (posadas, casas, bancos).

### Ubicaciones de Stash

| Ubicación | Descripción | Capacidad |
|-----------|-------------|-----------|
| **Posada** | Habitación alquilada | 50 slots |
| **Casa del jugador** | Propiedad comprada | 100 slots |
| **Banco** | Servicio de almacenamiento | 200 slots (con comisión) |
| **Campamento** | Tienda de campaña | 30 slots |

### Reglas del Stash

- Cada ubicación tiene su propio stash independiente
- Los items en stash no cuentan para el peso del jugador
- Se puede acceder al stash solo desde la ubicación correspondiente
- Transferir items entre stashes requiere viajar físicamente

### Estructura JSON

```json
{
  "stashes": {
    "posada_pueblo": {
      "ubicacion_id": "posada_pueblo",
      "capacidad": 50,
      "items": []
    },
    "casa_jugador": {
      "ubicacion_id": "casa_jugador",
      "capacidad": 100,
      "items": []
    }
  }
}
```

---

## Sistema de Identificación

**Sistema implementado**: Los items raros o superiores necesitan identificación para ver sus stats completos.

### Items que Requieren Identificación

| Rareza | Requiere Identificación |
|--------|------------------------|
| Común | No |
| Raro | Sí |
| Épico | Sí |
| Legendario | Sí |
| Único | Sí |

### Métodos de Identificación

| Método | Descripción | Coste |
|--------|-------------|-------|
| **Pergamino de Identificar** | Consumible de un uso | 50 oro |
| **NPC Identificador** | Servicios en ciudades | 100-500 oro según rareza |
| **Habilidad Identificar** | Habilidad del jugador (requiere nivel) | Sin coste |
| **Objetos mágicos** | Algunos items identifican automáticamente | N/A |

### Ejemplo de Item No Identificado

```json
{
  "id": "espada_desconocida_001",
  "base_id": "espada_rara",
  "nombre": "Espada Misteriosa",
  "rareza": "raro",
  "identificado": false,
  "descripcion": "Los símbolos en la hoja brillan con un resplandor extraño. Necesitas identificarla para conocer sus propiedades.",
  "stats_visibles": {
    "peso": 5,
    "valor_desconocido": "???"
  }
}
```

### Ejemplo de Item Identificado

```json
{
  "id": "espada_desconocida_001",
  "base_id": "espada_rara",
  "nombre": "Espada del Amanecer",
  "rareza": "raro",
  "identificado": true,
  "descripcion": "Forjada por los herreros del amanecer, esta espada brilla con la luz del sol.",
  "stats": {
    "dano_min": 15,
    "dano_max": 22,
    "velocidad": 1.2,
    "critico": 5
  }
}
```

---

## Sistema de Durabilidad

**Ver documento:** `SISTEMA_DURABILIDAD.md` para detalles completos.

### Resumen de Durabilidad por Rareza

| Rareza | Modificador Durabilidad | Reparaciones Máximas |
|--------|------------------------|---------------------|
| Común | x1.0 | 3 |
| Raro | x1.25 | 5 |
| Épico | x1.5 | 8 |
| Legendario | x2.0 | 10 |
| Único | x2.5 | 15 |

### Estados de Durabilidad

| Estado | Porcentaje | Efecto |
|--------|------------|--------|
| Perfecto | 100-76% | Sin penalización |
| Usado | 75-51% | Sin penalización |
| Gastado | 50-26% | -10% stats |
| 趙易 | 25-1% | -25% stats |
| Roto | 0% | No usable |

---

## Sistema de Encantamientos

**Sistema implementado**: Solo items raros o superiores pueden encantarse.

### Items Encantables

| Rareza | Encantable | Slots de Encantamiento |
|--------|------------|------------------------|
| Común | No | 0 |
| Raro | Sí | 1 slot |
| Épico | Sí | 2 slots |
| Legendario | Sí | 3 slots |
| Único | No (ya tiene efectos únicos) | N/A |

### Tipos de Encantamientos

| Tipo | Efecto | Ejemplo |
|------|--------|---------|
| **Ofensivo** | Aumenta daño | +5 daño, +10% crítico |
| **Defensivo** | Aumenta protección | +5 defensa, +10% resistencia |
| **Mágico** | Añade efecto mágico | Fuego, Hielo, Rayo |
| **Utilidad** | Mejoras prácticas | +10% velocidad, -20% peso |

### Métodos de Encantamiento

| Método | Descripción | Requisito |
|--------|-------------|-----------|
| **NPC Encantador** | Servicios en ciudades | Oro + materiales |
| **Pergamino de Encantamiento** | Consumible de un uso | Pergamino raro |
| **Habilidad Encantamiento** | Habilidad del jugador | Nivel + materiales |

### Ejemplo de Item Encantado

```json
{
  "id": "espada_rara_001",
  "nombre": "Espada del Fuego",
  "rareza": "raro",
  "encantamientos": [
    {
      "tipo": "ofensivo",
      "efecto": "dano_fuego",
      "valor": 5,
      "descripcion": "+5 daño de fuego"
    }
  ],
  "slots_encantamiento": 1,
  "slots_usados": 1
}
```

---

## Sistema de Trading

**Sistema implementado**: Venta a NPCs con precios variables según reputación.

### Factores que Afectan el Precio

| Factor | Efecto | Rango |
|--------|--------|-------|
| **Reputación** | Mejor reputación = mejores precios | -20% a +20% |
| **Carisma** | Atributo del personaje | -10% a +10% |
| **Habilidad Comercio** | Habilidad del jugador | -15% a +15% |
| **Relación con NPC** | Amistad con el vendedor | -5% a +5% |

### Precio Base de Venta

| Rareza | Precio Base | % del Valor Real |
|--------|-------------|-------------------|
| Común | 10-50 oro | 50% |
| Raro | 50-500 oro | 50% |
| Épico | 500-3000 oro | 50% |
| Legendario | 3000-20000 oro | 50% |
| Único | No se puede vender | N/A |

### Ejemplo de Cálculo

```
Item: Espada Rara (Valor: 500 oro)
Reputación: +10% (bueno)
Carisma: +5% (alto)
Habilidad Comercio: +10% (nivel 3)
Relación NPC: +5% (amigo)

Precio de venta = 500 × 0.50 × (1 + 0.10 + 0.05 + 0.10 + 0.05)
Precio de venta = 500 × 0.50 × 1.30
Precio de venta = 325 oro
```

### Compra a NPCs

Los NPCs venden items a precio completo (100% del valor), pero los descuentos por reputación, carisma y habilidades también aplican.

### Tipos de NPCs Comerciantes

| Tipo | Especialización | Inventario |
|------|-----------------|------------|
| **Herrero** | Armas y armaduras | Armas, armaduras, materiales |
| **Alquimista** | Pociones y consumibles | Pociones, ingredientes, pergaminos |
| **Mercader General** | Items variados | Misceláneos, comida, herramientas |
| **Mercader Ambulante** | Items raros | Items aleatorios, cambios cada visita |
| **Encantador** | Items mágicos | Pergaminos, items encantados |

---

## Estructura JSON Completa

### Inventario del Jugador

```json
{
  "inventario": {
    "alforjas": {
      "slots_maximos": 10,
      "items": [
        {
          "id": "espada_hierro_001",
          "base_id": "espada_hierro",
          "nombre": "Espada de Hierro",
          "tipo": "arma",
          "subtipo": "espada_una_mano",
          "rareza": "comun",
          "cantidad": 1,
          "slot": 0,
          "stats": {
            "dano_min": 10,
            "dano_max": 15,
            "velocidad": 1.0
          },
          "peso": 5,
          "valor": 100,
          "favorito": false,
          "identificado": true,
          "durabilidad": 100
        }
      ]
    },
    "equipamiento": {
      "casco": null,
      "peto": null,
      "guantes": null,
      "botas": null,
      "amuleto": null,
      "anillo_1": null,
      "anillo_2": null
    },
    "manos": {
      "izquierda": null,
      "derecha": null
    },
    "herramienta_activa": null,
    "oro": 150,
    "peso_total": 45,
    "capacidad_peso": 80,
    "estado_carga": "medio"
  }
}
```

---

## Sistema de Comparación de Items

**Implementado**: Al equipar un item, se muestra comparación con el item actual.

### UI de Comparación

```
┌─────────────────────────────────────────────────────────────────┐
│                        COMPARANDO                                │
├──────────────────────────┬──────────────────────────────────────┤
│     ITEM ACTUAL          │        NUEVO ITEM                   │
│   Espada de Hierro       │      Espada de Acero                 │
│   [Raro]                 │      [Épico]                         │
│                         │                                       │
│   Daño: 12-18           │      Daño: 15-22  (+4)               │
│   Velocidad: 1.0        │      Velocidad: 1.1 (+0.1)            │
│   Rareza: +10%          │      Rareza: +25%     (+15%)         │
│                         │      [Perk: filo durable]            │
│   ─────────────────     │      ─────────────────               │
│                         │                                       │
│   Estado: Perfecto      │      Estado: Perfecto                │
│                         │                                       │
├──────────────────────────┴──────────────────────────────────────┤
│  [ x ] No mostrar más    [Equipar]      [Cancelar]             │
└─────────────────────────────────────────────────────────────────┘
```

### Stats Comparados

| Stat | Mostrar |
|------|---------|
| Daño/Ataque | Diferencia (+/-) |
| Defensa | Diferencia (+/-) |
| Velocidad | Diferencia (+/-) |
| Perks | Nuevos perks en verde |
| Durabilidad | Estado actual |
| Peso | Diferencia (+/-) |
| Valor | Diferencia (+/-) |

### Comparación Automática

- Se muestra al hacer drag & drop a slot de equipamiento
- Se muestra al hacer doble-click en slot de equipamiento con item en cursor
- Se puede desactivar marcando "No mostrar más"
- Se puede reactivarr en opciones

### Acciones Disponibles

| Acción | Descripción | Atajo |
|--------|-------------|-------|
| **Equipar** | Mueve item a slot de equipamiento | Doble click |
| **Usar** | Usa un consumible | Click derecho → Usar |
| **Tirar** | Elimina el item del inventario | Click derecho → Tirar |
| **Favorito** | Marca/desmarca como favorito (protege de pérdida) | Click derecho → Favorito |
| **Info** | Muestra información detallada | Hover |
| **Dividir** | Divide un stack | Shift + Click |
| **Mover** | Reorganiza items libremente | Arrastrar |
| **Ordenar** | Ordena automáticamente por criterio | Botón ordenar |

### Drag and Drop

- Arrastrar entre slots de alforjas → Reorganiza
- Arrastrar a equipamiento → Equipa
- Arrastrar a manos → Equipa en mano
- Arrastrar fuera del inventario → Tirar (confirmar si es favorito)

### Protección de Favoritos

- Los items favoritos no se pueden vender accidentalmente
- Los items favoritos no se pueden tirar sin confirmación
- Los items favoritos no se pueden usar como material de crafteo
- Para eliminar un favorito, primero debe desmarcarse

---

## Preguntas para Definir

### Alta Prioridad - RESUELTAS

1. **Ampliación de alforjas**: ✅ Múltiples métodos (misiones, compra, nivel, items especiales)
2. **Sistema de peso**: ✅ Implementado con penalizaciones a velocidad y stamina
3. **Items favoritos**: ✅ Sistema de marcado con protección contra pérdida
4. **Ordenamiento**: ✅ Híbrido (automático + manual)

### Media Prioridad - RESUELTAS

5. **Sets de equipamiento**: ✅ Bonificaciones por 2/4/6 piezas (estilo BG3/Diablo/WoW)
6. **Armas de dos manos**: ✅ Ocupan ambos slots automáticamente
7. **Slots de equipamiento**: ✅ Añadidos amuleto y 2 anillos
8. **Stash compartido**: ✅ Stash en ubicaciones seguras (posadas, casas, bancos)
9. **Items no identificados**: ✅ Items raros+ necesitan identificación
10. **Encantamientos**: ✅ Solo items raros o superiores
11. **Trading**: ✅ Venta a NPCs con precios variables según reputación
12. **Durabilidad**: ✅ Items se desgastan con el uso

### Pendientes

- [x] **Comparación de items**: **Sí, comparar** → Al equipar, muestra stats old vs new
- [x] **Slots iniciales**: **10 slots**
- [x] **Stacks máximos**: **Como está ahora** → Consumibles 10, Materiales 50

---

## Implementación Técnica

### Archivos del Sistema

```
backend/src/systems/
├── inventario.py          # Lógica del inventario
├── items.py               # Gestión de items
└── equipamiento.py        # Lógica de equipamiento

backend/src/data/
└── items.json             # Catálogo de items base

frontend/src/components/
└── juego/panels/
    └── InventarioPanel.tsx  # UI del inventario
```

### Endpoints API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/inventario` | GET | Obtiene inventario completo |
| `/api/inventario/equipar` | POST | Equipa un item |
| `/api/inventario/desequipar` | POST | Desequipa un item |
| `/api/inventario/usar` | POST | Usa un consumible |
| `/api/inventario/tirar` | DELETE | Elimina un item |
| `/api/inventario/mover` | POST | Reorganiza items |
| `/api/inventario/dividir` | POST | Divide un stack |

---

## Checklist de Implementación

### Fase 1: Estructura Base
- [ ] Actualizar modelo de datos del inventario
- [ ] Implementar sistema de slots de alforjas
- [ ] Implementar sistema de equipamiento
- [ ] Implementar sistema de manos

### Fase 2: UI
- [ ] Crear componente de 3 columnas
- [ ] Implementar drag and drop
- [ ] Implementar tooltips de items
- [ ] Implementar acciones contextuales

### Fase 3: Lógica
- [ ] Implementar equipar/desequipar
- [ ] Implementar usar consumibles
- [ ] Implementar tirar items
- [ ] Implementar stacks

### Fase 4: Integración
- [ ] Conectar con backend
- [ ] Persistir cambios
- [ ] Sincronizar con combate

---

*Sistema documentado - Versión 3.0*
*Dependencias: SISTEMA_OBJETOS.md, SISTEMA_DURABILIDAD.md, SISTEMA_STATS.md*

## Resumen de Cambios (v3.0)

- ✅ **Ampliación de alforjas**: Múltiples métodos (misiones, compra, nivel, items)
- ✅ **Slots de equipamiento**: Añadidos amuleto y 2 anillos (estilo BG3/Diablo/WoW)
- ✅ **Sets de equipamiento**: Bonificaciones por 2/4/6 piezas
- ✅ **Armas de dos manos**: Ocupan ambos slots automáticamente
- ✅ **Sistema de peso**: Penalizaciones a velocidad y stamina por exceso
- ✅ **Sistema de favoritos**: Protección contra pérdida accidental
- ✅ **Ordenamiento**: Híbrido (automático + manual)
- ✅ **Stash**: Sistema de almacenamiento en ubicaciones seguras
- ✅ **Identificación**: Items raros+ necesitan identificación
- ✅ **Encantamientos**: Solo items raros o superiores
- ✅ **Trading**: Venta a NPCs con precios variables según reputación
- ✅ **Durabilidad**: Items se desgastan con el uso
- ✅ **Tipos de armas/herramientas**: Movidos a SISTEMA_OBJETOS.md
- ✅ **Adaptado a text-based**: Eliminadas referencias visuales 3D