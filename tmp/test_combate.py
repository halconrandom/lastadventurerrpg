
import sys
import os
import random

# Añadir src al path para poder importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src')))

from systems.combate import CombateManager, EstadoCombate
from models.personaje import Personaje
from models.stats import Stats

def test_combate():
    print("--- INICIANDO TEST DE COMBATE ---")
    
    # 1. Crear personaje de prueba
    print("\n1. Creando personaje...")
    p = Personaje(nombre="TestHero")
    p.stats.atk_base = 20 # ATK base 20
    p.stats.def_base = 10 # 10% defensa base
    p.habilidades.ganar_experiencia_habilidad("Defensa", 500) # Nivel 6 de defensa (+6%)
    # Total def = 16%
    
    print(f"Stats: ATK={p.ataque}, DEF={p.stats.get_def()}%, NvDefensa={p.get_nivel_defensa()}")
    
    # 2. Iniciar CombateManager
    manager = CombateManager()
    
    # Simular datos de enemigo
    enemigos_demo = [{
        "id": "lobo_1",
        "nombre": "Lobo de Test",
        "categoria": "bestia",
        "nivel": 1,
        "zona": "bosque",
        "stats_base": {"hp": 50, "atk": 10, "def": 0, "velocidad": 5},
        "experiencia_base": 100,
        "oro_base": 50,
        "drops": [],
        "habilidades": []
    }]
    
    manager.iniciar_combate(p, enemigos_demo)
    print(f"Combate iniciado contra {manager.enemigos['enemigo_1'].nombre}")
    
    # 3. Test de Ataque Jugador
    print("\n2. Test de Ataque...")
    manager.arma_equipada = "Espada"
    res_atk = manager._ejecutar_ataque(manager.jugadores['jugador_1'], 'enemigo_1')
    print(f"Resultado Ataque: {res_atk['mensaje']}")
    print(f"Exp acumulada: {manager.exp_acumulada}")
    
    if manager.exp_acumulada.get("Espada") == 5:
        print("✅ Experiencia de Espada registrada correctamente.")
    else:
        print("❌ Error en experiencia de Espada.")

    # 4. Test de Bloqueo y Daño Recibido
    print("\n3. Test de Bloqueo...")
    manager.jugadores['jugador_1'].esta_bloqueando = True
    
    # Simular ataque de enemigo (ATK 10)
    # Reducción jugador: 16% -> daño_recibido = 10 * (1 - 0.16) = 8.4 -> 8
    # Bloqueo: 8 * 0.5 = 4
    res_def = manager._ejecutar_ataque(manager.enemigos['enemigo_1'], 'jugador_1')
    print(f"Resultado Defensa (Bloqueando): {res_def['mensaje']}")
    
    if res_def['daño'] == 4:
        print("✅ Daño de bloqueo calculado correctamente (4).")
    else:
        print(f"❌ Error en daño de bloqueo. Esperaba 4, recibí {res_def['daño']}")
        
    print(f"Exp acumulada tras bloqueo: {manager.exp_acumulada}")
    if manager.exp_acumulada.get("Defensa") > 0:
        print("✅ Experiencia de Defensa registrada correctamente.")
    else:
        print("❌ Error en experiencia de Defensa.")

    print("\n--- TEST FINALIZADO ---")

if __name__ == "__main__":
    test_combate()
