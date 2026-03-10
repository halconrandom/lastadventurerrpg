"""
Script para completar el archivo nombres.py
"""

import os

# Contenido completo del archivo nombres.py
CONTENIDO_COMPLETO = '''"""
Sistema de generacion de nombres procedurales.

Genera nombres unicos para:
- NPCs
- Lugares
- Objetos
- Enemigos
- Titulos y apodos

Sistema hibrido: combina nombres predefinidos con generacion procedural.
"""

from typing import List, Optional, Tuple
from .seed import WorldSeed


class NombreGenerator:
    """Generador de nombres procedurales con sistema hibrido."""
    
    # ============================================================
    # SILABAS PARA CONSTRUCCION PROCEDURAL
    # ============================================================
    
    SILABAS_INICIO = [
        "Ae", "Ba", "Ce", "Da", "El", "Fa", "Go", "Ha", "Il", "Jo",
        "Ka", "La", "Ma", "No", "Or", "Pa", "Qu", "Ra", "Sa", "Th",
        "Ul", "Va", "Wo", "Xa", "Yr", "Zae",
        "Bre", "Cro", "Dra", "Eld", "Fen", "Gor", "Hil", "Irn", "Jar", "Kel",
        "Lor", "Mor", "Nar", "Oth", "Pra", "Qur", "Rho", "Ska", "Tra", "Ulr",
        "Ael", "Bael", "Cael", "Dael", "Eld", "Fael", "Gael", "Hael", "Iael", "Jael",
        "Kael", "Lael", "Mael", "Nael", "Oael", "Pael", "Qael", "Rael", "Sael", "Tael",
        "Zyr", "Vex", "Nyx", "Ryx", "Kyx", "Pyx", "Tyx", "Fyx", "Myx", "Lyx",
        "Aeth", "Baeth", "Caeth", "Daeth", "Eaeth", "Faeth", "Gaeth", "Haeth",
        "Alf", "Bald", "Ein", "Fenr", "Gunn", "Hrod", "Ing", "Jarl", "Knut", "Loki",
        "Magn", "Njor", "Odin", "Ragn", "Sig", "Thor", "Ull", "Val", "Yng", "Zig",
        "Bran", "Cuch", "Dagh", "Eoch", "Fion", "Goll", "Lugh", "Medb", "Nial", "Oeng",
        "Aure", "Cael", "Flav", "Gaiu", "Jul", "Luc", "Marc", "Nerv", "Octa", "Pompe",
        "Aer", "Bel", "Cel", "Dael", "Elen", "Fin", "Gal", "Hel", "Il", "Jael",
        "Kael", "Lael", "Maer", "Nael", "Oer", "Pael", "Quen", "Rael", "Sael", "Thael",
        "Dor", "Grom", "Hamm", "Krag", "Magn", "Nor", "Orn", "Thra", "Ulf", "Vorn",
        "Grok", "Krog", "Mok", "Nok", "Rok", "Sok", "Tok", "Vok", "Zok", "Brog",
    ]
    
    SILABAS_MEDIA = [
        "ba", "ce", "da", "el", "fa", "go", "ha", "il", "jo", "ka",
        "la", "ma", "no", "or", "pa", "ra", "sa", "th", "ul", "va",
        "wen", "xor", "yth", "zal", "bro", "cra", "dre", "eld", "fen",
        "gar", "hil", "irn", "jar", "kel", "lor", "mar", "nar", "oth",
        "ae", "ea", "ia", "oa", "ua", "ei", "ai", "oi", "ui", "au",
        "and", "end", "ind", "ond", "und", "ant", "ent", "int", "ont", "unt",
        "ard", "erd", "ird", "ord", "urd", "art", "ert", "irt", "ort", "urt",
        "ald", "eld", "ild", "old", "uld", "alt", "elt", "ilt", "olt", "ult",
        "ryn", "syn", "tyn", "vyn", "wyn", "xyn", "zyn",
        "ris", "sis", "tis", "vis", "wis", "xis", "zis",
        "ros", "sos", "tos", "vos", "wos", "xos", "zos",
        "gard", "heim", "holm", "land", "mark", "stad", "veld", "wick", "win",
        "ach", "ech", "ich", "och", "uch", "agh", "egh", "igh", "ogh", "ugh",
        "ius", "aeus", "eus", "ius", "ous", "eus", "ius", "aeus",
        "riel", "siel", "thiel", "viel", "wiel", "xiel", "yiel", "ziel",
        "rian", "sian", "thian", "vian", "wian", "xian", "yian", "zian",
        "grim", "krim", "mrim", "nrim", "prim", "rrim", "trim", "vrim",
        "gar", "kar", "mar", "nar", "par", "rar", "tar", "var",
        "gak", "kak", "mak", "nak", "pak", "rak", "tak", "vak", "zak",
    ]
    
    SILABAS_FIN = [
        "a", "on", "us", "ia", "or", "en", "is", "os", "um", "ax",
        "el", "ic", "yn", "ar", "eth", "ion", "wyn",
        "gard", "heim", "holm", "mark", "stad", "thor", "vald", "wyn",
        "son", "sen", "dottir", "sson",
        "us", "ius", "aeus", "eus", "inus", "anus", "enus", "onus", "unus",
        "a", "ia", "ea", "oa", "ua", "ae", "ie", "oe", "ue",
        "ach", "ech", "och", "ugh", "agh", "ann", "enn", "inn", "onn", "unn",
        "iel", "ael", "eel", "iel", "oel", "uel",
        "ian", "aen", "een", "ien", "oen", "uen",
        "thil", "thel", "thal", "thol", "thul",
        "son", "sson", "dottir", "heim", "holm", "gard", "veld",
        "grim", "krim", "mrim", "nrim",
        "gak", "kak", "mak", "nak", "rak", "tak", "vak", "zak",
        "gosh", "kosh", "mosh", "nosh", "rosh", "tosh", "vosh", "zosh",
        "an", "en", "in", "on", "un",
        "ar", "er", "ir", "or", "ur",
        "as", "es", "is", "os", "us",
        "al", "el", "il", "ol", "ul",
        "at", "et", "it", "ot", "ut",
    ]
    
    # ============================================================
    # NOMBRES PREDEFINIDOS - EXPANDIDOS
    # ============================================================
    
    NOMBRES_NPC_MASCULINOS = [
        "Aldric", "Baelin", "Cedric", "Dorian", "Edmund", "Faelan", "Garrick", "Hadrian", "Ivar", "Jorund",
        "Kael", "Lysander", "Magnus", "Nikolai", "Orion", "Percival", "Quillan", "Roland", "Sebastian", "Theron",
        "Ulric", "Viktor", "Wilhelm", "Xavier", "Yorick", "Zachariah",
        "Bjorn", "Erik", "Gunnar", "Harald", "Ingvar", "Johan", "Knute", "Leif", "Magni", "Nils",
        "Olaf", "Ragnar", "Sven", "Torsten", "Ulf", "Vagn", "Yngvar", "Zigfried",
        "Aidan", "Bran", "Cian", "Daire", "Eoin", "Fionn", "Gael", "Hugh", "Iomhar", "Kieran",
        "Liam", "Mael", "Niall", "Oisin", "Padraig", "Quinlan", "Rian", "Sean", "Tadgh", "Uilliam",
        "Aurelius", "Cassius", "Drusus", "Flavius", "Gaius", "Julius", "Lucius", "Marcus", "Nerva", "Octavius",
        "Pompeius", "Quintus", "Romulus", "Septimus", "Tiberius", "Valerius",
        "Aerandir", "Belthil", "Celemir", "Daeron", "Ecthelion", "Finrod", "Glorfindel", "Haldir", "Idril", "Jaerel",
        "Kellindil", "Lindir", "Maedhros", "Nimrodel", "Oropher", "Pengolod", "Quennar", "Rumil", "Thranduil", "Uldir",
        "Dorin", "Gromli", "Hammir", "Kragi", "Magni", "Norin", "Ornim", "Thrain", "Ulfar", "Vornir",
        "Balin", "Dwalin", "Fili", "Kili", "Oin", "Gloin", "Dori", "Nori", "Bifur", "Bofur",
        "Grom", "Krog", "Mok", "Nok", "Rok", "Sok", "Tok", "Vok", "Zok", "Brog",
        "Grommash", "Krogath", "Mokthar", "Nokthar", "Rokthar",
        "Zephyr", "Xerxes", "Valkor", "Thanatos", "Samael", "Raziel", "Phobos", "Orion", "Nyxon", "Moros",
        "Kaelthas", "Jarek", "Ithil", "Hypnos", "Grigori", "Fenris", "Erebos", "Dracon", "Caelum", "Azrael",
        "Arthur", "Benedict", "Conrad", "Duncan", "Edward", "Frederick", "Geoffrey", "Harold", "Ivan", "James",
        "Kenneth", "Lawrence", "Michael", "Nathan", "Oscar", "Patrick", "Quentin", "Robert", "Stephen", "Thomas",
        "Victor", "Walter", "Xenon", "Yves", "Zachary",
        "Achilles", "Beowulf", "Cuchulain", "Diomedes", "Egil", "Fionn", "Gilgamesh", "Hector", "Iason", "Jason",
        "Karna", "Lancelot", "Menelaus", "Nestor", "Odysseus", "Perseus", "Quirinus", "Roland", "Siegfried", "Theseus",
    ]
    
    NOMBRES_NPC_FEMENINOS = [
        "Adelina", "Beatrix", "Cordelia", "Diana", "Elara", "Fiona", "Gwendolyn", "Helena", "Isolde", "Juliana",
        "Katarina", "Lydia", "Mirabel", "Natasha", "Ophelia", "Penelope", "Quinn", "Rosalind", "Seraphina", "Theodora",
        "Ursula", "Valentina", "Willow", "Xanthe", "Yvonne", "Zelda",
        "Astrid", "Bodil", "Cecilia", "Dagny", "Eira", "Freya", "Gudrun", "Helga", "Ingrid", "Jorunn",
        "Kari", "Liv", "Magnhild", "Norna", "Olga", "Petra", "Quenby", "Ragnhild", "Sigrid", "Thyra",
        "Ulla", "Valkyrie", "Ylva", "Zahra",
        "Aine", "Bridget", "Ciara", "Deirdre", "Eileen", "Fiona", "Grainne", "Helen", "Iona", "Keeva",
        "Lile", "Maeve", "Niamh", "Orla", "Pippa", "Quinn", "Rhiannon", "Saoirse", "Tara", "Una",
        "Aurelia", "Claudia", "Drusilla", "Flavia", "Gaia", "Julia", "Livia", "Marcia", "Nerva", "Octavia",
        "Portia", "Quintia", "Romula", "Septima", "Tullia", "Valeria",
        "Aerin", "Belriel", "Celebrian", "Daelin", "Elbereth", "Finduilas", "Galadriel", "Haleth", "Idril", "Jaeriel",
        "Kellian", "Luthien", "Melian", "Nimriel", "Orophin", "Pengoliel", "Quenriel", "Rumiel", "Thriel", "Uldriel",
        "Dora", "Groma", "Hammi", "Kraga", "Magna", "Nora", "Orna", "Thraina", "Ulfa", "Vorna",
        "Balina", "Dwalina", "Fila", "Kila", "Oina", "Gloina", "Doria", "Noria", "Bifura", "Bofura",
        "Groma", "Kroga", "Moka", "Noka", "Roka", "Soka", "Toka", "Voka", "Zoka", "Broga",
        "Gromasha", "Krogatha", "Mokthara", "Nokthara", "Rokthara",
        "Zephyra", "Xerxia", "Valkora", "Thana", "Samara", "Raziela", "Phoebe", "Oriana", "Nyxa", "Mora",
        "Kaeltha", "Jareka", "Ithila", "Hypna", "Grigoria", "Fenrisa", "Ereba", "Draca", "Caela", "Azriela",
        "Alice", "Beatrice", "Charlotte", "Dorothy", "Eleanor", "Florence", "Grace", "Harriet", "Iris", "Jane",
        "Katherine", "Louise", "Margaret", "Nora", "Olivia", "Patricia", "Quinn", "Rose", "Sarah", "Theresa",
        "Victoria", "Wendy", "Xena", "Yvette", "Zara",
        "Athena", "Bellona", "Camilla", "Diana", "Epona", "Freya", "Gaia", "Hera", "Iris", "Juno",
        "Kali", "Luna", "Minerva", "Nemesis", "Ops", "Pax", "Quirina", "Rhea", "Selene", "Terra",
    ]
    
    # ============================================================
    # APELLIDOS - EXPANDIDOS
    # ============================================================
    
    APELLIDOS = [
        "Ashford", "Blackwood", "Cromwell", "Darkhollow", "Everhart", "Fairfax", "Grimshaw", "Holloway", "Ironside", "Jasper",
        "Kingsley", "Lockwood", "Mercer", "Nightingale", "Oakenshield", "Proudfoot", "Quicksilver", "Ravencroft", "Stormwind", "Thornwood",
        "Underhill", "Vance", "Winterborne", "Xavier", "Yarrow",
        "Bjornson", "Eriksson", "Gunnarson", "Haraldson", "Ingvarsson", "Johansson", "Knuteson", "Leifson", "Magnisson", "Nilsson",
        "Olafson", "Ragnarsson", "Svensson", "Torstenson", "Ulfson", "Vagnson", "Yngvarsson", "Zigfriedson",
        "O'Brien", "O'Connor", "O'Neill", "O'Sullivan", "O'Reilly", "O'Donovan", "O'Malley", "O'Doherty", "O'Kelly", "O'Shea",
        "MacDonald", "MacGregor", "MacKenzie", "MacLeod", "MacNeil", "MacPh