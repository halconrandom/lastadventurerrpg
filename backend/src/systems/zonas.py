"""
Sistema de Zonas y Tiles para exploracion procedural.

Una Zona es un area explorable del mapa que contiene:
- Tiles (casillas con terreno)
- Entidades (NPCs, enemigos)
- Puntos de interes (POI)
- Eventos disponibles
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from .seed import WorldSeed
from .biomas import Bioma, BiomaGenerator


@dataclass
class Tile:
    """Representa una casilla del mapa."""
    x: int
    y: int
    terreno: str
    explorado: bool = False
    especial: Optional[str] = None
    entidad_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "terreno": self.terreno,
            "explorado": self.explorado,
            "especial": self.especial,
            "entidad_id": self.entidad_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tile':
        return cls(**data)


@dataclass
class Entidad:
    """Representa una entidad en la zona (NPC, enemigo, etc)."""
    id: str
    tipo: str
    nombre: str
    hostil: bool
    nivel: int
    posicion: Tuple[int, int]
    activo: bool = True
    derrotado: bool = False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "hostil": self.hostil,
            "nivel": self.nivel,
            "posicion": list(self.posicion),
            "activo": self.activo,
            "derrotado": self.derrotado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Entidad':
        data["posicion"] = tuple(data["posicion"])
        return cls(**data)


@dataclass
class PuntoInteres:
    """Punto de interes en la zona."""
    tipo: str
    nombre: str
    posicion: Tuple[int, int]
    descubierto: bool = False
    explorado: bool = False
    
    def to_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "posicion": list(self.posicion),
            "descubierto": self.descubierto,
            "explorado": self.explorado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PuntoInteres':
        data["posicion"] = tuple(data["posicion"])
        return cls(**data)


class Zona:
    """
    Una zona explorable del mapa.
    
    Contiene tiles, entidades, POIs y eventos.
    """
    
    # Tipos de POI por bioma
    POIS_POR_BIOMA = {
        "bosque_ancestral": [
            ("claro_mistico", "Claro Mistico"),
            ("arbol_sagrado", "Arbol Sagrado"),
            ("cabaña_abandonada", "Cabana Abandonada"),
            ("ruinas_cubiertas", "Ruinas Cubiertas de Vegetacion"),
            ("fuente_antigua", "Fuente Antigua")
        ],
        "paramo_marchito": [
            ("tumba_antigua", "Tumba Antigua"),
            ("altar_olvidado", "Altar Olvidado"),
            ("cementerio", "Cementerio en Ruinas"),
            ("torre_derruida", "Torre Derruida"),
            ("fosa_comun", "Fosa Comun")
        ],
        "pantano_sombrio": [
            ("charca_toxica", "Charca Toxica"),
            ("nido_criaturas", "Nido de Criaturas"),
            ("cabaña_hechicero", "Cabana del Hechicero"),
            ("templo_hundido", "Templo Hundido"),
            ("pozo_negro", "Pozo Negro")
        ],
        "montanas_heladas": [
            ("cueva_profunda", "Cueva Profunda"),
            ("refugio_montanes", "Refugio Montanes"),
            ("templo_hielo", "Templo de Hielo"),
            ("grieta", "Grieta Peligrosa"),
            ("pico_sagrado", "Pico Sagrado")
        ],
        "desierto_ceniza": [
            ("oasis_oculto", "Oasis Oculto"),
            ("ciudad_enterrada", "Ciudad Enterrada"),
            ("crater_humante", "Crater Humeante"),
            ("tumba_faraon", "Tumba del Faraon"),
            ("portal_infernal", "Portal Infernal")
        ],
        "ruinas_subterraneas": [
            ("cripta_real", "Cripta Real"),
            ("laboratorio", "Laboratorio Alquimico"),
            ("bodega_antigua", "Bodega Antigua"),
            ("sala_trono", "Sala del Trono"),
            ("portal_dimensional", "Portal Dimensional")
        ]
    }
    
    # Tiles especiales posibles
    TILES_ESPECIALES = [
        "tesoro_menor",
        "tesoro_mayor",
        "trampa",
        "secreto",
        "evento",
        "rareza"
    ]
    
    def __init__(
        self,
        seed: WorldSeed,
        coordenadas: Tuple[int, int],
        bioma: Bioma
    ):
        self.seed = seed
        self.coordenadas = coordenadas
        self.bioma = bioma
        self.nombre = bioma.nombre_unico
        
        # Contenido procedural
        self.tiles: List[List[Tile]] = []
        self.entidades: List[Entidad] = []
        self.pois: List[PuntoInteres] = []
        self.eventos_disponibles: List[str] = []
        
        # Estado
        self.visitada = False
        self.veces_explorada = 0
        self.estado = "inexplorada"  # inexplorada, explorando, agotada
        
        # Tamaño
        self.tamaño = 0
    
    def generar(self) -> None:
        """Genera todo el contenido de la zona."""
        x, y = self.coordenadas
        contexto = f"zona_{x}_{y}"
        rng = self.seed.get_rng(contexto)
        
        # Generar tamaño variable
        self.tamaño = rng.randint(15, 30)
        
        # Generar tiles
        self._generar_tiles(rng)
        
        # Generar entidades
        self._generar_entidades(rng)
        
        # Generar POIs
        self._generar_pois(rng)
        
        # Seleccionar eventos disponibles
        self._seleccionar_eventos(rng)
    
    def _generar_tiles(self, rng) -> None:
        """Genera el mapa de tiles."""
        terrenos = self.bioma.terreno
        
        for y in range(self.tamaño):
            fila = []
            for x in range(self.tamaño):
                # Terreno basico
                terreno = rng.choice(terrenos)
                
                # Posible tile especial (5%)
                especial = None
                if rng.random() < 0.05:
                    especial = rng.choice(self.TILES_ESPECIALES)
                
                tile = Tile(
                    x=x,
                    y=y,
                    terreno=terreno,
                    especial=especial
                )
                fila.append(tile)
            self.tiles.append(fila)
    
    def _generar_entidades(self, rng) -> None:
        """Genera entidades en la zona."""
        fauna = self.bioma.fauna
        peligros = self.bioma.peligros
        
        # Calcular nivel base por distancia al centro
        cx, cy = self.coordenadas
        distancia_centro = abs(cx - 50) + abs(cy - 50)
        nivel_base = max(1, distancia_centro // 10)
        
        # Entidades hostiles (2-6)
        num_hostiles = rng.randint(2, 6)
        for i in range(num_hostiles):
            tipo = rng.choice(peligros + fauna)
            nivel = max(1, nivel_base + rng.randint(-1, 2))
            
            entidad = Entidad(
                id=f"ent_{cx}_{cy}_h{i}",
                tipo=tipo,
                nombre=self._generar_nombre_entidad(rng, tipo),
                hostil=True,
                nivel=nivel,
                posicion=(rng.randint(0, self.tamaño-1), rng.randint(0, self.tamaño-1))
            )
            self.entidades.append(entidad)
        
        # Entidades neutrales (1-3)
        num_neutrales = rng.randint(1, 3)
        for i in range(num_neutrales):
            tipo = rng.choice(fauna)
            nivel = max(1, nivel_base + rng.randint(-2, 1))
            
            entidad = Entidad(
                id=f"ent_{cx}_{cy}_n{i}",
                tipo=tipo,
                nombre=self._generar_nombre_entidad(rng, tipo),
                hostil=False,
                nivel=nivel,
                posicion=(rng.randint(0, self.tamaño-1), rng.randint(0, self.tamaño-1))
            )
            self.entidades.append(entidad)
    
    def _generar_nombre_entidad(self, rng, tipo: str) -> str:
        """Genera nombre para una entidad."""
        adjetivos = ["Viejo", "Joven", "Grande", "Pequeno", "Salvaje", "Hambriento", "Feroz"]
        
        if rng.random() < 0.3:
            return f"{rng.choice(adjetivos)} {tipo.replace('_', ' ').title()}"
        return tipo.replace('_', ' ').title()
    
    def _generar_pois(self, rng) -> None:
        """Genera puntos de interes."""
        pois_bioma = self.POIS_POR_BIOMA.get(self.bioma.key, [])
        
        if not pois_bioma:
            return
        
        # 1-3 POIs por zona
        num_pois = rng.randint(1, 3)
        pois_seleccionados = rng.sample(pois_bioma, min(num_pois, len(pois_bioma)))
        
        for tipo, nombre in pois_seleccionados:
            poi = PuntoInteres(
                tipo=tipo,
                nombre=nombre,
                posicion=(rng.randint(0, self.tamaño-1), rng.randint(0, self.tamaño-1))
            )
            self.pois.append(poi)
    
    def _seleccionar_eventos(self, rng) -> None:
        """Selecciona eventos disponibles en la zona."""
        eventos = self.bioma.eventos
        num_eventos = rng.randint(1, min(3, len(eventos)))
        self.eventos_disponibles = rng.sample(eventos, num_eventos)
    
    def explorar(self) -> Dict[str, Any]:
        """
        Ejecuta una accion de exploracion.
        
        Returns:
            Diccionario con resultados de la exploracion
        """
        self.visitada = True
        self.veces_explorada += 1
        
        x, y = self.coordenadas
        rng = self.seed.get_rng(f"explorar_{x}_{y}_{self.veces_explorada}")
        
        resultados = {
            "zona": self.nombre,
            "bioma": self.bioma.nombre,
            "variacion": self.bioma.variacion["tipo"],
            "descripcion": self.bioma.get_descripcion(),
            "tiles_descubiertos": [],
            "encuentros": [],
            "poi_descubierto": None,
            "evento": None
        }
        
        # Descubrir tiles
        tiles_descubiertos = self._descubrir_tiles(rng)
        resultados["tiles_descubiertos"] = tiles_descubiertos
        
        # Posible encuentro
        encuentro = self._generar_encuentro(rng)
        if encuentro:
            resultados["encuentros"].append(encuentro)
        
        # Posible descubrimiento de POI
        poi = self._descubrir_poi(rng)
        if poi:
            resultados["poi_descubierto"] = poi
        
        # Actualizar estado
        if self.veces_explorada > 5:
            self.estado = "agotada"
        else:
            self.estado = "explorando"
        
        resultados["estado_zona"] = self.estado
        resultados["veces_explorada"] = self.veces_explorada
        
        return resultados
    
    def _descubrir_tiles(self, rng) -> List[Dict]:
        """Descubre tiles aleatorios."""
        descubiertos = []
        num_descubrir = rng.randint(3, 8)
        
        intentos = 0
        while len(descubiertos) < num_descubrir and intentos < 100:
            x = rng.randint(0, self.tamaño - 1)
            y = rng.randint(0, self.tamaño - 1)
            
            tile = self.tiles[y][x]
            if not tile.explorado:
                tile.explorado = True
                descubiertos.append(tile.to_dict())
            
            intentos += 1
        
        return descubiertos
    
    def _generar_encuentro(self, rng) -> Optional[Dict]:
        """Genera un posible encuentro."""
        # 40% probabilidad de encuentro
        if rng.random() > 0.4:
            return None
        
        entidades_activas = [e for e in self.entidades if e.activo and not e.derrotado]
        
        if not entidades_activas:
            return None
        
        entidad = rng.choice(entidades_activas)
        
        return {
            "tipo": "encuentro",
            "entidad_id": entidad.id,
            "entidad_tipo": entidad.tipo,
            "entidad_nombre": entidad.nombre,
            "hostil": entidad.hostil,
            "nivel": entidad.nivel
        }
    
    def _descubrir_poi(self, rng) -> Optional[Dict]:
        """Descubre un POI aleatoriamente."""
        pois_no_descubiertos = [p for p in self.pois if not p.descubierto]
        
        if not pois_no_descubiertos:
            return None
        
        # 20% probabilidad de descubrir POI
        if rng.random() > 0.2:
            return None
        
        poi = rng.choice(pois_no_descubiertos)
        poi.descubierto = True
        
        return {
            "tipo": poi.tipo,
            "nombre": poi.nombre,
            "posicion": poi.posicion
        }
    
    def to_dict(self) -> dict:
        """Serializa la zona."""
        return {
            "coordenadas": list(self.coordenadas),
            "bioma": self.bioma.to_dict(),
            "nombre": self.nombre,
            "tamaño": self.tamaño,
            "tiles": [[tile.to_dict() for tile in fila] for fila in self.tiles],
            "entidades": [e.to_dict() for e in self.entidades],
            "pois": [p.to_dict() for p in self.pois],
            "eventos_disponibles": self.eventos_disponibles,
            "visitada": self.visitada,
            "veces_explorada": self.veces_explorada,
            "estado": self.estado
        }
    
    @classmethod
    def from_dict(cls, data: dict, seed: WorldSeed) -> 'Zona':
        """Deserializa una zona."""
        bioma = Bioma.from_dict(data["bioma"])
        
        zona = cls(
            seed=seed,
            coordenadas=tuple(data["coordenadas"]),
            bioma=bioma
        )
        
        zona.nombre = data["nombre"]
        zona.tamaño = data["tamaño"]
        zona.tiles = [[Tile.from_dict(t) for t in fila] for fila in data["tiles"]]
        zona.entidades = [Entidad.from_dict(e) for e in data["entidades"]]
        zona.pois = [PuntoInteres.from_dict(p) for p in data["pois"]]
        zona.eventos_disponibles = data["eventos_disponibles"]
        zona.visitada = data["visitada"]
        zona.veces_explorada = data["veces_explorada"]
        zona.estado = data["estado"]
        
        return zona
    
    def __repr__(self) -> str:
        return f"Zona('{self.nombre}', {self.tamaño}x{self.tamaño}, {self.estado})"


class ZonaGenerator:
    """Generador de zonas."""
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.bioma_gen = BiomaGenerator(seed)
    
    def generar_zona(self, coordenadas: Tuple[int, int]) -> Zona:
        """Genera una zona completa para las coordenadas."""
        bioma = self.bioma_gen.generar_bioma(coordenadas)
        zona = Zona(self.seed, coordenadas, bioma)
        zona.generar()
        return zona
