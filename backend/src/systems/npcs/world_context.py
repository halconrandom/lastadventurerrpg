"""
WorldContext — Proporciona contexto del mundo para el LLM.

Incluye:
- NPCs relacionados (del propio NPC, no hardcodeado)
- Ubicación actual
- Hora del día
- Eventos recientes relevantes

Las relaciones se almacenan en cada NPC y son persistentes.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from systems.npcs.npc import NPC, RelacionNPC, TipoRelacion


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
    
    Las relaciones ahora vienen del NPC mismo, no de una base hardcodeada.
    """
    
    # Ubicaciones conocidas (esto sí puede ser estático)
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
        self.ubicaciones = self.UBICACIONES
    
    def obtener_relaciones_npc(self, npc: NPC) -> List[RelacionNPC]:
        """Obtiene las relaciones del NPC desde sus propios datos."""
        return npc.relaciones_npcs
    
    def obtener_ubicacion(self, id_ubicacion: str) -> Optional[ContextoUbicacion]:
        """Obtiene información de una ubicación."""
        return self.ubicaciones.get(id_ubicacion)
    
    def formatear_contexto_para_prompt(
        self,
        npc: NPC,
        ubicacion_id: str = None,
        hora: int = 12
    ) -> str:
        """
        Formatea el contexto del mundo para inyectar en el prompt.
        
        Args:
            npc: El NPC que está hablando (con sus relaciones)
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
                if ubicacion.propietario and ubicacion.propietario != npc.nombre:
                    linea += f", lugar de {ubicacion.propietario}"
                lineas.append(linea + ".")
        
        # Hora
        fase_dia = self._fase_dia(hora)
        lineas.append(f"Es de {fase_dia}.")
        
        # Relaciones importantes del NPC
        relaciones = self.obtener_relaciones_npc(npc)
        if relaciones:
            # Filtrar relaciones importantes (familia, romance, rivalidad)
            importantes = [r for r in relaciones if r.tipo in [
                TipoRelacion.FAMILIA, 
                TipoRelacion.ROMANCE, 
                TipoRelacion.RIVALIDAD,
                TipoRelacion.ENEMISTAD
            ] or r.intensidad >= 70]
            
            if importantes:
                rels_texto = []
                for r in importantes[:2]:  # Máximo 2 para no saturar
                    tipo_str = self._tipo_relacion_legible(r.tipo)
                    rels_texto.append(f"{r.nombre} es tu {tipo_str}")
                    if r.notas:
                        rels_texto[-1] += f" ({r.notas})"
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
    
    def _tipo_relacion_legible(self, tipo: TipoRelacion) -> str:
        """Convierte el tipo de relación a texto legible."""
        mapeo = {
            TipoRelacion.FAMILIA: "familia",
            TipoRelacion.AMISTAD: "amigo",
            TipoRelacion.ROMANCE: "pareja",
            TipoRelacion.RIVALIDAD: "rival",
            TipoRelacion.ENEMISTAD: "enemigo",
            TipoRelacion.CONOCIDO: "conocido",
            TipoRelacion.PROFESIONAL: "colega",
            TipoRelacion.SUBORDINADO: "subordinado",
            TipoRelacion.SUPERIOR: "superior",
        }
        return mapeo.get(tipo, "conocido")
    
    def npc_mencionado(self, mensaje: str, npc: NPC) -> Optional[RelacionNPC]:
        """
        Detecta si se menciona un NPC relacionado en el mensaje.
        
        Args:
            mensaje: Mensaje del jugador
            npc: NPC actual (con sus relaciones)
        
        Returns:
            RelacionNPC si se encuentra, None si no
        """
        mensaje_lower = mensaje.lower()
        for rel in self.obtener_relaciones_npc(npc):
            if rel.nombre.lower() in mensaje_lower:
                return rel
        return None
    
    def agregar_relacion(
        self, 
        npc: NPC, 
        npc_id: str, 
        nombre: str, 
        tipo: TipoRelacion,
        intensidad: int = 50,
        confianza: int = 50,
        notas: str = ""
    ) -> None:
        """
        Agrega una nueva relación a un NPC.
        
        Args:
            npc: NPC al que se le agrega la relación
            npc_id: ID del NPC relacionado
            nombre: Nombre del NPC relacionado
            tipo: Tipo de relación
            intensidad: Intensidad (0-100)
            confianza: Nivel de confianza (0-100)
            notas: Notas contextuales
        """
        # Verificar si ya existe
        for r in npc.relaciones_npcs:
            if r.npc_id == npc_id:
                # Actualizar existente
                r.tipo = tipo
                r.intensidad = intensidad
                r.confianza = confianza
                r.notas = notas
                return
        
        # Crear nueva
        nueva_rel = RelacionNPC(
            npc_id=npc_id,
            nombre=nombre,
            tipo=tipo,
            intensidad=intensidad,
            confianza=confianza,
            notas=notas
        )
        npc.relaciones_npcs.append(nueva_rel)
    
    def modificar_relacion(
        self,
        npc: NPC,
        npc_id: str,
        delta_intensidad: int = 0,
        delta_confianza: int = 0
    ) -> None:
        """
        Modifica una relación existente.
        
        Args:
            npc: NPC con la relación
            npc_id: ID del NPC relacionado
            delta_intensidad: Cambio en intensidad (-100 a 100)
            delta_confianza: Cambio en confianza (-100 a 100)
        """
        for r in npc.relaciones_npcs:
            if r.npc_id == npc_id:
                r.intensidad = max(0, min(100, r.intensidad + delta_intensidad))
                r.confianza = max(0, min(100, r.confianza + delta_confianza))
                return


# Instancia global
_world_context_instance: Optional[WorldContext] = None


def get_world_context() -> WorldContext:
    """Obtiene la instancia global del contexto del mundo."""
    global _world_context_instance
    if _world_context_instance is None:
        _world_context_instance = WorldContext()
    return _world_context_instance