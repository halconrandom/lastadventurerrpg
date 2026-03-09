# Sistema LLM - Last Adventurer

## Descripción
Sistema de generación de narrativa procedural usando Llama 3.2 3B con fine-tuning mediante LoRA, hosteado en VPS propia.

---

## Stack Tecnológico

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| Modelo Base | Llama 3.2 3B | Generación de texto |
| Serving | Ollama o vLLM | Servir el modelo via API |
| Fine-tuning | LoRA adapters | Especialización en RPG |
| Backend | Python + FastAPI | Integración con el juego |
| Fallback | Error + Pausa | Cuando LLM no disponible |

---

## Requisitos de Hardware

### Mínimo (para desarrollo)
- **RAM**: 8 GB
- **VRAM**: 6 GB (si hay GPU)
- **Almacenamiento**: 10 GB
- **CPU**: 4 cores

### Recomendado (producción VPS)
- **RAM**: 16 GB
- **VRAM**: 8-12 GB (GPU dedicada)
- **Almacenamiento**: 20 GB SSD
- **CPU**: 8 cores

---

## Instalación

### Opción A: Ollama (Recomendado para empezar)

#### 1. Instalar Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Descargar desde: https://ollama.com/download

#### 2. Descargar Llama 3.2 3B

```bash
ollama pull llama3.2:3b
```

#### 3. Verificar instalación

```bash
ollama list
ollama run llama3.2:3b
```

#### 4. Probar API

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Eres un narrador de RPG. Describe un bosque oscuro:",
  "stream": false
}'
```

---

### Opción B: vLLM (Mayor control, producción)

#### 1. Instalar dependencias

```bash
pip install vllm torch
```

#### 2. Descargar modelo

```python
from vllm import LLM

llm = LLM(model="meta-llama/Llama-3.2-3B")
```

#### 3. Servir modelo

```bash
python -m vllm.entrypoints.api_server \
    --model meta-llama/Llama-3.2-3B \
    --host 0.0.0.0 \
    --port 8000
```

---

## Configuración para RPG

### Parámetros del Modelo

```python
LLM_CONFIG = {
    "model": "llama3.2:3b",
    "temperature": 0.65,        # Media creatividad
    "top_p": 0.9,               # Nucleus sampling
    "top_k": 50,                # Top-k sampling
    "max_tokens": 256,           # Máximo tokens por respuesta
    "repeat_penalty": 1.1,      # Evitar repetición
    "stop": ["\n\n", "JUGADOR:", "---"]  # Stop tokens
}
```

### Prompt Template

```python
SYSTEM_PROMPT = """Eres el narrador de un RPG de fantasía oscura con toques de D&D. Tu tono es inmersivo, atmosférico y misterioso. 

Reglas:
- Nunca des información que el jugador no haya descubierto
- Describe ambientes con detalles sensoriales
- Mantén el misterio y la tensión
- No hables en primera persona
- Máximo 150 palabras por descripción
- Termina con algo que invite a la acción"""

def build_prompt(context: dict) -> str:
    """Construye el prompt con contexto del juego"""
    
    historial = context.get("historial_reciente", [])
    zona = context.get("zona", "desconocida")
    estado = context.get("estado_jugador", {})
    tipo = context.get("tipo_evento", "exploracion")
    
    prompt = f"""Contexto:
- Zona actual: {zona}
- Estado del jugador: HP {estado.get('hp', 100)}/{estado.get('hp_max', 100)}, Nivel {estado.get('nivel', 1)}
- Eventos recientes: {', '.join(historial[-3:]) if historial else 'Ninguno'}

Tipo de generación: {tipo}

Genera una descripción de {tipo} para esta situación."""
    
    return prompt
```

---

## Integración con Backend

### Cliente LLM

```python
# backend/src/llm/client.py

import httpx
from typing import Optional
import json

