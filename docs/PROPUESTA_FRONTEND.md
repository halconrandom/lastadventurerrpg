# Propuesta de Frontend - Last Adventurer

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Frontend** | Next.js 14+ (App Router) |
| **Estilos** | Tailwind CSS |
| **Estado** | React Context / Zustand |
| **Backend** | Python FastAPI (existente) |
| **Comunicación** | API REST + JSON |

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                    │
├─────────────────────────────────────────────────────────┤
│  app/                                                    │
│  ├── page.tsx              → Menú principal              │
│  ├── nueva-partida/        → Creación de personaje       │
│  ├── cargar-partida/       → Cargar partida              │
│  ├── juego/                → Pantalla principal del juego│
│  │   ├── page.tsx          → Vista general               │
│  │   ├── explorar/         → Exploración                 │
│  │   ├── inventario/       → Inventario                  │
│  │   ├── personaje/        → Stats y habilidades         │
│  │   └── combate/          → Sistema de combate          │
│  └── layout.tsx            → Layout principal            │
│                                                          │
│  components/                                             │
│  ├── ui/                   → Componentes reutilizables   │
│  ├── game/                 → Componentes del juego       │
│  └── layout/               → Header, Footer, etc.        │
│                                                          │
│  lib/                                                    │
│  ├── api.ts                → Llamadas a FastAPI          │
│  └── types.ts              → Tipos TypeScript            │
└─────────────────────────────────────────────────────────┘
                           │
                           │ API REST (fetch/axios)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                      │
