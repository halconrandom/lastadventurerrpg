"""
Sistema de eventos de exploracion.

Eventos aleatorios que ocurren durante la exploracion:
- Encuentros con NPCs
- Descubrimientos
- Peligros naturales
- Eventos con elecciones
- Recompensas y consecuencias
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from .seed import WorldSeed
from .biomas import Bioma
from .nombres import NombreGenerator


@dataclass
class OpcionEvento:
    """Opcion de respuesta a un evento."""
    texto: str
    resultado_tipo: str  # "exito", "fallo", "neutral"
    resultado_texto: str
    recompensa: Optional[Dict] = None
    consecuencia: Optional[Dict] = None


@dataclass
class Evento:
    """Representa un evento de exploracion."""
    id: str
    tipo: str
    titulo: str
    descripcion: str
    opciones: List[OpcionEvento]
    biomas: List[str]  # Biomas donde puede aparecer, vacio = todos
    rareza: str  # "comun", "raro", "epico", "legendario"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "opciones": [
                {
                    "texto": o.texto,
                    "resultado_tipo": o.resultado_tipo,
                    "resultado_texto": o.resultado_texto,
                    "recompensa": o.recompensa,
                    "consecuencia": o.consecuencia
                }
                for o in self.opciones
            ],
            "biomas": self.biomas,
            "rareza": self.rareza
        }


class EventoGenerator:
    """Generador de eventos de exploracion."""
    
    # Eventos base por tipo
    EVENTOS_BASE = [
        # === ENCUENTROS CON NPCs ===
        Evento(
            id="viajero_perdido",
            tipo="encuentro_npc",
            titulo="Viajero Perdido",
            descripcion="Un viajero agotado aparece en tu camino. Sus ropas estan rasgadas y su mirada es de desesperacion.",
            opciones=[
                OpcionEvento(
                    texto="Ofrecer agua y comida",
                    resultado_tipo="exito",
                    resultado_texto="El viajero agradece tu bondad. Antes de partir, te entrega un mapa antiguo.",
                    recompensa={"item": "mapa_antiguo", "exp": 10}
                ),
                OpcionEvento(
                    texto="Ignorarlo y continuar",
                    resultado_tipo="neutral",
                    resultado_texto="El viajero te mira con tristeza antes de desaparecer entre los arboles.",
                    consecuencia=None
                ),
                OpcionEvento(
                    texto="Robarle sus pertenencias",
                    resultado_tipo="fallo",
                    resultado_texto="El viajero grita pidiendo ayuda. Un grupo de guardias aparece y te multan.",
                    consecuencia={"oro": -50, "reputacion": -10}
                )
            ],
            biomas=[],
            rareza="comun"
        ),
        
        Evento(
            id="mercader_ambulante",
            tipo="encuentro_npc",
            titulo="Mercader Ambulante",
            descripcion="Un mercader con una carreta llena de objetos curiosos te saluda amablemente.",
            opciones=[
                OpcionEvento(
                    texto="Comprar objetos raros (50 oro)",
                    resultado_tipo="exito",
                    resultado_texto="El mercader te vende un objeto misterioso que brilla con luz propia.",
                    recompensa={"item": "objeto_misterioso", "oro": -50}
                ),
                OpcionEvento(
                    texto="Pedir informacion gratis",
                    resultado_tipo="neutral",
                    resultado_texto="El mercader te cuenta rumores sobre un tesoro cercano.",
                    recompensa={"info": "tesoro_cercano"}
                ),
                OpcionEvento(
                    texto="Negar el saludo",
                    resultado_tipo="neutral",
                    resultado_texto="El mercader se encoge de hombros y continua su camino.",
                    consecuencia=None
                )
            ],
            biomas=[],
            rareza="comun"
        ),
        
        # === DESCUBRIMIENTOS ===
        Evento(
            id="ruinas_antiguas",
            tipo="descubrimiento",
            titulo="Ruinas Antiguas",
            descripcion="Entre la vegetacion descubres los restos de una estructura antigua. Simbolos extraños adornan las piedras.",
            opciones=[
                OpcionEvento(
                    texto="Explorar las ruinas",
                    resultado_tipo="exito",
                    resultado_texto="Encuentras una camara oculta con un cofre sellado.",
                    recompensa={"oro": 100, "item": "artefacto_antiguo", "exp": 25}
                ),
                OpcionEvento(
                    texto="Estudiar los simbolos",
                    resultado_tipo="exito",
                    resultado_texto="Los simbolos revelan conocimientos arcanos olvidados.",
                    recompensa={"exp": 50, "habilidad": "conocimiento_antiguo"}
                ),
                OpcionEvento(
                    texto="Marcar la ubicacion y continuar",
                    resultado_tipo="neutral",
                    resultado_texto="Anotas la ubicacion en tu mapa para explorar mas tarde.",
                    recompensa={"mapa": "ruinas_marcadas"}
                )
            ],
            biomas=["bosque_ancestral", "paramo_marchito", "ruinas_subterraneas"],
            rareza="raro"
        ),
        
        Evento(
            id="fuente_curativa",
            tipo="descubrimiento",
            titulo="Fuente Curativa",
            descripcion="Una fuente de agua cristalina brota de las rocas. El agua emite un brillo suave.",
            opciones=[
                OpcionEvento(
                    texto="Beber del agua",
                    resultado_tipo="exito",
                    resultado_texto="El agua te revitaliza completamente.",
                    recompensa={"vida": 100, "mana": 100}
                ),
                OpcionEvento(
                    texto="Llenar cantimplora",
                    resultado_tipo="exito",
                    resultado_texto="Guardas agua bendita en tu cantimplora.",
                    recompensa={"item": "agua_bendita", "cantidad": 3}
                ),
                OpcionEvento(
                    texto="Investigar la fuente",
                    resultado_tipo="exito",
                    resultado_texto="Descubres que la fuente esta consagrada a un dios antiguo.",
                    recompensa={"exp": 30, "bendicion": "proteccion_menor"}
                )
            ],
            biomas=[],
            rareza="raro"
        ),
        
        # === PELIGROS NATURALES ===
        Evento(
            id="tormenta_repentina",
            tipo="peligro",
            titulo="Tormenta Repentina",
            descripcion="El cielo se oscurece rapidamente. Una tormenta violenta esta por comenzar.",
            opciones=[
                OpcionEvento(
                    texto="Buscar refugio",
                    resultado_tipo="exito",
                    resultado_texto="Encuentras una cueva seca y esperas a que pase la tormenta.",
                    recompensa=None
                ),
                OpcionEvento(
                    texto="Continuar caminando",
                    resultado_tipo="fallo",
                    resultado_texto="La tormenta te golpea con fuerza. Pierdes objetos y energia.",
                    consecuencia={"vida": -20, "item_perdido": True}
                ),
                OpcionEvento(
                    texto="Usar magia para protegerte",
                    resultado_tipo="exito",
                    resultado_texto="Tu magia te protege de la tormenta.",
                    recompensa={"exp": 15},
                    consecuencia={"mana": -30}
                )
            ],
            biomas=[],
            rareza="comun"
        ),
        
        Evento(
            id="terreno_peligroso",
            tipo="peligro",
            titulo="Terreno Peligroso",
            descripcion="El camino se vuelve traicionero. Arenas movedizas y grietas amenazan cada paso.",
            opciones=[
                OpcionEvento(
                    texto="Proceder con cuidado",
                    resultado_tipo="exito",
                    resultado_texto="Avanzas lentamente pero de forma segura.",
                    recompensa={"exp": 10}
                ),
                OpcionEvento(
                    texto="Buscar un camino alternativo",
                    resultado_tipo="neutral",
                    resultado_texto="Das un rodeo largo pero evitas el peligro.",
                    consecuencia={"tiempo": 2}
                ),
                OpcionEvento(
                    texto="Arriesgarse a cruzar rapido",
                    resultado_tipo="fallo",
                    resultado_texto="Tu pie queda atrapado. Logras liberarte pero te lastimas.",
                    consecuencia={"vida": -15, "tiempo": 1}
                )
            ],
            biomas=["pantano_sombrio", "montanas_heladas", "desierto_ceniza"],
            rareza="comun"
        ),
        
        # === EVENTOS MISTICOS ===
        Evento(
            id="portal_dimensional",
            tipo="mistico",
            titulo="Portal Dimensional",
            descripcion="Un portal de luz pulsante aparece frente a ti. Emite un zumbido hipnotico.",
            opciones=[
                OpcionEvento(
                    texto="Atravesar el portal",
                    resultado_tipo="exito",
                    resultado_texto="El portal te transporta a una camara llena de tesoros.",
                    recompensa={"oro": 200, "item": "gema_dimensional", "exp": 50}
                ),
                OpcionEvento(
                    texto="Estudiar el portal",
                    resultado_tipo="exito",
                    resultado_texto="Aprendes sobre la naturaleza de los portales.",
                    recompensa={"exp": 40, "habilidad": "conocimiento_portales"}
                ),
                OpcionEvento(
                    texto="Cerrar el portal",
                    resultado_tipo="neutral",
                    resultado_texto="El portal se cierra, pero algo escapa de el.",
                    consecuencia={"enemigo": "sombra_dimensional"}
                )
            ],
            biomas=["ruinas_subterraneas", "desierto_ceniza"],
            rareza="epico"
        ),
        
        Evento(
            id="arbol_sagrado",
            tipo="mistico",
            titulo="Arbol Sagrado",
            descripcion="Un arbol gigantesco emite una luz dorada. Sus raices parecen respirar.",
            opciones=[
                OpcionEvento(
                    texto="Meditar bajo el arbol",
                    resultado_tipo="exito",
                    resultado_texto="El arbol te bendice con su sabiduria ancestral.",
                    recompensa={"bendicion": "sabiduria_ancestral", "exp": 60}
                ),
                OpcionEvento(
                    texto="Tomar una hoja sagrada",
                    resultado_tipo="fallo",
                    resultado_texto="El arbol se enfurece. Sus ramas te golpean.",
                    consecuencia={"vida": -30, "maldicion": "ira_naturaleza"}
                ),
                OpcionEvento(
                    texto="Dejar una ofrenda",
                    resultado_tipo="exito",
                    resultado_texto="El arbol acepta tu ofrenda y te protege.",
                    recompensa={"bendicion": "proteccion_naturaleza"},
                    consecuencia={"oro": -10}
                )
            ],
            biomas=["bosque_ancestral"],
            rareza="epico"
        ),
        
        # === TESOROS ===
        Evento(
            id="cofe_enterrado",
            tipo="tesoro",
            titulo="Cofre Enterrado",
            descripcion="Tu pie golpea algo duro bajo la tierra. Un cofre viejo asoma entre la tierra.",
            opciones=[
                OpcionEvento(
                    texto="Abrir el cofre",
                    resultado_tipo="exito",
                    resultado_texto="El cofre contiene monedas antiguas y una gema.",
                    recompensa={"oro": 75, "item": "gema_menor"}
                ),
                OpcionEvento(
                    texto="Revisar si hay trampas",
                    resultado_tipo="exito",
                    resultado_texto="Encuentras y desactivas una trampa antes de abrir el cofre.",
                    recompensa={"oro": 75, "item": "gema_mayor", "exp": 15}
                ),
                OpcionEvento(
                    texto="Dejarlo como esta",
                    resultado_tipo="neutral",
                    resultado_texto="Decides no arriesgarte y continuras tu camino.",
                    consecuencia=None
                )
            ],
            biomas=[],
            rareza="comun"
        ),
        
        Evento(
            id="tesoro_guardado",
            tipo="tesoro",
            titulo="Tesoro Guardado",
            descripcion="Un tesoro brilla en la distancia, pero un guardian espectral lo protege.",
            opciones=[
                OpcionEvento(
                    texto="Enfrentar al guardian",
                    resultado_tipo="exito",
                    resultado_texto="Derrotas al guardian y reclamas el tesoro.",
                    recompensa={"oro": 300, "item": "arma_legendaria", "exp": 100}
                ),
                OpcionEvento(
                    texto="Negar el tesoro",
                    resultado_tipo="neutral",
                    resultado_texto="El guardian asiente y desaparece.",
                    recompensa={"exp": 20}
                ),
                OpcionEvento(
                    texto="Intentar robarlo",
                    resultado_tipo="fallo",
                    resultado_texto="El guardian te detecta y te ataca por la espalda.",
                    consecuencia={"vida": -40, "maldicion": "marca_ladron"}
                )
            ],
            biomas=["paramo_marchito", "ruinas_subterraneas"],
            rareza="legendario"
        ),
    ]
    
    # Probabilidades por rareza
    PROBABILIDADES_RAREZA = {
        "comun": 0.60,
        "raro": 0.25,
        "epico": 0.12,
        "legendario": 0.03
    }
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
        self.nombre_gen = NombreGenerator(seed)
    
    def generar_evento(
        self,
        contexto: str,
        bioma_key: Optional[str] = None
    ) -> Optional[Evento]:
        """
        Genera un evento aleatorio apropiado para el contexto.
        
        Args:
            contexto: Contexto para el RNG
            bioma_key: Key del bioma actual (para filtrar eventos)
            
        Returns:
            Evento generado o None
        """
        rng = self.seed.get_rng(f"evento_{contexto}")
        
        # Determinar rareza
        rareza = self._determinar_rareza(rng)
        
        # Filtrar eventos por bioma y rareza
        eventos_disponibles = self._filtrar_eventos(bioma_key, rareza)
        
        if not eventos_disponibles:
            return None
        
        return rng.choice(eventos_disponibles)
    
    def _determinar_rareza(self, rng) -> str:
        """Determina la rareza del evento basado en probabilidades."""
        roll = rng.random()
        
        acumulado = 0
        for rareza, prob in self.PROBABILIDADES_RAREZA.items():
            acumulado += prob
            if roll <= acumulado:
                return rareza
        
        return "comun"
    
    def _filtrar_eventos(
        self,
        bioma_key: Optional[str],
        rareza: str
    ) -> List[Evento]:
        """Filtra eventos por bioma y rareza."""
        eventos = []
        
        for evento in self.EVENTOS_BASE:
            # Filtrar por rareza
            if evento.rareza != rareza:
                continue
            
            # Filtrar por bioma
            if bioma_key and evento.biomas:
                if bioma_key not in evento.biomas:
                    continue
            
            eventos.append(evento)
        
        # Si no hay eventos de la rareza exacta, usar comunes
        if not eventos and rareza != "comun":
            return self._filtrar_eventos(bioma_key, "comun")
        
        return eventos
    
    def resolver_evento(
        self,
        evento: Evento,
        opcion_idx: int,
        contexto: str
    ) -> Dict[str, Any]:
        """
        Resuelve un evento basado en la opcion elegida.
        
        Args:
            evento: Evento a resolver
            opcion_idx: Indice de la opcion elegida
            contexto: Contexto para RNG adicional
            
        Returns:
            Diccionario con resultados
        """
        if opcion_idx < 0 or opcion_idx >= len(evento.opciones):
            return {"error": "Opcion invalida"}
        
        opcion = evento.opciones[opcion_idx]
        
        resultado = {
            "evento_id": evento.id,
            "opcion_elegida": opcion_idx,
            "tipo_resultado": opcion.resultado_tipo,
            "texto_resultado": opcion.resultado_texto,
            "recompensa": opcion.recompensa,
            "consecuencia": opcion.consecuencia
        }
        
        return resultado
    
    def get_evento_by_id(self, evento_id: str) -> Optional[Evento]:
        """Obtiene un evento por su ID."""
        for evento in self.EVENTOS_BASE:
            if evento.id == evento_id:
                return evento
        return None
    
    def get_eventos_por_tipo(self, tipo: str) -> List[Evento]:
        """Obtiene todos los eventos de un tipo."""
        return [e for e in self.EVENTOS_BASE if e.tipo == tipo]
    
    def get_eventos_por_bioma(self, bioma_key: str) -> List[Evento]:
        """Obtiene eventos disponibles para un bioma."""
        return [
            e for e in self.EVENTOS_BASE
            if not e.biomas or bioma_key in e.biomas
        ]
