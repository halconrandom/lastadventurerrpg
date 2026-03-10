# Catálogo de Objetos - Last Adventurer

> **Estado:** En desarrollo
> **Última actualización:** 2026-03-09
> **Dependencias:** SISTEMA_INVENTARIO.md, SISTEMA_RAREZA.md, SISTEMA_CRAFTEO.md

---

## Resumen

Este catálogo cubre todos los objetos **no combativos** del juego: herramientas, consumibles de utilidad, materiales, misceláneos y objetos especiales. Las armas y armaduras están documentadas en `SISTEMA_ITEMS.md`.

---

## Categorías

| Categoría | Descripción | Stackeable |
|-----------|-------------|------------|
| **Herramientas** | Objetos de uso activo para exploración y supervivencia | No (1 por slot) |
| **Consumibles de Utilidad** | Objetos de un solo uso con efecto inmediato | Sí (x10) |
| **Materiales** | Recursos para crafteo y herrería | Sí (x50) |
| **Misceláneos** | Llaves, documentos, objetos de misión | Sí (x5) |
| **Objetos Especiales** | Items únicos con efectos pasivos o activos | No (1 por slot) |

---

## 1. Herramientas

Las herramientas se equipan en el slot de **Herramienta Activa** del inventario. Tienen durabilidad y se desgastan con el uso.

### 1.1 Herramientas de Exploración

| ID | Nombre | Rareza | Durabilidad | Efecto | Cómo Obtener | Valor |
|----|--------|--------|-------------|--------|--------------|-------|
| `antorcha` | Antorcha | Común | 20 usos | Ilumina cuevas y zonas oscuras. Revela sub-tiles ocultos en mazmorras. | Tienda, crafteo | 5 oro |
| `antorcha_magica` | Antorcha Mágica | Raro | Infinita | Ilumina sin consumirse. Revela trampas ocultas. | Tienda mágica, drop | 150 oro |
| `cuerda` | Cuerda | Común | 10 usos | Permite descender acantilados y acceder a zonas inaccesibles. | Tienda, crafteo | 10 oro |
| `cuerda_seda` | Cuerda de Seda | Raro | 25 usos | Más resistente. Permite escalar paredes verticales. | Tienda, crafteo | 80 oro |
| `gancho` | Gancho de Escalar | Raro | 15 usos | Combinado con cuerda, permite acceder a zonas elevadas. | Herrero, drop | 120 oro |
| `brujula` | Brújula | Común | Infinita | Muestra dirección Norte. Evita perderse en biomas confusos. | Tienda | 30 oro |
| `brujula_magica` | Brújula Mágica | Épico | Infinita | Apunta hacia la ubicación conocida más cercana. | Cartógrafo, quest | 500 oro |
| `telescopio` | Telescopio | Raro | Infinita | Revela tiles adyacentes sin explorarlos físicamente. | Tienda, crafteo | 200 oro |
| `kit_cartografo` | Kit de Cartógrafo | Raro | 30 usos | +50% XP de cartografía al explorar tiles nuevos. | Cartógrafo | 300 oro |
| `linterna` | Linterna de Aceite | Común | 30 usos | Ilumina más que la antorcha. Requiere aceite para recargar. | Tienda | 25 oro |
| `aceite_linterna` | Aceite de Linterna | Común | — | Recarga la linterna (+20 usos). | Tienda, alquimista | 8 oro |

### 1.2 Herramientas de Recolección

