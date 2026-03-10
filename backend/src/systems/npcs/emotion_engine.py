"""
EmotionEngine — Sistema de emociones con inercia para NPCs.

Principios:
- Las emociones NO saltan de un extremo al otro instantáneamente.
- Cada transición tiene un umbral de intensidad para activarse.
- Si no hay transición definida para un evento, la emoción no cambia.
- La intensidad decae con el tiempo (tick de mundo).
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# Emociones disponibles
# ---------------------------------------------------------------------------
EMOCIONES = {
    "neutral",
    "cauteloso",
    "molesto",
    "furioso",
    "feliz",
    "desconfiado",
    "asustado",
    "aliviado",
    "curioso",
    "triste",
}

# ---------------------------------------------------------------------------
# Tabla de transiciones
# Formato: (emocion_actual, evento) → (nueva_emocion, intensidad_resultante)
#
# Eventos posibles (generados por IntentClassifier):
#   saludo, queja_leve, queja_fuerte, amenaza, elogio,
#   comercio, pregunta, disculpa, silencio, agresion_fisica
# ---------------------------------------------------------------------------
TRANSICIONES: Dict[Tuple[str, str], Tuple[str, float]] = {
    # Desde neutral
    ("neutral",     "saludo"):          ("neutral",      0.0),
    ("neutral",     "queja_leve"):      ("cauteloso",    0.3),
    ("neutral",     "queja_fuerte"):    ("molesto",      0.5),
    ("neutral",     "amenaza"):         ("asustado",     0.6),
    ("neutral",     "elogio"):          ("feliz",        0.4),
    ("neutral",     "comercio"):        ("curioso",      0.2),
    ("neutral",     "pregunta"):        ("curioso",      0.2),
    ("neutral",     "agresion_fisica"): ("furioso",      0.9),

    # Desde cauteloso
    ("cauteloso",   "saludo"):          ("neutral",      0.1),
    ("cauteloso",   "queja_leve"):      ("molesto",      0.4),
    ("cauteloso",   "queja_fuerte"):    ("molesto",      0.7),
    ("cauteloso",   "amenaza"):         ("asustado",     0.7),
    ("cauteloso",   "elogio"):          ("neutral",      0.1),
    ("cauteloso",   "disculpa"):        ("neutral",      0.2),
    ("cauteloso",   "agresion_fisica"): ("furioso",      0.9),

    # Desde molesto
    ("molesto",     "saludo"):          ("molesto",      0.3),  # No se calma con un saludo
    ("molesto",     "queja_leve"):      ("molesto",      0.6),
    ("molesto",     "queja_fuerte"):    ("furioso",      0.7),
    ("molesto",     "amenaza"):         ("furioso",      0.8),
    ("molesto",     "elogio"):          ("cauteloso",    0.2),
    ("molesto",     "disculpa"):        ("cauteloso",    0.3),
    ("molesto",     "comercio"):        ("molesto",      0.4),
    ("molesto",     "agresion_fisica"): ("furioso",      1.0),

    # Desde furioso
    ("furioso",     "saludo"):          ("furioso",      0.7),  # No se calma fácil
    ("furioso",     "queja_leve"):      ("furioso",      0.8),
    ("furioso",     "amenaza"):         ("furioso",      1.0),
    ("furioso",     "elogio"):          ("molesto",      0.5),
    ("furioso",     "disculpa"):        ("molesto",      0.4),
    ("furioso",     "agresion_fisica"): ("furioso",      1.0),

    # Desde feliz
    ("feliz",       "saludo"):          ("feliz",        0.5),
    ("feliz",       "queja_leve"):      ("neutral",      0.1),
    ("feliz",       "queja_fuerte"):    ("cauteloso",    0.3),
    ("feliz",       "amenaza"):         ("asustado",     0.5),
    ("feliz",       "elogio"):          ("feliz",        0.7),
    ("feliz",       "comercio"):        ("feliz",        0.4),

    # Desde asustado
    ("asustado",    "saludo"):          ("asustado",     0.4),
    ("asustado",    "amenaza"):         ("asustado",     0.9),
    ("asustado",    "elogio"):          ("cauteloso",    0.2),
    ("asustado",    "disculpa"):        ("cauteloso",    0.3),
    ("asustado",    "agresion_fisica"): ("asustado",     1.0),

    # Desde desconfiado
    ("desconfiado", "saludo"):          ("desconfiado",  0.3),
    ("desconfiado", "queja_leve"):      ("molesto",      0.4),
    ("desconfiado", "elogio"):          ("cauteloso",    0.2),
    ("desconfiado", "comercio"):        ("desconfiado",  0.4),
    ("desconfiado", "disculpa"):        ("cauteloso",    0.2),

    # Desde curioso
    ("curioso",     "saludo"):          ("curioso",      0.3),
    ("curioso",     "pregunta"):        ("curioso",      0.4),
    ("curioso",     "amenaza"):         ("asustado",     0.5),
    ("curioso",     "queja_leve"):      ("neutral",      0.1),
    ("curioso",     "comercio"):        ("feliz",        0.3),
}

# Cuánto decae la intensidad por tick de mundo (llamar en update_tick)
DECAIMIENTO_POR_TICK = 0.05


@dataclass
class EstadoEmocional:
    emocion: str = "neutral"
    intensidad: float = 0.0  # 0.0 a 1.0

    def to_dict(self) -> Dict:
        return {
            "emocion": self.emocion,
            "intensidad": round(self.intensidad, 2)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "EstadoEmocional":
        return cls(
            emocion=data.get("emocion", "neutral"),
            intensidad=data.get("intensidad", 0.0)
        )


class EmotionEngine:
    """
    Gestiona las transiciones emocionales de un NPC.
    No usa LLM. Solo reglas deterministas con inercia.
    """

    def aplicar_evento(self, estado: EstadoEmocional, evento: str) -> EstadoEmocional:
        """
        Aplica un evento al estado emocional actual y devuelve el nuevo estado.
        Si no hay transición definida, el estado no cambia.
        """
        key = (estado.emocion, evento)

        if key in TRANSICIONES:
            nueva_emocion, nueva_intensidad = TRANSICIONES[key]
            return EstadoEmocional(
                emocion=nueva_emocion,
                intensidad=nueva_intensidad
            )

        # Sin transición definida → emoción estable, leve decaimiento
        nueva_intensidad = max(0.0, estado.intensidad - 0.05)
        return EstadoEmocional(emocion=estado.emocion, intensidad=nueva_intensidad)

    def tick_decaimiento(self, estado: EstadoEmocional) -> EstadoEmocional:
        """
        Llamar cada tick de mundo para que las emociones se enfríen con el tiempo.
        Cuando la intensidad llega a 0, vuelve a neutral.
        """
        nueva_intensidad = max(0.0, estado.intensidad - DECAIMIENTO_POR_TICK)
        nueva_emocion = estado.emocion if nueva_intensidad > 0.0 else "neutral"
        return EstadoEmocional(emocion=nueva_emocion, intensidad=nueva_intensidad)

    def describir(self, estado: EstadoEmocional) -> str:
        """
        Devuelve una descripción legible del estado emocional para el prompt.
        Ejemplo: "molesto (intensidad alta)"
        """
        if estado.intensidad < 0.2:
            nivel = "leve"
        elif estado.intensidad < 0.6:
            nivel = "moderado"
        else:
            nivel = "alto"

        if estado.emocion == "neutral" or estado.intensidad == 0.0:
            return "neutral"

        return f"{estado.emocion} (nivel {nivel})"
