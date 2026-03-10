from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from .items import (
    ItemInstancia,
    ItemTemplate,
    gestor_items,
    TipoItem,
    Rareza,
    TipoEquipamiento,
)


SLOTS_EQUIPAMIENTO = [
    "casco",
    "peto",
    "guantes",
    "botas",
    "amuleto",
    "anillo_1",
    "anillo_2",
    "escudo",
    "mano_izquierda",
    "mano_derecha",
]

SLOTS_ALFORJAS_DEFAULT = 10
SLOTS_ALFORJAS_MAX = 30

STACK_LIMITS = {
    TipoItem.POCION: 10,
    TipoItem.CONSUMIBLE: 10,
    TipoItem.MATERIAL: 50,
    TipoItem.MISC: 5,
}


@dataclass
class Inventario:
    alforjas: List[Optional[ItemInstancia]] = field(default_factory=list)
    equipamiento: Dict[str, Optional[ItemInstancia]] = field(default_factory=dict)
    slots_maximos: int = SLOTS_ALFORJAS_DEFAULT
    oro: int = 0

    def __post_init__(self):
        if not self.alforjas:
            self.alforjas = [None] * self.slots_maximos
        if not self.equipamiento:
            self.equipamiento = {slot: None for slot in SLOTS_EQUIPAMIENTO}

    def get_item(self, ubicacion: str, indice: int = None) -> Optional[ItemInstancia]:
        if ubicacion == "alforjas" and indice is not None:
            if 0 <= indice < len(self.alforjas):
                return self.alforjas[indice]
        elif ubicacion == "equipamiento":
            return self.equipamiento.get(indice)
        return None

    def agregar_item(self, item: ItemInstancia) -> tuple[bool, str]:
        if item.stackable and item.tipo in STACK_LIMITS:
            max_stack = STACK_LIMITS[item.tipo]
            for i, slot_item in enumerate(self.alforjas):
                if slot_item and slot_item.id_template == item.id_template:
                    if slot_item.cantidad < max_stack:
                        espacio = max_stack - slot_item.cantidad
                        cantidad_transferir = min(item.cantidad, espacio)
                        slot_item.cantidad += cantidad_transferir
                        item.cantidad -= cantidad_transferir
                        if item.cantidad <= 0:
                            return True, "Item apilado correctamente"
                        continue

        for i, slot in enumerate(self.alforjas):
            if slot is None:
                self.alforjas[i] = item
                item.slot_inventario = i
                return True, "Item añadido correctamente"

        return False, "Inventario lleno"

    def remover_item(self, ubicacion: str, indice: int) -> Optional[ItemInstancia]:
        if ubicacion == "alforjas":
            if 0 <= indice < len(self.alforjas):
                item = self.alforjas[indice]
                self.alforjas[indice] = None
                if item:
                    item.slot_inventario = None
                return item
        elif ubicacion == "equipamiento":
            item = self.equipamiento.get(indice)
            if item:
                item.slot_equipamiento = None
            self.equipamiento[indice] = None
            return item
        return None

    def mover_item(
        self, origen: str, indice_origen: int, destino: str, indice_destino: int
    ) -> tuple[bool, str]:
        item_origen = self.get_item(origen, indice_origen)
        if not item_origen:
            return False, "Origen inválido"

        if destino == "alforjas":
            if indice_destino < 0 or indice_destino >= len(self.alforjas):
                return False, "Destino inválido"
            item_destino = self.alforjas[indice_destino]

            if (
                item_destino
                and item_origen.stackable
                and item_destino.id_template == item_origen.id_template
            ):
                max_stack = STACK_LIMITS.get(item_origen.tipo, 1)
                espacio = max_stack - item_destino.cantidad
                if espacio > 0:
                    cantidad_transferir = min(item_origen.cantidad, espacio)
                    item_destino.cantidad += cantidad_transferir
                    item_origen.cantidad -= cantidad_transferir
                    if item_origen.cantidad <= 0:
                        self.remover_item(origen, indice_origen)
                    return True, "Items combinados"

            self.alforjas[indice_origen] = item_destino
            self.alforjas[indice_destino] = item_origen
            item_origen.slot_inventario = indice_destino
            if item_destino:
                item_destino.slot_inventario = indice_origen
            return True, "Item movido"

        elif destino == "equipamiento":
            return self.equipar_item(indice_origen, indice_destino)

        return False, "Destino inválido"

    def equipar_item(
        self, indice_alforjas: int, slot_equipamiento: str
    ) -> tuple[bool, str]:
        if indice_alforjas < 0 or indice_alforjas >= len(self.alforjas):
            return False, "Slot de alforjas inválido"

        item = self.alforjas[indice_alforjas]
        if not item:
            return False, "No hay item en ese slot"

        if slot_equipamiento not in SLOTS_EQUIPAMIENTO:
            return False, "Slot de equipamiento inválido"

        if item.tipo == TipoItem.ARMA:
            if item.stats.peso > 15:
                return False, "Arma demasiado pesada para equipar"

        item_actual = self.equipamiento.get(slot_equipamiento)
        if item_actual:
            self.equipamiento[slot_equipamiento] = item
            item.slot_equipamiento = slot_equipamiento
            self.agregar_item(item_actual)
        else:
            self.equipamiento[slot_equipamiento] = item
            item.slot_equipamiento = slot_equipamiento

        self.alforjas[indice_alforjas] = None
        item.slot_inventario = None

        return True, f"Item equipado en {slot_equipamiento}"

    def desequipar_item(
        self, slot_equipamiento: str, indice_alforjas: int = None
    ) -> tuple[bool, str]:
        item = self.equipamiento.get(slot_equipamiento)
        if not item:
            return False, "No hay item equipado"

        self.equipamiento[slot_equipamiento] = None
        item.slot_equipamiento = None

        if indice_alforjas is not None and 0 <= indice_alforjas < len(self.alforjas):
            if self.alforjas[indice_alforjas] is None:
                self.alforjas[indice_alforjas] = item
                item.slot_inventario = indice_alforjas
                return True, "Item desequipado"

        resultado, mensaje = self.agregar_item(item)
        if not resultado:
            self.equipamiento[slot_equipamiento] = item
            item.slot_equipamiento = slot_equipamiento
        return resultado, mensaje

    def usar_item(self, indice: int) -> tuple[bool, str]:
        if indice < 0 or indice >= len(self.alforjas):
            return False, "Slot inválido"

        item = self.alforjas[indice]
        if not item:
            return False, "No hay item"

        if item.tipo == TipoItem.POCION or item.tipo == TipoItem.CONSUMIBLE:
            if item.cantidad > 1:
                item.cantidad -= 1
                return True, f"Usado 1 de {item.nombre}"
            else:
                self.alforjas[indice] = None
                return True, f"Usado {item.nombre}"

        return False, "Item no usable"

    def tirar_item(self, indice: int) -> tuple[bool, str]:
        if indice < 0 or indice >= len(self.alforjas):
            return False, "Slot inválido"

        item = self.alforjas[indice]
        if not item:
            return False, "No hay item"

        if item.favorito:
            return False, "No puedes tirar items favoritos"

        self.alforjas[indice] = None
        return True, f"Tirado {item.nombre}"

    def toggle_favorito(self, indice: int) -> tuple[bool, str]:
        if indice < 0 or indice >= len(self.alforjas):
            return False, "Slot inválido"

        item = self.alforjas[indice]
        if not item:
            return False, "No hay item"

        item.favorito = not item.favorito
        estado = "marcado" if item.favorito else "desmarcado"
        return True, f"Favorito {estado}"

    def ampliar_inventario(self, slots: int) -> tuple[bool, str]:
        if self.slots_maximos + slots > SLOTS_ALFORJAS_MAX:
            return False, f"Máximo {SLOTS_ALFORJAS_MAX} slots"

        self.slots_maximos += slots
        self.alforjas.extend([None] * slots)
        return True, f"Inventario ampliado a {self.slots_maximos} slots"

    def get_peso_total(self) -> int:
        peso = 0
        for item in self.alforjas:
            if item:
                peso += item.stats.peso * item.cantidad
        for item in self.equipamiento.values():
            if item:
                peso += item.stats.peso
        return peso

    def get_stats_equipados(self) -> Dict[str, int]:
        stats = {
            "ataque": 0,
            "defensa": 0,
            "velocidad": 100,
            "critico": 0,
            "resistencia": 0,
            "robo_vida": 0,
            "bloqueo": 0,
        }

        for item in self.equipamiento.values():
            if item and item.durabilidad_actual > 0:
                mult = item.get_penalizacion_durabilidad()
                stats["ataque"] += int(
                    (item.stats.dano_min + item.stats.dano_max) / 2 * mult
                )
                stats["defensa"] += int(item.stats.defensa * mult)
                stats["velocidad"] = int(
                    stats["velocidad"] * (item.stats.velocidad / 100) * mult
                )
                stats["critico"] += int(item.stats.critico * mult)
                stats["resistencia"] += item.stats.resistencia
                stats["robo_vida"] += item.stats.robo_vida
                stats["bloqueo"] += item.stats.bloqueo

        return stats

    def get_items_equipados_list(self) -> List[Dict[str, Any]]:
        items = []
        for slot, item in self.equipamiento.items():
            if item:
                items.append({"slot": slot, "item": item.to_dict()})
        return items

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alforjas": [item.to_dict() if item else None for item in self.alforjas],
            "equipamiento": {
                slot: item.to_dict() if item else None
                for slot, item in self.equipamiento.items()
            },
            "slots_maximos": self.slots_maximos,
            "slots_usados": sum(1 for s in self.alforjas if s is not None),
            "oro": self.oro,
            "peso_total": self.get_peso_total(),
            "stats_equipados": self.get_stats_equipados(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Inventario":
        alforjas = []
        for item_data in data.get("alforjas", []):
            if item_data:
                alforjas.append(ItemInstancia.from_dict(item_data))
            else:
                alforjas.append(None)

        equipamiento = {}
        for slot, item_data in data.get("equipamiento", {}).items():
            if item_data:
                equipamiento[slot] = ItemInstancia.from_dict(item_data)
            else:
                equipamiento[slot] = None

        inventario = Inventario(
            alforjas=alforjas,
            equipamiento=equipamiento,
            slots_maximos=data.get("slots_maximos", SLOTS_ALFORJAS_DEFAULT),
            oro=data.get("oro", 0),
        )

        return inventario


class GestorInventario:
    def __init__(self, slot: int):
        self.slot = slot
        self.inventario: Optional[Inventario] = None

    def cargar_inventario(self, data: Dict[str, Any]) -> bool:
        try:
            self.inventario = Inventario.from_dict(data)
            return True
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            self.inventario = Inventario()
            return False

    def guardar_inventario(self) -> Dict[str, Any]:
        if self.inventario:
            return self.inventario.to_dict()
        return Inventario().to_dict()

    def agregar_item_por_id(self, item_id: str, cantidad: int = 1) -> tuple[bool, str]:
        if not self.inventario:
            return False, "Inventario no cargado"

        template = gestor_items.get_template(item_id)
        if not template:
            return False, f"Item {item_id} no encontrado"

        for _ in range(cantidad):
            instancia = template.generar_instancia()
            ok, msg = self.inventario.agregar_item(instancia)
            if not ok:
                return False, msg

        return True, f"Añadido {cantidad}x {template.nombre}"

    def get_inventario(self) -> Optional[Inventario]:
        return self.inventario

    def crear_inventario_inicial(self) -> Inventario:
        self.inventario = Inventario()
        return self.inventario


# Cache de gestores por slot
_gestores: Dict[int, GestorInventario] = {}


def get_gestor(slot: int) -> GestorInventario:
    """Obtiene o crea un gestor de inventario para un slot."""
    if slot not in _gestores:
        _gestores[slot] = GestorInventario(slot)
    return _gestores[slot]
