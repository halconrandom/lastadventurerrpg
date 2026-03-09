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
│  ┌───┐ ┌───┐ ┌───┐ │    ┌───┐           │   ┌─────┐      ┌─────┐      │
│  │   │ │   │ │   │ │    │   │ Casco     │   │     │      │     │      │
│  └───┘ └───┘ └───┘ │    └───┘           │   │ Mano│      │Mano  │      │
│  ┌───┐ ┌───┐ ┌───┐ │    ┌───┐           │   │ Izq.│      │Der.  │      │
│  │   │ │   │ │   │ │    │   │ Peto      │   └─────┘      └─────┘      │
│  └───┘ └───┘ └───┘ │    └───┘           │                              │
│  ┌───┐ ┌───┐ ┌───┐ │    ┌───┐           │   ┌─────────────────────┐  │
│  │   │ │   │ │   │ │    │   │ Botas     │   │ Herramienta Activa   │  │
│  └───┘ └───┘ └───┘ │    └───┘           │   └─────────────────────┘  │
│                     │                     │                              │
│  Capacidad: 10/20   │  Defensa Total: 15  │   Arma equipada: Espada    │
├─────────────────────┴─────────────────────┴─────────────────────────────┤
│                              INFO ITEM                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Nombre del Item                                                 │  │
│  │  Tipo: Arma | Rareza: Raro | Daño: 15-20                        │  │
│  │  Descripción del item con sus estadísticas...                    │  │
│  │  [Equipar] [Usar] [Tirar] [Favorito]                             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Sección 1: Alforjas

### Slots Base
- **Capacidad inicial**: 10 slots
- **Capacidad máxima**: 20 slots (con mejoras)
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

> [PENDIENTE] ¿Cómo se amplía el inventario?
> - [ ] Misiones específicas
> - [ ] Compra en tiendas
> - [ ] Subir de nivel
> - [ ] Items especiales (Mochilas)

---

## Sección 2: Equipamiento

### Slots de Equipamiento

| Slot | Descripción | Stat Principal |
|------|-------------|---------------|
| **Casco** | Protección de cabeza | Defensa + Resistencia mágica |
| **Peto** | Protección de torso | Defensa principal |
| **Guantes** | Protección de manos | Defensa + Velocidad ataque |
| **Botas** | Protección de pies | Defensa + Velocidad movimiento |

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

> [PENDIENTE] ¿Implementar sets con bonificaciones?
> - [ ] Sí, con bonificaciones por 2/4 piezas
> - [ ] No, cada pieza es independiente
> - [ ] Sets cosméticos únicamente

---

## Sección 3: Armas/Herramientas en Mano

### Slots de Mano

| Slot | Descripción | Uso |
|------|-------------|-----|
| **Mano Izquierda** | Arma secundaria, escudo, o herramienta | Combate o utilidad |
| **Mano Derecha** | Arma principal o herramienta | Combate o utilidad |

### Tipos de Armas

| Tipo | Manos | Daño Base | Velocidad |
|------|-------|-----------|-----------|
| Espada a una mano | 1 | Medio | Rápida |
| Espada a dos manos | 2 | Alto | Lenta |
| Daga | 1 | Bajo | Muy rápida |
| Arco | 2 | Medio | Media |
| Bastón mágico | 1 | Bajo | Media |
| Escudo | 1 | N/A | N/A (Defensa) |

### Herramientas

| Herramienta | Uso | Durabilidad |
|-------------|-----|--------------|
| Pico | Minar | Sí |
| Hacha | Talar | Sí |
| Caña de pescar | Pescar | Sí |
| Kit de crafteo | Craftear en campo | No |
| Antorcha | Iluminar | Sí (consume) |

### Sistema de Dos Manos

> [PENDIENTE] ¿Cómo funciona el equipamiento de dos manos?
> - [ ] Arma de dos manos ocupa ambos slots
> - [ ] Arma de dos manos + slot vacío obligatorio
> - [ ] Permitir arma dos manos + escudo en espalda

---

## Sistema de Rareza

### Colores y Efectos Visuales

| Rareza | Color | Efecto UI |
|--------|-------|-----------|
| Común | Gris | Sin brillo |
| Poco Común | Verde | Brillo suave |
| Raro | Azul | Brillo medio |
| Épico | Morado | Brillo intenso |
| Legendario | Naranja | Brillo + Partículas |
| Único | Rojo | Brillo + Partículas + Animación |

### Stats por Rareza

| Rareza | Modificadores | Ejemplo |
|--------|---------------|---------|
| Común | Base | Espada: 10-15 daño |
| Poco Común | +1 modificador | Espada: 11-16 daño |
| Raro | +2 modificadores | Espada: 12-17 daño + velocidad |
| Épico | +3 modificadores | Espada: 13-18 daño + velocidad + crítico |
| Legendario | +4 modificadores + efecto | Espada: 15-20 daño + efecto especial |
| Único | Stats únicos | Stats predefinidos |

---

## Sistema de Peso

> [PENDIENTE] ¿Implementar sistema de peso?
> - [ ] Sin límite de peso (solo slots)
> - [ ] Peso limitado con penalizaciones
> - [ ] Peso afecta velocidad/stamina