| ID | Nombre | Rareza | Durabilidad | Efecto | Cómo Obtener | Valor |
|----|--------|--------|-------------|--------|--------------|-------|
| `pico_hierro` | Pico de Hierro | Común | 50 usos | Permite minar minerales básicos (hierro, carbón, piedra). | Herrero, tienda | 40 oro |
| `pico_acero` | Pico de Acero | Raro | 100 usos | Permite minar minerales avanzados (mithril, gemas). | Herrero | 180 oro |
| `hacha_madera` | Hacha de Leñador | Común | 40 usos | Permite talar árboles y recolectar madera. | Herrero, tienda | 35 oro |
| `hacha_acero` | Hacha de Acero | Raro | 80 usos | Tala más rápido. Permite cortar árboles ancestrales. | Herrero | 150 oro |
| `pala` | Pala | Común | 30 usos | Permite excavar tierra, arena y nieve. Útil en ruinas. | Herrero, tienda | 20 oro |
| `hoz` | Hoz | Común | 30 usos | Recolecta plantas, hierbas y cultivos más eficientemente. | Herrero, tienda | 15 oro |
| `caña_pesca` | Caña de Pescar | Común | 20 usos | Permite pescar en ríos, lagos y costas. | Tienda | 20 oro |
| `caña_pesca_magica` | Caña Mágica | Épico | Infinita | Pesca más rápido. Posibilidad de obtener items raros del agua. | Quest, drop | 600 oro |
| `trampa_caza` | Trampa de Caza | Común | 5 usos | Se coloca en el suelo. Captura animales pequeños mientras el jugador descansa. | Tienda, crafteo | 15 oro |
| `red_pesca` | Red de Pesca | Común | 10 usos | Pesca múltiples peces a la vez en zonas costeras. | Tienda | 30 oro |

### 1.3 Herramientas de Supervivencia

| ID | Nombre | Rareza | Durabilidad | Efecto | Cómo Obtener | Valor |
|----|--------|--------|-------------|--------|--------------|-------|
| `yesca` | Yesca y Pedernal | Común | 15 usos | Enciende fogatas. Necesario para acampar en zonas frías. | Tienda | 5 oro |
| `yesca_magica` | Yesca Mágica | Raro | Infinita | Enciende fuego instantáneamente. Nunca se gasta. | Tienda mágica | 100 oro |
| `tienda_campana` | Tienda de Campaña | Común | 20 usos | Permite acampar en cualquier tile. Stash de 30 slots. | Tienda | 80 oro |
| `saco_dormir` | Saco de Dormir | Común | Infinita | Mejora la recuperación de HP/Stamina al descansar. | Tienda | 50 oro |
| `cantimplora` | Cantimplora | Común | Infinita | Almacena agua. Necesaria en biomas áridos (desierto, tundra). | Tienda | 15 oro |
| `cantimplora_magica` | Cantimplora Mágica | Épico | Infinita | Se llena sola con agua pura. Nunca se vacía. | Quest, drop | 400 oro |
| `kit_primeros_auxilios` | Kit de Primeros Auxilios | Común | 3 usos | Cura 30 HP fuera de combate. Detiene sangrado. | Tienda, alquimista | 40 oro |
| `mapa_basico` | Mapa Básico | Común | Infinita | Desbloquea el panel de mapa. Muestra tiles explorados. | Cartógrafo (100 oro) | 100 oro |
| `mapa_detallado` | Mapa Detallado | Raro | Infinita | Muestra biomas, rutas y nombres de ubicaciones. | Cartógrafo (500 oro) | 500 oro |
| `mapa_maestro` | Mapa Maestro | Legendario | Infinita | Muestra POIs, enemigos, recursos y rutas ocultas. | Quest especial | — |

---

## 2. Consumibles de Utilidad

Objetos de un solo uso con efecto inmediato. Se apilan hasta x10.

### 2.1 Pergaminos

