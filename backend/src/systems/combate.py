"""
Sistema de Combate para Last Adventurer.
Maneja el flujo completo de combate por turnos con grupo.
"""

import random
import json
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from models.personaje import Personaje
from models.enemigo import Enemigo


class TipoAccion(Enum):
    ATAQUE = "atacar"
    HABILIDAD = "habilidad"
    ITEM = "item"
    BLOQUEAR = "bloquear"
    EVADIR = "evadir"
    HUIR = "huir"


class TipoEstadoAlterado(Enum):
    # Estados de daño por tiempo
    QUEMADURA = "quemadura"
    VENENO = "veneno"
    SANGRADO = "sangrado"
    CONGELACION = "congelacion"
    ENFERMEDAD = "enfermedad"

    # Estados de control
    ATURDIR = "aturdir"
    INMOVILIZAR = "inmovilizar"
    CEGUERA = "ceguera"
    MIEDO = "miedo"
    CONFUSION = "confusion"
    SILENCIO = "silencio"

    # Estados de buff
    FURIA = "furia"
    ESCUDO = "escudo"
    VELOCIDAD = "velocidad"
    INVISIBILIDAD = "invisibilidad"
    REGENERACION = "regeneracion"


@dataclass
class EstadoAlterado:
    """Representa un estado alterado en un participante"""
    tipo: TipoEstadoAlterado
    duracion: int  # Turnos restantes
    daño_por_turno: int = 0
    modificador_stats: Dict[str, float] = field(default_factory=dict)  # {"ataque": 1.3, "defensa": 0.8}

    def to_dict(self) -> Dict:
        return {
            "tipo": self.tipo.value,
            "duracion": self.duracion,
            "daño_por_turno": self.daño_por_turno,
            "modificador_stats": self.modificador_stats
        }


class EstadoCombate(Enum):
    INICIADO = "iniciado"
    TURNO_JUGADOR = "turno_jugador"
    TURNO_ENEMIGO = "turno_enemigo"
    VICTORIA = "victoria"
    DERROTA = "derrota"
    HUIDA = "huida"


class TipoComportamientoIA(Enum):
    AGRESIVO = "agresivo"
    DEFENSIVO = "defensivo"
    MAGICO = "magico"
    SIGILOSO = "sigiloso"
    LIDER = "lider"
    JEFE = "jefe"


@dataclass
class Participante:
    """Representa un participante en combate (jugador o enemigo)"""
    id: str
    nombre: str
    tipo: str  # "jugador" o "enemigo"
    hp: int
    hp_max: int
    mana: int
    mana_max: int
    stamina: int
    stamina_max: int
    ataque: int
    defensa: int
    velocidad: int
    critico: float
    evasion: float
    nivel: int = 1
    esta_vivo: bool = True
    esta_bloqueando: bool = False
    esta_evadiendo: bool = False
    es_jugador: bool = False
    habilidades: List[Dict] = field(default_factory=list)
    # Recompensas (solo para enemigos)
    experiencia: int = 0
    oro: int = 0
    drops: List[Dict] = field(default_factory=list)
    # Estados alterados
    estados_alterados: List[EstadoAlterado] = field(default_factory=list)
    # IA de enemigos
    comportamiento_ia: TipoComportamientoIA = TipoComportamientoIA.AGRESIVO


    def get_velocidad(self) -> int:
        return self.velocidad

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "hp": self.hp,
            "hp_max": self.hp_max,
            "mana": self.mana,
            "mana_max": self.mana_max,
            "stamina": self.stamina,
            "stamina_max": self.stamina_max,
            "ataque": self.ataque,
            "defensa": self.defensa,
            "velocidad": self.velocidad,
            "critico": self.critico,
            "evasion": self.evasion,
            "nivel": self.nivel,
            "esta_vivo": self.esta_vivo,
            "esta_bloqueando": self.esta_bloqueando,
            "esta_evadiendo": self.esta_evadiendo,
            "es_jugador": self.es_jugador,
            "habilidades": self.habilidades,
            "experiencia": self.experiencia,
            "oro": self.oro,
            "drops": self.drops,
            "estados_alterados": [e.to_dict() for e in self.estados_alterados],
            "comportamiento_ia": self.comportamiento_ia.value if not self.es_jugador else None
        }



