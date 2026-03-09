"""
Demo interactivo del Sistema de Mapa.

Ejecuta: python experiments/mapa/demo.py
"""

import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tile import Tile, EstadoVisibilidad
from chunk import GestorChunks
from ubicacion import Ubicacion, UbicacionGenerator, TipoUbicacion
from ruta import Ruta, RutaGenerator, TipoRuta
from mapa import MapaMundo
from cartografia import SistemaCartografia, TipoMapa, CalidadMapa
import random


class MockSeed:
    """Mock de WorldSeed para la demo."""
    
    def __init__(self, seed_value=12345):
        self.seed_value = seed_value
        self.rng_states = {}
    
    def get_rng(self, contexto: str):
        if contexto not in self.rng_states:
            seed = hash(f"{self.seed_value}_{contexto}") % (2**32)
            self.rng_states[contexto] = random.Random(seed)
        return self.rng_states[contexto]


def limpiar_pantalla():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_mapa(mapa, radio=8):
    """Muestra el mapa visual."""
    visual = mapa.get_mapa_visual(radio=radio)
    
    print("\n" + "=" * (radio * 2 + 3))
    print(" MAPA DEL MUNDO")
    print("=" * (radio * 2 + 3))
    
    # Leyenda
    print("\nLeyenda:")
    print("  📍 = Tu posición")
    print("  🏘️ = Pueblo  |  🏰 = Ciudad  |  👑 = Capital")
    print("  ⚔️ = Mazmorra |  ✨ = POI")
    print("  🌲 = Bosque   |  🏔️ = Montaña |  🌾 = Pradera")
    print("  · = Descubierto (no explorado)")
    print("  ? = No descubierto")
    print()
    
    # Números de columna
    header = "   "
    for i in range(-radio, radio + 1):
        header += f"{i:2d}" if abs(i) < 10 else f"{i:2d}"[-2:]
    print(header)
    
    for i, fila in enumerate(visual):
        y = mapa.posicion_jugador[1] - radio + i
        linea = f"{y:3d} "
        for celda in fila:
            linea += celda + " "
        print(linea)


def mostrar_estado(mapa, cartografia):
    """Muestra el estado actual."""
    estado = mapa.get_estado_mapa()
    stats = cartografia.get_estadisticas()
    
    print("\n" + "-" * 40)
    print(" ESTADO DEL JUGADOR")
    print("-" * 40)
    print(f" Posición: ({estado['posicion_jugador'][0]}, {estado['posicion_jugador'][1]})")
    print(f" Tiles explorados: {estado['tiles_explorados']}")
    print(f" Ubicaciones descubiertas: {estado['ubicaciones_descubiertas']}/{estado['total_ubicaciones']}")
    print(f" Rutas descubiertas: {estado['rutas_descubiertas']}")
    print()
    print(f" Cartografía - Nivel: {stats['nombre_nivel']} ({stats['nivel']}/8)")
    print(f" Precisión: {stats['precision']*100:.0f}%")
    print(f" Radio de visión: {stats['radio_vision']} tiles")


def mostrar_ubicaciones_cercanas(mapa, radio=30):
    """Muestra las ubicaciones cercanas."""
    destinos = mapa.get_destinos_cercanos(radio=radio)
    
    print("\n" + "-" * 40)
    print(f" UBICACIONES CERCANAS (radio: {radio} tiles)")
    print("-" * 40)
    
    if not destinos:
        print(" No hay ubicaciones cercanas.")
        return
    
    for i, d in enumerate(destinos[:10]):  # Mostrar máximo 10
        u = d['ubicacion']
        distancia = d['distancia']
        tipo = u['tipo']
        nombre = u['nombre']
        descubierto = "✓" if d['descubierta'] else "?"
        
        print(f" {descubierto} {nombre} ({tipo}) - {distancia} tiles")
    
    if len(destinos) > 10:
        print(f" ... y {len(destinos) - 10} más")


def mostrar_inventario_mapas(cartografia):
    """Muestra los mapas disponibles."""
    mapas = cartografia.get_mapas_disponibles()
    
    print("\n" + "-" * 40)
    print(" MAPAS DISPONIBLES")
    print("-" * 40)
    
    if not mapas:
        print(" No tienes mapas disponibles.")
        return
    
    for m in mapas:
        print(f" [{m.id}] {m.nombre}")
        print(f"    Tipo: {m.tipo.value} | Calidad: {m.calidad.value}")
        print(f"    Área: ({m.centro_x}, {m.centro_y}) radio {m.radio} tiles")


def menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 40)
    print(" COMANDOS")
    print("=" * 40)
    print(" [W/A/S/D] Mover (Norte/Oeste/Sur/Este)")
    print(" [E] Explorar tile actual")
    print(" [M] Mostrar mapa")
    print(" [U] Ver ubicaciones cercanas")
    print(" [I] Inventario de mapas")
    print(" [C] Crear mapa")
    print(" [V] Usar mapa")
    print(" [T] Teleportar a ubicación")
    print(" [Q] Salir")
    print()