| ID | Nombre | Rareza | Efecto | Cómo Obtener | Valor |
|----|--------|--------|--------|--------------|-------|
| `pergamino_identificar` | Pergamino de Identificar | Común | Identifica un item desconocido (raro o superior). | Tienda mágica, drop | 50 oro |
| `pergamino_teletransporte` | Pergamino de Teletransporte | Épico | Teletransporta al jugador a la última posada visitada. | Drop raro, tienda mágica | 300 oro |
| `pergamino_revelacion` | Pergamino de Revelación | Raro | Revela todos los tiles en un radio de 5 en el mapa. | Drop, tienda mágica | 150 oro |
| `pergamino_encantamiento` | Pergamino de Encantamiento | Raro | Añade un encantamiento aleatorio a un item raro o superior. | Drop, tienda mágica | 200 oro |
| `pergamino_reparacion` | Pergamino de Reparación | Común | Repara completamente un item dañado. | Tienda, herrero | 60 oro |
| `pergamino_maldicion` | Pergamino de Maldición | Épico | Maldice un item enemigo (reduce sus stats un 30%). Solo en combate. | Drop raro | 250 oro |

### 2.2 Bombas y Trampas

| ID | Nombre | Rareza | Efecto | Cómo Obtener | Valor |
|----|--------|--------|--------|--------------|-------|
| `bomba_humo` | Bomba de Humo | Común | Permite huir del combate con 100% de éxito. | Tienda, crafteo | 30 oro |
| `bomba_fuego` | Bomba de Fuego | Raro | Inflige 20 daño de fuego a todos los enemigos. | Alquimista, crafteo | 80 oro |
| `bomba_hielo` | Bomba de Hielo | Raro | Congela a un enemigo por 1 turno. | Alquimista, crafteo | 80 oro |
| `bomba_veneno` | Bomba de Veneno | Raro | Envenena a todos los enemigos (5 daño/turno por 3 turnos). | Alquimista, crafteo | 90 oro |
| `trampa_explosiva` | Trampa Explosiva | Épico | Se coloca antes del combate. Explota al inicio, 40 daño. | Herrero, crafteo | 200 oro |
| `polvo_cegador` | Polvo Cegador | Común | Ciega a un enemigo por 2 turnos (-50% precisión). | Alquimista, drop | 40 oro |

### 2.3 Comida y Bebida

La comida restaura **Stamina** y otorga buffs temporales. No restaura HP directamente.

| ID | Nombre | Rareza | Efecto | Cómo Obtener | Valor |
|----|--------|--------|--------|--------------|-------|
| `pan` | Pan | Común | +20 Stamina. | Tienda, crafteo | 3 oro |
| `carne_asada` | Carne Asada | Común | +40 Stamina, +5 HP. | Tienda, crafteo | 8 oro |
| `estofado` | Estofado de Aventurero | Común | +60 Stamina, +10 HP. Requiere fogata. | Crafteo | 5 oro (materiales) |
| `festin` | Festín del Cazador | Raro | +100 Stamina, +20 HP, +10% ATK por 1 hora. | Crafteo (receta rara) | 50 oro (materiales) |
| `fruta_silvestre` | Fruta Silvestre | Común | +10 Stamina. | Recolección, tienda | 2 oro |
| `hongos_magicos` | Hongos Mágicos | Raro | +30 Stamina, +20 Mana. Efecto alucinógeno (visión alterada). | Recolección (pantano) | 25 oro |
| `vino` | Vino | Común | +15 Stamina. -5% precisión por 30 min. | Tienda, posada | 5 oro |
| `cerveza_enana` | Cerveza Enana | Raro | +30 Stamina, +10% DEF por 1 hora. -10% velocidad. | Posada enana, crafteo | 20 oro |
| `te_herbal` | Té Herbal | Común | +20 Stamina, +5 HP/min por 5 min. | Alquimista, crafteo | 10 oro |
| `elixir_vigor` | Elixir de Vigor | Épico | +50 Stamina, +20% velocidad por 2 horas. | Alquimista | 150 oro |

---

## 3. Materiales

Recursos para crafteo. Se apilan hasta x50. No tienen durabilidad.

### 3.1 Minerales

