# Catálogo de Enemigos - Last Adventurer

> **Versión:** 1.0 | **Sistema:** Turnos por velocidad | **Escalado:** Stats escalan con nivel

---

## Sistema de Stats

### Fórmulas de Escalado
```
HP = HP_Base × (1 + Nivel × 0.1)
ATK = ATK_Base × (1 + Nivel × 0.05)
DEF = DEF_Base × (1 + Nivel × 0.03)
Velocidad = Velocidad_Base × (1 + Nivel × 0.02)
Crítico = Crítico_Base + Nivel × 0.5 (cap 50%)
Evasión = Evasión_Base + Nivel × 0.3 (cap 50%)
Exp = Exp_Base × (1 + Nivel × 0.15)
Oro = Oro_Base × (1 + Nivel × 0.1)
```

### Categorías y Multipliers
| Categoría | HP Mult | Descripción |
|-----------|---------|-------------|
| Común | x1.0 | Enemigos básicos |
| Único | x1.5 | Enemigos especiales con nombre |
| Semi-Jefe | x2.0 | Mini-bosses de zona |
| Jefe | x3.0 | Bosses de dungeon/zona |
| Jefe Final | x5.0 | Bosses de historia |

---

# ENEMIGOS COMUNES

---

## 🐺 BESTIAS

### Lobo Salvaje
**HP:** 30 | **ATK:** 8 | **DEF:** 2 | **VEL:** 15 | **CRT:** 8% | **EVS:** 10% | **EXP:** 25 | **ORO:** 8
**Descripción:** Lobo gris que acecha en bosques.
**Comportamiento:** Ataca en manada (+20% ATK con otros lobos). Huye si HP < 30%.
**Habilidades:** Mordisco (1.2x, 15 STA)
**Drops:** Colmillo de Lobo (30%), Piel de Lobo (20%)

---

### Lobo Alfa
**HP:** 55 | **ATK:** 14 | **DEF:** 5 | **VEL:** 18 | **CRT:** 15% | **EVS:** 12% | **EXP:** 50 | **ORO:** 25
**Descripción:** Líder de la manada.
**Comportamiento:** Ataca primero. Invoca 1-2 Lobos Salvajes. Prioriza HP bajo.
**Habilidades:** Mordisco Salvaje (1.4x, Sangrado 3t), Aullido de Manada (+25% ATK aliados)
**Drops:** Colmillo Alfa (40%), Piel de Lobo Alfa (25%), Garra de Lobo (15%)

---

### Lobo de Sombra
**HP:** 45 | **ATK:** 12 | **DEF:** 3 | **VEL:** 20 | **CRT:** 18% | **EVS:** 22% | **EXP:** 40 | **ORO:** 18
**Descripción:** Lobo oscuro de zonas sin luz.
**Comportamiento:** Inmune a miedo. +30% evasión en oscuridad. Teleport corto.
**Habilidades:** Mordisco Sombrío (1.3x, Ceguera 30%), Paso de Sombra (+50% EVS 1t)
**Drops:** Colmillo Sombrío (25%), Pelaje de Sombra (20%), Esencia de Oscuridad (10%)

---

### Lobo Invernal
**HP:** 60 | **ATK:** 15 | **DEF:** 6 | **VEL:** 14 | **CRT:** 12% | **EVS:** 8% | **EXP:** 55 | **ORO:** 22
**Descripción:** Lobo blanco de zonas nevadas.
**Comportamiento:** Inmune a congelación. +20% ATK en nieve. Ralentiza con ataques.
**Habilidades:** Mordisco Helado (1.3x, Ralentiza 20%), Aliento de Escarcha (1.2x mágico, Congela 20%)
**Drops:** Colmillo Invernal (30%), Pelaje Blanco (25%), Cristal de Hielo (15%)

---

### Lobo Infernal
**HP:** 70 | **ATK:** 18 | **DEF:** 5 | **VEL:** 16 | **CRT:** 20% | **EVS:** 10% | **EXP:** 65 | **ORO:** 30
**Descripción:** Lobo con pelaje de llamas.
**Comportamiento:** Inmune a fuego. Quema con cada ataque. +30% ATK en zonas volcánicas.
**Habilidades:** Mordisco Ardiente (1.5x, Quemadura 8/t), Aullido Infernal (+30% ATK aliados, Quema área)
**Drops:** Colmillo Ardiente (30%), Pelaje de Fuego (20%), Esencia de Fuego (15%)

---

### Oso Pardo
**HP:** 80 | **ATK:** 15 | **DEF:** 8 | **VEL:** 8 | **CRT:** 5% | **EVS:** 3% | **EXP:** 60 | **ORO:** 20
**Descripción:** Oso grande de bosques y montañas.
**Comportamiento:** Furia si HP < 50% (+30% ATK, -20% DEF). Bloquea 25%.
**Habilidades:** Zarpazo (1.4x), Abrazo de Oso (1.8x, Inmoviliza 1t)
**Drops:** Garra de Oso (25%), Piel de Oso (15%), Carne de Oso (40%)

---

### Oso de las Cavernas
**HP:** 120 | **ATK:** 22 | **DEF:** 15 | **VEL:** 6 | **CRT:** 8% | **EVS:** 2% | **EXP:** 95 | **ORO:** 45
**Descripción:** Oso prehistórico de cavernas.
**Comportamiento:** Contraataca siempre. Inmune a miedo. Doble crítico en cavernas.
**Habilidades:** Golpe Sísmico (1.6x, Aturde), Rugido Aterrador (Miedo -20% ATK)
**Drops:** Garra de Oso Cave (35%), Piel de Oso Cave (20%), Hueso Grande (30%)

---

### Oso Polar
**HP:** 100 | **ATK:** 18 | **DEF:** 12 | **VEL:** 7 | **CRT:** 10% | **EVS:** 5% | **EXP:** 80 | **ORO:** 35
**Descripción:** Oso blanco del norte helado.
**Comportamiento:** Inmune a congelación/ralentización. +25% ATK en nieve. Nada.
**Habilidades:** Zarpazo Helado (1.5x, Congela 15%), Embestida Polar (1.7x, Aturde)
**Drops:** Garra Polar (30%), Piel Polar (20%), Grasa de Oso (25%)

---

### Oso Corrupto
**HP:** 110 | **ATK:** 20 | **DEF:** 10 | **VEL:** 8 | **CRT:** 12% | **EVS:** 4% | **EXP:** 85 | **ORO:** 40
**Descripción:** Oso corrompido por magia oscura.
**Comportamiento:** Siempre en Furia. Inmune a veneno/enfermedad. Aura de corrupción.
**Habilidades:** Zarpazo Corrupto (1.6x, Enfermedad), Rugido de Locura (Confusión 30%)
**Drops:** Garra Corrupta (30%), Piel Corrupta (20%), Esencia Oscura (15%)

---

### Serpiente Venenosa
**HP:** 20 | **ATK:** 6 | **DEF:** 1 | **VEL:** 20 | **CRT:** 15% | **EVS:** 25% | **EXP:** 20 | **ORO:** 5
**Descripción:** Serpiente con colmillos venenosos.
**Comportamiento:** Ataca primero. Huye si HP < 40%. +10% crítico desde sombras.
**Habilidades:** Mordedura Venenosa (1.0x, Veneno 5/t 3t)
**Drops:** Colmillo de Serpiente (20%), Veneno (30%), Piel de Serpiente (15%)

---

### Serpiente Coral
**HP:** 35 | **ATK:** 10 | **DEF:** 2 | **VEL:** 22 | **CRT:** 18% | **EVS:** 28% | **EXP:** 35 | **ORO:** 12
**Descripción:** Serpiente de colores brillantes, veneno mortal.
**Comportamiento:** Ataca primero. Veneno potente (8/t). Puede atacar 2 veces.
**Habilidades:** Mordedura Coral (1.1x, Veneno 8/t 4t), Enroscarse (+30% DEF 2t)
**Drops:** Colmillo de Coral (25%), Veneno Potente (20%), Escamas de Coral (10%)

---

### Serpiente Gigante
**HP:** 90 | **ATK:** 16 | **DEF:** 6 | **VEL:** 12 | **CRT:** 12% | **EVS:** 15% | **EXP:** 75 | **ORO:** 30
**Descripción:** Serpiente de tamaño descomunal.
**Comportamiento:** Traga si HP objetivo < 30%. Constrictor cada 3t. Inmune a veneno.
**Habilidades:** Constricción (1.4x, Inmoviliza), Tragar (2.0x, solo HP < 30%), Veneno Concentrado (12/t 3t)
**Drops:** Colmillo Gigante (35%), Piel de Serpiente Gigante (25%), Veneno Concentrado (20%)

---

### Serpiente de Ánima
**HP:** 55 | **ATK:** 14 | **DEF:** 4 | **VEL:** 18 | **CRT:** 20% | **EVS:** 20% | **EXP:** 50 | **ORO:** 25
**Descripción:** Serpiente espectral que drena energía vital.
**Comportamiento:** Drena HP con cada ataque. Inmune a efectos físicos parciales. Flota.
**Habilidades:** Mordedura de Ánima (1.3x, Drena 30% daño como HP), Toque Espectral (Ignora DEF)
**Drops:** Colmillo Espectral (25%), Esencia de Ánima (20%), Polvo de Alma (10%)

---

### Jabalí
**HP:** 45 | **ATK:** 12 | **DEF:** 6 | **VEL:** 12 | **CRT:** 10% | **EVS:** 8% | **EXP:** 35 | **ORO:** 12
**Descripción:** Jabalí agresivo con colmillos afilados.
**Comportamiento:** Carga al inicio (+30% daño). Contraataca 50%. Furia si HP < 40%.
**Habilidades:** Embestida (1.5x), Colmillazo (1.2x, Sangrado 2t)
**Drops:** Colmillo de Jabalí (30%), Piel de Jabalí (20%), Carne de Jabalí (45%)

---

### Jabalí Corrupto
**HP:** 65 | **ATK:** 18 | **DEF:** 8 | **VEL:** 14 | **CRT:** 15% | **EVS:** 6% | **EXP:** 55 | **ORO:** 22
**Descripción:** Jabalí corrompido por magia oscura.
**Comportamiento:** Siempre en Furia. Inmune a veneno/enfermedad. Carga cada 2t.
**Habilidades:** Embestida Corrupta (1.7x, Enfermedad -50% curación), Aura Oscura (+15% ATK 3t)
**Drops:** Colmillo Corrupto (35%), Piel Corrupta (20%), Esencia Oscura (15%)

---

