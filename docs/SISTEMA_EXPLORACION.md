# Sistema de Exploración Procedural

## Filosofía de Diseño

> *"El mundo no recuerda tu paso anterior. Cada viaje es único, cada descubrimiento irrepetible."*

Inspirado en **Dwarf Fortress**, **Caves of Qud**, y **CDDA**. El objetivo es crear un sistema donde:

1. **Nada es estático** - El mundo cambia entre partidas
2. **Emergencia narrativa** - Historias surgen de sistemas, no de scripts
3. **Memoria del mundo** - El mundo recuerda y reacciona
4. **Descubrimiento genuino** - El jugador explora lo desconocido, no lo prediseñado

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    MUNDO (World State)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Semilla   │  │   Tiempo    │  │  Historia Global    │  │
│  │   (Seed)    │  │   (Tick)    │  │  (Eventos Pasados)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  GENERADOR PROCEDURAL                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Biomas    │  │   Regiones  │  │    Puntos de        │  │
│  │   Clima     │  │   Facciones │  │    Interés (POI)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ZONA ACTUAL                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Tiles     │  │   Entidades │  │    Eventos          │  │
│  │   Mapa      │  │   NPCs      │  │    Dinámicos        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Sistema de Semillas (Seed)

### Concepto
Cada partida tiene una semilla única que determina TODO el mundo. Misma semilla = mismo mundo.

### Implementación

```python
import random
from hashlib import sha256

class WorldSeed:
    """Generador determinista basado en semilla"""
    
    def __init__(self, seed_string: str = None):
        self.master_seed = seed_string or self._generate_seed()
        self.rng = random.Random(self._hash_seed(self.master_seed))
        self.subseed_cache = {}
    
    def _hash_seed(self, seed: str) -> int:
        """Convierte string a hash numérico"""
        return int(sha256(seed.encode()).hexdigest(), 16) % (2**32)
    
    def get_subseed(self, context: str) -> int:
        """Genera sub-seeds para diferentes sistemas"""
        if context not in self.subseed_cache:
            combined = f"{self.master_seed}:{context}"
            self.subseed_cache[context] = self._hash_seed(combined)
        return self.subseed_cache[context]
    
    def get_rng(self, context: str) -> random.Random:
        """RNG independiente para cada sistema"""
        return random.Random(self.get_subseed(context))
    
    def _generate_seed(self) -> str:
        """Genera semilla aleatoria"""
        import time
        import uuid
        return f"{time.time()}:{uuid.uuid4()}"
```

### Uso

```python
# Cada sistema tiene su propio RNG determinista
world = WorldSeed("mi-partida-123")

bioma_rng = world.get_rng("biomas")      # Para generar biomas
enemigo_rng = world.get_rng("enemigos")  # Para generar enemigos
tesoro_rng = world.get_rng("tesoros")    # Para generar tesoros

# Siempre mismo resultado con misma semilla
print(bioma_rng.choice(["bosque", "desierto", "pantano"]))  # Determinista
```

---

## 2. Sistema de Biomas

### Biomas Base

| Bioma | Terreno | Clima | Recursos | Peligros |
|-------|---------|-------|----------|----------|
| **Bosque Ancestral** | Denso, húmedo | Lluvioso | Madera, hierbas | Lobos, bandidos |
| **Páramo Marchito** | Árido, polvoriento | Seco | Piedra, metales | No-muertos |
| **Pantano Sombrío** | Ciénaga, neblina | Húmedo | Hongos, venenos | Criaturas ácidas |
| **Montañas Heladas** | Rocosos, nevado | Frío extremo | Minerales raros | Yetis, avalanchas |
| **Desierto de Ceniza** | Volcánico, tóxico | Caliente | Obsidiana, azufre | Demonios menores |
| **Ruinas Subterráneas** | Piedra antigua | Estable | Artefactos | Constructos |

### Generación de Biomas

```python
class BiomaGenerator:
    """Genera biomas procedurales"""
    
    BIOMAS = {
        "bosque_ancestral": {
            "nombre": "Bosque Ancestral",
            "color": "#2d5a27",
            "terreno_base": ["densa_vegetacion", "arboles_antiguos", "claros"],
            "clima": ["lluvia", "niebla", "templado"],
            "recursos": ["madera_antigua", "hierbas_raras", "bayas"],
            "fauna": ["lobos", "ciervos", "osos", "hadas"],
            "peligros": ["trampas_naturales", "lobos_hambrientos"],
            "eventos": ["encuentro_viajero", "ruinas_ocultas", "claro_mistico"]
        },
        "paramo_marchito": {
            "nombre": "Páramo Marchito",
            "color": "#4a4a3a",
            "terreno_base": ["tierra_yerma", "tumbas_antiguas", "niebla"],
            "clima": ["seco", "ventoso", "noches_frias"],
            "recursos": ["piedra", "huesos", "metales_oxidados"],
            "fauna": ["no_muertos", "cuervos", "sombras"],
            "peligros": ["tumbas_profanadas", "niebla_venenosa"],
            "eventos": ["procesion_fantasma", "tumba_abierta", "viajero_perdido"]
        },
        # ... más biomas
    }
    
    def __init__(self, seed: WorldSeed):
        self.rng = seed.get_rng("biomas")
    
    def generar_bioma(self, coordenadas: tuple) -> dict:
        """Genera un bioma único basado en coordenadas"""
        x, y = coordenadas
        
        # Usar coordenadas como parte del seed
        local_seed = hash((x, y, self.rng.randint(0, 1000000)))
        local_rng = random.Random(local_seed)
        
        # Seleccionar bioma base con pesos
        bioma_key = local_rng.choice(list(self.BIOMAS.keys()))
        bioma_base = self.BIOMAS[bioma_key].copy()
        
        # Variaciones únicas
        bioma_base["variacion"] = self._generar_variacion(local_rng, bioma_key)
        bioma_base["nombre_unico"] = self._generar_nombre(local_rng, bioma_base)
        bioma_base["coordenadas"] = coordenadas
        
        return bioma_base
    
    def _generar_variacion(self, rng, bioma_key: str) -> dict:
        """Genera variaciones únicas del bioma"""
        variaciones = {
            "bosque_ancestral": [
                {"tipo": "encantado", "modificador": "magia +20%"},
                {"tipo": "corrupto", "modificador": "enemigos +30%"},
                {"tipo": "antiguo", "modificador": "tesoros +15%"},
            ],
            "paramo_marchito": [
                {"tipo": "maldito", "modificador": "no_muertos +40%"},
                {"tipo": "olvidado", "modificador": "secretos +25%"},
                {"tipo": "sagrado", "modificador": "reliquias +10%"},
            ],
        }
        return rng.choice(variaciones.get(bioma_key, [{"tipo": "normal", "modificador": "ninguno"}]))
    
    def _generar_nombre(self, rng, bioma: dict) -> str:
        """Genera nombre único para la zona"""
        prefijos = ["El", "Los", "Las", "Aquellas"]
        adjetivos = ["Olvidados", "Susurrantes", "Eternos", "Marchitos", "Vivientes"]
        sustantivos = bioma["terreno_base"]
        
        if rng.random() > 0.7:  # 30% de nombres especiales
            return f"{rng.choice(prefijos)} {rng.choice(sustantivos).title()} {rng.choice(adjetivos)}"
        return bioma["nombre"]
```

