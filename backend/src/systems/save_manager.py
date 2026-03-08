import json
import os
from datetime import datetime

class SaveManager:
    """Sistema de guardado y carga de partidas"""

    SLOTS_DIR = "saves"
    NUM_SLOTS = 3
    VERSION = "1.1"  # Actualizado para incluir exploracion

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

        return data

    def crear_save_vacio(self, nombre="", genero="no_especificar", dificultad="normal"):
        """Crea una estructura de save vacía para nueva partida"""
        from models.stats import Stats
        from models.experiencia import SistemaHabilidades
        from systems.exploracion_state import crear_exploracion_inicial
        from systems.seed import init_global_seed

        stats = Stats(dificultad=dificultad)
        habilidades = SistemaHabilidades()
        
        # Crear semilla y estado de exploracion
        seed = init_global_seed()
        exploracion = crear_exploracion_inicial(str(seed))

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
                "npcs_conocidos": []
            },
            "exploracion": exploracion.to_dict()
        }