### Jabalí Armadura
**HP:** 80 | **ATK:** 14 | **DEF:** 14 | **VEL:** 10 | **CRT:** 8% | **EVS:** 5% | **EXP:** 60 | **ORO:** 28
**Descripción:** Jabalí con piel endurecida como armadura.
**Comportamiento:** Bloquea 40%. Contraataca 30%. Lento pero resistente.
**Habilidades:** Embestida Blindada (1.4x, Aturde), Defensa Total (+50% DEF 2t)
**Drops:** Placa de Jabalí (25%), Colmillo de Jabalí (30%), Carne de Jabalí (35%)

---

### Araña del Bosque
**HP:** 25 | **ATK:** 8 | **DEF:** 3 | **VEL:** 16 | **CRT:** 12% | **EVS:** 18% | **EXP:** 22 | **ORO:** 8
**Descripción:** Araña mediana que teje telarañas.
**Comportamiento:** 30% enredar (-50% VEL). Ataca a distancia. Huye si HP < 30%.
**Habilidades:** Telaraña (-50% VEL 2t), Mordisco (1.1x)
**Drops:** Seda de Araña (35%), Veneno de Araña (20%), Patas de Araña (25%)

---

### Araña Viuda Negra
**HP:** 40 | **ATK:** 14 | **DEF:** 4 | **VEL:** 18 | **CRT:** 20% | **EVS:** 22% | **EXP:** 45 | **ORO:** 18
**Descripción:** Araña negra con marcas rojas, muy venenosa.
**Comportamiento:** Siempre envenena. Telaraña al inicio. Salta (ignora 30% DEF).
**Habilidades:** Mordedura Letal (1.2x, Veneno 10/t 4t), Telaraña Pegajosa (Inmoviliza 1t), Salto (1.4x, ignora 30% DEF)
**Drops:** Veneno de Viuda (30%), Seda de Viuda (25%), Caparazón de Viuda (15%)

---

### Araña Gigante
**HP:** 70 | **ATK:** 15 | **DEF:** 8 | **VEL:** 14 | **CRT:** 15% | **EVS:** 12% | **EXP:** 60 | **ORO:** 25
**Descripción:** Araña de tamaño monstruoso.
**Comportamiento:** Envuelve (inmoviliza). Invoca arañas pequeñas. Veneno fuerte.
**Habilidades:** Envoltura (Inmoviliza 2t), Llamada de Arácnidos (Invoca 2 Arañas Bosque), Veneno Paralizante (1.3x, Parálisis 20%)
**Drops:** Seda Gigante (30%), Veneno Paralizante (25%), Mandíbulas (20%)

---

### Araña de Cueva
**HP:** 50 | **ATK:** 12 | **DEF:** 6 | **VEL:** 15 | **CRT:** 14% | **EVS:** 16% | **EXP:** 45 | **ORO:** 18
**Descripción:** Araña pálida adaptada a la oscuridad.
**Comportamiento:** Inmune a ceguera. +20% crítico en oscuridad. Telarañas invisibles.
**Habilidades:** Telaraña Invisible (Inmoviliza, no avisa), Mordisco de Cueva (1.3x, Veneno 6/t)
**Drops:** Seda de Cueva (30%), Veneno de Cueva (20%), Ojos de Araña (15%)

---

### Águila Salvaje
**HP:** 35 | **ATK:** 10 | **DEF:** 2 | **VEL:** 25 | **CRT:** 20% | **EVS:** 30% | **EXP:** 30 | **ORO:** 10
**Descripción:** Águila que domina los cielos.
**Comportamiento:** Ataca primero siempre. +50% evasión en aire. Ataca ojos.
**Habilidades:** Picotazo (1.2x), Ataque en Picado (1.6x, ignora 40% DEF), Garra de Águila (1.3x, Ceguera 25%)
**Drops:** Pluma de Águila (35%), Garra de Águila (20%), Pico de Águila (15%)

---

### Águila Real
**HP:** 55 | **ATK:** 14 | **DEF:** 4 | **VEL:** 28 | **CRT:** 25% | **EVS:** 35% | **EXP:** 50 | **ORO:** 22
**Descripción:** Águila majestuosa de plumaje dorado.
**Comportamiento:** Ataca primero. Inmune a efectos de suelo. Visión mejorada (no ceguera).
**Habilidades:** Picotazo Real (1.4x, Sangrado), Torbellino (1.5x área), Ojo de Águila (+30% CRT 2t)
**Drops:** Pluma Dorada (30%), Garra de Águila Real (25%), Ojo de Águila (15%)

---

### Murciélago Común
**HP:** 15 | **ATK:** 4 | **DEF:** 1 | **VEL:** 22 | **CRT:** 10% | **EVS:** 35% | **EXP:** 12 | **ORO:** 4
**Descripción:** Pequeño murciélago de cueva.
**Comportamiento:** Ataca en grupos. +50% evasión en oscuridad. Huye si HP < 20%.
**Habilidades:** Mordisco (0.8x), Chirrido Aturdidor (Aturde 20%)
**Drops:** Ala de Murciélago (25%), Colmillo Pequeño (15%)

---

### Murciélago Gigante
**HP:** 45 | **ATK:** 12 | **DEF:** 4 | **VEL:** 18 | **CRT:** 15% | **EVS:** 25% | **EXP:** 40 | **ORO:** 15
**Descripción:** Murciélago de gran tamaño.
**Comportamiento:** Ataca primero. Carga en picado. +40% evasión en oscuridad.
**Habilidades:** Embestida Aérea (1.4x), Chirrido Sónico (1.2x mágico, Aturde)
**Drops:** Ala de Murciélago Grande (30%), Colmillo de Murciélago (20%), Piel de Murciélago (15%)

---

### Murciélago Vampiro
**HP:** 35 | **ATK:** 10 | **DEF:** 2 | **VEL:** 20 | **CRT:** 18% | **EVS:** 28% | **EXP:** 35 | **ORO:** 12
**Descripción:** Murciélago que se alimenta de sangre.
**Comportamiento:** Drena HP con cada ataque. Huye si HP < 30%. Inmune a sangrado.
**Habilidades:** Mordedura Vampírica (1.0x, Drena 50% daño como HP), Niebla (Evasión +30% 2t)
**Drops:** Colmillo de Vampiro (25%), Sangre Coagulada (20%), Ala de Vampiro (15%)

---

### Rata Común
**HP:** 10 | **ATK:** 3 | **DEF:** 1 | **VEL:** 18 | **CRT:** 5% | **EVS:** 20% | **EXP:** 8 | **ORO:** 2
**Descripción:** Rata pequeña de alcantarillas.
**Comportamiento:** Ataca en grupos de 3-5. Huye si HP < 30%. Porta enfermedades.
**Habilidades:** Mordisco (0.8x, Enfermedad 10%)
**Drops:** Cola de Rata (20%), Pelaje de Rata (15%)

---

### Rata Gigante
**HP:** 30 | **ATK:** 8 | **DEF:** 3 | **VEL:** 15 | **CRT:** 8% | **EVS:** 15% | **EXP:** 25 | **ORO:** 8
**Descripción:** Rata de tamaño descomunal.
**Comportamiento:** Ataca en grupos de 2-3. Mordedura infecciosa. Huye si HP < 25%.
**Habilidades:** Mordedura Infecciosa (1.2x, Enfermedad 25%), Plaga (Veneno 3/t 2t)
**Drops:** Cola de Rata Grande (25%), Colmillo de Rata (20%), Pelaje de Rata Grande (15%)

---

### Rata de Plaga
**HP:** 40 | **ATK:** 10 | **DEF:** 4 | **VEL:** 14 | **CRT:** 12% | **EVS:** 18% | **EXP:** 35 | **ORO:** 12
**Descripción:** Rata corrompida por enfermedad mágica.
**Comportamiento:** Siempre transmite enfermedad. Inmune a veneno. Aura de plaga.
**Habilidades:** Mordedura de Plaga (1.3x, Enfermedad 40%), Nube de Plaga (Veneno área 5/t)
**Drops:** Cola de Plaga (25%), Esencia de Plaga (20%), Colmillo Infectado (15%)

---

### Escorpión del Desierto
**HP:** 40 | **ATK:** 12 | **DEF:** 8 | **VEL:** 12 | **CRT:** 15% | **EVS:** 10% | **EXP:** 35 | **ORO:** 15
**Descripción:** Escorpión de las arenas del desierto.
**Comportamiento:** Pinza aturde. Cola envenena. +20% DEF en arena.
**Habilidades:** Pinza (1.3x, Aturde 20%), Aguijonazo (1.2x, Veneno 6/t 3t)
**Drops:** Pinza de Escorpión (25%), Aguijón de Escorpión (20%), Caparazón (15%)

---

### Escorpión Venenoso
**HP:** 55 | **ATK:** 15 | **DEF:** 6 | **VEL:** 14 | **CRT:** 18% | **EVS:** 12% | **EXP:** 50 | **ORO:** 22
**Descripción:** Escorpión con veneno mortal.
**Comportamiento:** Prioriza aguijonazo. Veneno acumulativo. Inmune a veneno.
**Habilidades:** Aguijonazo Mortal (1.4x, Veneno 10/t 4t), Pinza Venenosa (1.2x, Veneno 5/t)
**Drops:** Aguijón Mortal (25%), Veneno de Escorpión (20%), Caparazón Venenoso (15%)

---

### Escorpión Gigante
**HP:** 90 | **ATK:** 18 | **DEF:** 12 | **VEL:** 10 | **CRT:** 12% | **EVS:** 8% | **EXP:** 75 | **ORO:** 35
**Descripción:** Escorpión de tamaño monstruoso.
**Comportamiento:** Aturde con pinzas. Envenena con cola. Armadura natural.
**Habilidades:** Pinza Aplastante (1.6x, Inmoviliza), Aguijonazo Masivo (1.5x, Veneno 12/t 4t)
**Drops:** Pinza Gigante (30%), Aguijón Gigante (25%), Caparazón de Acero (20%)

---

### Ciervo Común
**HP:** 35 | **ATK:** 6 | **DEF:** 2 | **VEL:** 20 | **CRT:** 5% | **EVS:** 25% | **EXP:** 20 | **ORO:** 8
**Descripción:** Ciervo de bosque tranquilo.
**Comportamiento:** Huye al inicio 60%. Ataca solo si acorralado. Patada defensiva.
**Habilidades:** Coz (1.0x), Cornada (1.2x)
**Drops:** Asta de Ciervo (20%), Piel de Ciervo (25%), Carne de Ciervo (40%)

---

### Ciervo Corrupto
**HP:** 55 | **ATK:** 14 | **DEF:** 5 | **VEL:** 18 | **CRT:** 15% | **EVS:** 15% | **EXP:** 45 | **ORO:** 20
**Descripción:** Ciervo corrompido por magia oscura.
**Comportamiento:** Agresivo. No huye. Aura de corrupción. Ataca primero.
**Habilidades:** Cornada Corrupta (1.5x, Enfermedad), Bramido Oscuro (Miedo 25%)
**Drops:** Asta Corrupta (25%), Piel de Ciervo Corrupto (20%), Esencia Oscura (15%)