---

## 3. Sistema de Regiones y Mapa

### Estructura del Mundo

```
MUNDO
├── Región Norte (fría, montañosa)
│   ├── Zona A1 (Montañas Heladas)
│   ├── Zona A2 (Bosque Nevado)
│   └── Zona A3 (Cueva de Hielo)
├── Región Central (templada)
│   ├── Zona B1 (Bosque Ancestral)
│   ├── Zona B2 (Praderas)
│   └── Zona B3 (Ruinas Antiguas)
├── Región Sur (árida)
│   ├── Zona C1 (Desierto de Ceniza)
│   ├── Zona C2 (Páramo Marchito)
│   └── Zona C3 (Oasis Escondido)
└── Región Subterránea
    ├── Zona D1 (Cuevas Profundas)
    ├── Zona D2 (Ruinas Enanas)
    └── Zona D3 (Abismo)
```

### Generación de Mapa

```python
class WorldMap:
    """Mapa mundial procedural"""
    
    def __init__(self, seed: WorldSeed, tamaño: int = 100):
        self.seed = seed
        self.tamaño = tamaño
        self.zonas = {}
        self.zonas_descubiertas = set()
        self.zona_actual = None
        
        # Generar mapa completo (lazy - solo cuando se necesita)
        self._generar_regiones()
    
    def _generar_regiones(self):
        """Genera la estructura regional del mundo"""
        rng = self.seed.get_rng("regiones")
        
        # Usar Perlin noise para continuidad
        # Zonas adyacentes tienden a ser similares
        self.noise_map = self._generar_noise_map()
    
    def _generar_noise_map(self) -> list:
        """Genera mapa de ruido para continuidad de biomas"""
        # Simplificación - en producción usar librería de noise
        rng = self.seed.get_rng("noise")
        return [[rng.random() for _ in range(self.tamaño)] for _ in range(self.tamaño)]
    
    def obtener_zona(self, x: int, y: int) -> 'Zona':
        """Obtiene o genera una zona específica"""
        coords = (x, y)
        
        if coords not in self.zonas:
            self.zonas[coords] = Zona.generar(self.seed, coords, self.noise_map)
        
        return self.zonas[coords]
    
    def explorar_adyacente(self, direccion: str) -> 'Zona':
        """Mueve al jugador a una zona adyacente"""
        x, y = self.zona_actual.coordenadas if self.zona_actual else (50, 50)
        
        movimientos = {
            "norte": (0, -1),
            "sur": (0, 1),
            "este": (1, 0),
            "oeste": (-1, 0)
        }
        
        dx, dy = movimientos.get(direccion, (0, 0))
        nueva_zona = self.obtener_zona(x + dx, y + dy)
        
        self.zona_actual = nueva_zona
        self.zonas_descubiertas.add((x + dx, y + dy))
        
        return nueva_zona
```

---

## 4. Sistema de Zonas (Tiles)

### Estructura de una Zona

