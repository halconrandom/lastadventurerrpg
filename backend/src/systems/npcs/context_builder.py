"""
ContextBuilder — Construye el prompt minimalista para el LLM.

Principios:
- El LLM solo recibe lo que necesita para HABLAR, no para pensar.
- Máximo ~400 tokens de input (aumentado para incluir ejemplos RAG).
- El LLM devuelve SOLO texto de diálogo. Sin JSON. Sin etiquetas.
- El código ya tomó todas las decisiones lógicas antes de llegar aquí.
- RAG: Se inyectan ejemplos de diálogo relevantes para guiar el estilo.
"""

from typing import List, Dict
from systems.npcs.npc import NPC
from systems.npcs.emotion_engine import EmotionEngine, EstadoEmocional
from systems.npcs.goal_engine import Goal
from systems.npcs.intent_classifier import IntentResult
from systems.npcs.example_retriever import get_example_retriever, ExampleRetriever


# ---------------------------------------------------------------------------
# Prompt de sistema — Identidad del NPC + Reglas + Ejemplos RAG
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """Eres {nombre}, {articulo} {rol} {raza} en un mundo de fantasía medieval.
Rasgos de personalidad: {rasgos}.
Hablas de forma {voz}. Frases cortas. Lenguaje simple y directo.

REGLAS ABSOLUTAS:
1. Las acciones van entre asteriscos en TERCERA PERSONA usando tu nombre. Ejemplo: *{nombre} cruza los brazos*
2. NUNCA uses primera persona en las acciones. MAL: *miro al forastero* BIEN: *{nombre} mira al forastero*
3. NUNCA digas "jugador". Di "forastero", "viajero" o el nombre si lo sabes.
4. NUNCA uses lenguaje psicológico. Reacciona como un ser vivo, no como un analista.
5. Responde SOLO con la acción y el diálogo. Sin JSON. Sin etiquetas. Sin explicaciones.
6. Tu personalidad debe REFLEJARSE en lo que dices, no explicarse.

{ejemplos_rag}"""

# ---------------------------------------------------------------------------
# Prompt de usuario — Contexto + mensaje
# ---------------------------------------------------------------------------
USER_PROMPT_TEMPLATE = """Estado emocional: {emocion_descripcion}.
Ahora mismo: {actitud_meta}.
Relación con este forastero: {perfil_relacion}.

{hilo_conversacion}El forastero dice: "{mensaje}"

{nombre} responde (acción en tercera persona con tu nombre, luego diálogo):"""


class ContextBuilder:
    """
    Ensambla el prompt final para el LLM usando los resultados
    de EmotionEngine, GoalEngine, IntentClassifier y ExampleRetriever (RAG).
    """

    def __init__(self, retriever: ExampleRetriever = None):
        self.emotion_engine = EmotionEngine()
        self.retriever = retriever or get_example_retriever()

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

        # 2. Buscar ejemplos RAG relevantes
        tipo_interaccion = self._mapear_tipo_interaccion(intent.tipo)
        ejemplos = self.retriever.buscar_ejemplos(
            raza=npc.raza,
            rasgos=npc.personalidad.rasgos,
            rol=npc.rol_tipo,
            tipo_interaccion=tipo_interaccion,
            max_ejemplos=3
        )
        ejemplos_formateados = self.retriever.formatear_ejemplos_para_prompt(ejemplos, npc.nombre)

        # 3. Construir system prompt con ejemplos RAG
        system = SYSTEM_PROMPT_TEMPLATE.format(
            nombre=npc.nombre,
            articulo=self._articulo(npc.genero),
            rol=npc.rol_tipo,
            raza=npc.raza,
            rasgos=", ".join(npc.personalidad.rasgos) if npc.personalidad.rasgos else "ninguno definido",
            voz=self._describir_voz(npc),
            ejemplos_rag=ejemplos_formateados if ejemplos_formateados else "(Sin ejemplos específicos)",
        )

        # 4. Construir perfil de relación legible
        perfil = self._perfil_relacion(npc)

        # 5. Construir hilo de conversación (últimas 3 frases)
        hilo = self._hilo_conversacion(npc)

        # 6. Actitud basada en meta + efecto del jugador
        from systems.npcs.goal_engine import GoalEngine
        actitud = GoalEngine().describir_actitud(meta, efecto_jugador)

        # 7. Construir user prompt
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

    def _mapear_tipo_interaccion(self, tipo_intent: str) -> str:
        """Mapea el tipo de intent a tipo de interaccion para buscar ejemplos."""
        MAPEO = {
            "saludo": "saludo",
            "pregunta": "pregunta",
            "charla": "charla",
            "comercio": "comercio",
            "regateo": "regateo",
            "elogio": "elogio",
            "queja_leve": "queja",
            "queja_fuerte": "queja",
            "amenaza": "amenaza",
            "despedida": "despedida",
            "informacion": "pregunta",
            "encargo": "encargo",
            "herida": "herida",
            "plan": "plan",
            "conflicto": "conflicto",
        }
        return MAPEO.get(tipo_intent, "saludo")

    def _describir_voz(self, npc: NPC) -> str:
        """Traduce los rasgos de personalidad a un estilo de voz."""
        rasgos = [r.lower() for r in npc.personalidad.rasgos]
        sliders = npc.personalidad.sliders

        # Rasgos con prioridad alta (primero los más específicos)
        MAPA_RASGOS = {
            "fanático":      "intensa, apasionada y sin matices. Habla con convicción absoluta",
            "estoico":       "fría, contenida y de pocas palabras. No muestra emociones fácilmente",
            "paranoico":     "suspicaz y nerviosa, siempre buscando segundas intenciones",
            "desconfiado":   "cautelosa y reservada, mide cada palabra",
            "codicioso":     "calculadora, siempre pensando en el beneficio propio",
            "alegre":        "animada y amigable, con energía positiva",
            "optimista":     "animada y esperanzadora",
            "pesimista":     "apagada y resignada, espera lo peor",
            "arrogante":     "altiva y condescendiente, se cree superior",
            "humilde":       "modesta y respetuosa",
            "agresivo":      "brusca, directa y sin filtros",
            "cobarde":       "nerviosa y evasiva, evita el conflicto",
            "valiente":      "directa y sin miedo, habla con seguridad",
            "curioso":       "inquisitiva y entusiasta, hace preguntas",
            "serio":         "formal y sin humor, va al grano",
            "gracioso":      "con humor y sarcasmo ligero",
            "melancólico":   "lenta y nostálgica, con un tono triste",
            "leal":          "firme y comprometida, habla con honor",
            "traicionero":   "amable en la superficie pero con doble intención",
        }

        for rasgo in rasgos:
            if rasgo in MAPA_RASGOS:
                return MAPA_RASGOS[rasgo]

        # Fallback a sliders si no hay rasgo mapeado
        if sliders.get("agresividad", 0.5) > 0.7:
            return "brusca y directa"
        if sliders.get("empatía", 0.5) > 0.7:
            return "cálida y cercana"

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