---

## 👤 HUMANOIDES

### Bandido Novato
**HP:** 35 | **ATK:** 10 | **DEF:** 3 | **VEL:** 14 | **CRT:** 10% | **EVS:** 12% | **EXP:** 30 | **ORO:** 15
**Descripción:** Bandido inexperto que asalta viajeros.
**Comportamiento:** Ataca en grupos. Huye si HP < 30%. Intenta robar oro.
**Habilidades:** Tajo (1.2x), Robo (Roba 10% oro)
**Drops:** Daga Oxidada (20%), Poción Pequeña (15%), Monedas (50%)

---

### Bandido Experimentado
**HP:** 55 | **ATK:** 14 | **DEF:** 5 | **VEL:** 16 | **CRT:** 15% | **EVS:** 15% | **EXP:** 50 | **ORO:** 30
**Descripción:** Bandido veterano de los caminos.
**Comportamiento:** Prioriza objetivos débiles. Usa pociones si HP < 40%. Ataque furtivo.
**Habilidades:** Tajo Preciso (1.4x, Sangrado), Emboscada (1.6x, solo si ataca primero)
**Drops:** Daga (25%), Poción Mediana (15%), Botín (40%)

---

### Bandido Líder
**HP:** 80 | **ATK:** 18 | **DEF:** 8 | **VEL:** 15 | **CRT:** 18% | **EVS:** 12% | **EXP:** 80 | **ORO:** 55
**Descripción:** Líder de una banda de bandidos.
**Comportamiento:** Ordena a aliados (+15% ATK). Invoca 2 Bandidos Novatos. No huye.
**Habilidades:** Tajo de Líder (1.5x), Orden de Ataque (+20% ATK aliados), Grito de Guerra (Miedo 20%)
**Drops:** Espada de Bandido (25%), Poción Grande (15%), Tesoro de Bandido (20%)

---

### Ladrón Callejero
**HP:** 30 | **ATK:** 8 | **DEF:** 2 | **VEL:** 20 | **CRT:** 15% | **EVS:** 25% | **EXP:** 25 | **ORO:** 12
**Descripción:** Ladrón de los bajos fondos.
**Comportamiento:** Ataca primero. Roba items. Huye rápido si HP < 40%.
**Habilidades:** Puñalada (1.1x), Robo de Item (Roba 1 item aleatorio), Evasión Rápida (+30% EVS 1t)
**Drops:** Ganzúa (20%), Monedas (40%), Daga Pequeña (15%)

---

### Ladrón de Sombras
**HP:** 50 | **ATK:** 14 | **DEF:** 4 | **VEL:** 22 | **CRT:** 20% | **EVS:** 30% | **EXP:** 50 | **ORO:** 28
**Descripción:** Ladrón especializado en el sigilo.
**Comportamiento:** Ataca primero siempre. +50% crítico desde sombras. Inmune a detección.
**Habilidades:** Puñalada Sombría (1.5x, ignora 30% DEF), Desaparecer (Evasión total 1t)
**Drops:** Capa de Sombras (20%), Daga de Sombras (15%), Polvo de Invisibilidad (10%)

---

### Ladrón Maestro
**HP:** 75 | **ATK:** 18 | **DEF:** 6 | **VEL:** 25 | **CRT:** 25% | **EVS:** 35% | **EXP:** 85 | **ORO:** 50
**Descripción:** Maestro del robo y el sigilo.
**Comportamiento:** Ataca primero. Roba items raros. Evasión extrema. Huye si HP < 30%.
**Habilidades:** Golpe Maestro (1.8x, ignora 40% DEF), Robo Mayor (Roba item raro), Sombra (Inmune 1t)
**Drops:** Capa del Maestro (15%), Daga del Maestro (10%), Llave Maestra (5%)

---

### Mercenario Recluta
**HP:** 45 | **ATK:** 12 | **DEF:** 6 | **VEL:** 12 | **CRT:** 8% | **EVS:** 8% | **EXP:** 35 | **ORO:** 18
**Descripción:** Mercenario novato contratado.
**Comportamiento:** Sigue órdenes. Bloquea con escudo. Ataque básico.
**Habilidades:** Tajo (1.2x), Bloqueo con Escudo (+40% DEF 1t)
**Drops:** Espada Corta (20%), Escudo Pequeño (15%), Contrato (10%)

---

### Mercenario Veterano
**HP:** 70 | **ATK:** 16 | **DEF:** 10 | **VEL:** 14 | **CRT:** 12% | **EVS:** 10% | **EXP:** 60 | **ORO:** 35
**Descripción:** Mercenario con experiencia de guerra.
**Comportamiento:** Bloquea frecuentemente. Contraataca. Usa tácticas.
**Habilidades:** Tajo de Guerra (1.4x), Escudo de Guerra (+50% DEF, contraataca), Grito (Aturde)
**Drops:** Espada de Guerra (25%), Escudo de Guerra (20%), Poción Mediana (15%)

---

### Mercenario Élite
**HP:** 100 | **ATK:** 22 | **DEF:** 14 | **VEL:** 16 | **CRT:** 18% | **EVS:** 12% | **EXP:** 100 | **ORO:** 60
**Descripción:** Mercenario de élite, lo mejor del mercado.
**Comportamiento:** Bloquea y contraataca siempre. Inmune a miedo. Lidera a otros.
**Habilidades:** Tajo Élite (1.6x, Sangrado), Defensa Perfecta (Inmune 1t, contraataca), Liderazgo (+25% ATK aliados)
**Drops:** Espada de Élite (20%), Armadura de Mercenario (15%), Contrato de Élite (10%)

---

### Arquero Aprendiz
**HP:** 25 | **ATK:** 10 | **DEF:** 2 | **VEL:** 16 | **CRT:** 12% | **EVS:** 15% | **EXP:** 25 | **ORO:** 10
**Descripción:** Arquero en entrenamiento.
**Comportamiento:** Ataca a distancia. Huye si enemigo cerca. Precisión baja.
**Habilidades:** Flecha (1.2x), Disparo Rápido (0.8x, 2 ataques)
**Drops:** Arco Pequeño (20%), Flechas (40%), Carcaj (15%)

---

### Arquero Cazador
**HP:** 45 | **ATK:** 14 | **DEF:** 4 | **VEL:** 18 | **CRT:** 18% | **EVS:** 20% | **EXP:** 45 | **ORO:** 22
**Descripción:** Arquero experimentado de los bosques.
**Comportamiento:** Ataca a distancia. +30% crítico a objetivos lejanos. Trampa ocasional.
**Habilidades:** Flecha Precisa (1.4x, +30% CRT), Flecha de Fuego (1.3x, Quema), Trampa (Inmoviliza)
**Drops:** Arco de Caza (25%), Flechas de Caza (30%), Trampa (15%)

---

### Arquero Francotirador
**HP:** 60 | **ATK:** 20 | **DEF:** 5 | **VEL:** 20 | **CRT:** 30% | **EVS:** 22% | **EXP:** 80 | **ORO:** 45
**Descripción:** Arquero de élite, maestro del disparo a distancia.
**Comportamiento:** Ataca a distancia extrema. +50% crítico a objetivos lejanos. Prioriza HP bajo.
**Habilidades:** Disparo Mortal (2.0x, +50% CRT), Flecha de Veneno (1.3x, Veneno 8/t), Ojo de Águila (+40% CRT 3t)
**Drops:** Arco Largo (20%), Flechas de Precisión (25%), Mira (10%)

---

### Guerrero Escudero
**HP:** 50 | **ATK:** 12 | **DEF:** 8 | **VEL:** 10 | **CRT:** 8% | **EVS:** 5% | **EXP:** 40 | **ORO:** 18
**Descripción:** Guerrero en entrenamiento con escudo.
**Comportamiento:** Bloquea frecuentemente. Protege aliados. Ataque básico.
**Habilidades:** Tajo de Espada (1.2x), Bloqueo (+50% DEF), Proteger (Aliado recibe -30% daño)
**Drops:** Espada Básica (25%), Escudo Básico (20%), Armadura Ligera (15%)

---

### Guerrero Caballero
**HP:** 80 | **ATK:** 18 | **DEF:** 14 | **VEL:** 12 | **CRT:** 12% | **EVS:** 8% | **EXP:** 70 | **ORO:** 40
**Descripción:** Caballero con armadura completa.
**Comportamiento:** Bloquea siempre. Contraataca. Inmune a miedo. Protege aliados.
**Habilidades:** Tajo de Caballero (1.4x), Escudo de Caballero (+60% DEF, contraataca), Carga (1.6x, Aturde)
**Drops:** Espada de Caballero (20%), Escudo de Caballero (15%), Armadura de Placas (10%)

---

### Guerrero Campeón
**HP:** 120 | **ATK:** 25 | **DEF:** 18 | **VEL:** 14 | **CRT:** 18% | **EVS:** 10% | **EXP:** 120 | **ORO:** 80
**Descripción:** Campeón guerrero, élite del combate.
**Comportamiento:** Bloquea y contraataca siempre. Inmune a miedo y aturdir. Lidera.
**Habilidades:** Tajo de Campeón (1.8x, Sangrado), Defensa Impenetrable (Inmune 2t), Grito de Guerra (+30% ATK aliados)
**Drops:** Espada de Campeón (15%), Armadura de Campeón (10%), Medalla de Honor (5%)

---

### Mago Oscuro Aprendiz
**HP:** 30 | **ATK:** 12 | **DEF:** 2 | **VEL:** 14 | **CRT:** 10% | **EVS:** 12% | **EXP:** 30 | **ORO:** 15
**Descripción:** Aprendiz de las artes oscuras.
**Comportamiento:** Ataca con magia. Huye si HP < 40%. Bajo HP.
**Habilidades:** Orbe Oscuro (1.3x mágico), Drenar (1.0x, drena 20% HP)
**Drops:** Bastón de Aprendiz (20%), Tomo Oscuro (15%), Esencia Oscura (10%)

---

### Mago Oscuro Hechicero
**HP:** 55 | **ATK:** 18 | **DEF:** 4 | **VEL:** 16 | **CRT:** 15% | **EVS:** 15% | **EXP:** 60 | **ORO:** 35
**Descripción:** Hechicero de magia oscura.
**Comportamiento:** Ataca con magia potente. Drena HP. Maldiciones.
**Habilidades:** Orbe de Sombra (1.5x mágico), Drenar Vida (1.2x, drena 40% HP), Maldición (-20% ATK objetivo)
**Drops:** Bastón de Hechicero (20%), Tomo de Sombras (15%), Esencia de Sombra (10%)

