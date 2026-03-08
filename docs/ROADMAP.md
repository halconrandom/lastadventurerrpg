# Last Adventurer - Roadmap

## Proyecto
RPG para navegador con machine learning progresivo. Desarrollo guiado, código escrito por el usuario.

---

## Fase 0: Configuración del entorno

### Instalar Python
1. Descargar Python desde: https://www.python.org/downloads/
2. Al instalar, **marcar la opción "Add Python to PATH"**
3. Verificar instalación abriendo terminal:
   ```
   python --version
   ```

### Editor de código recomendado
- VS Code (gratuito) con extensión Python
- O PyCharm Community (gratuito)

### Estructura del proyecto
```
lastadventurer/
├── ROADMAP.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── personaje.py
│   │   ├── enemigo.py
│   │   └── item.py
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── combate.py
│   │   └── inventario.py
│   └── data/
│       └── game_data.json
└── tests/
```

---

## Fase 1: RPG en consola (Python puro)

### Objetivos
- [ ] Crear clase `Personaje` con stats básicos
- [ ] Crear clase `Enemigo`
- [ ] Crear clase `Item`
- [ ] Sistema de combate por turnos
- [ ] Inventario simple
- [ ] Loop principal del juego

### Conceptos a aprender
- Clases y objetos (POO)
- Métodos y atributos
- Condicionales y bucles
- Input/output en consola
- Listas y diccionarios

---

## Fase 2: Persistencia de datos

### Objetivos
- [ ] Guardar partida en JSON
- [ ] Cargar partida existente
- [ ] Sistema de guardado automático

### Conceptos a aprender
- Manejo de archivos
- Serialización JSON
- Manejo de errores (try/except)

---

## Fase 3: Versión web

### Objetivos
- [ ] Backend con FastAPI
- [ ] API REST para el juego
- [ ] Frontend básico (HTML/CSS/JS)
- [ ] WebSockets para tiempo real

### Conceptos a aprender
- APIs REST
- FastAPI framework
- JavaScript asíncrono (fetch)
- WebSockets

---

## Fase 4: Machine Learning progresivo

### Objetivos
- [ ] Enemigos que aprenden patrones del jugador
- [ ] Sistema de loot adaptativo
- [ ] NPCs con comportamiento dinámico
- [ ] Dificultad procedural

### Conceptos a aprender
- Algoritmos de ML básicos
- scikit-learn
- Sistemas de recomendación
- Aprendizaje por refuerzo simple

---

## Notas de desarrollo
- Cada fase se desarrolla paso a paso
- El usuario escribe el código con guía
- Commits frecuentes en git
- Testing manual en cada paso

---

## Progreso actual
**Estado:** Fase 0 - Pendiente instalación de Python
**Siguiente paso:** Instalar Python y verificar entorno