| ID | Nombre | Rareza | Fuente | Usos Principales |
|----|--------|--------|--------|-----------------|
| `hierro` | Hierro | Común | Minas, enemigos | Armas, armaduras, herramientas |
| `carbon` | Carbón | Común | Minas, bosques | Forja (hierro → acero), fogatas |
| `acero` | Acero | Común | Forja (hierro + carbón) | Armas mejoradas, armaduras |
| `cobre` | Cobre | Común | Minas costeras | Herramientas, monedas |
| `plata` | Plata | Raro | Minas profundas | Armas anti no-muertos, joyería |
| `oro_mineral` | Oro (mineral) | Raro | Minas profundas, ríos | Joyería, encantamientos |
| `mithril` | Mithril | Épico | Minas de montaña | Armas y armaduras épicas |
| `adamantita` | Adamantita | Legendario | Volcanes, dragones | Armas y armaduras legendarias |
| `piedra` | Piedra | Común | Minas, montañas | Construcción, herramientas básicas |
| `sal` | Sal | Común | Costas, minas de sal | Conservar comida, alquimia |

### 3.2 Gemas

| ID | Nombre | Rareza | Fuente | Usos Principales |
|----|--------|--------|--------|-----------------|
| `gema_roja` | Gema Roja (Rubí) | Raro | Minas volcánicas | Encantamientos de fuego |
| `gema_azul` | Gema Azul (Zafiro) | Raro | Minas de hielo | Encantamientos de hielo/mana |
| `gema_verde` | Gema Verde (Esmeralda) | Raro | Jungla, minas | Encantamientos de veneno/vida |
| `gema_morada` | Gema Morada (Amatista) | Épico | Mazmorras, drop | Encantamientos mágicos |
| `gema_negra` | Gema Negra (Ónix) | Épico | No-muertos, mazmorras | Encantamientos de oscuridad |
| `diamante` | Diamante | Legendario | Minas profundas, jefes | Encantamientos máximos |

### 3.3 Materiales Orgánicos

| ID | Nombre | Rareza | Fuente | Usos Principales |
|----|--------|--------|--------|-----------------|
| `madera` | Madera | Común | Bosques, tala | Armas, herramientas, construcción |
| `madera_ancestral` | Madera Ancestral | Épico | Bosques ancestrales | Armas mágicas, bastones |
| `cuero` | Cuero | Común | Animales (lobo, ciervo) | Armaduras ligeras, bolsas |
| `cuero_grueso` | Cuero Grueso | Raro | Bestias grandes (oso, troll) | Armaduras medias |
| `escama_dragon` | Escama de Dragón | Legendario | Dragones | Armaduras legendarias, armas de fuego |
| `hueso` | Hueso | Común | Enemigos, animales | Herramientas básicas, alquimia |
| `hueso_dragon` | Hueso de Dragón | Legendario | Dragones | Armas legendarias |
| `pluma` | Pluma | Común | Aves, harpías | Flechas, escritura |
| `seda_araña` | Seda de Araña | Raro | Arañas gigantes | Cuerdas, armaduras ligeras |
| `veneno_serpiente` | Veneno de Serpiente | Raro | Serpientes, basiliscos | Armas envenenadas, alquimia |
| `cristal_hielo` | Cristal de Hielo | Raro | Tundra, elementales | Armas de hielo, alquimia |
| `polvo_hada` | Polvo de Hada | Épico | Hadas, zonas mágicas | Encantamientos, pociones raras |
| `corazon_demonio` | Corazón de Demonio | Épico | Demonios | Armas oscuras, alquimia avanzada |

### 3.4 Plantas e Ingredientes Alquímicos

