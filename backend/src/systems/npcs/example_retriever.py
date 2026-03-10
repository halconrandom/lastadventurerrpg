"""
ExampleRetriever — Sistema RAG simplificado para ejemplos de dialogo.

Busca ejemplos relevantes basados en:
- Raza del NPC
- Rasgos de personalidad
- Rol
- Tipo de interaccion (saludo, pregunta, queja, etc.)

Principios:
- Maximo 3 ejemplos para no saturar el prompt
- Prioriza coincidencias exactas de rasgos
- Fallback a ejemplos genericos si no hay coincidencias
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class EjemploDialogo:
    """Un ejemplo de dialogo para un tipo de NPC."""
    id: str
    raza: str
    rasgos: List[str]
    rol: str
    tipo_interaccion: str
    accion: str
    dialogo: str
    
    def puntuacion_coincidencia(self, raza: str, rasgos: List[str], rol: str, tipo_interaccion: str) -> int:
        """Calcula que tan bien coincide este ejemplo con los criterios dados."""
        puntuacion = 0
        
        # Coincidencia de raza (peso alto)
        if self.raza == raza or self.raza == "cualquiera":
            puntuacion += 10
        
        # Coincidencia de rasgos (peso muy alto)
        rasgos_lower = [r.lower() for r in rasgos]
        for rasgo in self.rasgos:
            if rasgo.lower() in rasgos_lower:
                puntuacion += 15
        
        # Coincidencia de rol (peso medio)
        if self.rol == rol or self.rol == "cualquiera":
            puntuacion += 5
        
        # Coincidencia de tipo de interaccion (peso alto)
        if self.tipo_interaccion == tipo_interaccion:
            puntuacion += 10
        elif self.tipo_interaccion in ["saludo", "charla"]:  # Tipos genericos
            puntuacion += 3
        
        return puntuacion


class ExampleRetriever:
    """Recupera ejemplos de dialogo relevantes para un NPC."""
    
    def __init__(self, ruta_ejemplos: Optional[str] = None):
        if ruta_ejemplos is None:
            ruta_ejemplos = Path(__file__).parent.parent.parent / "data" / "dialogue_examples.json"
        
        self.ruta = Path(ruta_ejemplos)
        self._datos: Dict = {}
        self._ejemplos: List[EjemploDialogo] = []
        self._cargar()
    
    def _cargar(self) -> None:
        """Carga los ejemplos desde el archivo JSON."""
        try:
            with open(self.ruta, 'r', encoding='utf-8') as f:
                self._datos = json.load(f)
            
            self._ejemplos = [
                EjemploDialogo(
                    id=e["id"],
                    raza=e["raza"],
                    rasgos=e["rasgos"],
                    rol=e["rol"],
                    tipo_interaccion=e["tipo_interaccion"],
                    accion=e["accion"],
                    dialogo=e["dialogo"]
                )
                for e in self._datos.get("ejemplos", [])
            ]
        except FileNotFoundError:
            print(f"[ExampleRetriever] Archivo no encontrado: {self.ruta}")
            self._ejemplos = []
        except json.JSONDecodeError as e:
            print(f"[ExampleRetriever] Error parseando JSON: {e}")
            self._ejemplos = []
    
    def obtener_reglas_absolutas(self) -> List[str]:
        """Retorna las reglas absolutas del sistema."""
        return self._datos.get("reglas_absolutas", [])
    
    def buscar_ejemplos(
        self, 
        raza: str, 
        rasgos: List[str], 
        rol: str, 
        tipo_interaccion: str,
        max_ejemplos: int = 3
    ) -> List[EjemploDialogo]:
        """
        Busca los ejemplos mas relevantes para un NPC dado.
        
        Args:
            raza: Raza del NPC (enano, elfo, humano, orco, etc.)
            rasgos: Lista de rasgos de personalidad
            rol: Rol del NPC (tabernero, mercader, guardia, etc.)
            tipo_interaccion: Tipo de interaccion actual (saludo, pregunta, queja, etc.)
            max_ejemplos: Maximo de ejemplos a retornar
        
        Returns:
            Lista de ejemplos ordenados por relevancia
        """
        if not self._ejemplos:
            return []
        
        # Calcular puntuaciones
        ejemplos_puntuados = [
            (ejemplo, ejemplo.puntuacion_coincidencia(raza, rasgos, rol, tipo_interaccion))
            for ejemplo in self._ejemplos
        ]
        
        # Ordenar por puntuacion descendente
        ejemplos_puntuados.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar los mejores
        return [e[0] for e in ejemplos_puntuados[:max_ejemplos] if e[1] > 0]
    
    def formatear_ejemplos_para_prompt(
        self, 
        ejemplos: List[EjemploDialogo], 
        nombre_npc: str
    ) -> str:
        """
        Formatea los ejemplos para inyectarlos en el prompt del LLM.
        
        Args:
            ejemplos: Lista de ejemplos a formatear
            nombre_npc: Nombre del NPC (para personalizar los ejemplos)
        
        Returns:
            String formateado para el prompt
        """
        if not ejemplos:
            return ""
        
        lineas = ["EJEMPLOS DE COMO HABLA " + nombre_npc.upper() + ":"]
        
        for ejemplo in ejemplos:
            # Reemplazar nombre generico con el nombre del NPC
            accion = ejemplo.accion
            dialogo = ejemplo.dialogo
            lineas.append(f"- {accion} {dialogo}")
        
        return "\n".join(lineas)
    
    def formatear_reglas_para_prompt(self) -> str:
        """Formatea las reglas absolutas para el prompt."""
        reglas = self.obtener_reglas_absolutas()
        if not reglas:
            return ""
        
        return "REGLAS ABSOLUTAS:\n" + "\n".join(f"- {r}" for r in reglas)


# Instancia global para uso facil
_retriever_instance: Optional[ExampleRetriever] = None


def get_example_retriever() -> ExampleRetriever:
    """Obtiene la instancia global del retriever."""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = ExampleRetriever()
    return _retriever_instance
