# Sistema de Relaciones y Reputación

Este sistema gestiona todas las interacciones sociales del jugador con NPCs, facciones y el mundo. Define cómo se construyen, mantienen y rompen las relaciones, creando una red social dinámica y persistente.

## Pilares del Sistema

1. **Reputación Híbrida**: Sistema numérico (-100 a +100) combinado con estados discretos (Enemigo/Neutral/Aliado).
2. **Red de Relaciones**: Los NPCs tienen relaciones entre sí, creando una red compleja donde las acciones del jugador tienen efectos en cascada.
3. **Memoria Total**: NPCs recuerdan todo lo que el jugador ha hecho con/sobre ellos.
4. **Propagación de Información**: Las acciones se propagan por rutas y proximidad, no instantáneamente.

---

## Arquitectura de Datos

### 1. Reputación con NPCs

Cada NPC mantiene un registro de su relación con el jugador:

```json
{
  "npc_id": "npc_001",
  "nombre": "Haldor el Herrero",
  "reputacion": {
    "valor": 45,
    "estado": "amistoso",
    "modificadores": [
      {"causa": "ayudo_reparar_herradura", "valor": 10, "fecha": 12345678},
      {"causa": "compra_frecuente", "valor": 5, "fecha": 12345679}
    ]
  },
  "memoria": [
    {"evento": "primer_encuentro", "fecha": 12345000},
    {"evento": "ayudo_reparar_herradura", "fecha": 12345678},
    {"evento": "compro_espada", "fecha": 12345679}
  ],
  "opiniones": {
    "confianza": 60,
    "respeto": 40,
    "miedo": 0
  }
}
```

### 2. Estados de Relación

| Estado | Rango | Comportamiento |
|--------|-------|----------------|
| **Enemigo Mortal** | -100 a -80 | Ataca a vista, no negocia |
| **Enemigo** | -79 a -50 | Hostil, puede atacar |
| **Hostil** | -49 a -20 | Desconfiado, precios altos, información limitada |
| **Neutral** | -19 a +19 | Comportamiento base, sin modificadores |
| **Amistoso** | +20 a +49 | Descuentos, información extra, misiones especiales |
| **Aliado** | +50 a +79 | Acceso a servicios exclusivos, defiende al jugador |
| **Aliado Leal** | +80 a +100 | Sacrificaría recursos por el jugador, secreto total |

### 3. Opiniones (Sub-sistema)

Además de la reputación general, cada NPC tiene opiniones específicas:

```json
{
  "opiniones": {
    "confianza": {
      "valor": 0-100,
      "descripcion": "¿Cree el NPC que el jugador cumplirá su palabra?"
    },
    "respeto": {
      "valor": 0-100,
      "descripcion": "¿Admira el NPC las capacidades del jugador?"
    },
    "miedo": {
      "valor": 0-100,
      "descripcion": "¿Teme el NPC al jugador?"
    },
    "deuda": {
      "valor": 0-100,
      "descripcion": "¿Siente el NPC que debe algo al jugador?"
    },
    "romance": {
      "valor": 0-100,
      "descripcion": "Interés romántico (solo NPCs elegibles)"
    }
  }
}
```

---

## Red de Relaciones entre NPCs

### Estructura de la Red

Los NPCs no existen en aislamiento. Cada uno tiene relaciones con otros NPCs:

```json
{
  "npc_id": "npc_001",
  "nombre": "Haldor el Herrero",
  "relaciones_npcs": {
    "npc_002": {
      "nombre": "Mira la Tabernera",
      "tipo": "familia",
      "subtipo": "hermana",
      "afecto": 85,
      "historia": "Hermanos que se apoyan mutuamente"
    },
    "npc_003": {
      "nombre": "Guardia Theron",
      "tipo": "amistad",
      "subtipo": "cliente_regular",
      "afecto": 40,
      "historia": "Cliente frecuente de la herrería"
    },
    "npc_004": {
      "nombre": "Bandido Kael",
      "tipo": "rivalidad",
      "subtipo": "enemigo_personal",
      "afecto": -70,
      "historia": "Kael robó a Haldor hace 2 años"
    }
  }
}
```