---

### Mago Oscuro Archimago
**HP:** 90 | **ATK:** 26 | **DEF:** 6 | **VEL:** 18 | **CRT:** 22% | **EVS:** 18% | **EXP:** 110 | **ORO:** 70
**Descripción:** Archimago de las artes prohibidas.
**Comportamiento:** Magia devastadora. Drena HP. Invoca esbirros. Inmune a magia oscura.
**Habilidades:** Tormenta Oscura (1.8x área mágico), Drenar Alma (1.5x, drena 50% HP), Invocar Sombra (Invoca 2 Sombras)
**Drops:** Bastón de Archimago (15%), Tomo Prohibido (10%), Esencia de Abismo (5%)

---

### Asesino Iniciado
**HP:** 35 | **ATK:** 14 | **DEF:** 3 | **VEL:** 20 | **CRT:** 20% | **EVS:** 25% | **EXP:** 35 | **ORO:** 18
**Descripción:** Asesino en entrenamiento.
**Comportamiento:** Ataca primero. +50% daño por la espalda. Huye si detectado.
**Habilidades:** Puñalada (1.3x), Ataque Furtivo (1.8x si por la espalda)
**Drops:** Daga de Asesino (20%), Capa Oscura (15%), Veneno (25%)

---

### Asesino Profesional
**HP:** 60 | **ATK:** 22 | **DEF:** 5 | **VEL:** 24 | **CRT:** 28% | **EVS:** 30% | **EXP:** 75 | **ORO:** 45
**Descripción:** Asesino profesional a sueldo.
**Comportamiento:** Ataca primero siempre. +100% daño por la espalda. Veneno en armas.
**Habilidades:** Puñalada Venenosa (1.5x, Veneno 10/t), Golpe Mortal (2.2x si por la espalda), Desvanecerse (Evasión total 1t)
**Drops:** Daga de Profesional (15%), Capa de Sombras (10%), Veneno Potente (20%)

---

### Asesino Sombra
**HP:** 85 | **ATK:** 28 | **DEF:** 6 | **VEL:** 28 | **CRT:** 35% | **EVS:** 40% | **EXP:** 120 | **ORO:** 80
**Descripción:** Asesino de élite, una verdadera sombra.
**Comportamiento:** Ataca primero siempre. Inmune a detección. +150% daño por la espalda. Teleport.
**Habilidades:** Ejecución (3.0x si HP objetivo < 30%), Paso de Sombra (Teleport), Marca de Muerte (Objetivo recibe +50% daño)
**Drops:** Daga de Sombra (10%), Capa del Vacío (5%), Veneno Mortal (15%)

---

### Pirata Marinero
**HP:** 40 | **ATK:** 12 | **DEF:** 4 | **VEL:** 14 | **CRT:** 12% | **EVS:** 15% | **EXP:** 35 | **ORO:** 20
**Descripción:** Marinero pirata de los mares.
**Comportamiento:** Ataca en grupo. +20% ATK en agua. Intenta abordar.
**Habilidades:** Tajo de Sable (1.3x), Pistola (1.4x, rango), Grito de Abordaje (+15% ATK)
**Drops:** Sable (20%), Pistola Vieja (10%), Monedas de Oro (40%)

---

### Pirata Corsario
**HP:** 70 | **ATK:** 18 | **DEF:** 8 | **VEL:** 16 | **CRT:** 18% | **EVS:** 18% | **EXP:** 65 | **ORO:** 45
**Descripción:** Corsario experimentado.
**Comportamiento:** Ataca primero en agua. +30% ATK en barcos. Dispara y carga.
**Habilidades:** Tajo de Corsario (1.5x, Sangrado), Pistola de Corsario (1.6x, rango), Abordaje (Inmoviliza)
**Drops:** Sable de Corsario (20%), Pistola de Corsario (15%), Mapa del Tesoro (5%)

---

### Pirata Capitán
**HP:** 100 | **ATK:** 24 | **DEF:** 12 | **VEL:** 18 | **CRT:** 22% | **EVS:** 15% | **EXP:** 100 | **ORO:** 80
**Descripción:** Capitán pirata, líder de los mares.
**Comportamiento:** Lidera a piratas. +40% ATK en barcos. Invoca tripulación. Inmune a miedo.
**Habilidades:** Tajo de Capitán (1.7x), Pistola de Capitán (1.8x, rango), Orden de Abordaje (+30% ATK aliados)
**Drops:** Sable de Capitán (15%), Pistola de Capitán (10%), Llave del Tesoro (5%)

---

### Bárbaro de Tribu
**HP:** 55 | **ATK:** 16 | **DEF:** 6 | **VEL:** 14 | **CRT:** 15% | **EVS:** 10% | **EXP:** 45 | **ORO:** 22
**Descripción:** Bárbaro de las tribus salvajes.
**Comportamiento:** Ataque agresivo. Furia si HP < 50%. +20% ATK en grupo.
**Habilidades:** Tajo de Hacha (1.4x), Grito de Guerra (+20% ATK), Furia (+30% ATK, -20% DEF)
**Drops:** Hacha de Bárbaro (20%), Piel de Bestia (15%), Tótem (10%)

---

### Bárbaro Berserker
**HP:** 80 | **ATK:** 24 | **DEF:** 4 | **VEL:** 16 | **CRT:** 25% | **EVS:** 8% | **EXP:** 80 | **ORO:** 50
**Descripción:** Bárbaro en estado de furia constante.
**Comportamiento:** Siempre en Furia. Ataque doble ocasional. Inmune a miedo y aturdir.
**Habilidades:** Tajo Berserker (1.8x), Furia Incontrolable (+50% ATK, -30% DEF, 2 ataques), Grito Salvaje (Aturde área)
**Drops:** Hacha Berserker (15%), Piel de Oso (10%), Collar de Colmillos (10%)

---

### Bárbaro Jefe
**HP:** 120 | **ATK:** 30 | **DEF:** 10 | **VEL:** 18 | **CRT:** 28% | **EVS:** 10% | **EXP:** 130 | **ORO:** 100
**Descripción:** Jefe de una tribu bárbara.
**Comportamiento:** Lidera tribu. Siempre en Furia. Inmune a miedo. Invoca bárbaros.
**Habilidades:** Tajo de Jefe (2.0x, Sangrado), Grito de Jefe (+40% ATK aliados), Invocar Tribu (2 Bárbaros)
**Drops:** Hacha de Jefe (10%), Corona de Huesos (5%), Tótem Mayor (5%)

---

### Nigromante Aprendiz
**HP:** 35 | **ATK:** 14 | **DEF:** 3 | **VEL:** 14 | **CRT:** 10% | **EVS:** 12% | **EXP:** 40 | **ORO:** 20
**Descripción:** Aprendiz de nigromancia.
**Comportamiento:** Invoca esqueletos. Magia oscura básica. Huye si HP < 30%.
**Habilidades:** Orbe de Muerte (1.3x mágico), Invocar Esqueleto (1 Esqueleto Guerrero)
**Drops:** Bastón de Nigromante (20%), Hueso (30%), Tomo de Muerte (10%)

---

### Nigromante Oscuro
**HP:** 65 | **ATK:** 20 | **DEF:** 5 | **VEL:** 16 | **CRT:** 15% | **EVS:** 15% | **EXP:** 70 | **ORO:** 45
**Descripción:** Nigromante con poder oscuro.
**Comportamiento:** Invoca no-muertos. Magia de muerte. Drena vida.
**Habilidades:** Orbe de Oscuridad (1.6x mágico), Invocar Muertos (2 Esqueletos), Drenar Vida (1.2x, drena 30%)
**Drops:** Bastón Oscuro (15%), Tomo de Oscuridad (10%), Esencia de Muerte (10%)

---

### Nigromante Mayor
**HP:** 100 | **ATK:** 28 | **DEF:** 8 | **VEL:** 18 | **CRT:** 20% | **EVS:** 18% | **EXP:** 120 | **ORO:** 90
**Descripción:** Maestro nigromante de gran poder.
**Comportamiento:** Invoca ejército de no-muertos. Magia devastadora. Inmune a veneno/muerte.
**Habilidades:** Tormenta de Muerte (1.8x área mágico), Levantar Ejército (3 Esqueletos + 1 Zombi), Drenar Alma (1.5x, drena 50%)
**Drops:** Bastón Mayor (10%), Tomo de Nigromancia (5%), Filacteria (5%)

---

## 💀 NO-MUERTOS

### Esqueleto Guerrero
**HP:** 40 | **ATK:** 12 | **DEF:** 6 | **VEL:** 12 | **CRT:** 10% | **EVS:** 8% | **EXP:** 30 | **ORO:** 12
**Descripción:** Esqueleto armado con espada y escudo.
**Comportamiento:** Inmune a veneno/sangrado. Bloquea ocasionalmente. No huye.
**Habilidades:** Tajo de Espada (1.2x), Bloqueo (+40% DEF)
**Drops:** Hueso (40%), Espada Oxidada (15%), Escudo Oxidado (10%)

---

### Esqueleto Arquero
**HP:** 30 | **ATK:** 14 | **DEF:** 3 | **VEL:** 14 | **CRT:** 15% | **EVS:** 12% | **EXP:** 35 | **ORO:** 15
**Descripción:** Esqueleto con arco.
**Comportamiento:** Ataca a distancia. Inmune a veneno/sangrado. Precisión media.
**Habilidades:** Flecha de Hueso (1.3x), Lluvia de Flechas (1.0x área)
**Drops:** Hueso (35%), Arco Oxidado (15%), Flechas de Hueso (20%)

---

### Esqueleto Mago
**HP:** 35 | **ATK:** 16 | **DEF:** 2 | **VEL:** 15 | **CRT:** 12% | **EVS:** 15% | **EXP:** 45 | **ORO:** 22
**Descripción:** Esqueleto con poderes mágicos.
**Comportamiento:** Ataca con magia. Inmune a veneno/sangrado. Bajo HP.
**Habilidades:** Orbe de Hueso (1.4x mágico), Maldición de Hueso (-15% DEF objetivo)
**Drops:** Hueso (30%), Bastón de Hueso (15%), Tomo Antiguo (10%)

---

### Esqueleto Caballero
**HP:** 70 | **ATK:** 18 | **DEF:** 14 | **VEL:** 10 | **CRT:** 12% | **EVS:** 5% | **EXP:** 65 | **ORO:** 40
**Descripción:** Esqueleto de un antiguo caballero.
**Comportamiento:** Inmune a veneno/sangrado/miedo. Bloquea siempre. Contraataca.
**Habilidades:** Tajo de Caballero (1.5x), Escudo de Hueso (+60% DEF, contraataca), Carga (1.6x, Aturde)
**Drops:** Hueso de Caballero (25%), Espada Antigua (10%), Armadura Oxidada (10%)