class LLMClient:
    """Cliente para comunicarse con Ollama/vLLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
        self.available = False
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """Verifica si el servidor LLM está disponible"""
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            self.available = response.status_code == 200
            return self.available
        except:
            self.available = False
            return False
    
    def generate(
        self, 
        prompt: str, 
        system: str = None,
        temperature: float = 0.65,
        max_tokens: int = 256
    ) -> dict:
        """Genera texto usando el modelo"""
        
        if not self.available:
            raise LLMNotAvailableError("El servidor LLM no está disponible")
        
        payload = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": 0.9,
                "top_k": 50,
                "repeat_penalty": 1.1
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise LLMGenerationError(f"Error generando texto: {e}")
    
    def generate_narrative(
        self, 
        context: dict, 
        tipo: str = "exploracion"
    ) -> str:
        """Genera narrativa específica del juego"""
        
        prompt = self._build_game_prompt(context, tipo)
        system = SYSTEM_PROMPT
        
        result = self.generate(prompt, system)
        return result.get("response", "")
    
    def _build_game_prompt(self, context: dict, tipo: str) -> str:
        """Construye prompt específico para el juego"""
        
        templates = {
            "exploracion": "Describe lo que el jugador ve y siente al explorar esta zona.",
            "combate_inicio": "Describe el inicio del combate con el enemigo.",
            "combate_accion": "Describe la acción de combate que realiza el jugador.",
            "combate_victoria": "Describe la victoria del jugador sobre el enemigo.",
            "combate_derrota": "Describe la derrota del jugador.",
            "npc_dialogo": "Genera el diálogo del NPC basado en su personalidad.",
            "descubrimiento": "Describe el hallazgo del jugador.",
            "evento": "Describe el evento que ocurre.",
            "transicion": "Describe la transición entre zonas."
        }
        
        base_prompt = templates.get(tipo, templates["exploracion"])
        
        # Añadir contexto
        zona = context.get("zona", "zona desconocida")
        estado = context.get("estado_jugador", {})
        historial = context.get("historial_reciente", [])
        
        prompt = f"""{base_prompt}

Contexto del juego:
- Zona: {zona}
- Estado: HP {estado.get('hp', 100)}/{estado.get('hp_max', 100)}
- Eventos recientes: {', '.join(historial[-3:]) if historial else 'Ninguno'}
- Tono: D&D con toques oscuros

