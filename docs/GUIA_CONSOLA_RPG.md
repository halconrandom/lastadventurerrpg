# Guía: RPG en Consola - Last Adventurer

## Objetivo
Crear un juego RPG completo en consola con:
- Menú de inicio
- Creación de personaje con clases
- 10 tipos de objetos
- Exploración y combate
- Guardar/cargar partida

---

## Paso 1: Menú de Inicio

### Archivo a crear: `src/main.py`

### Funcionalidad:
- Mostrar opciones: "Nueva Partida", "Cargar Partida", "Salir"
- Usar `input()` para seleccionar
- Limpiar consola entre pantallas (opcional)

### Pseudocódigo:
```
mostrar_menu():
    while True:
        print "=== LAST ADVENTURER ==="
        print "1. Nueva Partida"
        print "2. Cargar Partida"
        print "3. Salir"
        opcion = input("Selecciona: ")
        
        si opcion == "1":
            crear_personaje()
        si opcion == "2":
            cargar_partida()
        si opcion == "3":
            exit()
```

---

## Paso 2: Creación de Personaje

### Archivo a modificar: `src/main.py` o nuevo `src/game_manager.py`

### Funcionalidad:
- Pedir nombre al jugador
- Elegir clase (afecta stats base)

### Clases propuestas:

| Clase | HP | Ataque | Defensa | Descripción |
|-------|-----|--------|---------|-------------|
| Guerrero | 120 | 18 | 8 | Resistente, alto daño |
| Mago | 70 | 25 | 3 | Frágil, daño devastador |
| Arquero | 90 | 20 | 5 | Balanceado |
| Paladín | 100 | 15 | 10 | Tanque, buena defensa |

### Pseudocódigo:
```
crear_personaje():
    nombre = input("Ingresa tu nombre: ")
    
    print "Elige tu clase:"
    print "1. Guerrero - HP:120 ATK:18 DEF:8"
    print "2. Mago - HP:70 ATK:25 DEF:3"
    print "3. Arquero - HP:90 ATK:20 DEF:5"
    print "4. Paladín - HP:100 ATK:15 DEF:10"
    
    clase = input("Selecciona clase: ")
    
    si clase == "1":
        personaje = Personaje(nombre, 120, 18, 8, 1)
    si clase == "2":
        personaje = Personaje(nombre, 70, 25, 3, 1)
    ...etc
    
    # Dar items iniciales
    personaje.inventario.agregar(Item("Poción Pequeña", "pocion", 20))
    
    return personaje
```

---

## Paso 3: Definir 10 Tipos de Objetos

### Archivo a modificar: `src/data/items.json`

### Tipos de objetos:

| # | Nombre | Tipo | Efecto | Descripción |
|---|--------|------|--------|-------------|
| 1 | Poción Pequeña | pocion | 20 | Cura 20 HP |
| 2 | Poción Grande | pocion | 50 | Cura 50 HP |
| 3 | Poción Máxima | pocion | 100 | Cura 100 HP |
| 4 | Elixir de Vida | pocion | 999 | Cura todo |
| 5 | Espada de Hierro | arma | +5 | Aumenta ataque +5 |
| 6 | Espada de Acero | arma | +10 | Aumenta ataque +10 |
| 7 | Escudo de Madera | armadura | +3 | Aumenta defensa +3 |
| 8 | Armadura de Placas | armadura | +8 | Aumenta defensa +8 |
| 9 | Anillo de Poder | accesorio | +3 ATK/DEF | Aumenta ambos |
| 10 | Poción de Fuerza | buff | +10 ATK temporal | Aumenta ataque en combate |

### JSON a crear:
```json
[
  {"nombre": "Poción Pequeña", "tipo": "pocion", "efecto": 20},
  {"nombre": "Poción Grande", "tipo": "pocion", "efecto": 50},
  {"nombre": "Poción Máxima", "tipo": "pocion", "efecto": 100},
  {"nombre": "Elixir de Vida", "tipo": "pocion", "efecto": 999},
  {"nombre": "Espada de Hierro", "tipo": "arma", "efecto": 5},
  {"nombre": "Espada de Acero", "tipo": "arma", "efecto": 10},
  {"nombre": "Escudo de Madera", "tipo": "armadura", "efecto": 3},
  {"nombre": "Armadura de Placas", "tipo": "armadura", "efecto": 8},
  {"nombre": "Anillo de Poder", "tipo": "accesorio", "efecto": 3},
  {"nombre": "Poción de Fuerza", "tipo": "buff", "efecto": 10}
]
```

---

## Paso 4: Modificar Inventario para Equipamiento

### Archivo a modificar: `src/systems/inventario.py`

### Funcionalidad nueva:
- `equipar(indice, personaje)` - Equipar armas/armaduras
- Los items equipados modifican stats permanentemente
- Solo 1 arma y 1 armadura equipada a la vez

