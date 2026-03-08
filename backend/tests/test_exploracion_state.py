"""
Tests para el sistema de estado de exploracion.
"""

import pytest
import sys
from pathlib import Path

# Añadir src al path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from systems.exploracion_state import (
    ExploracionState,
    ZonaDescubierta,
    crear_exploracion_inicial
)


class TestZonaDescubierta:
    """Tests para ZonaDescubierta."""
    
    def test_crear_zona_basica(self):
        """Una zona se crea correctamente."""
        zona = ZonaDescubierta(
            x=5,
            y=10,
            nombre="Bosque Sombrío",
            bioma_key="bosque_ancestral"
        )
        
        assert zona.x == 5
        assert zona.y == 10
        assert zona.nombre == "Bosque Sombrío"
        assert zona.bioma_key == "bosque_ancestral"
        assert zona.veces_explorada == 0
        assert zona.estado == "descubierta"
        assert zona.tiles_descubiertos == 0
        assert len(zona.pois_encontrados) == 0
    
    def test_zona_serializacion(self):
        """Una zona se serializa y deserializa correctamente."""
        zona_original = ZonaDescubierta(
            x=3,
            y=7,
            nombre="Cueva Oscura",
            bioma_key="cueva",
            veces_explorada=2,
            estado="explorando",
            tiles_descubiertos=15,
            pois_encontrados=["tesoro_antiguo", "altar"]
        )
        
        data = zona_original.to_dict()
        zona_restaurada = ZonaDescubierta.from_dict(data)
        
        assert zona_restaurada.x == zona_original.x
        assert zona_restaurada.y == zona_original.y
        assert zona_restaurada.nombre == zona_original.nombre
        assert zona_restaurada.bioma_key == zona_original.bioma_key
        assert zona_restaurada.veces_explorada == zona_original.veces_explorada
        assert zona_restaurada.estado == zona_original.estado
        assert zona_restaurada.tiles_descubiertos == zona_original.tiles_descubiertos
        assert zona_restaurada.pois_encontrados == zona_original.pois_encontrados