| ID | Nombre | Rareza | Fuente | Usos Principales |
|----|--------|--------|--------|-----------------|
| `hierba_curativa` | Hierba Curativa | Común | Praderas, bosques | Pociones de HP |
| `raiz_mana` | Raíz de Maná | Común | Bosques mágicos | Pociones de Mana |
| `flor_stamina` | Flor de Stamina | Común | Montañas, praderas | Pociones de Stamina |
| `hongo_venenoso` | Hongo Venenoso | Común | Pantanos, cuevas | Venenos, pociones negativas |
| `cristal_azul` | Cristal Azul | Raro | Cuevas mágicas | Pociones de Mana avanzadas |
| `cristal_rojo` | Cristal Rojo | Raro | Volcanes, minas | Pociones de fuerza |
| `flor_lunar` | Flor Lunar | Épico | Solo de noche, praderas | Pociones de invisibilidad |
| `raiz_oscura` | Raíz Oscura | Épico | Pantanos profundos | Pociones de sombra, maldiciones |
| `esencia_dragon` | Esencia de Dragón | Legendario | Dragones | Pociones legendarias |

---

## 4. Misceláneos

Objetos de misión, llaves y documentos. Se apilan hasta x5.

### 4.1 Llaves y Accesos

| ID | Nombre | Rareza | Efecto | Cómo Obtener |
|----|--------|--------|--------|--------------|
| `llave_mazmorra` | Llave de Mazmorra | Común | Abre puertas cerradas en mazmorras. | Drop de enemigos, cofres |
| `llave_maestra` | Llave Maestra | Raro | Abre cualquier cerradura común. | Drop raro, quest |
| `llave_magica` | Llave Mágica | Épico | Abre puertas selladas con magia. | Quest, jefes |
| `ganzua` | Ganzúa | Común | Permite forzar cerraduras (requiere habilidad). 3 usos. | Tienda, drop |
| `ganzua_maestra` | Ganzúa Maestra | Raro | Fuerza cualquier cerradura. 10 usos. | Tienda especial, drop |

### 4.2 Documentos y Libros

| ID | Nombre | Rareza | Efecto | Cómo Obtener |
|----|--------|--------|--------|--------------|
| `libro_receta` | Libro de Recetas | Común | Enseña 1 receta de crafteo al leerlo. Se consume. | Tienda, drop, quest |
| `libro_habilidad` | Libro de Habilidad | Raro | Enseña 1 habilidad pasiva al leerlo. Se consume. | Drop raro, quest |
| `diario_explorador` | Diario de Explorador | Raro | Revela la ubicación de un POI o mazmorra en el mapa. | Drop, quest |
| `mapa_tesoro` | Mapa del Tesoro | Épico | Marca la ubicación de un cofre legendario. | Drop raro, quest |
| `contrato_gremio` | Contrato de Gremio | Común | Acepta una misión de gremio. | Tablón de misiones |
| `carta_presentacion` | Carta de Presentación | Común | +20 reputación con una facción específica. | Quest, NPC |
| `pergamino_lore` | Pergamino de Lore | Común | Revela fragmento de historia del mundo. | Ruinas, drop, quest |

### 4.3 Objetos de Misión

| ID | Nombre | Rareza | Efecto | Cómo Obtener |
|----|--------|--------|--------|--------------|
| `reliquia_antigua` | Reliquia Antigua | Épico | Objeto de misión. No se puede vender ni tirar. | Quest específica |
| `cristal_memoria` | Cristal de Memoria | Épico | Contiene un recuerdo de un NPC. Necesario para quest. | Drop, quest |
| `sello_faccion` | Sello de Facción | Raro | Prueba de membresía en una facción. | Quest de facción |
| `fragmento_artefacto` | Fragmento de Artefacto | Legendario | Parte de un artefacto legendario. Se combina con otros fragmentos. | Jefes, mazmorras |

---

## 5. Objetos Especiales

Items únicos con efectos pasivos o activos. No se apilan. Algunos son equipables en slots de accesorio.

### 5.1 Amuletos y Anillos (Accesorios)

> Ver también `SISTEMA_ITEMS.md` para la lista completa de accesorios equipables.