@dataclass
class EntradaLog:
    """Entrada en el log de combate"""
    turno: int
    actor_id: str
    actor_nombre: str
    accion: str
    objetivo_id: Optional[str] = None
    objetivo_nombre: Optional[str] = None
    daño: Optional[int] = None
    es_critico: bool = False
    es_evasion: bool = False
    mensaje: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "turno": self.turno,
            "actor_id": self.actor_id,
            "actor_nombre": self.actor_nombre,
            "accion": self.accion,
            "objetivo_id": self.objetivo_id,
            "objetivo_nombre": self.objetivo_nombre,
            "daño": self.daño,
            "es_critico": self.es_critico,
            "es_evasion": self.es_evasion,
            "mensaje": self.mensaje
        }


class CombateManager:
    """
    Gestiona el combate completo entre jugador/aliados y enemigos.
    """
    
    def __init__(self):
        self.estado: EstadoCombate = EstadoCombate.INICIADO
        self.turno: int = 0
        self.orden_turnos: List[str] = []
        self.indice_turno_actual: int = 0
        
        self.jugadores: Dict[str, Participante] = {}
        self.enemigos: Dict[str, Participante] = {}
        
        self.log: List[EntradaLog] = []
        self.ultimo_resultado: Optional[Dict] = None
        
        # Tracking de experiencia de habilidades durante el combate
        self.exp_acumulada: Dict[str, int] = {} # {nombre_habilidad: cantidad}
        self.arma_equipada: str = "Espada" # Por defecto para el jugador
    
    def iniciar_combate(self, personaje: Personaje, enemigos_data: List[Dict]) -> Dict:
        """Inicia un nuevo combate."""
        # Crear participante del jugador
        jugador = Participante(
            id="jugador_1",
            nombre=personaje.nombre,
            tipo="jugador",
            hp=personaje.stats.hp_actual,
            hp_max=personaje.stats.get_hp_max(),
            mana=personaje.stats.mana_actual,
            mana_max=personaje.stats.get_mana_max(),
            stamina=personaje.stats.stamina_actual,
            stamina_max=personaje.stats.get_stamina_max(),
            ataque=personaje.ataque,
            defensa=personaje.defensa,
            velocidad=personaje.stats.get_velocidad(),
            critico=personaje.stats.get_critico(),
            evasion=personaje.stats.get_evasion(),
            nivel=personaje.get_nivel(),
            es_jugador=True,
            habilidades=[],
            experiencia=0
        )
        self.jugadores[jugador.id] = jugador
        
        # Intentar determinar el arma desde el personaje (si existiera el campo)
        # Por ahora usamos "Espada" como base o lo que el jugador elija
        
        # Crear enemigos
        for i, enemigo_data in enumerate(enemigos_data):
            enemigo = Enemigo.crear_desde_template(
                enemigo_data,
                nivel=enemigo_data.get("nivel", 1),
                zona=enemigo_data.get("zona", "bosque")
            )
            
            participante = Participante(
                id=f"enemigo_{i+1}",
                nombre=enemigo.nombre,
                tipo="enemigo",
                hp=enemigo.hp,
                hp_max=enemigo.hp_max,
                mana=enemigo.mana_actual,
                mana_max=enemigo.mana_base,
                stamina=enemigo.stamina_actual,
                stamina_max=enemigo.stamina_base,
                ataque=enemigo.ataque,
                defensa=enemigo.defensa,
                velocidad=enemigo.get_velocidad(),
                critico=enemigo.get_critico(),
                evasion=enemigo.get_evasion(),
                nivel=enemigo.nivel,
                es_jugador=False,
                habilidades=[h.to_dict() for h in enemigo.habilidades],
                experiencia=enemigo.experiencia,
                oro=enemigo.oro,
                drops=[d.to_dict() for d in enemigo.drops]
            )

            self.enemigos[participante.id] = participante
        
        # Calcular orden de turnos por velocidad
        self._calcular_orden_turnos()
        
        # Cambiar estado
        self.estado = EstadoCombate.TURNO_JUGADOR
        self.turno = 1
        
        # Log inicial
        self.log.append(EntradaLog(
            turno=0,
            actor_id="sistema",
            actor_nombre="Sistema",
            accion="inicio",
            mensaje=f"¡Comienza el combate! Enemigos: {', '.join(e.nombre for e in self.enemigos.values())}"
        ))
        
        return self.get_estado()
    
    def _calcular_turnos_extra(self, atacante: Participante, objetivo: Participante) -> int:
        """Calcula cuántos turnos extra tiene el atacante basado en velocidad"""
        if objetivo.velocidad == 0:
            return 0

        diferencia = (atacante.velocidad - objetivo.velocidad) / objetivo.velocidad * 100
        turnos_extra = int(diferencia // 50)
        return max(0, turnos_extra)

    def _calcular_orden_turnos(self):
        """Calcula el orden de turnos basado en velocidad"""
        todos = list(self.jugadores.values()) + list(self.enemigos.values())
        todos_vivos = [p for p in todos if p.esta_vivo]
        todos_vivos.sort(key=lambda p: p.get_velocidad(), reverse=True)
        self.orden_turnos = [p.id for p in todos_vivos]
        self.indice_turno_actual = 0
    
    def _get_participante(self, id_participante: str) -> Optional[Participante]:
        """Obtiene un participante por su ID"""
        if id_participante in self.jugadores:
            return self.jugadores[id_participante]
        if id_participante in self.enemigos:
            return self.enemigos[id_participante]
        return None
    
    def _get_siguiente_objetivo_vivo(self, atacante_es_jugador: bool) -> Optional[Participante]:
        """Obtiene el siguiente objetivo vivo del bando contrario"""
        objetivos = self.enemigos if atacante_es_jugador else self.jugadores
        vivos = [p for p in objetivos.values() if p.esta_vivo]
        return vivos[0] if vivos else None
    
    def _registrar_exp_habilidad(self, nombre_habilidad: str, cantidad: int):
        """Registra experiencia para una habilidad específica"""
        self.exp_acumulada[nombre_habilidad] = self.exp_acumulada.get(nombre_habilidad, 0) + cantidad
    
    def ejecutar_accion(self, actor_id: str, accion: str,
                        objetivo_id: Optional[str] = None,
                        habilidad_nombre: Optional[str] = None,
                        item_id: Optional[str] = None) -> Dict:
        """Ejecuta una acción en combate."""
        actor = self._get_participante(actor_id)
        if not actor or not actor.esta_vivo:
            return {"success": False, "message": "Actor no válido"}

        resultado = {"success": True, "accion": accion, "actor_id": actor_id}

        if accion == "atacar":
            resultado = self._ejecutar_ataque(actor, objetivo_id)
        elif accion == "habilidad":
            resultado = self._ejecutar_habilidad(actor, objetivo_id, habilidad_nombre)
        elif accion == "item":
            resultado = self._ejecutar_item(actor, item_id)
        elif accion == "bloquear":
            resultado = self._ejecutar_bloqueo(actor)
        elif accion == "evadir":
            resultado = self._ejecutar_evadir(actor)
        elif accion == "huir":
            resultado = self._ejecutar_huida(actor)

        # Verificar fin de combate
        fin = self._verificar_fin_combate()
        if fin:
            resultado["fin_combate"] = True
            resultado["estado_final"] = self.estado.value

        self.ultimo_resultado = resultado
        return resultado
    
    def _ejecutar_contraataque(self, defensor: Participante, atacante: Participante) -> Optional[Dict]:
        """Ejecuta un contraataque tras bloquear"""
        # Chance base: 10% + (Nivel Defensa × 1%)
        # Nota: Usamos nivel del personaje como proxy del nivel de defensa
        chance_contraataque = 10 + defensor.nivel

        if random.random() * 100 <= chance_contraataque:
            # Contraataque: ataque básico automático
            daño = defensor.ataque
            es_critico = False

            if random.random() * 100 <= defensor.critico:
                daño = int(daño * 1.5)
                es_critico = True

            # Aplicar reducción por defensa del atacante
            reduccion = min(atacante.defensa, 80) / 100
            daño_real = int(daño * (1 - reduccion))

            atacante.hp -= daño_real
            if atacante.hp < 0:
                atacante.hp = 0
                atacante.esta_vivo = False

            mensaje = f"¡{defensor.nombre} contraataca a {atacante.nombre}!"
            if es_critico:
                mensaje += " ¡CRÍTICO!"
            mensaje += f" causando {daño_real} de daño."

            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=defensor.id,
                actor_nombre=defensor.nombre,
                accion="contraataque",
                objetivo_id=atacante.id,
                objetivo_nombre=atacante.nombre,
                daño=daño_real,
                es_critico=es_critico,
                mensaje=mensaje
            ))

            return {
                "success": True,
                "accion": "contraataque",
                "daño": daño_real,
                "es_critico": es_critico,
                "objetivo_hp": atacante.hp,
                "objetivo_vivo": atacante.esta_vivo,
                "mensaje": mensaje
            }

        return None

    def _ejecutar_ataque(self, actor: Participante, objetivo_id: Optional[str]) -> Dict:
        """Ejecuta un ataque básico"""
        if objetivo_id:
            objetivo = self._get_participante(objetivo_id)
        else:
            objetivo = self._get_siguiente_objetivo_vivo(actor.es_jugador)

        if not objetivo or not objetivo.esta_vivo:
            return {"success": False, "message": "No hay objetivo válido"}

        # Verificar evasión activa (100% éxito)
        if objetivo.esta_evadiendo:
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="atacar",
                objetivo_id=objetivo.id,
                objetivo_nombre=objetivo.nombre,
                es_evasion=True,
                mensaje=f"¡{objetivo.nombre} evadió activamente el ataque de {actor.nombre}!"
            ))
            return {"success": True, "accion": "atacar", "evasion": True, "mensaje": f"¡{objetivo.nombre} evadió activamente el ataque!"}

        # Verificar evasión pasiva
        if random.random() * 100 <= objetivo.evasion:
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="atacar",
                objetivo_id=objetivo.id,
                objetivo_nombre=objetivo.nombre,
                es_evasion=True,
                mensaje=f"¡{objetivo.nombre} esquivó el ataque de {actor.nombre}!"
            ))
            return {"success": True, "accion": "atacar", "evasion": True, "mensaje": f"¡{objetivo.nombre} esquivó el ataque!"}

        # Calcular daño según SISTEMA_COMBATE.md
        # Daño Base = ATK Personaje + Daño Arma (simplificado: usamos actor.ataque)
        daño = actor.ataque
        es_critico = False

        if random.random() * 100 <= actor.critico:
            daño = int(daño * 1.5)
            es_critico = True

        # Aplicar reducción por defensa
        # Reducción = Defensa % + (Nivel Defensa × 1%)
        # Nota: actor.defensa ya debería incluir el nivel de defensa en su cálculo si viene del Personaje
        reduccion = min(objetivo.defensa, 80) / 100

        daño_recibido = int(daño * (1 - reduccion))

        # Aplicar Bloqueo (Si el objetivo está bloqueando, reduce daño recibido en 50%)
        daño_real = daño_recibido
        if objetivo.esta_bloqueando:
            daño_real = int(daño_recibido * 0.5)
            # Ganar exp de Defensa si el objetivo es jugador
            if not actor.es_jugador: # El jugador está bloqueando
                self._registrar_exp_habilidad("Defensa", actor.nivel * 2)

            # Intentar contraataque
            contraataque_result = self._ejecutar_contraataque(objetivo, actor)
            if contraataque_result:
                # Verificar si el atacante murió por el contraataque
                if not actor.esta_vivo:
                    return {
                        "success": True,
                        "accion": "atacar",
                        "daño": daño_real,
                        "es_critico": es_critico,
                        "contraataque": contraataque_result,
                        "objetivo_hp": objetivo.hp,
                        "objetivo_vivo": objetivo.esta_vivo,
                        "mensaje": f"{actor.nombre} ataca a {objetivo.nombre} causando {daño_real} de daño. ¡{objetivo.nombre} contraataca!"
                    }

        objetivo.hp -= daño_real
        if objetivo.hp < 0:
            objetivo.hp = 0
            objetivo.esta_vivo = False

        mensaje = f"{actor.nombre} ataca a {objetivo.nombre}"
        if es_critico:
            mensaje += " ¡CRÍTICO!"
        mensaje += f" causando {daño_real} de daño."

        # Registrar experiencia de arma si el actor es jugador
        if actor.es_jugador:
            self._registrar_exp_habilidad(self.arma_equipada, 5) # 5 exp base por ataque exitoso

        self.log.append(EntradaLog(
            turno=self.turno,
            actor_id=actor.id,
            actor_nombre=actor.nombre,
            accion="atacar",
            objetivo_id=objetivo.id,
            objetivo_nombre=objetivo.nombre,
            daño=daño_real,
            es_critico=es_critico,
            mensaje=mensaje
        ))

        return {
            "success": True,
            "accion": "atacar",
            "objetivo_id": objetivo.id,
            "daño": daño_real,
            "es_critico": es_critico,
            "objetivo_hp": objetivo.hp,
            "objetivo_vivo": objetivo.esta_vivo,
            "mensaje": mensaje
        }
    
    def _ejecutar_habilidad(self, actor: Participante, objetivo_id: Optional[str], 
                           habilidad_nombre: Optional[str]) -> Dict:
        """Ejecuta una habilidad especial"""
        if not habilidad_nombre:
            return {"success": False, "message": "No se especificó habilidad"}
        
        habilidad = None
        for h in actor.habilidades:
            if h.get("nombre") == habilidad_nombre:
                habilidad = h
                break
        
        if not habilidad:
            return {"success": False, "message": "Habilidad no encontrada"}
        
        costo = habilidad.get("costo", 10)
        if actor.stamina < costo and actor.mana < costo:
            return {"success": False, "message": "Recursos insuficientes"}
        
        if actor.mana >= costo:
            actor.mana -= costo
        else:
            actor.stamina -= costo
        
        if objetivo_id:
            objetivo = self._get_participante(objetivo_id)
        else:
            objetivo = self._get_siguiente_objetivo_vivo(actor.es_jugador)
        
        if not objetivo or not objetivo.esta_vivo:
            return {"success": False, "message": "No hay objetivo válido"}
        
        multiplicador = habilidad.get("multiplicador", 1.0)
        daño = int(actor.ataque * multiplicador)
        
        es_critico = False
        if random.random() * 100 <= actor.critico:
            daño = int(daño * 1.5)
            es_critico = True
        
        if random.random() * 100 <= objetivo.evasion:
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="habilidad",
                objetivo_id=objetivo.id,
                objetivo_nombre=objetivo.nombre,
                es_evasion=True,
                mensaje=f"¡{objetivo.nombre} esquivó {habilidad_nombre}!"
            ))
            return {"success": True, "accion": "habilidad", "habilidad": habilidad_nombre, "evasion": True}
        
        reduccion = min(objetivo.defensa, 80) / 100
        daño_real = int(daño * (1 - reduccion))
        
        objetivo.hp -= daño_real
        if objetivo.hp < 0:
            objetivo.hp = 0
            objetivo.esta_vivo = False
        
        mensaje = f"{actor.nombre} usa {habilidad_nombre} en {objetivo.nombre}"
        if es_critico:
            mensaje += " ¡CRÍTICO!"
        mensaje += f" causando {daño_real} de daño."

        self.log.append(EntradaLog(
            turno=self.turno,
            actor_id=actor.id,
            actor_nombre=actor.nombre,
            accion="habilidad",
            objetivo_id=objetivo.id,
            objetivo_nombre=objetivo.nombre,
            daño=daño_real,
            es_critico=es_critico,
            mensaje=mensaje
        ))
        
        # Registrar experiencia de habilidad si el actor es jugador
        if actor.es_jugador:
            self._registrar_exp_habilidad(habilidad_nombre, 10) # 10 exp base por uso de habilidad
        
        return {
            "success": True,
            "accion": "habilidad",
            "habilidad": habilidad_nombre,
            "objetivo_id": objetivo.id,
            "daño": daño_real,
            "es_critico": es_critico,
            "objetivo_hp": objetivo.hp,
            "objetivo_vivo": objetivo.esta_vivo,
            "mensaje": mensaje
        }
    
    def _ejecutar_item(self, actor: Participante, item_id: Optional[str]) -> Dict:
        """Ejecuta el uso de un item"""
        if item_id == "pocion_vida":
            curacion = 30
            actor.hp = min(actor.hp + curacion, actor.hp_max)
            
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="item",
                mensaje=f"{actor.nombre} usa una poción y recupera {curacion} HP."
            ))
            
            return {
                "success": True,
                "accion": "item",
                "item": item_id,
                "curacion": curacion,
                "hp_actual": actor.hp,
                "mensaje": f"Recuperaste {curacion} HP."
            }
        
        return {"success": False, "message": "Item no válido"}
    
    def _ejecutar_bloqueo(self, actor: Participante) -> Dict:
        """Ejecuta acción de bloqueo"""
        actor.esta_bloqueando = True

        self.log.append(EntradaLog(
            turno=self.turno,
            actor_id=actor.id,
            actor_nombre=actor.nombre,
            accion="bloquear",
            mensaje=f"{actor.nombre} se prepara para bloquear."
        ))

        return {
            "success": True,
            "accion": "bloquear",
            "mensaje": f"{actor.nombre} se prepara para bloquear el próximo ataque."
        }

    def _ejecutar_evadir(self, actor: Participante) -> Dict:
        """Ejecuta acción de evadir activamente"""
        actor.esta_evadiendo = True

        self.log.append(EntradaLog(
            turno=self.turno,
            actor_id=actor.id,
            actor_nombre=actor.nombre,
            accion="evadir",
            mensaje=f"{actor.nombre} se prepara para evadir el próximo ataque."
        ))

        return {
            "success": True,
            "accion": "evadir",
            "mensaje": f"{actor.nombre} se prepara para evadir el próximo ataque."
        }
    
    def _ejecutar_huida(self, actor: Participante) -> Dict:
        """Ejecuta intento de huida"""
        # Probabilidad basada en nivel del jugador vs enemigo
        enemigo_nivel = max([e.nivel for e in self.enemigos.values() if e.esta_vivo], default=1)
        prob_exito = 50 + (actor.nivel - enemigo_nivel) * 5
        prob_exito = max(10, min(90, prob_exito))
        
        if random.random() * 100 <= prob_exito:
            self.estado = EstadoCombate.HUIDA
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="huir",
                mensaje=f"¡{actor.nombre} logró escapar del combate!"
            ))
            return {
                "success": True,
                "accion": "huir",
                "escapo": True,
                "mensaje": "¡Lograste escapar del combate!"
            }
        else:
            self.log.append(EntradaLog(
                turno=self.turno,
                actor_id=actor.id,
                actor_nombre=actor.nombre,
                accion="huir",
                mensaje=f"{actor.nombre} intentó huir pero falló."
            ))
            return {
                "success": True,
                "accion": "huir",
                "escapo": False,
                "mensaje": "¡No pudiste escapar!"
            }
    
    def _verificar_fin_combate(self) -> bool:
        """Verifica si el combate ha terminado"""
        jugadores_vivos = [p for p in self.jugadores.values() if p.esta_vivo]
        enemigos_vivos = [p for p in self.enemigos.values() if p.esta_vivo]
        
        if not enemigos_vivos:
            self.estado = EstadoCombate.VICTORIA
            return True
        
        if not jugadores_vivos:
            self.estado = EstadoCombate.DERROTA
            return True
        
        return False
    
    def _regenerar_stamina(self):
        """Regenera la stamina de todos los participantes al inicio del turno"""
        for participante in list(self.jugadores.values()) + list(self.enemigos.values()):
            if participante.esta_vivo:
                participante.stamina = participante.stamina_max

    def _aplicar_estado_alterado(self, participante: Participante, tipo: TipoEstadoAlterado,
                                 duracion: int, daño_por_turno: int = 0,
                                 modificador_stats: Dict[str, float] = None):
        """Aplica un estado alterado a un participante"""
        if modificador_stats is None:
            modificador_stats = {}

        # Verificar si ya tiene el estado
        for estado in participante.estados_alterados:
            if estado.tipo == tipo:
                # Reiniciar duración
                estado.duracion = duracion
                return

        # Agregar nuevo estado
        estado = EstadoAlterado(
            tipo=tipo,
            duracion=duracion,
            daño_por_turno=daño_por_turno,
            modificador_stats=modificador_stats
        )
        participante.estados_alterados.append(estado)

    def _procesar_estados_alterados(self):
        """Procesa los efectos de los estados alterados al inicio del turno"""
        for participante in list(self.jugadores.values()) + list(self.enemigos.values()):
            if not participante.esta_vivo:
                continue

            estados_a_eliminar = []

            for estado in participante.estados_alterados:
                # Aplicar daño por tiempo
                if estado.daño_por_turno > 0:
                    participante.hp -= estado.daño_por_turno
                    if participante.hp < 0:
                        participante.hp = 0
                        participante.esta_vivo = False

                    self.log.append(EntradaLog(
                        turno=self.turno,
                        actor_id="sistema",
                        actor_nombre="Sistema",
                        accion="estado_alterado",
                        objetivo_id=participante.id,
                        objetivo_nombre=participante.nombre,
                        daño=estado.daño_por_turno,
                        mensaje=f"{participante.nombre} sufre {estado.daño_por_turno} de daño por {estado.tipo.value}."
                    ))

                # Reducir duración
                estado.duracion -= 1

                # Eliminar si expiró
                if estado.duracion <= 0:
                    estados_a_eliminar.append(estado)

            # Eliminar estados expirados
            for estado in estados_a_eliminar:
                participante.estados_alterados.remove(estado)

    def _get_stats_modificados(self, participante: Participante) -> Dict[str, int]:
        """Obtiene los stats modificados por los estados alterados"""
        stats_modificados = {
            "ataque": participante.ataque,
            "defensa": participante.defensa,
            "velocidad": participante.velocidad,
            "critico": participante.critico,
            "evasion": participante.evasion
        }

        for estado in participante.estados_alterados:
            for stat, modificador in estado.modificador_stats.items():
                if stat in stats_modificados:
                    stats_modificados[stat] = int(stats_modificados[stat] * modificador)

        return stats_modificados

    def _decidir_accion_ia(self, enemigo: Participante) -> Tuple[str, Optional[str]]:
        """Decide la acción del enemigo basado en su comportamiento"""
        comportamiento = enemigo.comportamiento_ia

        # Obtener objetivos vivos del jugador
        objetivos_jugador = [p for p in self.jugadores.values() if p.esta_vivo]
        if not objetivos_jugador:
            return "huir", None

        # Encontrar el objetivo con HP más bajo
        objetivo_hp_bajo = min(objetivos_jugador, key=lambda p: p.hp)

        if comportamiento == TipoComportamientoIA.AGRESIVO:
            # Ataca siempre, prioriza HP bajo
            return "atacar", objetivo_hp_bajo.id

        elif comportamiento == TipoComportamientoIA.DEFENSIVO:
            # Bloquea frecuentemente, protege aliados
            if random.random() < 0.3:  # 30% chance de bloquear
                return "bloquear", None
            return "atacar", objetivo_hp_bajo.id

        elif comportamiento == TipoComportamientoIA.MAGICO:
            # Usa habilidades, mantiene distancia
            if enemigo.habilidades and random.random() < 0.5:  # 50% chance de usar habilidad
                habilidad = random.choice(enemigo.habilidades)
                return "habilidad", habilidad.get("nombre")
            return "atacar", objetivo_hp_bajo.id

        elif comportamiento == TipoComportamientoIA.SIGILOSO:
            # Ataca primero, huye si HP bajo
            if enemigo.hp < enemigo.hp_max * 0.3:  # Menos de 30% HP
                return "huir", None
            return "atacar", objetivo_hp_bajo.id

        elif comportamiento == TipoComportamientoIA.LIDER:
            # Ordena a aliados, invoca refuerzos (simplificado: ataca agresivamente)
            return "atacar", objetivo_hp_bajo.id

        elif comportamiento == TipoComportamientoIA.JEFE:
            # Múltiples fases, habilidades especiales (simplificado: usa habilidades más frecuentemente)
            if enemigo.habilidades and random.random() < 0.7:  # 70% chance de usar habilidad
                habilidad = random.choice(enemigo.habilidades)
                return "habilidad", habilidad.get("nombre")
            return "atacar", objetivo_hp_bajo.id

        else:
            # Comportamiento por defecto: aleatorio
            return "atacar", objetivo_hp_bajo.id

    def resolver_turno_enemigos(self) -> List[Dict]:
        """Resuelve los turnos de todos los enemigos vivos"""
        resultados = []

        # Regenerar stamina al inicio del turno
        self._regenerar_stamina()

        # Procesar estados alterados
        self._procesar_estados_alterados()

        for enemigo_id, enemigo in self.enemigos.items():
            if not enemigo.esta_vivo:
                continue

            # Decidir acción basada en comportamiento
            accion, habilidad_nombre = self._decidir_accion_ia(enemigo)

            if accion == "habilidad" and habilidad_nombre:
                resultado = self.ejecutar_accion(
                    enemigo_id,
                    "habilidad",
                    habilidad_nombre=habilidad_nombre
                )
            elif accion == "bloquear":
                resultado = self.ejecutar_accion(enemigo_id, "bloquear")
            elif accion == "huir":
                resultado = self.ejecutar_accion(enemigo_id, "huir")
            else:
                resultado = self.ejecutar_accion(enemigo_id, "atacar")

            resultados.append(resultado)

        # Avanzar turno
        self.turno += 1

        # Resetear bloqueos y evasión activa
        for p in list(self.jugadores.values()) + list(self.enemigos.values()):
            p.esta_bloqueando = False
            p.esta_evadiendo = False

        return resultados
    
    def get_estado(self) -> Dict:
        """Retorna el estado actual del combate"""
        return {
            "estado": self.estado.value,
            "turno": self.turno,
            "orden_turnos": self.orden_turnos,
            "jugadores": {k: v.to_dict() for k, v in self.jugadores.items()},
            "enemigos": {k: v.to_dict() for k, v in self.enemigos.items()},
            "log": [e.to_dict() for e in self.log]
        }
    
    def get_recompensas(self) -> Dict:
        """Calcula las recompensas al ganar el combate"""
        if self.estado != EstadoCombate.VICTORIA:
            return {"experiencia": 0, "oro": 0, "drops": []}
        
        experiencia_total = 0
        oro_total = 0
        drops_finales = []
        
        for enemigo in self.enemigos.values():
            if not enemigo.esta_vivo:
                experiencia_total += enemigo.experiencia
                oro_total += enemigo.oro
                
                # Tirar drops (simular Enemigo.tirar_drops)
                for drop_data in enemigo.drops:
                    if random.random() <= drop_data.get("probabilidad", 1.0):
                        cantidad = random.randint(
                            drop_data.get("cantidad_min", 1), 
                            drop_data.get("cantidad_max", 1)
                        )
                        drops_finales.append({
                            "item_id": drop_data["item_id"],
                            "cantidad": cantidad
                        })
        
        return {
            "experiencia": experiencia_total,
            "oro": oro_total,
            "drops": drops_finales
        }