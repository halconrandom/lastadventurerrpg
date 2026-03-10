import json
import os
from datetime import datetime

class SaveManager:
    """Sistema de guardado y carga de partidas"""

    SLOTS_DIR = "saves"
    NUM_SLOTS = 3
    VERSION = "1.5"  # Actualizado para incluir narrativa e historial

    def __init__(self):
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        """Crea el directorio de saves si no existe"""
        if not os.path.exists(self.SLOTS_DIR):
            os.makedirs(self.SLOTS_DIR)

    def _ruta_slot(self, slot_num):
        """Retorna la ruta del archivo de guardado"""
        return os.path.join(self.SLOTS_DIR, f"slot_{slot_num}.json")

    def slot_existe(self, slot_num):
        """Verifica si un slot tiene partida guardada"""
        ruta = self._ruta_slot(slot_num)
        return os.path.exists(ruta)

    def obtener_info_slot(self, slot_num):
        """Obtiene información básica del slot para mostrar en menú"""
        if not self.slot_existe(slot_num):
            return None

        try:
            with open(self._ruta_slot(slot_num), "r", encoding="utf-8") as f:
                data = json.load(f)
                # El nivel y dificultad están en stats
                stats = data["personaje"].get("stats", {})
                nivel = stats.get("nivel", 1)
                dificultad = stats.get("dificultad", "normal")
                
                # Obtener zona actual de exploracion
                exploracion = data.get("exploracion", {})
                zona_actual = exploracion.get("zonas", {})
                if zona_actual:
                    # Obtener la ultima zona visitada
                    x = exploracion.get("x", 0)
                    y = exploracion.get("y", 0)
                    zona_key = f"{x}_{y}"
                    if zona_key in zona_actual:
                        zona_nombre = zona_actual[zona_key].get("nombre", "Desconocida")
                    else:
                        zona_nombre = "Desconocida"
                else:
                    zona_nombre = "Pueblo Inicio"
                
                return {
                    "nombre": data["personaje"]["nombre"],
                    "nivel": nivel,
                    "dificultad": dificultad,
                    "zona": zona_nombre,
                    "fecha": data["fecha"]
                }
        except Exception:
            return None

    def guardar(self, slot_num, juego_data):
        """Guarda la partida en un slot"""
        if slot_num < 1 or slot_num > self.NUM_SLOTS:
            return False, "Slot inválido"

        # Añadir metadatos
        data = {
            "version": self.VERSION,
            "fecha": datetime.now().isoformat(),
            **juego_data
        }

        try:
            with open(self._ruta_slot(slot_num), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, "Partida guardada correctamente"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    def cargar(self, slot_num):
        """Carga una partida desde un slot"""
        if not self.slot_existe(slot_num):
            return None, "Slot vacío"

        try:
            with open(self._ruta_slot(slot_num), "r", encoding="utf-8") as f:
                data = json.load(f)

            # Verificar versión y migrar si es necesario
            data = self._migrar_si_necesario(data)

            return data, "Partida cargada correctamente"
        except Exception as e:
            return None, f"Error al cargar: {str(e)}"

    def eliminar(self, slot_num):
        """Elimina una partida guardada"""
        if not self.slot_existe(slot_num):
            return False, "Slot vacío"

        try:
            os.remove(self._ruta_slot(slot_num))
            return True, "Partida eliminada"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def _migrar_si_necesario(self, data):
        """Migra datos antiguos a la versión actual"""
        version_guardada = data.get("version", "0.0")

        # Migracion de 1.0 a 1.1: añadir exploracion
        if version_guardada == "1.0" and "exploracion" not in data:
            from systems.exploracion_state import crear_exploracion_inicial
            from systems.seed import init_global_seed
            
            # Crear semilla si no existe
            seed = init_global_seed()
            data["exploracion"] = crear_exploracion_inicial(str(seed)).to_dict()

        # Migración de 1.1 a 1.2: añadir mapa
        if version_guardada in ["1.0", "1.1"] and "mapa" not in data:
            from systems.mapa import MapaMundo
            from systems.seed import init_global_seed
            
            # Crear semilla si no existe
            seed = init_global_seed()
            mapa = MapaMundo(seed=seed)
            # Generar mundo inicial con ubicaciones
            mapa.generar_mundo_inicial()
            data["mapa"] = mapa.to_dict()

        # Migración de 1.2 a 1.3: añadir NPCs
        if version_guardada in ["1.0", "1.1", "1.2"] and "npcs" not in data:
            data["npcs"] = {
                "version": "1.0",
                "activos": [],
                "por_id": {},
                "rumores": []
            }

        # Migración de 1.3 a 1.4: añadir tiempo
        if version_guardada in ["1.0", "1.1", "1.2", "1.3"] and "tiempo" not in data:
            data["tiempo"] = {"tick_total": 480} # 08:00 AM

        # Migración de 1.4 a 1.5: añadir historial y tags
        if version_guardada in ["1.0", "1.1", "1.2", "1.3", "1.4"]:
            if "historial_eventos" not in data:
                data["historial_eventos"] = []
            if "progreso" not in data:
                data["progreso"] = {}
            if "tags" not in data["progreso"]:
                data["progreso"]["tags"] = []

        # Migración de stats: añadir aliases para frontend
        if "personaje" in data and "stats" in data["personaje"]:
            stats = data["personaje"]["stats"]
            
            # Añadir aliases si no existen
            if "hp" not in stats:
                stats["hp"] = stats.get("hp_actual", stats.get("hp_base", 100))
            if "hp_max" not in stats:
                stats["hp_max"] = stats.get("hp_base", 100)
            if "mana" not in stats:
                stats["mana"] = stats.get("mana_actual", stats.get("mana_base", 50))
            if "mana_max" not in stats:
                stats["mana_max"] = stats.get("mana_base", 50)
            if "stamina" not in stats:
                stats["stamina"] = stats.get("stamina_actual", stats.get("stamina_base", 100))
            if "stamina_max" not in stats:
                stats["stamina_max"] = stats.get("stamina_base", 100)
            if "ataque" not in stats:
                stats["ataque"] = stats.get("atk_base", 10)
            if "defensa" not in stats:
                stats["defensa"] = stats.get("def_base", 5)
            if "velocidad" not in stats:
                stats["velocidad"] = stats.get("velocidad_base", 10)
            if "critico" not in stats:
                stats["critico"] = stats.get("critico_base", 5)
            if "evasion" not in stats:
                stats["evasion"] = stats.get("evasion_base", 5)
            if "experiencia_necesaria" not in stats:
                # Calcular experiencia necesaria para el nivel actual
                nivel = stats.get("nivel", 1)
                stats["experiencia_necesaria"] = int(nivel * 100 * (1 + nivel * 0.1))
            if "puntos_distribuibles" not in stats:
                stats["puntos_distribuibles"] = stats.get("puntos_disponibles", 0)

        return data

    def crear_save_vacio(self, nombre="", genero="no_especificar", dificultad="normal"):
        """Crea una estructura de save vacía para nueva partida"""
        from models.stats import Stats
        from models.experiencia import SistemaHabilidades
        from systems.exploracion_state import crear_exploracion_inicial
        from systems.mapa import MapaMundo
        from systems.seed import init_global_seed

        stats = Stats(dificultad=dificultad)
        habilidades = SistemaHabilidades()
        
        # Crear semilla y estado de exploracion
        seed = init_global_seed()
        exploracion = crear_exploracion_inicial(str(seed))
        
        # Crear mapa del mundo
        mapa = MapaMundo(seed=seed)
        mapa.generar_mundo_inicial()

        return {
            "personaje": {
                "nombre": nombre,
                "genero": genero,
                "stats": stats.to_dict(),
                "habilidades": habilidades.to_dict()
            },
            "perks_desbloqueados": [],
            "inventario": {
                "slots_maximos": 10,
                "items": [],
                "materiales": [],
                "oro": 0
            },
            "equipamiento": {
                "arma": None,
                "casco": None,
                "peto": None,
                "botas": None
            },
            "progreso": {
                "misiones_completadas": [],
                "misiones_activas": [],
                "zonas_visitadas": ["pueblo_inicio"],
                "npcs_conocidos": [],
                "tags": []
            },
            "exploracion": exploracion.to_dict(),
            "mapa": mapa.to_dict(),
            "npcs": {
                "version": "1.0",
                "activos": [],
                "por_id": {},
                "rumores": []
            },
            "tiempo": {"tick_total": 480},
            "historial_eventos": []
        }