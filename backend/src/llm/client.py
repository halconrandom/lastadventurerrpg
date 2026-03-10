import requests
import json
import time
import os
from typing import Optional, Dict, Any

# Configuración por defecto (puede sobreescribirse con env vars)
DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "dolphin3")

class LLMClient:
    """Cliente para interactuar con Ollama o APIs remotas de LLM."""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or DEFAULT_OLLAMA_URL
        self.model = model or DEFAULT_MODEL
        self.timeout = 60  # Aumentado para modelos más grandes
        self.is_available = True
        print(f"[LLMClient] Modelo: {self.model}, URL: {self.base_url}")

    def generar(self, prompt: str, system_prompt: Optional[str] = None, stream: bool = False) -> Optional[str]:
        """Genera una respuesta del LLM."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            if stream:
                # Manejo de stream no implementado por ahora para simplicidad
                return None
            
            data = response.json()
            self.is_available = True
            return data.get("response", "").strip()

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error en LLMClient: {str(e)}")
            self.is_available = False
            return None

    def chat(self, messages: list, stream: bool = False) -> Optional[str]:
        """Interfaz de chat para el LLM."""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            self.is_available = True
            return data.get("message", {}).get("content", "").strip()

        except Exception as e:
            print(f"Error en LLMClient (chat): {str(e)}")
            self.is_available = False
            return None

    def check_health(self) -> bool:
        """Verifica si el servicio de LLM está activo."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            self.is_available = response.status_code == 200
            return self.is_available
        except:
            self.is_available = False
            return False