Genera la narrativa:"""
        
        return prompt


class LLMNotAvailableError(Exception):
    """Error cuando el LLM no está disponible"""
    pass


class LLMGenerationError(Exception):
    """Error durante la generación"""
    pass


# Instancia global
llm_client = LLMClient()
```

### Manejo de Errores

```python
# backend/src/llm/handler.py

from .client import llm_client, LLMNotAvailableError

async def generate_narrative_safe(context: dict, tipo: str) -> dict:
    """Genera narrativa con manejo de errores"""
    
    try:
        if not llm_client.available:
            return {
                "success": False,
                "error": "LLM_NO_DISPONIBLE",
                "message": "El servidor de narrativa no está disponible. El juego se pausará.",
                "action": "PAUSAR_JUEGO"
            }
        
        narrative = llm_client.generate_narrative(context, tipo)
        
        return {
            "success": True,
            "narrative": narrative,
            "tokens_used": len(narrative.split())  # Aproximación
        }
    
    except LLMNotAvailableError:
        return {
            "success": False,
            "error": "LLM_NO_DISPONIBLE",
            "message": "El servidor de narrativa no está disponible.",
            "action": "PAUSAR_JUEGO"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": "ERROR_GENERACION",
            "message": f"Error generando narrativa: {str(e)}",
            "action": "REINTENTAR"
        }
```

### Endpoint API

```python
# backend/src/api/narrativa.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..llm.handler import generate_narrative_safe

router = APIRouter(prefix="/api/narrativa", tags=["narrativa"])

class NarrativeRequest(BaseModel):
    context: dict
    tipo: str = "exploracion"

class NarrativeResponse(BaseModel):
    success: bool
    narrative: str = None
    error: str = None
    message: str = None
    action: str = None

@router.post("/generar", response_model=NarrativeResponse)
async def generar_narrativa(request: NarrativeRequest):
    """Genera narrativa usando LLM"""
    
    result = await generate_narrative_safe(request.context, request.tipo)
    
    if not result["success"]:
        if result.get("action") == "PAUSAR_JUEGO":
            # El frontend debe mostrar error y pausar
            return NarrativeResponse(**result)
        else:
            raise HTTPException(status_code=503, detail=result["message"])
    
    return NarrativeResponse(
        success=True,
        narrative=result["narrative"]
    )

@router.get("/status")
async def verificar_llm():
    """Verifica estado del servidor LLM"""
    
    from ..llm.client import llm_client
    
    return {
        "available": llm_client.available,
        "model": "llama3.2:3b" if llm_client.available else None
    }
```

---

## Fine-Tuning con LoRA

### Preparar Dataset

```python
# scripts/prepare_dataset.py

import json

def create_training_data():
    """Crea dataset de entrenamiento para fine-tuning"""
    
    training_examples = [
        # Exploraciones
        {
            "instruction": "Genera una descripción de exploración para un bosque oscuro.",
            "input": {"zona": "bosque_somrio", "estado": "herido_leve"},
            "output": "Los árboles se ciernen sobre ti como guardianes silenciosos. La luz apenas filtra entre las ramas retorcidas, y el olor a humedad te recuerda que no estás solo aquí. Un crujido entre los arbustos..."
        },
        # Combates
        {
            "instruction": "Describe el inicio de un combate con un lobo.",
            "input": {"enemigo": "lobo_somrio", "zona": "bosque"},
            "output": "Un par de ojos amarillos te observan desde las sombras. El lobo emerge lentamente, sus colmillos brillan bajo la escasa luz. Un gruñido grave hace vibrar el aire. No hay escape."
        },
        # NPCs
        {
            "instruction": "Genera el saludo de un tabernero desconfiado.",
            "input": {"npc": "tabernero", "relacion": "neutral", "zona": "taberna"},
            "output": "El tabernero te mira de arriba a abajo mientras limpia un vaso con un trapo sucio. '¿Qué quieres, forastero?' Su tono no invita a la conversación, pero sus ojos evalúan tu bolsa de monedas."
        },
        # Más ejemplos...
    ]
    
    # Guardar en formato para entrenamiento
    with open("training_data.jsonl", "w", encoding="utf-8") as f:
        for example in training_examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    create_training_data()
```

### Entrenar LoRA

```bash
# Instalar dependencias
pip install peft transformers datasets

# Script de entrenamiento
python scripts/train_lora.py \
    --model meta-llama/Llama-3.2-3B \
    --data training_data.jsonl \
    --output ./lora_adapters \
    --epochs 3 \
    --lr 1e-4
```

### Usar LoRA en Producción

```python
# backend/src/llm/lora_loader.py

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model_with_lora():
    """Carga modelo base con adaptador LoRA"""
    
    # Cargar modelo base
    base_model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.2-3B",
        device_map="auto"
    )
    
    # Cargar adaptador LoRA
    model = PeftModel.from_pretrained(
        base_model,
        "./lora_adapters"
    )
    
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B")
    
    return model, tokenizer
```

---

## Monitoreo y Logs

### Logs de Uso

```python
# backend/src/llm/logger.py

import logging
from datetime import datetime

logging.basicConfig(
    filename='logs/llm_usage.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_llm_call(prompt: str, response: str, tokens: int, latency: float):
    """Registra llamadas al LLM"""
    logging.info(f"""
    CALL:
    - Prompt length: {len(prompt)}
    - Response length: {len(response)}
    - Tokens: {tokens}
    - Latency: {latency:.2f}s
    - Timestamp: {datetime.now().isoformat()}
    """)
```

---

## Checklist de Instalación

- [ ] Instalar Ollama o vLLM
- [ ] Descargar Llama 3.2 3B
- [ ] Verificar API funcionando
- [ ] Configurar parámetros del modelo
- [ ] Crear cliente LLM en backend
- [ ] Implementar manejo de errores
- [ ] Crear endpoint de narrativa
- [ ] Preparar dataset de entrenamiento
- [ ] Entrenar LoRA (opcional)
- [ ] Configurar logs
- [ ] Probar integración completa

---

## Comandos Útiles

```bash
# Ver modelos instalados
ollama list

# Probar modelo
ollama run llama3.2:3b

# Ver logs
tail -f logs/llm_usage.log

# Verificar API
curl http://localhost:11434/api/tags

# Reiniciar Ollama
ollama serve
```

---

## Próximos Pasos

1. Instalar Ollama en VPS
2. Descargar Llama 3.2 3B
3. Probar generación básica
4. Integrar con backend
5. Crear dataset de entrenamiento
6. Entrenar LoRA
7. Optimizar parámetros