### Pseudocódigo:
```
equipar(self, indice, personaje):
    item = self.items[indice]
    
    si item.tipo == "arma":
        personaje.ataque += item.efecto
        print(f"Equipaste {item.nombre}. ATK +{item.efecto}")
        self.items.pop(indice)
    
    si item.tipo == "armadura":
        personaje.defensa += item.efecto
        print(f"Equipaste {item.nombre}. DEF +{item.efecto}")
        self.items.pop(indice)
```

---

## Paso 5: Definir Enemigos

### Archivo a crear: `src/data/enemigos.json`

### Enemigos por zona:

| Nombre | HP | ATK | DEF | XP | Zona |
|--------|-----|-----|-----|-----|------|
| Slime | 30 | 8 | 2 | 15 | Bosque |
| Lobo | 50 | 12 | 4 | 30 | Bosque |
| Bandido | 70 | 15 | 6 | 50 | Camino |
| Orco | 100 | 20 | 10 | 80 | Cueva |
| Esqueleto | 60 | 18 | 5 | 40 | Cueva |
| Mago Oscuro | 80 | 25 | 3 | 100 | Torre |
| Dragón | 200 | 35 | 20 | 300 | Torre |

---

## Paso 6: Loop Principal del Juego

### Archivo a crear/modificar: `src/game_manager.py`

### Funcionalidad:
- Exploración (elegir zona)
- Encuentros aleatorios
- Tienda (comprar items)
- Ver stats e inventario

### Pseudocódigo:
```
loop_principal(personaje):
    mientras True:
        mostrar_estado(personaje)
        print "¿Qué quieres hacer?"
        print "1. Explorar"
        print "2. Ver Inventario"
        print "3. Ver Stats"
        print "4. Tienda"
        print "5. Guardar"
        print "6. Salir"
        
        opcion = input("> ")
        
        si opcion == "1":
            explorar(personaje)
        si opcion == "2":
            personaje.inventario.mostrar()
            # Opción de usar/equipar
        si opcion == "3":
            mostrar_stats(personaje)
        si opcion == "4":
            tienda(personaje)
        si opcion == "5":
            guardar_partida(personaje)
        si opcion == "6":
            break
```

---

## Paso 7: Sistema de Exploración

### Archivo a crear: `src/systems/exploracion.py`

### Funcionalidad:
- Elegir zona (Bosque, Camino, Cueva, Torre)
- Probabilidad de encuentro aleatorio
- Enemigos según zona

### Pseudocódigo:
```
explorar(personaje):
    print "Elige zona:"
    print "1. Bosque (Nivel 1-3)"
    print "2. Camino (Nivel 3-5)"
    print "3. Cueva (Nivel 5-8)"
    print "4. Torre (Nivel 8+)"
    
    zona = input("> ")
    
    # Probabilidad de encuentro (70%)
    si random.random() < 0.7:
        enemigo = generar_enemigo_aleatorio(zona)
        combate = CombatSystem(personaje, enemigo)
        combate.iniciar_combate()
    sino:
        print "No encuentras nada..."
```

---

## Paso 8: Sistema de Guardado

### Archivo a crear: `src/systems/guardado.py`

### Funcionalidad:
- Guardar personaje en JSON
- Cargar personaje desde JSON

### Datos a guardar:
```json
{
  "nombre": "Arthur",
  "clase": "Guerrero",
  "hp": 120,
  "hp_max": 120,
  "ataque": 18,
  "defensa": 8,
  "nivel": 5,
  "experiencia": 250,
  "inventario": [
    {"nombre": "Poción Pequeña", "tipo": "pocion", "efecto": 20}
  ]
}
```

### Pseudocódigo:
```
guardar(personaje):
    datos = {
        "nombre": personaje.nombre,
        "hp": personaje.hp,
        "hp_max": personaje.hp_max,
        ...
    }
    with open("data/guardado.json", "w") as f:
        json.dump(datos, f)
    print "Partida guardada"

cargar():
    with open("data/guardado.json", "r") as f:
        datos = json.load(f)
    # Reconstruir personaje desde datos
    personaje = Personaje(...)
    return personaje
```

---

## Paso 9: Tienda

### Archivo a crear: `src/systems/tienda.py`

### Funcionalidad:
- Mostrar items disponibles
- Comprar con oro (nuevo atributo en Personaje)
- Los enemigos sueltan oro al morir

---

## Orden de implementación sugerido:

1. ✅ Menú de inicio
2. ✅ Creación de personaje con clases
3. ✅ Actualizar `items.json` con 10 objetos
4. ✅ Modificar inventario para equipar
5. ✅ Crear `enemigos.json`
6. ✅ Loop principal del juego
7. ✅ Sistema de exploración
8. ✅ Sistema de guardado
9. ✅ Tienda (opcional)

---

## Notas:

- Usa `import random` para encuentros aleatorios
- Usa `import os` y `os.system('cls')` para limpiar consola en Windows
- Prueba cada paso antes de avanzar al siguiente
- Haz commits en git después de cada paso

---

## Entregable:

Cuando termines cada paso, avísame y revisamos juntos. ¡Tú puedes!
