from typing import List, Dict, Optional
from .npc import NPC, MemoriaNPC

class MemoryIndex:
    """Gestiona el indexado y resumen de memorias para el Context Builder del LLM."""

    def __init__(self):
        pass

    def generar_contexto_memoria(self, npc: NPC, max_eventos: int = 5) -> Dict:
        """
        Construye un diccionario de contexto optimizado para el prompt del LLM.
        Incluye resúmenes y los eventos más recientes.
        """
        memoria = npc.memoria
        
        # Obtener los N eventos más recientes
        eventos_recientes = memoria.eventos[-max_eventos:] if memoria.eventos else []
        
        return {
            "resumen_general": memoria.resumen_general,
            "resumen_jugador": memoria.resumen_jugador,
            "interacciones_recientes": memoria.ultimas_interacciones[-3:],
            "eventos_clave": eventos_recientes
        }

    def añadir_evento(self, npc: NPC, evento: Dict):
        """Añade un evento a la memoria del NPC y actualiza el índice si es necesario."""
        npc.memoria.eventos.append(evento)
        # Aquí se dispararía la lógica de "resumen" si la memoria crece mucho
        if len(npc.memoria.eventos) > 50:
            self._compactar_memoria(npc)

    def _compactar_memoria(self, npc: NPC):
        """
        Lógica placeholder para resumir eventos antiguos.
        En una implementación real, esto podría llamar a un LLM 'resumidor'.
        """
        # Por ahora solo mantenemos los últimos 50 y actualizamos el resumen general
        # (Simulado)
        pass
