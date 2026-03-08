from models.entidad import Entidad


class Personaje(Entidad):
    def __init__(self, nombre, hp, ataque, defensa, nivel, experiencia):
        super().__init__(nombre, hp, ataque, defensa)
        self.nivel = nivel
        self.experiencia = experiencia

