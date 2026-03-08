"""
Sistema de Semillas (Seed) para generación procedural determinista.

Cada partida tiene una semilla única que determina TODO el mundo.
Misma semilla = mismo mundo, siempre.
"""

import random
import time
import uuid
from hashlib import sha256
from typing import Optional, Dict


class WorldSeed:
    """
    Generador determinista basado en semilla.
    
    Uso:
        seed = WorldSeed("mi-partida-123")
        bioma_rng = seed.get_rng("biomas")
        enemigo_rng = seed.get_rng("enemigos")
        
        # Siempre mismo resultado con misma semilla
        print(bioma_rng.choice(["bosque", "desierto"]))  # Determinista
    """
    
    def __init__(self, seed_string: Optional[str] = None):
        """
        Inicializa el sistema de semillas.
        
        Args:
            seed_string: String de semilla. Si es None, genera una aleatoria.
        """
        self.master_seed = seed_string or self._generate_seed()
        self._rng = random.Random(self._hash_seed(self.master_seed))
        self._subseed_cache: Dict[str, int] = {}
        self._rng_cache: Dict[str, random.Random] = {}
    
    def _hash_seed(self, seed: str) -> int:
        """Convierte un string a un hash numérico determinista."""
        return int(sha256(seed.encode()).hexdigest(), 16) % (2**32)
    
    def _generate_seed(self) -> str:
        """Genera una semilla aleatoria única."""
        return f"{int(time.time() * 1000)}:{uuid.uuid4()}"
    
    def get_subseed(self, context: str) -> int:
        """
        Genera una sub-seed para un contexto específico.
        
        Args:
            context: Nombre del contexto (ej: "biomas", "enemigos", "zona_5_3")
            
        Returns:
            Hash numérico único para ese contexto
        """
        if context not in self._subseed_cache:
            combined = f"{self.master_seed}:{context}"
            self._subseed_cache[context] = self._hash_seed(combined)
        return self._subseed_cache[context]
    
    def get_rng(self, context: str) -> random.Random:
        """
        Obtiene un RNG independiente para un contexto específico.
        
        Cada contexto tiene su propio RNG que no afecta a otros contextos.
        Esto permite que el sistema sea modular y predecible.
        
        Args:
            context: Nombre del contexto
            
        Returns:
            Instancia de random.Random con semilla única para ese contexto
        """
        if context not in self._rng_cache:
            self._rng_cache[context] = random.Random(self.get_subseed(context))
        return self._rng_cache[context]
    
    def get_int(self, context: str, min_val: int = 0, max_val: int = 100) -> int:
        """Helper rápido para obtener un entero aleatorio."""
        return self.get_rng(context).randint(min_val, max_val)
    
    def get_choice(self, context: str, choices: list) -> any:
        """Helper rápido para elegir de una lista."""
        return self.get_rng(context).choice(choices)
    
    def get_float(self, context: str) -> float:
        """Helper rápido para obtener un float entre 0 y 1."""
        return self.get_rng(context).random()
    
    def get_weighted_choice(self, context: str, choices: list, weights: list) -> any:
        """Helper para elección ponderada."""
        return self.get_rng(context).choices(choices, weights=weights)[0]
    
    def regenerate_context(self, context: str) -> random.Random:
        """
        Regenera el RNG de un contexto (útil para testing).
        
        Args:
            context: Contexto a regenerar
            
        Returns:
            Nuevo RNG para ese contexto
        """
        if context in self._rng_cache:
            del self._rng_cache[context]
        if context in self._subseed_cache:
            del self._subseed_cache[context]
        return self.get_rng(context)
    
    def to_dict(self) -> dict:
        """Serializa la semilla para guardar."""
        return {
            "master_seed": self.master_seed,
            "subseed_cache": self._subseed_cache.copy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WorldSeed':
        """Deserializa una semilla desde dict."""
        instance = cls(data["master_seed"])
        instance._subseed_cache = data.get("subseed_cache", {})
        return instance
    
    def __repr__(self) -> str:
        return f"WorldSeed('{self.master_seed[:20]}...')"
    
    def __str__(self) -> str:
        return self.master_seed


# Instancia global (opcional, para conveniencia)
_global_seed: Optional[WorldSeed] = None


def get_global_seed() -> Optional[WorldSeed]:
    """Obtiene la semilla global actual."""
    return _global_seed


def set_global_seed(seed: WorldSeed) -> None:
    """Establece la semilla global."""
    global _global_seed
    _global_seed = seed


def init_global_seed(seed_string: Optional[str] = None) -> WorldSeed:
    """Inicializa la semilla global y la retorna."""
    global _global_seed
    _global_seed = WorldSeed(seed_string)
    return _global_seed