---

### Zombi Común
**HP:** 50 | **ATK:** 10 | **DEF:** 4 | **VEL:** 6 | **CRT:** 5% | **EVS:** 3% | **EXP:** 25 | **ORO:** 8
**Descripción:** Cadáver reanimado.
**Comportamiento:** Lento. Inmune a veneno/sangrado/miedo. Ataca sin parar. No huye.
**Habilidades:** Golpe (1.0x), Mordisco (1.1x, Enfermedad 10%)
**Drops:** Carne Podrida (40%), Hueso (30%), Ropa Andrajosa (15%)

---

### Zombi Putrefacto
**HP:** 65 | **ATK:** 14 | **DEF:** 5 | **VEL:** 8 | **CRT:** 8% | **EVS:** 5% | **EXP:** 40 | **ORO:** 15
**Descripción:** Zombi en estado de descomposición avanzada.
**Comportamiento:** Aura de enfermedad. Inmune a veneno/sangrado/miedo. Explota al morir.
**Habilidades:** Golpe Putrefacto (1.2x, Enfermedad 25%), Nube de Plaga (Veneno área 3/t), Explosión (Daño área al morir)
**Drops:** Carne Putrefacta (35%), Hueso (25%), Esencia de Plaga (10%)

---

### Zombi Guerrero
**HP:** 80 | **ATK:** 16 | **DEF:** 10 | **VEL:** 8 | **CRT:** 10% | **EVS:** 5% | **EXP:** 55 | **ORO:** 25
**Descripción:** Zombi de un guerrero caído.
**Comportamiento:** Inmune a veneno/sangrado/miedo/aturdir. Bloquea. No huye.
**Habilidades:** Tajo de Zombi (1.4x), Bloqueo (+50% DEF), Golpe Brutal (1.6x, Aturde)
**Drops:** Carne de Guerrero (30%), Espada Oxidada (20%), Armadura Podrida (15%)

---

### Zombi Brujo
**HP:** 55 | **ATK:** 18 | **DEF:** 4 | **VEL:** 10 | **CRT:** 12% | **EVS:** 10% | **EXP:** 50 | **ORO:** 22
**Descripción:** Zombi con poderes mágicos oscuros.
**Comportamiento:** Inmune a veneno/sangrado/miedo. Magia oscura. Invoca zombis.
**Habilidades:** Orbe de Muerte (1.4x mágico), Invocar Zombi (1 Zombi Común), Maldición (-20% ATK)
**Drops:** Carne de Brujo (25%), Bastón Podrido (15%), Tomo Maldito (10%)

---

### Fantasma Común
**HP:** 35 | **ATK:** 12 | **DEF:** 1 | **VEL:** 20 | **CRT:** 15% | **EVS:** 40% | **EXP:** 35 | **ORO:** 15
**Descripción:** Espíritu de un difunto.
**Comportamiento:** Inmune a físico parcialmente (50%). Flota. Atraviesa paredes. Huye si HP < 20%.
**Habilidades:** Toque Espectral (1.2x, ignora 30% DEF), Aullido (Miedo 20%)
**Drops:** Esencia Espectral (25%), Polvo de Alma (15%), Ectoplasma (20%)

---

### Fantasma Vengativo
**HP:** 60 | **ATK:** 18 | **DEF:** 2 | **VEL:** 22 | **CRT:** 20% | **EVS:** 45% | **EXP:** 60 | **ORO:** 35
**Descripción:** Espíritu con sed de venganza.
**Comportamiento:** Inmune a físico (60%). Ataca obsesivamente. Miedo constante.
**Habilidades:** Toque de Venganza (1.5x, ignora 40% DEF), Grito de Ira (Miedo 40%), Posesión (Confusión 30%)
**Drops:** Esencia de Venganza (20%), Alma Atormentada (15%), Cadena Espectral (10%)

---

### Poltergeist
**HP:** 45 | **ATK:** 14 | **DEF:** 1 | **VEL:** 25 | **CRT:** 18% | **EVS:** 50% | **EXP:** 50 | **ORO:** 25
**Descripción:** Espíritu travieso que mueve objetos.
**Comportamiento:** Inmune a físico (70%). Lanza objetos. Ataca primero. Travesuras.
**Habilidades:** Lanzar Objeto (1.3x), Telequinesis (Inmoviliza 1t), Caos (Confusión área)
**Drops:** Esencia de Caos (20%), Objeto Flotante (15%), Polvo de Poltergeist (10%)

---

### Wraith Sombra
**HP:** 70 | **ATK:** 20 | **DEF:** 3 | **VEL:** 24 | **CRT:** 22% | **EVS:** 50% | **EXP:** 80 | **ORO:** 50
**Descripción:** Espectro de las sombras.
**Comportamiento:** Inmune a físico (70%). Inmune a veneno/sangrado. Drena vida. Invisible.
**Habilidades:** Toque de Sombra (1.6x, drena 30% HP), Drenar Alma (1.3x, drena 40% HP), Desvanecerse (Invisible 1t)
**Drops:** Esencia de Sombra (20%), Alma Oscura (15%), Fragmento de Wraith (10%)

---

### Wraith Atemporal
**HP:** 100 | **ATK:** 26 | **DEF:** 5 | **VEL:** 26 | **CRT:** 28% | **EVS:** 55% | **EXP:** 120 | **ORO:** 80
**Descripción:** Espectro antiguo de gran poder.
**Comportamiento:** Inmune a físico (80%). Inmune a efectos de tiempo. Drena vida. Teleport.
**Habilidades:** Toque Atemporal (1.8x, drena 50% HP), Drenar Existencia (1.5x, drena 60% HP), Paso del Tiempo (Teleport)
**Drops:** Esencia Atemporal (15%), Alma Ancestral (10%), Reloj Roto (5%)

---

### Momia Guardián
**HP:** 90 | **ATK:** 18 | **DEF:** 12 | **VEL:** 8 | **CRT:** 10% | **EVS:** 5% | **EXP:** 70 | **ORO:** 45
**Descripción:** Momia guardián de tumbas.
**Comportamiento:** Inmune a veneno/sangrado/miedo. Lento pero resistente. Maldición al morir.
**Habilidades:** Golpe de Momia (1.4x), Vendas (Inmoviliza 1t), Maldición de Tumba (-20% ATK permanente hasta curar)
**Drops:** Vendas de Momia (30%), Hueso Antiguo (25%), Amuleto de Faraón (5%)

---

### Momia Faraón
**HP:** 140 | **ATK:** 28 | **DEF:** 18 | **VEL:** 10 | **CRT:** 18% | **EVS:** 8% | **EXP:** 150 | **ORO:** 120
**Descripción:** Momia de un antiguo faraón.
**Comportamiento:** Inmune a veneno/sangrado/miedo/aturdir. Invoca guardias. Magia de tumba.
**Habilidades:** Cetro de Faraón (1.8x), Maldición Real (-30% stats permanentes), Invocar Guardia (2 Momias Guardián)
**Drops:** Vendas Reales (20%), Cetro de Faraón (10%), Máscara de Faraón (5%)

---

### Calavera Flotante
**HP:** 25 | **ATK:** 10 | **DEF:** 1 | **VEL:** 22 | **CRT:** 20% | **EVS:** 35% | **EXP:** 25 | **ORO:** 10
**Descripción:** Calavera que flota y ataca.
**Comportamiento:** Inmune a físico (40%). Vuela. Ataca en grupos. Huye si HP < 30%.
**Habilidades:** Mordisco (1.0x), Chirrido (Miedo 15%)
**Drops:** Cráneo (40%), Diente (25%), Polvo de Hueso (20%)

---

### Calavera Explosiva
**HP:** 20 | **ATK:** 8 | **DEF:** 1 | **VEL:** 18 | **CRT:** 30% | **EVS:** 25% | **EXP:** 30 | **ORO:** 12
**Descripción:** Calavera que explota al contacto.
**Comportamiento:** Inmune a físico (30%). Persigue al jugador. Explota al morir o contacto.
**Habilidades:** Explosión (2.5x área al morir), Persecución (Doble velocidad)
**Drops:** Cráneo (30%), Polvo Explosivo (20%), Cenizas (25%)

---

### Espectro Común
**HP:** 50 | **ATK:** 16 | **DEF:** 2 | **VEL:** 22 | **CRT:** 18% | **EVS:** 45% | **EXP:** 45 | **ORO:** 22
**Descripción:** Espíritu menor.
**Comportamiento:** Inmune a físico (50%). Flota. Ataca en grupos. Huye si HP < 25%.
**Habilidades:** Toque Espectral (1.3x, ignora 25% DEF), Aullido Espeluznante (Miedo 25%)
**Drops:** Esencia Espectral (25%), Ectoplasma (20%), Polvo de Alma (15%)

---

### Espectro Mayor
**HP:** 85 | **ATK:** 24 | **DEF:** 4 | **VEL:** 26 | **CRT:** 25% | **EVS:** 50% | **EXP:** 90 | **ORO:** 60
**Descripción:** Espíritu de gran poder.
**Comportamiento:** Inmune a físico (65%). Inmune a miedo. Drena vida. Teleport.
**Habilidades:** Toque Mayor (1.7x, ignora 40% DEF), Drenar Espíritu (1.4x, drena 40% HP), Paso Espectral (Teleport)
**Drops:** Esencia Mayor (20%), Alma Mayor (15%), Fragmento Espectral (10%)

---

### Lich Menor
**HP:** 80 | **ATK:** 24 | **DEF:** 6 | **VEL:** 18 | **CRT:** 20% | **EVS:** 20% | **EXP:** 100 | **ORO:** 70
**Descripción:** Hechicero que alcanzó inmortalidad parcial.
**Comportamiento:** Inmune a veneno/sangrado/miedo. Magia oscura potente. Invoca no-muertos.
**Habilidades:** Orbe de Muerte (1.8x mágico), Invocar Esqueletos (3 Esqueletos), Drenar Vida (1.3x, drena 40%)
**Drops:** Bastón de Lich (15%), Tomo de Lich (10%), Fragmento de Filacteria (5%)

---

### Lich Guardián
**HP:** 120 | **ATK:** 32 | **DEF:** 10 | **VEL:** 20 | **CRT:** 25% | **EVS:** 25% | **EXP:** 160 | **ORO:** 120
**Descripción:** Lich guardián de una tumba o dungeon.
**Comportamiento:** Inmune a veneno/sangrado/miedo/aturdir. Magia devastadora. Ejército de no-muertos.
**Habilidades:** Tormenta de Muerte (2.0x área mágico), Ejército de Muertos (5 Esqueletos + 2 Zombis), Maldición Eterna (-40% stats)
**Drops:** Bastón de Guardián (10%), Tomo de Guardián (5%), Filacteria Parcial (3%)

