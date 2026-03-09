# World Lore - Last Adventurer

> **Estado:** En desarrollo - Decisiones parciales tomadas
> **Última actualización:** 2026-03-09
> **Fuentes:** `STORYTELLER_SYSTEM.md`, `SISTEMA_HISTORIA.md`, `SISTEMA_EXPLORACION.md`, `ROADMAP.md`

---

## Resumen de Decisiones Tomadas

| Aspecto | Decisión | Fuente |
|---------|----------|--------|
| **Nombre del mundo** | Aleatorio por partida (LLM genera opciones) | STORYTELLER_SYSTEM.md |
| **Cosmología** | Generada por LLM, única por mundo | STORYTELLER_SYSTEM.md |
| **Facciones** | Generadas por LLM, únicas por mundo | STORYTELLER_SYSTEM.md |
| **Razas** | Clásicas de fantasía (Humanos, Elfos, Enanos, etc.) | STORYTELLER_SYSTEM.md |
| **Conflicto central** | Mundo neutral - no hay bien/mal absolutos | STORYTELLER_SYSTEM.md |
| **El jugador** | Primero en 1000 años con el Don de Exploración | STORYTELLER_SYSTEM.md |
| **Geografía** | Sistema procedural (tiles X/Y, mundo infinito con chunks) | SISTEMA_MAPA.md |
| **Historia procedural** | 100 años de eventos generados al crear mundo | STORYTELLER_SYSTEM.md |
| **Tono** | D&D con toques oscuros y lore profundo | SISTEMA_HISTORIA.md |
| **Voz narrativa** | Omnisciente pero limitada en información | SISTEMA_HISTORIA.md |
| **LLM** | Llama 3.2 3B con fine-tuning (LoRA), VPS propia | SISTEMA_LLM.md |
| **Mapa** | Sistema dual (mundial + local), tiles de 1km, subtiles de 100m | SISTEMA_MAPA_DUAL.md |
| **Tiempo** | Día/noche, estaciones, avanza por acción | SISTEMA_TIEMPO.md |
| **Relaciones** | Sistema híbrido (numérico + estados), red de NPCs | SISTEMA_RELACIONES.md |
| **Combate** | Por turnos, por velocidad, grupo completo | SISTEMA_COMBATE.md |
| **Creación personaje** | Sin arquetipos al inicio, se definen por misiones | SISTEMA_CREACION_PERSONAJE.md |
| **Spawn** | Aleatorio en pueblo/ciudad seguro | SISTEMA_HISTORIA.md |
| **Fast travel** | No, exploración a pie obligatoria | SISTEMA_HISTORIA.md |
| **Persistencia** | Todo se guarda permanentemente | SISTEMA_HISTORIA.md |
| **Memoria NPCs** | Total, recuerdan todo | SISTEMA_HISTORIA.md |
| **Mundo dinámico** | Sí, cambia sin intervención del jugador | SISTEMA_HISTORIA.md |
| **Consecuencias** | Retardadas pero consistentes, irreversibles | SISTEMA_HISTORIA.md |

---

## 1. El Don de Exploración

**Concepto confirmado:**
- Las entidades cosmológicas dotaron a ciertos humanos con la capacidad de exploración
- Este don permite descubrir cosas donde otros no las ven
- Las guerras y la codicia humana provocaron que el don se debilitara
- Han pasado más de 1000 años desde el nacimiento del último humano aventurero
- **El jugador es el primero en 1000 años en nacer con este don**

### Preguntas Pendientes

1. **¿Qué puede hacer exactamente el jugador con el Don?**
   - ¿Ver cosas ocultas que otros no ven?
   - ¿Encontrar secretos automáticamente?
   - ¿Acceder a áreas bloqueadas para otros?
   - ¿Interactuar con entidades cosmológicas?
   - ¿Combinación de todo lo anterior?

2. **¿El Don tiene niveles o se desarrolla?**
   - ¿Es estático desde el inicio?
   - ¿Puede mejorar con el tiempo?
   - ¿Hay habilidades específicas del Don?

3. **¿El Don tiene un costo?**
   - ¿Consume algo (stamina, mana)?
   - ¿Tiene límites de uso?
   - ¿Puede perderse o debilitarse?

