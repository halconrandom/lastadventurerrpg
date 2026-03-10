from typing import Dict, Any
import json
from llm.client import LLMClient

class IntentParser:
    """Analiza la intención y el tono del mensaje del jugador."""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def parsear(self, mensaje: str) -> Dict[str, Any]:
        prompt = f"""
Analiza la intención del jugador en un RPG.
Mensaje: "{mensaje}"

REGLAS:
- Si el jugador dice "estoy molesto", la intención es 'QUEJA'.
- Identifica si el jugador expresa una emoción propia o pregunta por la del NPC.

Responde EXCLUSIVAMENTE con un JSON:
{{
  "intencion": "saludo | pregunta | queja | amenaza | comercio | charla_casual",
  "agresion": 0.0 a 1.0,
  "emocion_jugador": "frustración | alegría | odio | miedo | neutral",
  "objetivo_social": "qué busca el jugador con este mensaje"
}}
"""
        respuesta = self.llm.generar(prompt)
        try:
            # Limpiar posible texto extra del LLM
            inicio = respuesta.find('{')
            fin = respuesta.rfind('}') + 1
            return json.loads(respuesta[inicio:fin])
        except:
            return {
                "intencion": "charla_casual",
                "agresion": 0.1,
                "tono": "neutral",
                "tema_principal": "desconocido"
            }
