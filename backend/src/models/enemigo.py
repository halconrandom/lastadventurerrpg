"""
Modelo de Enemigo para el sistema de combate.
Extiende Entidad con stats escalables, drops y habilidades.
"""

import random
from typing import List, Dict, Optional, Any
from models.entidad import Entidad


class Drop:
    """Representa un drop posible de un enemigo"""
    
    def __init__(self, item_id: str, probabilidad: float = 1.0, 
                 cantidad_min: int = 1, cantidad_max: int = 1):
        self.item_id = item_id
        self.probabilidad = probabilidad  # 0.0 a 1.0
        self.cantidad_min = cantidad_min
        self.cantidad_max = cantidad_max
    
    def tirar(self) -> Optional[Dict[str, Any]]:
        """Determina si el drop ocurre y retorna el resultado"""
        if random.random() <= self.probabilidad:
            cantidad = random.randint(self.cantidad_min, self.cantidad_max)
            return {
                "item_id": self.item_id,
                "cantidad": cantidad
            }
        return None
    
    def to_dict(self) -> Dict:
        return {
            "item_id": self.item_id,
            "probabilidad": self.probabilidad,
            "cantidad_min": self.cantidad_min,
            "cantidad_max": self.cantidad_max
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Drop':
        return cls(
            item_id=data["item_id"],
            probabilidad=data.get("probabilidad", 1.0),
            cantidad_min=data.get("cantidad_min", 1),
            cantidad_max=data.get("cantidad_max", 1)
        )


class HabilidadEnemigo:
    """Habilidad especial de un enemigo"""
    
    def __init__(self, nombre: str, tipo: str = "fisico", 
                 multiplicador: float = 1.0, costo: int = 0,
                 efecto: Optional[str] = None):
        self.nombre = nombre
        self.tipo = tipo  # "fisico", "magico", "fuego", "hielo", "sangrado"
        self.multiplicador = multiplicador
        self.costo = costo  # Mana/Stamina que consume
        self.efecto = efecto  # Efecto adicional (congelar, sangrado, etc.)
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "multiplicador": self.multiplicador,
            "costo": self.costo,
            "efecto": self.efecto
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HabilidadEnemigo':
        return cls(
            nombre=data["nombre"],
            tipo=data.get("tipo", "fisico"),
            multiplicador=data.get("multiplicador", 1.0),
            costo=data.get("costo", 0),
            efecto=data.get("efecto")
        )


class Enemigo(Entidad):
    """
    Enemigo del juego con stats escalables, drops y habilidades.
    Extiende la clase Entidad base.
    """
    
    # Categorías de enemigos
    CATEGORIAS = ["bestia", "humanoide", "no_muerto", "magico", "jefe"]
    
    def __init__(self, id_enemigo: str, nombre: str, categoria: str = "bestia",
                 nivel: int = 1, zona: str = "bosque"):
        # Stats base (se escalarán según nivel)
        self.id_enemigo = id_enemigo
        self.categoria = categoria
        self.nivel = nivel
        self.zona = zona
        
        # Inicializar con stats base (se sobrescriben con escalar)
        super().__init__(nombre, hp=30, ataque=5, defensa=0)
        
        # Stats base (sin escalar)
        self.hp_base = 30
        self.atk_base = 5
        self.def_base = 0
        self.velocidad_base = 10
        self.critico_base = 5
        self.evasion_base = 5
        
        # Recursos
        self.mana_base = 0
        self.mana_actual = 0
        self.stamina_base = 100
        self.stamina_actual = 100
        
        # Recompensas
        self.experiencia_base = 10
        self.oro_base = 5
        
        # Drops y habilidades
        self.drops: List[Drop] = []
        self.habilidades: List[HabilidadEnemigo] = []
        
        # Estado
        self.es_jefe = False
        self.esta_bloqueando = False
        
        # Escalar stats según nivel
        self._escalar_stats()
    
    def _escalar_stats(self):
        """Escala los stats según el nivel del enemigo"""
        # Fórmulas de escalado
        self.hp = int(self.hp_base * (1 + self.nivel * 0.1))
        self.hp_max = self.hp
        self.ataque = int(self.atk_base * (1 + self.nivel * 0.05))
        self.defensa = int(self.def_base * (1 + self.nivel * 0.03))
        self.velocidad = int(self.velocidad_base * (1 + self.nivel * 0.02))
        self.critico = min(self.critico_base + self.nivel * 0.5, 50)
        self.evasion = min(self.evasion_base + self.nivel * 0.3, 50)
        
        # Recursos
        self.mana_base = int(self.mana_base * (1 + self.nivel * 0.05))
        self.mana_actual = self.mana_base
        self.stamina_actual = self.stamina_base
        
        # Recompensas escaladas
        self.experiencia = int(self.experiencia_base * (1 + self.nivel * 0.15))
        self.oro = int(self.oro_base * (1 + self.nivel * 0.1))
    
    def get_velocidad(self) -> int:
        return self.velocidad
    
    def get_critico(self) -> float:
        return min(self.critico, 50)
    
    def get_evasion(self) -> float:
        return min(self.evasion, 50)
    
    def calcular_daño(self, multiplicador: float = 1.0) -> int:
        """Calcula el daño que inflige el enemigo"""
        daño = int(self.ataque * multiplicador)
        
        # Verificar crítico
        if random.random() * 100 <= self.critico:
            daño = int(daño * 1.5)
            return daño, True  # (daño, es_critico)
        
        return daño, False
    
    def recibir_daño(self, cantidad: int, es_critico: bool = False) -> Dict:
        """
        Recibe daño aplicando reducción por defensa.
        Retorna información del daño recibido.
        """
        # Si está bloqueando, reduce 50%
        if self.esta_bloqueando:
            cantidad = int(cantidad * 0.5)
        
        # Aplicar reducción por defensa
        reduccion = min(self.defensa, 80) / 100
        daño_real = int(cantidad * (1 - reduccion))
        
        self.hp -= daño_real
        if self.hp < 0:
            self.hp = 0
        
        return {
            "daño_real": daño_real,
            "daño_original": cantidad,
            "reduccion": reduccion * 100,
            "es_critico": es_critico,
            "bloqueado": self.esta_bloqueando
        }
    
    def intentar_evasion(self) -> bool:
        """Intenta evadir un ataque"""
        return random.random() * 100 <= self.evasion
    
    def iniciar_turno(self):
        """Prepara al enemigo para su turno"""
        self.esta_bloqueando = False
        self.stamina_actual = self.stamina_base  # Refrescar stamina
    
    def bloquear(self):
        """Enemigo se pone en posición de bloqueo"""
        self.esta_bloqueando = True
    
    def tirar_drops(self) -> List[Dict]:
        """Calcula los drops al morir"""
        drops_obtenidos = []
        
        for drop in self.drops:
            resultado = drop.tirar()
            if resultado:
                drops_obtenidos.append(resultado)
        
        # Siempre dar oro
        drops_obtenidos.append({
            "item_id": "oro",
            "cantidad": self.oro
        })
        
        return drops_obtenidos
    
    def elegir_accion(self) -> Dict:
        """
        IA básica para elegir acción del enemigo.
        Retorna la acción a realizar.
        """
        # Si HP bajo, probabilidad de bloquear
        if self.hp < self.hp_max * 0.3 and random.random() < 0.3:
            return {"tipo": "bloquear"}
        
        # Si tiene habilidades y mana/stamina, usarlas
        if self.habilidades and self.stamina_actual >= 10:
            habilidad = random.choice(self.habilidades)
            if self.stamina_actual >= habilidad.costo:
                return {
                    "tipo": "habilidad",
                    "habilidad": habilidad.to_dict()
                }
        
        # Ataque básico
        return {"tipo": "atacar"}
    
    def to_dict(self) -> Dict:
        """Serializa el enemigo a diccionario"""
        return {
            "id_enemigo": self.id_enemigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "nivel": self.nivel,
            "zona": self.zona,
            "es_jefe": self.es_jefe,
            # Stats
            "hp": self.hp,
            "hp_max": self.hp_max,
            "ataque": self.ataque,
            "defensa": self.defensa,
            "velocidad": self.velocidad,
            "critico": self.critico,
            "evasion": self.evasion,
            "mana": self.mana_actual,
            "mana_max": self.mana_base,
            "stamina": self.stamina_actual,
            "stamina_max": self.stamina_base,
            # Recompensas
            "experiencia": self.experiencia,
            "oro": self.oro,
            # Estado
            "esta_vivo": self.esta_vivo(),
            "esta_bloqueando": self.esta_bloqueando,
            # Drops y habilidades
            "drops": [d.to_dict() for d in self.drops],
            "habilidades": [h.to_dict() for h in self.habilidades]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Enemigo':
        """Crea un Enemigo desde un diccionario"""
        enemigo = cls(
            id_enemigo=data["id_enemigo"],
            nombre=data["nombre"],
            categoria=data.get("categoria", "bestia"),
            nivel=data.get("nivel", 1),
            zona=data.get("zona", "bosque")
        )
        
        # Stats base
        enemigo.hp_base = data.get("hp_base", 30)
        enemigo.atk_base = data.get("atk_base", 5)
        enemigo.def_base = data.get("def_base", 0)
        enemigo.velocidad_base = data.get("velocidad_base", 10)
        enemigo.critico_base = data.get("critico_base", 5)
        enemigo.evasion_base = data.get("evasion_base", 5)
        enemigo.mana_base = data.get("mana_base", 0)
        enemigo.stamina_base = data.get("stamina_base", 100)
        
        # Recompensas base
        enemigo.experiencia_base = data.get("experiencia_base", 10)
        enemigo.oro_base = data.get("oro_base", 5)
        
        # Re-escalar
        enemigo._escalar_stats()
        
        # Sobrescribir valores actuales si vienen en data
        if "hp" in data:
            enemigo.hp = data["hp"]
        if "hp_max" in data:
            enemigo.hp_max = data["hp_max"]
        
        # Drops
        enemigo.drops = [Drop.from_dict(d) for d in data.get("drops", [])]
        
        # Habilidades
        enemigo.habilidades = [HabilidadEnemigo.from_dict(h) for h in data.get("habilidades", [])]
        
        # Flags
        enemigo.es_jefe = data.get("es_jefe", False)
        enemigo.esta_bloqueando = data.get("esta_bloqueando", False)
        
        return enemigo
    
    @classmethod
    def crear_desde_template(cls, template: Dict, nivel: int = 1, 
                             zona: str = "bosque", instancia_id: str = None) -> 'Enemigo':
        """
        Crea un enemigo desde un template (de enemigos.json).
        El nivel y zona pueden modificar los stats.
        """
        id_instancia = instancia_id or f"{template['id']}_{random.randint(1000, 9999)}"
        
        enemigo = cls(
            id_enemigo=id_instancia,
            nombre=template["nombre"],
            categoria=template.get("categoria", "bestia"),
            nivel=nivel,
            zona=zona
        )
        
        # Stats base del template
        stats_base = template.get("stats_base", {})
        enemigo.hp_base = stats_base.get("hp", 30)
        enemigo.atk_base = stats_base.get("atk", 5)
        enemigo.def_base = stats_base.get("def", 0)
        enemigo.velocidad_base = stats_base.get("velocidad", 10)
        enemigo.critico_base = stats_base.get("critico", 5)
        enemigo.evasion_base = stats_base.get("evasion", 5)
        enemigo.mana_base = stats_base.get("mana", 0)
        enemigo.stamina_base = stats_base.get("stamina", 100)
        
        # Recompensas base
        enemigo.experiencia_base = template.get("experiencia_base", 10)
        enemigo.oro_base = template.get("oro_base", 5)
        
        # Escalar según nivel
        enemigo._escalar_stats()
        
        # Drops
        for drop_data in template.get("drops", []):
            enemigo.drops.append(Drop.from_dict(drop_data))
        
        # Habilidades
        for hab_data in template.get("habilidades", []):
            enemigo.habilidades.append(HabilidadEnemigo.from_dict(hab_data))
        
        # Flags especiales
        enemigo.es_jefe = template.get("es_jefe", False)
        
        return enemigo
    
    def __str__(self):
        return f"{self.nombre} (Nv.{self.nivel}) | HP: {self.hp}/{self.hp_max} | ATK: {self.ataque} | DEF: {self.defensa}%"
