from enum import Enum
from typing import Dict, List, Optional, Tuple

class Estacion(Enum):
    PRIMAVERA = "primavera"
    VERANO = "verano"
    OTOÑO = "otoño"
    INVIERNO = "invierno"

class FaseDia(Enum):
    MADRUGADA = "madrugada" # 00-05
    AMANECER = "amanecer"   # 06-07
    DIA = "día"             # 08-17
    ATARDECER = "atardecer" # 18-19
    ANOCHECER = "anochecer" # 20-21
    NOCHE = "noche"         # 22-23

class TimeManager:
    """Gestiona el tiempo del mundo: ticks, horas, días, estaciones y años."""
    
    TICKS_POR_HORA = 60 # 1 tick = 1 minuto de juego
    HORAS_POR_DIA = 24
    DIAS_POR_ESTACION = 30
    ESTACIONES_POR_AÑO = 4

    def __init__(self, tick_inicial: int = 480): # Empieza a las 08:00 (8 * 60)
        self.tick_total = tick_inicial

    @property
    def hora(self) -> int:
        return (self.tick_total // self.TICKS_POR_HORA) % self.HORAS_POR_DIA

    @property
    def minuto(self) -> int:
        return self.tick_total % self.TICKS_POR_HORA

    @property
    def dia_total(self) -> int:
        return self.tick_total // (self.TICKS_POR_HORA * self.HORAS_POR_DIA)

    @property
    def dia_estacion(self) -> int:
        return self.dia_total % self.DIAS_POR_ESTACION + 1

    @property
    def estacion(self) -> Estacion:
        idx = (self.dia_total // self.DIAS_POR_ESTACION) % self.ESTACIONES_POR_AÑO
        return list(Estacion)[idx]

    @property
    def año(self) -> int:
        return self.dia_total // (self.DIAS_POR_ESTACION * self.ESTACIONES_POR_AÑO) + 1

    @property
    def fase_dia(self) -> FaseDia:
        h = self.hora
        if 0 <= h <= 5: return FaseDia.MADRUGADA
        if 6 <= h <= 7: return FaseDia.AMANECER
        if 8 <= h <= 17: return FaseDia.DIA
        if 18 <= h <= 19: return FaseDia.ATARDECER
        if 20 <= h <= 21: return FaseDia.ANOCHECER
        return FaseDia.NOCHE

    def avanzar_minutos(self, minutos: int):
        """Avanza el tiempo una cantidad de minutos."""
        self.tick_total += minutos

    def avanzar_horas(self, horas: int):
        self.avanzar_minutos(horas * self.TICKS_POR_HORA)

    def avanzar_dias(self, dias: int):
        self.avanzar_horas(dias * self.HORAS_POR_DIA)

    def get_formato_hora(self) -> str:
        return f"{self.hora:02d}:{self.minuto:02d}"

    def get_estado_completo(self) -> Dict:
        return {
            "tick_total": self.tick_total,
            "hora": self.get_formato_hora(),
            "fase": self.fase_dia.value,
            "dia": self.dia_estacion,
            "estacion": self.estacion.value,
            "año": self.año,
            "dia_absoluto": self.dia_total
        }

    def to_dict(self) -> Dict:
        return {"tick_total": self.tick_total}

    @classmethod
    def from_dict(cls, data: Dict) -> 'TimeManager':
        return cls(tick_inicial=data.get("tick_total", 480))
