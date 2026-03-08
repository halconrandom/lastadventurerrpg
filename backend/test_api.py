import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_api():
    print("--- Probando API de Last Adventurer ---")
    
    # 1. Probar nueva partida
    print("\n1. Creando nueva partida...")
    payload = {
        "nombre": "Tester",
        "genero": "masculino",
        "dificultad": "normal"
    }
    r = requests.post(f"{BASE_URL}/partida/nueva", json=payload)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(json.dumps(data, indent=2))
    
    if not data.get("success"):
        print("Error al crear partida")
        return
    
    slot = data["data"]["slot"]
    
    # 2. Verificar compatibilidad de stats
    print("\n2. Verificando stats del personaje...")
    personaje = data["data"]["datos"]["personaje"]
    stats = personaje["stats"]
    
    campos_esperados = ["hp", "hp_max", "ataque", "defensa", "velocidad", "experiencia_necesaria", "puntos_distribuibles"]
    for campo in campos_esperados:
        if campo in stats:
            print(f"✅ Campo '{campo}' presente: {stats[campo]}")
        else:
            print(f"❌ Campo '{campo}' FALTANTE")

    # 3. Probar exploración
    print("\n3. Probando exploración...")
    r = requests.post(f"{BASE_URL}/juego/explorar", json={"slot": slot})
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error de conexión: {e}")