```python
class Zona:
    """Una zona explorable del mapa"""
    
    def __init__(self, seed: WorldSeed, coordenadas: tuple, bioma: dict):
        self.seed = seed
        self.coordenadas = coordenadas
        self.bioma = bioma
        self.nombre = bioma["nombre_unico"]
        
        # Generación procedural
        self.tiles = []           # Mapa de tiles
        self.entidades = []      # NPCs, enemigos, objetos
        self.eventos = []        # Eventos disponibles
        self.poi = []            # Puntos de interés
        
        # Estado dinámico
        self.visitada = False
        self.veces_explorada = 0
        self.estado = "inexplorada"  # inexplorada, explorando, agotada
    
    @classmethod
    def generar(cls, seed: WorldSeed, coordenadas: tuple, noise_map: list) -> 'Zona':
        """Genera una zona completa"""
        rng = seed.get_rng(f"zona_{coordenadas}")
        
        # Determinar bioma basado en noise
        bioma_gen = BiomaGenerator(seed)
        bioma = bioma_gen.generar_bioma(coordenadas)
        
        zona = cls(seed, coordenadas, bioma)
        
        # Generar contenido
        zona._generar_tiles(rng)
        zona._generar_entidades(rng)
        zona._generar_poi(rng)
        zona._generar_eventos(rng)
        
        return zona
    
    def _generar_tiles(self, rng):
        """Genera el mapa de tiles de la zona"""
        tamaño = rng.randint(20, 40)  # Zonas de tamaño variable
        
        self.tiles = []
        for y in range(tamaño):
            fila = []
            for x in range(tamaño):
                tile = self._generar_tile(rng, x, y, tamaño)
                fila.append(tile)
            self.tiles.append(fila)
    
    def _generar_tile(self, rng, x: int, y: int, tamaño: int) -> dict:
        """Genera un tile individual"""
        terrenos = self.bioma["terreno_base"]
        terreno = rng.choice(terrenos)
        
        # Probabilidad de tiles especiales
        especial = None
        if rng.random() < 0.05:  # 5% tiles especiales
            especial = rng.choice(["tesoro_menor", "trampa", "secreto", "evento"])
        
        return {
            "x": x,
            "y": y,
            "terreno": terreno,
            "especial": especial,
            "explorado": False,
            "entidad": None
        }
    
    def _generar_entidades(self, rng):
        """Genera NPCs y enemigos en la zona"""
        fauna = self.bioma.get("fauna", [])
        peligros = self.bioma.get("peligros", [])
        
        # Número de entidades basado en bioma y variación
        num_hostiles = rng.randint(2, 8)
        num_neutrales = rng.randint(1, 5)
        
        for _ in range(num_hostiles):
            if peligros and rng.random() > 0.3:
                tipo = rng.choice(peligros)
            else:
                tipo = rng.choice(fauna) if fauna else "criatura_desconocida"
            
            self.entidades.append({
                "tipo": tipo,
                "hostil": True,
                "nivel": self._calcular_nivel(rng),
                "posicion": (rng.randint(0, 39), rng.randint(0, 39))
            })
        
        for _ in range(num_neutrales):
            tipo = rng.choice(fauna) if fauna else "criatura_neutral"
            self.entidades.append({
                "tipo": tipo,
                "hostil": False,
                "nivel": self._calcular_nivel(rng),
                "posicion": (rng.randint(0, 39), rng.randint(0, 39))
            })
    
    def _generar_poi(self, rng):
        """Genera puntos de interés"""
        num_poi = rng.randint(1, 5)
        
        tipos_poi = {
            "bosque_ancestral": ["claro_mistico", "arbol_sagrado", "cabaña_abandonada", "ruinas_cubiertas"],
            "paramo_marchito": ["tumba_antigua", "altar_olvidado", "cementerio", "torre_derruida"],
            # ... más biomas
        }
        
        poi_bioma = tipos_poi.get(self.bioma.get("key", ""), ["punto_generico"])
        
        for _ in range(num_poi):
            self.poi.append({
                "tipo": rng.choice(poi_bioma),
                "descubierto": False,
                "posicion": (rng.randint(0, 39), rng.randint(0, 39))
            })
    
    def _generar_eventos(self, rng):
        """Genera eventos disponibles en la zona"""
        eventos_bioma = self.bioma.get("eventos", [])
        num_eventos = rng.randint(0, 3)
        
        for _ in range(num_eventos):
            if eventos_bioma:
                self.eventos.append({
                    "tipo": rng.choice(eventos_bioma),
                    "disponible": True,
                    "resuelto": False
                })
    
    def _calcular_nivel(self, rng) -> int:
        """Calcula nivel de entidades basado en distancia al centro"""
        x, y = self.coordenadas
        distancia_centro = abs(x - 50) + abs(y - 50)
        nivel_base = max(1, distancia_centro // 10)
        return nivel_base + rng.randint(-1, 2)
    
    def explorar(self) -> dict:
        """Ejecuta una acción de exploración"""
        self.visitada = True
        self.veces_explorada += 1
        
        # Resultados posibles
        resultados = []
        
        # Descubrir tiles
        tiles_descubiertos = self._descubrir_tiles()
        resultados.extend(tiles_descubiertos)
        
        # Encuentros
        encuentros = self._generar_encuentros()
        resultados.extend(encuentros)
        
        # Eventos
        eventos = self._activar_evento()
        if eventos:
            resultados.append(eventos)
        
        # Actualizar estado
        if self.veces_explorada > 5:
            self.estado = "agotada"
        else:
            self.estado = "explorando"
        
        return {
            "zona": self.nombre,
            "resultados": resultados,
            "estado": self.estado
        }
    
    def _descubrir_tiles(self) -> list:
        """Descubre tiles aleatorios"""
        descubiertos = []
        rng = self.seed.get_rng(f"explorar_{self.coordenadas}_{self.veces_explorada}")
        
        num_descubrir = rng.randint(3, 8)
        for _ in range(num_descubrir):
            x, y = rng.randint(0, len(self.tiles)-1), rng.randint(0, len(self.tiles[0])-1)
            tile = self.tiles[y][x]
            if not tile["explorado"]:
                tile["explorado"] = True
                descubiertos.append({
                    "tipo": "tile_descubierto",
                    "terreno": tile["terreno"],
                    "especial": tile["especial"]
                })
        
        return descubiertos
    
    def _generar_encuentros(self) -> list:
        """Genera encuentros con entidades"""
        encuentros = []
        rng = self.seed.get_rng(f"encuentros_{self.coordenadas}_{self.veces_explorada}")
        
        # Probabilidad de encuentro
        if rng.random() < 0.4:  # 40% probabilidad
            entidades_activas = [e for e in self.entidades if e.get("activo", True)]
            if entidades_activas:
                entidad = rng.choice(entidades_activas)
                encuentros.append({
                    "tipo": "encuentro",
                    "entidad": entidad["tipo"],
                    "hostil": entidad["hostil"],
                    "nivel": entidad["nivel"]
                })
        
        return encuentros
    
    def _activar_evento(self) -> dict:
        """Activa un evento de zona"""
        eventos_disponibles = [e for e in self.eventos if e["disponible"] and not e["resuelto"]]
        
        if eventos_disponibles:
            rng = self.seed.get_rng(f"eventos_{self.coordenadas}_{self.veces_explorada}")
            evento = rng.choice(eventos_disponibles)
            evento["disponible"] = False
            
            return {
                "tipo": "evento",
                "evento": evento["tipo"]
            }
        
        return None
```

---

## 5. Sistema de Eventos Dinámicos

### Tipos de Eventos

