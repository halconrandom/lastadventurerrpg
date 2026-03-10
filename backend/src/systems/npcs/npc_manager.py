import math
from typing import List, Dict, Optional, Tuple
from .npc import NPC
from .generador import GeneradorNPC
from ..seed import WorldSeed

class NPCManager:
    """Gestor de NPCs: carga, caché y simulación de radio activo."""
    
    RADIO_ACTIVO_TILES = 500 # Radio de simulación activa definido por el usuario

    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.generador = GeneradorNPC(seed)
        self.npcs_cargados: Dict[str, NPC] = {} # id -> NPC
        self.npcs_activos_ids: List[str] = []
        self.rumores: List[Dict] = []
        self.version = "1.0"

    def cargar_desde_save(self, data: Dict):
        """Carga el estado de los NPCs desde el diccionario del save."""
        self.version = data.get("version", "1.0")
        self.rumores = data.get("rumores", [])
        
        por_id = data.get("por_id", {})
        self.npcs_cargados = {}
        for npc_id, npc_data in por_id.items():
            self.npcs_cargados[npc_id] = NPC.from_dict(npc_data)
            
        self.npcs_activos_ids = data.get("activos", [])

    def to_dict(self) -> Dict:
        """Serializa el estado para el save."""
        return {
            "version": self.version,
            "activos": self.npcs_activos_ids,
            "por_id": {npc_id: npc.to_dict() for npc_id, npc in self.npcs_cargados.items()},
            "rumores": self.rumores
        }

    def actualizar_activos(self, jugador_tile: Tuple[int, int]):
        """
        Actualiza la lista de NPCs activos basados en la posición del jugador.
        NPCs fuera del radio se 'compactan' (se mantienen en por_id pero no en activos).
        """
        self.npcs_activos_ids = []
        for npc_id, npc in self.npcs_cargados.items():
            dist = self._calcular_distancia(jugador_tile, npc.ubicacion.tile)
            if dist <= self.RADIO_ACTIVO_TILES:
                self.npcs_activos_ids.append(npc_id)

    def obtener_npc(self, npc_id: str) -> Optional[NPC]:
        return self.npcs_cargados.get(npc_id)

    def registrar_npc(self, npc: NPC):
        self.npcs_cargados[npc.id] = npc

    def generar_npcs_para_ubicacion(self, ubicacion_id: str, tipo: str, tile: Tuple[int, int], cantidad: int = 10):
        """Genera un grupo de NPCs para una nueva ubicación descubierta."""
        for i in range(cantidad):
            npc_id = f"npc_{ubicacion_id}_{i}"
            if npc_id not in self.npcs_cargados:
                nuevo_npc = self.generador.generar_npc(npc_id, ubicacion_id, tipo, tile)
                self.registrar_npc(nuevo_npc)

    def _calcular_distancia(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_npcs_en_ubicacion(self, ubicacion_id: str) -> List[NPC]:
        """Retorna lista de NPCs que están actualmente en una ubicación."""
        return [npc for npc in self.npcs_cargados.values() if npc.ubicacion.ubicacion_id == ubicacion_id]