### Tipos de Relación entre NPCs

| Tipo | Subtipos | Efecto en Jugador |
|------|----------|-------------------|
| **Familia** | Padre, Madre, Hijo, Hermano, Esposo/a, Primo | Ayudar a uno afecta al otro positivamente |
| **Amistad** | Mejor amigo, Amigo, Conocido, Compañero | Rumores se propagan, opiniones moderadas |
| **Rivalidad** | Enemigo personal, Competidor, Ex-amigo | Ayudar a uno afecta al otro negativamente |
| **Romance** | Esposo/a, Amante, Ex-pareja, Interés | Muy sensible a acciones del jugador |
| **Profesional** | Empleador, Empleado, Socio, Cliente | Afecta economía y servicios |
| **Política** | Aliado, Enemigo, Subordinado, Líder | Afecta facciones y misiones |

---

## Propagación de Reputación

### Reglas de Propagación

1. **Propagación por Proximidad**: Los NPCs cercanos (misma zona) se enteran de eventos más rápido.
2. **Propagación por Rutas**: Los viajeros y comerciantes llevan rumores entre zonas.
3. **Propagación por Relación**: Ayudar a un NPC mejora tu reputación con sus aliados y empeora con sus enemigos.

### Fórmula de Propagación

```python
def propagar_reputacion(accion, npc_afectado, npc_receptor):
    # Distancia social (qué tan cercanos son los NPCs)
    distancia_social = calcular_distancia_social(npc_afectado, npc_receptor)
    
    # Factor de propagación (qué tan "chismoso" es el receptor)
    factor_chisme = npc_receptor.personalidad.chisme  # 0.0 - 1.0
    
    # Tiempo desde el evento
    factor_tiempo = 1.0 / (1 + dias_transcurridos * 0.1)
    
    # Cálculo final
    cambio = accion.impacto_base * distancia_social * factor_chisme * factor_tiempo
    
    return cambio
```

### Ejemplo de Propagación

```
Jugador ayuda a Haldor el Herrero (+10 reputación con Haldor)

→ Mira (hermana de Haldor): +5 reputación (50% por familia)
→ Guardia Theron (cliente): +2 reputación (20% por amistad)
→ Bandido Kael (enemigo de Haldor): -3 reputación (30% negativo por rivalidad)
```

---

## Memoria de NPCs

### Estructura de Memoria

```json
{
  "npc_id": "npc_001",
  "memoria": [
    {
      "id": "mem_001",
      "tipo": "evento",
      "categoria": "ayuda",
      "descripcion": "El jugador me ayudó a reparar la puerta de la herrería",
      "fecha": 12345678,
      "ubicacion": "herreria_pueblo",
      "impacto_emocional": 0.7,
      "etiquetas": ["ayuda", "trabajo", "positivo"]
    },
    {
      "id": "mem_002",
      "tipo": "rumor",
      "categoria": "informacion",
      "descripcion": "Escuché que el jugador mató a un dragón",
      "fecha": 12345700,
      "fuente": "npc_002",
      "veracidad": 0.8,
      "etiquetas": ["combate", "dragon", "leyenda"]
    }
  ]
}
```

### Tipos de Memoria

| Tipo | Persistencia | Ejemplo |
|------|--------------|---------|
| **Evento Directo** | Permanente | "El jugador me atacó" |
| **Rumor** | Se degrada con tiempo | "Escuché que el jugador es un héroe" |
| **Observación** | Permanente | "Vi al jugador entrar en la cueva" |
| **Trato Comercial** | Se acumula | "Ha comprado 15 espadas" |
| **Promesa** | Hasta cumplir/romper | "Prometió traerme hierro" |

---

## Sistema de Facciones

### Estructura de Facción