class TestExploracionState:
    """Tests para ExploracionState."""
    
    def test_crear_estado_inicial(self):
        """Un estado inicial se crea correctamente."""
        state = ExploracionState(seed="test_seed_123")
        
        assert state.seed == "test_seed_123"
        assert state.x == 0
        assert state.y == 0
        assert len(state.zonas) == 0
        assert len(state.eventos_completados) == 0
        assert state.estadisticas["total_exploraciones"] == 0
    
    def test_descubrir_zona(self):
        """Descubrir una zona la registra correctamente."""
        state = ExploracionState(seed="test")
        
        zona = state.descubrir_zona(5, 10, "Bosque Encantado", "bosque_ancestral")
        
        assert state.zona_descubierta(5, 10)
        assert zona.nombre == "Bosque Encantado"
        assert state.estadisticas["zonas_descubiertas"] == 1
    
    def test_descubrir_zona_existente(self):
        """Descubrir una zona ya existente no duplica."""
        state = ExploracionState(seed="test")
        
        state.descubrir_zona(5, 10, "Bosque Encantado", "bosque_ancestral")
        state.descubrir_zona(5, 10, "Otro Nombre", "otro_bioma")
        
        assert len(state.zonas) == 1
        assert state.zonas["5_10"].nombre == "Bosque Encantado"
        assert state.estadisticas["zonas_descubiertas"] == 1
    
    def test_explorar_zona(self):
        """Explorar una zona actualiza su estado."""
        state = ExploracionState(seed="test")
        state.descubrir_zona(0, 0, "Inicio", "pueblo")
        
        # Primera exploracion
        zona = state.explorar_zona(0, 0, tiles_descubiertos=5)
        assert zona.veces_explorada == 1
        assert zona.estado == "explorando"
        assert zona.tiles_descubiertos == 5
        assert state.estadisticas["total_exploraciones"] == 1
        
        # Segunda exploracion
        state.explorar_zona(0, 0, tiles_descubiertos=3)
        assert zona.veces_explorada == 2
        assert zona.tiles_descubiertos == 8
        
        # Tercera exploracion - cambia a "explorada"
        state.explorar_zona(0, 0)
        assert zona.estado == "explorada"
        
        # Quinta exploracion - cambia a "agotada"
        state.explorar_zona(0, 0)
        state.explorar_zona(0, 0)
        assert zona.estado == "agotada"
    
    def test_explorar_zona_poi(self):
        """Explorar puede descubrir POIs."""
        state = ExploracionState(seed="test")
        state.descubrir_zona(0, 0, "Inicio", "pueblo")
        
        zona = state.explorar_zona(0, 0, poi_encontrado="tesoro_oculto")
        
        assert "tesoro_oculto" in zona.pois_encontrados
        assert state.estadisticas["pois_descubiertos"] == 1
        
        # No duplica POIs
        state.explorar_zona(0, 0, poi_encontrado="tesoro_oculto")
        assert len(zona.pois_encontrados) == 1
    
    def test_explorar_zona_no_descubierta(self):
        """Explorar zona no descubierta lanza error."""
        state = ExploracionState(seed="test")
        
        with pytest.raises(ValueError):
            state.explorar_zona(5, 5)
    
    def test_mover_jugador(self):
        """Mover al jugador actualiza coordenadas."""
        state = ExploracionState(seed="test")
        
        assert state.x == 0
        assert state.y == 0
        
        state.mover_jugador(10, -5)
        
        assert state.x == 10
        assert state.y == -5
    
    def test_registrar_evento(self):
        """Registrar evento lo añade a completados."""
        state = ExploracionState(seed="test")
        
        state.registrar_evento("evento_001")
        
        assert "evento_001" in state.eventos_completados
        assert state.estadisticas["eventos_encontrados"] == 1
        
        # No duplica
        state.registrar_evento("evento_001")
        assert len(state.eventos_completados) == 1
    
    def test_registrar_encuentro_hostil(self):
        """Registrar encuentro hostil incrementa contador."""
        state = ExploracionState(seed="test")
        
        state.registrar_encuentro_hostil()
        state.registrar_encuentro_hostil()
        
        assert state.estadisticas["encuentros_hostiles"] == 2
    
    def test_zonas_adyacentes(self):
        """Obtener zonas adyacentes funciona correctamente."""
        state = ExploracionState(seed="test")
        
        # Descubrir zonas alrededor
        state.descubrir_zona(0, 0, "Centro", "pueblo")
        state.descubrir_zona(1, 0, "Este", "bosque")
        state.descubrir_zona(-1, 0, "Oeste", "bosque")
        state.descubrir_zona(0, 1, "Norte", "monte")
        state.descubrir_zona(0, -1, "Sur", "pantano")
        
        adyacentes = state.get_zonas_adyacentes()
        
        assert len(adyacentes) == 4
        assert "1_0" in adyacentes
        assert "-1_0" in adyacentes
        assert "0_1" in adyacentes
        assert "0_-1" in adyacentes
    
    def test_get_resumen(self):
        """El resumen contiene datos correctos."""
        state = ExploracionState(seed="test")
        state.descubrir_zona(0, 0, "Inicio", "pueblo")
        state.descubrir_zona(1, 0, "Bosque", "bosque")
        state.registrar_evento("evento_001")
        
        resumen = state.get_resumen()
        
        assert resumen["posicion"] == {"x": 0, "y": 0}
        assert resumen["zonas_descubiertas"] == 2
        assert resumen["eventos_completados"] == 1
        assert "estadisticas" in resumen
    
    def test_serializacion_completa(self):
        """El estado completo se serializa correctamente."""
        state = ExploracionState(seed="test_seed")
        state.descubrir_zona(0, 0, "Inicio", "pueblo")
        state.descubrir_zona(5, 10, "Bosque", "bosque_ancestral")
        state.explorar_zona(0, 0, tiles_descubiertos=10, poi_encontrado="fuente")
        state.mover_jugador(5, 10)
        state.registrar_evento("evento_001")
        
        data = state.to_dict()
        state_restaurado = ExploracionState.from_dict(data)
        
        assert state_restaurado.seed == state.seed
        assert state_restaurado.x == state.x
        assert state_restaurado.y == state.y
        assert len(state_restaurado.zonas) == len(state.zonas)
        assert state_restaurado.eventos_completados == state.eventos_completados
        assert state_restaurado.estadisticas == state.estadisticas


class TestCrearExploracionInicial:
    """Tests para crear_exploracion_inicial."""
    
    def test_crear_inicial(self):
        """Crear estado inicial funciona correctamente."""
        state = crear_exploracion_inicial("mi_semilla_123")
        
        assert state.seed == "mi_semilla_123"
        assert state.x == 0
        assert state.y == 0
        assert len(state.zonas) == 1
        assert "0_0" in state.zonas
        assert state.zonas["0_0"].nombre == "Pueblo Inicio"
    
    def test_determinismo(self):
        """Misma semilla produce mismo estado inicial."""
        state1 = crear_exploracion_inicial("semilla_test")
        state2 = crear_exploracion_inicial("semilla_test")
        
        assert state1.seed == state2.seed
        assert state1.zonas["0_0"].nombre == state2.zonas["0_0"].nombre