---

## ✨ MÁGICOS

### Elemental de Fuego
**HP:** 60 | **ATK:** 20 | **DEF:** 4 | **VEL:** 16 | **CRT:** 18% | **EVS:** 15% | **EXP:** 55 | **ORO:** 30
**Descripción:** Espíritu de fuego puro.
**Comportamiento:** Inmune a fuego. Quema con cada ataque. Débil a agua. Explota al morir.
**Habilidades:** Llama (1.4x, Quema), Bola de Fuego (1.6x área, Quema), Explosión Ígnea (2.0x área al morir)
**Drops:** Esencia de Fuego (25%), Carbón Ardiente (20%), Cenizas Mágicas (15%)

---

### Elemental de Agua
**HP:** 55 | **ATK:** 16 | **DEF:** 8 | **VEL:** 14 | **CRT:** 12% | **EVS:** 20% | **EXP:** 50 | **ORO:** 28
**Descripción:** Espíritu de agua pura.
**Comportamiento:** Inmune a agua. Ralentiza con ataques. Débil a rayo. Cura en agua.
**Habilidades:** Chorro de Agua (1.3x, Ralentiza), Oleada (1.4x área, Ralentiza), Curar (Recupera 20% HP)
**Drops:** Esencia de Agua (25%), Agua Mágica (20%), Perla de Agua (10%)

---

### Elemental de Tierra
**HP:** 90 | **ATK:** 14 | **DEF:** 18 | **VEL:** 8 | **CRT:** 8% | **EVS:** 5% | **EXP:** 60 | **ORO:** 35
**Descripción:** Espíritu de tierra y roca.
**Comportamiento:** Inmune a veneno. Alta defensa. Débil a agua. Lento pero resistente.
**Habilidades:** Puña de Roca (1.5x, Aturde), Terremoto (1.3x área, Aturde), Muro de Piedra (+80% DEF 2t)
**Drops:** Esencia de Tierra (25%), Piedra Mágica (20%), Cristal de Tierra (10%)

---

### Elemental de Aire
**HP:** 45 | **ATK:** 18 | **DEF:** 2 | **VEL:** 28 | **CRT:** 25% | **EVS:** 40% | **EXP:** 50 | **ORO:** 28
**Descripción:** Espíritu de aire y viento.
**Comportamiento:** Inmune a tierra. Alta velocidad y evasión. Débil a hielo. Vuela.
**Habilidades:** Tornado (1.4x), Torbellino (1.5x área, Desplaza), Velocidad del Viento (+50% VEL 2t)
**Drops:** Esencia de Aire (25%), Pluma de Viento (20%), Cristal de Aire (10%)

---

### Elemental de Hielo
**HP:** 65 | **ATK:** 18 | **DEF:** 10 | **VEL:** 12 | **CRT:** 15% | **EVS:** 12% | **EXP:** 55 | **ORO:** 32
**Descripción:** Espíritu de hielo y escarcha.
**Comportamiento:** Inmune a congelación. Congela con ataques. Débil a fuego. Ralentiza.
**Habilidades:** Carámbano (1.4x, Congela 20%), Tormenta de Hielo (1.5x área, Congela 15%), Muro de Hielo (Bloquea)
**Drops:** Esencia de Hielo (25%), Cristal de Hielo (20%), Escarcha Mágica (15%)

---

### Elemental de Rayo
**HP:** 50 | **ATK:** 22 | **DEF:** 3 | **VEL:** 30 | **CRT:** 30% | **EVS:** 35% | **EXP:** 60 | **ORO:** 35
**Descripción:** Espíritu de electricidad pura.
**Comportamiento:** Inmune a parálisis. Aturde con ataques. Débil a tierra. Ataca primero.
**Habilidades:** Rayo (1.5x, Aturde 25%), Tormenta (1.6x área, Aturde 20%), Velocidad del Rayo (Ataca primero)
**Drops:** Esencia de Rayo (25%), Cristal de Rayo (20%), Fragmento Eléctrico (15%)

---

### Golem de Piedra
**HP:** 120 | **ATK:** 18 | **DEF:** 22 | **VEL:** 6 | **CRT:** 5% | **EVS:** 2% | **EXP:** 80 | **ORO:** 50
**Descripción:** Construcción de piedra animada.
**Comportamiento:** Inmune a veneno/sangrado/miedo/aturdir. Lento. Alta defensa. No huye.
**Habilidades:** Puño de Roca (1.6x), Terremoto (1.4x área, Aturde), Modo Defensa (+100% DEF 2t)
**Drops:** Piedra de Golem (30%), Núcleo de Piedra (15%), Runa de Tierra (10%)

---

### Golem de Hierro
**HP:** 180 | **ATK:** 25 | **DEF:** 30 | **VEL:** 4 | **CRT:** 8% | **EVS:** 0% | **EXP:** 140 | **ORO:** 100
**Descripción:** Construcción de hierro macizo.
**Comportamiento:** Inmune a todo efecto. Reflecta magia 30%. Extremadamente lento. Inmune a daño físico parcial.
**Habilidades:** Puño de Hierro (2.0x, Aturde), Estampida (1.8x área), Reflejo (Reflecta magia 1t)
**Drops:** Hierro de Golem (25%), Núcleo de Hierro (10%), Runa de Metal (5%)

---

### Golem de Cristal
**HP:** 100 | **ATK:** 22 | **DEF:** 15 | **VEL:** 12 | **CRT:** 20% | **EVS:** 15% | **EXP:** 100 | **ORO:** 70
**Descripción:** Construcción de cristal mágico.
**Comportamiento:** Inmune a veneno/sangrado. Reflecta magia 50%. Frágil pero potente.
**Habilidades:** Fragmento de Cristal (1.7x, Sangrado), Prisma (1.5x mágico área), Reflejo Cristalino (Reflecta 100% 1t)
**Drops:** Cristal de Golem (25%), Núcleo de Cristal (10%), Prisma Mágico (5%)

---

### Slime Verde
**HP:** 30 | **ATK:** 6 | **DEF:** 2 | **VEL:** 8 | **CRT:** 5% | **EVS:** 5% | **EXP:** 15 | **ORO:** 5
**Descripción:** Masa gelatinosa verde.
**Comportamiento:** Se divide al recibir daño. Inmune a físico parcial (30%). Absorbe ataques pequeños.
**Habilidades:** Golpe Gelatinoso (0.8x), División (Se divide en 2 si HP > 50%), Absorber (Drena 10 HP)
**Drops:** Gel Verde (40%), Núcleo de Slime (10%), Esencia Viscosa (15%)

---

### Slime Ácido
**HP:** 45 | **ATK:** 12 | **DEF:** 3 | **VEL:** 10 | **CRT:** 10% | **EVS:** 8% | **EXP:** 35 | **ORO:** 18
**Descripción:** Slime con propiedades corrosivas.
**Comportamiento:** Derrite armadura (-DEF). Inmune a veneno. Se divide. Ácido constante.
**Habilidades:** Ácido (1.2x, -20% DEF), Lluvia Ácida (1.0x área, -15% DEF), División (Se divide en 2)
**Drops:** Gel Ácido (30%), Núcleo Ácido (15%), Veneno de Slime (20%)

---

### Slime Veneno
**HP:** 55 | **ATK:** 14 | **DEF:** 4 | **VEL:** 12 | **CRT:** 12% | **EVS:** 10% | **EXP:** 45 | **ORO:** 25
**Descripción:** Slime altamente venenoso.
**Comportamiento:** Inmune a veneno. Envenena con cada contacto. Se divide. Aura tóxica.
**Habilidades:** Veneno (1.3x, Veneno 8/t), Nube Tóxica (Veneno área 5/t), División (Se divide en 2)
**Drops:** Gel Venenoso (25%), Núcleo Venenoso (15%), Esencia de Veneno (20%)

---

### Slime Metal
**HP:** 80 | **ATK:** 10 | **DEF:** 25 | **VEL:** 6 | **CRT:** 5% | **EVS:** 3% | **EXP:** 70 | **ORO:** 50
**Descripción:** Slime metálico con alta defensa.
**Comportamiento:** Inmune a físico (50%). Alta defensa. Se divide menos. Reflecta daño.
**Habilidades:** Golpe Metálico (1.0x), Reflejo (Devuelve 30% daño), División (Se divide en 2 si HP > 70%)
**Drops:** Gel Metálico (20%), Núcleo Metálico (10%), Mineral de Slime (15%)

---

### Espíritu del Bosque
**HP:** 50 | **ATK:** 14 | **DEF:** 6 | **VEL:** 18 | **CRT:** 15% | **EVS:** 25% | **EXP:** 45 | **ORO:** 25
**Descripción:** Espíritu protector del bosque.
**Comportamiento:** Inmune a efectos de tierra. Cura plantas. +30% stats en bosque. Neutral.
**Habilidades:** Hoja Cortante (1.3x), Curar Naturaleza (Cura 30% HP aliado), Raíces (Inmoviliza 1t)
**Drops:** Esencia de Bosque (25%), Hoja Espiritual (20%), Semilla Mágica (15%)

---

### Espíritu del Agua
**HP:** 45 | **ATK:** 12 | **DEF:** 8 | **VEL:** 16 | **CRT:** 12% | **EVS:** 22% | **EXP:** 40 | **ORO:** 22
**Descripción:** Espíritu de fuentes y ríos.
**Comportamiento:** Inmune a agua. Cura en agua. +30% stats en agua. Neutral.
**Habilidades:** Burbuja (1.2x, Ralentiza), Curar Agua (Cura 25% HP aliado), Oleada (1.3x área)
**Drops:** Esencia de Agua (25%), Gota Espiritual (20%), Perla de Agua (15%)

---

### Espíritu del Fuego
**HP:** 55 | **ATK:** 18 | **DEF:** 4 | **VEL:** 18 | **CRT:** 18% | **EVS:** 18% | **EXP:** 50 | **ORO:** 28
**Descripción:** Espíritu de llamas y volcanes.
**Comportamiento:** Inmune a fuego. +30% stats en zonas volcánicas. Quema con ataques.
**Habilidades:** Llama Espiritual (1.4x, Quema), Fuego Fatuo (1.5x, Ceguera 20%), Cura Fuego (Cura 20% HP aliado de fuego)
**Drops:** Esencia de Fuego (25%), Llama Espiritual (20%), Ceniza Mágica (15%)

---

