import time
import os
import sys

# Añadir src al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from systems.save_manager import SaveManager
from game_manager import crear_nuevo_personaje
from models.stats import Stats

class Juego:
    """Clase principal del juego"""

    def __init__(self):
        self.save_manager = SaveManager()
        self.datos_juego = None
        self.en_combate = False

    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        """Muestra el menú principal del juego"""
        self.limpiar_pantalla()
        print("=" * 40)
        print("         LAST ADVENTURER")
        print("=" * 40)
        print()
        print("1. Nueva Partida")
        print("2. Cargar Partida")
        print("3. Salir")
        print()

    def menu_cargar_partida(self):
        """Muestra el menú de cargar partida"""
        self.limpiar_pantalla()
        print("=" * 40)
        print("        CARGAR PARTIDA")
        print("=" * 40)
        print()

        for slot in range(1, SaveManager.NUM_SLOTS + 1):
            info = self.save_manager.obtener_info_slot(slot)
            if info:
                dificultad_str = f"[{info.get('dificultad', 'normal').capitalize()}]"
                print(f"{slot}. {info['nombre']} - Nv{info['nivel']} {dificultad_str} - {info['zona']}")
            else:
                print(f"{slot}. [Vacío]")

        print()
        print(f"{SaveManager.NUM_SLOTS + 1}. Volver")
        print()

    def nueva_partida(self):
        """Inicia una nueva partida"""
        # Buscar slot libre
        slot_libre = None
        for slot in range(1, SaveManager.NUM_SLOTS + 1):
            if not self.save_manager.slot_existe(slot):
                slot_libre = slot
                break

        if slot_libre is None:
            # Todos los slots ocupados
            self.limpiar_pantalla()
            print("=" * 40)
            print("        NUEVA PARTIDA")
            print("=" * 40)
            print()
            print("Todos los slots están ocupados.")
            print("Debes eliminar una partida para crear una nueva.")
            print()
            input("Presiona Enter para volver...")
            return

        # Crear personaje con el nuevo flujo
        personaje = crear_nuevo_personaje()

        if personaje:
            # Crear datos iniciales usando el personaje creado
            self.datos_juego = self.save_manager.crear_save_vacio(
                nombre=personaje.nombre,
                genero=personaje.genero,
                dificultad=personaje.stats.dificultad
            )
            self.datos_juego["personaje"]["stats"] = personaje.stats.to_dict()
            self.datos_juego["personaje"]["habilidades"] = personaje.habilidades.to_dict()

            # Guardar en el slot libre
            exito, mensaje = self.save_manager.guardar(slot_libre, self.datos_juego)

            if exito:
                print(f"\n{mensaje}")
                print(f"Partida guardada en Slot {slot_libre}")
                time.sleep(2)
                self.jugar()
            else:
                print(f"\nError: {mensaje}")
                input("Presiona Enter para volver...")
        else:
            # Creación cancelada - volver al menú principal silenciosamente
            pass

    def cargar_partida(self):
        """Carga una partida existente"""
        while True:
            self.menu_cargar_partida()
            opcion = input("Selecciona: ")

            if opcion == str(SaveManager.NUM_SLOTS + 1):
                return

            try:
                slot = int(opcion)
                if 1 <= slot <= SaveManager.NUM_SLOTS:
                    datos, mensaje = self.save_manager.cargar(slot)
                    if datos:
                        self.datos_juego = datos
                        print(f"\n{mensaje}")
                        time.sleep(1)
                        self.jugar()
                        return
                    else:
                        print(f"\n{mensaje}")
                        time.sleep(1)
                else:
                    print("\nOpción inválida")
                    time.sleep(1)
            except ValueError:
                print("\nIngresa un número válido")
                time.sleep(1)

    def guardar_automatico(self):
        """Guardado automático durante el juego"""
        if self.en_combate:
            return  # No guardar durante combate

        # Buscar slot con el nombre del personaje actual
        for slot in range(1, SaveManager.NUM_SLOTS + 1):
            info = self.save_manager.obtener_info_slot(slot)
            if info and info["nombre"] == self.datos_juego["personaje"]["nombre"]:
                self.save_manager.guardar(slot, self.datos_juego)
                break

    def jugar(self):
        """Loop principal del juego"""
        while True:
            self.limpiar_pantalla()
            stats = self.datos_juego["personaje"]["stats"]
            nivel = stats.get("nivel", 1)
            dificultad = stats.get("dificultad", "normal").capitalize()
            print("=" * 40)
            print(f"  {self.datos_juego['personaje']['nombre']} - Nivel {nivel}")
            print(f"  Dificultad: {dificultad}")
            print("=" * 40)
            print()
            print("1. Explorar")
            print("2. Inventario")
            print("3. Personaje")
            print("4. Guardar")
            print("5. Menú Principal")
            print()

            opcion = input("Selecciona: ")

            if opcion == "1":
                self.explorar()
            elif opcion == "2":
                self.ver_inventario()
            elif opcion == "3":
                self.ver_personaje()
            elif opcion == "4":
                self.guardar_manual()
            elif opcion == "5":
                self.guardar_automatico()
                return

    def explorar(self):
        """Placeholder para exploración"""
        self.limpiar_pantalla()
        print("Explorando...")
        print("(Funcionalidad en desarrollo)")
        input("\nPresiona Enter para volver...")

    def ver_inventario(self):
        """Muestra el inventario"""
        self.limpiar_pantalla()
        print("=" * 30)
        print("      INVENTARIO")
        print("=" * 30)
        print()

        inventario = self.datos_juego["inventario"]
        print(f"Oro: {inventario['oro']}")
        print(f"Slots: {len(inventario['items'])}/{inventario['slots_maximos']}")
        print()

        if inventario["items"]:
            print("Items:")
            for item in inventario["items"]:
                print(f"  - {item['id']} x{item['cantidad']}")
        else:
            print("Inventario vacío")

        print()
        input("Presiona Enter para volver...")

    def ver_personaje(self):
        """Muestra los stats del personaje"""
        self.limpiar_pantalla()
        print("=" * 40)
        print("          PERSONAJE")
        print("=" * 40)
        print()

        p = self.datos_juego["personaje"]
        stats = Stats.from_dict(p["stats"])

        # Mostrar datos personales
        print(f"Nombre: {p['nombre']}")
        print(f"Género: {p.get('genero', 'no_especificar').capitalize()}")
        print(f"Dificultad: {stats.dificultad.capitalize()}")
        print()
        print(stats)
        print()

        print("Habilidades:")
        for nombre, datos in p["habilidades"].items():
            print(f"  {nombre}: Nivel {datos['nivel']} ({datos['experiencia']} exp)")
        print()

        input("Presiona Enter para volver...")

    def guardar_manual(self):
        """Guardado manual desde el menú"""
        print("\nGuardando partida...")
        self.guardar_automatico()
        print("Partida guardada.")
        time.sleep(1)

    def iniciar(self):
        """Punto de entrada del juego"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Selecciona: ")

            if opcion == "1":
                self.nueva_partida()
            elif opcion == "2":
                self.cargar_partida()
            elif opcion == "3":
                print("\n¡Hasta pronto!")
                break
            else:
                print("\nOpción inválida")
                time.sleep(1)


if __name__ == "__main__":
    juego = Juego()
    juego.iniciar()