def demo():
    """Ejecuta la demo interactiva."""
    print("\n" + "=" * 50)
    print(" DEMO DEL SISTEMA DE MAPA - LAST ADVENTURER")
    print("=" * 50)
    print("\n Generando mundo...")
    
    # Crear seed y mapa
    seed = MockSeed(seed_value=42)
    mapa = MapaMundo(seed=seed)
    cartografia = SistemaCartografia(seed)
    
    # Generar mundo inicial
    mapa.generar_mundo_inicial(
        cantidad_pueblos=(8, 12),
        cantidad_ciudades=(3, 5),
        cantidad_capitales=(1, 2),
        cantidad_mazmorras=(15, 25),
        cantidad_pois=(20, 30),
        radio_mundo=50
    )
    
    print(f" Mundo generado: {len(mapa.ubicaciones)} ubicaciones")
    print(f" Rutas creadas: {len(mapa.rutas)}")
    
    # Crear algunos mapas iniciales
    for i in range(3):
        cartografia.crear_mapa(
            tipo=TipoMapa.REGIONAL,
            calidad=CalidadMapa.NORMAL,
            centro_x=random.randint(-20, 20),
            centro_y=random.randint(-20, 20),
            radio=15
        )
    
    # Posición inicial
    mapa.mover_jugador(0, 0)
    
    # Loop principal
    while True:
        limpiar_pantalla()
        mostrar_mapa(mapa, radio=6)
        mostrar_estado(mapa, cartografia)
        menu()
        
        comando = input("\n> ").strip().upper()
        
        if comando == 'Q':
            print("\n¡Hasta pronto!")
            break
        
        elif comando == 'W':  # Norte
            x, y = mapa.posicion_jugador
            resultado = mapa.mover_jugador(x, y - 1)
            print(f"\n Movido al norte. Tiempo: {resultado['tiempo_horas']:.1f} horas")
            input("Presiona Enter...")
        
        elif comando == 'S':  # Sur
            x, y = mapa.posicion_jugador
            resultado = mapa.mover_jugador(x, y + 1)
            print(f"\n Movido al sur. Tiempo: {resultado['tiempo_horas']:.1f} horas")
            input("Presiona Enter...")
        
        elif comando == 'A':  # Oeste
            x, y = mapa.posicion_jugador
            resultado = mapa.mover_jugador(x - 1, y)
            print(f"\n Movido al oeste. Tiempo: {resultado['tiempo_horas']:.1f} horas")
            input("Presiona Enter...")
        
        elif comando == 'D':  # Este
            x, y = mapa.posicion_jugador
            resultado = mapa.mover_jugador(x + 1, y)
            print(f"\n Movido al este. Tiempo: {resultado['tiempo_horas']:.1f} horas")
            input("Presiona Enter...")
        
        elif comando == 'E':  # Explorar
            resultado = mapa.explorar_tile_actual()
            print(f"\n Tile explorado!")
            if resultado.get('ubicacion'):
                u = resultado['ubicacion']
                print(f" ¡Ubicación encontrada: {u['nombre']} ({u['tipo']})!")
            exp = cartografia.habilidad.explorar_tile()
            print(f" Experiencia ganada: {exp}")
            input("Presiona Enter...")
        
        elif comando == 'M':  # Mapa grande
            limpiar_pantalla()
            mostrar_mapa(mapa, radio=12)
            input("\nPresiona Enter...")
        
        elif comando == 'U':  # Ubicaciones
            limpiar_pantalla()
            mostrar_ubicaciones_cercanas(mapa, radio=50)
            input("\nPresiona Enter...")
        
        elif comando == 'I':  # Inventario
            limpiar_pantalla()
            mostrar_inventario_mapas(cartografia)
            input("\nPresiona Enter...")
        
        elif comando == 'C':  # Crear mapa
            print("\n Crear mapa en posición actual:")
            print(" [1] Regional (radio 20)")
            print(" [2] Local (radio 10)")
            print(" [3] Tesoro (radio 3)")
            tipo_op = input("Tipo: ").strip()
            
            tipos = {
                '1': (TipoMapa.REGIONAL, 20),
                '2': (TipoMapa.LOCAL, 10),
                '3': (TipoMapa.TESORO, 3),
            }
            
            if tipo_op in tipos:
                tipo, radio = tipos[tipo_op]
                x, y = mapa.posicion_jugador
                mapa_item = cartografia.crear_mapa(
                    tipo=tipo,
                    calidad=CalidadMapa.NORMAL,
                    centro_x=x,
                    centro_y=y,
                    radio=radio
                )
                print(f"\n Mapa creado: {mapa_item.nombre}")
            else:
                print(" Opción inválida")
            input("Presiona Enter...")
        
        elif comando == 'V':  # Usar mapa
            mapas = cartografia.get_mapas_disponibles()
            if not mapas:
                print("\n No tienes mapas disponibles.")
                input("Presiona Enter...")
                continue
            
            print("\n Mapas disponibles:")
            for m in mapas:
                print(f" [{m.id}] {m.nombre}")
            
            mapa_id = input("\nID del mapa a usar: ").strip()
            if mapa_id in [m.id for m in mapas]:
                resultado = cartografia.usar_mapa(mapa_id, mapa)
                print(f"\n Mapa usado!")
                print(f" Tiles revelados: {resultado['tiles_revelados']}")
                print(f" Ubicaciones reveladas: {len(resultado['ubicaciones_reveladas'])}")
                print(f" Experiencia ganada: {resultado['experiencia_ganada']}")
            else:
                print(" Mapa no encontrado")
            input("Presiona Enter...")
        
        elif comando == 'T':  # Teleportar
            destinos = mapa.get_destinos_cercanos(radio=100)
            print("\n Ubicaciones:")
            for i, d in enumerate(destinos[:15]):
                u = d['ubicacion']
                print(f" [{i}] {u['nombre']} ({u['tipo']}) - {d['distancia']} tiles")
            
            try:
                idx = int(input("\nNúmero de ubicación: ").strip())
                if 0 <= idx < len(destinos):
                    u = destinos[idx]['ubicacion']
                    resultado = mapa.mover_a_ubicacion(u['id'])
                    print(f"\n Viajado a: {u['nombre']}")
                    print(f" Tiempo de viaje: {resultado['tiempo_horas']:.1f} horas")
                else:
                    print(" Índice inválido")
            except ValueError:
                print(" Entrada inválida")
            input("Presiona Enter...")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n¡Hasta pronto!")