### Hada Pícara
**HP:** 25 | **ATK:** 8 | **DEF:** 2 | **VEL:** 28 | **CRT:** 20% | **EVS:** 45% | **EXP:** 30 | **ORO:** 18
**Descripción:** Hada traviesa del bosque.
**Comportamiento:** Alta evasión. Travesuras (confusión, ceguera). Huye rápido. Vuela.
**Habilidades:** Polvo de Hada (Confusión 30%), Destello (Ceguera 25%), Curita (Cura 15 HP)
**Drops:** Polvo de Hada (30%), Ala de Hada (20%), Esencia Pícara (15%)

---

### Hada Oscura
**HP:** 45 | **ATK:** 16 | **DEF:** 4 | **VEL:** 26 | **CRT:** 25% | **EVS:** 40% | **EXP:** 55 | **ORO:** 35
**Descripción:** Hada corrompida por oscuridad.
**Comportamiento:** Inmune a miedo. Maldiciones constantes. Drena vida. Vuela.
**Habilidades:** Maldición de Hada (-20% stats), Drenar Vida (1.2x, drena 30%), Oscuridad (Ceguera 40%)
**Drops:** Polvo Oscuro (25%), Ala Oscura (15%), Esencia de Hada Oscura (10%)

---

## 😈 DEMONIOS

### Imp Común
**HP:** 25 | **ATK:** 10 | **DEF:** 2 | **VEL:** 20 | **CRT:** 15% | **EVS:** 25% | **EXP:** 25 | **ORO:** 12
**Descripción:** Pequeño demonio débil.
**Comportamiento:** Ataca en grupos. Huye si HP < 30%. Inmune a fuego. Travesuras.
**Habilidades:** Arañazo (1.0x), Bola de Fuego Pequeña (1.2x, Quema), Travesura (Confusión 15%)
**Drops:** Cuerno de Imp (25%), Cola de Imp (20%), Esencia Demoníaca (10%)

---

### Imp de Fuego
**HP:** 40 | **ATK:** 16 | **DEF:** 3 | **VEL:** 22 | **CRT:** 20% | **EVS:** 20% | **EXP:** 45 | **ORO:** 25
**Descripción:** Imp con poder de fuego.
**Comportamiento:** Inmune a fuego. Quema con cada ataque. Débil a hielo. Explota al morir.
**Habilidades:** Bola de Fuego (1.4x, Quema), Llamas (1.3x área, Quema), Explosión (2.0x área al morir)
**Drops:** Cuerno Ardiente (20%), Cola de Fuego (15%), Esencia de Fuego Demoníaco (15%)

---

### Imp de Sombra
**HP:** 35 | **ATK:** 12 | **DEF:** 2 | **VEL:** 26 | **CRT:** 22% | **EVS:** 35% | **EXP:** 40 | **ORO:** 22
**Descripción:** Imp de las sombras.
**Comportamiento:** Inmune a miedo. +50% evasión en oscuridad. Teleport. Invisible.
**Habilidades:** Puñalada Sombría (1.3x), Desvanecerse (Invisible 1t), Mordisco de Sombra (1.2x, Ceguera)
**Drops:** Cuerno de Sombra (20%), Cola de Sombra (15%), Esencia de Sombra Demoníaca (15%)

---

### Súcubo Menor
**HP:** 55 | **ATK:** 18 | **DEF:** 5 | **VEL:** 20 | **CRT:** 22% | **EVS:** 30% | **EXP:** 60 | **ORO:** 40
**Descripción:** Demonio femenino seductor.
**Comportamiento:** Encanta objetivos. Drena vida. Inmune a miedo. Vuela.
**Habilidades:** Encanto (Confusión 40%), Drenar Vida (1.3x, drena 35%), Beso de Súcubo (1.5x, Encanta)
**Drops:** Ala de Súcubo (20%), Esencia de Súcubo (15%), Perfume Demoníaco (10%)

---

### Súcubo Mayor
**HP:** 90 | **ATK:** 26 | **DEF:** 8 | **VEL:** 24 | **CRT:** 28% | **EVS:** 35% | **EXP:** 110 | **ORO:** 80
**Descripción:** Súcubo de gran poder.
**Comportamiento:** Encanta área. Drena vida masivamente. Inmune a miedo/confusión. Vuela.
**Habilidades:** Encanto Mayor (Confusión área 50%), Drenar Alma (1.6x, drena 50%), Dominación (Controla 1t)
**Drops:** Ala de Súcubo Mayor (15%), Esencia Mayor (10%), Corazón de Súcubo (5%)

---

### Íncubo Menor
**HP:** 60 | **ATK:** 20 | **DEF:** 6 | **VEL:** 18 | **CRT:** 20% | **EVS:** 25% | **EXP:** 65 | **ORO:** 45
**Descripción:** Demonio masculino seductor.
**Comportamiento:** Encanta objetivos. Drena energía. Inmune a miedo. Vuela.
**Habilidades:** Encanto (Confusión 35%), Drenar Energía (1.4x, drena STA), Abrazo de Íncubo (1.6x, Encanta)
**Drops:** Ala de Íncubo (20%), Esencia de Íncubo (15%), Perfume Oscuro (10%)

---

### Demonio Menor
**HP:** 70 | **ATK:** 20 | **DEF:** 8 | **VEL:** 16 | **CRT:** 18% | **EVS:** 15% | **EXP:** 70 | **ORO:** 50
**Descripción:** Demonio básico.
**Comportamiento:** Inmune a fuego/miedo. Ataque físico fuerte. Aura de miedo.
**Habilidades:** Garra de Demonio (1.5x, Sangrado), Aura de Miedo (Miedo 25%), Rugido Demoníaco (Aturde)
**Drops:** Cuerno de Demonio (20%), Garra de Demonio (15%), Esencia Demoníaca (15%)

---

### Demonio Guerrero
**HP:** 110 | **ATK:** 28 | **DEF:** 14 | **VEL:** 14 | **CRT:** 20% | **EVS:** 10% | **EXP:** 100 | **ORO:** 80
**Descripción:** Demonio guerrero de élite.
**Comportamiento:** Inmune a fuego/miedo/aturdir. Bloquea. Contraataca. Armadura natural.
**Habilidades:** Tajo Demoníaco (1.8x, Sangrado), Escudo Infernal (+60% DEF, contraataca), Carga Demoníaca (2.0x, Aturde)
**Drops:** Cuerno de Guerrero (15%), Armadura Demoníaca (10%), Espada Infernal (10%)

---

### Demonio Mago
**HP:** 80 | **ATK:** 30 | **DEF:** 6 | **VEL:** 18 | **CRT:** 25% | **EVS:** 20% | **EXP:** 95 | **ORO:** 75
**Descripción:** Demonio con poderes mágicos.
**Comportamiento:** Inmune a fuego/miedo. Magia devastadora. Invoca imps. Bajo HP.
**Habilidades:** Infierno (2.0x área mágico, Quema), Invocar Imps (3 Imps), Maldición Demoníaca (-30% stats)
**Drops:** Cuerno de Mago (15%), Bastón Infernal (10%), Tomo Demoníaco (10%)

---

### Sombra Común
**HP:** 40 | **ATK:** 14 | **DEF:** 2 | **VEL:** 24 | **CRT:** 20% | **EVS:** 45% | **EXP:** 45 | **ORO:** 25
**Descripción:** Manifestación de oscuridad.
**Comportamiento:** Inmune a físico (60%). Inmune a miedo. Alta evasión. Drena vida.
**Habilidades:** Toque de Sombra (1.3x, ignora 30% DEF), Drenar (1.0x, drena 25% HP), Desvanecerse (Inmune 1t)
**Drops:** Esencia de Sombra (25%), Fragmento de Oscuridad (20%), Polvo de Sombra (15%)

---

### Sombra Mayor
**HP:** 75 | **ATK:** 24 | **DEF:** 4 | **VEL:** 28 | **CRT:** 28% | **EVS:** 50% | **EXP:** 90 | **ORO:** 60
**Descripción:** Manifestación de oscuridad poderosa.
**Comportamiento:** Inmune a físico (75%). Inmune a miedo/confusión. Drena vida masivamente. Teleport.
**Habilidades:** Toque Mayor (1.7x, ignora 50% DEF), Drenar Alma (1.4x, drena 45% HP), Paso de Sombra (Teleport)
**Drops:** Esencia Mayor (20%), Fragmento de Abismo (15%), Corazón de Sombra (10%)

---

### Hellhound Común
**HP:** 65 | **ATK:** 18 | **DEF:** 8 | **VEL:** 18 | **CRT:** 18% | **EVS:** 12% | **EXP:** 60 | **ORO:** 40
**Descripción:** Perro demoníaco de fuego.
**Comportamiento:** Inmune a fuego. Quema con mordiscos. Ataca en manada. Rastrea.
**Habilidades:** Mordisco de Fuego (1.4x, Quema), Aullido Infernal (+20% ATK aliados), Rastreo (No pierde objetivo)
**Drops:** Colmillo de Hellhound (25%), Piel de Fuego (15%), Esencia de Fuego (20%)

---

### Hellhound Alfa
**HP:** 100 | **ATK:** 26 | **DEF:** 12 | **VEL:** 22 | **CRT:** 25% | **EVS:** 15% | **EXP:** 100 | **ORO:** 75
**Descripción:** Líder de la manada de hellhounds.
**Comportamiento:** Inmune a fuego/miedo. Invoca hellhounds. Quema área. Ataca primero.
**Habilidades:** Mordisco Infernal (1.8x, Quema fuerte), Invocar Manada (2 Hellhounds), Rugido del Infierno (Quema área)
**Drops:** Colmillo Alfa (20%), Piel de Hellhound Alfa (15%), Corazón de Fuego (10%)

---

## 🐉 DRAGONES

### Wyrm Joven
**HP:** 150 | **ATK:** 28 | **DEF:** 16 | **VEL:** 14 | **CRT:** 18% | **EVS:** 10% | **EXP:** 150 | **ORO:** 120
**Descripción:** Dragón joven sin alas.
**Comportamiento:** Inmune a miedo. Aliento elemental. Alta defensa. Cola devastadora.
**Habilidades:** Mordisco de Dragón (1.6x, Sangrado), Aliento de Fuego (1.8x área, Quema), Coletazo (1.5x área)
**Drops:** Escama de Wyrm (25%), Colmillo de Dragón (15%), Corazón de Dragón Joven (5%)

---

### Wyrm Adulto
**HP:** 250 | **ATK:** 40 | **DEF:** 25 | **VEL:** 16 | **CRT:** 22% | **EVS:** 12% | **EXP:** 280 | **ORO:** 250
**Descripción:** Dragón adulto sin alas.
**Comportamiento:** Inmune a fuego/miedo. Aliento devastador. Alta defensa. Terremoto.
**Habilidades:** Mordisco de Wyrm (2.0x, Sangrado fuerte), Aliento Infernal (2.5x área, Quema fuerte), Terremoto (1.8x área, Aturde)
**Drops:** Escama de Wyrm Adulto (20%), Colmillo de Wyrm (15%), Corazón de Wyrm (5%)

