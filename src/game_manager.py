from models.arquetipo import cargar_arquetipos
from models.personaje import Personaje

def crear_personaje():
    nombre = input("Ingresa tu nombre: ")

    arquetipos = cargar_arquetipos()

    print("Elige tu clase:")
    for i, ar in enumerate(arquetipos):
        print(f"{i + 1}. {ar.arquetipo} - HP: {ar.hp} ATK: {ar.ataque} DEF: {ar.defensa} - {ar.descripcion}")

    opcion = input("Selecciona: ")
    arquetipo_elegido = arquetipos[int(opcion) - 1]

    # Crear personaje con stats del arquetipo
    personaje = Personaje(nombre, arquetipo_elegido.hp, arquetipo_elegido.ataque, arquetipo_elegido.defensa, 1)

    # Configurar stats según arquetipo
    personaje.stats.hp_base = arquetipo_elegido.hp
    personaje.stats.hp_actual = arquetipo_elegido.hp
    personaje.stats.atk_base = arquetipo_elegido.ataque
    personaje.stats.def_base = arquetipo_elegido.defensa

    # Actualizar valores de Entidad para que coincidan
    personaje.hp = arquetipo_elegido.hp
    personaje.hp_max = arquetipo_elegido.hp
    personaje.ataque = arquetipo_elegido.ataque
    personaje.defensa = arquetipo_elegido.defensa

    print(f"\n¡Bienvenido, {nombre} el {arquetipo_elegido.arquetipo}!")
    print(f"HP: {personaje.hp} | ATK: {personaje.ataque} | DEF: {personaje.defensa}")

    return personaje
