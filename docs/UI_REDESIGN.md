# UI Redesign - Last Adventurer

## Estado Actual y Análisis

### Visión General
El UI actual tiene una base sólida con tema medieval oscuro, pero presenta problemas de **usabilidad, jerarquía visual y experiencia de usuario** que necesitan ser abordados.

---

## Problemas Identificados

### 1. Pantalla Principal (Home)

**Problemas:**
- ❌ Antorchas animadas son distracciones visuales innecesarias
- ❌ El título "LAST ADVENTURER" es demasiado grande (text-7xl/8xl)
- ❌ Botones sin jerarquía clara (todos mismo tamaño)
- ❌ Fondo demasiado oscuro, falta profundidad
- ❌ No hay preview del juego o screenshots
- ❌ "Opciones" está disabled sin explicación

**Soluciones:**
- Reducir tamaño del título a text-4xl/5xl
- Añadir subtítulo con lore del juego
- Crear botón primario (Nueva Partida) más prominente
- Añadir preview cards con features del juego
- Implementar sistema de opciones funcional

### 2. Pantalla de Juego (Game Page)

**Problemas:**
- ❌ Header ocupa demasiado espacio vertical
- ❌ Sidebar de personaje es un modal, debería ser siempre visible
- ❌ Navegación de tabs no indica contexto actual
- ❌ No hay minimapa o indicador de ubicación
- ❌ Falta feedback visual de acciones del jugador

**Soluciones:**
- Rediseñar header como barra compacta
- Sidebar permanente con toggle para colapsar
- Añadir breadcrumb de ubicación actual
- Implementar minimapa en esquina
- Sistema de notificaciones/toasts

### 3. Panel de Exploración

**Problemas:**
- ❌ Información de zona es texto plano sin jerarquía
- ❌ Botón "EXPLORAR ZONA" es el único elemento interactivo
- ❌ Log de exploración es aburrido (solo texto)
- ❌ No hay representación visual del mapa/zona
- ❌ Eventos son modales que interrumpen el flujo

**Soluciones:**
- Añadir visualización del bioma (imagen/animación)
- Crear mini-mapa de la zona actual
- Log con iconos y colores por tipo de evento
- Eventos como cards deslizantes, no modales
- Añadir acciones contextuales (buscar, investigar, descansar)

### 4. Panel de Inventario

**Problemas:**
- ❌ No hay grid visual de items
- ❌ Falta categorización (armas, armaduras, consumibles)
- ❌ No hay preview de stats de items
- ❌ Falta comparación de equipamiento

**Soluciones:**
- Grid de slots estilo RPG
- Tabs de categorías con iconos
- Tooltip con stats detallados
- Sistema de comparación equipado vs nuevo

### 5. Panel de Combate

**Problemas:**
- ❌ HUD de combate es básico
- ❌ No hay animaciones de ataque
- ❌ Log de combate es texto plano
- ❌ Falta indicador de turnos
- ❌ No hay preview de daño/efectos

**Soluciones:**
- HUD con barras animadas de HP/Mana
- Animaciones de ataque básicas
- Log con colores por tipo de acción
- Indicador visual de turno actual
- Preview de daño antes de confirmar

### 6. Sidebar de Personaje

**Problemas:**
- ❌ Es un modal, debería ser sidebar permanente
- ❌ Demasiado padding/espacio vacío
- ❌ Stats son solo números sin contexto
- ❌ Sendas de combate están ocultas en accordion
- ❌ No hay preview de cómo afectan los stats

**Soluciones:**
- Sidebar colapsable permanente
- Layout más compacto con más información
- Tooltips explicativos para cada stat
- Sendas visibles por defecto
- Calculadora de stats al mejorar

---

## Nueva Arquitectura de UI

### Layout Principal

