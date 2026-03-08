# Sistema de Items - Last Adventurer

## Categorías de Items

### 1. Armas (20 items)

**Estructura propuesta:**
```
Armas:
├── Espadas (5)
├── Espadones (4)
├── Arcos (4)
├── Dagas (4)
├── Magia/Catalizadores (3)
```

**Preguntas:**

- [ ] **¿Requisitos de nivel?** ¿El jugador necesita nivel X para equipar armas?
  - Respuesta: Si, va a necesitar niveles especificos o incluso perks. Por ejemplo, que para llevar una espada del infierno, deba tener algún perk que le permita no recibir daño de fuego. 

- [ ] **¿Requisitos de habilidad?** ¿Necesitas nivel 10 en Espada para usar una espada avanzada?
  - Respuesta: No, el requisito de habilidad es el tipo de daño que da la arma. Por ejemplo, una espada de fuego solo puede ser usada por un personaje que tenga el perk de fuego.

- [ ] **¿Tipos de daño?** ¿Físico/Mágico? ¿Cortante/Contundente/Punzante?
  - Respuesta: Físico/Mágico

- [ ] **¿Rareza?** ¿Hay rareza de items? (Común, Raro, Épico, Legendario)
  - Respuesta: Común, Raro, Épico, Legendario. Quisiera crear templates de armas base para crear un sistema de aleatoriedad que permita forjar armas personalizadas con nombres y perks personalizados con sistema de rareza.

- [ ] **¿Armas con perks?** ¿Algunas armas dan perks pasivos al equiparlas?
  - Respuesta: Si, algunas armas podran tener perks pasivos tanto positivos como negativos. No siempre tendran ambos, pero dependerá el tipo de arma.

- [ ] **¿Daño base por arma?** ¿Cada arma tiene su propio daño base?
  - Respuesta: Si, cada arma tendrá su propio daño base.

---

### 2. Objetos de Salud (10 items)

**Estructura propuesta:**
```
Salud:
├── Pociones HP (4-5)
├── Pociones Mana (2-3)
├── Pociones Stamina (2)
├── Pociones Buff (1-2)
```

**Preguntas:**

- [ ] **¿Tipos de curación?** ¿Solo HP? ¿También Mana/Stamina?
  - Respuesta: Si, pociones de HP, Mana y Stamina.

- [ ] **¿Curación instantánea o overtime?** ¿Poción cura 50 HP ya o 10 HP por 5 segundos?
  - Respuesta: Poción cura 50 HP ya.

- [ ] **¿Límite por combate?** ¿Cuántas pociones se pueden usar por pelea?
  - Respuesta: No hay límite.

- [ ] **¿Pociones de buff?** ¿Poción de fuerza (+ATK temporal)? ¿Duración?
  - Respuesta: Me gusta la idea. Podriamos añadir incluso un sistema de creacion de pociones personalizadas con nombres y perks personalizados con sistema de rareza que aumenten duracion, cantidad de curacion, etc.

- [ ] **¿Se guardan en inventario?** ¿O se usan inmediatamente?
  - Respuesta: Se guardan en inventario.

---

### 3. Armaduras (10 sets)

**Estructura propuesta:**
```
Armaduras:
├── Ligeras (3 sets) - Poca defensa, sin penalización
├── Medias (4 sets) - Defensa media, penalización leve
├── Pesadas (3 sets) - Mucha defensa, penalización alta
```

**Preguntas:**

- [ ] **¿Sets completos o piezas?** ¿Set completo = 1 item? ¿O Casco + Peto + Guantes + Botas?
  - Respuesta: Casco, Peto, Guantes y Botas.

- [ ] **¿Armadura pesa?** ¿Armadura pesada reduce velocidad/esquivar?
  - Respuesta: No, pero te cohibe usar armas en su maximo esplendor. Por ejemplo, una armadura pesada puede reducir el daño hecho con arco pues te cuesta moverte bien para apuntar o algo asi.

- [ ] **¿Requisitos?** ¿Necesitas ciertos stats para equipar armaduras?
  - Respuesta: No.

