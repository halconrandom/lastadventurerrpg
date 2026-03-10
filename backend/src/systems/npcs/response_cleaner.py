"""
ResponseCleaner — Limpia respuestas del LLM.

Elimina:
- Exageraciones (ojos desorbitados, contorsionado, etc.)
- Respuestas demasiado largas
- Múltiples acciones en una respuesta
- Primera persona en acciones
"""

import re
from typing import Optional


# Patrones de exageración a eliminar o simplificar
EXAGERACIONES = {
    # Físicas exageradas
    r"ojos desorbitados": "mirada intensa",
    r"contorsionado por la ira": "frunce el ceño",
    r"se contorsiona": "se tensa",
    r"grita con furia": "dice con dureza",
    r"se eleva al punto de casi un grito": "dice con firmeza",
    r"voz se eleva en un grito": "dice con dureza",
    r"desprecio sin límites": "desprecio",
    r"furia descontrolada": "ira",
    r"ira descontrolada": "ira",
    r"desesperación y furia": "frustración",
    r"desesperada y furiosa": "alterada",
    
    # Acciones múltiples (detectar y simplificar)
    r"\*[^*]+\*[^*]*\*[^*]+\*": None,  # Dos acciones -> mantener solo la primera
    
    # Primera persona en acciones
    r"\*miro": "*{nombre} mira",
    r"\*me acerco": "*{nombre} se acerca",
    r"\*me pongo": "*{nombre} se pone",
    r"\*digo": None,  # Eliminar, el diálogo ya lo dice
}

# Palabras prohibidas que indican exageración
PALABRAS_PROHIBIDAS = [
    "desorbitados",
    "contorsionado",
    "contorsiona",
    "descontrolada",
    "sin límites",
    "casi un grito",
    "en un grito",
    "se eleva",
]


class ResponseCleaner:
    """Limpia respuestas del LLM para hacerlas más naturales."""
    
    def __init__(self):
        self.palabras_prohibidas = PALABRAS_PROHIBIDAS
        self.exageraciones = EXAGERACIONES
    
    def limpiar(self, respuesta: str, nombre_npc: str = "NPC") -> str:
        """
        Limpia la respuesta del LLM.
        
        Args:
            respuesta: Texto crudo del LLM
            nombre_npc: Nombre del NPC para reemplazar primera persona
        
        Returns:
            Respuesta limpia
        """
        if not respuesta:
            return respuesta
        
        texto = respuesta.strip()
        original = texto
        
        # 1. Eliminar prefijos comunes del LLM
        texto = self._eliminar_prefijos(texto)
        
        # 2. Corregir primera persona en acciones
        texto = self._corregir_primera_persona(texto, nombre_npc)
        
        # 3. Simplificar exageraciones
        texto = self._simplificar_exageraciones(texto)
        
        # 4. Limitar longitud (máximo 2 oraciones de diálogo)
        texto = self._limitar_longitud(texto)
        
        # 5. Si hay múltiples acciones, mantener solo la primera
        texto = self._una_accion(texto)
        
        # 6. Limpiar espacios y caracteres extra
        texto = self._limpiar_espacios(texto)
        
        return texto
    
    def _eliminar_prefijos(self, texto: str) -> str:
        """Elimina prefijos como 'Dorian Xavier:', 'Respuesta:', etc."""
        patrones = [
            r"^[A-Z][a-z]+ [A-Z][a-z]+:\s*",
            r"^Respuesta:\s*",
            r"^Diálogo:\s*",
            r"^\*\*[^*]+\*\*:\s*",
        ]
        for patron in patrones:
            texto = re.sub(patron, "", texto)
        return texto
    
    def _corregir_primera_persona(self, texto: str, nombre: str) -> str:
        """Corrige acciones en primera persona."""
        reemplazos = [
            (r"\*miro\b", f"*{nombre} mira"),
            (r"\*me acerco\b", f"*{nombre} se acerca"),
            (r"\*me pongo\b", f"*{nombre} se pone"),
            (r"\*me llevo\b", f"*{nombre} se lleva"),
            (r"\*me giro\b", f"*{nombre} se gira"),
            (r"\*digo\b", ""),  # Eliminar
        ]
        for patron, reemplazo in reemplazos:
            texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
        return texto
    
    def _simplificar_exageraciones(self, texto: str) -> str:
        """Simplifica expresiones exageradas."""
        for patron, reemplazo in self.exageraciones.items():
            if reemplazo:
                texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
            else:
                texto = re.sub(patron, "", texto, flags=re.IGNORECASE)
        return texto
    
    def _limitar_longitud(self, texto: str) -> str:
        """Limita la respuesta a máximo 2 oraciones de diálogo."""
        # Separar acción y diálogo
        match = re.match(r"(\*[^*]+\*)\s*(.+)", texto)
        if not match:
            return texto
        
        accion = match.group(1)
        dialogo = match.group(2)
        
        # Dividir en oraciones
        oraciones = re.split(r'[.!?]+', dialogo)
        oraciones = [o.strip() for o in oraciones if o.strip()]
        
        # Mantener máximo 2 oraciones
        if len(oraciones) > 2:
            dialogo = ". ".join(oraciones[:2]) + "."
        
        return f"{accion} {dialogo}"
    
    def _una_accion(self, texto: str) -> str:
        """Asegura que solo haya una acción."""
        # Buscar todas las acciones entre asteriscos
        acciones = re.findall(r"\*[^*]+\*", texto)
        if len(acciones) <= 1:
            return texto
        
        # Mantener solo la primera acción
        primera_accion = acciones[0]
        resto = re.sub(r"\*[^*]+\*", "", texto, count=1).strip()
        
        return f"{primera_accion} {resto}"
    
    def _limpiar_espacios(self, texto: str) -> str:
        """Limpia espacios y caracteres extra."""
        # Espacios múltiples
        texto = re.sub(r"\s+", " ", texto)
        # Espacios antes de puntuación
        texto = re.sub(r"\s+([.,!?])", r"\1", texto)
        # Espacios después de asteriscos
        texto = re.sub(r"\*\s+", "* ", texto)
        return texto.strip()
    
    def validar(self, respuesta: str) -> bool:
        """
        Valida si una respuesta es aceptable.
        
        Returns:
            True si la respuesta no contiene exageraciones
        """
        texto_lower = respuesta.lower()
        for palabra in self.palabras_prohibidas:
            if palabra.lower() in texto_lower:
                return False
        return True


# Instancia global
_cleaner_instance: Optional[ResponseCleaner] = None


def get_response_cleaner() -> ResponseCleaner:
    """Obtiene la instancia global del limpiador."""
    global _cleaner_instance
    if _cleaner_instance is None:
        _cleaner_instance = ResponseCleaner()
    return _cleaner_instance