```
┌─────────────────────────────────────────────────────────────────┐
│  [≡] Last Adventurer    │ Ubicación: Bosque Ancestral    │ ⚙️ 💾 │
│  Lv.5 Guerrero          │ Día 1 - Mañana                 │       │
├─────────────────────────────────────────────────────────────────┤
│         │                                                       │
│  SIDEBAR │              CONTENIDO PRINCIPAL                      │
│  ─────── │                                                       │
│  Avatar  │   ┌─────────────────────────────────────────────┐    │
│  HP ████ │   │                                             │    │
│  MP ███░ │   │           PANEL ACTIVO                       │    │
│  ST ██░░ │   │                                             │    │
│          │   │   (Exploración / Inventario / Combate)      │    │
│  Stats   │   │                                             │    │
│  ─────── │   │                                             │    │
│  ATK  15 │   │                                             │    │
│  DEF  8% │   │                                             │    │
│  SPD  12 │   │                                             │    │
│  CRT  5% │   └─────────────────────────────────────────────┘    │
│  EVA  3% │                                                       │
│          │   ┌─────────────────────────────────────────────┐    │
│  Sendas  │   │  MINIMAPA / LOG / ACCIONES RÁPIDAS          │    │
│  ─────── │   └─────────────────────────────────────────────┘    │
│          │                                                       │
├─────────────────────────────────────────────────────────────────┤
│  [Explorar] [Inventario] [Combate] [Mapa] [Diario]              │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Header Compacto
```tsx
// Altura: 48px
// Contenido: Logo pequeño + Ubicación + Tiempo + Acciones
// Sticky: Sí
```

#### 2. Sidebar Permanente
```tsx
// Ancho: 280px (colapsable a 60px)
// Contenido: Avatar, Stats, Sendas
// Posición: Izquierda, siempre visible
```

#### 3. Panel de Exploración Rediseñado
```tsx
// Layout: 2 columnas
// Izquierda: Visual del bioma + Minimapa
// Derecha: Acciones + Log + Eventos
```

#### 4. Sistema de Notificaciones
```tsx
// Posición: Esquina superior derecha
// Tipos: Info, Success, Warning, Error
// Auto-dismiss: 3 segundos
```

---

## Sistema de Diseño

### Colores (Refinados)

```css
/* Tema Medieval Oscuro - Refinado */
--bg-primary: #0a0a0f;      /* Fondo principal */
--bg-secondary: #12121a;    /* Cards y paneles */
--bg-tertiary: #1a1a25;     /* Hover states */

--gold-primary: #d4a843;    /* Acento principal */
--gold-light: #f0c654;      /* Hover */
--gold-dark: #a67c00;       /* Active */

--text-primary: #e8e4d9;    /* Texto principal */
--text-secondary: #9a978a;  /* Texto secundario */
--text-muted: #6b6b6b;      /* Texto deshabilitado */

--hp: #c44536;              /* Salud */
--mana: #3b82f6;            /* Energía */
--stamina: #22c55e;         /* Resistencia */
--exp: #d4a843;             /* Experiencia */

--danger: #ef4444;          /* Error/Peligro */
--success: #22c55e;         /* Éxito */
--warning: #f59e0b;         /* Advertencia */
```

### Tipografía

```css
/* Títulos - Cinzel */
.font-title {
  font-family: 'Cinzel', serif;
  letter-spacing: 0.05em;
}

/* UI - Inter */
.font-ui {
  font-family: 'Inter', sans-serif;
}

/* Jerarquía */
.text-display: 48px;   /* Título principal */
.text-title: 32px;     /* Títulos de sección */
.text-subtitle: 20px;  /* Subtítulos */
.text-body: 16px;      /* Texto normal */
.text-caption: 12px;   /* Captions */
.text-micro: 10px;     /* Labels pequeños */
```

### Espaciado

```css
/* Sistema de espaciado consistente */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

### Componentes Base

#### Botones
```tsx
// Variantes: primary, secondary, ghost, danger
// Tamaños: sm, md, lg
// Estados: default, hover, active, disabled, loading

// Ejemplo:
<Button variant="primary" size="lg" loading={false}>
  Explorar
</Button>
```

#### Cards
```tsx
// Variantes: default, elevated, interactive
// Con header, contenido y footer opcionales

<Card variant="elevated">
  <CardHeader>Título</CardHeader>
  <CardContent>Contenido</CardContent>
  <CardFooter>Acciones</CardFooter>
</Card>
```

#### Barras de Progreso
```tsx
// Variantes: hp, mana, stamina, exp
// Con animación de transición
// Con tooltip de valores

<ProgressBar type="hp" current={80} max={100} showLabel />
```

---

## Plan de Implementación

### Fase 1: Fundamentos (2-3 días)

1. **Sistema de Diseño**
   - [ ] Crear `styles/design-tokens.css`
   - [ ] Actualizar `globals.css` con nuevos tokens
   - [ ] Crear componentes base en `components/ui/`

2. **Layout Principal**
   - [ ] Rediseñar `GameHeader` (compacto)
   - [ ] Crear `GameLayout` con sidebar permanente
   - [ ] Implementar sistema de notificaciones

