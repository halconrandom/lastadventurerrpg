"""
GoalEngine — Sistema de metas para NPCs.

Principios:
- Cada NPC tiene metas según su rol (tabernero, guardia, mercader...).
- Las metas tienen prioridad y pueden bloquearse por condiciones.
- El horario del mundo afecta qué meta está activa.
- El GoalEngine evalúa si el jugador ayuda u obstaculiza la meta activa.
- El LLM recibe la meta activa como contexto para dar respuestas coherentes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclass de Meta
# ---------------------------------------------------------------------------
@dataclass
class Goal:
    tipo: str               # "vender", "descansar", "patrullar", etc.
    descripcion: str        # Texto legible para el prompt
    prioridad: int          # 1 (baja) a 10 (crítica)
    horas_activa: List[int] = field(default_factory=list)  # [] = siempre activa
    bloqueada: bool = False

    def to_dict(self) -> Dict:
        return {
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "horas_activa": self.horas_activa
        }


# ---------------------------------------------------------------------------
# Metas predefinidas por rol
# ---------------------------------------------------------------------------
METAS_POR_ROL: Dict[str, List[Goal]] = {
    "tabernero": [
        Goal("atender_clientes",  "Atender a los clientes y vender bebidas",       prioridad=8, horas_activa=list(range(8, 24))),
        Goal("limpiar_taberna",   "Limpiar la taberna antes de abrir",              prioridad=5, horas_activa=[6, 7]),
        Goal("descansar",         "Dormir y recuperar fuerzas",                     prioridad=9, horas_activa=list(range(0, 6))),
        Goal("conseguir_suministros", "Conseguir más barriles de cerveza",          prioridad=4),
    ],
    "mercader": [
        Goal("vender_mercancias", "Vender sus productos al mejor precio posible",   prioridad=9, horas_activa=list(range(8, 20))),
        Goal("conseguir_info",    "Obtener información sobre rutas comerciales",    prioridad=5),
        Goal("descansar",         "Descansar en la posada",                         prioridad=8, horas_activa=list(range(21, 24)) + list(range(0, 7))),
        Goal("negociar_precios",  "Negociar mejores precios con proveedores",       prioridad=6, horas_activa=list(range(9, 12))),
    ],
    "guardia": [
        Goal("patrullar",         "Patrullar el perímetro asignado",                prioridad=8, horas_activa=list(range(6, 22))),
        Goal("proteger_ciudad",   "Mantener el orden y la seguridad",               prioridad=10),
        Goal("descansar",         "Descansar en el cuartel",                        prioridad=7, horas_activa=list(range(22, 24)) + list(range(0, 6))),
        Goal("interrogar_sospechosos", "Investigar actividad sospechosa",           prioridad=6),
    ],
    "campesino": [
        Goal("cosechar",          "Trabajar los campos antes de que anochezca",     prioridad=8, horas_activa=list(range(6, 18))),
        Goal("vender_cosecha",    "Llevar la cosecha al mercado",                   prioridad=7, horas_activa=list(range(8, 14))),
        Goal("descansar",         "Descansar después de un día de trabajo",         prioridad=9, horas_activa=list(range(20, 24)) + list(range(0, 6))),
        Goal("reparar_herramientas", "Reparar las herramientas de labranza",        prioridad=3, horas_activa=[18, 19]),
    ],
    "herrero": [
        Goal("forjar",            "Forjar armas y armaduras en la fragua",          prioridad=8, horas_activa=list(range(7, 19))),
        Goal("vender_equipo",     "Vender el equipo fabricado",                     prioridad=7, horas_activa=list(range(9, 18))),
        Goal("descansar",         "Descansar y enfriar la fragua",                  prioridad=8, horas_activa=list(range(20, 24)) + list(range(0, 7))),
        Goal("conseguir_materiales", "Conseguir más hierro y carbón",               prioridad=5),
    ],
    "curandero": [
        Goal("atender_enfermos",  "Atender a los enfermos y heridos",               prioridad=9),
        Goal("preparar_pociones", "Preparar pociones y remedios",                   prioridad=7, horas_activa=list(range(6, 10))),
        Goal("recolectar_hierbas","Salir a recolectar hierbas medicinales",         prioridad=6, horas_activa=list(range(10, 14))),
        Goal("descansar",         "Descansar para estar alerta ante emergencias",   prioridad=8, horas_activa=list(range(22, 24)) + list(range(0, 6))),
    ],
    "aldeano": [
        Goal("trabajo_diario",    "Realizar las tareas cotidianas del día",         prioridad=6, horas_activa=list(range(7, 18))),
        Goal("socializar",        "Hablar con los vecinos en la plaza",             prioridad=4, horas_activa=list(range(12, 14)) + list(range(17, 20))),
        Goal("descansar",         "Descansar en casa",                              prioridad=8, horas_activa=list(range(21, 24)) + list(range(0, 7))),
    ],
}

# Meta por defecto si el rol no está definido
META_DEFAULT = Goal("existir", "Seguir con su vida cotidiana", prioridad=1)


# ---------------------------------------------------------------------------
# Evaluación de cómo el jugador afecta la meta
# ---------------------------------------------------------------------------
RELACION_INTENT_META: Dict[str, Dict[str, str]] = {
    # intent_tipo → { meta_tipo → efecto }
    "comercio": {
        "vender_mercancias": "ayuda",
        "atender_clientes":  "ayuda",
        "vender_equipo":     "ayuda",
        "vender_cosecha":    "ayuda",
    },
    "pregunta": {
        "conseguir_info":    "ayuda",
        "interrogar_sospechosos": "neutral",
    },
    "amenaza": {
        "patrullar":         "obstaculiza",
        "proteger_ciudad":   "obstaculiza",
        "atender_clientes":  "obstaculiza",
    },
    "queja_fuerte": {
        "atender_clientes":  "obstaculiza",
        "vender_mercancias": "obstaculiza",
    },
}


class GoalEngine:
    """
    Gestiona las metas activas de un NPC según su rol y la hora del mundo.
    """

    def get_meta_activa(self, rol: str, hora: int) -> Goal:
        """
        Devuelve la meta de mayor prioridad que esté activa en la hora actual.
        """
        metas = METAS_POR_ROL.get(rol, [META_DEFAULT])

        # Filtrar metas activas en esta hora
        activas = [
            m for m in metas
            if not m.bloqueada and (not m.horas_activa or hora in m.horas_activa)
        ]

        if not activas:
            return META_DEFAULT

        # Retornar la de mayor prioridad
        return max(activas, key=lambda m: m.prioridad)

    def evaluar_jugador(self, meta: Goal, intent_tipo: str) -> str:
        """
        Evalúa si el jugador ayuda, obstaculiza o es neutral respecto a la meta.
        Retorna: "ayuda" | "obstaculiza" | "neutral"
        """
        relaciones = RELACION_INTENT_META.get(intent_tipo, {})
        return relaciones.get(meta.tipo, "neutral")

    def describir_actitud(self, meta: Goal, efecto_jugador: str) -> str:
        """
        Genera una descripción de la actitud del NPC hacia el jugador
        basada en si le ayuda o no con su meta. Para inyectar en el prompt.
        """
        if efecto_jugador == "ayuda":
            return f"Este forastero podría ayudarme a {meta.descripcion.lower()}."
        elif efecto_jugador == "obstaculiza":
            return f"Este forastero me está interrumpiendo. Necesito {meta.descripcion.lower()}."
        else:
            return f"Estoy ocupado: {meta.descripcion.lower()}."