| ID | Nombre | Rareza | Slot | Efecto Pasivo | Cómo Obtener |
|----|--------|--------|------|---------------|--------------|
| `amuleto_exploracion` | Amuleto del Explorador | Raro | Amuleto | +1 tile de radio de visión. +25% XP de cartografía. | Quest, drop |
| `anillo_peso` | Anillo de Carga | Raro | Anillo | +20 kg de capacidad de peso. | Tienda mágica, drop |
| `amuleto_suerte` | Amuleto de la Suerte | Épico | Amuleto | +10% probabilidad de drops raros. | Quest, jefes |
| `anillo_velocidad` | Anillo de Velocidad | Épico | Anillo | +15% velocidad de movimiento. | Drop, tienda mágica |
| `amuleto_vida` | Amuleto de Vida | Épico | Amuleto | +50 HP máximo. | Quest, jefes |
| `anillo_mana` | Anillo de Maná | Raro | Anillo | +30 Mana máximo. | Tienda mágica, drop |
| `amuleto_resistencia` | Amuleto de Resistencia | Épico | Amuleto | +15% resistencia a todos los elementos. | Jefes, quest |
| `anillo_comerciante` | Anillo del Comerciante | Raro | Anillo | +10% precio de venta a NPCs. | Tienda especial |

### 5.2 Objetos de Uso Activo (No Equipables)

Se usan desde el inventario con efecto inmediato o temporal.

| ID | Nombre | Rareza | Efecto | Usos | Cómo Obtener | Valor |
|----|--------|--------|--------|------|--------------|-------|
| `piedra_portal` | Piedra de Portal | Épico | Crea un portal temporal de regreso a la última posada. 1 uso. | 1 | Drop raro, quest | 500 oro |
| `orbe_vision` | Orbe de Visión | Raro | Revela el contenido de un cofre o habitación antes de entrar. 3 usos. | 3 | Drop, tienda mágica | 200 oro |
| `campana_niebla` | Campana de Niebla | Raro | Crea niebla densa en combate. Todos los enemigos pierden 1 turno. | 1 | Drop, alquimista | 180 oro |
| `espejo_verdad` | Espejo de la Verdad | Épico | Revela la identidad real de NPCs disfrazados o traidores. | 5 | Quest, drop raro | 400 oro |
| `reloj_arena` | Reloj de Arena Mágico | Épico | Pausa el tiempo del mundo por 1 hora de juego. | 1 | Quest especial | — |
| `cubo_almacenaje` | Cubo de Almacenaje | Legendario | Bolsa extradimensional. +20 slots de inventario permanentes. | Infinita | Quest legendaria | — |
| `piedra_afilado` | Piedra de Afilar | Común | +10% daño en el próximo combate. Se consume. | 1 | Tienda, crafteo | 15 oro |
| `aceite_bendito` | Aceite Bendito | Raro | +25% daño contra no-muertos y demonios por 1 combate. | 1 | Templo, alquimista | 80 oro |
| `silbato_bestia` | Silbato de Bestia | Raro | Llama a un animal aliado aleatorio para ayudar en combate. | 3 | Drop, quest | 250 oro |
| `moneda_suerte` | Moneda de la Suerte | Épico | Reroll de cualquier tirada de dados (drop, crafteo, evento). | 5 | Drop raro, quest | 350 oro |

---

## 6. Kits de Reparación y Mantenimiento

| ID | Nombre | Rareza | Efecto | Usos | Cómo Obtener | Valor |
|----|--------|--------|--------|------|--------------|-------|
| `kit_reparacion` | Kit de Reparación | Común | Repara un item al 50% de durabilidad. | 1 | Herrero, tienda | 25 oro |
| `kit_reparacion_avanzado` | Kit de Reparación Avanzado | Raro | Repara un item al 100% de durabilidad. | 1 | Herrero | 80 oro |
| `aceite_mantenimiento` | Aceite de Mantenimiento | Común | Reduce el desgaste de herramientas en un 50% por 10 usos. | 1 | Tienda, crafteo | 20 oro |
| `piedra_amolar` | Piedra de Amolar | Común | Restaura la durabilidad de armas cortantes en +20. | 1 | Tienda, crafteo | 10 oro |

