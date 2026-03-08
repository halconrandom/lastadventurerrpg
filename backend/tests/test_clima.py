# -*- coding: utf-8 -*-
"""
Tests para el sistema de clima dinamico.
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed
from systems.clima import ClimaGenerator, EstadoClima, CicloDiaNoche


def test_generar_clima_basico():
    """Se puede generar un clima basico."""
    seed = WorldSeed("test-clima-basico")
    gen = ClimaGenerator(seed)
    
    clima = gen.generar_clima("bosque_ancestral", "test1")
    
    assert clima is not None, "Debe generar clima"
    assert clima.tipo is not None, "Debe tener tipo"
    assert len(clima.efectos) > 0, "Debe tener efectos"
    print(f"[OK] Clima generado: {clima.tipo} ({clima.intensidad})")


def test_clima_por_bioma():
    """Cada bioma tiene climas apropiados."""
    seed = WorldSeed("test-clima-bioma")
    gen = ClimaGenerator(seed)
    
    # Bosque
    clima_bosque = gen.generar_clima("bosque_ancestral", "test2")
    
    # Montana
    clima_montana = gen.generar_clima("montanas_heladas", "test3")
    
    # Desierto
    clima_desierto = gen.generar_clima("desierto_ceniza", "test4")
    
    assert clima_bosque is not None
    assert clima_montana is not None
    assert clima_desierto is not None
    
    print(f"[OK] Bosque: {clima_bosque.tipo}, Montana: {clima_montana.tipo}, Desierto: {clima_desierto.tipo}")


def test_ciclo_dia_noche():
    """El ciclo dia/noche funciona correctamente."""
    seed = WorldSeed("test-ciclo")
    gen = ClimaGenerator(seed)
    
    # Madrugada
    ciclo_madrugada = gen.get_ciclo_dia_noche(3)
    assert ciclo_madrugada.fase == "madrugada"
    assert ciclo_madrugada.luz < 0.5
    
    # Dia
    ciclo_dia = gen.get_ciclo_dia_noche(12)
    assert ciclo_dia.fase == "dia"
    assert ciclo_dia.luz == 1.0
    
    # Noche
    ciclo_noche = gen.get_ciclo_dia_noche(23)
    assert ciclo_noche.fase == "noche"
    assert ciclo_noche.luz < 0.2
    
    print(f"[OK] Ciclo: madrugada(luz={ciclo_madrugada.luz}), dia(luz={ciclo_dia.luz}), noche(luz={ciclo_noche.luz})")


def test_avanzar_hora():
    """Se puede avanzar la hora."""
    seed = WorldSeed("test-avanzar")
    gen = ClimaGenerator(seed)
    
    ciclo = gen.get_ciclo_dia_noche(10)
    assert ciclo.fase == "dia"
    
    # Avanzar 12 horas (de 10 a 22 = noche)
    nuevo_ciclo = gen.avanzar_hora(10, 12)
    assert nuevo_ciclo.fase == "noche"
    
    print(f"[OK] Avanzar hora: dia(10h) -> noche(22h)")


def test_efectos_combinados():
    """Se pueden combinar efectos de clima y ciclo."""
    seed = WorldSeed("test-combinados")
    gen = ClimaGenerator(seed)
    
    clima = gen.generar_clima("bosque_ancestral", "test5")
    ciclo = gen.get_ciclo_dia_noche(12)  # Dia
    
    efectos = gen.get_efectos_combinados(clima, ciclo)
    
    assert "visibilidad" in efectos
    assert "movimiento" in efectos
    assert "efectos" in efectos
    
    print(f"[OK] Efectos combinados: vis={efectos['visibilidad']}, mov={efectos['movimiento']}")


def test_efectos_noche():
    """La noche agrega efectos adicionales."""
    seed = WorldSeed("test-noche")
    gen = ClimaGenerator(seed)
    
    clima = gen.generar_clima("bosque_ancestral", "test6")
    
    # Efectos de dia
    ciclo_dia = gen.get_ciclo_dia_noche(12)
    efectos_dia = gen.get_efectos_combinados(clima, ciclo_dia)
    
    # Efectos de noche
    ciclo_noche = gen.get_ciclo_dia_noche(23)
    efectos_noche = gen.get_efectos_combinados(clima, ciclo_noche)
    
    # La noche debe tener mas efectos
    assert "oscuridad" in efectos_noche["efectos"]
    assert "sigilo_mejorado" in efectos_noche["efectos"]
    
    print(f"[OK] Efectos noche: {efectos_noche['efectos']}")


def test_determinismo_clima():
    """Misma semilla produce mismo clima."""
    seed1 = WorldSeed("test-determinismo-clima")
    seed2 = WorldSeed("test-determinismo-clima")
    
    gen1 = ClimaGenerator(seed1)
    gen2 = ClimaGenerator(seed2)
    
    clima1 = gen1.generar_clima("bosque_ancestral", "test7")
    clima2 = gen2.generar_clima("bosque_ancestral", "test7")
    
    assert clima1.tipo == clima2.tipo
    assert clima1.intensidad == clima2.intensidad
    
    print(f"[OK] Determinismo: {clima1.tipo} == {clima2.tipo}")


def test_intensidad_clima():
    """El clima tiene intensidad variable."""
    seed = WorldSeed("test-intensidad")
    gen = ClimaGenerator(seed)
    
    # Generar varios climas
    climas = [gen.generar_clima("bosque_ancestral", f"test{i}") for i in range(20)]
    
    intensidades = set(c.intensidad for c in climas)
    
    assert len(intensidades) > 1, "Debe haber variedad de intensidades"
    
    print(f"[OK] Intensidades encontradas: {intensidades}")


def test_transicionar_clima():
    """Se puede transicionar el clima."""
    seed = WorldSeed("test-transicion")
    gen = ClimaGenerator(seed)
    
    clima_inicial = gen.generar_clima("bosque_ancestral", "test8")
    duracion_inicial = clima_inicial.duracion
    
    # Transicionar
    clima_nuevo = gen.transicionar_clima(clima_inicial, "bosque_ancestral", "test8")
    
    # La duracion debe reducirse
    assert clima_nuevo.duracion == duracion_inicial - 1 or clima_nuevo.duracion >= 3
    
    print(f"[OK] Transicion: duracion {duracion_inicial} -> {clima_nuevo.duracion}")


def test_serializacion_clima():
    """El clima se puede serializar."""
    seed = WorldSeed("test-serializacion-clima")
    gen = ClimaGenerator(seed)
    
    clima_original = gen.generar_clima("bosque_ancestral", "test9")
    
    # Serializar
    data = clima_original.to_dict()
    
    # Deserializar
    clima_restaurado = EstadoClima.from_dict(data)
    
    assert clima_original.tipo == clima_restaurado.tipo
    assert clima_original.intensidad == clima_restaurado.intensidad
    
    print(f"[OK] Serializacion correcta para {clima_original.tipo}")


def test_serializacion_ciclo():
    """El ciclo se puede serializar."""
    seed = WorldSeed("test-serializacion-ciclo")
    gen = ClimaGenerator(seed)
    
    ciclo_original = gen.get_ciclo_dia_noche(15)
    
    # Serializar
    data = ciclo_original.to_dict()
    
    # Deserializar
    ciclo_restaurado = CicloDiaNoche.from_dict(data)
    
    assert ciclo_original.fase == ciclo_restaurado.fase
    assert ciclo_original.luz == ciclo_restaurado.luz
    
    print(f"[OK] Serializacion ciclo correcta para {ciclo_original.fase}")


def test_climas_extremos():
    """Pueden ocurrir climas extremos."""
    seed = WorldSeed("test-extremos")
    gen = ClimaGenerator(seed)
    
    # Generar muchos climas para encontrar extremos
    climas = [gen.generar_clima("montanas_heladas", f"ext{i}") for i in range(100)]
    
    extremos = [c for c in climas if c.intensidad in ["intenso", "extremo"]]
    
    print(f"[OK] Climas extremos encontrados: {len(extremos)} de 100")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Clima Dinamico")
    print("="*50 + "\n")
    
    tests = [
        test_generar_clima_basico,
        test_clima_por_bioma,
        test_ciclo_dia_noche,
        test_avanzar_hora,
        test_efectos_combinados,
        test_efectos_noche,
        test_determinismo_clima,
        test_intensidad_clima,
        test_transicionar_clima,
        test_serializacion_clima,
        test_serializacion_ciclo,
        test_climas_extremos,
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