### Fase 2: Pantalla Principal (1-2 días)

1. **Home Page**
   - [ ] Rediseñar hero section
   - [ ] Añadir feature cards
   - [ ] Mejorar selector de slots
   - [ ] Implementar página de opciones

### Fase 3: Sidebar de Personaje (1-2 días)

1. **CharacterSidebar**
   - [ ] Convertir a sidebar permanente
   - [ ] Añadir modo colapsable
   - [ ] Mejorar visualización de stats
   - [ ] Añadir tooltips explicativos

### Fase 4: Panel de Exploración (2-3 días)

1. **ExplorarPanel**
   - [ ] Añadir visualización de bioma
   - [ ] Crear minimapa de zona
   - [ ] Mejorar log de exploración
   - [ ] Rediseñar sistema de eventos

### Fase 5: Panel de Inventario (2-3 días)

1. **InventarioPanel**
   - [ ] Crear grid de slots
   - [ ] Implementar categorías
   - [ ] Añadir tooltips de items
   - [ ] Sistema de comparación

### Fase 6: Panel de Combate (2-3 días)

1. **CombatePanel**
   - [ ] Rediseñar HUD de combate
   - [ ] Añadir animaciones básicas
   - [ ] Mejorar log de combate
   - [ ] Indicador de turnos

---

## Archivos a Crear/Modificar

### Nuevos Archivos

```
frontend/src/
├── styles/
│   └── design-tokens.css        # Sistema de diseño
├── components/
│   ├── layout/
│   │   ├── GameLayout.tsx      # Layout principal
│   │   ├── Sidebar.tsx         # Sidebar colapsable
│   │   └── NotificationToast.tsx
│   ├── game/
│   │   ├── Minimap.tsx         # Minimapa
│   │   ├── BiomeVisual.tsx     # Visual de bioma
│   │   ├── ActionLog.tsx       # Log con iconos
│   │   └── QuickActions.tsx    # Acciones rápidas
│   └── ui/
│       ├── ProgressBar.tsx     # Barras animadas
│       ├── ItemSlot.tsx        # Slot de item
│       └── Tooltip.tsx         # Tooltips mejorados
```

### Archivos a Modificar

```
frontend/src/
├── app/
│   ├── page.tsx                # Home rediseñado
│   ├── layout.tsx              # Layout con providers
│   └── juego/page.tsx          # Layout de juego
├── components/
│   ├── juego/
│   │   ├── GameHeader.tsx      # Header compacto
│   │   ├── GameNav.tsx         # Nav mejorada
│   │   ├── CharacterSidebar.tsx # Sidebar permanente
│   │   └── panels/
│   │       ├── ExplorarPanel.tsx
│   │       ├── InventarioPanel.tsx
│   │       └── CombatePanel.tsx
│   └── ui/
│       └── button.tsx          # Variantes mejoradas
```

---

## Prioridades

### Alta Prioridad (Must Have)
1. ✅ Sistema de diseño consistente
2. ✅ Layout con sidebar permanente
3. ✅ Header compacto
4. ✅ Panel de exploración funcional

### Media Prioridad (Should Have)
1. Minimapa de zona
2. Sistema de notificaciones
3. Grid de inventario
4. Animaciones de combate

### Baja Prioridad (Nice to Have)
1. Visual de biomas animado
2. Transiciones entre paneles
3. Sonidos/UI feedback
4. Temas alternativos

---

## Referencias de Diseño

### Juegos de Referencia
- **Darkest Dungeon**: UI oscura, tipografía medieval
- **Slay the Spire**: Cards, iconos claros
- **Dead Cells**: HUD compacto, barras de vida
- **Hades**: Interacciones fluidas, feedback visual

### Principios de UI/UX
1. **Claridad**: Información importante siempre visible
2. **Jerarquía**: Tamaño y color guían la atención
3. **Feedback**: Acciones tienen respuesta visual inmediata
4. **Eficiencia**: Mínimo clicks para acciones comunes
5. **Accesibilidad**: Contraste suficiente, tamaños legibles

---

## Próximos Pasos

1. **Revisar y aprobar** este documento
2. **Crear rama** `feature/ui-redesign`
3. **Implementar Fase 1** (Sistema de diseño)
4. **Iterar** con feedback del usuario

---

## Notas Adicionales

- Mantener compatibilidad con el backend actual
- No cambiar endpoints ni tipos de datos
- Tests visuales en cada fase
- Documentar cambios en CHANGELOG