from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import random
import uuid
import json
import os


class TipoItem(Enum):
    ARMA = "arma"
    ARMADURA = "armadura"
    ACCESORIO = "accesorio"
    POCION = "pocion"
    CONSUMIBLE = "consumible"
    MATERIAL = "material"
    MISC = "misc"
    HERRAMIENTA = "herramienta"


class Rareza(Enum):
    COMUN = "comun"
    RARO = "raro"
    EPICO = "epico"
    LEGENDARIO = "legendario"
    UNICO = "unico"


class TipoEnemigo(Enum):
    NORMAL = "normal"
    ELITE = "elite"
    JEFE = "jefe"


DROP_PROBABILIDADES = {
    TipoEnemigo.NORMAL: {
        "comun": 80,
        "raro": 15,
        "epico": 4,
        "legendario": 1,
        "unico": 0,
    },
    TipoEnemigo.ELITE: {
        "comun": 40,
        "raro": 40,
        "epico": 15,
        "legendario": 5,
        "unico": 0,
    },
    TipoEnemigo.JEFE: {
        "comun": 0,
        "raro": 20,
        "epico": 50,
        "legendario": 25,
        "unico": 5,
    },
}

SPAWN_PESOS = {
    "normal": 75,
    "elite": 20,
    "jefe": 5,
}


class TipoEquipamiento(Enum):
    CASCO = "casco"
    PETO = "peto"
    GUANTES = "guantes"
    BOTAS = "botas"
    AMULETO = "amuleto"
    ANILLO = "anillo"
    ESCUDO = "escudo"
    ARMA_IZQUIERDA = "arma_izquierda"
    ARMA_DERECHA = "arma_derecha"


class TipoArma(Enum):
    ESPADA = "espada"
    ESPADON = "espadon"
    ARCO = "arco"
    BALLESTA = "ballesta"
    DAGA = "daga"
    CATALIZADOR = "catalizador"
    BASTON = "baston"
    HACHA = "hacha"


@dataclass
class Perk:
    id: str
    nombre: str
    tipo: str
    efecto: str
    valor: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "efecto": self.efecto,
            "valor": self.valor,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Perk":
        return Perk(
            id=data["id"],
            nombre=data["nombre"],
            tipo=data["tipo"],
            efecto=data["efecto"],
            valor=data["valor"],
        )


RARO_MODIFIERS = {
    Rareza.COMUN: {"damage_mult": 1.0, "durability_mult": 1.0},
    Rareza.RARO: {"damage_mult": 1.1, "durability_mult": 1.25},
    Rareza.EPICO: {"damage_mult": 1.25, "durability_mult": 1.5},
    Rareza.LEGENDARIO: {"damage_mult": 1.5, "durability_mult": 2.0},
    Rareza.UNICO: {"damage_mult": 2.0, "durability_mult": 2.5},
}

REPARACIONES_MAX = {
    Rareza.COMUN: 3,
    Rareza.RARO: 5,
    Rareza.EPICO: 8,
    Rareza.LEGENDARIO: 10,
    Rareza.UNICO: 15,
}


@dataclass
class ItemStats:
    dano_min: int = 0
    dano_max: int = 0
    dano_fuego: int = 0
    dano_hielo: int = 0
    dano_rayo: int = 0
    dano_veneno: int = 0
    defensa: int = 0
    resistencia: int = 0
    velocidad: int = 100
    critico: int = 0
    robo_vida: int = 0
    bloqueo: int = 0
    peso: int = 1
    valor: int = 0
    durabilidad_maxima: int = 100

    def aplicar_multiplicador_rareza(self, rareza: Rareza) -> "ItemStats":
        mult = RARO_MODIFIERS.get(rareza, RARO_MODIFIERS[Rareza.COMUN])
        self.dano_min = int(self.dano_min * mult["damage_mult"])
        self.dano_max = int(self.dano_max * mult["damage_mult"])
        self.durabilidad_maxima = int(self.durabilidad_maxima * mult["durability_mult"])
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dano_min": self.dano_min,
            "dano_max": self.dano_max,
            "dano_fuego": self.dano_fuego,
            "dano_hielo": self.dano_hielo,
            "dano_rayo": self.dano_rayo,
            "dano_veneno": self.dano_veneno,
            "defensa": self.defensa,
            "resistencia": self.resistencia,
            "velocidad": self.velocidad,
            "critico": self.critico,
            "robo_vida": self.robo_vida,
            "bloqueo": self.bloqueo,
            "peso": self.peso,
            "valor": self.valor,
            "durabilidad_maxima": self.durabilidad_maxima,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ItemStats":
        stats = ItemStats()
        for key, value in data.items():
            if hasattr(stats, key):
                setattr(stats, key, value)
        return stats


