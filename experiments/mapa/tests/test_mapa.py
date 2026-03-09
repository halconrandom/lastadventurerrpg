"""
Tests para el Sistema de Mapa.

Valida:
- Generación de tiles y chunks
- Sistema de ubicaciones
- Rutas y pathfinding
- Cartografía y progresión
"""

import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tile import Tile, SubTile, EstadoVisibilidad, TipoTerreno, calcular_costo_movimiento
from chunk import Chunk, GestorChunks
from ubicacion import Ubicacion, UbicacionGenerator, TipoUbicacion
from ruta import Ruta, RutaGenerator, TipoRuta
from mapa import MapaMundo
from cartografia import (
    HabilidadCartografia, MapaItem, SistemaCartografia,
    CalidadMapa, TipoMapa, NIVELES_CARTOGRAFIA
)


# Mock de WorldSeed para tests
class MockSeed:
    """Mock de WorldSeed para tests."""
    
    def __init__(self, seed_value=12345):
        self.seed_value = seed_value
        self.rng_states = {}
    
    def get_rng(self, contexto: str):
        """Retorna un RNG determinista para el contexto."""
        import random
        if contexto not in self.rng_states:
            # Crear RNG con seed basada en el contexto
            seed = hash(f"{self.seed_value}_{contexto}") % (2**32)
            self.rng_states[contexto] = random.Random(seed)
        return self.rng_states[contexto]


def test_tile_creation():
    """Test de creación de tiles."""
    print("\n=== Test: Creación de Tiles ===")
    
    # Crear tile básico
    tile = Tile(x=10, y=20, bioma="bosque_ancestral")
    assert tile.x == 10
    assert tile.y == 20
    assert tile.bioma == "bosque_ancestral"
    assert tile.visibilidad == EstadoVisibilidad.NO_DESCUBIERTO
    print(f"✓ Tile creado: {tile}")
    
    # Test de descubrimiento
    tile.descubrir()
    assert tile.visibilidad == EstadoVisibilidad.DESCUBIERTO
    print(f"✓ Tile descubierto: {tile.visibilidad.value}")
    
    # Test de exploración
    tile.explorar()
    assert tile.visibilidad == EstadoVisibilidad.EXPLORADO
    print(f"✓ Tile explorado: {tile.visibilidad.value}")
    
    # Test de sub-tiles
    tile.generar_sub_tiles("pueblo")
    assert len(tile.sub_tiles) == 5  # Pueblo: 5x5
    assert len(tile.sub_tiles[0]) == 5
    print(f"✓ Sub-tiles generados: {len(tile.sub_tiles)}x{len(tile.sub_tiles[0])}")
    
    # Test de serialización
    data = tile.to_dict()
    tile2 = Tile.from_dict(data)
    assert tile2.x == tile.x
    assert tile2.y == tile.y
    print("✓ Serialización correcta")
    
    return True


def test_chunk_management():
    """Test de gestión de chunks."""
    print("\n=== Test: Gestión de Chunks ===")
    
    gestor = GestorChunks()
    
    # Test de conversión de coordenadas positivas
    chunk_coords = GestorChunks.tile_a_chunk(5, 7)
    assert chunk_coords == (1, 2), f"Expected (1, 2), got {chunk_coords}"  # Tile (5,7) está en chunk (1,2)
    print(f"✓ Tile (5,7) -> Chunk {chunk_coords}")
    
    # Test de conversión de coordenadas negativas
    # Tile -3 está en chunk -1 (chunks: -1 tiene tiles -3,-2,-1)
    chunk_coords = GestorChunks.tile_a_chunk(-3, -2)
    assert chunk_coords == (-1, -1), f"Expected (-1, -1), got {chunk_coords}"
    print(f"✓ Tile (-3,-2) -> Chunk {chunk_coords}")
    
    # Test de coordenadas en el límite
    chunk_coords = GestorChunks.tile_a_chunk(0, 0)
    assert chunk_coords == (0, 0), f"Expected (0, 0), got {chunk_coords}"
    print(f"✓ Tile (0,0) -> Chunk {chunk_coords}")
    
    # Test de coordenadas locales
    local = GestorChunks.tile_a_local(5, 7)
    assert local == (2, 1), f"Expected (2, 1), got {local}"  # Posición local dentro del chunk
    print(f"✓ Tile (5,7) -> Local {local}")
    
    # Test de creación de chunk
    chunk = Chunk(x=0, y=0)
    assert chunk.x == 0
    assert chunk.y == 0
    print(f"✓ Chunk creado: {chunk}")
    
    # Test de tiles en chunk
    tile = Tile(x=1, y=1, bioma="pradera")
    gestor.set_tile(tile)
    retrieved = gestor.get_tile(1, 1)
    assert retrieved is not None
    assert retrieved.x == 1
    print(f"✓ Tile guardado y recuperado: {retrieved}")
    
    # Test de actualización de posición
    chunks_a_cargar = gestor.actualizar_posicion_jugador(0, 0)
    print(f"✓ Posición actualizada, chunks a cargar: {len(chunks_a_cargar)}")
    
    return True