---

## 7. Estructura JSON

### Herramienta
```json
{
  "id": "pico_hierro",
  "nombre": "Pico de Hierro",
  "tipo": "herramienta",
  "subtipo": "recoleccion",
  "rareza": "comun",
  "durabilidad_max": 50,
  "durabilidad_actual": 50,
  "efecto": "minar_basico",
  "descripcion": "Un pico robusto de hierro. Permite extraer minerales básicos de las minas.",
  "peso": 4,
  "valor": 40,
  "stackeable": false,
  "favorito": false
}
```

### Consumible de Utilidad
```json
{
  "id": "bomba_humo",
  "nombre": "Bomba de Humo",
  "tipo": "consumible",
  "subtipo": "bomba",
  "rareza": "comun",
  "efecto": "huida_garantizada",
  "descripcion": "Una pequeña esfera de arcilla rellena de polvo negro. Al romperse, crea una nube de humo que permite escapar de cualquier combate.",
  "peso": 0.5,
  "valor": 30,
  "stackeable": true,
  "stack_max": 10,
  "cantidad": 1,
  "favorito": false
}
```

### Material
```json
{
  "id": "hierro",
  "nombre": "Hierro",
  "tipo": "material",
  "subtipo": "mineral",
  "rareza": "comun",
  "descripcion": "Mineral metálico gris. Base de la mayoría de herramientas y armas.",
  "peso": 1,
  "valor": 5,
  "stackeable": true,
  "stack_max": 50,
  "cantidad": 1
}
```

### Objeto Especial
```json
{
  "id": "amuleto_exploracion",
  "nombre": "Amuleto del Explorador",
  "tipo": "accesorio",
  "subtipo": "amuleto",
  "rareza": "raro",
  "slot_equipo": "amuleto",
  "efectos_pasivos": [
    {"stat": "radio_vision", "valor": 1, "tipo": "suma"},
    {"stat": "xp_cartografia", "valor": 25, "tipo": "porcentaje"}
  ],
  "descripcion": "Un amuleto tallado en madera ancestral con un ojo grabado. Los exploradores lo consideran un símbolo de buena fortuna.",
  "peso": 0.2,
  "valor": 300,
  "stackeable": false,
  "identificado": true,
  "favorito": false
}
```

---

## 8. Recetas de Crafteo

### Herramientas Crafteables

| Resultado | Materiales | Tipo Crafteo | Nivel Requerido |
|-----------|------------|--------------|-----------------|
| Antorcha | Madera x1 + Tela x1 | Básico | 0 |
| Cuerda | Tela x3 | Básico | 0 |
| Pico de Hierro | Hierro x3 + Madera x1 | Herrería | 1 |
| Hacha de Leñador | Hierro x2 + Madera x2 | Herrería | 1 |
| Pala | Hierro x2 + Madera x1 | Herrería | 1 |
| Hoz | Hierro x1 + Madera x1 | Herrería | 1 |
| Trampa de Caza | Hierro x2 + Cuerda x1 | Herrería | 2 |
| Caña de Pescar | Madera x1 + Cuerda x1 | Básico | 0 |
| Linterna de Aceite | Hierro x1 + Cristal x1 | Herrería | 2 |
| Pico de Acero | Acero x3 + Madera x1 | Herrería | 3 |
| Hacha de Acero | Acero x2 + Madera x2 | Herrería | 3 |
| Kit de Primeros Auxilios | Tela x2 + Hierba Curativa x3 | Alquimia | 1 |
| Bomba de Humo | Carbón x2 + Tela x1 | Alquimia | 2 |
| Bomba de Fuego | Cristal Rojo x1 + Carbón x2 | Alquimia | 3 |
| Bomba de Hielo | Cristal de Hielo x1 + Carbón x2 | Alquimia | 3 |
| Bomba de Veneno | Veneno de Serpiente x1 + Carbón x2 | Alquimia | 3 |
| Piedra de Afilar | Piedra x2 | Básico | 0 |
| Aceite de Mantenimiento | Grasa Animal x1 + Sal x1 | Alquimia | 1 |
| Kit de Reparación | Hierro x1 + Tela x1 | Herrería | 1 |