```json
{
  "faccion_id": "fac_001",
  "nombre": "Gremio de Comerciantes",
  "descripcion": "Red de comerciantes que controlan el comercio regional",
  "lider": "npc_010",
  "miembros": ["npc_001", "npc_005", "npc_008"],
  "relaciones_facciones": {
    "fac_002": {"nombre": "Bandidos del Camino", "estado": "enemigo", "valor": -60},
    "fac_003": {"nombre": "Guardia Real", "estado": "aliado", "valor": 30}
  },
  "recursos": {
    "oro": 5000,
    "influencia": 70,
    "territorios": ["pueblo_central", "camino_este"]
  },
  "misiones_disponibles": ["mision_001", "mision_005"]
}
```

### Reputación con Facciones

```json
{
  "jugador_id": "player_001",
  "reputacion_facciones": {
    "fac_001": {
      "valor": 25,
      "estado": "amistoso",
      "contribuciones": [
        {"mision": "mision_001", "valor": 15},
        {"donacion": 100_oro", "valor": 10}
      ]
    }
  }
}
```

---

## Eventos de Relación

### Acciones que Afectan Reputación

| Acción | Impacto Base | NPCs Afectados |
|--------|--------------|----------------|
| Ayudar en combate | +15 a +30 | NPC ayudado + aliados |
| Comerciar | +1 a +5 | Solo el vendedor |
| Regalar | +5 a +20 | Solo el receptor |
| Matar NPC aliado | -50 a -100 | Familia/amigos del muerto |
| Robar (detectado) | -20 a -40 | Víctima + testigos |
| Cumplir promesa | +10 a +25 | Solo el interesado |
| Romper promesa | -15 a -30 | Solo el interesado |
| Matar enemigo de NPC | +10 a +30 | NPC + aliados del NPC |
| Insultar | -5 a -15 | Solo el receptor |
| Elogiar | +2 a +8 | Solo el receptor |

### Modificadores Contextuales

```python
def calcular_impacto_real(accion, npc, contexto):
    base = accion.impacto_base
    
    # Modificador por personalidad del NPC
    if npc.personalidad == "rencoroso" and accion.tipo == "negativa":
        base *= 1.5  # Lo recuerda más tiempo
    elif npc.personalidad == "perdonativo" and accion.tipo == "negativa":
        base *= 0.7  # Lo olvida más rápido
    
    # Modificador por estado actual
    if npc.estado_emocional == "enfadado":
        base *= 1.3 if accion.tipo == "negativa" else 0.7
    
    # Modificador por relación previa
    if npc.reputacion.valor > 50:  # Aliado
        base *= 1.2 if accion.tipo == "negativa" else 1.0  # Traición duele más
    
    return int(base)
```

---

## Sistema de Romance

### Requisitos para Romance

1. **Compatibilidad**: El NPC debe ser elegible para romance (orientación, estado civil).
2. **Reputación mínima**: +30 (Amistoso) para iniciar.
3. **Interacciones previas**: Mínimo 5 conversaciones significativas.
4. **Opinión de romance**: Debe superar 50.

### Estados de Romance

| Estado | Requisitos | Efectos |
|--------|------------|---------|
| **Desconocido** | Romance < 10 | Sin opciones románticas |
| **Interés** | Romance 10-30 | Opciones de coqueteo |
| **Atracción** | Romance 30-50 | Misiones románticas disponibles |
| **Enamorado** | Romance 50-80 | Puede iniciar relación formal |
| **Pareja** | Romance 80+ + evento | Beneficios de pareja, eventos especiales |
| **Casado** | Evento de boda | Máxima integración social |

### Eventos Románticos

```json
{
  "evento_romantico": {
    "id": "rom_001",
    "nombre": "Cena bajo las estrellas",
    "requisitos": {
      "romance_min": 30,
      "reputacion_min": 40,
      "ubicacion": ["zona_segura", "exterior", "noche"]
    },
    "efectos": {
      "romance": 15,
      "confianza": 10,
      "memoria": "Cena romántica con el jugador"
    }
  }
}
```

