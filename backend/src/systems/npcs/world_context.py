"""
WorldContext — Proporciona contexto del mundo para el LLM.

Incluye:
- NPCs relacionados (conocidos, familiares, rivales)
- Ubicación actual
- Hora del día
- Eventos recientes relevantes
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class NPCRelacionado:
    """Un NPC relacionado con el NPC actual."""
    nombre: str
    relacion: str  # "amigo", "rival", "familia", "conocido", "enemigo"
    rol: str
    notas: str = ""


@dataclass
class ContextoUbicacion:
    """Contexto de la ubicación actual."""
    nombre: str
    tipo: str  # "taberna", "casa", "plaza", "tienda"
    propietario: Optional[str] = None
    es_publico: bool = True


class WorldContext:
    """
    Gestiona el contexto del mundo para enriquecer el prompt del LLM.
    
    Este sistema permite que el NPC tenga conocimiento de:
    - Otros NPCs en la misma ubicación
    - Relaciones con otros NPCs
    - El entorno donde se encuentra
    """
    
    # Base de datos de NPCs y sus relaciones (hardcodeada por ahora)
    # En el futuro, esto vendría de una base de datos o sistema de guardado
    RELACIONES_NPC: Dict[str, List[NPCRelacionado]] = {
        "Dorian Xavier": [
            NPCRelacionado(
                nombre="Adelina",
                relacion="prometida",
                rol="tabernera",
                notas="Comprometidos hace 2 años. Ella trabaja en la taberna El Viajero."
            ),
            NPCRelacionado(
                nombre="Gareth",
                relacion="rival",
                rol="mercader",
                notas="También interesado en Adelina. Dorian desconfía de él."
            ),
        ],
        "Adelina": [
            NPCRelacionado(
                nombre="Dorian Xavier",
                relacion="prometido",
                rol="herrero",
                notas="Comprometidos. Él es celoso y protector."
            ),
        ],
        # Agregar más NPCs según sea necesario
    }
    
    # Ubicaciones conocidas
    UBICACIONES: Dict[str, ContextoUbicacion] = {
        "pueblo_inicio": ContextoUbicacion(
            nombre="Pueblo de Inicio",
            tipo="pueblo",
            es_publico=True
        ),
        "taberna_el_viajero": ContextoUbicacion(
            nombre="Taberna El Viajero",
            tipo="taberna",
            propietario="Adelina",
            es_publico=True
        ),
        "herreria_dorian": ContextoUbicacion(
            nombre="Herrería de Dorian",
            tipo="tienda",
            propietario="Dorian Xavier",
            es_publico=False
        ),
    }
    
    def __init__(self):
        self.relaciones = self.RELACIONES_NPC
        self.ubicaciones = self.UBICACIONES
    
    def obtener_relaciones(self, nombre_npc: str) -> List[NPCRelacionado]:
        """Obtiene los NPCs relacionados con el NPC dado."""
        return self.relaciones.get(nombre_npc, [])
    
    def obtener_ubicacion(self, id_ubicacion: str) -> Optional[ContextoUbicacion]:
        """Obtiene información de una ubicación."""
        return self.ubicaciones.get(id_ubicacion)
    
    def formatear_contexto_para_prompt(
        self,
        nombre_npc: str,
        ubicacion_id: str = None,
        hora: int = 12
    ) -> str:
        """
        Formatea el contexto del mundo para inyectar en el prompt.
        
        Args:
            nombre_npc: Nombre del NPC actual
            ubicacion_id: ID de la ubicación actual
            hora: Hora del día (0-23)
        
        Returns:
            String formateado para el prompt
        """
        lineas = []
        
        # Ubicación
        if ubicacion_id:
            ubicacion = self.obtener_ubicacion(ubicacion_id)
            if ubicacion:
                linea = f"Estás en {ubicacion.nombre}"
                if ubicacion.propietario and ubicacion.propietario != nombre_npc:
                    linea += f", lugar de {ubicacion.propietario}"
                lineas.append(linea + ".")
        
        # Hora
        fase_dia = self._fase_dia(hora)
        lineas.append(f"Es de {fase_dia}.")
        
        # Relaciones importantes
        relaciones = self.obtener_relaciones(nombre_npc)
        if relaciones:
            rels_texto = []
            for r in relaciones[:2]:  # Máximo 2 para no saturar
                rels_texto.append(f"{r.nombre} es tu {r.relacion} ({r.rol})")
            lineas.append("Personas importantes: " + ", ".join(rels_texto) + ".")
        
        return "\n".join(lineas)
    
    def _fase_dia(self, hora: int) -> str:
        """Determina la fase del día."""
        if 6 <= hora < 12:
            return "mañana"
        elif 12 <= hora < 18:
            return "tarde"
        elif 18 <= hora < 22:
            return "noche"
        else:
            return "madrugada"
    
    def npc_mencionado(self, mensaje: str, nombre_npc: str) -> Optional[NPCRelacionado]:
        """
        Detecta si se menciona un NPC relacionado en el mensaje.
        
        Args:
            mensaje: Mensaje del jugador
            nombre_npc: Nombre del NPC actual
        
        Returns:
            NPCRelacionado si se encuentra, None si no
        """
        mensaje_lower = mensaje.lower()
        for rel in self.obtener_relaciones(nombre_npc):
            if rel.nombre.lower() in mensaje_lower:
                return rel
        return None


# Instancia global
_world_context_instance: Optional[WorldContext] = None


def get_world_context() -> WorldContext:
    """Obtiene la instancia global del contexto del mundo."""
    global _world_context_instance
    if _world_context_instance is None:
        _world_context_instance = WorldContext()
    return _world_context_instance