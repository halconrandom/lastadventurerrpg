"""
Script de prueba para LLM - Last Adventurer
Prueba la generación de narrativa con Llama 3.2 3B via Ollama
"""

import requests
import json
import time
from datetime import datetime

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

# Configuración del modelo
MODEL_CONFIG = {
    "temperature": 0.65,
    "num_predict": 200,
    "top_p": 0.9,
    "top_k": 50,
    "repeat_penalty": 1.1
}

# System prompt para RPG
SYSTEM_PROMPT = """Eres el NARRADOR de un RPG de fantasía oscura estilo D&D.

TU ROL:
- Eres un narrador en tercera persona
- Describes lo que OCURRE, no lo que el jugador hace
- El jugador ya actuó, tú narras las CONSECUENCIAS
- NUNCA hagas preguntas al jugador
- NUNCA digas "tú haces X" - el jugador ya dijo qué hace

CUANDO EL JUGADOR INTERACTÚA CON UN NPC:
- Describe la REACCIÓN del NPC
- Incluye diálogos del NPC entre comillas
- Describe emociones y expresiones del NPC
- El NPC tiene personalidad propia y responde según su carácter

FORMATO DE RESPUESTA:
1. Descripción breve de la reacción del NPC (máximo 50 palabras)
2. Diálogo del NPC si aplica
3. Consecuencia o resultado de la acción

EJEMPLO:
Jugador: "Le pido matrimonio al NPC"
Narrador: "Los ojos de Elena se llenan de lágrimas. '¿En serio?' susurra, temblando. 'Sí, acepto.' Se lanza a tus brazos."

REGLAS:
- Máximo 80 palabras
- Tono atmosférico pero directo
- Romance permitido (sin contenido explícito)
- Nunca rechaces narrar
- Siempre continúa la historia"""