4. **¿Las otras razas pueden tener el Don?**
   - ¿Solo humanos?
   - ¿Alguna raza puede tenerlo?
   - ¿Es exclusivo del jugador?

---

## 2. Razas

**Decisión:** Usar las **razas clásicas de fantasía**.

### Lista de Razas a Definir

| Raza | ¿Incluida? | ¿Jugable? | Notas |
|------|------------|-----------|-------|
| Humanos | ✅ Sí | ✅ Sí | Base del juego, pueden tener el Don |
| Elfos | ❓ Pendiente | ❓ | ¿Elfos Nocturnos? ¿Elfos clásicos? |
| Enanos | ❓ Pendiente | ❓ | ¿Enanos del Vacío? ¿Enanos clásicos? |
| Orcos | ❓ Pendiente | ❓ | ¿Hostiles? ¿Jugables? |
| Gnomos | ❓ Pendiente | ❓ | |
| Halflings | ❓ Pendiente | ❓ | |
| Otros | ❓ Pendiente | ❓ | ¿Dragones? ¿Demonios? ¿No-muertos? |

### Preguntas Pendientes

1. **¿Qué razas específicas incluimos?**
2. **¿Todas las razas son jugables?**
3. **¿Alguna raza puede tener el Don de Exploración?**
4. **¿Las razas tienen bonificación/stats diferentes?**
5. **¿Hay sub-razas?**

---

## 3. Sistema de Magia

**PENDIENTE DE DECISIÓN**

### Preguntas sobre Magia:

1. **¿La magia existe?**
   - Sí, es común
   - Sí, pero es rara
   - Sí, pero es peligrosa
   - No, es tecnología avanzada

2. **¿Cómo funciona la magia?**
   - **Vanciana:** Spells memorizados, slots
   - **Mana:** Recurso que se gasta
   - **Ritual:** Tiempo y componentes
   - **Pactos:** Poder de entidades

3. **¿Quién puede usar magia?**
   - ¿Cualquiera con entrenamiento?
   - ¿Solo los nacidos con el don?
   - ¿Solo mediante artefactos?
   - ¿Solo mediante pactos?

4. **¿El Don de Exploración es magia?**
   - ¿Es lo mismo que usar hechizos?
   - ¿Es un poder diferente?
   - ¿Pueden coexistir?

---

## 4. Tecnología y Sociedad

**PENDIENTE DE DECISIÓN**

### Preguntas sobre Tecnología:

1. **¿Qué nivel tecnológico tiene el mundo?**
   - **Primitivo:** Piedra, bronce
   - **Medieval:** Hierro, castillos
   - **Renacentista:** Pólvora, imprenta
   - **Steampunk:** Vapor, engranajes
   - **Magitech:** Magia + tecnología

2. **¿Cómo es la sociedad?**
   - **Feudal:** Reyes, nobles, campesinos
   - **Republicana:** Consejos, gremios
   - **Tribal:** Clanes, jefes
   - **Mixta:** Diferente según región

3. **¿Hay economía?**
   - ¿Monedas universales?
   - ¿Trueque?
   - ¿Sistema de reputación?

---

## 5. Criaturas y Monstruos

**PENDIENTE DE DECISIÓN**

### Preguntas sobre Criaturas:

1. **¿Qué tipo de criaturas existen?**
   - ¿Bestias naturales?
   - ¿Criaturas mágicas?
   - ¿Monstruos del vacío?
   - ¿Muertos vivientes?

2. **¿Los monstruos son siempre hostiles?**
   - ¿Se pueden domesticar?
   - ¿Se pueden negociar?
   - ¿Hay monstruos "buenos"?

3. **¿Hay jefes únicos?**
   - ¿Dragones antiguos?
   - ¿Demonios mayores?
   - ¿Criaturas legendarias?

---

## 6. Misterios Centrales

**PENDIENTE DE DECISIÓN**

### Preguntas sobre Misterios:

1. **¿Cuántos misterios principales quieres?**
   - 1 (Muy enfocado, todo gira alrededor)
   - 2-3 (Interconectados, pero distintos)
   - 4-5 (Complejo, múltiples líneas de historia)

2. **¿Los misterios tienen solución?**
   - ¿El jugador puede resolverlos?
   - ¿Son permanentes del mundo?
   - ¿Hay múltiples interpretaciones?

