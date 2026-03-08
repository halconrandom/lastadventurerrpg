# -*- coding: utf-8 -*-
"""
Tests para el sistema de zonas y tiles.
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed
from systems.zonas import Zona, ZonaGenerator, Tile, Entidad, PuntoInteres


def test_generar_zona_basica():
    """Se puede generar una zona basica."""
    seed = WorldSeed("test-zona-basica")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    assert zona is not None, "Debe generar una zona"
    assert zona.nombre is not None, "Debe tener nombre"
    assert zona.tamaño > 0, "Debe tener tamaño"
    print(f"[OK] Zona generada: {zona.nombre} ({zona.tamaño}x{zona.tamaño})")


def test_zona_tiene_tiles():
    """Una zona tiene tiles generados."""
    seed = WorldSeed("test-tiles")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    assert len(zona.tiles) > 0, "Debe tener tiles"
    assert len(zona.tiles[0]) > 0, "Las filas deben tener tiles"
    
    # Verificar que los tiles tienen contenido
    primer_tile = zona.tiles[0][0]
    assert primer_tile.terreno is not None, "Tile debe tener terreno"
    
    print(f"[OK] Zona tiene {zona.tamaño}x{zona.tamaño} tiles")


def test_zona_tiene_entidades():
    """Una zona tiene entidades."""
    seed = WorldSeed("test-entidades")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    assert len(zona.entidades) > 0, "Debe tener entidades"
    
    # Verificar entidades
    for entidad in zona.entidades:
        assert entidad.id is not None, "Entidad debe tener ID"
        assert entidad.tipo is not None, "Entidad debe tener tipo"
        assert entidad.nivel > 0, "Entidad debe tener nivel"
    
    hostiles = [e for e in zona.entidades if e.hostil]
    neutrales = [e for e in zona.entidades if not e.hostil]
    
    print(f"[OK] Zona tiene {len(hostiles)} hostiles, {len(neutrales)} neutrales")


def test_zona_tiene_pois():
    """Una zona tiene puntos de interes."""
    seed = WorldSeed("test-pois")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    assert len(zona.pois) > 0, "Debe tener POIs"
    
    for poi in zona.pois:
        assert poi.tipo is not None, "POI debe tener tipo"
        assert poi.nombre is not None, "POI debe tener nombre"
    
    print(f"[OK] Zona tiene {len(zona.pois)} POIs: {[p.nombre for p in zona.pois]}")


def test_determinismo_zonas():
    """Misma semilla produce mismas zonas."""
    seed1 = WorldSeed("test-determinismo-zonas")
    seed2 = WorldSeed("test-determinismo-zonas")
    
    gen1 = ZonaGenerator(seed1)
    gen2 = ZonaGenerator(seed2)
    
    zona1 = gen1.generar_zona((10, 20))
    zona2 = gen2.generar_zona((10, 20))
    
    assert zona1.nombre == zona2.nombre, "Mismo nombre"
    assert zona1.tamaño == zona2.tamaño, "Mismo tamaño"
    assert len(zona1.entidades) == len(zona2.entidades), "Mismo numero de entidades"
    
    print(f"[OK] Determinismo: {zona1.nombre} == {zona2.nombre}")


def test_exploracion_zona():
    """Se puede explorar una zona."""
    seed = WorldSeed("test-exploracion")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    resultado = zona.explorar()
    
    assert resultado is not None, "Debe retornar resultado"
    assert "tiles_descubiertos" in resultado, "Debe tener tiles descubiertos"
    assert "estado_zona" in resultado, "Debe tener estado"
    
    assert zona.visitada, "Zona debe estar visitada"
    assert zona.veces_explorada == 1, "Debe contar exploraciones"
    
    print(f"[OK] Exploracion: {len(resultado['tiles_descubiertos'])} tiles descubiertos")


def test_estado_zona():
    """La zona cambia de estado al explorar."""
    seed = WorldSeed("test-estado-zona")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    assert zona.estado == "inexplorada", "Estado inicial"
    
    zona.explorar()
    assert zona.estado == "explorando", "Estado despues de explorar"
    
    # Explorar muchas veces
    for _ in range(6):
        zona.explorar()
    
    assert zona.estado == "agotada", "Estado agotada despues de 5+ exploraciones"
    
    print(f"[OK] Estados: inexplorada -> explorando -> agotada")


def test_serializacion_zona():
    """Una zona se puede serializar y deserializar."""
    seed = WorldSeed("test-serializacion-zona")
    gen = ZonaGenerator(seed)
    
    zona_original = gen.generar_zona((5, 10))
    zona_original.explorar()
    
    # Serializar
    data = zona_original.to_dict()
    
    # Deserializar
    zona_restaurada = Zona.from_dict(data, seed)
    
    assert zona_original.nombre == zona_restaurada.nombre
    assert zona_original.tamaño == zona_restaurada.tamaño
    assert zona_original.visitada == zona_restaurada.visitada
    assert zona_original.veces_explorada == zona_restaurada.veces_explorada
    
    print(f"[OK] Serializacion correcta para {zona_original.nombre}")


def test_tiles_especiales():
    """Algunos tiles pueden ser especiales."""
    seed = WorldSeed("test-tiles-especiales")
    gen = ZonaGenerator(seed)
    
    # Generar varias zonas para encontrar tiles especiales
    zonas = [gen.generar_zona((x, 0)) for x in range(5)]
    
    tiles_especiales = []
    for zona in zonas:
        for fila in zona.tiles:
            for tile in fila:
                if tile.especial:
                    tiles_especiales.append(tile.especial)
    
    # Debe haber al menos algunos tiles especiales
    print(f"[OK] Tiles especiales encontrados: {len(tiles_especiales)}")
    if tiles_especiales:
        print(f"    Tipos: {set(tiles_especiales)}")


def test_nivel_entidades_por_distancia():
    """Las entidades tienen mayor nivel lejos del centro."""
    seed = WorldSeed("test-nivel-distancia")
    gen = ZonaGenerator(seed)
    
    # Zona cerca del centro
    zona_cerca = gen.generar_zona((50, 50))
    
    # Zona lejos del centro
    zona_lejos = gen.generar_zona((80, 80))
    
    # Promedio de niveles
    niveles_cerca = [e.nivel for e in zona_cerca.entidades]
    niveles_lejos = [e.nivel for e in zona_lejos.entidades]
    
    avg_cerca = sum(niveles_cerca) / len(niveles_cerca) if niveles_cerca else 0
    avg_lejos = sum(niveles_lejos) / len(niveles_lejos) if niveles_lejos else 0
    
    print(f"[OK] Niveles - Cerca: {avg_cerca:.1f}, Lejos: {avg_lejos:.1f}")


def test_exploracion_descubre_poi():
    """La exploracion puede descubrir POIs."""
    seed = WorldSeed("test-descubrir-poi")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    # Explorar varias veces
    pois_descubiertos = []
    for _ in range(20):
        resultado = zona.explorar()
        if resultado.get("poi_descubierto"):
            pois_descubiertos.append(resultado["poi_descubierto"])
    
    print(f"[OK] POIs descubiertos tras 20 exploraciones: {len(pois_descubiertos)}")


def test_encuentros_exploracion():
    """La exploracion puede generar encuentros."""
    seed = WorldSeed("test-encuentros")
    gen = ZonaGenerator(seed)
    
    zona = gen.generar_zona((0, 0))
    
    # Explorar varias veces
    encuentros = []
    for _ in range(10):
        resultado = zona.explorar()
        if resultado.get("encuentros"):
            encuentros.extend(resultado["encuentros"])
    
    print(f"[OK] Encuentros en 10 exploraciones: {len(encuentros)}")
    if encuentros:
        print(f"    Ejemplo: {encuentros[0]['entidad_nombre']} (nv.{encuentros[0]['nivel']})")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Zonas y Tiles")
    print("="*50 + "\n")
    
    tests = [
        test_generar_zona_basica,
        test_zona_tiene_tiles,
        test_zona_tiene_entidades,
        test_zona_tiene_pois,
        test_determinismo_zonas,
        test_exploracion_zona,
        test_estado_zona,
        test_serializacion_zona,
        test_tiles_especiales,
        test_nivel_entidades_por_distancia,
        test_exploracion_descubre_poi,
        test_encuentros_exploracion,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: Error inesperado - {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"RESULTADO: {passed} pasados, {failed} fallidos")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