### Opción: Sistema de Peso (si se implementa)

```json
{
  "peso_total": 45,
  "capacidad_peso": 100,
  "penalizacion": {
    "velocidad": -5,  // Si peso > 70%
    "stamina_regen": -10  // Si peso > 90%
  }
}
```

---

## Sistema de Favoritos

> [PENDIENTE] ¿Sistema de items favoritos?
> - [ ] Sí, marcar items como favoritos
> - [ ] No, no es necesario
> - [ ] Solo para consumibles de acceso rápido

### Opción: Items Favoritos (si se implementa)

- Los items favoritos aparecen primero en la lista
- Icono de estrella en la esquina del item
- Acceso rápido con teclas 1-5

---

## Sistema de Ordenamiento

> [PENDIENTE] ¿Ordenamiento automático?
> - [ ] Por tipo (consumibles, armas, etc.)
> - [ ] Por rareza (legendario → común)
> - [ ] Por valor (más caros primero)
> - [ ] Manual (el jugador decide)
> - [ ] Híbrido (auto + ajuste manual)

---

## Inventario Compartido (Stash)

> [PENDIENTE] ¿Sistema de stash/baúl?
> - [ ] Sí, stash en ubicaciones seguras
> - [ ] Stash global accesible desde cualquier lugar
> - [ ] No, inventario personal únicamente

### Opción: Sistema de Stash (si se implementa)

```json
{
  "stash": {
    "ubicaciones": ["pueblo_principal", "campamento_base"],
    "capacidad": 50,
    "items": []
  }
}
```

---

## Sistema de Identificación

> [PENDIENTE] ¿Items no identificados?
> - [ ] Sí, items raros necesitan identificación
> - [ ] No, todos los items son visibles
> - [ ] Solo items legendarios/únicos

---

## Sistema de Durabilidad

> [PENDIENTE] ¿Sistema de durabilidad?
> - [ ] Sí, items se desgastan
> - [ ] Solo armas y armaduras
> - [ ] No, los items no se rompen

Ver documento: `SISTEMA_DURABILIDAD.md`

---

## Sistema de Encantamientos

> [PENDIENTE] ¿Sistema de encantamientos?
> - [ ] Sí, items pueden encantarse
> - [ ] Solo items raros o superiores
> - [ ] No, los items tienen stats fijos

---

## Sistema de Trading

> [PENDIENTE] ¿Sistema de venta a NPCs?
> - [ ] Sí, con precios variables según reputación
> - [ ] Sí, con precios fijos
> - [ ] No, solo sistema de trueque

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
      "botas": null
    },
    "manos": {
      "izquierda": null,
      "derecha": null
    },
    "herramienta_activa": null,
    "oro": 150
  }
}
```

---

## Interacciones del Inventario

### Acciones Disponibles

| Acción | Descripción | Atajo |
|--------|-------------|-------|
| **Equipar** | Mueve item a slot de equipamiento | Doble click |
| **Usar** | Usa un consumible | Click derecho → Usar |
| **Tirar** | Elimina el item del inventario | Click derecho → Tirar |
| **Favorito** | Marca/desmarca como favorito | Click derecho → Favorito |
| **Info** | Muestra información detallada | Hover |
| **Dividir** | Divide un stack | Shift + Click |
| **Mover** | Reorganiza items | Arrastrar |

### Drag and Drop

- Arrastrar entre slots de alforjas → Reorganiza
- Arrastrar a equipamiento → Equipa
- Arrastrar a manos → Equipa en mano
- Arrastrar fuera del inventario → Tirar

---

## Preguntas para Definir

### Alta Prioridad

1. **Ampliación de alforjas**: ¿Cómo se amplía el inventario?
   > [PENDIENTE]

2. **Sistema de peso**: ¿Implementar límite de peso?
   > [PENDIENTE]

3. **Stash compartido**: ¿Sistema de baúl?
   > [PENDIENTE]

4. **Items favoritos**: ¿Sistema de marcado?
   > [PENDIENTE]

5. **Ordenamiento**: ¿Automático o manual?
   > [PENDIENTE]

### Media Prioridad

6. **Sets de equipamiento**: ¿Bonificaciones por set?
   > [PENDIENTE]

7. **Armas de dos manos**: ¿Cómo funcionan?
   > [PENDIENTE]

8. **Items no identificados**: ¿Sistema de identificación?
   > [PENDIENTE]

9. **Encantamientos**: ¿Sistema de mejora de items?
   > [PENDIENTE]

10. **Trading**: ¿Sistema de venta a NPCs?
    > [PENDIENTE]

### Baja Prioridad

11. **Durabilidad**: ¿Items se rompen?
    > [PENDIENTE - Ver SISTEMA_DURABILIDAD.md]

12. **Comparación de items**: ¿Mostrar comparación al equipar?
    > [PENDIENTE]

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

*Sistema documentado - Versión 2.0*
*Dependencias: SISTEMA_ITEMS.md, SISTEMA_DURABILIDAD.md, SISTEMA_STATS.md*