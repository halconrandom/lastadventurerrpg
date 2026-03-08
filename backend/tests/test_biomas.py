# -*- coding: utf-8 -*-
"""
Tests para el sistema de biomas.
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed
from systems.biomas import Bioma, BiomaGenerator


def test_generar_bioma_basico():
    """Se puede generar un bioma basico."""
    seed = WorldSeed("test-bioma-basico")
    gen = BiomaGenerator(seed)
    
    bioma = gen.generar_bioma((0, 0))
    
    assert bioma is not None, "Debe generar un bioma"
    assert bioma.nombre is not None, "Debe tener nombre"
    assert bioma.key in gen.BIOMAS_BASE, "Key debe ser valida"
    print(f"[OK] Bioma generado: {bioma.nombre_unico}")


def test_determinismo_biomas():
    """Misma semilla produce mismos biomas."""
    seed1 = WorldSeed("test-determinismo-biomas")
    seed2 = WorldSeed("test-determinismo-biomas")
    
    gen1 = BiomaGenerator(seed1)
    gen2 = BiomaGenerator(seed2)
    
    bioma1 = gen1.generar_bioma((5, 10))
    bioma2 = gen2.generar_bioma((5, 10))
    
    assert bioma1.key == bioma2.key, "Misma key"
    assert bioma1.nombre_unico == bioma2.nombre_unico, "Mismo nombre unico"
    assert bioma1.variacion == bioma2.variacion, "Misma variacion"
    print(f"[OK] Determinismo: {bioma1.nombre_unico} == {bioma2.nombre_unico}")


def test_biomas_diferentes_coordenadas():
    """Diferentes coordenadas pueden generar diferentes biomas."""
    seed = WorldSeed("test-coords-biomas")
    gen = BiomaGenerator(seed)
    
    # Generar varios biomas
    biomas = [gen.generar_bioma((x, y)) for x in range(3) for y in range(3)]
    
    # Verificar que hay variedad
    keys = [b.key for b in biomas]
    nombres = [b.nombre_unico for b in biomas]
    
    # Debe haber al menos algo de variedad en keys o nombres
    print(f"[OK] Generados {len(biomas)} biomas")
    print(f"    Keys unicas: {len(set(keys))}, Nombres unicos: {len(set(nombres))}")


def test_bioma_tiene_contenido():
    """Un bioma generado tiene todo el contenido necesario."""
    seed = WorldSeed("test-contenido-bioma")
    gen = BiomaGenerator(seed)
    
    bioma = gen.generar_bioma((0, 0))
    
    assert len(bioma.terreno) > 0, "Debe tener terreno"
    assert len(bioma.clima) > 0, "Debe tener clima"
    assert len(bioma.recursos) > 0, "Debe tener recursos"
    assert len(bioma.fauna) > 0, "Debe tener fauna"
    assert len(bioma.peligros) > 0, "Debe tener peligros"
    assert len(bioma.eventos) > 0, "Debe tener eventos"
    
    print(f"[OK] Bioma tiene contenido completo")
    print(f"    Terreno: {bioma.terreno}")
    print(f"    Clima: {bioma.clima}")
    print(f"    Recursos: {bioma.recursos}")


def test_variaciones_bioma():
    """Los biomas pueden tener variaciones."""
    seed = WorldSeed("test-variaciones")
    gen = BiomaGenerator(seed)
    
    # Generar muchos biomas para encontrar variaciones
    biomas = [gen.generar_bioma((x, 0)) for x in range(20)]
    
    variaciones_encontradas = set()
    for b in biomas:
        variaciones_encontradas.add(b.variacion["tipo"])
    
    assert len(variaciones_encontradas) > 1, "Debe haber variedad de variaciones"
    print(f"[OK] Variaciones encontradas: {variaciones_encontradas}")


def test_nombre_unico():
    """Cada bioma tiene nombre unico."""
    seed = WorldSeed("test-nombres")
    gen = BiomaGenerator(seed)
    
    bioma = gen.generar_bioma((0, 0))
    
    assert bioma.nombre_unico is not None, "Debe tener nombre unico"
    assert len(bioma.nombre_unico) > 0, "Nombre no puede estar vacio"
    print(f"[OK] Nombre unico: {bioma.nombre_unico}")


def test_descripcion_bioma():
    """Se puede generar descripcion del bioma."""
    seed = WorldSeed("test-descripcion")
    gen = BiomaGenerator(seed)
    
    bioma = gen.generar_bioma((0, 0))
    descripcion = bioma.get_descripcion()
    
    assert descripcion is not None, "Debe tener descripcion"
    assert len(descripcion) > 0, "Descripcion no puede estar vacia"
    print(f"[OK] Descripcion: {descripcion}")


def test_serializacion_bioma():
    """Un bioma se puede serializar y deserializar."""
    seed = WorldSeed("test-serializacion-bioma")
    gen = BiomaGenerator(seed)
    
    bioma_original = gen.generar_bioma((7, 14))
    
    # Serializar
    data = bioma_original.to_dict()
    
    # Deserializar
    bioma_restaurado = Bioma.from_dict(data)
    
    assert bioma_original.key == bioma_restaurado.key
    assert bioma_original.nombre_unico == bioma_restaurado.nombre_unico
    assert bioma_original.variacion == bioma_restaurado.variacion
    assert bioma_original.coordenadas == bioma_restaurado.coordenadas
    
    print(f"[OK] Serializacion correcta para {bioma_original.nombre_unico}")


def test_coordenadas_bioma():
    """El bioma recuerda sus coordenadas."""
    seed = WorldSeed("test-coords")
    gen = BiomaGenerator(seed)
    
    coords = (15, 27)
    bioma = gen.generar_bioma(coords)
    
    assert bioma.coordenadas == coords, "Debe recordar coordenadas"
    print(f"[OK] Coordenadas correctas: {bioma.coordenadas}")


def test_todos_biomas_disponibles():
    """Todos los biomas base estan disponibles."""
    seed = WorldSeed("test-todos-biomas")
    gen = BiomaGenerator(seed)
    
    biomas_disponibles = gen.get_todos_biomas()
    
    assert len(biomas_disponibles) == 6, "Debe haber 6 biomas base"
    assert "bosque_ancestral" in biomas_disponibles
    assert "paramo_marchito" in biomas_disponibles
    assert "pantano_sombrio" in biomas_disponibles
    assert "montanas_heladas" in biomas_disponibles
    assert "desierto_ceniza" in biomas_disponibles
    assert "ruinas_subterraneas" in biomas_disponibles
    
    print(f"[OK] Todos los biomas disponibles: {biomas_disponibles}")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Biomas")
    print("="*50 + "\n")
    
    tests = [
        test_generar_bioma_basico,
        test_determinismo_biomas,
        test_biomas_diferentes_coordenadas,
        test_bioma_tiene_contenido,
        test_variaciones_bioma,
        test_nombre_unico,
        test_descripcion_bioma,
        test_serializacion_bioma,
        test_coordenadas_bioma,
        test_todos_biomas_disponibles,
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