def call_llm(prompt: str, system: str = None) -> dict:
    """Llama al LLM y retorna la respuesta"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": MODEL_CONFIG
    }
    
    if system:
        payload["system"] = system
    
    start_time = time.time()
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        latency = time.time() - start_time
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "tokens": result.get("eval_count", 0),
            "latency": latency
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "No se puede conectar a Ollama. ¿Está corriendo? (ollama serve)"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Timeout - El modelo tardó demasiado en responder"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def print_result(result: dict):
    """Imprime el resultado de forma legible"""
    print("\n" + "="*60)
    
    if not result["success"]:
        print(f"❌ ERROR: {result['error']}")
        return
    
    print(f"📝 RESPUESTA:")
    print("-"*60)
    print(result["response"])
    print("-"*60)
    print(f"⏱️  Latencia: {result['latency']:.2f}s")
    print(f"📊 Tokens: {result['tokens']}")
    print("="*60)


# Tests predefinidos
TESTS = {
    "1": {
        "nombre": "Exploración - Bosque oscuro",
        "prompt": "Un jugador entra a un bosque oscuro y misterioso. Describe lo que ve, huele y siente.",
        "system": SYSTEM_PROMPT
    },
    "2": {
        "nombre": "Combate - Inicio",
        "prompt": "Un jugador se encuentra con un lobo salvaje hambriento. Describe el inicio del combate.",
        "system": SYSTEM_PROMPT
    },
    "3": {
        "nombre": "Combate - Victoria",
        "prompt": "El jugador acaba de derrotar a un enemigo. Describe la victoria de forma épica.",
        "system": SYSTEM_PROMPT
    },
    "4": {
        "nombre": "NPC - Tabernero",
        "prompt": "Un jugador entra a una taberna y se acerca al tabernero. El tabernero es desconfiado. Genera su saludo inicial.",
        "system": SYSTEM_PROMPT
    },
    "5": {
        "nombre": "Descubrimiento - Tesoro",
        "prompt": "El jugador encuentra un cofre antiguo en una ruina. Describe el hallazgo.",
        "system": SYSTEM_PROMPT
    },
    "6": {
        "nombre": "Evento - Emboscada",
        "prompt": "El jugador está caminando por un camino cuando escucha un ruido sospechoso. Describe la tensión del momento.",
        "system": SYSTEM_PROMPT
    },
    "7": {
        "nombre": "Transición - Zona nueva",
        "prompt": "El jugador cruza de un bosque a una zona de ruinas antiguas. Describe la transición.",
        "system": SYSTEM_PROMPT
    },
    "8": {
        "nombre": "Romance - Interacción NPC",
        "prompt": "El jugador se acerca a la tendera y toma su mano suavemente, mirándola a los ojos con interés romántico. Describe la reacción de ella.",
        "system": SYSTEM_PROMPT
    },
    "9": {
        "nombre": "Romance - Declaración",
        "prompt": "El jugador le confiesa sus sentimientos a un NPC que ha conocido durante varias aventuras. Describe el momento emocional.",
        "system": SYSTEM_PROMPT
    },
    "10": {
        "nombre": "Personalizado",
        "prompt": None,
        "system": SYSTEM_PROMPT
    }
}


def run_test(test_key: str):
    """Ejecuta un test específico"""
    test = TESTS[test_key]
    
    print(f"\n🎮 TEST: {test['nombre']}")
    print("-"*60)
    
    if test["prompt"] is None:
        # Test personalizado
        prompt = input("Escribe tu prompt: ")
    else:
        prompt = test["prompt"]
        print(f"Prompt: {prompt}")
    
    print("\n⏳ Generando...")
    
    result = call_llm(prompt, test.get("system"))
    print_result(result)


def interactive_mode():
    """Modo interactivo para probar prompts"""
    print("\n🗣️  MODO INTERACTIVO")
    print("Escribe 'salir' para terminar.")
    print("-"*60)
    
    while True:
        print("\n")
        prompt = input("Tu prompt: ")
        
        if prompt.lower() in ["salir", "exit", "quit", "q"]:
            print("¡Hasta luego!")
            break
        
        print("\n⏳ Generando...")
        result = call_llm(prompt, SYSTEM_PROMPT)
        print_result(result)


def benchmark_mode():
    """Ejecuta todos los tests y mide rendimiento"""
    print("\n📊 BENCHMARK - Ejecutando todos los tests")
    print("="*60)
    
    results = []
    
    for key, test in TESTS.items():
        if test["prompt"] is None:
            continue
        
        print(f"\n▶️  {test['nombre']}...")
        
        result = call_llm(test["prompt"], test.get("system"))
        
        results.append({
            "test": test["nombre"],
            "success": result["success"],
            "latency": result.get("latency", 0),
            "tokens": result.get("tokens", 0)
        })
        
        if result["success"]:
            print(f"   ✅ {result['latency']:.2f}s - {result['tokens']} tokens")
        else:
            print(f"   ❌ {result['error']}")
    
    # Resumen
    print("\n" + "="*60)
    print("📈 RESUMEN")
    print("-"*60)
    
    successful = [r for r in results if r["success"]]
    
    if successful:
        avg_latency = sum(r["latency"] for r in successful) / len(successful)
        avg_tokens = sum(r["tokens"] for r in successful) / len(successful)
        
        print(f"Tests exitosos: {len(successful)}/{len(results)}")
        print(f"Latencia promedio: {avg_latency:.2f}s")
        print(f"Tokens promedio: {avg_tokens:.0f}")
    else:
        print("Ningún test fue exitoso.")


def optimization_mode():
    """Prueba diferentes configuraciones para optimizar velocidad"""
    print("\n⚡ MODO OPTIMIZACIÓN")
    print("="*60)
    print("Probando diferentes configuraciones para reducir latencia...")
    print("="*60)
    
    prompt = "Describe un bosque oscuro en 50 palabras."
    
    configs = [
        {
            "nombre": "Base (200 tokens)",
            "config": {
                "temperature": 0.65,
                "num_predict": 200,
                "top_p": 0.9,
                "top_k": 40
            }
        },
        {
            "nombre": "Tokens reducidos (80)",
            "config": {
                "temperature": 0.65,
                "num_predict": 80,
                "top_p": 0.9,
                "top_k": 40
            }
        },
        {
            "nombre": "Tokens mínimos (50)",
            "config": {
                "temperature": 0.65,
                "num_predict": 50,
                "top_p": 0.9,
                "top_k": 40
            }
        },
        {
            "nombre": "Temperatura baja (0.3)",
            "config": {
                "temperature": 0.3,
                "num_predict": 80,
                "top_p": 0.9,
                "top_k": 40
            }
        }
    ]
    
    results = []
    
    for cfg in configs:
        print(f"\n▶️  Probando: {cfg['nombre']}...")
        
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": cfg["config"]
        }
        
        start = time.time()
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            result = response.json()
            latency = time.time() - start
            
            results.append({
                "nombre": cfg["nombre"],
                "latency": latency,
                "tokens": result.get("eval_count", 0),
                "success": True
            })
            
            print(f"   ✅ {latency:.2f}s - {result.get('eval_count', 0)} tokens")
        except Exception as e:
            results.append({
                "nombre": cfg["nombre"],
                "latency": 0,
                "tokens": 0,
                "success": False,
                "error": str(e)
            })
            print(f"   ❌ Error: {e}")
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS")
    print("="*60)
    
    successful = [r for r in results if r["success"]]
    if successful:
        best = min(successful, key=lambda x: x["latency"])
        print(f"\n🏆 Mejor configuración: {best['nombre']}")
        print(f"   Latencia: {best['latency']:.2f}s")
        print(f"   Tokens: {best['tokens']}")
        
        print("\n📋 Ranking por velocidad:")
        for r in sorted(successful, key=lambda x: x["latency"]):
            print(f"   {r['nombre']}: {r['latency']:.2f}s ({r['tokens']} tokens)")
    
    print("\n💡 Recomendaciones:")
    print("   - Menos tokens = más rápido (pero respuestas más cortas)")
    print("   - Temperatura baja = más determinista (puede ser más rápido)")
    print("   - Para RPG: 50-80 tokens suelen ser suficientes")
    print("   - Si tienes GPU, Ollama la usa automáticamente")


def main():
    """Menú principal"""
    print("\n" + "="*60)
    print("🐉 LAST ADVENTURER - Test LLM")
    print("="*60)
    print(f"Modelo: {MODEL}")
    print(f"URL: {OLLAMA_URL}")
    print("="*60)
    
    # Verificar conexión
    print("\n🔍 Verificando conexión con Ollama...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está funcionando!\n")
        else:
            print("⚠️  Ollama respondió con error\n")
    except:
        print("❌ No se puede conectar a Ollama")
        print("   Asegúrate de que esté corriendo: ollama serve\n")
        return
    
    while True:
        print("\n📋 MENÚ")
        print("-"*60)
        print("Tests predefinidos:")
        for key, test in TESTS.items():
            print(f"  {key}. {test['nombre']}")
        print("\nOtras opciones:")
        print("  I. Modo interactivo")
        print("  B. Benchmark (todos los tests)")
        print("  O. Optimización (probar configuraciones)")
        print("  S. Salir")
        print("-"*60)
        
        opcion = input("\nSelecciona una opción: ").strip().upper()
        
        if opcion == "S":
            print("¡Hasta luego!")
            break
        elif opcion == "I":
            interactive_mode()
        elif opcion == "B":
            benchmark_mode()
        elif opcion == "O":
            optimization_mode()
        elif opcion in TESTS:
            run_test(opcion)
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()