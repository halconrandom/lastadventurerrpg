from datetime import datetime, timedelta
from typing import List, Dict, Optional
from systems.npcs.npc import NPC, EstadoNPC
from systems.tiempo import TimeManager

class NPCScheduler:
    """Gestiona la actualización de rutinas y actividades de los NPCs basadas en el tiempo."""

    def __init__(self):
        pass

    def actualizar_activos_por_tiempo(self, manager, tiempo: TimeManager):
        """Actualiza todos los NPCs activos según el tiempo actual."""
        hora = tiempo.hora
        minuto = tiempo.minuto
        
        for npc_id in manager.npcs_activos_ids:
            npc = manager.obtener_npc(npc_id)
            if npc:
                actividad = self.obtener_actividad_actual(npc, hora, minuto)
                # Aquí se podrían disparar cambios de estado o ubicación
                # Por ahora solo registramos la actividad si fuera necesario
                pass

    def obtener_actividad_actual(self, npc: NPC, hora_actual: int, minuto_actual: int = 0) -> str:
        """Determina qué actividad debería estar haciendo el NPC según su agenda."""
        hora_str = f"{hora_actual:02d}:{minuto_actual:02d}"
        
        # 1. Revisar excepciones (eventos temporales)
        for excepcion in npc.rutina.excepciones:
            if self._esta_en_rango(hora_str, excepcion["desde"], excepcion["hasta"]):
                return excepcion["actividad"]
        
        # 2. Revisar agenda diaria
        for bloque in npc.rutina.agenda_diaria:
            if self._esta_en_rango(hora_str, bloque["desde"], bloque["hasta"]):
                return bloque["actividad"]
        
        return "ocio" # Actividad por defecto

    def _esta_en_rango(self, actual: str, inicio: str, fin: str) -> bool:
        """Verifica si la hora actual está entre inicio y fin (formato HH:MM)."""
        if inicio <= fin:
            return inicio <= actual <= fin
        else: # Rango que cruza la medianoche (ej: 22:00 a 06:00)
            return actual >= inicio or actual <= fin

    def actualizar_npcs(self, npcs: List[NPC], hora_actual: int, minuto_actual: int = 0):
        """Actualiza el estado de una lista de NPCs según la hora."""
        for npc in npcs:
            actividad = self.obtener_actividad_actual(npc, hora_actual, minuto_actual)
            # Aquí se podrían disparar cambios de estado o ubicación si la actividad lo requiere
            # Por ahora solo actualizamos un flag interno o log si fuera necesario
            pass