### Comida Crafteable (Requiere Fogata)

| Resultado | Materiales | Tipo Crafteo |
|-----------|------------|--------------|
| Pan | Trigo x2 + Agua x1 | Cocina |
| Carne Asada | Carne Cruda x1 | Cocina |
| Estofado de Aventurero | Carne Cruda x1 + Verdura x1 + Agua x1 | Cocina |
| Festín del Cazador | Carne Cruda x2 + Hierba Curativa x1 + Flor de Stamina x1 | Cocina (receta rara) |
| Té Herbal | Hierba Curativa x1 + Agua x1 | Cocina |

---

## 9. Tabla de Drops por Enemigo

| Enemigo | Drops Posibles | Probabilidad |
|---------|---------------|--------------|
| Lobo | Cuero, Hueso, Carne Cruda | 70% |
| Oso | Cuero Grueso, Hueso, Carne Cruda, Grasa Animal | 80% |
| Serpiente | Veneno de Serpiente, Cuero | 60% |
| Araña Gigante | Seda de Araña, Veneno | 65% |
| Bandido | Hierro, Oro, Ganzúa, Bomba de Humo | 75% |
| Esqueleto | Hueso, Llave de Mazmorra | 50% |
| Demonio | Corazón de Demonio, Gema Morada | 40% |
| Dragón | Escama de Dragón, Hueso de Dragón, Esencia de Dragón | 100% (jefe) |
| Hada | Polvo de Hada, Flor Lunar | 55% |
| Elemental de Hielo | Cristal de Hielo, Cristal Azul | 70% |

---

## 10. Tiendas y Disponibilidad

| Tipo de Tienda | Objetos Disponibles |
|----------------|---------------------|
| **Mercader General** | Antorcha, Cuerda, Yesca, Cantimplora, Saco de Dormir, Comida básica, Ganzúa |
| **Herrero** | Pico, Hacha, Pala, Hoz, Kits de Reparación, Trampa de Caza |
| **Alquimista** | Bombas, Pergaminos básicos, Ingredientes, Aceite de Mantenimiento |
| **Cartógrafo** | Mapa Básico, Mapa Detallado, Brújula, Telescopio, Kit de Cartógrafo |
| **Tienda Mágica** | Antorcha Mágica, Brújula Mágica, Pergaminos raros, Orbe de Visión, Accesorios |
| **Posada** | Comida, Bebida, Saco de Dormir |
| **Templo** | Aceite Bendito, Pergamino de Reparación, Amuletos básicos |
| **Mercader Ambulante** | Items aleatorios, cambia cada visita. Puede tener items épicos. |

---

## Checklist de Implementación

- [ ] Crear `backend/src/data/objetos.json` con todos los items de este catálogo
- [ ] Implementar lógica de herramientas en `backend/src/systems/inventario.py`
- [ ] Implementar drops en `backend/src/systems/combate.py`
- [ ] Implementar crafteo de objetos en `backend/src/systems/crafteo.py`
- [ ] Implementar tiendas con inventario dinámico
- [ ] Conectar herramientas con sistema de exploración (antorcha, cuerda, etc.)
- [ ] Conectar herramientas de recolección con sistema de recursos del mapa
- [ ] UI: Panel de herramienta activa en inventario

---

*Catálogo v1.0 - Last Adventurer*
*Dependencias: SISTEMA_INVENTARIO.md, SISTEMA_RAREZA.md, SISTEMA_CRAFTEO.md, SISTEMA_MAPA.md*