```python
class EventoManager:
    """Gestor de eventos procedurales"""
    
    EVENTOS_BASE = {
        # Eventos de exploración
        "encuentro_viajero": {
            "tipo": "npc",
            "descripcion": "Un viajero solitario aparece en el camino...",
            "opciones": ["hablar", "ignorar", "atacar"],
            "consecuencias": {
                "hablar": {"reputacion": 1, "info": True},
                "ignorar": {},
                "atacar": {"reputacion": -5, "combate": True}
            }
        },
        "ruinas_ocultas": {
            "tipo": "lugar",
            "descripcion": "Entre la maleza, descubres ruinas antiguas...",
            "opciones": ["explorar", "saquear", "ignorar"],
            "consecuencias": {
                "explorar": {"tesoro": True, "peligro": 0.3},
                "saquear": {"oro": "2d10", "peligro": 0.6},
                "ignorar": {}
            }
        },
        "claro_mistico": {
            "tipo": "misterio",
            "descripcion": "Un claro extrañamente iluminado emite un brillo sobrenatural...",
            "opciones": ["entrar", "observar", "huir"],
            "consecuencias": {
                "entrar": {"magia": 5, "locura": 0.2},
                "observar": {"sabiduria": 1},
                "huir": {}
            }
        },
        "procesion_fantasma": {
            "tipo": "sobrenatural",
            "descripcion": "Una procesión de espectros cruza el camino...",
            "opciones": ["observar", "unirse", "huir"],
            "consecuencias": {
                "observar": {"sabiduria": 2, "maldicion": 0.1},
                "unirse": {"muerte": 0.5, "poder": 10},
                "huir": {"estamina": -10}
            }
        },
        # ... más eventos
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.rng = seed.get_rng("eventos")
        self.historial_eventos = []
    
    def generar_evento(self, contexto: dict) -> dict:
        """Genera un evento único basado en contexto"""
        bioma = contexto.get("bioma", "generico")
        nivel_jugador = contexto.get("nivel", 1)
        
        # Filtrar eventos por bioma
        eventos_bioma = self._filtrar_por_bioma(bioma)
        
        # Seleccionar evento
        evento_key = self.rng.choice(eventos_bioma)
        evento_base = self.EVENTOS_BASE[evento_key].copy()
        
        # Variar evento
        evento = self._variar_evento(evento_base, nivel_jugador)
        evento["id"] = f"{evento_key}_{len(self.historial_eventos)}"
        
        self.historial_eventos.append(evento)
        return evento
    
    def _filtrar_por_bioma(self, bioma: str) -> list:
        """Filtra eventos apropiados para el bioma"""
        eventos_por_bioma = {
            "bosque_ancestral": ["encuentro_viajero", "ruinas_ocultas", "claro_mistico"],
            "paramo_marchito": ["procesion_fantasma", "tumba_abierta", "viajero_perdido"],
            # ... más biomas
        }
        return eventos_por_bioma.get(bioma, list(self.EVENTOS_BASE.keys()))
    
    def _variar_evento(self, evento: dict, nivel: int) -> dict:
        """Añade variaciones únicas al evento"""
        # Modificar dificultades basado en nivel
        if "consecuencias" in evento:
            for opcion, consecuencias in evento["consecuencias"].items():
                if "peligro" in consecuencias:
                    consecuencias["peligro"] = min(0.9, consecuencias["peligro"] + nivel * 0.02)
        
        # Añadir flavor text único
        adjetivos = ["inesperado", "misterioso", "perturbador", "fascinante"]
        evento["descripcion"] = f"Un {self.rng.choice(adjetivos)} encuentro: {evento['descripcion']}"
        
        return evento
    
    def resolver_evento(self, evento_id: str, opcion: str, personaje: dict) -> dict:
        """Resuelve un evento y aplica consecuencias"""
        evento = next((e for e in self.historial_eventos if e["id"] == evento_id), None)
        
        if not evento:
            return {"error": "Evento no encontrado"}
        
        consecuencias = evento["consecuencias"].get(opcion, {})
        resultado = self._aplicar_consecuencias(consecuencias, personaje)
        
        return {
            "evento": evento["tipo"],
            "opcion": opcion,
            "resultado": resultado
        }
    
    def _aplicar_consecuencias(self, consecuencias: dict, personaje: dict) -> dict:
        """Aplica las consecuencias al personaje"""
        resultado = {"cambios": {}, "mensajes": []}
        
        for key, valor in consecuencias.items():
            if key == "oro":
                cantidad = self._tirar_dado(valor) if isinstance(valor, str) else valor
                personaje["oro"] = personaje.get("oro", 0) + cantidad
                resultado["cambios"]["oro"] = cantidad
                resultado["mensajes"].append(f"Obtienes {cantidad} de oro.")
            
            elif key == "experiencia":
                personaje["experiencia"] = personaje.get("experiencia", 0) + valor
                resultado["cambios"]["experiencia"] = valor
            
            elif key == "peligro":
                if self.rng.random() < valor:
                    resultado["mensajes"].append("¡Algo sale mal!")
                    resultado["peligro_activado"] = True
            
            elif key == "combate":
                resultado["iniciar_combate"] = True
            
            # ... más consecuencias
        
        return resultado
    
    def _tirar_dado(self, notacion: str) -> int:
        """Tira dados usando notación d20 (ej: '2d10' = 2 dados de 10 caras)"""
        import re
        match = re.match(r"(\d+)d(\d+)", notacion)
        if match:
            num_dados = int(match.group(1))
            caras = int(match.group(2))
            return sum(self.rng.randint(1, caras) for _ in range(num_dados))
        return 0
```

---

## 6. Sistema de Generación de Enemigos

### Enemigos Procedurales

