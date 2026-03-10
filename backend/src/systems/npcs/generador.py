import random
from typing import List, Dict, Optional, Tuple
from systems.npcs.npc import NPC, Personalidad, EstadoNPC, UbicacionNPC, Rutina, MemoriaNPC, RelacionJugador, RelacionNPC, EstadoVital, TipoRelacion
from systems.seed import WorldSeed
from systems.nombres import NombreGenerator

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
    
    # Rasgos apropiados por rol (máximo 2 de esta lista)
    RASGOS_POR_ROL = {
        "alcalde": ["honorable", "pragmático", "ambicioso", "estoico", "leal", "desconfiado"],
        "tabernero": ["amable", "curioso", "chismoso", "generoso", "pragmático"],
        "herrero": ["estoico", "honorable", "pragmático", "valiente", "leal"],
        "comerciante": ["pragmático", "ambicioso", "tacaño", "generoso", "desconfiado"],
        "guardia": ["valiente", "honorable", "leal", "estoico", "desconfiado"],
        "curandero": ["generoso", "curioso", "pragmático", "leal", "optimista"],
        "aldeano": ["generoso", "curioso", "optimista", "pesimista", "leal"],
        "noble": ["ambicioso", "honorable", "tacaño", "generoso", "desconfiado"],
        "sacerdote": ["honorable", "leal", "fanático", "generoso", "estoico"],
        "cazador": ["valiente", "pragmático", "curioso", "estoico", "desconfiado"],
        "aldeano": ["generoso", "curioso", "optimista", "pesimista", "leal", "pragmático"],
    }
    
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
        personalidad = self._generar_personalidad(rng, rol_tipo)
        
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

    def _generar_personalidad(self, rng, rol: str = "aldeano") -> Personalidad:
        # Usar rasgos apropiados para el rol
        rasgos_posibles = self.RASGOS_POR_ROL.get(rol, self.RASGOS_POR_ROL.get("aldeano", self.RASGOS_DISPONIBLES))
        rasgos = rng.sample(rasgos_posibles, min(2, len(rasgos_posibles)))
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

        # Generar ejes de conducta persistente (-100 a 100)
        moralidad = rng.randint(-100, 100)
        sociabilidad = rng.randint(-100, 100)
        templanza = rng.randint(-100, 100)
        
        return Personalidad(
            rasgos=rasgos,
            valores=valores,
            sliders=sliders,
            moralidad=moralidad,
            sociabilidad=sociabilidad,
            templanza=templanza,
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

    def generar_relaciones_iniciales(
        self, 
        npc: NPC, 
        otros_npcs: List[NPC],
        ubicacion_id: str
    ) -> None:
        """
        Genera relaciones iniciales para un NPC basándose en su rol y ubicación.
        
        Args:
            npc: NPC al que se le generan relaciones
            otros_npcs: Lista de otros NPCs en la misma ubicación
            ubicacion_id: ID de la ubicación actual
        """
        rng = self.seed.get_rng(f"rel_{npc.id}")
        
        # Relaciones predefinidas por rol (hardcodeadas para NPCs importantes)
        relaciones_predefinidas = self._obtener_relaciones_predefinidas(npc.nombre, ubicacion_id)
        
        for rel_data in relaciones_predefinidas:
            npc.relaciones_npcs.append(RelacionNPC(
                npc_id=rel_data["npc_id"],
                nombre=rel_data["nombre"],
                tipo=TipoRelacion(rel_data["tipo"]),
                intensidad=rel_data.get("intensidad", 50),
                confianza=rel_data.get("confianza", 50),
                notas=rel_data.get("notas", "")
            ))
        
        # Generar relaciones aleatorias con otros NPCs de la ubicación
        for otro in otros_npcs:
            if otro.id == npc.id:
                continue
            
            # Probabilidad de tener una relación (30% base)
            if rng.random() < 0.3:
                tipo = self._determinar_tipo_relacion(npc.rol_tipo, otro.rol_tipo, rng)
                intensidad = rng.randint(30, 70)
                confianza = rng.randint(30, 70)
                
                npc.relaciones_npcs.append(RelacionNPC(
                    npc_id=otro.id,
                    nombre=otro.nombre,
                    tipo=tipo,
                    intensidad=intensidad,
                    confianza=confianza,
                    notas=""
                ))
    
    def _obtener_relaciones_predefinidas(self, nombre_npc: str, ubicacion_id: str) -> List[Dict]:
        """
        Retorna relaciones predefinidas para NPCs importantes.
        
        Args:
            nombre_npc: Nombre del NPC
            ubicacion_id: ID de la ubicación
        
        Returns:
            Lista de diccionarios con datos de relación
        """
        # Base de datos de relaciones predefinidas
        # Formato: {nombre_npc: [{npc_id, nombre, tipo, intensidad, confianza, notas}]}
        RELACIONES_PREDEFINIDAS = {
            "Dorian Xavier": [
                {
                    "npc_id": "npc_adelina",
                    "nombre": "Adelina",
                    "tipo": "romance",
                    "intensidad": 90,
                    "confianza": 85,
                    "notas": "Prometidos hace 2 años. Ella trabaja en la taberna."
                },
                {
                    "npc_id": "npc_gareth",
                    "nombre": "Gareth",
                    "tipo": "rivalidad",
                    "intensidad": 60,
                    "confianza": 20,
                    "notas": "También interesado en Adelina. Dorian desconfía de él."
                }
            ],
            "Adelina": [
                {
                    "npc_id": "npc_dorian",
                    "nombre": "Dorian Xavier",
                    "tipo": "romance",
                    "intensidad": 90,
                    "confianza": 85,
                    "notas": "Prometidos. Él es celoso y protector."
                }
            ],
            # Agregar más NPCs según sea necesario
        }
        
        return RELACIONES_PREDEFINIDAS.get(nombre_npc, [])
    
    def _determinar_tipo_relacion(self, rol1: str, rol2: str, rng) -> TipoRelacion:
        """Determina el tipo de relación entre dos NPCs basándose en sus roles."""
        # Tabla de probabilidades por combinación de roles
        if rol1 == rol2:
            # Mismo rol: probablemente colegas o rivales
            return rng.choice([TipoRelacion.PROFESIONAL, TipoRelacion.RIVALIDAD, TipoRelacion.AMISTAD])
        
        # Roles complementarios
        if (rol1 == "tabernero" and rol2 in ["aldeano", "comerciante"]) or \
           (rol2 == "tabernero" and rol1 in ["aldeano", "comerciante"]):
            return rng.choice([TipoRelacion.CONOCIDO, TipoRelacion.AMISTAD])
        
        if (rol1 == "guardia" and rol2 == "aldeano") or \
           (rol2 == "guardia" and rol1 == "aldeano"):
            return TipoRelacion.CONOCIDO
        
        # Default
        return rng.choice([TipoRelacion.CONOCIDO, TipoRelacion.AMISTAD])
