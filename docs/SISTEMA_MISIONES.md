# Sistema de Misiones - Last Adventurer

## Concepto

Misiones que dan experiencia, items y desbloquean contenido. Tipos: principales, secundarias y repetibles.

---

## Tipos de Misiones

| Tipo | Descripción | Recompensa |
|------|-------------|------------|
| Principal | Historia del juego | Experiencia alta, items únicos |
| Secundaria | Contenido adicional | Experiencia media, oro |
| Repetible | Se puede hacer múltiples veces | Experiencia baja, materiales |
| Diario | Se renueva cada día | Experiencia media, oro |

---

## Objetivos de Misión

| Objetivo | Descripción |
|----------|-------------|
| Matar | Derrotar X enemigos de tipo Y |
| Recolectar | Obtener X items |
| Explorar | Llegar a una zona |
| Hablar | Conversar con NPC |
| Entregar | Llevar item a NPC |
| Escoltar | Proteger a NPC |

---

## Recompensas

### Tipos de Recompensa

| Recompensa | Descripción |
|------------|-------------|
| Experiencia | Sube nivel del personaje |
| Oro | Moneda del juego |
| Item | Arma, armadura, poción |
| Desbloqueo | Nueva zona, habilidad, NPC |

---

## Preguntas a Definir

- [ ] **¿Límite de misiones activas?**
  - Sin límite
  - 5 misiones activas
  - Respuesta:

- [ ] **¿Misiones con tiempo?**
  - Misiones que expiran
  - Sin límite de tiempo
  - Respuesta:

- [ ] **¿Misiones en cadena?**
  - Misiones que desbloquean otras
  - Respuesta:

- [ ] **¿Recompensas opcionales?**
  - Objetivos extra para más recompensa
  - Respuesta:

- [ ] **¿Misiones de facción?**
  - Misiones específicas de grupos/NPCs
  - Sistema de reputación
  - Respuesta:

---

## Estructura JSON Propuesta

### Misión
```json
{
  "id": "mision_001",
  "nombre": "Los Lobos del Bosque",
  "tipo": "secundaria",
  "descripcion": "Los aldeanos necesitan ayuda para reducir la población de lobos.",
  "objetivos": [
    {"tipo": "matar", "objetivo": "lobo", "cantidad": 5, "actual": 0}
  ],
  "recompensas": {
    "experiencia": 100,
    "oro": 50,
    "items": [
      {"id": "pocion_hp", "cantidad": 2}
    ]
  },
  "requisitos": {
    "nivel_minimo": 1,
    "mision_previa": null
  },
  "estado": "disponible"
}
```

### Estados de Misión

| Estado | Descripción |
|--------|-------------|
| Disponible | Se puede aceptar |
| Activa | En progreso |
| Completada | Terminada |
| Fallida | Tiempo agotado o objetivo perdido |

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de misiones -->