```python
class EnemigoGenerator:
    """Genera enemigos únicos proceduralmente"""
    
    # Plantillas base
    PLANTILLAS = {
        "lobo": {
            "nombre_base": "Lobo",
            "stats_base": {"hp": 20, "ataque": 5, "defensa": 2, "velocidad": 8},
            "habilidades": ["mordisco", "aullido"],
            "botin": {"oro": "1d5", "piel": 0.3}
        },
        "bandido": {
            "nombre_base": "Bandido",
            "stats_base": {"hp": 30, "ataque": 7, "defensa": 4, "velocidad": 5},
            "habilidades": ["tajo", "robar"],
            "botin": {"oro": "2d10", "arma": 0.1}
        },
        "no_muerto": {
            "nombre_base": "No-Muerto",
            "stats_base": {"hp": 40, "ataque": 6, "defensa": 3, "velocidad": 3},
            "habilidades": ["toque_pestilente", "regeneracion"],
            "botin": {"oro": "1d20", "hueso": 0.5}
        },
        # ... más plantillas
    }
    
    # Modificadores únicos
    MODIFICADORES = {
        "ancestral": {"prefijo": "Ancestral", "stats": {"hp": 1.5, "ataque": 1.3}},
        "corrupto": {"prefijo": "Corrupto", "stats": {"ataque": 1.5}, "habilidad_extra": "veneno"},
        "gigante": {"sufijo": "Gigante", "stats": {"hp": 2.0, "velocidad": 0.7}},
        "espectral": {"prefijo": "Espectral", "stats": {"defensa": 0}, "inmune": ["fisico"]},
        "albino": {"prefijo": "Albino", "stats": {"velocidad": 1.3}, "botin_extra": 2.0},
        "legendario": {"prefijo": "Legendario", "stats": {"hp": 2.0, "ataque": 1.5, "defensa": 1.5}},
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.rng = seed.get_rng("enemigos")
    
    def generar_enemigo(self, nivel_zona: int, bioma: str) -> dict:
        """Genera un enemigo único"""
        # Seleccionar plantilla base
        plantilla_key = self._seleccionar_plantilla(bioma)
        plantilla = self.PLANTILLAS[plantilla_key].copy()
        
        # Aplicar nivel
        enemigo = self._escalar_por_nivel(plantilla, nivel_zona)
        
        # Posible modificador único
        if self.rng.random() < 0.2:  # 20% de enemigos especiales
            modificador = self.rng.choice(list(self.MODIFICADORES.keys()))
            enemigo = self._aplicar_modificador(enemigo, modificador)
        
        # Generar nombre único
        enemigo["nombre"] = self._generar_nombre(enemigo)
        enemigo["id"] = self._generar_id()
        
        return enemigo
    
    def _seleccionar_plantilla(self, bioma: str) -> str:
        """Selecciona plantilla apropiada para el bioma"""
        bioma_enemigos = {
            "bosque_ancestral": ["lobo", "bandido", "oso"],
            "paramo_marchito": ["no_muerto", "espectro", "esqueleto"],
            "montañas_heladas": ["yeti", "lobo_nevado", "gigante_hielo"],
            # ... más biomas
        }
        opciones = bioma_enemigos.get(bioma, list(self.PLANTILLAS.keys()))
        return self.rng.choice(opciones)
    
    def _escalar_por_nivel(self, plantilla: dict, nivel: int) -> dict:
        """Escala stats basado en nivel de zona"""
        multiplicador = 1 + (nivel - 1) * 0.15
        
        stats = plantilla["stats_base"].copy()
        for stat, valor in stats.items():
            stats[stat] = int(valor * multiplicador)
        
        return {
            **plantilla,
            "stats": stats,
            "nivel": nivel
        }
    
    def _aplicar_modificador(self, enemigo: dict, modificador_key: str) -> dict:
        """Aplica un modificador único"""
        mod = self.MODIFICADORES[modificador_key]
        
        # Aplicar stats
        for stat, mult in mod.get("stats", {}).items():
            if stat in enemigo["stats"]:
                enemigo["stats"][stat] = int(enemigo["stats"][stat] * mult)
        
        # Añadir prefijo/sufijo
        if "prefijo" in mod:
            enemigo["prefijo"] = mod["prefijo"]
        if "sufijo" in mod:
            enemigo["sufijo"] = mod["sufijo"]
        
        # Habilidad extra
        if "habilidad_extra" in mod:
            enemigo["habilidades"].append(mod["habilidad_extra"])
        
        # Inmunidades
        if "inmune" in mod:
            enemigo["inmune"] = mod["inmune"]
        
        enemigo["modificador"] = modificador_key
        enemigo["especial"] = True
        
        return enemigo
    
    def _generar_nombre(self, enemigo: dict) -> str:
        """Genera nombre completo del enemigo"""
        partes = []
        
        if "prefijo" in enemigo:
            partes.append(enemigo["prefijo"])
        
        partes.append(enemigo["nombre_base"])
        
        if "sufijo" in enemigo:
            partes.append(enemigo["sufijo"])
        
        return " ".join(partes)
    
    def _generar_id(self) -> str:
        """Genera ID único para el enemigo"""
        import uuid
        return f"enemy_{uuid.uuid4().hex[:8]}"
```

---

## 7. Sistema de Tesoros Procedurales

### Generación de Botín

