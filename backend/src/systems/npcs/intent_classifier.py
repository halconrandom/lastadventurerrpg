"""
IntentClassifier — Clasifica la intención del jugador SIN usar LLM.

Principios:
- Solo usa keywords, patrones regex y reglas simples.
- Rápido, determinista y sin coste de tokens.
- Devuelve: tipo de intención, nivel de agresión (0.0-1.0) y evento
  para el EmotionEngine.
"""

import re
from dataclasses import dataclass
from typing import Dict, Tuple


# ---------------------------------------------------------------------------
# Resultado de la clasificación
# ---------------------------------------------------------------------------
@dataclass
class IntentResult:
    tipo: str           # "saludo" | "queja" | "amenaza" | "comercio" | "pregunta" | "elogio" | "charla"
    agresion: float     # 0.0 a 1.0
    evento_emocion: str # Evento para EmotionEngine: "queja_leve", "amenaza", etc.
    descripcion: str    # Texto legible para el prompt

    def to_dict(self) -> Dict:
        return {
            "tipo": self.tipo,
            "agresion": self.agresion,
            "evento_emocion": self.evento_emocion,
            "descripcion": self.descripcion
        }


# ---------------------------------------------------------------------------
# Tablas de keywords por categoría
# ---------------------------------------------------------------------------

KEYWORDS_AMENAZA = [
    "te mato", "te voy a matar", "muere", "te voy a cortar",
    "te arrepentirás", "pagarás", "te destruyo", "te aplasto",
    "saca tu espada", "prepárate para morir", "ataco", "ataque",
    "te clavo", "te rebano", "te parto"
]

KEYWORDS_QUEJA_FUERTE = [
    "eres un idiota", "eres un estúpido", "eres inútil", "eres un fraude",
    "me has robado", "me engañaste", "mentiroso", "traidor", "maldito",
    "te odio", "eres terrible", "eres horrible", "incompetente",
    "estoy harto de ti", "me has fallado"
]

KEYWORDS_QUEJA_LEVE = [
    "estoy molesto", "estoy enojado", "me molesta", "no me gusta",
    "me decepciona", "esperaba más", "no estoy contento", "me frustra",
    "eso no está bien", "no es justo", "me parece mal", "tengo un problema",
    "hay un problema", "algo anda mal", "no funciona"
]

KEYWORDS_ELOGIO = [
    "eres increíble", "eres genial", "gracias", "muchas gracias",
    "excelente trabajo", "bien hecho", "te admiro", "eres el mejor",
    "qué bueno eres", "impresionante", "fantástico", "maravilloso",
    "me alegra", "estoy contento contigo", "buen trabajo"
]

KEYWORDS_COMERCIO = [
    "quiero comprar", "quiero vender", "cuánto cuesta", "cuanto cuesta",
    "cuánto vale", "cuanto vale", "tienes en venta", "qué vendes", "que vendes",
    "qué tienes", "que tienes", "precio", "intercambio", "trueque", "negocio",
    "mercancía", "mercancia", "poción", "pocion", "arma", "armadura",
    "equipo", "oro", "monedas", "comprar", "vender"
]

KEYWORDS_SALUDO = [
    "hola", "buenos días", "buenas tardes", "buenas noches", "buenas",
    "saludos", "hey", "ey", "qué tal", "cómo estás", "cómo te va",
    "buen día", "bienvenido"
]

KEYWORDS_DESPEDIDA = [
    "adiós", "hasta luego", "nos vemos", "chao", "me voy",
    "hasta pronto", "cuídate", "que te vaya bien"
]

KEYWORDS_PREGUNTA_INFO = [
    "dónde está", "donde esta", "dónde queda", "donde queda",
    "cómo llego", "como llego", "sabes algo de", "has visto",
    "conoces", "qué sabes de", "que sabes de", "cuéntame sobre",
    "cuentame sobre", "información sobre", "informacion sobre",
    "qué hay en", "que hay en", "qué pasó con", "que paso con"
]


# ---------------------------------------------------------------------------
# Clasificador
# ---------------------------------------------------------------------------
class IntentClassifier:
    """
    Clasifica la intención del jugador usando solo reglas y keywords.
    Sin LLM. Determinista y rápido.
    """

    def clasificar(self, mensaje: str) -> IntentResult:
        texto = mensaje.lower().strip()

        # Orden de prioridad: amenaza > queja_fuerte > queja_leve > elogio > comercio > pregunta > saludo > charla

        if self._contiene(texto, KEYWORDS_AMENAZA):
            return IntentResult(
                tipo="amenaza",
                agresion=0.9,
                evento_emocion="amenaza",
                descripcion="El jugador está amenazando directamente al NPC."
            )

        if self._contiene(texto, KEYWORDS_QUEJA_FUERTE):
            return IntentResult(
                tipo="queja_fuerte",
                agresion=0.65,
                evento_emocion="queja_fuerte",
                descripcion="El jugador está insultando o acusando al NPC."
            )

        if self._contiene(texto, KEYWORDS_QUEJA_LEVE):
            return IntentResult(
                tipo="queja_leve",
                agresion=0.3,
                evento_emocion="queja_leve",
                descripcion="El jugador expresa su propia molestia o frustración."
            )

        if self._contiene(texto, KEYWORDS_ELOGIO):
            return IntentResult(
                tipo="elogio",
                agresion=0.0,
                evento_emocion="elogio",
                descripcion="El jugador está siendo amable o agradecido."
            )

        if self._contiene(texto, KEYWORDS_COMERCIO):
            return IntentResult(
                tipo="comercio",
                agresion=0.0,
                evento_emocion="comercio",
                descripcion="El jugador quiere comerciar o preguntar precios."
            )

        if self._contiene(texto, KEYWORDS_PREGUNTA_INFO):
            return IntentResult(
                tipo="pregunta",
                agresion=0.0,
                evento_emocion="pregunta",
                descripcion="El jugador busca información o pide orientación."
            )

        if self._contiene(texto, KEYWORDS_SALUDO):
            return IntentResult(
                tipo="saludo",
                agresion=0.0,
                evento_emocion="saludo",
                descripcion="El jugador está saludando al NPC."
            )

        if self._contiene(texto, KEYWORDS_DESPEDIDA):
            return IntentResult(
                tipo="despedida",
                agresion=0.0,
                evento_emocion="saludo",
                descripcion="El jugador se está despidiendo."
            )

        # Si hay signos de interrogación, probablemente es una pregunta genérica
        if "?" in texto:
            return IntentResult(
                tipo="pregunta",
                agresion=0.0,
                evento_emocion="pregunta",
                descripcion="El jugador está haciendo una pregunta."
            )

        # Default: charla casual
        return IntentResult(
            tipo="charla",
            agresion=0.05,
            evento_emocion="saludo",
            descripcion="El jugador está teniendo una conversación casual."
        )

    def _contiene(self, texto: str, keywords: list) -> bool:
        """Verifica si el texto contiene alguna de las keywords."""
        return any(kw in texto for kw in keywords)
