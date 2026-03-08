# Sistema de Creación de Personaje - Last Adventurer

## Flujo Actual

```
1. Menú Principal → "Nueva Partida"
2. Input: Nombre del personaje
3. Selección: Arquetipo (Guerrero, Mago, Arquero, Paladín)
4. Se asignan stats según arquetipo
5. Se guarda en slot libre
6. Inicia el juego
```

---

## Estado Actual

| Componente | Estado |
|------------|--------|
| `game_manager.py` | ✅ Básico - Pide nombre y clase |
| `arquetipos.json` | ✅ 4 clases con stats |
| `personaje.py` | ✅ Integrado con Stats y Habilidades |
| `save_manager.py` | ✅ Guarda/carga partidas |

---

## Preguntas de Diseño

### 1. ¿Los arquetipos definen stats fijos o base?

**Opción A:** Stats fijos
- Guerrero siempre empieza con HP:120, ATK:18, DEF:8
- Sin variación

**Opción B:** Stats base + puntos extra para distribuir
- Guerrero: HP base 100 + 20 extra, ATK 15 + 3 extra
- El jugador elige dónde poner los puntos extra
- Más personalización desde el inicio

**Opción C:** Stats base + bono pasivo único por clase
- Guerrero: HP:100, ATK:15, DEF:5 + Pasivo "Resistencia" (+10% HP)
- Cada clase tiene un pasivo único

> **Pregunta:** ¿Prefieres stats fijos simples o más personalización?
Respuesta: Si bien, existiran arquetipos. Ya no se elegiran al comienzo. Sino mediante misiones que se le daran al jugador para definir que tipo de arquetipo quiere jugar. me hago entender. Ahi si se define.
---

### 2. ¿Mostrar descripción detallada de cada clase?

**Opción A:** Solo stats
```
1. Guerrero - HP:120 ATK:18 DEF:8
```

**Opción B:** Stats + descripción corta
```
1. Guerrero - HP:120 ATK:18 DEF:8
   "Resistente en primera línea, ideal para principiantes"
```

**Opción C:** Pantalla de detalles antes de confirmar
```
Seleccionaste: Guerrero
┌─────────────────────────────────┐
│ HP: 120 (alto)                  │
│ ATK: 18 (medio-alto)            │
│ DEF: 8 (medio)                  │
│                                 │
│ Descripción: Tanque de daño,    │
│ ideal para absorber golpes y    │
│ proteger al equipo.             │
│                                 │
│ ¿Confirmar? (S/N)               │
└─────────────────────────────────┘
```

> **Pregunta:** ¿Cuánta información mostrar antes de elegir?

Respuesta: Opcion C
---

### 3. ¿Permitir cambiar de clase antes de confirmar?

**Opción A:** Un solo paso - eliges y ya está
**Opción B:** Vista previa con opción de volver
- Muestra resumen del personaje
- "¿Confirmar? (S)í / (N)o / (C)ambiar clase"

> **Pregunta:** ¿Vista previa antes de confirmar?
Respuesta: Opcion B
---

### 4. ¿Apariencia del personaje?

**Opción A:** Sin apariencia (solo texto)
**Opción B:** Género (Masculino/Femenino/No especificar)
- Solo afecta pronombres en diálogos
**Opción C:** Personalización visual futura
- Placeholder por ahora, se expande después

> **Pregunta:** ¿Agregar selección de género?
Respuesta: Opcion B
---

### 5. ¿Items iniciales?

Actualmente no se dan items. Opciones:

**Opción A:** Sin items iniciales
**Opción B:** Items básicos según clase
- Guerrero: Espada de Hierro, Escudo de Madera
- Mago: Bastón, 2 Pociones de Mana
- Arquero: Arco, 10 Flechas
- Paladín: Espada, Escudo

**Opción C:** Inventario base igual para todos
- 2 Pociones Pequeñas
- 1 Arma básica según clase

> **Pregunta:** ¿Items iniciales? ¿Cuáles?
Respuesta: Opcion A. Sin embargo, el usuario portará ropajes basicos pues sino significa que anda desnudo.
---

### 6. ¿Nombre del personaje obligatorio o con default?

**Opción A:** Obligatorio - no puede estar vacío
**Opción B:** Default si está vacío
- "Aventurero" si no ingresa nombre
- "Guerrero" si no ingresa nombre (según clase)

> **Pregunta:** ¿Permitir nombre vacío con default?
Respuesta: Opcion A. Minimo 3 caracteres.

---

### 7. ¿Tutorial después de crear personaje?

**Opción A:** Directo al juego
**Opción B:** Tutorial opcional
- "¿Deseas ver el tutorial? (S/N)"
**Opción C:** Tutorial obligatorio primera vez
- Se guarda en el save que ya vio el tutorial

