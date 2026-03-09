# CATÁLOGO COMPLETO DE ENEMIGOS

## ÍNDICE

1. [Sistema de Stats](#1-sistema-de-stats)
2. [Bestias](#2-bestias)
3. [Humanoides](#3-humanoides)
4. [No-Muertos](#4-no-muertos)
5. [Mágicos](#5-mágicos)
6. [Demonios](#6-demonios)
7. [Dragones](#7-dragones)
8. [Enemigos Únicos](#8-enemigos-únicos)
9. [Semi-Jefes](#9-semi-jefes)
10. [Jefes](#10-jefes)
11. [Jefes Finales](#11-jefes-finales)
12. [Catálogo de Items de Drop](#12-catálogo-de-items-de-drop)

---

## 1. SISTEMA DE STATS

### Fórmulas de Escalado por Nivel

El sistema de stats se basa en un escalado progresivo según el nivel del enemigo y su categoría de rareza.

#### Fórmula Base de Stats

```
Stat_Base = (Stat_Fundamental × Multiplicador_Categoría) + (Nivel × Escalado_Por_Nivel)
```

#### Multiplicadores por Categoría

| Categoría | Multiplicador | Color | Descripción |
|-----------|---------------|-------|-------------|
| **Común** | x1.0 | Blanco | Enemigos estándar, abundantes |
| **Único** | x1.5 | Verde | Enemigos especiales, poco comunes |
| **Semi-Jefe** | x2.0 | Azul | Mini-bosses de zona |
| **Jefe** | x3.0 | Púrpura | Bosses de dungeons/zonas |
| **Jefe Final** | x5.0 | Dorado | Bosses de historia principal |

#### Stats Fundamentales por Tipo de Enemigo

| Tipo | HP_Base | ATK_Base | DEF_Base | VEL_Base | CRT_Base | EVS_Base |
|------|---------|----------|----------|----------|----------|----------|
| Bestia Menor | 30 | 8 | 3 | 12 | 5% | 8% |
| Bestia Mayor | 60 | 12 | 6 | 8 | 8% | 5% |
| Humanoide Débil | 25 | 10 | 5 | 10 | 5% | 10% |
| Humanoide Fuerte | 50 | 15 | 10 | 8 | 10% | 8% |
| No-Muerto Menor | 20 | 6 | 2 | 6 | 3% | 3% |
| No-Muerto Mayor | 80 | 14 | 8 | 5 | 5% | 5% |
| Mágico Menor | 35 | 18 | 4 | 10 | 12% | 15% |
| Mágico Mayor | 70 | 25 | 8 | 12 | 15% | 12% |
| Demonio Menor | 45 | 16 | 8 | 11 | 10% | 10% |
| Demonio Mayor | 120 | 28 | 15 | 9 | 12% | 8% |
| Dragón Joven | 150 | 30 | 20 | 7 | 15% | 5% |
| Dragón Adulto | 300 | 50 | 35 | 6 | 20% | 3% |

#### Escalado por Nivel

```
HP_Escalado = Nivel × 8
ATK_Escalado = Nivel × 2
DEF_Escalado = Nivel × 1.5
VEL_Escalado = Nivel × 0.5
CRT_Escalado = Nivel × 0.5% (máximo 50%)
EVS_Escalado = Nivel × 0.3% (máximo 40%)
```

#### Fórmulas de Recompensas

```
EXP_Base = (HP_Total + ATK_Total + DEF_Total) × 0.5 × Multiplicador_Categoría
ORO_Base = Nivel × 10 × Multiplicador_Categoría
```

#### Tabla de Niveles por Zona

| Zona | Nivel Enemigos | Nivel Jefe |
|------|----------------|------------|
| Pradera Inicial | 1-5 | 6 |
| Bosque Sombrío | 5-10 | 12 |
| Cueva Cristal | 8-15 | 18 |
| Desierto Ardiente | 15-22 | 25 |
| Pantano Corrupto | 20-28 | 32 |
| Montaña Helada | 25-35 | 40 |
| Volcán Infernal | 35-45 | 50 |
| Castillo Oscuro | 45-55 | 60 |
| Abismo Demoníaco | 55-70 | 75 |
| Torre del Caos | 70-90 | 95 |

---

## 2. BESTIAS

### 2.1 Lobos

#### Lobo Salvaje
**HP:** 38 | **ATK:** 10 | **DEF:** 4 | **VEL:** 14 | **CRT:** 5% | **EVS:** 10% | **EXP:** 26 | **ORO:** 10
**Categoría:** Común | **Nivel:** 1-3
**Descripción:** Un lobo común que habita en los bosques y praderas cercanas a los asentamientos humanos. Su pelaje gris le permite camuflarse entre la vegetación.
**Comportamiento:** Ataca en manadas de 3-5 individuos. Prioriza objetivos con baja salud. Huye si queda solo y su HP baja del 20%.
**Habilidades:**
- **Mordisco:** Ataque básico que causa daño físico.
- **Aullido de Manada:** Aumenta ATK +15% a todos los lobos aliados por 3 turnos.
**Drops:**
- Piel de Lobo (45%)
- Colmillo de Lobo (30%)
- Carne Cruda (25%)
- Garra Menor (10%)

---

#### Lobo Alfa
**HP:** 65 | **ATK:** 16 | **DEF:** 8 | **VEL:** 13 | **CRT:** 10% | **EVS:** 8% | **EXP:** 45 | **ORO:** 25
**Categoría:** Común | **Nivel:** 4-7
**Descripción:** El líder de una manada de lobos, más grande y fuerte que sus subordinados. Su pelaje tiene un tono plateado distintivo.
**Comportamiento:** Siempre acompaña a 2-4 Lobos Salvajes. Ataca primero al objetivo con mayor ATK. Usa Aullido de Manada en su primer turno.
**Habilidades:**
- **Mordisco Feroz:** Ataque que causa 150% de daño y tiene 20% de probabilidad de sangrado.
- **Aullido de Manada:** Aumenta ATK +20% a todos los aliados por 3 turnos.
- **Zarpazo:** Ataque de área que causa 80% de daño a todos los enemigos.
**Drops:**
- Piel de Lobo Alfa (40%)
- Colmillo de Lobo Alfa (35%)
- Carne de Calidad (20%)
- Garra Media (15%)
- Amuleto de Lobo (5%)

---

#### Lobo Sombra
**HP:** 85 | **ATK:** 22 | **DEF:** 6 | **VEL:** 18 | **CRT:** 15% | **EVS:** 20% | **EXP:** 65 | **ORO:** 40
**Categoría:** Único | **Nivel:** 8-12
**Descripción:** Un lobo de pelaje negro como la noche que habita en zonas oscuras. Se dice que fue corrompido por magia oscura antigua.
**Comportamiento:** Aparece solo o en parejas. Usa sigilo para atacar por la espalda. Puede desvanecerse en las sombras para evitar ataques.
**Habilidades:**
- **Mordisco Sombrío:** Causa daño físico + daño oscuro adicional (20% del daño físico).
- **Paso de Sombra:** Se vuelve intocable por 1 turno, evitando todos los ataques.
- **Garra de las Tinieblas:** Ataque que ignora 50% de la DEF del objetivo.
- **Aura de Oscuridad:** Reduce la precisión de todos los enemigos -15% por 3 turnos.
**Drops:**
- Pelaje de Sombra (35%)
- Esencia Oscura (25%)
- Colmillo Negro (20%)
- Fragmento de Sombra (15%)
- Gema de Oscuridad (5%)

---

#### Lobo Invernal
**HP:** 110 | **ATK:** 28 | **DEF:** 12 | **VEL:** 11 | **CRT:** 12% | **EVS:** 8% | **EXP:** 90 | **ORO:** 55
**Categoría:** Único | **Nivel:** 13-18
**Descripción:** Un majestuoso lobo de pelaje blanco que habita en las regiones heladas. Su aliento congela el aire a su alrededor.
**Comportamiento:** Aparece en zonas nevadas. Usa ataques de hielo para ralentizar enemigos. Inmune a efectos de congelación.
**Habilidades:**
- **Mordisco Helado:** Causa daño físico + daño de hielo. 30% de probabilidad de ralentizar.
- **Aliento de Escarcha:** Ataque de área que causa daño de hielo y reduce VEL -20% por 2 turnos.
- **Aura Invernal:** Todos los enemigos reciben 5% de su HP máximo como daño de hielo cada turno.
- **Reflejo de Hielo:** Crea un escudo que absorbe 50 de daño y refleja 25% como daño de hielo.
**Drops:**
- Pelaje Invernal (30%)
- Cristal de Hielo (25%)
- Colmillo de Escarcha (20%)
- Esencia de Frío (15%)
- Núcleo de Hielo (5%)

---

#### Lobo Infernal
**HP:** 150 | **ATK:** 35 | **DEF:** 10 | **VEL:** 15 | **CRT:** 18% | **EVS:** 12% | **EXP:** 130 | **ORO:** 80
**Categoría:** Único | **Nivel:** 19-25
**Descripción:** Un lobo demoníaco de pelaje rojo llameante y ojos de fuego. Se dice que proviene del mismo infierno.
**Comportamiento:** Extremadamente agresivo. Ataca sin importar su HP. Causa daño de fuego con cada ataque. Inmune a fuego.
**Habilidades:**
- **Mordisco Infernal:** Causa daño físico + daño de fuego. 40% de probabilidad de quemar.
- **Llamas del Infierno:** Ataque de área que causa daño de fuego masivo a todos los enemigos.
- **Rugido de Fuego:** Aumenta ATK +30% y sus ataques causan +50% daño de fuego por 3 turnos.
- **Renacer de las Cenizas:** Al morir, revive con 25% de HP máximo (una vez por combate).
**Drops:**
- Pelaje de Fuego (25%)
- Colmillo Infernal (20%)
- Esencia de Fuego (20%)
- Cenizas Ardientes (15%)
- Núcleo de Fuego (10%)
- Alma de Lobo Infernal (3%)

---

### 2.2 Osos

#### Oso Pardo
**HP:** 80 | **ATK:** 18 | **DEF:** 12 | **VEL:** 6 | **CRT:** 8% | **EVS:** 3% | **EXP:** 55 | **ORO:** 20
**Categoría:** Común | **Nivel:** 3-6
**Descripción:** Un imponente oso pardo que habita en los bosques templados. Su fuerza bruta es temible pero suele ser pacífico si no se le provoca.
**Comportamiento:** Ataca solo cuando se le provoca o se acerca demasiado a su territorio. Se enfurece cuando su HP baja del 50%.
**Habilidades:**
- **Zarpazo:** Ataque básico de daño físico pesado.
- **Abrazo de Oso:** Inmoviliza al objetivo por 1 turno y causa daño continuo.
- **Rugido Amenazante:** Reduce la DEF de todos los enemigos -10% por 2 turnos.
**Drops:**
- Piel de Oso (40%)
- Garra de Oso (30%)
- Carne de Oso (25%)
- Miel Silvestre (15%)

---

#### Oso de las Cavernas
**HP:** 130 | **ATK:** 25 | **DEF:** 18 | **VEL:** 5 | **CRT:** 10% | **EVS:** 2% | **EXP:** 85 | **ORO:** 40
**Categoría:** Común | **Nivel:** 7-12
**Descripción:** Un oso prehistórico que habita en cuevas profundas. Más grande y resistente que el oso pardo común.
**Comportamiento:** Extremadamente territorial. Ataca a cualquier intruso en su cueva. Tiene alta resistencia a efectos de estado.
**Habilidades:**
- **Golpe Sísmico:** Ataque de área que causa daño y tiene 25% de aturdir.
- **Piel de Piedra:** Aumenta DEF +40% por 3 turnos.
- **Rugido de Caverna:** Reduce ATK de todos los enemigos -15% por 2 turnos.
- **Furia Salvaje:** Cuando HP < 30%, ATK +50% pero DEF -30%.
**Drops:**
- Piel de Caverna (35%)
- Garra Grande (25%)
- Hueso de Oso (20%)
- Cristal de Cueva (15%)
- Corazón de Oso (5%)

---

#### Oso Polar
**HP:** 160 | **ATK:** 30 | **DEF:** 20 | **VEL:** 7 | **CRT:** 12% | **EVS:** 4% | **EXP:** 110 | **ORO:** 60
**Categoría:** Único | **Nivel:** 13-18
**Descripción:** El señor de los hielos, un oso blanco majestuoso que domina las regiones árticas. Perfectamente adaptado al frío extremo.
**Comportamiento:** Cazador paciente. Espera el momento perfecto para atacar. Inmune a hielo y efectos de congelación.
**Habilidades:**
- **Zarpazo Helado:** Causa daño físico + daño de hielo. 35% de congelar.
- **Aliento Ártico:** Ataque de área de hielo que reduce VEL -30% por 2 turnos.
- **Camuflaje Blanco:** Aumenta EVS +20% por 2 turnos.
- **Furia Invernal:** Cuando HP < 40%, todos sus ataques causan daño de hielo adicional.
**Drops:**
- Piel Polar (30%)
- Garra de Hielo (25%)
- Cristal Ártico (20%)
- Esencia de Frío (15%)
- Núcleo de Hielo (5%)

---

#### Oso Corrupto
**HP:** 200 | **ATK:** 40 | **DEF:** 15 | **VEL:** 8 | **CRT:** 15% | **EVS:** 5% | **EXP:** 150 | **ORO:** 90
**Categoría:** Único | **Nivel:** 19-25
**Descripción:** Un oso que ha sido corrompido por energías oscuras. Su pelaje es negro como la noche y sus ojos brillan con un rojo enfermizo.
**Comportamiento:** Extremadamente agresivo y enloquecido. Ataca todo lo que se mueve. Sus ataques pueden corromper.
**Habilidades:**
- **Zarpazo Corrupt