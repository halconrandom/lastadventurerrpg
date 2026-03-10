"""
Sistema de generación de nombres procedimentales.

Genera nombres únicos para:
- NPCs
- Lugares
- Objetos
- Enemigos
- Títulos y apodos

Sistema híbrido: combina nombres predefinidos con generación procedural.
"""

import random
from typing import List, Optional, Tuple


class NombreGenerator:
    """Generador de nombres procedimentales con sistema híbrido."""

    # Probabilidad de usar nombre predefinido vs procedural
    PROB_PREDEFINIDO = 0.60

    # ============================================================
    # SÍLABAS PARA CONSTRUCCIÓN PROCEDURAL
    # ============================================================

    SILABAS_INICIO = [
        "Ae",
        "Ba",
        "Ce",
        "Da",
        "El",
        "Fa",
        "Go",
        "Ha",
        "Il",
        "Jo",
        "Ka",
        "La",
        "Ma",
        "No",
        "Or",
        "Pa",
        "Qu",
        "Ra",
        "Sa",
        "Th",
        "Ul",
        "Va",
        "Wo",
        "Xa",
        "Yr",
        "Zae",
        "Bre",
        "Cro",
        "Dra",
        "Eld",
        "Fen",
        "Gor",
        "Hil",
        "Irn",
        "Jar",
        "Kel",
        "Lor",
        "Mor",
        "Nar",
        "Oth",
        "Pra",
        "Qur",
        "Rho",
        "Ska",
        "Tra",
        "Ulr",
        "Ael",
        "Bael",
        "Cael",
        "Dael",
        "Eld",
        "Fael",
        "Gael",
        "Hael",
        "Iael",
        "Jael",
        "Kael",
        "Lael",
        "Mael",
        "Nael",
        "Oael",
        "Pael",
        "Qael",
        "Rael",
        "Sael",
        "Tael",
        "Zyr",
        "Vex",
        "Nyx",
        "Ryx",
        "Kyx",
        "pyx",
        "Tyx",
        "Fyx",
        "Myx",
        "Lyx",
        "Aeth",
        "Baeth",
        "Caeth",
        "Daeth",
        "Eaeth",
        "Faeth",
        "Gaeth",
        "Haeth",
        "Alf",
        "Bald",
        "Ein",
        "Fenr",
        "Gunn",
        "Hrod",
        "Ing",
        "Jarl",
        "Knut",
        "Loki",
        "Magn",
        "Njor",
        "Odin",
        "Ragn",
        "Sig",
        "Thor",
        "Ull",
        "Val",
        "Yng",
        "Zig",
        "Bran",
        "Cuch",
        "Dagh",
        "Eoch",
        "Fion",
        "Goll",
        "Lugh",
        "Medb",
        "Nial",
        "Oeng",
    ]

    SILABAS_MEDIA = [
        "ba",
        "ce",
        "da",
        "el",
        "fa",
        "go",
        "ha",
        "il",
        "jo",
        "ka",
        "la",
        "ma",
        "no",
        "or",
        "pa",
        "ra",
        "sa",
        "th",
        "ul",
        "va",
        "wen",
        "xor",
        "yth",
        "zal",
        "bro",
        "cra",
        "dre",
        "eld",
        "fen",
        "gar",
        "hil",
        "irn",
        "jar",
        "kel",
        "lor",
        "mar",
        "nar",
        "oth",
        "ae",
        "ea",
        "ia",
        "oa",
        "ua",
        "ei",
        "ai",
        "oi",
        "ui",
        "au",
        "and",
        "end",
        "ind",
        "ond",
        "und",
        "ant",
        "ent",
        "int",
        "ont",
        "unt",
        "ard",
        "erd",
        "ird",
        "ord",
        "urd",
        "art",
        "ert",
        "irt",
        "ort",
        "urt",
        "ald",
        "eld",
        "ild",
        "old",
        "uld",
        "alt",
        "elt",
        "ilt",
        "olt",
        "ult",
    ]

    SILABAS_FIN = [
        "a",
        "on",
        "us",
        "ia",
        "or",
        "en",
        "is",
        "os",
        "um",
        "ax",
        "el",
        "ic",
        "yn",
        "ar",
        "eth",
        "ion",
        "wyn",
        "son",
        "sen",
        "dottir",
        "sson",
        "us",
        "ius",
        "aeus",
        "eus",
        "inus",
        "anus",
        "enus",
        "onus",
        "unus",
    ]

    # ============================================================
    # NOMBRES PREDEFINIDOS - EXPANDIDOS
    # ============================================================

    NOMBRES_NPC_MASCULINOS = [
        "Aldric",
        "Baelin",
        "Cedric",
        "Dorian",
        "Edmund",
        "Faelan",
        "Garrick",
        "Hadrian",
        "Ivar",
        "Jorund",
        "Kael",
        "Lysander",
        "Magnus",
        "Nikolai",
        "Orion",
        "Percival",
        "Quillan",
        "Roland",
        "Sebastian",
        "Theron",
        "Ulric",
        "Viktor",
        "Wilhelm",
        "Xavier",
        "Yorick",
        "Zachariah",
        "Bjorn",
        "Erik",
        "Gunnar",
        "Harald",
        "Ingvar",
        "Johan",
        "Knute",
        "Leif",
        "Magni",
        "Nils",
        "Olaf",
        "Ragnar",
        "Sven",
        "Torsten",
        "Ulf",
        "Vagn",
        "Yngvar",
        "Zigfried",
        "Aidan",
        "Bran",
        "Cian",
        "Daire",
        "Eoin",
        "Fionn",
        "Gael",
        "Hugh",
        "Iomhar",
        "Kieran",
        "Liam",
        "Mael",
        "Niall",
        "Oisin",
        "Padraig",
        "Quinlan",
        "Rian",
        "Sean",
        "Tadgh",
        "Uilliam",
        "Aurelius",
        "Cassius",
        "Drusus",
        "Flavius",
        "Gaius",
        "Julius",
        "Lucius",
        "Marcus",
        "Nerva",
        "Octavius",
        "Aerandir",
        "Belthil",
        "Celemir",
        "Daeron",
        "Ecthelion",
        "Finrod",
        "Glorfindel",
        "Haldir",
        "Idril",
        "Jaerel",
        "Dorin",
        "Gromli",
        "Hammir",
        "Kragi",
        "Magni",
        "Norin",
        "Ornim",
        "Thrain",
        "Ulfar",
        "Vornir",
        "Balin",
        "Dwalin",
        "Fili",
        "Kili",
        "Oin",
        "Gloin",
        "Dori",
        "Nori",
        "Bifur",
        "Bofur",
        "Grom",
        "Krog",
        "Mok",
        "Nok",
        "Rok",
        "Sok",
        "Tok",
        "Vok",
        "Zok",
        "Brog",
        "Arthur",
        "Benedict",
        "Conrad",
        "Duncan",
        "Edward",
        "Frederick",
        "Geoffrey",
        "Harold",
        "Ivan",
        "James",
        "Kenneth",
        "Lawrence",
        "Michael",
        "Nathan",
        "Oscar",
        "Patrick",
        "Quentin",
        "Robert",
        "Stephen",
        "Thomas",
        "Victor",
        "Walter",
        "Xenon",
        "Yves",
        "Zachary",
        "Roderick",
        "Alaric",
        "Godfrey",
        "Baldwin",
        "Nigel",
        "Herman",
        "Bertram",
        "Willem",
        "Reinhold",
        "Dietrich",
        "Caius",
        "Lucian",
        "Julian",
        "Dominic",
        "Fabian",
        "Gareth",
        "Tristan",
        "Gavin",
        "Marcus",
        "Julian",
    ]

    NOMBRES_NPC_FEMENINOS = [
        "Adelina",
        "Beatrix",
        "Cordelia",
        "Diana",
        "Elara",
        "Fiona",
        "Gwendolyn",
        "Helena",
        "Isolde",
        "Juliana",
        "Katarina",
        "Lydia",
        "Mirabel",
        "Natasha",
        "Ophelia",
        "Penelope",
        "Quinn",
        "Rosalind",
        "Seraphina",
        "Theodora",
        "Ursula",
        "Valentina",
        "Willow",
        "Xanthe",
        "Yvonne",
        "Zelda",
        "Astrid",
        "Bodil",
        "Cecilia",
        "Dagny",
        "Eira",
        "Freya",
        "Gudrun",
        "Helga",
        "Ingrid",
        "Jorunn",
        "Kari",
        "Liv",
        "Magnhild",
        "Norna",
        "Olga",
        "Petra",
        "Quenby",
        "Ragnhild",
        "Sigrid",
        "Thyra",
        "Aine",
        "Bridget",
        "Ciara",
        "Deirdre",
        "Eileen",
        "Fiona",
        "Grainne",
        "Helen",
        "Iona",
        "Keeva",
        "Aurelia",
        "Claudia",
        "Drusilla",
        "Flavia",
        "Gaia",
        "Julia",
        "Livia",
        "Marcia",
        "Nerva",
        "Octavia",
        "Aerin",
        "Belriel",
        "Celebrian",
        "Daelin",
        "Elbereth",
        "Finduilas",
        "Galadriel",
        "Haleth",
        "Idril",
        "Jaeriel",
        "Alice",
        "Beatrice",
        "Charlotte",
        "Dorothy",
        "Eleanor",
        "Florence",
        "Grace",
        "Harriet",
        "Iris",
        "Jane",
        "Katherine",
        "Louise",
        "Margaret",
        "Nora",
        "Olivia",
        "Patricia",
        "Quinn",
        "Rose",
        "Sarah",
        "Theresa",
        "Victoria",
        "Wendy",
        "Xena",
        "Yvette",
        "Zara",
        "Eowyn",
        "Arwen",
        "Luthien",
        "Melian",
        "Nimrodel",
        "Taewen",
        "Yvaine",
        "Oriana",
        "Seraphina",
        "Celestine",
    ]

    # ============================================================
    # APELLIDOS - EXPANDIDOS
    # ============================================================

    APELLIDOS = [
        "Ashford",
        "Blackwood",
        "Cromwell",
        "Darkhollow",
        "Everhart",
        "Fairfax",
        "Grimshaw",
        "Holloway",
        "Ironside",
        "Jasper",
        "Kingsley",
        "Lockwood",
        "Mercer",
        "Nightingale",
        "Oakenshield",
        "Proudfoot",
        "Quicksilver",
        "Ravencroft",
        "Stormwind",
        "Thornwood",
        "Underhill",
        "Vance",
        "Winterborne",
        "Xavier",
        "Yarrow",
        "Bjornson",
        "Eriksson",
        "Gunnarson",
        "Haraldson",
        "Ingvarsson",
        "Johansson",
        "Knuteson",
        "Leifson",
        "Magnisson",
        "Nilsson",
        "Olafson",
        "Ragnarsson",
        "Svensson",
        "Torstenson",
        "Ulfson",
        "Vagnson",
        "Yngvarsson",
        "O'Brien",
        "O'Connor",
        "O'Neill",
        "O'Sullivan",
        "O'Reilly",
        "O'Donovan",
        "O'Malley",
        "O'Doherty",
        "O'Kelly",
        "O'Shea",
        "MacDonald",
        "MacGregor",
        "MacKenzie",
        "MacLeod",
        "MacNeil",
        "MacPherson",
        "MacQuarrie",
        "MacRae",
        "MacSween",
        "MacTavish",
        "Stoneforge",
        "Ironheart",
        "Silverleaf",
        "Goldweaver",
        "Brightblade",
        "Darkfrost",
        "Swiftwind",
        "Flameheart",
        "Frostborn",
        "Stormcaller",
        "vonDrachen",
        "vonSchatten",
        "vonEisen",
        "vonBurg",
        "vonKönig",
        "vonReich",
        "vonWald",
        "vonBerg",
        "vonTal",
        "vonDunkel",
    ]

    # ============================================================
    # TÍTULOS Y APODOS
    # ============================================================

    TITULOS_MASCULINOS = [
        "El Sabio",
        "El Valiente",
        "El Guerrero",
        "El Mago",
        "El Herrero",
        "El Cazador",
        "El Explorador",
        "El Ladron",
        "El Guerrero",
        "El Berserker",
        "El Paladin",
        "El Clerigo",
        "El Druida",
        "El Bardo",
        "de la Luz",
        "de las Sombras",
        "del Trueno",
        "de la Tormenta",
        "del Viento",
        "del Mar",
        "de la Montaña",
    ]

    TITULOS_FEMENINOS = [
        "La Sabia",
        "La Valiente",
        "La Guerrera",
        "La Maga",
        "La Herrera",
        "La Cazadora",
        "La Exploradora",
        "La Ladrona",
        "La Berserker",
        "La Paladina",
        "La Cleriga",
        "La Druida",
        "La Barda",
        "de la Luz",
        "de las Sombras",
        "del Trueno",
        "de la Tormenta",
        "del Viento",
        "del Mar",
        "de la Montaña",
    ]

    # ============================================================
    # NOMBRES DE LUGARES - PREFIJOS
    # ============================================================

    PREFIJOS_LUGARES = {
        "pueblo": [
            "Aldea",
            "Pueblo",
            "Caserío",
            "Hamlet",
            "Villa",
            "Villorrio",
            "Aldea",
            "Poblado",
            "Refugio",
            "Coto",
        ],
        "ciudad": [
            "Ciudad",
            "Fortaleza",
            "Puerto",
            "Villa",
            "Bastión",
            "Cidadela",
            "Metrópolis",
            "Urbe",
        ],
        "capital": ["Capital", "Metrópolis", "Ciudadela", "Imperial", "Sede", "Trono"],
        "mazmorra": [
            "Cueva",
            "Ruinas",
            "Mazmorra",
            "Cripta",
            "Templo",
            "Sótano",
            "Abismo",
            "Pozo",
            "Laberinto",
        ],
        "poi": [
            "Santuario",
            "Monolito",
            "Fuente",
            "Árbol",
            "Piedra",
            "Estatua",
            "Altar",
            "Pozo",
            "Túmulo",
        ],
    }

    # ============================================================
    # NOMBRES DE LUGARES - ADJETIVOS
    # ============================================================

    ADJETIVOS_LUGARES = [
        "Antiguo",
        "Olvidado",
        "Sagrado",
        "Maldito",
        "Eterno",
        "Sombrío",
        "Luminoso",
        "Helado",
        "Ardiente",
        "Verde",
        "Dorado",
        "Plateado",
        "Carmesí",
        "Azul",
        "Negro",
        "Blanco",
        "Gris",
        "Púrpura",
        "Esmeralda",
        "Rubí",
        "Perdido",
        "Abandonado",
        "Encantado",
        "Embrujado",
        "Protegido",
        "Oculto",
        "Secreto",
        "Misterioso",
        "Legendario",
        "Fantasmal",
        "Silencioso",
        "Trágico",
        "Santo",
        "Profano",
        "Divino",
    ]

    # ============================================================
    # NOMBRES DE LUGARES - SUSTANTIVOS
    # ============================================================

    SUSTANTIVOS_LUGARES = {
        "pueblo": [
            "del Roble",
            "del Río",
            "de la Colina",
            "del Bosque",
            "del Valle",
            "de la Ladera",
            "del Prado",
            "de las Flores",
            "del Viento",
            "de la Lluvia",
        ],
        "ciudad": [
            "de Plata",
            "del Hierro",
            "de la Luz",
            "de las Tormentas",
            "del Mar",
            "del Sol",
            "de la Luna",
            "de las Estrellas",
            "del Trueno",
            "de la Aurora",
        ],
        "capital": [
            "de los Reyes",
            "Imperial",
            "del Trono",
            "Eterna",
            "de la Corona",
            "del Reino",
            "de los Cielos",
            "de la Victoria",
            "del Destino",
            "Eterna",
        ],
        "mazmorra": [
            "de los Caídos",
            "del Destino",
            "de las Sombras",
            "del Dragón",
            "del Terror",
            "de la Muerte",
            "del Vacío",
            "de la Locura",
            "del Infierno",
            "de los Milagros",
        ],
        "poi": [
            "de los Deseos",
            "del Viento",
            "de la Luna",
            "del Sol",
            "de las Estrellas",
            "del Silencio",
            "de la Verdad",
            "de la Vida",
            "de la Muerte",
            "del Tiempo",
        ],
    }

    # ============================================================
    # CONSTRUCTOR
    # ============================================================

    def __init__(self, seed: Optional[int] = None):
        """Inicializa el generador de nombres."""
        self.seed = seed if seed else random.randint(0, 999999)
        random.seed(self.seed)

    # ============================================================
    # MÉTODOS DE GENERACIÓN HÍBRIDA
    # ============================================================

    def _es_predefinido(self) -> bool:
        """Determina si se usa nombre predefinido o procedural."""
        return random.random() < self.PROB_PREDEFINIDO

    def generar_nombre_npc(
        self,
        genero: str = "masculino",
        con_apellido: bool = True,
        con_titulo: bool = False,
    ) -> str:
        """
        Genera un nombre para NPC con sistema híbrido.

        Args:
            genero: 'masculino' o 'femenino'
            con_apellido: Si incluye apellido
            con_titulo: Si incluye título

        Returns:
            Nombre generado
        """
        nombres = (
            self.NOMBRES_NPC_MASCULINOS
            if genero == "masculino"
            else self.NOMBRES_NPC_FEMENINOS
        )

        if self._es_predefinido():
            nombre = random.choice(nombres)
        else:
            nombre = self._generar_nombre_procedural(len(nombre) if nombre else 3)

        resultado = [nombre]

        if con_apellido and random.random() < 0.7:
            resultado.append(random.choice(self.APELLIDOS))

        if con_titulo:
            titulos = (
                self.TITULOS_MASCULINOS
                if genero == "masculino"
                else self.TITULOS_FEMENINOS
            )
            resultado.insert(0, random.choice(titulos))

        return " ".join(resultado)

    def generar_nombre_lugar(
        self, tipo: str = "pueblo", con_adjetivo: bool = True
    ) -> str:
        """
        Genera un nombre para lugar con sistema híbrido.

        Args:
            tipo: Tipo de lugar (pueblo, ciudad, capital, mazmorra, poi)
            con_adjetivo: Si incluye adjetivo en lugar de sustantivo

        Returns:
            Nombre generado
        """
        prefijos = self.PREFIJOS_LUGARES.get(tipo, ["Lugar"])
        sustantivos = self.SUSTANTIVOS_LUGARES.get(tipo, ["Misterioso"])

        if self._es_predefinido():
            prefijo = random.choice(prefijos)
        else:
            prefijo = self._generar_nombre_procedural(2, usar_mayuscula=True)

        if con_adjetivo and random.random() < 0.5:
            adjetivo = random.choice(self.ADJETIVOS_LUGARES)
            return f"{prefijo} {adjetivo}"
        else:
            sustantivo = random.choice(sustantivos)
            return f"{prefijo} {sustantivo}"

    def _generar_nombre_procedural(
        self, silabas: int = 3, usar_mayuscula: bool = False
    ) -> str:
        """
        Genera un nombre procedural usando sílabas.

        Args:
            silabas: Número de sílabas
            usar_mayuscula: Si la primera letra es mayúscula

        Returns:
            Nombre procedural
        """
        nombre = random.choice(self.SILABAS_INICIO)

        for _ in range(silabas - 1):
            nombre += random.choice(self.SILABAS_MEDIA)

        nombre += random.choice(self.SILABAS_FIN)

        if usar_mayuscula:
            nombre = nombre.capitalize()

        return nombre

    def generar_nombre_objeto(self, tipo: str = "arma") -> str:
        """
        Genera un nombre para objeto/arma.

        Args:
            tipo: Tipo de objeto

        Returns:
            Nombre generado
        """
        prefijos = [
            "Espada",
            "Arco",
            "Daga",
            "Escudo",
            "Armadura",
            "Anillo",
            "Amuleto",
            "Báculo",
        ]
        adjetivos = ["del", "de la", "de las", "del"]
        sustantivos = [
            "Luz",
            "Sombra",
            "Tormenta",
            "Fuego",
            "Hielo",
            "Trueno",
            "Muerte",
            "Vida",
            "Gloria",
            "Victoria",
            "Derrota",
            "Locura",
            "Sabiduría",
            "Poder",
            "Justicia",
        ]

        if self._es_predefinido():
            return f"{random.choice(prefijos)} {random.choice(adjetivos)} {random.choice(sustantivos)}"
        else:
            return f"{random.choice(prefijos)} {self._generar_nombre_procedural(2)}"


# Instancia global
generador_nombres = NombreGenerator()
