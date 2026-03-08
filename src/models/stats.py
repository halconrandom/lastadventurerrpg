class Stats:
    """Sistema de stats del personaje - incluye nivel y experiencia"""

    # Nivel máximo
    NIVEL_MAX = 100

    # Valores base iniciales
    HP_BASE_INICIAL = 100
    ATK_BASE_INICIAL = 10
    DEF_BASE_INICIAL = 0
    VELOCIDAD_BASE_INICIAL = 10
    CRITICO_BASE_INICIAL = 5
    EVASION_BASE_INICIAL = 10
    MANA_BASE_INICIAL = 100
    STAMINA_BASE_INICIAL = 10

    # Caps máximos
    DEF_CAP = 80
    CRITICO_CAP = 50
    EVASION_CAP = 50

    # Multiplicadores por punto
    HP_POR_PUNTO = 10
    ATK_POR_PUNTO = 2
    DEF_POR_PUNTO = 1
    VELOCIDAD_POR_PUNTO = 1
    CRITICO_POR_PUNTO = 1
    EVASION_POR_PUNTO = 1
    MANA_POR_PUNTO = 10
    STAMINA_POR_PUNTO = 2

    def __init__(self):
        # Nivel y experiencia
        self.nivel = 1
        self.experiencia = 0

        # Stats base (se modifican al asignar puntos)
        self.hp_base = self.HP_BASE_INICIAL
        self.atk_base = self.ATK_BASE_INICIAL
        self.def_base = self.DEF_BASE_INICIAL
        self.velocidad_base = self.VELOCIDAD_BASE_INICIAL
        self.critico_base = self.CRITICO_BASE_INICIAL
        self.evasion_base = self.EVASION_BASE_INICIAL
        self.mana_base = self.MANA_BASE_INICIAL
        self.stamina_base = self.STAMINA_BASE_INICIAL

        # Valores actuales (pueden variar en combate)
        self.hp_actual = self.hp_base
        self.mana_actual = self.mana_base
        self.stamina_actual = self.stamina_base

        # Puntos asignados (para tracking)
        self.puntos_hp = 0
        self.puntos_atk = 0
        self.puntos_def = 0
        self.puntos_velocidad = 0
        self.puntos_critico = 0
        self.puntos_evasion = 0
        self.puntos_mana = 0
        self.puntos_stamina = 0

        # Puntos disponibles para asignar
        self.puntos_disponibles = 0

    # ==================== GETTERS DE STATS TOTALES ====================

    def get_hp_max(self):
        """HP máximo total"""
        return self.hp_base

    def get_atk(self):
        """ATK total"""
        return self.atk_base

    def get_def(self):
        """DEF total (porcentaje)"""
        return min(self.def_base, self.DEF_CAP)

    def get_velocidad(self):
        """Velocidad total"""
        return self.velocidad_base

    def get_critico(self):
        """Probabilidad de crítico total (porcentaje)"""
        return min(self.critico_base, self.CRITICO_CAP)

    def get_evasion(self):
        """Probabilidad de evasión total (porcentaje)"""
        return min(self.evasion_base, self.EVASION_CAP)

    def get_mana_max(self):
        """Mana máximo total"""
        return self.mana_base

    def get_stamina_max(self):
        """Stamina máxima total"""
        return self.stamina_base

    # ==================== SISTEMA DE NIVEL Y EXPERIENCIA ====================

    def experiencia_para_subir(self):
        """Fórmula tipo Diablo: Nivel × 100 × (1 + Nivel × 0.1)"""
        return int(self.nivel * 100 * (1 + self.nivel * 0.1))

    def ganar_experiencia(self, cantidad):
        """Añade experiencia y sube de nivel si es necesario"""
        if self.nivel >= self.NIVEL_MAX:
            return False, "Nivel máximo alcanzado"

        self.experiencia += cantidad
        subio_nivel = False

        # Verificar si sube de nivel (puede subir varios niveles de una vez)
        while self.experiencia >= self.experiencia_para_subir() and self.nivel < self.NIVEL_MAX:
            self.experiencia -= self.experiencia_para_subir()
            self.subir_nivel()
            subio_nivel = True

        if subio_nivel:
            return True, f"¡Subiste a nivel {self.nivel}!"
        return True, f"+{cantidad} experiencia"

    def subir_nivel(self):
        """Sube de nivel y otorga puntos según el rango"""
        self.nivel += 1

        # Puntos por nivel según rango
        if self.nivel <= 10:
            puntos = 5
        elif self.nivel <= 20:
            puntos = 7
        elif self.nivel <= 50:
            puntos = 10
        else:
            puntos = 15

        self.puntos_disponibles += puntos

        # Restaurar recursos al subir de nivel
        self.hp_actual = self.hp_base
        self.mana_actual = self.mana_base
        self.stamina_actual = self.stamina_base

    def get_progreso_nivel(self):
        """Retorna el porcentaje de progreso hacia el siguiente nivel"""
        exp_necesaria = self.experiencia_para_subir()
        return int((self.experiencia / exp_necesaria) * 100)

    # ==================== ASIGNACIÓN DE PUNTOS ====================

    def _asignar_punto(self, stat_nombre, cantidad=1):
        """Método interno para asignar puntos"""
        if self.puntos_disponibles < cantidad:
            return False, "No tienes puntos disponibles"

        return True, None

    def asignar_hp(self, cantidad=1):
        """Asigna puntos a HP"""
        puede, error = self._asignar_punto("hp", cantidad)
        if not puede:
            return False, error

        self.puntos_hp += cantidad
        self.hp_base += self.HP_POR_PUNTO * cantidad
        self.hp_actual = self.hp_base  # Curar al asignar
        self.puntos_disponibles -= cantidad
        return True, f"+{self.HP_POR_PUNTO * cantidad} HP"

    def asignar_atk(self, cantidad=1):
        """Asigna puntos a ATK"""
        puede, error = self._asignar_punto("atk", cantidad)
        if not puede:
            return False, error

        self.puntos_atk += cantidad
        self.atk_base += self.ATK_POR_PUNTO * cantidad
        self.puntos_disponibles -= cantidad
        return True, f"+{self.ATK_POR_PUNTO * cantidad} ATK"

    def asignar_def(self, cantidad=1):
        """Asigna puntos a DEF"""
        puede, error = self._asignar_punto("def", cantidad)
        if not puede:
            return False, error

        self.puntos_def += cantidad
        self.def_base += self.DEF_POR_PUNTO * cantidad
        self.puntos_disponibles -= cantidad
        return True, f"+{self.DEF_POR_PUNTO * cantidad}% DEF"

    def asignar_velocidad(self, cantidad=1):
        """Asigna puntos a Velocidad"""
        puede, error = self._asignar_punto("velocidad", cantidad)
        if not puede:
            return False, error

        self.puntos_velocidad += cantidad
        self.velocidad_base += self.VELOCIDAD_POR_PUNTO * cantidad
        self.puntos_disponibles -= cantidad
        return True, f"+{self.VELOCIDAD_POR_PUNTO * cantidad} Velocidad"

    def asignar_critico(self, cantidad=1):
        """Asigna puntos a Crítico"""
        puede, error = self._asignar_punto("critico", cantidad)
        if not puede:
            return False, error

        nuevo_critico = self.critico_base + self.CRITICO_POR_PUNTO * cantidad
        if nuevo_critico > self.CRITICO_CAP:
            return False, f"Crítico máximo alcanzado ({self.CRITICO_CAP}%)"

        self.puntos_critico += cantidad
        self.critico_base = nuevo_critico
        self.puntos_disponibles -= cantidad
        return True, f"+{self.CRITICO_POR_PUNTO * cantidad}% Crítico"

    def asignar_evasion(self, cantidad=1):
        """Asigna puntos a Evasión"""
        puede, error = self._asignar_punto("evasion", cantidad)
        if not puede:
            return False, error

        nueva_evasion = self.evasion_base + self.EVASION_POR_PUNTO * cantidad
        if nueva_evasion > self.EVASION_CAP:
            return False, f"Evasión máxima alcanzada ({self.EVASION_CAP}%)"

        self.puntos_evasion += cantidad
        self.evasion_base = nueva_evasion
        self.puntos_disponibles -= cantidad
        return True, f"+{self.EVASION_POR_PUNTO * cantidad}% Evasión"

    def asignar_mana(self, cantidad=1):
        """Asigna puntos a Mana"""
        puede, error = self._asignar_punto("mana", cantidad)
        if not puede:
            return False, error

        self.puntos_mana += cantidad
        self.mana_base += self.MANA_POR_PUNTO * cantidad
        self.mana_actual = self.mana_base
        self.puntos_disponibles -= cantidad
        return True, f"+{self.MANA_POR_PUNTO * cantidad} Mana"

    def asignar_stamina(self, cantidad=1):
        """Asigna puntos a Stamina"""
        puede, error = self._asignar_punto("stamina", cantidad)
        if not puede:
            return False, error

        self.puntos_stamina += cantidad
        self.stamina_base += self.STAMINA_POR_PUNTO * cantidad
        self.stamina_actual = self.stamina_base
        self.puntos_disponibles -= cantidad
        return True, f"+{self.STAMINA_POR_PUNTO * cantidad} Stamina"

    # ==================== GESTIÓN DE RECURSOS ====================

    def recibir_daño(self, cantidad):
        """Recibe daño y reduce HP"""
        self.hp_actual -= cantidad
        if self.hp_actual < 0:
            self.hp_actual = 0
        return self.hp_actual

    def curar(self, cantidad):
        """Cura HP"""
        self.hp_actual += cantidad
        if self.hp_actual > self.hp_base:
            self.hp_actual = self.hp_base
        return self.hp_actual

    def usar_mana(self, cantidad):
        """Consume mana"""
        if self.mana_actual < cantidad:
            return False
        self.mana_actual -= cantidad
        return True

    def recuperar_mana(self, cantidad):
        """Recupera mana"""
        self.mana_actual += cantidad
        if self.mana_actual > self.mana_base:
            self.mana_actual = self.mana_base
        return self.mana_actual

    def usar_stamina(self, cantidad):
        """Consume stamina"""
        if self.stamina_actual < cantidad:
            return False
        self.stamina_actual -= cantidad
        return True

    def recuperar_stamina(self, cantidad):
        """Recupera stamina"""
        self.stamina_actual += cantidad
        if self.stamina_actual > self.stamina_base:
            self.stamina_actual = self.stamina_base
        return self.stamina_actual

    def refrescar_stamina(self):
        """Refresca stamina al inicio de cada turno"""
        self.stamina_actual = self.stamina_base

    def descanso_largo(self):
        """Descanso largo: recupera HP, Mana y Stamina al máximo"""
        self.hp_actual = self.hp_base
        self.mana_actual = self.mana_base
        self.stamina_actual = self.stamina_base

    # ==================== CÁLCULOS DE COMBATE ====================

    def calcular_reduccion_daño(self, nivel_defensa=0):
        """Calcula la reducción de daño total"""
        reduccion = self.get_def() + (nivel_defensa * 1)
        return min(reduccion, self.DEF_CAP)

    def calcular_daño_recibido(self, daño_enemigo, nivel_defensa=0):
        """Calcula el daño real después de reducción"""
        reduccion = self.calcular_reduccion_daño(nivel_defensa)
        return int(daño_enemigo * (1 - reduccion / 100))

    def calcular_turnos_extra(self, velocidad_enemigo):
        """Calcula turnos extra basado en diferencia de velocidad"""
        if velocidad_enemigo <= 0:
            return 0

        diferencia = (self.get_velocidad() - velocidad_enemigo) / velocidad_enemigo * 100
        turnos_extra = int(diferencia // 50)
        return max(0, turnos_extra)

    def calcular_chance_contraataque(self, nivel_defensa=0):
        """Calcula la probabilidad de contraataque tras bloqueo"""
        # 10% base + 1% por nivel de defensa
        return 10 + nivel_defensa

    # ==================== SERIALIZACIÓN ====================

    def to_dict(self):
        """Convierte los stats a diccionario para guardar"""
        return {
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "hp_base": self.hp_base,
            "hp_actual": self.hp_actual,
            "puntos_hp": self.puntos_hp,
            "atk_base": self.atk_base,
            "puntos_atk": self.puntos_atk,
            "def_base": self.def_base,
            "puntos_def": self.puntos_def,
            "velocidad_base": self.velocidad_base,
            "puntos_velocidad": self.puntos_velocidad,
            "critico_base": self.critico_base,
            "puntos_critico": self.puntos_critico,
            "evasion_base": self.evasion_base,
            "puntos_evasion": self.puntos_evasion,
            "mana_base": self.mana_base,
            "mana_actual": self.mana_actual,
            "puntos_mana": self.puntos_mana,
            "stamina_base": self.stamina_base,
            "stamina_actual": self.stamina_actual,
            "puntos_stamina": self.puntos_stamina,
            "puntos_disponibles": self.puntos_disponibles
        }

    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Stats desde un diccionario"""
        stats = cls()

        stats.nivel = data.get("nivel", 1)
        stats.experiencia = data.get("experiencia", 0)

        stats.hp_base = data.get("hp_base", cls.HP_BASE_INICIAL)
        stats.hp_actual = data.get("hp_actual", stats.hp_base)
        stats.puntos_hp = data.get("puntos_hp", 0)

        stats.atk_base = data.get("atk_base", cls.ATK_BASE_INICIAL)
        stats.puntos_atk = data.get("puntos_atk", 0)

        stats.def_base = data.get("def_base", cls.DEF_BASE_INICIAL)
        stats.puntos_def = data.get("puntos_def", 0)

        stats.velocidad_base = data.get("velocidad_base", cls.VELOCIDAD_BASE_INICIAL)
        stats.puntos_velocidad = data.get("puntos_velocidad", 0)

        stats.critico_base = data.get("critico_base", cls.CRITICO_BASE_INICIAL)
        stats.puntos_critico = data.get("puntos_critico", 0)

        stats.evasion_base = data.get("evasion_base", cls.EVASION_BASE_INICIAL)
        stats.puntos_evasion = data.get("puntos_evasion", 0)

        stats.mana_base = data.get("mana_base", cls.MANA_BASE_INICIAL)
        stats.mana_actual = data.get("mana_actual", stats.mana_base)
        stats.puntos_mana = data.get("puntos_mana", 0)

        stats.stamina_base = data.get("stamina_base", cls.STAMINA_BASE_INICIAL)
        stats.stamina_actual = data.get("stamina_actual", stats.stamina_base)
        stats.puntos_stamina = data.get("puntos_stamina", 0)

        stats.puntos_disponibles = data.get("puntos_disponibles", 0)

        return stats

    # ==================== UTILIDADES ====================

    def __str__(self):
        """Representación en string de los stats"""
        return f"""Nivel: {self.nivel} ({self.get_progreso_nivel()}%)
HP: {self.hp_actual}/{self.get_hp_max()}
ATK: {self.get_atk()}
DEF: {self.get_def()}%
Velocidad: {self.get_velocidad()}
Crítico: {self.get_critico()}%
Evasión: {self.get_evasion()}%
Mana: {self.mana_actual}/{self.get_mana_max()}
Stamina: {self.stamina_actual}/{self.get_stamina_max()}
Puntos disponibles: {self.puntos_disponibles}"""

    def resumen(self):
        """Resumen corto de stats"""
        return f"Nv{self.nivel} | HP: {self.hp_actual}/{self.get_hp_max()} | ATK: {self.get_atk()} | DEF: {self.get_def()}% | Mana: {self.mana_actual}/{self.get_mana_max()}"