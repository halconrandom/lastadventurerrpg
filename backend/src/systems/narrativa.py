"""
NarrativaManager — Orquestador del pipeline cognitivo de NPCs.

Pipeline:
  1. IntentClassifier  → Clasifica intención del jugador (sin LLM)
  2. EmotionEngine     → Actualiza emoción del NPC con inercia
  3. GoalEngine        → Obtiene meta activa y evalúa al jugador
  4. DialoguePolicy    → Filtra decisiones absurdas
  5. ContextBuilder    → Construye prompt minimalista
  6. LLMClient         → Solo genera el texto del diálogo
  7. ResponseCleaner   → Limpia exageraciones y errores
"""

import re
from typing import List, Dict, Optional

from systems.tiempo import TimeManager
from systems.npcs.npc import NPC
from systems.npcs.intent_classifier import IntentClassifier
from systems.npcs.emotion_engine import EmotionEngine
from systems.npcs.goal_engine import GoalEngine
from systems.npcs.context_builder import ContextBuilder
from systems.npcs.response_cleaner import get_response_cleaner
from llm.client import LLMClient
from llm.prompts import PROMPT_DESCRIPCION_ESCENA


class NarrativaManager:
    """
    Orquestador del pipeline cognitivo de NPCs.
    El LLM solo genera diálogo. Toda la lógica es código.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.intent_classifier = IntentClassifier()
        self.emotion_engine = EmotionEngine()
        self.goal_engine = GoalEngine()
        self.context_builder = ContextBuilder()
        self.response_cleaner = get_response_cleaner()

    # -----------------------------------------------------------------------
    # Pipeline principal de diálogo
    # -----------------------------------------------------------------------
    def generar_dialogo_npc(
        self,
        npc: NPC,
        mensaje_jugador: str,
        jugador_data: Dict,
        tiempo: TimeManager,
        rumores_locales: List[Dict],
        ubicacion_id: str = None,
    ) -> Dict:
        """
        Ejecuta el pipeline completo y devuelve la respuesta del NPC.
        
        Args:
            npc: El NPC que responde
            mensaje_jugador: Mensaje del jugador
            jugador_data: Datos del jugador
            tiempo: Gestor de tiempo
            rumores_locales: Rumores disponibles
            ubicacion_id: ID de la ubicación actual (opcional)
        """

        # PASO 1: Clasificar intención del jugador (sin LLM)
        intent = self.intent_classifier.clasificar(mensaje_jugador)

        # PASO 2: Obtener meta activa según rol y hora
        hora_actual = tiempo.hora if hasattr(tiempo, 'hora') else 12
        meta = self.goal_engine.get_meta_activa(npc.rol_tipo, hora_actual)

        # PASO 3: Evaluar si el jugador ayuda u obstaculiza la meta
        efecto_jugador = self.goal_engine.evaluar_jugador(meta, intent.tipo)

        # PASO 4: Construir prompt (también actualiza emoción del NPC)
        prompt_data = self.context_builder.construir(
            npc=npc,
            mensaje=mensaje_jugador,
            intent=intent,
            meta=meta,
            efecto_jugador=efecto_jugador,
            ubicacion_id=ubicacion_id,
            hora=hora_actual,
        )

        # PASO 5: Llamar al LLM solo para generar el texto
        respuesta_raw = self.llm.generar(
            prompt_data["user"],
            system_prompt=prompt_data["system"]
        )

        if not respuesta_raw:
            return self._respuesta_fallback(npc)

        # PASO 6: Limpiar la respuesta con ResponseCleaner
        respuesta_limpia = self.response_cleaner.limpiar(respuesta_raw, npc.nombre)

        # PASO 7: Validar que no tenga exageraciones
        if not self.response_cleaner.validar(respuesta_limpia):
            # Si tiene exageraciones, intentar limpiar más agresivamente
            respuesta_limpia = self._limpiar_respuesta(respuesta_limpia, npc.nombre)

        # PASO 8: Guardar en memoria del NPC
        npc.memoria.ultimas_interacciones.append({
            "jugador": mensaje_jugador,
            "npc": respuesta_limpia,
            "timestamp": getattr(tiempo, 'tick_total', 0)
        })
        # Mantener solo las últimas 10 interacciones
        npc.memoria.ultimas_interacciones = npc.memoria.ultimas_interacciones[-10:]

        return {
            "respuesta": respuesta_limpia,
            "debug": {
                "intent": intent.tipo,
                "agresion": intent.agresion,
                "emocion": npc.estado_emocional.emocion,
                "emocion_intensidad": npc.estado_emocional.intensidad,
                "meta_activa": meta.tipo,
                "efecto_jugador": efecto_jugador,
            }
        }

    # -----------------------------------------------------------------------
    # Descripción de escena (para exploración)
    # -----------------------------------------------------------------------
    def generar_descripcion_escena(
        self,
        bioma: str,
        ubicacion: str,
        hora: str,
        clima: str,
        eventos: List[str],
        tono: str = "misterioso"
    ) -> str:
        """Genera una descripción narrativa del entorno para la exploración."""
        prompt = PROMPT_DESCRIPCION_ESCENA.format(
            bioma=bioma,
            ubicacion=ubicacion,
            hora=hora,
            clima=clima,
            eventos="\n".join(f"- {e}" for e in eventos) if eventos else "Ninguno.",
            tono=tono
        )
        respuesta = self.llm.generar(prompt)
        return respuesta or "El silencio del camino te envuelve."

    # -----------------------------------------------------------------------
    # Helpers privados
    # -----------------------------------------------------------------------

    def _limpiar_respuesta(self, texto: str, nombre_npc: str) -> str:
        """
        Elimina artefactos comunes del LLM:
        - Prefijos como "NPC:", "Dorian:", "Respuesta:"
        - Etiquetas JSON residuales
        - Líneas vacías múltiples
        """
        # Eliminar prefijos de nombre
        texto = re.sub(rf"^{re.escape(nombre_npc)}\s*:\s*", "", texto, flags=re.IGNORECASE)
        texto = re.sub(r"^(NPC|Respuesta|Response)\s*:\s*", "", texto, flags=re.IGNORECASE)

        # Eliminar bloques JSON residuales
        texto = re.sub(r"\{.*?\}", "", texto, flags=re.DOTALL)

        # Eliminar etiquetas tipo [PENSAMIENTO], [DECISION]
        texto = re.sub(r"\[.*?\]", "", texto)

        # Limpiar espacios y saltos de línea múltiples
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        texto = texto.strip()

        return texto if texto else "..."

    def _respuesta_fallback(self, npc: NPC) -> Dict:
        """Respuesta de emergencia si el LLM no está disponible."""
        emocion = npc.estado_emocional.emocion
        fallbacks = {
            "neutral":      "*asiente levemente* Mmm.",
            "molesto":      "*frunce el ceño* Ahora no.",
            "furioso":      "*aprieta los puños* ...",
            "feliz":        "*sonríe* ¡Ah, forastero!",
            "asustado":     "*retrocede un paso* ¿Qué quieres?",
            "cauteloso":    "*te observa con cautela* ¿Sí?",
            "desconfiado":  "*entrecierra los ojos* ¿Qué buscas?",
        }
        return {
            "respuesta": fallbacks.get(emocion, "..."),
            "debug": {
                "intent": "desconocido",
                "agresion": 0.0,
                "emocion": emocion,
                "emocion_intensidad": npc.estado_emocional.intensidad,
                "meta_activa": "desconocida",
                "efecto_jugador": "neutral",
            }
        }
