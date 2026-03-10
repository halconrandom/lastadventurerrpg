# Sistema de Combate - Last Adventurer

> **Estado:** Actualizado - Consistente con sistemas actuales
> **Última actualización:** 2026-03-09
> **Dependencias:** SISTEMA_STATS.md, CATALOGO_ENEMIGOS_COMPLETO.md, SISTEMA_INVENTARIO.md

## Concepto

Combate por turnos con **grupo completo** (múltiples aliados y enemigos). El orden de turnos se determina por velocidad. El jugador puede atacar, usar habilidades, usar items, bloquear, evadir activamente, o huir.

---

## Flujo de Combate

```
1. Inicio del combate
   - Generar participantes (jugador + aliados vs enemigos)
   - Calcular orden de turnos por velocidad
   - Determinar turnos extra por diferencia de velocidad

2. Turno de cada participante (en orden de velocidad)
   - Jugador/Aliado: Elige acción
   - Enemigo: IA elige acción
   - Ejecutar acción
   - Verificar efectos (estados alterados, muerte)

3. Fin de turno
   - Resetear bloqueos
   - Aplicar efectos de tiempo (veneno, sangrado, etc.)
   - Regenerar stamina

4. Verificar fin de combate
   - Victoria: Todos los enemigos muertos
   - Derrota: Todos los aliados muertos
   - Huida: Jugador escapa con éxito

5. Repetir hasta fin del combate
```

---

## Acciones del Jugador

### Atacar
- Usa el arma equipada
- Cálculo: `Daño = (ATK Personaje + Daño Arma) × Multiplicador Habilidad`
- Costo: 10 Stamina
- Da experiencia a la habilidad del arma

### Usar Habilidad (Perk Activo)
- Consume Mana o Stamina según el perk
- Efecto variable según el perk
- Da experiencia a la habilidad relacionada

### Usar Item
- Consume una poción del inventario
- Costo: 5 Stamina
- **Consume turno** (según decisión del usuario)

### Bloquear
- Reduce daño recibido en 50%
- Da experiencia a Defensa
- Costo: 5 Stamina
- **Chance de contraataque:** 10% base + (Nivel Defensa × 1%)
- Si contraataca: Ataque básico automático sin costo adicional

### Evadir Activamente
- Evade 100% del daño del próximo ataque
- Costo: 5 Stamina
- No ataca en este turno

### Huir
- Probabilidad basada en nivel del enemigo vs jugador
- Fórmula: `Probabilidad = 50% + (Nivel Jugador - Nivel Enemigo) × 5%`
- Rango: 10% - 90%
- Si falla, el enemigo ataca con ventaja

---

## Sistema de Stamina

La stamina es el **recurso de acción por turno**. Se regenera completamente al inicio de cada turno.

### Costos de Acción

| Acción | Costo de Stamina | Efecto |
|--------|-----------------|--------|
| Ataque básico | 10 puntos | Daño normal |
| Usar habilidad | Variable (10-30 puntos) | Efecto según habilidad |
| Usar item | 5 puntos | Cura HP/Mana |
| Bloquear | 5 puntos | Reduce daño 50% + chance contraataque |
| Evadir activamente | 5 puntos | Evade 100% del daño |

### Ejemplo de Turno

```
Stamina disponible: 20

Opción 1: Ataque básico (10) → Turno terminado
Opción 2: Tomar poción (5) + Bloquear (5) → Turno terminado
Opción 3: Usar habilidad fuerte (15) → Turno terminado
Opción 4: Ataque básico (10) + Bloquear (5) → Necesitas más stamina
```

### Perks que Afectan Stamina

- Reducen costo de acciones específicas
- Aumentan stamina máxima
- Permiten recuperar stamina parcial en combate

---

## Sistema de Turnos Extra por Velocidad

La velocidad determina no solo el orden de ataque, sino también **cuántas veces atacas por turno**.

### Cálculo de Turnos Extra

```
Diferencia = (Velocidad Atacante - Velocidad Objetivo) / Velocidad Objetivo × 100
Turnos Extra = floor(Diferencia / 50)
Ataques Totales = 1 + Turnos Extra
```

### Tabla de Turnos Extra

| Diferencia de Velocidad | Ataques por Turno |
|------------------------|-------------------|
| 0-49% superior | 1 ataque |
| 50-99% superior | 2 ataques |
| 100-149% superior | 3 ataques |
| 150-199% superior | 4 ataques |
| ... | +1 por cada 50% |

### Ejemplos

```
Tu velocidad: 100
Enemigo velocidad: 50
Diferencia: 100% superior → Atacas 3 veces (1 base + 2 extra)

Tu velocidad: 100
Enemigo velocidad: 60
Diferencia: 66% superior → Atacas 2 veces (1 base + 1 extra)
```

