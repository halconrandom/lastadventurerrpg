class Entidad:
    def __init__(self, nombre, hp, ataque, defensa):
        self.nombre = nombre
        self.hp = hp
        self.hp_max = hp
        self.ataque = ataque
        self.defensa = defensa

    def esta_vivo(self):
        return self.hp > 0

    def recibir_daño(self, cantidad):
        daño_real = cantidad - self.defensa
        if daño_real < 0:
            daño_real = 0
        self.hp -= daño_real

    def curar(self, cantidad):
        self.hp += cantidad
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        
    def atacar(self, objetivo):
        objetivo.recibir_daño(self.ataque)
        print(f"{self.nombre} ataca a {objetivo.nombre}")
        