---

## Diálogos Dinámicos

### Modificadores de Diálogo

El sistema de relaciones afecta los diálogos disponibles:

```json
{
  "dialogo_base": {
    "id": "dlg_001",
    "npc": "npc_001",
    "saludo_base": "Hola, viajero.",
    "saludo_modificado": {
      "enemigo": "¿Qué quieres? No tengo nada para ti.",
      "hostil": "Mira, no busques problemas.",
      "neutral": "Hola, viajero.",
      "amistoso": "¡Amigo! Qué gusto verte.",
      "aliado": "Hermano, siempre es bueno verte.",
      "enemigo_mortal": "¡Tú! ¡Guardias!"
    }
  }
}
```

### Árbol de Diálogo Condicional

```json
{
  "opcion_dialogo": {
    "id": "opt_001",
    "texto": "¿Tienes trabajo para mí?",
    "requisitos": {
      "reputacion_min": 20,
      "NO_estado": ["enemigo", "enemigo_mortal"]
    },
    "respuesta": {
      "exito": "Sí, tengo algo que podría interesarte...",
      "fallo": "No confío lo suficiente en ti para eso."
    }
  }
}
```

---

## Implementación Técnica

### Estructura de Archivos

```
backend/src/systems/
├── relaciones/
│   ├── __init__.py
│   ├── gestor_relaciones.py    # Clase principal
│   ├── reputacion.py           # Cálculos de reputación
│   ├── propagacion.py          # Sistema de propagación
│   ├── memoria_npc.py          # Gestión de memoria
│   └── romance.py              # Sistema de romance
├── data/
│   ├── npcs.json               # Datos de NPCs
│   ├── facciones.json          # Datos de facciones
│   └── eventos_relacion.json   # Eventos predefinidos
```

### Clase Principal

```python
class GestorRelaciones:
    def __init__(self, save_manager):
        self.save = save_manager
        self.npcs = cargar_npcs()
        self.facciones = cargar_facciones()
    
    def modificar_reputacion(self, npc_id, cambio, causa):
        """Modifica la reputación con un NPC y propaga el cambio."""
        pass
    
    def propagar_evento(self, evento, npc_origen):
        """Propaga un evento a NPCs relacionados."""
        pass
    
    def obtener_estado_relacion(self, npc_id):
        """Devuelve el estado actual de la relación."""
        pass
    
    def verificar_requisitos(self, npc_id, requisitos):
        """Verifica si se cumplen requisitos de relación."""
        pass
    
    def obtener_dialogo_modificado(self, npc_id, dialogo_base):
        """Modifica un diálogo según la relación actual."""
        pass
    
    def procesar_memoria(self, npc_id, evento):
        """Añade un evento a la memoria del NPC."""
        pass
```

---

## Preguntas para Definir Detalles

### Preguntas sobre Propagación

1. **Velocidad de propagación**: ¿Cuántos días reales debería tardar un rumor en viajar de un pueblo a otro?
   > [La misma cantidad de días que tarda el jugador en viajar de un pueblo a otro, osea que si el jugador tarda 2 días en viajar de un pueblo a otro, el rumor tardará 2 días en viajar de un pueblo a otro, aunque dependerá tambien de factores que afecten el mundo. Por ejemplo si hay una lluvia que provoca tardanzas en los viajes para el jugador, se da por hecho que para otros npc tambien. Puede tambien afectar otras cosas, como que alguien tenag un caballo y pueda ir mas rapido.]

2. **Degradación de rumores**: ¿Los rumores deberían perder veracidad con el tiempo y la distancia?
   > [Si, podria funcionar, pero debemos asegurarnos de que tampoco sea tanta perdida ni tan rapido.]

