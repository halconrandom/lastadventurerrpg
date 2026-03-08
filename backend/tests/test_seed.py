# -*- coding: utf-8 -*-
"""
Tests para el sistema de semillas (WorldSeed).
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed, init_global_seed, get_global_seed, set_global_seed


def test_semilla_aleatoria():
    """Las semillas aleatorias deben ser unicas."""
    seed1 = WorldSeed()
    seed2 = WorldSeed()
    
    assert seed1.master_seed != seed2.master_seed, "Las semillas aleatorias deben ser diferentes"
    print("[OK] Semillas aleatorias son unicas")


def test_semilla_desde_string():
    """Se puede crear semilla desde string."""
    seed = WorldSeed("mi-partida-123")
    
    assert seed.master_seed == "mi-partida-123", "La semilla debe mantener el string original"
    print("[OK] Semilla desde string funciona")


def test_determinismo():
    """Misma semilla debe producir mismos resultados."""
    seed1 = WorldSeed("test-determinismo")
    seed2 = WorldSeed("test-determinismo")
    
    # Obtener RNG para mismo contexto
    rng1 = seed1.get_rng("test")
    rng2 = seed2.get_rng("test")
    
    # Deben producir misma secuencia
    resultados1 = [rng1.randint(0, 100) for _ in range(10)]
    resultados2 = [rng2.randint(0, 100) for _ in range(10)]
    
    assert resultados1 == resultados2, "Misma semilla debe producir mismos resultados"
    print(f"[OK] Determinismo verificado: {resultados1}")


def test_contextos_independientes():
    """Contextos diferentes no deben afectarse entre si."""
    seed = WorldSeed("test-independencia")
    
    rng_biomas = seed.get_rng("biomas")
    rng_enemigos = seed.get_rng("enemigos")
    
    # Avanzar rng_biomas no debe afectar rng_enemigos
    _ = [rng_biomas.random() for _ in range(100)]
    
    # rng_enemigos debe empezar desde su posicion inicial
    seed_nueva = WorldSeed("test-independencia")
    rng_enemigos_nuevo = seed_nueva.get_rng("enemigos")
    
    assert rng_enemigos.random() == rng_enemigos_nuevo.random(), "Contextos deben ser independientes"
    print("[OK] Contextos son independientes")


def test_subseed_unicas():
    """Cada contexto debe tener sub-seed unica."""
    seed = WorldSeed("test-subseeds")
    
    subseed1 = seed.get_subseed("biomas")
    subseed2 = seed.get_subseed("enemigos")
    subseed3 = seed.get_subseed("tesoros")
    
    assert subseed1 != subseed2 != subseed3, "Cada contexto debe tener sub-seed unica"
    print(f"[OK] Sub-seeds unicas: biomas={subseed1}, enemigos={subseed2}, tesoros={subseed3}")


def test_helpers():
    """Los helpers deben funcionar correctamente."""
    seed = WorldSeed("test-helpers")
    
    # get_int
    entero = seed.get_int("test", 0, 10)
    assert 0 <= entero <= 10, "get_int debe estar en rango"
    
    # get_choice
    lista = ["a", "b", "c"]
    eleccion = seed.get_choice("test", lista)
    assert eleccion in lista, "get_choice debe estar en la lista"
    
    # get_float
    flotante = seed.get_float("test")
    assert 0 <= flotante <= 1, "get_float debe estar entre 0 y 1"
    
    print("[OK] Helpers funcionan correctamente")


def test_serializacion():
    """La serializacion debe preservar la semilla."""
    seed_original = WorldSeed("test-serializacion")
    
    # Generar algunos valores para poblar caches
    seed_original.get_rng("biomas").random()
    seed_original.get_rng("enemigos").random()
    
    # Serializar
    data = seed_original.to_dict()
    
    # Deserializar
    seed_restaurada = WorldSeed.from_dict(data)
    
    # Deben producir mismos resultados
    assert seed_original.master_seed == seed_restaurada.master_seed, "Master seed debe preservarse"
    
    # Los RNG deben seguir siendo deterministas
    rng1 = seed_original.get_rng("test_nuevo")
    rng2 = seed_restaurada.get_rng("test_nuevo")
    
    assert rng1.random() == rng2.random(), "RNG debe seguir siendo determinista despues de serializar"
    print("[OK] Serializacion funciona correctamente")


def test_semilla_global():
    """La semilla global debe funcionar."""
    # Limpiar estado previo
    seed = init_global_seed("test-global")
    
    assert get_global_seed() is not None, "Semilla global debe estar inicializada"
    assert get_global_seed().master_seed == "test-global", "Semilla global debe tener valor correcto"
    
    # Cambiar semilla global
    nueva_seed = WorldSeed("nueva-global")
    set_global_seed(nueva_seed)
    
    assert get_global_seed().master_seed == "nueva-global", "Semilla global debe actualizarse"
    print("[OK] Semilla global funciona correctamente")


def test_reproducibilidad_partida():
    """Simula el caso de uso real: reproducir una partida."""
    # Crear partida con semilla
    seed = WorldSeed("partida-12345")
    
    # Simular generacion de mundo
    bioma_inicial = seed.get_choice("zona_0_0", ["bosque", "desierto", "pantano"])
    nivel_enemigo = seed.get_int("zona_0_0", 1, 10)
    tesoro = seed.get_weighted_choice("zona_0_0", ["comun", "raro", "epico"], [70, 25, 5])
    
    # Guardar semilla
    seed_guardada = seed.to_dict()
    
    # Mas tarde, cargar partida
    seed_cargada = WorldSeed.from_dict(seed_guardada)
    
    # Generar mismo mundo
    bioma_cargado = seed_cargada.get_choice("zona_0_0", ["bosque", "desierto", "pantano"])
    nivel_cargado = seed_cargada.get_int("zona_0_0", 1, 10)
    tesoro_cargado = seed_cargada.get_weighted_choice("zona_0_0", ["comun", "raro", "epico"], [70, 25, 5])
    
    assert bioma_inicial == bioma_cargado, "Bioma debe ser igual"
    assert nivel_enemigo == nivel_cargado, "Nivel debe ser igual"
    assert tesoro == tesoro_cargado, "Tesoro debe ser igual"
    
    print(f"[OK] Partida reproducible: bioma={bioma_inicial}, nivel={nivel_enemigo}, tesoro={tesoro}")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Semillas (WorldSeed)")
    print("="*50 + "\n")
    
    tests = [
        test_semilla_aleatoria,
        test_semilla_desde_string,
        test_determinismo,
        test_contextos_independientes,
        test_subseed_unicas,
        test_helpers,
        test_serializacion,
        test_semilla_global,
        test_reproducibilidad_partida,
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
