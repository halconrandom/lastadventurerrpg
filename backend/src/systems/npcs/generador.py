import random
from typing import List, Dict, Optional, Tuple
from .npc import NPC, Personalidad, EstadoNPC, UbicacionNPC, Rutina, MemoriaNPC, RelacionJugador, EstadoVital
from ..seed import WorldSeed
from ..nombres import NombreGenerator

class GeneradorNPC:
    """Generador procedural determinista de NPCs."""
    
    ROLES_POR_UBICACION = {
        "pueblo": ["tabernero", "herrero", "comerciante", "guardia", "aldeano", "alcalde", "curandero"],
        "ciudad": ["tabernero", "herrero", "comerciante", "guardia", "noble", "bibliotecario", "alquimista", "mendigo", "artesano"],
        "fortaleza": ["comandante", "guardia", "herrero", "cocinero", "prisionero"],
        "templo": ["sacerdote", "monje", "peregrino", "acólito"],
        "ruinas": ["explorador", "bandido", "ermitaño", "fantasma"],
        "bosque": ["cazador", "leñador", "ermitaño", "druida"]
    }
    
    RASGOS_DISPONIBLES = [
        "generoso", "tacaño", "valiente", "cobarde", "curioso", "fanático", 
        "paranoico", "honorable", "mentiroso", "ambicioso", "pragmático",
        "leal", "desconfiado", "optimista", "pesimista", "estoico", "irascible"
    ]
    
    VALORES_DISPONIBLES = [
        "lealtad", "orden", "caos", "riqueza", "familia", "honor", 
        "conocimiento", "supervivencia", "justicia", "venganza"
    ]
    
    RAZAS_PROPORCIONES = {
        "humano": 0.5,
        "elfo": 0.15,
        "enano": 0.15,
        "orco": 0.1,
        "gnomo": 0.05,
        "halfling": 0.05
    }

    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.nombre_gen = NombreGenerator(seed)

    def generar_npc(self, npc_id: str, ubicacion_id: Optional[str] = None, tipo_ubicacion: str = "pueblo", tile: Tuple[int, int] = (0,0)) -> NPC:
        """Genera un NPC completo de forma determinista basado en su ID."""
        rng = self.seed.get_rng(f"gen_npc_{npc_id}")
        
        # 1. Identidad Básica
        genero = rng.choice(["masculino", "femenino"])
        raza = self._elegir_raza(rng)
        nombre_completo = self.nombre_gen.generar_nombre_npc(npc_id, genero=genero)
        
        # 2. Rol
        roles_posibles = self.ROLES_POR_UBICACION.get(tipo_ubicacion, ["aldeano"])
        rol_tipo = rng.choice(roles_posibles)
        
        # 3. Personalidad
        personalidad = self._generar_personalidad(rng)
        
        # 4. Estado Inicial
        estado = EstadoNPC(
            vital=EstadoVital.VIVO,
            hp=100,
            hp_max=100,
            oro=rng.randint(10, 500)
        )
        
        # 5. Ubicación
        ubicacion = UbicacionNPC(
            tile=tile,
            ubicacion_id=ubicacion_id,
            modo="mundial"
        )
        
        # 6. Rutina (Básica por ahora)
        rutina = self._generar_rutina_basica(rol_tipo, ubicacion_id or "desconocido")
        
        # 7. NPC Object
        npc = NPC(
            id=npc_id,
            nombre=nombre_completo,
            genero=genero,
            raza=raza,
            rol_tipo=rol_tipo,
            personalidad=personalidad,
            estado=estado,
            ubicacion=ubicacion,
            rutina=rutina,
            año_nacimiento=rng.randint(1, 100) # Simplificado
        )
        
        return npc

    def _elegir_raza(self, rng) -> str:
        r = rng.random()
        acumulado = 0
        for raza, prop in self.RAZAS_PROPORCIONES.items():
            acumulado += prop
            if r <= acumulado:
                return raza
        return "humano"

    def _generar_personalidad(self, rng) -> Personalidad:
        rasgos = rng.sample(self.RASGOS_DISPONIBLES, 2)
        valores = rng.sample(self.VALORES_DISPONIBLES, 1)
        
        sliders = {
            "agresividad": rng.random(),
            "empatía": rng.random(),
            "codicia": rng.random(),
            "chisme": rng.random(),
            "valentía": rng.random(),
            "honor": rng.random(),
            "paciencia": rng.random(),
            "supersticion": rng.random()
        }
        
        return Personalidad(
            rasgos=rasgos,
            valores=valores,
            sliders=sliders,
            tono_voz=rng.choice(["seco", "amable", "autoritario", "susurrante", "alegre"]),
            registro_voz=rng.choice(["coloquial", "formal", "vulgar"])
        )

    def _generar_rutina_basica(self, rol: str, ubicacion_id: str) -> Rutina:
        # Agenda estándar: dormir 22-06, trabajar 08-18
        agenda = [
            {"desde": "00:00", "hasta": "06:00", "actividad": "dormir"},
            {"desde": "06:00", "hasta": "08:00", "actividad": "desayunar"},
            {"desde": "08:00", "hasta": "12:00", "actividad": "trabajar"},
            {"desde": "12:00", "hasta": "14:00", "actividad": "comer"},
            {"desde": "14:00", "hasta": "18:00", "actividad": "trabajar"},
            {"desde": "18:00", "hasta": "22:00", "actividad": "ocio"},
            {"desde": "22:00", "hasta": "23:59", "actividad": "dormir"}
        ]
        return Rutina(zona_base_id=ubicacion_id, agenda_diaria=agenda)
