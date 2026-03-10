from typing import Dict, Any
from .npc import NPC

class DialoguePolicy:
    """Filtra y valida las decisiones del LLM para evitar comportamientos absurdos."""

    def __init__(self):
        pass

    def validar_decision(self, npc: NPC, intent: Dict[str, Any], decision_llm: str) -> str:
        """
        Asegura que la decisión del LLM sea coherente con la agresión del jugador.
        """
        agresion = intent.get("agresion", 0.0)
        
        # 1. Bloquear ataques si no hay agresión real
        if decision_llm == "ATACAR" and agresion < 0.6:
            # Si el jugador solo está molesto, el NPC no debería atacar a menos que sea un psicópata
            if npc.personalidad.sliders.get("agresividad", 0.5) < 0.8:
                return "HABLAR" # Forzar a hablar/discutir en lugar de matar
        
        # 2. Bloquear huidas si el jugador es amigable
        if decision_llm == "HUIR" and agresion < 0.2:
            return "HABLAR"
            
        # 3. Si el jugador amenaza seriamente (>0.8) y el NPC es cobarde, forzar HUIR
        if agresion > 0.8 and npc.personalidad.sliders.get("valentía", 0.5) < 0.3:
            return "HUIR"

        return decision_llm
