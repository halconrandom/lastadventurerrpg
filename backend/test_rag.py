"""Test del sistema RAG de ejemplos de dialogo."""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from systems.npcs.example_retriever import ExampleRetriever

def main():
    retriever = ExampleRetriever()
    print(f"Ejemplos cargados: {len(retriever._ejemplos)}")
    
    if not retriever._ejemplos:
        print("ERROR: No se cargaron ejemplos")
        return
    
    # Test 1: Enano fanatico estoico
    print("\n=== Test 1: Enano fanatico estoico (saludo) ===")
    ejemplos = retriever.buscar_ejemplos(
        raza='enano',
        rasgos=['fanatico', 'estoico'],
        rol='cualquiera',
        tipo_interaccion='saludo'
    )
    for e in ejemplos:
        print(f"  - {e.accion} {e.dialogo}")
    
    # Test 2: Tabernero alegre
    print("\n=== Test 2: Tabernero alegre (saludo) ===")
    ejemplos = retriever.buscar_ejemplos(
        raza='humano',
        rasgos=['alegre'],
        rol='tabernero',
        tipo_interaccion='saludo'
    )
    for e in ejemplos:
        print(f"  - {e.accion} {e.dialogo}")
    
    # Test 3: Formatear para prompt
    print("\n=== Test 3: Formatear para prompt ===")
    ejemplos = retriever.buscar_ejemplos(
        raza='enano',
        rasgos=['fanatico', 'estoico'],
        rol='cualquiera',
        tipo_interaccion='conflicto'
    )
    formateado = retriever.formatear_ejemplos_para_prompt(ejemplos, "Dorian")
    print(formateado)

if __name__ == "__main__":
    main()