├─────────────────────────────────────────────────────────┤
│  /api/                                                   │
│  ├── /personaje           → CRUD personaje               │
│  ├── /partida             → Guardar/cargar               │
│  ├── /combate             → Sistema de combate           │
│  └── /exploracion         → Exploración y encuentros     │
└─────────────────────────────────────────────────────────┘
```

---

## Estructura de Carpetas Propuesta

```
lastadventurer/
├── backend/                    # Python FastAPI
│   ├── main.py                 # Entry point FastAPI
│   ├── routers/                # API endpoints
│   │   ├── personaje.py
│   │   ├── partida.py
│   │   ├── combate.py
│   │   └── exploracion.py
│   ├── models/                 # Modelos existentes
│   ├── systems/                # Sistemas existentes
│   ├── data/                   # JSONs existentes
│   └── requirements.txt
│
├── frontend/                   # Next.js
│   ├── app/
│   │   ├── page.tsx            # Menú principal
│   │   ├── layout.tsx
│   │   ├── nueva-partida/
│   │   │   └── page.tsx
│   │   ├── cargar-partida/
│   │   │   └── page.tsx
│   │   └── juego/
│   │       ├── page.tsx
│   │       ├── explorar/
│   │       ├── inventario/
│   │       ├── personaje/
│   │       └── combate/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   ├── game/
│   │   │   ├── StatBar.tsx
│   │   │   ├── InventorySlot.tsx
│   │   │   ├── CombatLog.tsx
│   │   │   └── CharacterCard.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── lib/
│   │   ├── api.ts              # Funciones de API
│   │   └── types.ts            # Tipos TypeScript
│   ├── styles/
│   │   └── globals.css
│   ├── public/
│   │   └── images/             # Assets estáticos
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/                       # Documentación
└── README.md
```

---

## Preguntas de Diseño

### 1. Estética Visual

**1.1 ¿Qué estilo visual prefieres?**

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| **A. Medieval Fantástico** | Colores cálidos, texturas de pergamino, bordes dorados | Skyrim, Diablo |
| **B. Minimalista Moderno** | Colores oscuros, líneas limpias, sin decoración excesiva | Slay the Spire |
| **C. Pixel Art** | Estilo retro, sprites pixelados | Stardew Valley |
| **D. Otro** | Especificar |

> **Respuesta:** Opcion A

---

**1.2 ¿Paleta de colores base?**

| Opción | Colores |
|--------|---------|
| **A. Oscuro** | Fondo negro/gris oscuro, texto claro, acentos dorados/rojos |
| **B. Claro** | Fondo beige/blanco, texto oscuro, acentos verdes/azules |
| **C. Personalizada** | Especificar colores principales |

> **Respuesta:** Opcion A

---

**1.3 ¿Tipografía?**

| Opción | Estilo |
|--------|--------|
| **A. Serif medieval** | Tipografía con serifa, estilo antiguo (ej: Cinzel, MedievalSharp) |
| **B. Sans-serif moderna** | Limpia y legible (ej: Inter, Roboto) |
| **C. Monospace** | Estilo terminal/RPG clásico (ej: JetBrains Mono) |

> **Respuesta:** Opcion A

---

### 2. Pantallas Principales

**2.1 ¿Qué debe mostrar el Menú Principal?**

| Opción | Elementos |
|--------|-----------|
| **A. Minimalista** | Solo logo + 3 botones (Nueva Partida, Cargar, Salir) |
| **B. Con fondo** | Logo + botones + imagen de fondo animada/estática |
| **C. Con preview** | Logo + botones + preview de la última partida |

> **Respuesta:** Minimalista pero con un fondo animado como si fuera un calabozo con antorchas iluminando cada cierto tiempo, haciendo efecto de fuego.

---

**2.2 ¿Cómo mostrar la creación de personaje?**

| Opción | Descripción |
|--------|-------------|
| **A. Una pantalla, pasos secuenciales** | Wizard con pasos: Nombre → Género → Dificultad → Confirmar |
| **B. Todo en una pantalla** | Formulario completo con todos los campos visibles |
| **C. Cards interactivas** | Cards para cada decisión con animaciones |

> **Respuesta:** Opcion C. 

---

**2.3 ¿Layout del juego principal?**

| Opción | Descripción |
|--------|-------------|
| **A. Sidebar izquierdo** | Menú lateral + área principal central |
| **B. Tabs superiores** | Navegación por pestañas arriba + contenido abajo |
| **C. Panel único** | Una pantalla a la vez, navegación por botones |

> **Respuesta:** Tabs Superiores.

---

### 3. Componentes del Juego

**3.1 ¿Cómo mostrar los stats del personaje?**

| Opción | Descripción |
|--------|-------------|
| **A. Barras de progreso** | HP/Mana/Stamina como barras con colores |
| **B. Números grandes** | Solo números, sin barras |
| **C. Mixto** | Barras + números |

> **Respuesta:** Mixto. Sin embargo, eso en la tab de stats, en la pantalla principal, solo el nivel y experiencia de nivel.

---

**3.2 ¿Cómo mostrar el inventario?**

| Opción | Descripción |
|--------|-------------|
| **A. Grid** | Cuadrícula de slots (estilo Minecraft) |
| **B. Lista** | Lista vertical con detalles |
| **C. Ambos** | Toggle para cambiar entre vista grid y lista |

> **Respuesta:** Grid estilo Diablo.

---

**3.3 ¿Cómo mostrar el combate?**

| Opción | Descripción |
|--------|-------------|
| **A. Por turnos clásico** | Menú de acciones + log de combate + sprites de personajes |
| **B. Cards** | Acciones como cartas que se seleccionan |
| **C. Minimalista** | Solo texto + botones de acción |

> **Respuesta:** Por turnos clasico. 

---

### 4. Animaciones y Efectos

**4.1 ¿Nivel de animaciones?**

| Opción | Descripción |
|--------|-------------|
| **A. Ninguna** | Sin animaciones, solo transiciones instantáneas |
| **B. Básicas** | Fade in/out, hover effects, transiciones suaves |
| **C. Elaboradas** | Animaciones de ataque, partículas, efectos de daño |

> **Respuesta:** Elaboradas

---

**4.2 ¿Efectos de sonido?**

| Opción | Descripción |
|--------|-------------|
| **A. Sin audio** | Juego silencioso |
| **B. Música de fondo** | Solo música ambiental |
| **C. Efectos + música** | Clicks, sonidos de combate, música |

> **Respuesta:** opcion C

---

### 5. Backend y API

**5.1 ¿Cómo manejar el estado del juego?**

| Opción | Descripción |
|--------|-------------|
| **A. Solo backend** | Todo el estado en Python, frontend solo muestra |
| **B. Híbrido** | Estado en frontend, backend para persistencia |
| **C. LocalStorage + sync** | LocalStorage como cache, sync con backend |

> **Respuesta:** Opcion A

---

**5.2 ¿Autenticación?**

| Opción | Descripción |
|--------|-------------|
| **A. Sin auth** | Partidas locales, sin cuentas |
| **B. Usuario/contraseña simple** | Login básico para guardar en servidor |
| **C. OAuth** | Login con Google/Discord/etc. |

> **Respuesta:** Sin auth por ahora

---

**5.3 ¿Puerto del backend?**

| Opción | Puerto |
|--------|--------|
| **A. 8000** | Puerto por defecto de FastAPI |
| **B. 3001** | Para evitar conflictos con Next.js (3000) |
| **C. Otro** | Especificar |

> **Respuesta:** Opcion A

---

### 6. Assets y Recursos

**6.1 ¿Imágenes de personajes/enemigos?**

| Opción | Descripción |
|--------|-------------|
| **A. Placeholder** | Usar emojis o iconos simples por ahora |
| **B. Imágenes estáticas** | Imágenes PNG/JPG estáticas |
| **C. Sprites animados** | Spritesheets con animaciones |

> **Respuesta:** Usa iconos simples por ahora.

---

**6.2 ¿Iconos para items/habilidades?**

| Opción | Descripción |
|--------|-------------|
| **A. Emojis** | Usar emojis como iconos (⚔️ 🗡️ 🏹 etc.) |
| **B. Iconos SVG** | Librería como Heroicons o Lucide |
| **C. Imágenes propias** | Iconos personalizados |

> **Respuesta:** Iconos SVG de Lucide por ahora.

---

### 7. Responsive y Accesibilidad

**7.1 ¿Soporte móvil?**

| Opción | Descripción |
|--------|-------------|
| **A. Solo desktop** | Optimizado solo para PC |
| **B. Responsive** | Funciona en móvil pero no es óptimo |
| **C. Mobile-first** | Diseñado primero para móvil |

> **Respuesta:** Solo desktop por ahora

---

**7.2 ¿Idioma?**

| Opción | Descripción |
|--------|-------------|
| **A. Solo español** | Interfaz en español |
| **B. Solo inglés** | Interfaz en inglés |
| **C. Multiidioma** | Sistema de traducción (i18n) |

> **Respuesta:** Solo español. Pero ten presente que mas adelante implementaremos inglés.

---

### 8. Prioridad de Implementación

**8.1 ¿Qué implementar primero?**

Ordena de 1 (más importante) a 5 (menos importante):

| Pantalla | Orden |
|----------|-------|
| Menú Principal | 1 |
| Creación de Personaje | 3|
| Pantalla de Juego (stats/inventario) | 2 |
| Exploración | 5|
| Combate | 4 |

> **Respuesta:** 

---

## Resumen de Respuestas

> Completa las respuestas arriba y luego resumiremos las decisiones aquí.

---

## Siguiente Paso

Una vez definidas las respuestas:

1. Crear estructura de carpetas
2. Inicializar Next.js + Tailwind
3. Configurar FastAPI con CORS
4. Crear componentes base
5. Implementar primera pantalla priorizada
