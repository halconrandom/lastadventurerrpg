from typing import List, Dict, Optional
from .npc import NPC, MemoriaNPC

class MemoryIndex:
    """Gestiona el indexado y resumen de memorias para el Context Builder del LLM."""

    def __init__(self):
        pass

    def generar_contexto_memoria(self, npc: NPC, max_eventos: int = 5) -> Dict:
        """
        Construye un contexto de memoria que prioriza la continuidad narrativa.
        """
        memoria = npc.memoria
        
        # 1. Formatear interacciones como un hilo de chat coherente
        hilo_conversacion = ""
        if memoria.ultimas_interacciones:
            # Solo tomamos las últimas 3 para no saturar al modelo pequeño
            for i in memoria.ultimas_interacciones[-3:]:
                hilo_conversacion += f"> Jugador: {i.get('jugador', '')}\n"
                hilo_conversacion += f"> {npc.nombre}: {i.get('npc', '')}\n"
        
        # 2. Crear un perfil de cómo el NPC ve al jugador basado en el ánimo
        perfil_relacion = "Neutral"
        valor = npc.relacion_jugador.reputacion_valor
        if valor > 20: perfil_relacion = "Amistosa/Confianza"
        elif valor > 50: perfil_relacion = "Lealtad absoluta"
        elif valor < -20: perfil_relacion = "Hostil/Desconfianza"
        elif valor < -50: perfil_relacion = "Enemistad/Odio"

        return {
            "hilo_reciente": hilo_conversacion or "Acabáis de empezar a hablar.",
            "perfil_relacion": perfil_relacion,
            "resumen_jugador": memoria.resumen_jugador or "Un forastero recién llegado."
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
