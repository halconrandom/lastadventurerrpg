"""
ContextBuilder — Construye el prompt minimalista para el LLM.

Principios:
- El LLM solo recibe lo que necesita para HABLAR, no para pensar.
- Máximo ~300 tokens de input.
- El LLM devuelve SOLO texto de diálogo. Sin JSON. Sin etiquetas.
- El código ya tomó todas las decisiones lógicas antes de llegar aquí.
"""

from typing import List, Dict
from systems.npcs.npc import NPC
from systems.npcs.emotion_engine import EmotionEngine, EstadoEmocional
from systems.npcs.goal_engine import Goal
from systems.npcs.intent_classifier import IntentResult


# ---------------------------------------------------------------------------
# Prompt de sistema — Identidad del NPC
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """Eres {nombre}, {articulo} {rol} {raza} en un mundo de fantasía medieval.
Hablas de forma {voz}. Frases cortas. Lenguaje simple y directo.
NUNCA uses lenguaje psicológico ni analices al jugador.
Responde SOLO con el diálogo. Sin JSON. Sin explicaciones. Sin etiquetas."""

# ---------------------------------------------------------------------------
# Prompt de usuario — Contexto + mensaje
# ---------------------------------------------------------------------------
USER_PROMPT_TEMPLATE = """Estado: {emocion_descripcion}.
Ahora mismo: {actitud_meta}.
Relación con este forastero: {perfil_relacion}.

{hilo_conversacion}
El forastero dice: "{mensaje}"

{nombre} responde:"""


class ContextBuilder:
    """
    Ensambla el prompt final para el LLM usando los resultados
    de EmotionEngine, GoalEngine e IntentClassifier.
    """

    def __init__(self):
        self.emotion_engine = EmotionEngine()

    def construir(
        self,
        npc: NPC,
        mensaje: str,
        intent: IntentResult,
        meta: Goal,
        efecto_jugador: str,
    ) -> Dict[str, str]:
        """
        Devuelve {"system": ..., "user": ...} listos para enviar al LLM.
        """

        # 1. Actualizar emoción del NPC con el evento del intent
        nuevo_estado = self.emotion_engine.aplicar_evento(
            npc.estado_emocional, intent.evento_emocion
        )
        npc.estado_emocional = nuevo_estado  # Persistir en el objeto

        # 2. Construir system prompt
        system = SYSTEM_PROMPT_TEMPLATE.format(
            nombre=npc.nombre,
            articulo=self._articulo(npc.genero),
            rol=npc.rol_tipo,
            raza=npc.raza,
            voz=self._describir_voz(npc),
        )

        # 3. Construir perfil de relación legible
        perfil = self._perfil_relacion(npc)

        # 4. Construir hilo de conversación (últimas 3 frases)
        hilo = self._hilo_conversacion(npc)

        # 5. Actitud basada en meta + efecto del jugador
        from systems.npcs.goal_engine import GoalEngine
        actitud = GoalEngine().describir_actitud(meta, efecto_jugador)

        # 6. Construir user prompt
        user = USER_PROMPT_TEMPLATE.format(
            emocion_descripcion=self.emotion_engine.describir(nuevo_estado),
            actitud_meta=actitud,
            perfil_relacion=perfil,
            hilo_conversacion=hilo,
            mensaje=mensaje,
            nombre=npc.nombre,
        )

        return {"system": system, "user": user}

    # -----------------------------------------------------------------------
    # Helpers privados
    # -----------------------------------------------------------------------

    def _articulo(self, genero: str) -> str:
        return "una" if genero.lower() in ("femenino", "f") else "un"

    def _describir_voz(self, npc: NPC) -> str:
        """Traduce los rasgos de personalidad a un estilo de voz."""
        rasgos = npc.personalidad.rasgos
        sliders = npc.personalidad.sliders

        if sliders.get("agresividad", 0.5) > 0.7:
            return "brusca y directa"
        if sliders.get("empatía", 0.5) > 0.7:
            return "cálida y cercana"
        if sliders.get("codicia", 0.5) > 0.7:
            return "calculadora y desconfiada"
        if "paranoico" in rasgos or "desconfiado" in rasgos:
            return "suspicaz y nerviosa"
        if "alegre" in rasgos or "optimista" in rasgos:
            return "animada y amigable"
        if "seria" in rasgos or "formal" in rasgos:
            return "seria y formal"

        return "neutral y directa"

    def _perfil_relacion(self, npc: NPC) -> str:
        """Convierte los valores numéricos de relación en texto."""
        v = npc.relacion_jugador.reputacion_valor
        c = npc.relacion_jugador.confianza
        m = npc.relacion_jugador.miedo

        if m > 60:
            return "le tienes miedo"
        if v > 50 and c > 60:
            return "es un amigo de confianza"
        if v > 20:
            return "es un conocido amigable"
        if v < -50:
            return "es un enemigo, no te fías de él"
        if v < -20:
            return "te cae mal, es un forastero problemático"
        return "es un desconocido, no sabes si fiarte"

    def _hilo_conversacion(self, npc: NPC) -> str:
        """Formatea las últimas 3 interacciones como hilo de chat."""
        interacciones = npc.memoria.ultimas_interacciones[-3:]
        if not interacciones:
            return ""

        lineas = []
        for i in interacciones:
            jugador = i.get("jugador", "")
            npc_resp = i.get("npc", "")
            if jugador:
                lineas.append(f'Forastero: "{jugador}"')
            if npc_resp:
                lineas.append(f'{npc.nombre}: "{npc_resp}"')

        return "\n".join(lineas) + "\n" if lineas else ""