> **Pregunta:** ¿Tutorial integrado?

Respuesta: opcion A pues aun no tenemos una ruta definida de como todo será. Quizas a furuto haya uno.
---

## Ideas Adicionales

### A. Sistema de "Background" (Trasfondo)

Antes de elegir clase, elegir trasfondo que da bonos menores:

| Trasfondo | Bono |
|-----------|------|
| Mercader | +50 oro inicial |
| Soldado | +5 ATK |
| Sanador | +1 Poción extra |
| Explorador | +5 Velocidad |

> **Pregunta:** ¿Interesa este sistema o es demasiado complejo para ahora?
Respuesta: me gusta la idea, pero no la implementemos aun.

---

### B. Dificultad inicial

| Dificultad | Efecto |
|------------|--------|
| Fácil | +20% HP, enemigos -10% daño |
| Normal | Sin modificadores |
| Difícil | -10% HP, enemigos +10% daño |

> **Pregunta:** ¿Implementar dificultad o dejar para después?
Respuesta: Si, añadelo.
---

### C. Resumen final antes de empezar

```
╔══════════════════════════════════╗
║     RESUMEN DEL PERSONAJE       ║
╠══════════════════════════════════╣
║ Nombre: Aelar                   ║
║ Clase:  Arquero                 ║
║ Nivel:  1                       ║
╠══════════════════════════════════╣
║ HP:     90    ATK: 20    DEF: 5 ║
╠══════════════════════════════════╣
║ Inventario inicial:             ║
║ - Arco                          ║
║ - 2 Pociones Pequeñas           ║
╚══════════════════════════════════╝

¿Comenzar aventura? (S/N)
```
Respuesta: Si, implementa eso
---

## Decisiones Finales

| Aspecto | Decisión |
|---------|----------|
| **Arquetipos** | NO se eligen al inicio. Se definen mediante misiones durante el juego |
| **Stats iniciales** | Base iguales para todos: HP:100, ATK:10, DEF:5, etc. |
| **Género** | Sí - Masculino/Femenino/No especificar (afecta pronombres en diálogos) |
| **Items iniciales** | Sin items de combate. Ropajes básicos (solo cosméticos, sin stats) |
| **Nombre** | Obligatorio, mínimo 3 caracteres |
| **Tutorial** | Sin tutorial por ahora |
| **Dificultad** | Sí implementar. Normal = base |
| **Resumen final** | Sí, con opción de editar antes de confirmar |
| **Trasfondo** | Para después |

---

## Modificadores de Dificultad

| Dificultad | HP Jugador | Daño Enemigo |
|------------|------------|--------------|
| Fácil | +20% | -10% |
| **Normal** | 0% (base) | 0% (base) |
| Difícil | -10% | +10% |

---

## Flujo Final de Creación

```
1. Menú Principal → "Nueva Partida"
2. [Si todos los slots ocupados] → Mensaje de error → Volver
3. Input: Nombre
   - Obligatorio, mínimo 3 caracteres
   - Validar y re-pedir si no cumple
4. Selección: Género
   - (M)asculino
   - (F)emenino
   - (N)o especificar
5. Selección: Dificultad
   - (1) Fácil - +20% HP, enemigos -10% daño
   - (2) Normal - Sin modificadores [DEFAULT]
   - (3) Difícil - -10% HP, enemigos +10% daño
6. Resumen final
   - Muestra todos los datos
   - Opciones: (C)onfirmar / (E)ditar nombre / (C)ambiar género / (D)ificultad
7. Confirmar → Guardar en slot libre
8. Iniciar juego
```

---

## Stats Base Iniciales

| Stat | Valor Base |
|------|------------|
| HP | 100 |
| ATK | 10 |
| DEF | 5 |
| Velocidad | 10 |
| Crítico | 5% |
| Evasión | 5% |
| Mana | 50 |
| Stamina | 100 |

---

## Archivos a Crear/Modificar

| Archivo | Cambios |
|---------|---------|
| `game_manager.py` | Nuevo flujo completo de creación |
| `models/personaje.py` | Agregar campo `genero`, `dificultad` |
| `models/stats.py` | Aplicar modificadores de dificultad |
| `systems/save_manager.py` | Guardar género y dificultad |
| `main.py` | Integrar nuevo flujo |
| `data/items.json` | Agregar "Ropajes Básicos" (cosmético) |

---

## Notas de Implementación

- Los arquetipos se desbloquean mediante misiones (no implementar aún)
- Los ropajes básicos son un item de tipo "cosmetico" sin efecto en stats
- El género solo afecta pronombres en diálogos futuros
- La dificultad se aplica al crear el personaje y se guarda
