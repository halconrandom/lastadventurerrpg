"""
Sistema de clima dinamico para la exploracion.

El clima afecta:
- Visibilidad
- Movimiento
- Combate
- Eventos disponibles
- Riesgos y peligros
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .seed import WorldSeed


@dataclass
class EstadoClima:
    """Estado actual del clima."""
    tipo: str
    intensidad: str  # "leve", "moderado", "intenso", "extremo"
    duracion: int  # Turnos restantes
    efectos: List[str]
    descripcion: str
    
    def to_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "intensidad": self.intensidad,
            "duracion": self.duracion,
            "efectos": self.efectos,
            "descripcion": self.descripcion
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EstadoClima':
        return cls(**data)


@dataclass
class CicloDiaNoche:
    """Estado del ciclo dia/noche."""
    hora: int  # 0-23
    fase: str  # "madrugada", "amanecer", "dia", "atardecer", "anochecer", "noche"
    luz: float  # 0.0 - 1.0
    
    def to_dict(self) -> dict:
        return {
            "hora": self.hora,
            "fase": self.fase,
            "luz": self.luz
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CicloDiaNoche':
        return cls(**data)


class ClimaGenerator:
    """Generador de clima dinamico."""
    
    # Clima por bioma
    CLIMA_POR_BIOMA = {
        "bosque_ancestral": {
            "comun": ["soleado", "nublado", "lluvia_ligera", "niebla"],
            "raro": ["tormenta", "lluvia_torrencial"],
            "extremo": ["tormenta_electrica", "inundacion"]
        },
        "paramo_marchito": {
            "comun": ["nublado", "niebla_densa", "ventoso", "frio"],
            "raro": ["tormenta_nieve", "granizo"],
            "extremo": ["ventisca", "niebla_toxica"]
        },
        "pantano_sombrio": {
            "comun": ["humedo", "lluvia_ligera", "niebla", "bochornoso"],
            "raro": ["tormenta", "niebla_toxica"],
            "extremo": ["inundacion", "plaga_insectos"]
        },
        "montanas_heladas": {
            "comun": ["frio", "ventoso", "nublado", "nevada_ligera"],
            "raro": ["tormenta_nieve", "ventisca"],
            "extremo": ["avalancha", "tormenta_hielo"]
        },
        "desierto_ceniza": {
            "comun": ["caluroso", "soleado", "seco", "ventoso"],
            "raro": ["tormenta_arena", "calor_extremo"],
            "extremo": ["tormenta_fuego", "espejismo"]
        },
        "ruinas_subterraneas": {
            "comun": ["estable", "humedo", "frio", "oscuro"],
            "raro": ["gases", "derrumbe"],
            "extremo": ["inundacion_subterranea", "terremoto"]
        }
    }
    
    # Efectos del clima
    EFECTOS_CLIMA = {
        "soleado": {
            "modificadores": {"visibilidad": 1.2, "movimiento": 1.0},
            "efectos": ["buena_visibilidad"],
            "descripcion": "El sol brilla en el cielo despejado."
        },
        "nublado": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 1.0},
            "efectos": ["clima_neutral"],
            "descripcion": "Nubes cubren el cielo."
        },
        "lluvia_ligera": {
            "modificadores": {"visibilidad": 0.9, "movimiento": 0.95},
            "efectos": ["humedad", "huellas_borradas"],
            "descripcion": "Una llovizna suave cae del cielo."
        },
        "lluvia_torrencial": {
            "modificadores": {"visibilidad": 0.6, "movimiento": 0.8},
            "efectos": ["humedad", "huellas_borradas", "dificultad_vision"],
            "descripcion": "La lluvia cae con fuerza, dificultando la vision."
        },
        "tormenta": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 0.7},
            "efectos": ["humedad", "peligro_rayos", "dificultad_vision"],
            "descripcion": "Una tormenta violenta azota la zona."
        },
        "tormenta_electrica": {
            "modificadores": {"visibilidad": 0.4, "movimiento": 0.6},
            "efectos": ["peligro_rayos", "magia_ampliada", "dificultad_vision"],
            "descripcion": "Rayos iluminan el cielo con destellos cegadores."
        },
        "niebla": {
            "modificadores": {"visibilidad": 0.7, "movimiento": 0.9},
            "efectos": ["vision_reducida", "sigilo_mejorado"],
            "descripcion": "Una niebla densa reduce la visibilidad."
        },
        "niebla_densa": {
            "modificadores": {"visibilidad": 0.4, "movimiento": 0.8},
            "efectos": ["vision_muy_reducida", "sigilo_mejorado", "perdida_direccion"],
            "descripcion": "La niebla es tan densa que apenas ves tus manos."
        },
        "niebla_toxica": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 0.7},
            "efectos": ["vision_reducida", "dano_toxico", "enfermedad"],
            "descripcion": "Una niebla verdosa huele a veneno."
        },
        "ventoso": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 0.9},
            "efectos": ["sonidos_enmascarados", "proyectiles_desviados"],
            "descripcion": "El viento sopla con fuerza."
        },
        "ventisca": {
            "modificadores": {"visibilidad": 0.3, "movimiento": 0.5},
            "efectos": ["vision_nula", "frio_extremo", "perdida_direccion"],
            "descripcion": "La nieve y el viento te ciegan por completo."
        },
        "nevada_ligera": {
            "modificadores": {"visibilidad": 0.9, "movimiento": 0.95},
            "efectos": ["frio", "huellas_visibles"],
            "descripcion": "Suaves copos de nieve caen del cielo."
        },
        "tormenta_nieve": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 0.6},
            "efectos": ["frio_extremo", "vision_reducida", "huellas_borradas"],
            "descripcion": "La nieve cae con violencia."
        },
        "caluroso": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 0.95},
            "efectos": ["sed", "fatiga"],
            "descripcion": "El calor es intenso."
        },
        "calor_extremo": {
            "modificadores": {"visibilidad": 0.9, "movimiento": 0.7},
            "efectos": ["sed_rapida", "fatiga_severa", "golpe_calor"],
            "descripcion": "El calor es insoportable, te sientes mareado."
        },
        "tormenta_arena": {
            "modificadores": {"visibilidad": 0.3, "movimiento": 0.5},
            "efectos": ["vision_nula", "dano_arena", "perdida_direccion"],
            "descripcion": "La arena te golpea desde todos lados."
        },
        "tormenta_fuego": {
            "modificadores": {"visibilidad": 0.4, "movimiento": 0.4},
            "efectos": ["dano_fuego", "calor_extremo", "vision_reducida"],
            "descripcion": "Llamas y ceniza llenan el aire."
        },
        "humedo": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 1.0},
            "efectos": ["humedad", "enfermedad_potencial"],
            "descripcion": "El aire esta cargado de humedad."
        },
        "bochornoso": {
            "modificadores": {"visibilidad": 0.95, "movimiento": 0.9},
            "efectos": ["fatiga", "incomodidad"],
            "descripcion": "El aire es pesado y dificil de respirar."
        },
        "frio": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 0.95},
            "efectos": ["frio", "congelacion_potencial"],
            "descripcion": "El frio cala hasta los huesos."
        },
        "estable": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 1.0},
            "efectos": ["clima_neutral"],
            "descripcion": "El clima es estable y predecible."
        },
        "oscuro": {
            "modificadores": {"visibilidad": 0.6, "movimiento": 0.9},
            "efectos": ["vision_reducida", "sigilo_mejorado"],
            "descripcion": "La oscuridad envuelve todo."
        },
        "gases": {
            "modificadores": {"visibilidad": 0.7, "movimiento": 0.8},
            "efectos": ["dano_toxico", "vision_reducida"],
            "descripcion": "Gases toxicos emanan de las paredes."
        },
        "inundacion": {
            "modificadores": {"visibilidad": 0.7, "movimiento": 0.5},
            "efectos": ["dificultad_movimiento", "peligro_ahogamiento"],
            "descripcion": "El agua sube rapidamente de nivel."
        },
        "avalancha": {
            "modificadores": {"visibilidad": 0.2, "movimiento": 0.3},
            "efectos": ["peligro_muerte", "vision_nula"],
            "descripcion": "Una avalancha se acerca!"
        },
        "plaga_insectos": {
            "modificadores": {"visibilidad": 0.8, "movimiento": 0.7},
            "efectos": ["dano_insectos", "enfermedad"],
            "descripcion": "Enjambres de insectos te rodean."
        },
        "espejismo": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 1.0},
            "efectos": ["vision_falsa", "confusion"],
            "descripcion": "El calor crea ilusiones en el horizonte."
        },
        "seco": {
            "modificadores": {"visibilidad": 1.0, "movimiento": 1.0},
            "efectos": ["sed_lenta"],
            "descripcion": "El aire es seco."
        },
        "granizo": {
            "modificadores": {"visibilidad": 0.7, "movimiento": 0.8},
            "efectos": ["dano_fisico", "vision_reducida"],
            "descripcion": "Granizo cae del cielo."
        },
        "tormenta_hielo": {
            "modificadores": {"visibilidad": 0.4, "movimiento": 0.5},
            "efectos": ["frio_extremo", "dano_fisico", "vision_reducida"],
            "descripcion": "El hielo cae con violencia."
        },
        "derrumbe": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 0.6},
            "efectos": ["peligro_fisico", "vision_reducida"],
            "descripcion": "El techo se debilita."
        },
        "inundacion_subterranea": {
            "modificadores": {"visibilidad": 0.6, "movimiento": 0.4},
            "efectos": ["peligro_ahogamiento", "dificultad_movimiento"],
            "descripcion": "El agua inunda los pasillos."
        },
        "terremoto": {
            "modificadores": {"visibilidad": 0.5, "movimiento": 0.3},
            "efectos": ["peligro_muerte", "derrumbe"],
            "descripcion": "La tierra tiembla violentamente!"
        }
    }
    
    # Fases del dia
    FASES_DIA = {
        "madrugada": {"horas": range(0, 5), "luz": 0.2, "descripcion": "La madrugada es oscura y silenciosa."},
        "amanecer": {"horas": range(5, 7), "luz": 0.5, "descripcion": "El sol comienza a asomar en el horizonte."},
        "dia": {"horas": range(7, 17), "luz": 1.0, "descripcion": "Es pleno dia."},
        "atardecer": {"horas": range(17, 20), "luz": 0.7, "descripcion": "El sol se pone tiñendo el cielo de naranja."},
        "anochecer": {"horas": range(20, 22), "luz": 0.4, "descripcion": "La luz se desvanece."},
        "noche": {"horas": range(22, 24), "luz": 0.1, "descripcion": "La noche cubre todo con su manto oscuro."}
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
    
    def generar_clima(self, bioma_key: str, contexto: str) -> EstadoClima:
        """Genera el clima actual para un bioma."""
        rng = self.seed.get_rng(f"clima_{contexto}")
        
        # Obtener climas disponibles para el bioma
        climas_bioma = self.CLIMA_POR_BIOMA.get(bioma_key, self.CLIMA_POR_BIOMA["bosque_ancestral"])
        
        # Determinar rareza del clima
        roll = rng.random()
        if roll < 0.05:  # 5% extremo
            rareza = "extremo"
        elif roll < 0.20:  # 15% raro
            rareza = "raro"
        else:  # 80% comun
            rareza = "comun"
        
        # Seleccionar clima
        climas_disponibles = climas_bioma.get(rareza, climas_bioma["comun"])
        tipo_clima = rng.choice(climas_disponibles)
        
        # Obtener efectos
        info_clima = self.EFECTOS_CLIMA.get(tipo_clima, self.EFECTOS_CLIMA["nublado"])
        
        # Determinar intensidad
        if rareza == "extremo":
            intensidad = rng.choice(["intenso", "extremo"])
        elif rareza == "raro":
            intensidad = rng.choice(["moderado", "intenso"])
        else:
            intensidad = rng.choice(["leve", "moderado"])
        
        # Duracion en turnos
        duracion = rng.randint(3, 10)
        
        return EstadoClima(
            tipo=tipo_clima,
            intensidad=intensidad,
            duracion=duracion,
            efectos=info_clima["efectos"],
            descripcion=info_clima["descripcion"]
        )
    
    def get_ciclo_dia_noche(self, hora: int) -> CicloDiaNoche:
        """Obtiene el estado del ciclo dia/noche."""
        hora = hora % 24
        
        for fase, info in self.FASES_DIA.items():
            if hora in info["horas"]:
                return CicloDiaNoche(
                    hora=hora,
                    fase=fase,
                    luz=info["luz"]
                )
        
        return CicloDiaNoche(hora=hora, fase="dia", luz=1.0)
    
    def avanzar_hora(self, hora_actual: int, horas: int = 1) -> CicloDiaNoche:
        """Avanza el tiempo y retorna el nuevo ciclo."""
        nueva_hora = (hora_actual + horas) % 24
        return self.get_ciclo_dia_noche(nueva_hora)
    
    def get_modificadores_clima(self, clima: EstadoClima) -> Dict:
        """Obtiene los modificadores del clima actual."""
        info = self.EFECTOS_CLIMA.get(clima.tipo, {})
        return info.get("modificadores", {"visibilidad": 1.0, "movimiento": 1.0})
    
    def get_efectos_combinados(self, clima: EstadoClima, ciclo: CicloDiaNoche) -> Dict:
        """Combina efectos del clima y ciclo dia/noche."""
        mods_clima = self.get_modificadores_clima(clima)
        
        # Visibilidad afectada por luz
        visibilidad = mods_clima.get("visibilidad", 1.0) * ciclo.luz
        
        # Movimiento base
        movimiento = mods_clima.get("movimiento", 1.0)
        
        # Efectos combinados
        efectos = clima.efectos.copy()
        
        # Agregar efectos de noche
        if ciclo.fase in ["noche", "madrugada"]:
            efectos.append("oscuridad")
            efectos.append("sigilo_mejorado")
        
        return {
            "visibilidad": round(visibilidad, 2),
            "movimiento": round(movimiento, 2),
            "efectos": efectos,
            "fase_dia": ciclo.fase,
            "descripcion_clima": clima.descripcion,
            "descripcion_fase": self.FASES_DIA.get(ciclo.fase, {}).get("descripcion", "")
        }
    
    def transicionar_clima(self, clima_actual: EstadoClima, bioma_key: str, contexto: str) -> EstadoClima:
        """Genera una transicion de clima."""
        rng = self.seed.get_rng(f"transicion_{contexto}")
        
        # Reducir duracion
        nueva_duracion = clima_actual.duracion - 1
        
        if nueva_duracion <= 0:
            # Generar nuevo clima
            return self.generar_clima(bioma_key, contexto)
        
        # Mantener clima actual con duracion reducida
        return EstadoClima(
            tipo=clima_actual.tipo,
            intensidad=clima_actual.intensidad,
            duracion=nueva_duracion,
            efectos=clima_actual.efectos,
            descripcion=clima_actual.descripcion
        )
    
    def get_climas_disponibles(self, bioma_key: str) -> Dict:
        """Retorna todos los climas disponibles para un bioma."""
        return self.CLIMA_POR_BIOMA.get(bioma_key, self.CLIMA_POR_BIOMA["bosque_ancestral"])