3. **Fuentes de rumor**: ¿Todos los NPCs pueden propagar rumores o solo ciertos tipos (viajeros, comerciantes)?
   > [Todos los NPCs deberian poder propagar rumores, pero no todos deberian tener la misma capacidad para hacerlo. Por ejemplo, un viajero deberia tener mas capacidad para propagar rumores que un NPC que vive en un pueblo y no sale de el.]

### Preguntas sobre Romance

4. **Múltiples romances**: ¿Puede el jugador tener múltiples relaciones románticas simultáneas?
   > [Si, el jugador puede tener múltiples relaciones románticas simultáneas, pero no puede tener múltiples relaciones románticas simultáneas con el mismo NPC.]

5. **Celos de NPCs**: ¿Los NPCs pueden ponerse celosos si el jugador tiene relaciones con otros?
   > [Si, los NPCs pueden ponerse celosos si el jugador tiene relaciones con otros, pero solo si el NPC tiene una relación romántica con el jugador y descubre al jugador. Por ejemplo, si el jugador tiene una relación romántica con el NPC y descubre al jugador teniendo una relación romántica con otro NPC, el NPC se pondrá celoso y su reputación con el jugador disminuirá.]

### Preguntas sobre Facciones

6. **Traición de facción**: ¿Qué pasa si el jugador traiciona una facción? ¿Hay redención posible?
   > [Si el jugador traiciona una facción, su reputación con la facción disminuirá y podrá ser perseguido por la facción. La redención es posible, pero será difícil y requerirá tiempo y esfuerzo.]

7. **Facciones opuestas**: ¿Puede el jugador estar en dos facciones enemigas simultáneamente?
   > [Si, pero de ser descubierto, el jugador perderá reputación con ambas facciones. Además, tiene que ser algo logico. Supongamos que nuestro personaje es un don nadie y se une a la Faccion A, pero viaja y se une a la Faccion B y ellos son enemigos, como andie nos conoce, dudablemente tengas problemas hasta que se involucre alguna situacion que nos afecte en general. Por ejemplo, que nos encuentre quien nos reclutó en alguno de los dos lados, etc. Esto habria que trabajarlo arduamente.]

---

### Preguntas Adicionales - Memoria y Perdón

8. **Olvido de eventos**: ¿Los NPCs pueden olvidar eventos si pasa mucho tiempo?
   > [Solo eventos menores. Los eventos importantes (asesinatos, traiciones, ayudas significativas) se recuerdan permanentemente.]

9. **Perdón de acciones negativas**: ¿Los NPCs pueden perdonar si el jugador hace suficientes acciones positivas?
   > [Sí, claramente. Con suficientes acciones positivas y tiempo, un NPC puede perdonar acciones negativas pasadas.]

### Preguntas Adicionales - Comercio

10. **Límite de descuentos**: ¿Los descuentos por reputación tienen un límite?
   > [Sí, máximo 50% de descuento para aliados leales. Los precios también pueden aumentar hasta 200% para enemigos.]

11. **Negativa de venta**: ¿Un NPC puede negarse a vender si la reputación es muy baja?
   > [Sí, un NPC puede negarse a comerciar si la reputación es de "Hostil" o peor (-20 o menos).]

### Preguntas Adicionales - Combate

12. **NPCs aliados en combate**: ¿Un NPC aliado puede unirse al jugador en combate?
   > [Solo si está en la zona cercana. Un NPC que pase por casualidad puede ayudar, pero no aparecerá de la nada.]

13. **Clemencia en combate**: ¿Un NPC enemigo puede pedir clemencia?
   > [Sí, dependiendo de la personalidad del NPC. Un cobarde puede pedir clemencia, un fanático puede preferir morir.]

### Preguntas Adicionales - Muerte de NPCs

14. **Herencia de relaciones**: ¿Si un NPC importante muere, quién hereda sus relaciones?
   > [Las relaciones no se heredan automáticamente. Cada persona es consecuente con sus propias relaciones. Sin embargo, si el hijo sabe que X mató a su padre, puede cambiar su relación hacia esa persona.]

