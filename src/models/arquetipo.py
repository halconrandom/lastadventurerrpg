import json

def cargar_arquetipos():
    with open("src/data/arquetipos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    arquetipos = []
    for dato in datos:
        nuevo_arquetipo = Arquetipo(dato["arquetipo"], dato["hp"], dato["ataque"], dato["defensa"], dato["descripcion"])
        arquetipos.append(nuevo_arquetipo)

    return arquetipos

class Arquetipo:
    def __init__(self, arquetipo, hp, ataque, defensa, descripcion):
        self.arquetipo = arquetipo
        self.hp = hp
        self.ataque = ataque
        self.defensa = defensa
        self.descripcion = descripcion