```python
class TesoroGenerator:
    """Genera tesoros y botín procedural"""
    
    CALIDADES = {
        "comun": {"color": "#9a978a", "mult": 1.0},
        "poco_comun": {"color": "#22c55e", "mult": 1.5},
        "raro": {"color": "#3b82f6", "mult": 2.0},
        "epico": {"color": "#a855f7", "mult": 3.0},
        "legendario": {"color": "#d4a843", "mult": 5.0}
    }
    
    TIPOS_TESORO = {
        "oro": {"peso": 50, "min": 1, "max": 100},
        "pocion": {"peso": 20, "tipos": ["vida", "mana", "stamina"]},
        "arma": {"peso": 10, "niveles": ["comun", "poco_comun", "raro"]},
        "armadura": {"peso": 10, "niveles": ["comun", "poco_comun"]},
        "accesorio": {"peso": 5, "niveles": ["raro", "epico"]},
        "material": {"peso": 15, "tipos": ["madera", "metal", "gema", "tela"]},
        "libro": {"peso": 3, "tipos": ["habilidad", "historia", "mapa"]},
        "artefacto": {"peso": 1, "niveles": ["epico", "legendario"]}
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.rng = seed.get_rng("tesoros")
    
    def generar_botin(self, nivel: int, tipo_enemigo: str = None) -> list:
        """Genera botín basado en nivel y contexto"""
        botin = []
        
        # Número de items
        num_items = self.rng.randint(0, 3) + (1 if nivel > 5 else 0)
        
        for _ in range(num_items):
            item = self._generar_item(nivel, tipo_enemigo)
            if item:
                botin.append(item)
        
        # Oro garantizado
        oro_base = nivel * self.rng.randint(2, 5)
        botin.append({
            "tipo": "oro",
            "cantidad": oro_base,
            "calidad": "comun"
        })
        
        return botin
    
    def _generar_item(self, nivel: int, tipo_enemigo: str) -> dict:
        """Genera un item individual"""
        # Seleccionar tipo de tesoro
        tipos = list(self.TIPOS_TESORO.keys())
        pesos = [self.TIPOS_TESORO[t]["peso"] for t in tipos]
        tipo = self.rng.choices(tipos, weights=pesos)[0]
        
        # Determinar calidad
        calidad = self._determinar_calidad(nivel)
        
        # Generar item específico
        item = {
            "tipo": tipo,
            "calidad": calidad,
            "nivel": nivel,
            "stats": self._generar_stats_item(tipo, calidad, nivel)
        }
        
        # Nombre procedural
        item["nombre"] = self._generar_nombre_item(item)
        
        return item
    
    def _determinar_calidad(self, nivel: int) -> str:
        """Determina la calidad del item"""
        # Probabilidades basadas en nivel
        probs = {
            "comun": max(50 - nivel * 2, 20),
            "poco_comun": 25 + nivel,
            "raro": 15 + nivel // 2,
            "epico": 5 + nivel // 5,
            "legendario": nivel // 10
        }
        
        calidades = list(probs.keys())
        pesos = list(probs.values())
        
        return self.rng.choices(calidades, weights=pesos)[0]
    
    def _generar_stats_item(self, tipo: str, calidad: str, nivel: int) -> dict:
        """Genera stats del item"""
        mult = self.CALIDADES[calidad]["mult"]
        
        stats_base = {}
        
        if tipo == "arma":
            stats_base = {
                "ataque": int((5 + nivel * 2) * mult),
                "velocidad": self.rng.randint(-2, 2),
                "critico": self.rng.randint(0, int(5 * mult))
            }
        elif tipo == "armadura":
            stats_base = {
                "defensa": int((3 + nivel) * mult),
                "hp_extra": int(nivel * 5 * mult)
            }
        elif tipo == "pocion":
            stats_base = {
                "curacion": int((20 + nivel * 5) * mult)
            }
        elif tipo == "accesorio":
            stats_base = {
                "bonus": self.rng.choice(["ataque", "defensa", "velocidad", "critico"]),
                "valor": int(nivel * mult)
            }
        
        return stats_base
    
    def _generar_nombre_item(self, item: dict) -> str:
        """Genera nombre procedural para el item"""
        prefijos = {
            "comun": ["Viejo", "Gastado", "Simple"],
            "poco_comun": ["Decente", "Aceptable", "Bueno"],
            "raro": ["Superior", "Refinado", "Notable"],
            "epico": ["Excepcional", "Magnífico", "Glorioso"],
            "legendario": ["Legendario", "Mítico", "Divino"]
        }
        
        nombres_tipo = {
            "arma": ["Espada", "Hacha", "Daga", "Arco", "Bastón"],
            "armadura": ["Coraza", "Cota", "Túnica", "Armadura"],
            "pocion": ["Poción", "Elixir", "Brebaje"],
            "accesorio": ["Anillo", "Amuleto", "Talismán"],
            "material": ["Fragmento", "Pieza", "Trozo"],
            "libro": ["Tomo", "Manual", "Grimorio"],
            "artefacto": ["Reliquia", "Artefacto", "Reliquia"]
        }
        
        prefijo = self.rng.choice(prefijos.get(item["calidad"], [""]))
        nombre_base = self.rng.choice(nombres_tipo.get(item["tipo"], ["Objeto"]))
        
        return f"{prefijo} {nombre_base}"
```

---

## 8. Sistema de Clima Dinámico

### Clima que Afecta Gameplay

```python
class ClimaSystem:
    """Sistema de clima dinámico"""
    
    CLIMAS = {
        "despejado": {
            "modificadores": {},
            "visibilidad": 1.0,
            "eventos_extra": 0
        },
        "lluvia": {
            "modificadores": {"velocidad": -0.1, "evasion": 0.1},
            "visibilidad": 0.7,
            "eventos_extra": 0.1
        },
        "tormenta": {
            "modificadores": {"velocidad": -0.3, "ataque": -0.1},
            "visibilidad": 0.4,
            "eventos_extra": 0.3,
            "peligro": "rayos"
        },
        "niebla": {
            "modificadores": {"evasion": 0.2},
            "visibilidad": 0.3,
            "eventos_extra": 0.2,
            "sigilo": True
        },
        "nevada": {
            "modificadores": {"velocidad": -0.2, "stamina_cost": 1.5},
            "visibilidad": 0.6,
            "huellas": True
        },
        "calor_extremo": {
            "modificadores": {"stamina_regen": -0.5},
            "visibilidad": 0.9,
            "peligro": "golpe_calor"
        }
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.rng = seed.get_rng("clima")
        self.clima_actual = None
        self.duracion = 0
    
    def actualizar(self, tick: int, bioma: dict) -> dict:
        """Actualiza el clima basado en tick y bioma"""
        # Cambiar clima cada cierto tiempo
        if self.duracion <= 0:
            self.clima_actual = self._generar_clima(bioma)
            self.duracion = self.rng.randint(5, 20)
        
        self.duracion -= 1
        
        return self.CLI MAS[self.clima_actual]
    
    def _generar_clima(self, bioma: dict) -> str:
        """Genera clima apropiado para el bioma"""
        climas_bioma = bioma.get("clima", ["despejado"])
        
        # Pesos basados en bioma
        if "lluvia" in climas_bioma:
            pesos = [30, 40, 10, 15, 5, 0]  # Más lluvia
        elif "seco" in climas_bioma:
            pesos = [50, 5, 5, 0, 0, 40]  # Más calor
        else:
            pesos = [40, 20, 10, 15, 10, 5]  # Balanceado
        
        climas = list(self.CLIMAS.keys())
        return self.rng.choices(climas, weights=pesos)[0]
```

---

## 9. Sistema de Facciones y Reputación

### Facciones Dinámicas

