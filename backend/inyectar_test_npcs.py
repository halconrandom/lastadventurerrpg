import sys
import os
from pathlib import Path

# Configurar paths para que Python encuentre los módulos
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from systems.save_manager import SaveManager
from systems.npcs.npc_manager import NPCManager
from systems.seed import init_global_seed

def inyectar_npcs_prueba(slot_num=1):
    save_manager = SaveManager()
    
    # 1. Cargar o crear datos base
    datos, _ = save_manager.cargar(slot_num)
    if not datos:
        print(f"Creando nueva partida base en Slot {slot_num}...")
        datos = save_manager.crear_save_vacio("Tester", "masculino", "normal")
    
    # Asegurar que los datos tienen la estructura de NPCs (migración)
    if "npcs" not in datos:
        datos["npcs"] = {
            "version": "1.0",
            "activos": [],
            "por_id": {},
            "rumores": []
        }
    
    # 2. Inicializar Manager de NPCs
    seed = init_global_seed(datos.get("exploracion", {}).get("seed", "test_seed_123"))
    manager = NPCManager(seed)
    manager.cargar_desde_save(datos.get("npcs", {}))
    
    # 3. Generar NPCs en el pueblo de inicio
    print("Generando NPCs en 'pueblo_inicio'...")
    manager.generar_npcs_para_ubicacion("pueblo_inicio", "pueblo", (0, 0), cantidad=5)
    
    # 4. Marcar algunos como activos para que aparezcan en la lista
    manager.npcs_activos_ids = list(manager.npcs_cargados.keys())
    
    # 5. Guardar de vuelta al slot
    datos["npcs"] = manager.to_dict()
    exito, msg = save_manager.guardar(slot_num, datos)
    
    if exito:
        print(f"¡ÉXITO! Se han inyectado {len(manager.npcs_cargados)} NPCs en el Slot {slot_num}.")
        print("Ahora puedes iniciar 'python main.py' y verlos en http://localhost:3000/test-npcs")
    else:
        print(f"Error al guardar: {msg}")

if __name__ == "__main__":
    inyectar_npcs_prueba(1)
