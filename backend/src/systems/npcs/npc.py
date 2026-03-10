from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from systems.npcs.emotion_engine import EstadoEmocional

class EstadoVital(Enum):
    VIVO = "vivo"
    MUERTO = "muerto"
    DESAPARECIDO = "desaparecido"
    PRESO = "preso"
    HERIDO = "herido"
    ENFERMO = "enfermo"

@dataclass
class Personalidad:
    rasgos: List[str] = field(default_factory=list)
    valores: List[str] = field(default_factory=list)
    sliders: Dict[str, float] = field(default_factory=lambda: {
        "agresividad": 0.5,
        "empatía": 0.5,
        "codicia": 0.5,
        "chisme": 0.5,
        "valentía": 0.5,
        "honor": 0.5,
        "paciencia": 0.5,
        "supersticion": 0.5
    })
    # EJES DE CONDUCTA PERSISTENTE (-100 a 100)
    moralidad: int = 0      # Malvado <-> Heroico
    sociabilidad: int = 0   # Ermitaño <-> Extrovertido
    templanza: int = 0      # Impulsivo <-> Calculador
    
    tono_voz: str = "neutral"
    muletillas: List[str] = field(default_factory=list)
    registro_voz: str = "coloquial"

    def to_dict(self) -> Dict:
        return {
            "rasgos": self.rasgos,
            "valores": self.valores,
            "sliders": self.sliders,
            "conducta": {
                "moralidad": self.moralidad,
                "sociabilidad": self.sociabilidad,
                "templanza": self.templanza
            },
            "voz": {
                "tono": self.tono_voz,
                "muletillas": self.muletillas,
                "registro": self.registro_voz
            }
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Personalidad':
        voz = data.get("voz", {})
        conducta = data.get("conducta", {})
        return cls(
            rasgos=data.get("rasgos", []),
            valores=data.get("valores", []),
            sliders=data.get("sliders", {}),
            moralidad=conducta.get("moralidad", 0),
            sociabilidad=conducta.get("sociabilidad", 0),
            templanza=conducta.get("templanza", 0),
            tono_voz=voz.get("tono", "neutral"),
            muletillas=voz.get("muletillas", []),
            registro_voz=voz.get("registro", "coloquial")
        )

@dataclass
class EstadoNPC:
    vital: EstadoVital = EstadoVital.VIVO
    hp: int = 100
    hp_max: int = 100
    heridas: List[str] = field(default_factory=list)
    oro: int = 0
    deudas: List[Dict] = field(default_factory=list)
    emocion_actual: str = "neutral"
    emocion_intensidad: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "vital": self.vital.value,
            "salud": {"hp": self.hp, "hp_max": self.hp_max, "heridas": self.heridas},
            "riqueza": {"oro": self.oro, "deudas": self.deudas},
            "emocion": {"estado": self.emocion_actual, "intensidad": self.emocion_intensidad}
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'EstadoNPC':
        salud = data.get("salud", {})
        riqueza = data.get("riqueza", {})
        emocion = data.get("emocion", {})
        return cls(
            vital=EstadoVital(data.get("vital", "vivo")),
            hp=salud.get("hp", 100),
            hp_max=salud.get("hp_max", 100),
            heridas=salud.get("heridas", []),
            oro=riqueza.get("oro", 0),
            deudas=riqueza.get("deudas", []),
            emocion_actual=emocion.get("estado", "neutral"),
            emocion_intensidad=emocion.get("intensidad", 0.0)
        )

@dataclass
class UbicacionNPC:
    tile: Tuple[int, int] = (0, 0)
    subtile: Tuple[int, int] = (0, 0)
    ubicacion_id: Optional[str] = None
    interior_id: Optional[str] = None
    modo: str = "mundial" # "mundial" o "local"

    def to_dict(self) -> Dict:
        return {
            "modo": self.modo,
            "tile": list(self.tile),
            "subtile": list(self.subtile),
            "ubicacion_id": self.ubicacion_id,
            "interior_id": self.interior_id
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'UbicacionNPC':
        return cls(
            modo=data.get("modo", "mundial"),
            tile=tuple(data.get("tile", [0, 0])),
            subtile=tuple(data.get("subtile", [0, 0])),
            ubicacion_id=data.get("ubicacion_id"),
            interior_id=data.get("interior_id")
        )

@dataclass
class Rutina:
    zona_base_id: str
    agenda_diaria: List[Dict] = field(default_factory=list)
    excepciones: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "zona_base_id": self.zona_base_id,
            "agenda_diaria": self.agenda_diaria,
            "excepciones": self.excepciones
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Rutina':
        return cls(
            zona_base_id=data.get("zona_base_id", ""),
            agenda_diaria=data.get("agenda_diaria", []),
            excepciones=data.get("excepciones", [])
        )

@dataclass
class MemoriaNPC:
    eventos: List[Dict] = field(default_factory=list)
    rumores: List[Dict] = field(default_factory=list)
    resumen_general: str = ""
    resumen_jugador: str = ""
    ultimas_interacciones: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "eventos": self.eventos,
            "rumores": self.rumores,
            "indice": {
                "resumen_general": self.resumen_general,
                "resumen_jugador": self.resumen_jugador,
                "ultimas_interacciones": self.ultimas_interacciones
            }
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoriaNPC':
        indice = data.get("indice", {})
        return cls(
            eventos=data.get("eventos", []),
            rumores=data.get("rumores", []),
            resumen_general=indice.get("resumen_general", ""),
            resumen_jugador=indice.get("resumen_jugador", ""),
            ultimas_interacciones=indice.get("ultimas_interacciones", [])
        )

@dataclass
class RelacionJugador:
    reputacion_valor: int = 0
    reputacion_estado: str = "neutral"
    confianza: int = 50
    respeto: int = 50
    miedo: int = 0
    deuda: int = 0
    romance: int = 0
    eventos_compartidos: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "reputacion": {"valor": self.reputacion_valor, "estado": self.reputacion_estado},
            "opiniones": {
                "confianza": self.confianza,
                "respeto": self.respeto,
                "miedo": self.miedo,
                "deuda": self.deuda,
                "romance": self.romance
            },
            "eventos": self.eventos_compartidos
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'RelacionJugador':
        rep = data.get("reputacion", {})
        op = data.get("opiniones", {})
        return cls(
            reputacion_valor=rep.get("valor", 0),
            reputacion_estado=rep.get("estado", "neutral"),
            confianza=op.get("confianza", 50),
            respeto=op.get("respeto", 50),
            miedo=op.get("miedo", 0),
            deuda=op.get("deuda", 0),
            romance=op.get("romance", 0),
            eventos_compartidos=data.get("eventos", [])
        )

@dataclass
class NPC:
    id: str
    nombre: str
    genero: str
    raza: str
    alias: List[str] = field(default_factory=list)
    
    # Origen
    año_nacimiento: int = 0
    region_origen_id: Optional[str] = None
    ubicacion_origen_id: Optional[str] = None
    linaje: Dict[str, Any] = field(default_factory=lambda: {"padre": None, "madre": None, "familia": []})
    
    # Rol
    rol_tipo: str = "aldeano"
    rol_subtipo: str = "comun"
    faccion_id: Optional[str] = None
    servicios: List[str] = field(default_factory=list)
    
    # Sistemas
    personalidad: Personalidad = field(default_factory=Personalidad)
    estado: EstadoNPC = field(default_factory=EstadoNPC)
    ubicacion: UbicacionNPC = field(default_factory=UbicacionNPC)
    rutina: Rutina = field(default_factory=lambda: Rutina(zona_base_id=""))
    relacion_jugador: RelacionJugador = field(default_factory=RelacionJugador)
    relaciones_npcs: Dict[str, Dict] = field(default_factory=dict)
    
    # Inventario
    inventario_tipo: str = "personal"
    stock: List[Dict] = field(default_factory=list)
    multiplicador_precios: float = 1.0
    
    # Memoria
    memoria: MemoriaNPC = field(default_factory=MemoriaNPC)

    # Emoción (gestionada por EmotionEngine)
    estado_emocional: EstadoEmocional = field(default_factory=EstadoEmocional)
    
    # Flags
    conocido_por_jugador: bool = False
    importante: bool = False
    es_unico: bool = False
    version: str = "1.0"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "alias": self.alias,
            "genero": self.genero,
            "raza": self.raza,
            "origen": {
                "nacimiento": {
                    "año": self.año_nacimiento,
                    "region_id": self.region_origen_id,
                    "ubicacion_id": self.ubicacion_origen_id
                },
                "linaje": self.linaje
            },
            "rol": {
                "tipo": self.rol_tipo,
                "subtipo": self.rol_subtipo,
                "faccion_id": self.faccion_id,
                "servicios": self.servicios
            },
            "personalidad": self.personalidad.to_dict(),
            "estado": self.estado.to_dict(),
            "ubicacion": self.ubicacion.to_dict(),
            "rutina": self.rutina.to_dict(),
            "relaciones": {
                "jugador": self.relacion_jugador.to_dict(),
                "npcs": self.relaciones_npcs
            },
            "inventario": {
                "tipo": self.inventario_tipo,
                "stock": self.stock,
                "tabla_precios": {"multiplicador": self.multiplicador_precios}
            },
            "memoria": self.memoria.to_dict(),
            "estado_emocional": self.estado_emocional.to_dict(),
            "flags": {
                "conocido_por_jugador": self.conocido_por_jugador,
                "importante": self.importante,
                "es_unico": self.es_unico
            },
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'NPC':
        origen = data.get("origen", {})
        nacimiento = origen.get("nacimiento", {})
        rol = data.get("rol", {})
        rel = data.get("relaciones", {})
        inv = data.get("inventario", {})
        flags = data.get("flags", {})
        
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            alias=data.get("alias", []),
            genero=data["genero"],
            raza=data["raza"],
            año_nacimiento=nacimiento.get("año", 0),
            region_origen_id=nacimiento.get("region_id"),
            ubicacion_origen_id=nacimiento.get("ubicacion_id"),
            linaje=origen.get("linaje", {"padre": None, "madre": None, "familia": []}),
            rol_tipo=rol.get("tipo", "aldeano"),
            rol_subtipo=rol.get("subtipo", "comun"),
            faccion_id=rol.get("faccion_id"),
            servicios=rol.get("servicios", []),
            personalidad=Personalidad.from_dict(data.get("personalidad", {})),
            estado=EstadoNPC.from_dict(data.get("estado", {})),
            ubicacion=UbicacionNPC.from_dict(data.get("ubicacion", {})),
            rutina=Rutina.from_dict(data.get("rutina", {})),
            relacion_jugador=RelacionJugador.from_dict(rel.get("jugador", {})),
            relaciones_npcs=rel.get("npcs", {}),
            inventario_tipo=inv.get("tipo", "personal"),
            stock=inv.get("stock", []),
            multiplicador_precios=inv.get("tabla_precios", {}).get("multiplicador", 1.0),
            memoria=MemoriaNPC.from_dict(data.get("memoria", {})),
            estado_emocional=EstadoEmocional.from_dict(data.get("estado_emocional", {})),
            conocido_por_jugador=flags.get("conocido_por_jugador", False),
            importante=flags.get("importante", False),
            es_unico=flags.get("es_unico", False),
            version=data.get("version", "1.0")
        )