```python
class FaccionSystem:
    """Sistema de facciones con relaciones dinámicas"""
    
    FACCIONES = {
        "orden_plata": {
            "nombre": "Orden de la Plata",
            "descripcion": "Caballeros defensores de la luz",
            "enemigos": ["culto_sombras", "bandidos"],
            "aliados": ["iglesia", "aldeanos"],
            "recompensas": {"respetado": "titulo_caballero", "exaltado": "montura"}
        },
        "culto_sombras": {
            "nombre": "Culto de las Sombras",
            "descripcion": "Seguidores de poderes oscuros",
            "enemigos": ["orden_plata", "iglesia"],
            "aliados": ["no_muertos"],
            "recompensas": {"respetado": "hechizo_oscuro", "exaltado": "artefacto"}
        },
        "gremio_mercaderes": {
            "nombre": "Gremio de Mercaderes",
            "descripcion": "Comerciantes sin escrúpulos",
            "enemigos": ["bandidos"],
            "aliados": ["aldeanos"],
            "recompensas": {"respetado": "descuento", "exaltado": "tienda_secreta"}
        },
        "bandidos": {
            "nombre": "Bandidos del Camino",
            "descripcion": "Forajidos y ladrones",
            "enemigos": ["orden_plata", "gremio_mercaderes", "aldeanos"],
            "aliados": ["culto_sombras"],
            "recompensas": {"respetado": "escondite", "exaltado": "liderazgo"}
        }
    }
    
    NIVELES_REPUTACION = [
        (-100, "Exiliado"),
        (-50, "Enemigo"),
        (-25, "Hostil"),
        (0, "Neutral"),
        (25, "Amistoso"),
        (50, "Honrado"),
        (75, "Respetado"),
        (100, "Exaltado")
    ]
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.rng = seed.get_rng("facciones")
        self.reputacion = {f: 0 for f in self.FACCIONES}
        self.eventos_faccion = []
    
    def modificar_reputacion(self, faccion: str, cantidad: int):
        """Modifica reputación con una facción"""
        if faccion in self.reputacion:
            self.reputacion[faccion] = max(-100, min(100, self.reputacion[faccion] + cantidad))
            
            # Afectar facciones aliadas/enemigas
            fac = self.FACCIONES[faccion]
            for aliado in fac.get("aliados", []):
                self.reputacion[aliado] = max(-100, min(100, self.reputacion[aliado] + cantidad // 2))
            for enemigo in fac.get("enemigos", []):
                self.reputacion[enemigo] = max(-100, min(100, self.reputacion[enemigo] - cantidad // 2))
    
    def get_nivel_reputacion(self, faccion: str) -> str:
        """Obtiene el nivel de reputación"""
        rep = self.reputacion.get(faccion, 0)
        for threshold, nombre in reversed(self.NIVELES_REPUTACION):
            if rep >= threshold:
                return nombre
        return "Neutral"
    
    def generar_encuentro_faccion(self, bioma: str) -> dict:
        """Genera un encuentro relacionado con facciones"""
        # Filtrar facciones activas en el bioma
        facciones_activas = self._get_facciones_bioma(bioma)
        
        if not facciones_activas:
            return None
        
        faccion = self.rng.choice(facciones_activas)
        nivel = self.get_nivel_reputacion(faccion)
        
        # Generar encuentro basado en reputación
        if nivel in ["Exiliado", "Enemigo"]:
            return self._generar_emboscada(faccion)
        elif nivel in ["Respetado", "Exaltado"]:
            return self._generar_recompensa(faccion)
        else:
            return self._generar_encuentro_neutral(faccion)
    
    def _get_facciones_bioma(self, bioma: str) -> list:
        """Obtiene facciones activas en un bioma"""
        # Mapeo bioma -> facciones
        mapeo = {
            "bosque_ancestral": ["orden_plata", "bandidos"],
            "paramo_marchito": ["culto_sombras"],
            "ciudad": ["gremio_mercaderes", "orden_plata", "iglesia"]
        }
        return mapeo.get(bioma, [])
```

---

## 10. Integración con Backend

### API Endpoints

```python
# backend/src/systems/exploracion.py

from flask import Blueprint, request, jsonify
from src.systems.world import WorldManager

exploracion_bp = Blueprint('exploracion', __name__)
world_manager = None

def init_world(seed: str = None):
    global world_manager
    world_manager = WorldManager(seed)

@exploracion_bp.route('/explorar', methods=['POST'])
def explorar():
    """Ejecuta una acción de exploración"""
    data = request.json
    personaje_id = data.get('personaje_id')
    accion = data.get('accion', 'explorar')  # explorar, moverse, interactuar
    
    resultado = world_manager.procesar_accion(personaje_id, accion)
    
    return jsonify(resultado)

@exploracion_bp.route('/zona', methods=['GET'])
def get_zona():
    """Obtiene información de la zona actual"""
    personaje_id = request.args.get('personaje_id')
    
    zona = world_manager.get_zona_actual(personaje_id)
    
    return jsonify({
        "nombre": zona.nombre,
        "bioma": zona.bioma["nombre"],
        "estado": zona.estado,
        "clima": zona.clima_actual,
        "entidades": len(zona.entidades),
        "poi_descubiertos": len([p for p in zona.poi if p["descubierto"]])
    })

@exploracion_bp.route('/mover', methods=['POST'])
def mover():
    """Mueve al jugador a una zona adyacente"""
    data = request.json
    personaje_id = data.get('personaje_id')
    direccion = data.get('direccion')  # norte, sur, este, oeste
    
    nueva_zona = world_manager.mover_personaje(personaje_id, direccion)
    
    return jsonify({
        "zona": nueva_zona.nombre,
        "bioma": nueva_zona.bioma["nombre"],
        "descripcion": nueva_zona.descripcion
    })

@exploracion_bp.route('/evento/<evento_id>/resolver', methods=['POST'])
def resolver_evento(evento_id):
    """Resuelve un evento"""
    data = request.json
    opcion = data.get('opcion')
    
    resultado = world_manager.resolver_evento(evento_id, opcion)
    
    return jsonify(resultado)
```

---

## 11. Frontend Integration

### Componente React