@dataclass
class ItemTemplate:
    id: str
    nombre: str
    tipo: TipoItem
    subtipo: str
    descripcion: str
    stackable: bool = False
    stack_max: int = 1
    rarity: Rareza = Rareza.COMUN
    stats: ItemStats = field(default_factory=ItemStats)
    perks: List[Perk] = field(default_factory=list)
    perks_negativos: List[Perk] = field(default_factory=list)
    requisitos: Dict[str, int] = field(default_factory=dict)
    tipo_arma: Optional[TipoArma] = None
    tipo_equipamiento: Optional[TipoEquipamiento] = None
    manos: int = 1
    efectos: List[str] = field(default_factory=list)

    def generar_instancia(self, generador_stats: bool = True) -> "ItemInstancia":
        instance_id = f"{self.id}_{uuid.uuid4().hex[:8]}"

        stats = ItemStats()
        if self.stats:
            stats = ItemStats.from_dict(self.stats.to_dict())

        if generador_stats:
            stats.aplicar_multiplicador_rareza(self.rarity)
            stats.durabilidad_maxima = stats.durabilidad_maxima
        else:
            stats.durabilidad_maxima = self.stats.durabilidad_maxima

        perks = [Perk.from_dict(p.to_dict()) for p in self.perks]
        perks_neg = [Perk.from_dict(p.to_dict()) for p in self.perks_negativos]

        return ItemInstancia(
            id=instance_id,
            id_template=self.id,
            nombre=self.nombre,
            tipo=self.tipo,
            subtipo=self.subtipo,
            descripcion=self.descripcion,
            rareza=self.rarity,
            cantidad=1,
            stackable=self.stackable,
            stats=stats,
            perks=perks,
            perks_negativos=perks_neg,
            durabilidad_actual=stats.durabilidad_maxima,
            numero_reparaciones=0,
            identificado=True,
            favorito=False,
            slot_inventario=None,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "subtipo": self.subtipo,
            "descripcion": self.descripcion,
            "stackable": self.stackable,
            "stack_max": self.stack_max,
            "rareza": self.rarity.value,
            "stats": self.stats.to_dict() if self.stats else {},
            "perks": [p.to_dict() for p in self.perks],
            "perks_negativos": [p.to_dict() for p in self.perks_negativos],
            "requisitos": self.requisitos,
            "tipo_arma": self.tipo_arma.value if self.tipo_arma else None,
            "tipo_equipamiento": self.tipo_equipamiento.value
            if self.tipo_equipamiento
            else None,
            "manos": self.manos,
            "efectos": self.efectos,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ItemTemplate":
        stats = (
            ItemStats.from_dict(data.get("stats", {}))
            if data.get("stats")
            else ItemStats()
        )

        perks = [Perk.from_dict(p) for p in data.get("perks", [])]
        perks_neg = [Perk.from_dict(p) for p in data.get("perks_negativos", [])]

        return ItemTemplate(
            id=data["id"],
            nombre=data["nombre"],
            tipo=TipoItem(data["tipo"]),
            subtipo=data["subtipo"],
            descripcion=data["descripcion"],
            stackable=data.get("stackable", False),
            stack_max=data.get("stack_max", 1),
            rarity=Rareza(data.get("rareza", "comun")),
            stats=stats,
            perks=perks,
            perks_negativos=perks_neg,
            requisitos=data.get("requisitos", {}),
            tipo_arma=TipoArma(data["tipo_arma"]) if data.get("tipo_arma") else None,
            tipo_equipamiento=TipoEquipamiento(data["tipo_equipamiento"])
            if data.get("tipo_equipamiento")
            else None,
            manos=data.get("manos", 1),
            efectos=data.get("efectos", []),
        )


@dataclass
class ItemInstancia:
    id: str
    id_template: str
    nombre: str
    tipo: TipoItem
    subtipo: str
    descripcion: str
    rareza: Rareza = Rareza.COMUN
    cantidad: int = 1
    stackable: bool = False
    stats: ItemStats = field(default_factory=ItemStats)
    perks: List[Perk] = field(default_factory=list)
    perks_negativos: List[Perk] = field(default_factory=list)
    durabilidad_actual: int = 100
    numero_reparaciones: int = 0
    identificado: bool = True
    favorito: bool = False
    slot_inventario: Optional[int] = None
    slot_equipamiento: Optional[str] = None

    def get_estado_durabilidad(self) -> str:
        if self.durabilidad_actual <= 0:
            return "roto"
        pct = (self.durabilidad_actual / self.stats.durabilidad_maxima) * 100
        if pct >= 76:
            return "perfecto"
        elif pct >= 51:
            return "usado"
        elif pct >= 26:
            return "gastado"
        else:
            return "daniado"

    def get_penalizacion_durabilidad(self) -> float:
        estado = self.get_estado_durabilidad()
        if estado == "perfecto" or estado == "usado":
            return 1.0
        elif estado == "gastado":
            return 0.9
        elif estado == "daniado":
            return 0.75
        return 0.0

    def puede_repararse(self) -> bool:
        return self.numero_reparaciones < REPARACIONES_MAX.get(self.rareza, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "id_template": self.id_template,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "subtipo": self.subtipo,
            "descripcion": self.descripcion,
            "rareza": self.rareza.value,
            "cantidad": self.cantidad,
            "stackable": self.stackable,
            "stats": self.stats.to_dict(),
            "perks": [p.to_dict() for p in self.perks],
            "perks_negativos": [p.to_dict() for p in self.perks_negativos],
            "durabilidad_actual": self.durabilidad_actual,
            "durabilidad_maxima": self.stats.durabilidad_maxima,
            "estado_durabilidad": self.get_estado_durabilidad(),
            "numero_reparaciones": self.numero_reparaciones,
            "identificado": self.identificado,
            "favorito": self.favorito,
            "slot_inventario": self.slot_inventario,
            "slot_equipamiento": self.slot_equipamiento,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ItemInstancia":
        stats = ItemStats.from_dict(data.get("stats", {}))
        perks = [Perk.from_dict(p) for p in data.get("perks", [])]
        perks_neg = [Perk.from_dict(p) for p in data.get("perks_negativos", [])]

        return ItemInstancia(
            id=data["id"],
            id_template=data["id_template"],
            nombre=data["nombre"],
            tipo=TipoItem(data["tipo"]),
            subtipo=data["subtipo"],
            descripcion=data["descripcion"],
            rareza=Rareza(data.get("rareza", "comun")),
            cantidad=data.get("cantidad", 1),
            stackable=data.get("stackable", False),
            stats=stats,
            perks=perks,
            perks_negativos=perks_neg,
            durabilidad_actual=data.get("durabilidad_actual", 100),
            numero_reparaciones=data.get("numero_reparaciones", 0),
            identificado=data.get("identificado", True),
            favorito=data.get("favorito", False),
            slot_inventario=data.get("slot_inventario"),
            slot_equipamiento=data.get("slot_equipamiento"),
        )


class GestorItems:
    def __init__(self):
        self.templates: Dict[str, ItemTemplate] = {}
        self._cargar_templates()

    def _cargar_templates(self):
        try:
            import json

            # Path relativo a este archivo
            current_dir = os.path.dirname(os.path.abspath(__file__))
            items_path = os.path.join(current_dir, "..", "data", "items.json")
            
            with open(items_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item_data in data:
                template = ItemTemplate.from_dict(item_data)
                self.templates[template.id] = template
        except Exception as e:
            print(f"Error cargando items: {e}")

    def get_template(self, item_id: str) -> Optional[ItemTemplate]:
        return self.templates.get(item_id)

    def crear_instancia(self, item_id: str) -> Optional[ItemInstancia]:
        template = self.get_template(item_id)
        if template:
            return template.generar_instancia()
        return None

    def generar_item_aleatorio(
        self, tipo: TipoItem = None, rareza: Rareza = None
    ) -> Optional[ItemInstancia]:
        if rareza is None:
            rareza = self._determinar_rareza_aleatoria()

        templates_filtrados = list(self.templates.values())
        if tipo:
            templates_filtrados = [t for t in templates_filtrados if t.tipo == tipo]

        if not templates_filtrados:
            return None

        template = random.choice(templates_filtrados)
        template.rarity = rareza
        return template.generar_instancia()

    def _determinar_rareza_aleatoria(self) -> Rareza:
        roll = random.random() * 100
        if roll < 60:
            return Rareza.COMUN
        elif roll < 85:
            return Rareza.RARO
        elif roll < 95:
            return Rareza.EPICO
        elif roll < 99:
            return Rareza.LEGENDARIO
        else:
            return Rareza.UNICO

    def _determinar_rareza_por_tipo_enemigo(self, tipo_enemigo: TipoEnemigo) -> Rareza:
        probabilidades = DROP_PROBABILIDADES.get(
            tipo_enemigo, DROP_PROBABILIDADES[TipoEnemigo.NORMAL]
        )
        roll = random.random() * 100
        acumulado = 0
        for rareza_str, probabilidad in probabilidades.items():
            acumulado += probabilidad
            if roll < acumulado:
                return Rareza(rareza_str)
        return Rareza.COMUN

    def generar_drop(
        self,
        tipo_enemigo: TipoEnemigo = TipoEnemigo.NORMAL,
        nivel_enemigo: int = 1,
        chance_drop: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Genera drops para un enemigo derrotado.

        Args:
            tipo_enemigo: Tipo de enemigo (normal, elite, jefe)
            nivel_enemigo: Nivel del enemigo (afecta oro)
            chance_drop: Probabilidad de que suelte algo (0.0 - 1.0)

        Returns:
            Dict con 'oro', 'items' y 'materiales'
        """
        resultado = {"oro": 0, "items": [], "materiales": []}

        if random.random() > chance_drop:
            return resultado

        oro_base = nivel_enemigo * random.randint(3, 8)
        multiplicador_oro = random.uniform(0.8, 1.2)
        resultado["oro"] = int(oro_base * multiplicador_oro)

        templates_armas = [
            t for t in self.templates.values() if t.tipo == TipoItem.ARMA
        ]
        templates_armaduras = [
            t for t in self.templates.values() if t.tipo == TipoItem.ARMADURA
        ]
        templates_accesorios = [
            t for t in self.templates.values() if t.tipo == TipoItem.ACCESORIO
        ]
        templates_pociones = [
            t for t in self.templates.values() if t.tipo == TipoItem.POCION
        ]
        templates_materiales = [
            t for t in self.templates.values() if t.tipo == TipoItem.MATERIAL
        ]

        num_drops = 0
        if tipo_enemigo == TipoEnemigo.NORMAL:
            num_drops = random.choices([0, 1], weights=[60, 40])[0]
        elif tipo_enemigo == TipoEnemigo.ELITE:
            num_drops = random.choices([0, 1, 2], weights=[30, 50, 20])[0]
        else:
            num_drops = random.choices([1, 2, 3], weights=[20, 50, 30])[0]

        for _ in range(num_drops):
            tipo_drop = random.choices(
                ["arma", "armadura", "accesorio", "pocion", "material"],
                weights=[25, 25, 10, 25, 15],
            )[0]

            if tipo_drop == "arma" and templates_armas:
                template = random.choice(templates_armas)
                rareza = self._determinar_rareza_por_tipo_enemigo(tipo_enemigo)
                template.rarity = rareza
                instancia = template.generar_instancia()
                resultado["items"].append(instancia.to_dict())

            elif tipo_drop == "armadura" and templates_armaduras:
                template = random.choice(templates_armaduras)
                rareza = self._determinar_rareza_por_tipo_enemigo(tipo_enemigo)
                template.rarity = rareza
                instancia = template.generar_instancia()
                resultado["items"].append(instancia.to_dict())

            elif tipo_drop == "accesorio" and templates_accesorios:
                template = random.choice(templates_accesorios)
                rareza = self._determinar_rareza_por_tipo_enemigo(tipo_enemigo)
                template.rarity = rareza
                instancia = template.generar_instancia()
                resultado["items"].append(instancia.to_dict())

            elif tipo_drop == "pocion" and templates_pociones:
                template = random.choice(templates_pociones)
                instancia = template.generar_instancia()
                instancia.cantidad = random.randint(1, 3)
                resultado["items"].append(instancia.to_dict())

            elif tipo_drop == "material" and templates_materiales:
                template = random.choice(templates_materiales)
                instancia = template.generar_instancia()
                cantidad = (
                    random.randint(1, 3) if tipo_enemigo == TipoEnemigo.JEFE else 1
                )
                instancia.cantidad = cantidad
                resultado["materiales"].append(instancia.to_dict())

        return resultado

    def generar_drop_desde_enemigo(
        self,
        categoria_enemigo: str = "bestia",
        es_elite: bool = False,
        es_jefe: bool = False,
        nivel: int = 1,
        forzar_tipo: str = None,
    ) -> Dict[str, Any]:
        """Wrapper para generar drops desde datos de enemigo.

        Args:
            categoria_enemigo: Categoría del enemigo (bestia, humanoide, etc.)
            es_elite: Si se fuerza que sea elite
            es_jefe: Si se fuerza que sea jefe
            nivel: Nivel del enemigo
            forzar_tipo: Forzar un tipo específico ('normal', 'elite', 'jefe')

        Returns:
            Dict con 'oro', 'items' y 'materiales'
        """
        if forzar_tipo:
            tipo_str = forzar_tipo
        elif es_jefe:
            tipo_str = "jefe"
        elif es_elite:
            tipo_str = "elite"
        else:
            tipo_str = random.choices(
                list(SPAWN_PESOS.keys()), weights=list(SPAWN_PESOS.values())
            )[0]

        tipo_enemigo = TipoEnemigo(tipo_str)

        if tipo_enemigo == TipoEnemigo.JEFE:
            chance = 1.0
        elif tipo_enemigo == TipoEnemigo.ELITE:
            chance = 0.8
        else:
            chance = 0.4

        return self.generar_drop(tipo_enemigo, nivel, chance)


gestor_items = GestorItems()
