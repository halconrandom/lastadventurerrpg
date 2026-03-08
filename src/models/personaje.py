from models.entidad import Entidad
from models.stats import Stats
from models.experiencia import SistemaHabilidades


class Personaje(Entidad):
    def __init__(self, nombre, hp, ataque, defensa, nivel):
        # Inicializar Entidad (nombre, hp, ataque, defensa)
        super().__init__(nombre, hp, ataque, defensa)

        # Sistema de stats (incluye nivel y experiencia)
        self.stats = Stats()
        self.stats.nivel = nivel

        # Sistema de habilidades
        self.habilidades = SistemaHabilidades()

    def ganar_experiencia(self, cantidad):
        """Gana experiencia y sube de nivel si es necesario"""
        exito, mensaje = self.stats.ganar_experiencia(cantidad)
        if "Subiste" in mensaje:
            # Actualizar hp_max del personaje con los nuevos stats
            self.hp_max = self.stats.get_hp_max()
            self.ataque = self.stats.get_atk()
            self.defensa = self.stats.get_def()
        return exito, mensaje

    def ganar_experiencia_habilidad(self, nombre_habilidad, cantidad):
        """Gana experiencia en una habilidad específica"""
        return self.habilidades.ganar_experiencia_habilidad(nombre_habilidad, cantidad)

    def get_nivel(self):
        """Retorna el nivel del personaje"""
        return self.stats.nivel

    def get_nivel_defensa(self):
        """Retorna el nivel de la habilidad Defensa"""
        return self.habilidades.get_nivel_defensa()

    def calcular_daño_total(self, nombre_habilidad, daño_arma=0):
        """Calcula el daño total con multiplicador de habilidad"""
        habilidad = self.habilidades.obtener_habilidad(nombre_habilidad)
        if habilidad:
            multiplicador = habilidad.obtener_multiplicador()
            return int((self.ataque + daño_arma) * multiplicador)
        return self.ataque + daño_arma

    def calcular_reduccion_total(self):
        """Calcula la reducción de daño total (stats + habilidad defensa)"""
        reduccion_stats = self.stats.get_def()
        reduccion_habilidad = self.get_nivel_defensa()
        return min(reduccion_stats + reduccion_habilidad, 80)

    def to_dict(self):
        """Serializa el personaje a diccionario"""
        return {
            "nombre": self.nombre,
            "hp": self.hp,
            "hp_max": self.hp_max,
            "ataque": self.ataque,
            "defensa": self.defensa,
            "stats": self.stats.to_dict(),
            "habilidades": self.habilidades.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un Personaje desde un diccionario"""
        personaje = cls(
            data["nombre"],
            data.get("hp", 100),
            data.get("ataque", 10),
            data.get("defensa", 0),
            1
        )
        personaje.hp = data.get("hp", personaje.hp)
        personaje.hp_max = data.get("hp_max", personaje.hp)

        if "stats" in data:
            personaje.stats = Stats.from_dict(data["stats"])

        if "habilidades" in data:
            personaje.habilidades = SistemaHabilidades.from_dict(data["habilidades"])

        return personaje

    def __str__(self):
        return f"{self.nombre} - Nv{self.get_nivel()} | HP: {self.hp}/{self.hp_max} | ATK: {self.ataque} | DEF: {self.defensa}"