---

### Drake de Fuego
**HP:** 120 | **ATK:** 24 | **DEF:** 14 | **VEL:** 18 | **CRT:** 20% | **EVS:** 15% | **EXP:** 120 | **ORO:** 90
**Descripción:** Dragón menor de fuego con alas.
**Comportamiento:** Inmune a fuego. Vuela. Aliento de fuego. Ataque en picado.
**Habilidades:** Aliento de Fuego (1.6x área, Quema), Picado (1.8x, ignora 30% DEF), Garra de Drake (1.4x)
**Drops:** Escama de Drake (25%), Ala de Drake (15%), Esencia de Fuego (20%)

---

### Drake de Hielo
**HP:** 110 | **ATK:** 22 | **DEF:** 16 | **VEL:** 16 | **CRT:** 18% | **EVS:** 12% | **EXP:** 115 | **ORO:** 85
**Descripción:** Dragón menor de hielo con alas.
**Comportamiento:** Inmune a congelación. Vuela. Aliento de hielo. Ralentiza.
**Habilidades:** Aliento de Hielo (1.5x área, Congela 25%), Picado (1.7x), Garra Helada (1.3x, Ralentiza)
**Drops:** Escama de Hielo (25%), Ala de Drake (15%), Cristal de Hielo (20%)

---

### Drake de Veneno
**HP:** 100 | **ATK:** 20 | **DEF:** 12 | **VEL:** 20 | **CRT:** 22% | **EVS:** 18% | **EXP:** 110 | **ORO:** 80
**Descripción:** Dragón menor de veneno con alas.
**Comportamiento:** Inmune a veneno. Vuela. Aliento venenoso. Aura tóxica.
**Habilidades:** Aliento Venenoso (1.4x área, Veneno 12/t), Picado (1.6x), Garra Venenosa (1.3x, Veneno 8/t)
**Drops:** Escama de Veneno (25%), Ala de Drake (15%), Veneno de Dragón (20%)

---

### Wyverna Común
**HP:** 140 | **ATK:** 26 | **DEF:** 12 | **VEL:** 22 | **CRT:** 22% | **EVS:** 20% | **EXP:** 140 | **ORO:** 110
**Descripción:** Dragón con alas y cola venenosa.
**Comportamiento:** Inmune a veneno. Vuela. Cola venenosa. Ataque aéreo.
**Habilidades:** Picado de Wyverna (1.8x), Aguijón Venenoso (1.5x, Veneno 15/t), Rasguño (1.4x)
**Drops:** Escama de Wyverna (25%), Aguijón de Wyverna (15%), Ala de Wyverna (15%)

---

### Wyverna Mayor
**HP:** 200 | **ATK:** 35 | **DEF:** 18 | **VEL:** 26 | **CRT:** 28% | **EVS:** 25% | **EXP:** 220 | **ORO:** 180
**Descripción:** Wyverna de gran tamaño.
**Comportamiento:** Inmune a veneno/miedo. Vuela. Cola devastadora. Ataque aéreo múltiple.
**Habilidades:** Picado Mayor (2.2x), Aguijón Mortal (2.0x, Veneno 20/t), Torbellino (1.8x área)
**Drops:** Escama de Wyverna Mayor (20%), Aguijón Mayor (10%), Corazón de Wyverna (5%)

---

### Dragón Joven
**HP:** 200 | **ATK:** 35 | **DEF:** 22 | **VEL:** 18 | **CRT:** 22% | **EVS:** 15% | **EXP:** 220 | **ORO:** 200
**Descripción:** Dragón joven con alas.
**Comportamiento:** Inmune a fuego/miedo. Vuela. Aliento devastador. Magia dragón.
**Habilidades:** Aliento de Dragón (2.0x área, Quema fuerte), Mordisco de Dragón (1.8x, Sangrado), Rugido (Aturde área)
**Drops:** Escama de Dragón (20%), Colmillo de Dragón (15%), Corazón de Dragón Joven (5%)

---

### Dragón Adulto
**HP:** 400 | **ATK:** 55 | **DEF:** 35 | **VEL:** 20 | **CRT:** 28% | **EVS:** 18% | **EXP:** 500 | **ORO:** 500
**Descripción:** Dragón adulto de gran poder.
**Comportamiento:** Inmune a fuego/miedo/aturdir. Vuela. Aliento devastador. Magia dragón. Invoca drakes.
**Habilidades:** Aliento Infernal (3.0x área, Quema masiva), Mordisco de Dragón Adulto (2.5x, Sangrado fuerte), Invocar Drakes (2 Drakes)
**Drops:** Escama de Dragón Adulto (15%), Colmillo de Dragón Adulto (10%), Corazón de Dragón (3%)

---

# ENEMIGOS ÚNICOS

### Fenrir - El Lobo Legendario
**HP:** 300 | **ATK:** 45 | **DEF:** 20 | **VEL:** 35 | **CRT:** 35% | **EVS:** 30% | **EXP:** 400 | **ORO:** 350
**Descripción:** Lobo gigante de la mitología nórdica.
**Comportamiento:** Ataca primero siempre. Inmune a miedo. Invoca lobos. Destruye armas.
**Habilidades:** Mordisco de Fenrir (2.5x, Destruye arma), Aullido del Fin (+50% ATK aliados), Invocar Manada (5 Lobos Alfa)
**Drops:** Colmillo de Fenrir (10%), Pelaje de Fenrir (5%), Runa de Fenrir (3%)

---

### Arachne - La Reina Araña
**HP:** 280 | **ATK:** 40 | **DEF:** 18 | **VEL:** 28 | **CRT:** 30% | **EVS:** 25% | **EXP:** 380 | **ORO:** 320
**Descripción:** Araña humanoide de gran poder.
**Comportamiento:** Inmune a veneno. Teje trampas. Invoca arañas. Captura objetivos.
**Habilidades:** Telaraña Mortal (Inmoviliza 3t), Veneno de Arachne (20/t 5t), Invocar Arañas (4 Arañas Gigantes)
**Drops:** Seda de Arachne (10%), Veneno de Reina (8%), Corazón de Arachne (3%)

---

### Kraken - El Terror del Mar
**HP:** 350 | **ATK:** 50 | **DEF:** 25 | **VEL:** 15 | **CRT:** 25% | **EVS:** 15% | **EXP:** 450 | **ORO:** 400
**Descripción:** Calamar gigante de las profundidades.
**Comportamiento:** Inmune a agua. Tentáculos múltiples. Hundir barcos. Tragar objetivos.
**Habilidades:** Tentáculo (1.8x, Inmoviliza), Torbellino (2.0x área), Tragar (3.0x, solo HP < 25%)
**Drops:** Tentáculo de Kraken (10%), Ojo de Kraken (5%), Perla del Mar (3%)

---

### Gorgona - La Medusa
**HP:** 250 | **ATK:** 38 | **DEF:** 15 | **VEL:** 25 | **CRT:** 28% | **EVS:** 22% | **EXP:** 350 | **ORO:** 300
**Descripción:** Criatura con serpientes por cabello.
**Comportamiento:** Petrifica con mirada. Inmune a veneno. Serpientes atacan independientes.
**Habilidades:** Mirada Petrificante (Petrifica 1t, 40%), Mordedura de Serpientes (1.5x, Veneno 15/t), Grito de Gorgona (Miedo 50%)
**Drops:** Sangre de Gorgona (10%), Escama de Gorgona (8%), Cabeza de Medusa (3%)

---

### Quimera
**HP:** 320 | **ATK:** 48 | **DEF:** 22 | **VEL:** 22 | **CRT:** 28% | **EVS:** 18% | **EXP:** 420 | **ORO:** 380
**Descripción:** Bestia con cabeza de león, cabra y serpiente.
**Comportamiento:** Tres ataques por turno. Inmune a fuego/veneno. Aliento múltiple.
**Habilidades:** Mordisco de León (2.0x), Aliento de Fuego (1.8x área), Mordedura de Serpiente (1.6x, Veneno 12/t)
**Drops:** Cabeza de León (10%), Cuerno de Quimera (8%), Corazón de Quimera (3%)

---

### Minotauro
**HP:** 280 | **ATK:** 52 | **DEF:** 25 | **VEL:** 18 | **CRT:** 25% | **EVS:** 10% | **EXP:** 360 | **ORO:** 320
**Descripción:** Hombre-toro del laberinto.
**Comportamiento:** Inmune a miedo/aturdir. Carga devastadora. Destruye paredes. Furia constante.
**Habilidades:** Carga del Minotauro (3.0x, Aturde), Hachazo (2.2x, Sangrado), Rugido del Laberinto (Miedo 40%)
**Drops:** Hacha del Minotauro (10%), Cuerno de Minotauro (8%), Hueso de Minotauro (5%)

---

### Hidra
**HP:** 400 | **ATK:** 42 | **DEF:** 20 | **VEL:** 16 | **CRT:** 22% | **EVS:** 12% | **EXP:** 500 | **ORO:** 450
**Descripción:** Serpiente de múltiples cabezas.
**Comportamiento:** Regenera cabezas (cura 50 HP por cabeza). Ataque múltiple. Inmune a veneno.
**Habilidades:** Mordisco Múltiple (5 cabezas, 1.5x cada una), Regeneración (Cura 100 HP/turno), Veneno de Hidra (15/t)
**Drops:** Cabeza de Hidra (10%), Sangre de Hidra (8%), Corazón de Hidra (3%)

---

### Fénix
**HP:** 260 | **ATK:** 45 | **DEF:** 12 | **VEL:** 30 | **CRT:** 35% | **EVS:** 30% | **EXP:** 400 | **ORO:** 380
**Descripción:** Ave de fuego inmortal.
**Comportamiento:** Inmune a fuego. Renace al morir (50% HP). Vuela. Cura con fuego.
**Habilidades:** Llamas del Fénix (2.0x área, Quema fuerte), Renacer (Revive 1 vez), Curación de Fuego (Cura 30% HP)
**Drops:** Pluma de Fénix (10%), Lágrima de Fénix (5%), Cenizas de Fénix (3%)

---

### Behemoth
**HP:** 500 | **ATK:** 55 | **DEF:** 40 | **VEL:** 10 | **CRT:** 20% | **EVS:** 5% | **EXP:** 600 | **ORO:** 550
**Descripción:** Bestia colosal de tierra.
**Comportamiento:** Inmune a aturdir/miedo. Terremoto constante. Alta defensa. Lento.
**Habilidades:** Pisada del Behemoth (2.5x área, Aturde), Terremoto (2.0x área), Rugido de la Tierra