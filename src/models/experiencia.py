class Habilidad:
    """Representa una habilidad individual (Espada, Arco, Magia, etc.)"""

    def __init__(self, nombre, nivel_max=100):
        self.nombre = nombre
        self.nivel = 1
        self.experiencia = 0
        self.nivel_max = nivel_max
        self.perks_desbloqueados = []

    def experiencia_para_subir(self):
        """Calcula la experiencia necesaria para el siguiente nivel"""
        return self.nivel * 100

    def ganar_experiencia(self, cantidad):
        """Añade experiencia y sube de nivel si es necesario"""
        if self.nivel >= self.nivel_max:
            return False

        self.experiencia += cantidad

        # Verificar si sube de nivel
        while self.experiencia >= self.experiencia_para_subir() and self.nivel < self.nivel_max:
            self.experiencia -= self.experiencia_para_subir()
            self.nivel += 1

        return True

    def obtener_multiplicador(self):
        """Retorna el multiplicador de daño basado en el nivel"""
        return 1 + (self.nivel * 0.05)  # 5% extra por nivel

    def get_progreso(self):
        """Retorna el porcentaje de progreso hacia el siguiente nivel"""
        exp_necesaria = self.experiencia_para_subir()
        return int((self.experiencia / exp_necesaria) * 100)

    def to_dict(self):
        """Serializa la habilidad a diccionario"""
        return {
            "nombre": self.nombre,
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "perks_desbloqueados": self.perks_desbloqueados
        }

    @classmethod
    def from_dict(cls, data):
        """Crea una habilidad desde un diccionario"""
        habilidad = cls(data["nombre"])
        habilidad.nivel = data.get("nivel", 1)
        habilidad.experiencia = data.get("experiencia", 0)
        habilidad.perks_desbloqueados = data.get("perks_desbloqueados", [])
        return habilidad

    def __str__(self):
        return f"{self.nombre}: Nv{self.nivel} ({self.get_progreso()}%)"


class SistemaHabilidades:
    """Maneja todas las habilidades del personaje"""

    HABILIDADES_BASE = ["Espada", "Espadón", "Arco", "Magia", "Dagas", "Defensa"]

    def __init__(self):
        self.habilidades = {}
        self._inicializar_habilidades()

    def _inicializar_habilidades(self):
        """Crea las habilidades base"""
        for nombre in self.HABILIDADES_BASE:
            self.habilidades[nombre] = Habilidad(nombre)

    def agregar_habilidad(self, nombre):
        """Agrega una nueva habilidad (extensible)"""
        if nombre not in self.habilidades:
            self.habilidades[nombre] = Habilidad(nombre)
            return True
        return False

    def obtener_habilidad(self, nombre):
        """Retorna una habilidad por su nombre"""
        return self.habilidades.get(nombre)

    def ganar_experiencia_habilidad(self, nombre, cantidad):
        """Añade experiencia a una habilidad específica"""
        habilidad = self.obtener_habilidad(nombre)
        if habilidad:
            habilidad.ganar_experiencia(cantidad)
            return True
        return False

    def get_nivel_defensa(self):
        """Retorna el nivel de la habilidad Defensa (especial)"""
        defensa = self.obtener_habilidad("Defensa")
        return defensa.nivel if defensa else 0

    def listar_habilidades(self):
        """Retorna lista de todas las habilidades con su nivel"""
        return [(nombre, hab.nivel) for nombre, hab in self.habilidades.items()]

    def to_dict(self):
        """Serializa todas las habilidades a diccionario"""
        return {nombre: hab.to_dict() for nombre, hab in self.habilidades.items()}

    @classmethod
    def from_dict(cls, data):
        """Crea un SistemaHabilidades desde un diccionario"""
        sistema = cls()
        sistema.habilidades = {}
        for nombre, hab_data in data.items():
            sistema.habilidades[nombre] = Habilidad.from_dict(hab_data)
        return sistema

    def __str__(self):
        lineas = [str(hab) for hab in self.habilidades.values()]
        return "\n".join(lineas)