---

## Sistema de Evasión

### Evasión Pasiva
- Ocurre automáticamente si decides atacar
- Chance base: 10% + puntos de evasión
- Cap: 50%
- No consume recursos

### Evasión Activa
- Decides evadir conscientemente
- Siempre evade (100% éxito)
- Costo: 5 Stamina
- No atacas en este turno

### Bloqueo vs Evasión

| Tipo | Descripción | Efecto |
|------|-------------|--------|
| **Pasiva** | Ocurre automáticamente si decides atacar | Chance base de evadir (10% + puntos) |
| **Activa** | Decides evadir conscientemente | Siempre evade (100% éxito) |
| **Bloqueo** | Decides bloquear | Reduce daño + da exp a Defensa + chance contraataque |

### Contraataque tras Bloqueo

- Chance base: 10%
- Se calcula: `Contraataque Base + (Nivel Defensa × 1%)`
- Si activa: Realizas un ataque básico automático tras bloquear
- No consume stamina adicional

**Ejemplo:**
```
Nivel Defensa: 15
Chance de contraataque: 10% + 15% = 25%

Enemigo ataca con 40 de daño
Bloqueas → Recibes 20 de daño (50% reducido)
Sistema calcula contraataque: 25% chance
Si activa → Atacas automáticamente al enemigo
```

---

## Cálculo de Daño

### Fórmula de Daño Físico
```
Daño Base = ATK Personaje + Daño Arma
Multiplicador = 1 + (Nivel Habilidad × 0.05)
Daño Final = Daño Base × Multiplicador
```

### Fórmula de Crítico
```
Probabilidad Crítico = Crítico Base + Puntos Crítico
Daño Crítico = Daño Final × 1.5
```

### Fórmula de Reducción de Daño
```
Reducción = DEF % + (Nivel Defensa × 1%)
Reducción Máxima = 80%
Daño Recibido = Daño Enemigo × (1 - Reducción)
```

### Fórmula de Bloqueo
```
Daño Bloqueado = Daño Recibido × 0.5
Experiencia Defensa = Nivel Enemigo × 2
```

---

## Tipos de Daño

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Físico | Daño normal | Espada, Arco, Dagas |
| Mágico | Daño de hechizos | Bola de Fuego |
| Fuego | Daño elemental, puede quemar | Espada del Infierno |
| Hielo | Daño elemental, puede congelar | Espadón de Escarcha |
| Rayo | Daño elemental, puede aturdir | Bastón de Tormenta |
| Veneno | Daño por tiempo | Daga Ensangrentada |
| Sangrado | Daño por tiempo | Hacha de Carnicero |
| Oscuridad | Daño mágico oscuro | Orbe de Sombra |

---

## Estados Alterados

Los estados alterados son efectos que persisten durante varios turnos.

### Estados de Daño por Tiempo

| Estado | Efecto | Duración | Cómo se cura |
|--------|--------|----------|--------------|
| **Quemadura** | 5-10 daño/turno | 3 turnos | Agua, Poción de Curación |
| **Veneno** | 5-15 daño/turno | 3-5 turnos | Antídoto, Poción de Curación |
| **Sangrado** | 3-8 daño/turno | 2-4 turnos | Vendas, Poción de Curación |
| **Congelación** | -20% velocidad, 50% chance de saltar turno | 2 turnos | Fuego, Poción de Calor |
| **Enfermedad** | -20% stats, -50% curación | 4 turnos | Poción de Curación, Descanso largo |

### Estados de Control

| Estado | Efecto | Duración | Cómo se cura |
|--------|--------|----------|--------------|
| **Aturdir** | No puede actuar | 1 turno | Pasa automáticamente |
| **Inmovilizar** | No puede moverse, -50% evasión | 1-2 turnos | Pasa automáticamente |
| **Ceguera** | -50% precisión, -30% crítico | 2-3 turnos | Poción de Visión |
| **Miedo** | -20% ATK, 20% chance de huir | 2 turnos | Pasa automáticamente |
| **Confusión** | 50% chance de atacar aliado | 2 turnos | Pasa automáticamente |
| **Silencio** | No puede usar habilidades mágicas | 2 turnos | Pasa automáticamente |

### Estados de Buff

| Estado | Efecto | Duración | Fuente |
|--------|--------|----------|--------|
| **Furia** | +30% ATK, -20% DEF | 3 turnos | Habilidad, Item |
| **Escudo** | +50% DEF | 2 turnos | Habilidad, Item |
| **Velocidad** | +30% velocidad | 2 turnos | Habilidad, Item |
| **Invisibilidad** | 100% evasión | 1 turno | Habilidad, Item |
| **Regeneración** | +10 HP/turno | 3 turnos | Habilidad, Item |