def test_ubicaciones():
    """Test de sistema de ubicaciones."""
    print("\n=== Test: Sistema de Ubicaciones ===")
    
    seed = MockSeed()
    gen = UbicacionGenerator(seed)
    
    # Test de generación de ubicación
    ubicacion = gen.generar_ubicacion(
        id="pueblo_0",
        tipo=TipoUbicacion.PUEBLO,
        x=10,
        y=20,
        bioma="bosque_ancestral"
    )
    
    assert ubicacion.id == "pueblo_0"
    assert ubicacion.tipo == TipoUbicacion.PUEBLO
    assert ubicacion.x == 10
    assert ubicacion.y == 20
    print(f"✓ Ubicación generada: {ubicacion}")
    
    # Test de tiempo de exploración
    tiempo = ubicacion.get_tiempo_exploracion()
    assert tiempo > 0
    print(f"✓ Tiempo de exploración: {tiempo} minutos")
    
    # Test de serialización
    data = ubicacion.to_dict()
    ubicacion2 = Ubicacion.from_dict(data)
    assert ubicacion2.id == ubicacion.id
    assert ubicacion2.nombre == ubicacion.nombre
    print("✓ Serialización correcta")
    
    # Test de generación de múltiples ubicaciones
    ubicaciones = gen.generar_ubicaciones_iniciales(
        cantidad_pueblos=(5, 5),
        cantidad_ciudades=(2, 2),
        cantidad_capitales=(1, 1),
        cantidad_mazmorras=(10, 10),
        cantidad_pois=(20, 20),
        radio_mundo=50
    )
    
    tipos = {}
    for u in ubicaciones:
        tipos[u.tipo] = tipos.get(u.tipo, 0) + 1
    
    print(f"✓ Ubicaciones generadas: {len(ubicaciones)}")
    for tipo, count in tipos.items():
        print(f"  - {tipo.value}: {count}")
    
    return True


def test_rutas():
    """Test de sistema de rutas."""
    print("\n=== Test: Sistema de Rutas ===")
    
    seed = MockSeed()
    gen = RutaGenerator(seed)
    
    # Test de cálculo de ruta
    origen = (0, 0)
    destino = (5, 5)
    camino = gen.calcular_ruta(origen, destino, None)
    
    assert len(camino) > 0
    assert camino[0] == origen
    assert camino[-1] == destino
    print(f"✓ Camino calculado: {len(camino)} tiles")
    
    # Test de generación de ruta
    ruta = gen.generar_ruta(
        id="ruta_test",
        origen_id="pueblo_0",
        destino_id="pueblo_1",
        origen_coords=(0, 0),
        destino_coords=(10, 10),
        mapa_tiles=None
    )
    
    assert ruta.id == "ruta_test"
    assert ruta.origen == "pueblo_0"
    assert ruta.destino == "pueblo_1"
    print(f"✓ Ruta generada: {ruta}")
    
    # Test de tiempo de viaje
    tiempo = ruta.calcular_tiempo()
    assert tiempo > 0
    print(f"✓ Tiempo de viaje: {tiempo} horas")
    
    # Test de descripción
    desc = ruta.get_descripcion()
    assert len(desc) > 0
    print(f"✓ Descripción: {desc}")
    
    # Test de serialización
    data = ruta.to_dict()
    ruta2 = Ruta.from_dict(data)
    assert ruta2.id == ruta.id
    print("✓ Serialización correcta")
    
    return True


def test_mapa_mundo():
    """Test de mapa mundial."""
    print("\n=== Test: Mapa Mundial ===")
    
    seed = MockSeed()
    mapa = MapaMundo(seed=seed)
    
    # Test de generación inicial
    mapa.generar_mundo_inicial(
        cantidad_pueblos=(5, 5),
        cantidad_ciudades=(2, 2),
        cantidad_capitales=(1, 1),
        cantidad_mazmorras=(10, 10),
        cantidad_pois=(20, 20),
        radio_mundo=50
    )
    
    assert len(mapa.ubicaciones) > 0
    assert len(mapa.rutas) > 0
    print(f"✓ Mundo generado: {len(mapa.ubicaciones)} ubicaciones, {len(mapa.rutas)} rutas")
    
    # Test de movimiento
    resultado = mapa.mover_jugador(5, 5)
    assert resultado["posicion_nueva"] == (5, 5)
    print(f"✓ Jugador movido a: {resultado['posicion_nueva']}")
    
    # Test de exploración
    resultado = mapa.explorar_tile_actual()
    assert "tile" in resultado
    print(f"✓ Tile explorado")
    
    # Test de destinos cercanos
    destinos = mapa.get_destinos_cercanos(radio=100)
    print(f"✓ Destinos cercanos: {len(destinos)}")
    
    # Test de estado del mapa
    estado = mapa.get_estado_mapa()
    print(f"✓ Estado del mapa: {estado}")
    
    # Test de visualización
    visual = mapa.get_mapa_visual(radio=5)
    print(f"✓ Mapa visual: {len(visual)}x{len(visual[0])}")
    for fila in visual[:3]:
        print(f"  {' '.join(fila)}")
    
    # Test de serialización
    data = mapa.to_dict()
    mapa2 = MapaMundo.from_dict(data, seed)
    assert len(mapa2.ubicaciones) == len(mapa.ubicaciones)
    print("✓ Serialización correcta")
    
    return True