15. **Venganza**: ¿Los familiares de un NPC asesinado pueden contratar asesinos?
   > [Sí, siempre y cuando sea lógico. Un familiar con recursos y motivación puede buscar venganza.]

---

## Ejemplos de Uso

### Ejemplo 1: Ayudar a un NPC

```python
# El jugador ayuda a Haldor a repeler unos bandidos
gestor.modificar_reputacion(
    npc_id="npc_001",
    cambio=25,
    causa="ayuda_combate_bandidos"
)

# El sistema propaga automáticamente:
# - Mira (hermana): +12 reputación
# - Guardia Theron (cliente): +5 reputación
# - Bandido Kael (enemigo): -8 reputación
```

### Ejemplo 2: Matar un NPC

```python
# El jugador mata a un comerciante inocente
gestor.procesar_evento(
    tipo="asesinato",
    victima="npc_005",
    testigos=["npc_002", "npc_003"]
)

# Efectos:
# - Reputación con familia: -80 (enemigo mortal)
# - Reputación con testigos: -40 (hostil)
# - Propagación a pueblo: -20 (hostil) en 3 días
# - Posible bounty del jugador
```

### Ejemplo 3: Iniciar Romance

```python
# Verificar si se puede iniciar romance
if gestor.verificar_requisitos("npc_002", {
    "reputacion_min": 30,
    "interacciones_min": 5,
    "romance_min": 10
}):
    # Mostrar opción de coqueteo
    dialogo = gestor.obtener_opcion_romance("npc_002", "coqueteo_inicial")
```

---

## Integración con Otros Sistemas

### Dependencias

| Sistema | Uso |
|---------|-----|
| **SISTEMA_NPCS** | Datos base de NPCs, personalidad, ubicación |
| **SISTEMA_MAPA** | Propagación por proximidad y rutas |
| **SISTEMA_TIEMPO** | Degradación de memoria, eventos retardados |
| **SISTEMA_HISTORIA** | Registro de eventos para memoria |
| **SISTEMA_MISIONES** | Recompensas de reputación, requisitos de relación |

### Eventos que Escucha

- `combate_terminado`: Actualizar reputación con NPCs involucrados
- `npc_interactuado`: Registrar en memoria
- `item_comprado`: Mejorar relación con vendedor
- `mision_completada`: Aplicar recompensas de reputación
- `npc_muerto`: Propagar consecuencias

### Eventos que Emite

- `reputacion_cambiada`: Para actualizar UI
- `relacion_estado_cambiado`: Para desbloquear/bloquear contenido
- `rumor_propagado`: Para sistema de historia
- `romance_iniciado`: Para eventos especiales

---

## Checklist de Implementación

### Fase 1: Estructura Base
- [ ] Crear `npcs.json` con estructura de relaciones
- [ ] Crear `facciones.json` con datos de facciones
- [ ] Implementar clase `GestorRelaciones`
- [ ] Implementar cálculo de estados de relación

### Fase 2: Memoria y Propagación
- [ ] Implementar sistema de memoria de NPCs
- [ ] Implementar propagación por relación
- [ ] Implementar propagación por proximidad
- [ ] Implementar degradación de rumores

### Fase 3: Integración
- [ ] Conectar con sistema de NPCs
- [ ] Conectar con sistema de mapa
- [ ] Conectar con sistema de misiones
- [ ] Implementar modificadores de diálogo

### Fase 4: Romance (Opcional)
- [ ] Implementar requisitos de romance
- [ ] Implementar eventos románticos
- [ ] Implementar sistema de pareja

---

## Notas Adicionales

- El sistema debe ser persistente: todo se guarda en el save
- Los NPCs deben sentirse "vivos" con sus opiniones cambiantes
- La propagación no debe ser instantánea para mantener inmersión
- El romance es un sistema opcional que puede expandirse después

---

*Sistema documentado - Versión 1.0*
*Dependencias: SISTEMA_NPCS, SISTEMA_MAPA, SISTEMA_TIEMPO*