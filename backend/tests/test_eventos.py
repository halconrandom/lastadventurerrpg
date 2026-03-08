# -*- coding: utf-8 -*-
"""
Tests para el sistema de eventos de exploracion.
"""

import sys
sys.path.insert(0, 'src')

from systems.seed import WorldSeed
from systems.eventos import EventoGenerator, Evento, OpcionEvento


def test_generar_evento_basico():
    """Se puede generar un evento basico."""
    seed = WorldSeed("test-evento-basico")
    gen = EventoGenerator(seed)
    
    evento = gen.generar_evento("test1")
    
    assert evento is not None, "Debe generar un evento"
    assert evento.titulo is not None, "Debe tener titulo"
    assert len(evento.opciones) > 0, "Debe tener opciones"
    print(f"[OK] Evento generado: {evento.titulo}")


def test_evento_tiene_opciones():
    """Un evento tiene opciones validas."""
    seed = WorldSeed("test-opciones")
    gen = EventoGenerator(seed)
    
    evento = gen.generar_evento("test2")
    
    for opcion in evento.opciones:
        assert opcion.texto is not None, "Opcion debe tener texto"
        assert opcion.resultado_tipo in ["exito", "fallo", "neutral"], "Tipo valido"
        assert opcion.resultado_texto is not None, "Debe tener resultado"
    
    print(f"[OK] Evento tiene {len(evento.opciones)} opciones validas")


def test_resolver_evento():
    """Se puede resolver un evento."""
    seed = WorldSeed("test-resolver")
    gen = EventoGenerator(seed)
    
    evento = gen.generar_evento("test3")
    
    # Resolver con primera opcion
    resultado = gen.resolver_evento(evento, 0, "test3")
    
    assert resultado is not None, "Debe retornar resultado"
    assert "tipo_resultado" in resultado, "Debe tener tipo de resultado"
    assert "texto_resultado" in resultado, "Debe tener texto resultado"
    
    print(f"[OK] Evento resuelto: {resultado['tipo_resultado']}")


def test_eventos_por_bioma():
    """Se pueden filtrar eventos por bioma."""
    seed = WorldSeed("test-bioma")
    gen = EventoGenerator(seed)
    
    # Eventos para bosque
    eventos_bosque = gen.get_eventos_por_bioma("bosque_ancestral")
    
    # Eventos para pantano
    eventos_pantano = gen.get_eventos_por_bioma("pantano_sombrio")
    
    assert len(eventos_bosque) > 0, "Debe haber eventos para bosque"
    assert len(eventos_pantano) > 0, "Debe haber eventos para pantano"
    
    print(f"[OK] Eventos bosque: {len(eventos_bosque)}, pantano: {len(eventos_pantano)}")


def test_eventos_por_tipo():
    """Se pueden filtrar eventos por tipo."""
    seed = WorldSeed("test-tipo")
    gen = EventoGenerator(seed)
    
    encuentros = gen.get_eventos_por_tipo("encuentro_npc")
    descubrimientos = gen.get_eventos_por_tipo("descubrimiento")
    peligros = gen.get_eventos_por_tipo("peligro")
    
    assert len(encuentros) > 0, "Debe haber encuentros"
    assert len(descubrimientos) > 0, "Debe haber descubrimientos"
    assert len(peligros) > 0, "Debe haber peligros"
    
    print(f"[OK] Encuentros: {len(encuentros)}, Descubrimientos: {len(descubrimientos)}, Peligros: {len(peligros)}")


def test_determinismo_eventos():
    """Misma semilla produce mismos eventos."""
    seed1 = WorldSeed("test-determinismo-eventos")
    seed2 = WorldSeed("test-determinismo-eventos")
    
    gen1 = EventoGenerator(seed1)
    gen2 = EventoGenerator(seed2)
    
    evento1 = gen1.generar_evento("test5")
    evento2 = gen2.generar_evento("test5")
    
    assert evento1.id == evento2.id, "Mismo evento"
    assert evento1.titulo == evento2.titulo, "Mismo titulo"
    
    print(f"[OK] Determinismo: {evento1.titulo} == {evento2.titulo}")


def test_rarezas_eventos():
    """Los eventos tienen rarezas diferentes."""
    seed = WorldSeed("test-rarezas")
    gen = EventoGenerator(seed)
    
    # Generar muchos eventos para ver rarezas
    eventos = [gen.generar_evento(f"test{i}") for i in range(50)]
    
    rarezas = set(e.rareza for e in eventos)
    
    assert len(rarezas) > 1, "Debe haber variedad de rarezas"
    
    print(f"[OK] Rarezas encontradas: {rarezas}")


def test_recompensas_evento():
    """Los eventos pueden dar recompensas."""
    seed = WorldSeed("test-recompensas")
    gen = EventoGenerator(seed)
    
    # Buscar evento con recompensa
    evento = gen.get_evento_by_id("viajero_perdido")
    
    # Resolver opcion que da recompensa
    resultado = gen.resolver_evento(evento, 0, "test")
    
    assert resultado["recompensa"] is not None, "Debe tener recompensa"
    assert "item" in resultado["recompensa"] or "oro" in resultado["recompensa"] or "exp" in resultado["recompensa"]
    
    print(f"[OK] Recompensa: {resultado['recompensa']}")


def test_consecuencias_evento():
    """Los eventos pueden tener consecuencias negativas."""
    seed = WorldSeed("test-consecuencias")
    gen = EventoGenerator(seed)
    
    evento = gen.get_evento_by_id("viajero_perdido")
    
    # Resolver opcion con consecuencia
    resultado = gen.resolver_evento(evento, 2, "test")  # Robar
    
    assert resultado["consecuencia"] is not None, "Debe tener consecuencia"
    
    print(f"[OK] Consecuencia: {resultado['consecuencia']}")


def test_serializacion_evento():
    """Un evento se puede serializar."""
    seed = WorldSeed("test-serializacion")
    gen = EventoGenerator(seed)
    
    evento = gen.generar_evento("test_serial")
    data = evento.to_dict()
    
    assert "id" in data, "Debe tener id"
    assert "titulo" in data, "Debe tener titulo"
    assert "opciones" in data, "Debe tener opciones"
    assert "biomas" in data, "Debe tener biomas"
    assert "rareza" in data, "Debe tener rareza"
    
    print(f"[OK] Serializacion correcta para {evento.titulo}")


def test_opcion_invalida():
    """Opcion invalida retorna error."""
    seed = WorldSeed("test-invalida")
    gen = EventoGenerator(seed)
    
    evento = gen.generar_evento("test_invalid")
    
    resultado = gen.resolver_evento(evento, 999, "test")
    
    assert "error" in resultado, "Debe retornar error"
    
    print(f"[OK] Opcion invalida manejada correctamente")


def test_evento_por_id():
    """Se puede obtener evento por ID."""
    seed = WorldSeed("test-id")
    gen = EventoGenerator(seed)
    
    evento = gen.get_evento_by_id("viajero_perdido")
    
    assert evento is not None, "Debe encontrar el evento"
    assert evento.id == "viajero_perdido", "Debe ser el evento correcto"
    
    print(f"[OK] Evento por ID: {evento.titulo}")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: Sistema de Eventos de Exploracion")
    print("="*50 + "\n")
    
    tests = [
        test_generar_evento_basico,
        test_evento_tiene_opciones,
        test_resolver_evento,
        test_eventos_por_bioma,
        test_eventos_por_tipo,
        test_determinismo_eventos,
        test_rarezas_eventos,
        test_recompensas_evento,
        test_consecuencias_evento,
        test_serializacion_evento,
        test_opcion_invalida,
        test_evento_por_id,
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