def test_cartografia():
    """Test de sistema de cartografía."""
    print("\n=== Test: Sistema de Cartografía ===")
    
    seed = MockSeed()
    sistema = SistemaCartografia(seed)
    
    # Test de habilidad inicial
    assert sistema.habilidad.nivel == 1
    print(f"✓ Nivel inicial: {sistema.habilidad.get_nombre_nivel()}")
    
    # Test de experiencia
    subio = sistema.habilidad.add_experiencia(50)
    print(f"✓ Experiencia añadida, subió de nivel: {subio}")
    
    # Test de exploración
    exp = sistema.habilidad.explorar_tile()
    assert exp > 0
    print(f"✓ Experiencia por tile: {exp}")
    
    # Test de descubrimiento
    exp = sistema.habilidad.descubrir_ubicacion()
    assert exp > 0
    print(f"✓ Experiencia por ubicación: {exp}")
    
    # Test de creación de mapa
    mapa = sistema.crear_mapa(
        tipo=TipoMapa.REGIONAL,
        calidad=CalidadMapa.NORMAL,
        centro_x=0,
        centro_y=0,
        radio=20
    )
    
    assert mapa.id is not None
    assert mapa.tipo == TipoMapa.REGIONAL
    print(f"✓ Mapa creado: {mapa.nombre}")
    
    # Test de área del mapa
    area = mapa.get_area()
    assert area == (-20, -20, 20, 20)
    print(f"✓ Área del mapa: {area}")
    
    # Test de estadísticas
    stats = sistema.get_estadisticas()
    print(f"✓ Estadísticas: {stats}")
    
    # Test de serialización
    data = sistema.to_dict()
    sistema2 = SistemaCartografia.from_dict(data, seed)
    assert sistema2.habilidad.nivel == sistema.habilidad.nivel
    print("✓ Serialización correcta")
    
    return True


def test_integracion():
    """Test de integración completa."""
    print("\n=== Test: Integración Completa ===")
    
    seed = MockSeed()
    
    # Crear mapa mundial
    mapa = MapaMundo(seed=seed)
    mapa.generar_mundo_inicial(
        cantidad_pueblos=(10, 10),
        cantidad_ciudades=(3, 3),
        cantidad_capitales=(1, 1),
        cantidad_mazmorras=(15, 15),
        cantidad_pois=(30, 30),
        radio_mundo=100
    )
    
    # Crear sistema de cartografía
    cartografia = SistemaCartografia(seed)
    
    # Crear mapa item
    mapa_item = cartografia.crear_mapa(
        tipo=TipoMapa.REGIONAL,
        calidad=CalidadMapa.DETALLADO,
        centro_x=0,
        centro_y=0,
        radio=30
    )
    
    # Usar mapa
    resultado = cartografia.usar_mapa(mapa_item.id, mapa)
    print(f"✓ Mapa usado: {resultado['tiles_revelados']} tiles revelados")
    
    # Mover jugador
    mapa.mover_jugador(10, 10)
    mapa.explorar_tile_actual()
    cartografia.habilidad.explorar_tile()
    
    # Verificar estado
    estado = mapa.get_estado_mapa()
    stats = cartografia.get_estadisticas()
    
    print(f"✓ Estado final:")
    print(f"  - Posición: {estado['posicion_jugador']}")
    print(f"  - Tiles explorados: {estado['tiles_explorados']}")
    print(f"  - Ubicaciones descubiertas: {estado['ubicaciones_descubiertas']}")
    print(f"  - Nivel cartografía: {stats['nombre_nivel']}")
    
    return True


def run_tests():
    """Ejecuta todos los tests."""
    print("=" * 50)
    print("INICIANDO TESTS DEL SISTEMA DE MAPA")
    print("=" * 50)
    
    tests = [
        ("Tiles", test_tile_creation),
        ("Chunks", test_chunk_management),
        ("Ubicaciones", test_ubicaciones),
        ("Rutas", test_rutas),
        ("Mapa Mundial", test_mapa_mundo),
        ("Cartografía", test_cartografia),
        ("Integración", test_integracion),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado, None))
            print(f"\n✅ Test '{nombre}' PASADO")
        except Exception as e:
            resultados.append((nombre, False, str(e)))
            print(f"\n❌ Test '{nombre}' FALLIDO: {e}")
    
    print("\n" + "=" * 50)
    print("RESUMEN DE TESTS")
    print("=" * 50)
    
    pasados = sum(1 for _, r, _ in resultados if r)
    total = len(resultados)
    
    for nombre, resultado, error in resultados:
        estado = "✅ PASADO" if resultado else "❌ FALLIDO"
        print(f"{estado}: {nombre}")
        if error:
            print(f"   Error: {error}")
    
    print(f"\nTotal: {pasados}/{total} tests pasados")
    
    return pasados == total


if __name__ == "__main__":
    exito = run_tests()
    sys.exit(0 if exito else 1)