- [ ] **¿Set bonuses?** ¿Bonus por usar set completo?
  - Respuesta: Dependiendo de la armadura.

- [ ] **¿Reducción de daño plana o porcentaje?** ¿Armadura da +5 DEF o +5% reducción?
  - Respuesta: Porcentaje.

---

### 4. Preguntas Generales

- [ ] **¿Cómo se consiguen los items?**
  - [ ] Drops de enemigos
  - [ ] Tiendas
  - [ ] Misiones
  - [ ] Crafteo
  - Respuesta: Todas las anteriores.

- [ ] **¿Durabilidad?** ¿Las armas se rompen con uso?
  - Respuesta: Si, se podrá crear tambien sistema de durabilidad y herreria para mejorarlas o repararlas.

- [ ] **¿Mejoras?** ¿Se pueden mejorar armas? ¿Cómo?
  - Respuesta: Si, se podrá crear tambien sistema de mejora de armas.

- [ ] **¿Inventario limitado?** ¿Cuántos items puede llevar el jugador?
  - Respuesta: 10 slots base. Ampleable con mejoras de inventario.

- [ ] **¿Stack de items?** ¿Las pociones se apilan (stack) o ocupan 1 slot cada una?
  - Respuesta: Las pociones se apilan (stack de 10).

- [ ] **¿Items consumibles vs equipables?** ¿Cómo diferenciamos en el JSON?
  - Respuesta: Consumibles son pociones, etc. Equipables son armas, armaduras, etc.

---

### 5. Estructura JSON Propuesta

**Arma:**
```json
{
  "nombre": "Espada de Hierro",
  "tipo": "arma",
  "subtipo": "espada",
  "daño": 5,
  "requisito_nivel": 1,
  "requisito_habilidad": null,
  "rareza": "comun",
  "perk": null
}
```

**Poción:**
```json
{
  "nombre": "Poción Pequeña",
  "tipo": "consumible",
  "subtipo": "pocion_hp",
  "efecto": 20,
  "curacion_instantanea": true,
  "rareza": "comun"
}
```

**Armadura:**
```json
{
  "nombre": "Armadura de Cuero",
  "tipo": "armadura",
  "subtipo": "ligera",
  "defensa": 5,
  "penalizacion": 0,
  "requisito_nivel": 1,
  "rareza": "comun"
}
```

---

### 6. Lista de Items a Definir

#### Armas - Espadas (5)
| # | Nombre | Daño | Requisitos | Rareza |
|---|--------|------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

#### Armas - Espadones (4)
| # | Nombre | Daño | Requisitos | Rareza |
|---|--------|------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

#### Armas - Arcos (4)
| # | Nombre | Daño | Requisitos | Rareza |
|---|--------|------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

#### Armas - Dagas (4)
| # | Nombre | Daño | Requisitos | Rareza |
|---|--------|------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

#### Armas - Catalizadores/Magia (3)
| # | Nombre | Daño | Requisitos | Rareza |
|---|--------|------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

#### Pociones HP (4-5)
| # | Nombre | Curación | Instantánea? | Rareza |
|---|--------|----------|--------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

#### Pociones Mana/Stamina (4-5)
| # | Nombre | Tipo | Cantidad | Rareza |
|---|--------|------|-----------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

#### Pociones Buff (1-2)
| # | Nombre | Efecto | Duración | Rareza |
|---|--------|--------|----------|--------|
| 1 | | | | |
| 2 | | | | |

#### Armaduras Ligeras (3 sets)
| # | Nombre | Defensa | Penalización | Rareza |
|---|--------|---------|--------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

#### Armaduras Medias (4 sets)
| # | Nombre | Defensa | Penalización | Rareza |
|---|--------|---------|--------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

#### Armaduras Pesadas (3 sets)
| # | Nombre | Defensa | Penalización | Rareza |
|---|--------|---------|--------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## Notas Adicionales

<!-- Agrega aquí cualquier idea o comentario adicional sobre el sistema de items -->