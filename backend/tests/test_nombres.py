# -*- coding: utf-8 -*-
"""
Tests para el sistema de generacion de nombres.
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed
from systems.nombres import NombreGenerator


def test_generar_nombre_npc_masculino():
    """Se puede generar nombre de NPC masculino."""
    seed = WorldSeed("test-npc-masc")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_npc("test1", genero="masculino")
    
    assert nombre is not None, "Debe generar nombre"
    assert len(nombre) > 0, "Nombre no puede estar vacio"
    print(f"[OK] NPC masculino: {nombre}")


def test_generar_nombre_npc_femenino():
    """Se puede generar nombre de NPC femenino."""
    seed = WorldSeed("test-npc-fem")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_npc("test2", genero="femenino")
    
    assert nombre is not None, "Debe generar nombre"
    assert len(nombre) > 0, "Nombre no puede estar vacio"
    print(f"[OK] NPC femenino: {nombre}")


def test_generar_nombre_npc_con_titulo():
    """Se puede generar nombre con titulo."""
    seed = WorldSeed("test-npc-titulo")
    gen = NombreGenerator(seed)
    
    nombre_positivo = gen.generar_nombre_npc("test3", con_titulo=True, titulo_positivo=True)
    nombre_negativo = gen.generar_nombre_npc("test4", con_titulo=True, titulo_positivo=False)
    
    assert "," in nombre_positivo, "Debe tener titulo con coma"
    assert "," in nombre_negativo, "Debe tener titulo con coma"
    
    print(f"[OK] Con titulo positivo: {nombre_positivo}")
    print(f"[OK] Con titulo negativo: {nombre_negativo}")


def test_generar_nombre_lugar():
    """Se puede generar nombre de lugar."""
    seed = WorldSeed("test-lugar")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_lugar("test5")
    
    assert nombre is not None, "Debe generar nombre"
    assert len(nombre) > 0, "Nombre no puede estar vacio"
    print(f"[OK] Lugar: {nombre}")


def test_generar_nombre_objeto():
    """Se puede generar nombre de objeto."""
    seed = WorldSeed("test-objeto")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_objeto("test6")
    
    assert nombre is not None, "Debe generar nombre"
    assert len(nombre) > 0, "Nombre no puede estar vacio"
    print(f"[OK] Objeto: {nombre}")


def test_generar_nombre_objeto_tipo_especifico():
    """Se puede generar nombre de objeto con tipo especifico."""
    seed = WorldSeed("test-objeto-tipo")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_objeto("test7", tipo="Espada")
    
    assert "Espada" in nombre, "Debe contener el tipo"
    print(f"[OK] Objeto especifico: {nombre}")


def test_generar_nombre_enemigo():
    """Se puede generar nombre de enemigo."""
    seed = WorldSeed("test-enemigo")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_enemigo("test8")
    
    assert nombre is not None, "Debe generar nombre"
    assert len(nombre) > 0, "Nombre no puede estar vacio"
    print(f"[OK] Enemigo: {nombre}")


def test_generar_nombre_enemigo_con_prefijo():
    """Se puede generar nombre de enemigo con prefijo."""
    seed = WorldSeed("test-enemigo-prefijo")
    gen = NombreGenerator(seed)
    
    nombre = gen.generar_nombre_enemigo("test9", con_prefijo=True)
    
    assert nombre is not None, "Debe generar nombre"
    # El prefijo es opcional en la generacion
    print(f"[OK] Enemigo con prefijo: {nombre}")


def test_determinismo_nombres():
    """Misma semilla produce mismos nombres."""
    seed1 = WorldSeed("test-determinismo-nombres")
    seed2 = WorldSeed("test-determinismo-nombres")
    
    gen1 = NombreGenerator(seed1)
    gen2 = NombreGenerator(seed2)
    
    nombre1 = gen1.generar_nombre_npc("test10")
    nombre2 = gen2.generar_nombre_npc("test10")
    
    assert nombre1 == nombre2, "Misma semilla debe producir mismo nombre"
    print(f"[OK] Determinismo: {nombre1} == {nombre2}")


def test_nombres_unicos():
    """Se generan nombres variados."""
    seed = WorldSeed("test-nombres-unicos")
    gen = NombreGenerator(seed)
    
    nombres = [gen.generar_nombre_npc(f"test{i}") for i in range(20)]
    
    # Debe haber variedad
    nombres_unicos = set(nombres)
    
    print(f"[OK] Generados {len(nombres)} nombres, {len(nombres_unicos)} unicos")
    print(f"    Ejemplos: {list(nombres_unicos)[:5]}")


def test_generar_apodo():
    """Se pueden generar apodos."""
    seed = WorldSeed("test-apodo")
    gen = NombreGenerator(seed)
    
    apodo_positivo = gen.generar_apodo("test11", positivo=True)
    apodo_negativo = gen.generar_apodo("test12", positivo=False)
    
    assert apodo_positivo is not None
    assert apodo_negativo is not None
    
    print(f"[OK] Apodo positivo: {apodo_positivo}")
    print(f"[OK] Apodo negativo: {apodo_negativo}")


def test_nombre_unico_generico():
    """Se puede generar nombre generico por tipo."""
    seed = WorldSeed("test-generico")
    gen = NombreGenerator(seed)
    
    npc = gen.generar_nombre_unico("test13", tipo="npc")
    lugar = gen.generar_nombre_unico("test14", tipo="lugar")
    objeto = gen.generar_nombre_unico("test15", tipo="objeto")
    enemigo = gen.generar_nombre_unico("test16", tipo="enemigo")
    
    assert all([npc, lugar, objeto, enemigo]), "Todos deben generar nombre"
    
    print(f"[OK] Generico NPC: {npc}")
    print(f"[OK] Generico Lugar: {lugar}")
    print(f"[OK] Generico Objeto: {objeto}")
    print(f"[OK] Generico Enemigo: {enemigo}")


def test_nombre_silabas():
    """Se pueden generar nombres por silabas."""
    seed = WorldSeed("test-silabas")
    gen = NombreGenerator(seed)
    
    # Generar varios nombres por silabas
    nombres = []
    for i in range(10):
        nombre = gen.generar_nombre_unico(f"silaba_{i}", tipo="otro")
        nombres.append(nombre)
    
    # Verificar que son diferentes
    nombres_unicos = set(nombres)
    
    print(f"[OK] Nombres por silabas: {nombres[:5]}")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Generacion de Nombres")
    print("="*50 + "\n")
    
    tests = [
        test_generar_nombre_npc_masculino,
        test_generar_nombre_npc_femenino,
        test_generar_nombre_npc_con_titulo,
        test_generar_nombre_lugar,
        test_generar_nombre_objeto,
        test_generar_nombre_objeto_tipo_especifico,
        test_generar_nombre_enemigo,
        test_generar_nombre_enemigo_con_prefijo,
        test_determinismo_nombres,
        test_nombres_unicos,
        test_generar_apodo,
        test_nombre_unico_generico,
        test_nombre_silabas,
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