---

## Combate en Grupo

El combate soporta **múltiples participantes** en ambos bandos.

### Estructura de Grupo

```
Bando del Jugador:
├── Jugador (siempre presente)
├── Aliado 1 (opcional)
├── Aliado 2 (opcional)
└── Aliado 3 (opcional)

Bando Enemigo:
├── Enemigo 1
├── Enemigo 2
├── Enemigo 3
└── Enemigo 4
```

### Orden de Turnos

1. Calcular velocidad de todos los participantes
2. Ordenar de mayor a menor velocidad
3. Cada participante actúa en su orden
4. Aplicar turnos extra por diferencia de velocidad

### IA de Enemigos

Los enemigos tienen comportamientos predefinidos según su tipo:

| Tipo de Enemigo | Comportamiento |
|----------------|----------------|
| **Agresivo** | Ataca siempre, prioriza HP bajo |
| **Defensivo** | Bloquea frecuentemente, protege aliados |
| **Mágico** | Usa habilidades, mantiene distancia |
| **Sigiloso** | Ataca primero, huye si HP bajo |
| **Líder** | Ordena a aliados, invoca refuerzos |
| **Jefe** | Múltiples fases, habilidades especiales |

### Ejemplo de Combate en Grupo

```
Orden de turnos (por velocidad):
1. Águila Real (VEL: 28) - Enemigo
2. Asesino Sombra (VEL: 28) - Enemigo
3. Jugador (VEL: 20) - Aliado
4. Guerrero Caballero (VEL: 12) - Aliado
5. Oso Pardo (VEL: 8) - Enemigo

Turno 1:
- Águila Real ataca a Guerrero Caballero
- Asesino Sombra ataca a Jugador
- Jugador ataca a Águila Real
- Guerrero Caballero bloquea
- Oso Pardo ataca a Jugador

Fin de turno 1:
- Resetear bloqueos
- Aplicar efectos de tiempo
- Regenerar stamina
```

---

## Recompensas

### Experiencia
- Cada enemigo otorga experiencia al ser derrotado
- La experiencia se divide entre los participantes vivos del bando ganador
- Fórmula: `Exp por participante = Exp Total / Participantes Vivos`

### Oro
- Cada enemigo otorga oro al ser derrotado
- El oro se divide entre los participantes vivos del bando ganador
- Fórmula: `Oro por participante = Oro Total / Participantes Vivos`

### Drops
- Cada enemigo tiene una lista de drops con probabilidades
- Los drops se asignan aleatoriamente a los participantes vivos
- Probabilidad de drop: `Probabilidad Base × (1 + Nivel Jugador × 0.01)`

### Tabla de Drops por Rareza

| Rareza Drop | Probabilidad | Ejemplo |
|-------------|--------------|---------|
| Común | 30-50% | Hueso, Piel |
| Poco Común | 15-25% | Colmillo, Garra |
| Raro | 8-15% | Esencia, Núcleo |
| Muy Raro | 3-8% | Corazón, Fragmento |
| Legendario | 1-3% | Item único de jefe |

---

## Estructura JSON

### Estado de Combate
```json
{
  "estado": "turno_jugador",
  "turno": 5,
  "orden_turnos": ["jugador_1", "enemigo_1", "enemigo_2"],
  "jugadores": {
    "jugador_1": {
      "id": "jugador_1",
      "nombre": "Aventurero",
      "tipo": "jugador",
      "hp": 85,
      "hp_max": 100,
      "mana": 30,
      "mana_max": 50,
      "stamina": 10,
      "stamina_max": 10,
      "ataque": 20,
      "defensa": 15,
      "velocidad": 20,
      "critico": 10,
      "evasion": 15,
      "nivel": 5,
      "esta_vivo": true,
      "esta_bloqueando": false,
      "habilidades": []
    }
  },
  "enemigos": {
    "enemigo_1": {
      "id": "enemigo_1",
      "nombre": "Lobo Salvaje",
      "tipo": "enemigo",
      "hp": 20,
      "hp_max": 30,
      "mana": 0,
      "mana_max": 0,
      "stamina": 10,
      "stamina_max": 10,
      "ataque": 8,
      "defensa": 2,
      "velocidad": 15,
      "critico": 8,
      "evasion": 10,
      "nivel": 3,
      "esta_vivo": true,
      "esta_bloqueando": false,
      "habilidades": [
        {
          "nombre": "Mordisco",
          "multiplicador": 1.2,
          "costo": 15,
          "tipo": "fisico"
        }
      ],
      "experiencia": 25,
      "oro": 8,
      "drops": [
        {
          "item_id": "colmillo_lobo",
          "probabilidad": 0.3,
          "cantidad_min": 1,
          "cantidad_max": 1
        }
      ]
    }
  },
  "log": [
    {
      "turno": 1,
      "actor_id": "jugador_1",
      "actor_nombre": "Aventurero",
      "accion": "atacar",
      "objetivo_id": "enemigo_1",
      "objetivo_nombre": "Lobo Salvaje",
      "daño": 15,
      "es_critico": false,
      "es_evasion": false,
      "mensaje": "Aventurero ataca a Lobo Salvaje causando 15 de daño."
    }
  ]
}
```

