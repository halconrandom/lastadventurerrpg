"""
Sistema de Biomas para generacion procedural del mundo.

Cada bioma tiene caracteristicas unicas que afectan:
- Terreno y apariencia
- Clima predominante
- Recursos disponibles
- Fauna y enemigos
- Peligros naturales
- Eventos posibles
"""

from typing import Dict, List, Optional, Tuple
from .seed import WorldSeed


class Bioma:
    """Representa un bioma generado proceduralmente."""
    
    def __init__(
        self,
        key: str,
        nombre: str,
        nombre_unico: str,
        terreno: List[str],
        clima: List[str],
        recursos: List[str],
        fauna: List[str],
        peligros: List[str],
        eventos: List[str],
        variacion: Optional[Dict] = None,
        coordenadas: Optional[Tuple[int, int]] = None
    ):
        self.key = key
        self.nombre = nombre
        self.nombre_unico = nombre_unico
        self.terreno = terreno
        self.clima = clima
        self.recursos = recursos
        self.fauna = fauna
        self.peligros = peligros
        self.eventos = eventos
        self.variacion = variacion or {"tipo": "normal", "modificador": "ninguno"}
        self.coordenadas = coordenadas or (0, 0)
    
    def to_dict(self) -> dict:
        """Serializa el bioma."""
        return {
            "key": self.key,
            "nombre": self.nombre,
            "nombre_unico": self.nombre_unico,
            "terreno": self.terreno,
            "clima": self.clima,
            "recursos": self.recursos,
            "fauna": self.fauna,
            "peligros": self.peligros,
            "eventos": self.eventos,
            "variacion": self.variacion,
            "coordenadas": self.coordenadas
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Bioma':
        """Deserializa un bioma."""
        return cls(**data)
    
    def get_descripcion(self) -> str:
        """Genera una descripcion procedural del bioma."""
        variacion_tipo = self.variacion.get("tipo", "normal")
        
        descripciones_base = {
            "bosque_ancestral": "Arboles milenarios se alzan hacia el cielo",
            "paramo_marchito": "Tierra yerma se extiende hasta el horizonte",
            "pantano_sombrio": "Cienagas pestilentes ocultan secretos",
            "montanas_heladas": "Picos nevados rasgan las nubes",
            "desierto_ceniza": "Ceniza volcanica cubre todo a la vista",
            "ruinas_subterraneas": "Pasillos antiguos se pierden en la oscuridad"
        }
        
        base = descripciones_base.get(self.key, "Un lugar misterioso")
        
        modificadores_variacion = {
            "encantado": "impregnado de magia antigua",
            "corrupto": "corrompido por fuerzas oscuras",
            "antiguo": "lleno de historia olvidada",
            "maldito": "bajo una maldicion ancestral",
            "olvidado": "abandonado por el tiempo",
            "sagrado": "consagrado por poderes divinos",
            "normal": ""
        }
        
        extra = modificadores_variacion.get(variacion_tipo, "")
        
        if extra:
            return f"{base}, {extra}."
        return f"{base}."
    
    def __repr__(self) -> str:
        return f"Bioma('{self.nombre_unico}')"


class BiomaGenerator:
    """Genera biomas procedurales."""
    
    # Definicion de biomas base
    BIOMAS_BASE = {
        "bosque_ancestral": {
            "nombre": "Bosque Ancestral",
            "terreno": ["densa_vegetacion", "arboles_antiguos", "claros", "riachuelos"],
            "clima": ["lluvia", "niebla", "templado", "humedo"],
            "recursos": ["madera_antigua", "hierbas_raras", "bayas", "setas", "resina"],
            "fauna": ["lobos", "ciervos", "osos", "jabalies", "ardillas"],
            "peligros": ["lobos_hambrientos", "bandidos", "trampas_naturales", "plantas_venenosas"],
            "eventos": ["encuentro_viajero", "ruinas_ocultas", "claro_mistico", "arbol_sagrado"]
        },
        "paramo_marchito": {
            "nombre": "Paramo Marchito",
            "terreno": ["tierra_yerma", "tumbas_antiguas", "niebla", "piedras_hundidas"],
            "clima": ["seco", "ventoso", "noches_frias", "niebla_densa"],
            "recursos": ["piedra", "huesos", "metales_oxidados", "telas_raidas"],
            "fauna": ["no_muertos", "cuervos", "sombras", "ratas", "serpientes"],
            "peligros": ["tumbas_profanadas", "niebla_venenosa", "espectros", "trampas_antiguas"],
            "eventos": ["procesion_fantasma", "tumba_abierta", "viajero_perdido", "altar_olvidado"]
        },
        "pantano_sombrio": {
            "nombre": "Pantano Sombrio",
            "terreno": ["cienagas", "arboles_muertos", "neblina", "aguas_negras"],
            "clima": ["humedo", "lluvia", "calido", "bochornoso"],
            "recursos": ["hongos_venenosos", "plantas_carnivoras", "lodo_curativo", "musgo"],
            "fauna": ["criaturas_acidas", "serpientes", "sapos_gigantes", "mosquitos", "cocodrilos"],
            "peligros": ["arenas_movedizas", "gases_toxicos", "criaturas_hambrientas", "infecciones"],
            "eventos": ["bruja_del_pantano", "tesoro_hundido", "cabaña_abandonada", "portal_oculto"]
        },
        "montanas_heladas": {
            "nombre": "Montanas Heladas",
            "terreno": ["picos_nevados", "glaciares", "cuevas", "acantilados"],
            "clima": ["frio_extremo", "tormenta_nieve", "viento", "helado"],
            "recursos": ["minerales_raros", "hielo_eterno", "pieles", "cristales"],
            "fauna": ["yetis", "lobos_nevados", "aguilas", "cabras_monteses", "osos_polares"],
            "peligros": ["avalanchas", "grietas", "hipotermia", "criaturas_de_hielo"],
            "eventos": ["refugio_montanes", "cueva_tesoro", "templo_olvidado", "gigante_dormido"]
        },
        "desierto_ceniza": {
            "nombre": "Desierto de Ceniza",
            "terreno": ["ceniza_volcanica", "crateres", "ruinas_quemadas", "oasis_ocultos"],
            "clima": ["caliente", "seco", "tormentas_ceniza", "noches_frias"],
            "recursos": ["obsidiana", "azufre", "gemas_volcanicas", "cactus"],
            "fauna": ["demonios_menores", "escorpiones", "serpientes_arena", "buitres"],
            "peligros": ["tormentas_fuego", "grietas_volcanicas", "demonios", "espejismos"],
            "eventos": ["portal_infernal", "ciudad_enterrada", "genio_encadenado", "fuente_magica"]
        },
        "ruinas_subterraneas": {
            "nombre": "Ruinas Subterraneas",
            "terreno": ["pasillos_antiguos", "salas_colapsadas", "criptas", "minas_abandonadas"],
            "clima": ["estable", "humedo", "frio", "oscuro"],
            "recursos": ["artefactos", "minerales", "libros_antiguos", "gemas"],
            "fauna": ["constructos", "arañas_gigantes", "murcielagos", "hongos_ambulantes"],
            "peligros": ["trampas_antiguas", "derrumbes", "constructos_hostiles", "gases"],
            "eventos": ["tumba_antigua", "laboratorio_alquimista", "portal_dimensional", "golem_dormido"]
        }
    }
    
    # Variaciones posibles por bioma
    VARIACIONES = {
        "bosque_ancestral": [
            {"tipo": "encantado", "modificador": "magia +20%", "bonus": {"tesoros": 1.2}},
            {"tipo": "corrupto", "modificador": "enemigos +30%", "bonus": {"peligros": 1.3}},
            {"tipo": "antiguo", "modificador": "secretos +25%", "bonus": {"eventos": 1.25}},
        ],
        "paramo_marchito": [
            {"tipo": "maldito", "modificador": "no_muertos +40%", "bonus": {"peligros": 1.4}},
            {"tipo": "olvidado", "modificador": "secretos +25%", "bonus": {"tesoros": 1.25}},
            {"tipo": "sagrado", "modificador": "reliquias +15%", "bonus": {"eventos": 1.15}},
        ],
        "pantano_sombrio": [
            {"tipo": "toxico", "modificador": "veneno +50%", "bonus": {"peligros": 1.5}},
            {"tipo": "mistico", "modificador": "magia +30%", "bonus": {"eventos": 1.3}},
            {"tipo": "ancestral", "modificador": "tesoros +20%", "bonus": {"tesoros": 1.2}},
        ],
        "montanas_heladas": [
            {"tipo": "eterno", "modificador": "hielo +40%", "bonus": {"recursos": 1.4}},
            {"tipo": "sagrado", "modificador": "templos +20%", "bonus": {"eventos": 1.2}},
            {"tipo": "hostil", "modificador": "peligros +35%", "bonus": {"peligros": 1.35}},
        ],
        "desierto_ceniza": [
            {"tipo": "infernal", "modificador": "demonios +30%", "bonus": {"peligros": 1.3}},
            {"tipo": "olvidado", "modificador": "ruinas +25%", "bonus": {"tesoros": 1.25}},
            {"tipo": "mistico", "modificador": "portales +15%", "bonus": {"eventos": 1.15}},
        ],
        "ruinas_subterraneas": [
            {"tipo": "antiguo", "modificador": "artefactos +30%", "bonus": {"tesoros": 1.3}},
            {"tipo": "colapsado", "modificador": "peligros +25%", "bonus": {"peligros": 1.25}},
            {"tipo": "habitado", "modificador": "npcs +20%", "bonus": {"eventos": 1.2}},
        ]
    }
    
    # Partes para nombres procedurales
    PREFIJOS_NOMBRE = ["El", "Los", "Las", "Aquellos", "Estos"]
    ADJETIVOS_NOMBRE = [
        "Olvidados", "Susurrantes", "Eternos", "Marchitos", "Vivientes",
        "Silenciosos", "Perturbadores", "Antiguos", "Malditos", "Sagrados",
        "Oscuros", "Helados", "Ardientes", "Profundos", "Perdidos"
    ]
    
    def __init__(self, seed: WorldSeed):
        """
        Inicializa el generador de biomas.
        
        Args:
            seed: Instancia de WorldSeed para determinismo
        """
        self.seed = seed
    
    def generar_bioma(self, coordenadas: Tuple[int, int]) -> Bioma:
        """
        Genera un bioma unico para las coordenadas dadas.
        
        Args:
            coordenadas: Tupla (x, y) de la posicion
            
        Returns:
            Instancia de Bioma generada proceduralmente
        """
        x, y = coordenadas
        contexto = f"bioma_{x}_{y}"
        rng = self.seed.get_rng(contexto)
        
        # Seleccionar bioma base
        bioma_key = rng.choice(list(self.BIOMAS_BASE.keys()))
        bioma_base = self.BIOMAS_BASE[bioma_key].copy()
        
        # Seleccionar variacion
        variaciones = self.VARIACIONES.get(bioma_key, [{"tipo": "normal", "modificador": "ninguno"}])
        variacion = rng.choice(variaciones)
        
        # Generar nombre unico
        nombre_unico = self._generar_nombre_unico(rng, bioma_base["nombre"], variacion)
        
        # Seleccionar subconjuntos de cada lista
        terreno = self._seleccionar_subconjunto(rng, bioma_base["terreno"], 2, 4)
        clima = self._seleccionar_subconjunto(rng, bioma_base["clima"], 1, 3)
        recursos = self._seleccionar_subconjunto(rng, bioma_base["recursos"], 2, 5)
        fauna = self._seleccionar_subconjunto(rng, bioma_base["fauna"], 2, 4)
        peligros = self._seleccionar_subconjunto(rng, bioma_base["peligros"], 1, 3)
        eventos = self._seleccionar_subconjunto(rng, bioma_base["eventos"], 1, 3)
        
        return Bioma(
            key=bioma_key,
            nombre=bioma_base["nombre"],
            nombre_unico=nombre_unico,
            terreno=terreno,
            clima=clima,
            recursos=recursos,
            fauna=fauna,
            peligros=peligros,
            eventos=eventos,
            variacion=variacion,
            coordenadas=coordenadas
        )
    
    def _generar_nombre_unico(self, rng, nombre_base: str, variacion: dict) -> str:
        """Genera un nombre unico para el bioma."""
        # 30% de nombres especiales
        if rng.random() < 0.3:
            prefijo = rng.choice(self.PREFIJOS_NOMBRE)
            adjetivo = rng.choice(self.ADJETIVOS_NOMBRE)
            sustantivo = rng.choice(["Bosques", "Paramos", "Pantanos", "Montanas", "Desiertos", "Ruinas"])
            return f"{prefijo} {sustantivo} {adjetivo}"
        
        # 70% nombre base + variacion
        tipo_variacion = variacion.get("tipo", "normal")
        if tipo_variacion != "normal":
            return f"{nombre_base} {tipo_variacion.title()}"
        
        return nombre_base
    
    def _seleccionar_subconjunto(self, rng, lista: List[str], minimo: int, maximo: int) -> List[str]:
        """Selecciona un subconjunto aleatorio de una lista."""
        cantidad = rng.randint(minimo, max(maximo, minimo))
        cantidad = min(cantidad, len(lista))
        return rng.sample(lista, cantidad) if lista else []
    
    def get_bioma_base(self, key: str) -> Optional[dict]:
        """Obtiene la definicion base de un bioma."""
        return self.BIOMAS_BASE.get(key)
    
    def get_todos_biomas(self) -> List[str]:
        """Retorna lista de keys de todos los biomas."""
        return list(self.BIOMAS_BASE.keys())