3. **¿Cómo se revelan los misterios?**
   - ¿Exploración de ruinas?
   - ¿NPCs y diálogos?
   - ¿Libros y documentos?
   - ¿Visiones y sueños?

4. **Misterios potenciales:**
   - ¿Qué son las entidades cosmológicas?
   - ¿Por qué se debilitó el Don?
   - ¿Puede recuperarse el Don para todos?
   - ¿Qué pasó en los últimos 1000 años?
   - ¿Hay otros con el Don ocultos?

---

## 7. Entidades Cosmológicas

**PENDIENTE DE DECISIÓN**

### Preguntas:

1. **¿Qué son las entidades cosmológicas?**
   - ¿Dioses que caminaban el mundo?
   - ¿Una civilización avanzada?
   - ¿Visitantes de otro plano?
   - ¿Fuerzas de la naturaleza personificadas?
   - ¿Algo más abstracto?

2. **¿Todavía existen?**
   - ¿Se fueron?
   - ¿Están dormidas?
   - ¿Observan desde lejos?
   - ¿Desaparecieron completamente?

3. **¿Tienen relación con el jugador?**
   - ¿El jugador es su "elegido"?
   - ¿El jugador es un accidente?
   - ¿Observan al jugador?
   - ¿Son indiferentes?

---

## 8. Duración y Progresión

**PENDIENTE DE DECISIÓN**

### Preguntas:

1. **¿Cuánto dura una partida "completa"?**
   - ¿5-10 horas?
   - ¿20-40 horas?
   - ¿Infinita (roguelike/sandbox)?

2. **¿Qué hace que el jugador vuelva?**
   - ¿Descubrir secretos?
   - ¿Progresar en poder?
   - ¿Ver las consecuencias de sus decisiones?
   - ¿Completar la historia?

3. **¿Hay un "final"?**
   - ¿El juego tiene fin?
   - ¿Se puede seguir jugando después?
   - ¿Hay múltiples finales?

---

## 9. Los 3 Pilares (Prioridad)

> **Define estos primero** - el resto de decisiones fluirán naturalmente.

### Pilar 1: Experiencia Core
**¿Qué hace el jugador minuto a minuto?**
- [ ] Combatir
- [ ] Explorar
- [ ] Hablar/Negociar
- [ ] Resolver puzzles
- [ ] Gestionar recursos
- [ ] Otro: ____________

### Pilar 2: Progresión
**¿Qué mantiene al jugador enganchado?**
- [ ] Descubrir secretos/historia
- [ ] Subir de nivel/poder
- [ ] Consecuencias de decisiones
- [ ] Coleccionar/Completar
- [ ] Superar desafíos
- [ ] Otro: ____________

### Pilar 3: Finalidad
**¿Cuál es el objetivo del juego?**
- [ ] Completar la historia principal
- [ ] Sobrevivir el mayor tiempo posible
- [ ] Descubrir todos los secretos
- [ ] Construir/Crear algo
- [ ] No hay objetivo fijo (sandbox)
- [ ] Otro: ____________

---

## 10. Próximos Pasos

### Orden sugerido para responder:

1. **Primero: Los 3 Pilares (Sección 9)** - Define la experiencia core, progresión y finalidad
2. **Segundo: El Don de Exploración (Sección 1)** - Qué hace exactamente
3. **Tercero: Razas (Sección 2)** - Cuáles y cómo funcionan
4. **Cuarto: Magia (Sección 3)** - Existe y cómo funciona
5. **Quinto: Tecnología (Sección 4)** - Nivel tecnológico del mundo
6. **Sexto: El resto de secciones** - Detalles específicos

### Una vez respondas, podemos:

1. Crear templates para generación procedural de nombres/cosmología/facciones
2. Definir la lista exacta de razas con stats
3. Diseñar el sistema del Don de Exploración
4. Crear el generador de eventos históricos
5. Diseñar las criaturas y monstruos
6. Escribir la documentación técnica para el Storyteller System

---

## Notas de Diseño

> Espacio para notas adicionales, ideas sueltas, o referencias que quieras guardar.

```
[ Tus notas aquí ]
```

---

**Recuerda:** No hay respuestas correctas o incorrectas. Este es TU mundo. Solo necesito saber qué dirección tomas para ayudarte a construirlo de forma coherente.