---

## Preguntas Resueltas

### Alta Prioridad - RESUELTAS

1. **¿Usar item consume turno?** ✅ Sí, consume turno (5 stamina)
2. **¿Orden de turnos?** ✅ Por velocidad (stat existente)
3. **¿Combate en grupo?** ✅ Grupo completo (múltiples aliados y enemigos)
4. **¿Críticos?** ✅ Basado en stat crítico (x1.5 daño)
5. **¿Evasión?** ✅ Probabilidad de esquivar ataque completo (basado en stat evasion)
6. **¿Qué pasa al huir?** ✅ Probabilidad basada en nivel (jugador vs enemigo)
7. **¿Recompensas al ganar?** ✅ Experiencia + oro + drops (depende del tipo de monstruo)

### Media Prioridad - RESUELTAS

8. **¿Sistema de Stamina?** ✅ Implementado (10 base, acciones por turno)
9. **¿Turnos extra por velocidad?** ✅ Implementado (cada 50% diferencia = +1 ataque)
10. **¿Contraataque tras bloqueo?** ✅ Implementado (10% base + nivel defensa)
11. **¿Evasión activa vs pasiva?** ✅ Implementado (activa = 100%, pasiva = chance)
12. **¿Estados alterados?** ✅ Documentados (quemadura, veneno, sangrado, etc.)
13. **¿IA de enemigos?** ✅ Documentada (agresivo, defensivo, mágico, etc.)

### Pendientes - RESUELTAS

14. **¿Sistema de combos?** ¿Encadenar ataques para efectos especiales?
    > ❌ NO - No se implementará sistema de combos

15. **¿Sistema de cover?** ¿Proteger a aliados recibiendo daño por ellos?
    > ❌ NO - No se implementará sistema de cover

16. **¿Sistema de interrupción?** ¿Interrumpir habilidades enemigas?
    > ❌ NO - No se implementará sistema de interrupción

---

## Implementación Técnica

### Archivos del Sistema

```
backend/src/systems/
├── combate.py              # Lógica del combate (CombateManager)
└── stats.py                # Cálculo de stats

backend/src/api/
├── combate.py              # Endpoints de combate
└── ...

backend/src/models/
├── personaje.py            # Modelo de personaje
└── enemigo.py              # Modelo de enemigo

frontend/src/components/
└── juego/combat/
    ├── CombatHUD.tsx       # UI de combate
    └── ...
```

### Endpoints API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/combate/iniciar` | POST | Inicia un nuevo combate |
| `/api/combate/accion` | POST | Ejecuta una acción |
| `/api/combate/estado` | GET | Obtiene estado actual |
| `/api/combate/recompensas` | GET | Obtiene recompensas tras victoria |

---

## Checklist de Implementación

### Fase 1: Estructura Base
- [x] Actualizar modelo de datos de combate
- [x] Implementar sistema de turnos por velocidad
- [x] Implementar sistema de grupo completo
- [x] Implementar sistema de stamina

### Fase 2: Acciones
- [x] Implementar atacar
- [x] Implementar usar habilidad
- [x] Implementar usar item
- [x] Implementar bloquear
- [x] Implementar evadir activamente
- [x] Implementar huir

### Fase 3: Mecánicas Avanzadas
- [x] Implementar turnos extra por velocidad
- [x] Implementar contraataque tras bloqueo
- [x] Implementar evasión pasiva vs activa
- [ ] Implementar estados alterados
- [ ] Implementar IA de enemigos

### Fase 4: Integración
- [x] Conectar con backend
- [x] Persistir cambios
- [x] Sincronizar con inventario
- [ ] Sincronizar con sistema de experiencia

---

*Sistema documentado - Versión 2.0*
*Dependencias: SISTEMA_STATS.md, CATALOGO_ENEMIGOS_COMPLETO.md, SISTEMA_INVENTARIO.md*
3. **¿Combate en grupo?** ✅ Grupo completo (múltiples aliados y enemigos)
4. **¿Críticos?** ✅ Basado en stat crítico (x1.5 daño)
5. **¿Evasión?