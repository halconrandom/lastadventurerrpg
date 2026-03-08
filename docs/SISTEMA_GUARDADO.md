# Sistema de Guardado - Last Adventurer

## Concepto

Guardar el progreso del jugador en archivos JSON para persistencia de datos.

---

## Datos a Guardar

### Datos del Personaje
| Dato | Descripción |
|------|-------------|
| Nombre | Nombre del jugador |
| Nivel | Nivel general |
| Experiencia | Experiencia actual |
| Puntos disponibles | Puntos para asignar |
| HP/ATK/DEF | Stats actuales |

### Datos de Habilidades
| Dato | Descripción |
|------|-------------|
| Nivel de cada habilidad | Espada, Arco, Magia, etc. |
| Experiencia de cada habilidad | Progreso actual |
| Perks desbloqueados | Lista de perks |

### Datos de Inventario
| Dato | Descripción |
|------|-------------|
| Items | Lista de items con cantidades |
| Equipamiento | Items equipados |
| Materiales | Recursos para crafteo |
| Oro | Moneda del juego |

### Datos de Progreso
| Dato | Descripción |
|------|-------------|
| Misiones completadas | IDs de misiones |
| Misiones activas | Estado actual |
| Zonas desbloqueadas | Áreas visitadas |
| NPCs conocidos | Personajes encontrados |

---

## Estructura de Archivo

### Ubicación
```
saves/
├── slot_1.json
├── slot_2.json
└── slot_3.json
```

### Formato JSON Completo
```json
{
  "version": "1.0",
  "fecha": "2024-01-15T14:30:00",
  "personaje": {
    "nombre": "Aventurero",
    "nivel": 15,
    "experiencia": 1250,
    "puntos_disponibles": 3,
    "stats": {
      "hp_base": 100,
      "hp_actual": 85,
      "puntos_hp": 5,
      "atk_base": 10,
      "puntos_atk": 8,
      "def_base": 0,
      "puntos_def": 2
    }
  },
  "habilidades": {
    "Espada": {"nivel": 12, "experiencia": 450},
    "Arco": {"nivel": 5, "experiencia": 120},
    "Magia": {"nivel": 3, "experiencia": 50},
    "Dagas": {"nivel": 1, "experiencia": 0},
    "Defensa": {"nivel": 8, "experiencia": 300}
  },
  "perks_desbloqueados": [
    "Filo Afilado",
    "Puntería",
    "Piel Dura"
  ],
  "inventario": {
    "slots_maximos": 10,
    "items": [
      {"id": "espada_hierro_001", "cantidad": 1},
      {"id": "pocion_hp", "cantidad": 5}
    ],
    "materiales": [
      {"id": "hierro", "cantidad": 15},
      {"id": "madera", "cantidad": 8}
    ],
    "oro": 250
  },
  "equipamiento": {
    "arma": "espada_hierro_001",
    "casco": null,
    "peto": "armadura_cuero_001",
    "botas": null
  },
  "progreso": {
    "misiones_completadas": ["mision_001", "mision_002"],
    "misiones_activas": ["mision_003"],
    "zonas_visitadas": ["pueblo_inicio", "bosque"],
    "npcs_conocidos": ["herrero", "aldeano"]
  }
}
```

---

## Preguntas a Definir

- [ ] **¿Cuántos slots de guardado?**
  - 3 slots
  - 5 slots
  - Ilimitado
  - Respuesta: 3 Slots

- [ ] **¿Autoguardado?**
  - Guardado automático al entrar a zonas
  - Solo guardado manual
  - Respuesta: Guardado automático al realizar alguna accion. Excepto cuando estas en combate, ahi se guarda al iniciar el combate y al finalizarlo.

- [ ] **¿Guardar al salir?**
  - Guardar automáticamente
  - Preguntar si guardar
  - Respuesta: Guardar automáticamente

- [ ] **¿Versionado de datos?**
  - Sistema para actualizar saves antiguos
  - Respuesta: Si

- [ ] **¿Backup de saves?**
  - Crear copias de seguridad
  - Respuesta: No

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de guardado -->