```tsx
// frontend/src/components/juego/panels/ExploracionPanel.tsx

"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Map, Compass, AlertTriangle, Sparkles } from 'lucide-react';

interface Zona {
  nombre: string;
  bioma: string;
  clima: string;
  estado: string;
}

export function ExploracionPanel() {
  const [zona, setZona] = useState<Zona | null>(null);
  const [explorando, setExplorando] = useState(false);
  const [eventos, setEventos] = useState<any[]>([]);
  const [clima, setClima] = useState<string>('');

  const explorar = async () => {
    setExplorando(true);
    try {
      const res = await fetch('/api/explorar', {
        method: 'POST',
        body: JSON.stringify({ accion: 'explorar' })
      });
      const data = await res.json();
      
      if (data.eventos) {
        setEventos(prev => [...prev, ...data.eventos]);
      }
    } finally {
      setExplorando(false);
    }
  };

  return (
    <div className="relative">
      {/* Header de zona */}
      <div className="mb-8">
        <h2 className="font-medieval text-3xl text-[#d4a843]">{zona?.nombre}</h2>
        <p className="text-[#9a978a]">{zona?.bioma} • Clima: {clima}</p>
      </div>

      {/* Mapa visual */}
      <div className="grid grid-cols-5 gap-2 mb-8">
        {/* Renderizar tiles descubiertos */}
      </div>

      {/* Botón de explorar */}
      <button
        onClick={explorar}
        disabled={explorando}
        className="w-full py-4 bg-[#d4a843] text-black font-medieval"
      >
        {explorando ? 'Explorando...' : 'ADENTRARSE'}
      </button>

      {/* Eventos */}
      <AnimatePresence>
        {eventos.map((evento, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-4 p-4 bg-[#12121a] border border-[#d4a843]/30"
          >
            <p>{evento.descripcion}</p>
            <div className="flex gap-2 mt-2">
              {evento.opciones?.map((op: string) => (
                <button key={op} className="px-4 py-2 bg-[#2a2a35]">
                  {op}
                </button>
              ))}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

---

## 12. Guardado y Persistencia

### Estructura de Datos Guardados

```python
class WorldSave:
    """Maneja el guardado del mundo procedural"""
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
    
    def guardar(self, personaje_id: str) -> dict:
        """Genera datos para guardar"""
        return {
            "seed": self.seed.master_seed,
            "zonas_descubiertas": list(self.zonas_descubiertas),
            "zonas_visitadas": {
                str(coords): {
                    "veces_explorada": zona.veces_explorada,
                    "estado": zona.estado,
                    "entidades_derrotadas": [e["id"] for e in zona.entidades if e.get("derrotado")]
                }
                for coords, zona in self.zonas.items()
                if zona.visitada
            },
            "eventos_resueltos": [e["id"] for e in self.eventos if e.get("resuelto")],
            "reputacion": self.facciones.reputacion,
            "historial": self.historial_eventos[-50:]  # Últimos 50 eventos
        }
    
    def cargar(self, datos: dict):
        """Carga datos guardados"""
        self.zonas_descubiertas = set(tuple(c) for c in datos.get("zonas_descubiertas", []))
        self.facciones.reputacion = datos.get("reputacion", {})
        # ... restaurar más estado
```

---

## 13. Consideraciones de Rendimiento

### Optimizaciones

1. **Generación Lazy**: Solo generar zonas cuando se visitan
2. **Cache de Semillas**: Reutilizar RNG para mismo contexto
3. **Serialización Eficiente**: No guardar zonas completas, solo cambios
4. **Chunk Loading**: Cargar zonas adyacentes en background

```python
class WorldManager:
    """Manager optimizado del mundo"""
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.zona_cache = {}  # Cache de zonas generadas
        self.max_cache = 20   # Máximo zonas en memoria
    
    def get_zona(self, coords: tuple) -> Zona:
        """Obtiene zona con cache"""
        if coords in self.zona_cache:
            return self.zona_cache[coords]
        
        # Si cache lleno, eliminar zona más lejana
        if len(self.zona_cache) >= self.max_cache:
            self._limpiar_cache()
        
        zona = Zona.generar(self.seed, coords, self.noise_map)
        self.zona_cache[coords] = zona
        
        return zona
    
    def _limpiar_cache(self):
        """Limpia zonas lejanas del cache"""
        if not self.zona_actual:
            return
        
        # Mantener solo zonas adyacentes
        x, y = self.zona_actual.coordenadas
        adyacentes = {(x+dx, y+dy) for dx in [-1,0,1] for dy in [-1,0,1]}
        
        self.zona_cache = {
            coords: zona 
            for coords, zona in self.zona_cache.items()
            if coords in adyacentes
        }
```

---

## 14. Próximos Pasos de Implementación

### Fase 1: Core (Semana 1-2)
- [ ] Sistema de semillas funcional
- [ ] Generación básica de biomas
- [ ] Zonas con tiles simples
- [ ] API de exploración básica

### Fase 2: Contenido (Semana 3-4)
- [ ] Generación de enemigos
- [ ] Sistema de eventos
- [ ] Tesoros procedurales
- [ ] Clima dinámico

### Fase 3: Profundidad (Semana 5-6)
- [ ] Facciones y reputación
- [ ] POIs únicos
- [ ] Historia emergente
- [ ] Encuentros especiales

### Fase 4: Polish (Semana 7-8)
- [ ] UI completa
- [ ] Animaciones
- [ ] Audio contextual
- [ ] Balanceo

---

## 15. Ejemplo de Uso Completo

```python
# Crear mundo
seed = WorldSeed("mi-partida-123")
world = WorldManager(seed)

# Jugador explora
zona = world.get_zona_actual()
resultado = zona.explorar()

print(f"Zona: {zona.nombre}")
print(f"Bioma: {zona.bioma['nombre']}")
print(f"Clima: {zona.clima_actual}")

for r in resultado['resultados']:
    if r['tipo'] == 'encuentro':
        print(f"¡Encuentro con {r['entidad']}!")
    elif r['tipo'] == 'evento':
        print(f"Evento: {r['evento']}")
    elif r['tipo'] == 'tile_descubierto':
        print(f"Descubres: {r['terreno']}")

# Mover a otra zona
nueva_zona = world.mover("norte")
print(f"Llegas a: {nueva_zona.nombre}")
```

---

## Notas Finales

Este sistema está diseñado para ser:
- **Determinista**: Misma semilla = mismo mundo
- **Infinito**: El mundo se genera según se explora
- **Memorable**: Cada partida es única
- **Emergente**: Las historias surgen de los sistemas

La clave está en que **nada está predefinido** excepto las reglas. El contenido emerge de la interacción de los sistemas.