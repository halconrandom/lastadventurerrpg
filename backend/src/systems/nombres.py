"""
Sistema de generacion de nombres procedurales.

Genera nombres unicos para:
- NPCs
- Lugares
- Objetos
- Enemigos
- Titulos y apodos
"""

from typing import List, Optional, Tuple
from .seed import WorldSeed


class NombreGenerator:
    """Generador de nombres procedurales."""
    
    # Silabas para construccion de nombres
    SILABAS_INICIO = [
        "Ae", "Ba", "Ce", "Da", "El", "Fa", "Go", "Ha", "Il", "Jo",
        "Ka", "La", "Ma", "No", "Or", "Pa", "Qu", "Ra", "Sa", "Th",
        "Ul", "Va", "Wo", "Xa", "Yr", "Zae", "Bre", "Cro", "Dra", "Eld",
        "Fen", "Gor", "Hil", "Irn", "Jar", "Kel", "Lor", "Mor", "Nar", "Oth"
    ]
    
    SILABAS_MEDIA = [
        "ba", "ce", "da", "el", "fa", "go", "ha", "il", "jo", "ka",
        "la", "ma", "no", "or", "pa", "ra", "sa", "th", "ul", "va",
        "wen", "xor", "yth", "zal", "bro", "cra", "dre", "eld", "fen",
        "gar", "hil", "irn", "jar", "kel", "lor", "mar", "nar", "oth"
    ]
    
    SILABAS_FIN = [
        "a", "on", "us", "ia", "or", "en", "is", "os", "um", "ax",
        "el", "ic", "us", "yn", "ar", "eth", "ion", "or", "us", "wyn",
        "gard", "heim", "holm", "mark", "stad", "thor", "vald", "wyn"
    ]
    
    # Nombres predefinidos por tipo
    NOMBRES_NPC_MASCULINOS = [
        "Aldric", "Baelin", "Cedric", "Dorian", "Edmund",
        "Faelan", "Garrick", "Hadrian", "Ivar", "Jorund",
        "Kael", "Lysander", "Magnus", "Nikolai", "Orion",
        "Percival", "Quillan", "Roland", "Sebastian", "Theron",
        "Ulric", "Viktor", "Wilhelm", "Xavier", "Yorick"
    ]
    
    NOMBRES_NPC_FEMENINOS = [
        "Adelina", "Beatrix", "Cordelia", "Diana", "Elara",
        "Fiona", "Gwendolyn", "Helena", "Isolde", "Juliana",
        "Katarina", "Lydia", "Mirabel", "Natasha", "Ophelia",
        "Penelope", "Quinn", "Rosalind", "Seraphina", "Theodora",
        "Ursula", "Valentina", "Willow", "Xanthe", "Yvonne"
    ]
    
    # Apellidos
    APELLIDOS = [
        "Ashford", "Blackwood", "Cromwell", "Darkhollow", "Everhart",
        "Fairfax", "Grimshaw", "Holloway", "Ironside", "Jasper",
        "Kingsley", "Lockwood", "Mercer", "Nightingale", "Oakenshield",
        "Proudfoot", "Quicksilver", "Ravencroft", "Stormwind", "Thornwood",
        "Underhill", "Vance", "Winterborne", "Xavier", "Yarrow"
    ]
    
    # Titulos y apodos
    TITULOS_POSITIVOS = [
        "el Sabio", "el Valiente", "el Justo", "el Noble", "el Piadoso",
        "el Magnifico", "el Iluminado", "el Bendito", "el Honorable", "el Leal",
        "el Guerrero", "el Mago", "el Sanador", "el Explorador", "el Guardian"
    ]
    
    TITULOS_NEGATIVOS = [
        "el Cruel", "el Despiadado", "el Oscuro", "el Maldito", "el Traidor",
        "el Corrupto", "el Malvado", "el Siniestro", "el Temido", "el Impio",
        "el Asesino", "el Ladron", "el Hechicero", "el Necromante", "el Demonio"
    ]
    
    # Prefijos para lugares
    PREFIJOS_LUGAR = [
        "Fortaleza", "Castillo", "Torre", "Ruinas", "Templo",
        "Santuario", "Cripta", "Cueva", "Bosque", "Montana",
        "Valle", "Lago", "Rio", "Puente", "Portal",
        "El", "La", "Los", "Las", "Aquel"
    ]
    
    # Sustantivos para lugares
    SUSTANTIVOS_LUGAR = [
        "Olvidado", "Perdido", "Sagrado", "Maldito", "Antiguo",
        "Eterno", "Susurrante", "Silencioso", "Oscuro", "Helado",
        "Ardiente", "Profundo", "Alto", "Bajo", "Verde",
        "Negro", "Blanco", "Rojo", "Azul", "Dorado"
    ]
    
    # Sufijos para lugares
    SUFIJOS_LUGAR = [
        "de la Muerte", "de los Dioses", "del Destino", "de las Sombras", "de la Luz",
        "del Olvido", "de la Esperanza", "del Terror", "de los Caidos", "del Fin",
        "de los Antiguos", "del Poder", "de la Gloria", "del Silencio", "de la Tormenta"
    ]
    
    # Tipos de objetos
    TIPOS_OBJETO = [
        "Espada", "Hacha", "Arco", "Daga", "Varita",
        "Amuleto", "Anillo", "Tunica", "Botas", "Guantes",
        "Escudo", "Casco", "Pocion", "Tomo", "Gema"
    ]
    
    # Adjetivos para objetos
    ADJETIVOS_OBJETO = [
        "Afilado", "Poderoso", "Antiguo", "Maldito", "Bendito",
        "Luminoso", "Oscuro", "Helado", "Ardiente", "Toxico",
        "Sagrado", "Profano", "Eterno", "Efimero", "Legendario"
    ]
    
    # Prefijos para enemigos
    PREFIJOS_ENEMIGO = [
        "Gran", "Pequeno", "Viejo", "Joven", "Salvaje",
        "Hambriento", "Feroz", "Anciano", "Corrupto", "Sombrio",
        "Alfa", "Lider", "Campeon", "Guardian", "Señor"
    ]
    
    # Tipos de enemigos
    TIPOS_ENEMIGO = [
        "Lobo", "Oso", "Araña", "Murcielago", "Rata",
        "Esqueleto", "Zombi", "Fantasma", "Demonio", "Dragon",
        "Goblin", "Orco", "Troll", "Ogro", "Gigante",
        "Sombra", "Espectro", "Wraith", "Banshee", "Liche"
    ]
    
    def __init__(self, seed: WorldSeed):
        self.seed = seed
    
    def generar_nombre_npc(
        self,
        contexto: str,
        genero: Optional[str] = None,
        con_titulo: bool = False,
        titulo_positivo: bool = True
    ) -> str:
        """
        Genera un nombre para un NPC.
        
        Args:
            contexto: Contexto para el RNG
            genero: "masculino", "femenino" o None (aleatorio)
            con_titulo: Si incluir titulo
            titulo_positivo: Si el titulo es positivo
            
        Returns:
            Nombre completo del NPC
        """
        rng = self.seed.get_rng(f"npc_{contexto}")
        
        # Genero
        if genero is None:
            genero = rng.choice(["masculino", "femenino"])
        
        # Nombre
        if genero == "masculino":
            nombre = rng.choice(self.NOMBRES_NPC_MASCULINOS)
        else:
            nombre = rng.choice(self.NOMBRES_NPC_FEMENINOS)
        
        # Apellido
        apellido = rng.choice(self.APELLIDOS)
        
        # Titulo
        titulo = ""
        if con_titulo:
            if titulo_positivo:
                titulo = f", {rng.choice(self.TITULOS_POSITIVOS)}"
            else:
                titulo = f", {rng.choice(self.TITULOS_NEGATIVOS)}"
        
        return f"{nombre} {apellido}{titulo}"
    
    def generar_nombre_lugar(
        self,
        contexto: str,
        tipo: Optional[str] = None
    ) -> str:
        """
        Genera un nombre para un lugar.
        
        Args:
            contexto: Contexto para el RNG
            tipo: Tipo de lugar (fortaleza, templo, etc.) o None
            
        Returns:
            Nombre del lugar
        """
        rng = self.seed.get_rng(f"lugar_{contexto}")
        
        # Estructura del nombre
        estructura = rng.randint(1, 4)
        
        if estructura == 1:
            # Prefijo + Sustantivo
            prefijo = rng.choice(self.PREFIJOS_LUGAR)
            sustantivo = rng.choice(self.SUSTANTIVOS_LUGAR)
            return f"{prefijo} {sustantivo}"
        
        elif estructura == 2:
            # Prefijo + Sustantivo + Sufijo
            prefijo = rng.choice(self.PREFIJOS_LUGAR)
            sustantivo = rng.choice(self.SUSTANTIVOS_LUGAR)
            sufijo = rng.choice(self.SUFIJOS_LUGAR)
            return f"{prefijo} {sustantivo} {sufijo}"
        
        elif estructura == 3:
            # Nombre procedurale
            return self._generar_nombre_silabas(rng, 2, 4)
        
        else:
            # Tipo + Adjetivo
            if tipo:
                tipo_lugar = tipo
            else:
                tipo_lugar = rng.choice(["Fortaleza", "Castillo", "Torre", "Templo", "Santuario"])
            
            adjetivo = rng.choice(self.SUSTANTIVOS_LUGAR)
            return f"{tipo_lugar} {adjetivo}"
    
    def generar_nombre_objeto(
        self,
        contexto: str,
        tipo: Optional[str] = None,
        con_adjetivo: bool = True
    ) -> str:
        """
        Genera un nombre para un objeto.
        
        Args:
            contexto: Contexto para el RNG
            tipo: Tipo de objeto (espada, anillo, etc.) o None
            con_adjetivo: Si incluir adjetivo
            
        Returns:
            Nombre del objeto
        """
        rng = self.seed.get_rng(f"objeto_{contexto}")
        
        # Tipo
        if tipo is None:
            tipo = rng.choice(self.TIPOS_OBJETO)
        
        # Adjetivo
        if con_adjetivo:
            adjetivo = rng.choice(self.ADJETIVOS_OBJETO)
            return f"{tipo} {adjetivo}"
        
        return tipo
    
    def generar_nombre_enemigo(
        self,
        contexto: str,
        tipo: Optional[str] = None,
        con_prefijo: bool = False
    ) -> str:
        """
        Genera un nombre para un enemigo.
        
        Args:
            contexto: Contexto para el RNG
            tipo: Tipo de enemigo o None
            con_prefijo: Si incluir prefijo (Gran, Salvaje, etc.)
            
        Returns:
            Nombre del enemigo
        """
        rng = self.seed.get_rng(f"enemigo_{contexto}")
        
        # Tipo
        if tipo is None:
            tipo = rng.choice(self.TIPOS_ENEMIGO)
        
        # Prefijo
        if con_prefijo:
            prefijo = rng.choice(self.PREFIJOS_ENEMIGO)
            return f"{prefijo} {tipo}"
        
        return tipo
    
    def generar_apodo(
        self,
        contexto: str,
        positivo: bool = True
    ) -> str:
        """
        Genera un apodo.
        
        Args:
            contexto: Contexto para el RNG
            positivo: Si el apodo es positivo
            
        Returns:
            Apodo generado
        """
        rng = self.seed.get_rng(f"apodo_{contexto}")
        
        if positivo:
            return rng.choice(self.TITULOS_POSITIVOS)
        return rng.choice(self.TITULOS_NEGATIVOS)
    
    def _generar_nombre_silabas(
        self,
        rng,
        min_silabas: int = 2,
        max_silabas: int = 4
    ) -> str:
        """Genera un nombre construyendo silabas."""
        num_silabas = rng.randint(min_silabas, max_silabas)
        
        nombre = rng.choice(self.SILABAS_INICIO)
        
        for i in range(1, num_silabas - 1):
            nombre += rng.choice(self.SILABAS_MEDIA)
        
        nombre += rng.choice(self.SILABAS_FIN)
        
        return nombre
    
    def generar_nombre_unico(
        self,
        contexto: str,
        tipo: str = "npc"
    ) -> str:
        """
        Genera un nombre unico generico.
        
        Args:
            contexto: Contexto para el RNG
            tipo: "npc", "lugar", "objeto" o "enemigo"
            
        Returns:
            Nombre generado
        """
        if tipo == "npc":
            return self.generar_nombre_npc(contexto)
        elif tipo == "lugar":
            return self.generar_nombre_lugar(contexto)
        elif tipo == "objeto":
            return self.generar_nombre_objeto(contexto)
        elif tipo == "enemigo":
            return self.generar_nombre_enemigo(contexto)
        else:
            return self._generar_nombre_silabas(self.seed.get_rng(contexto))
