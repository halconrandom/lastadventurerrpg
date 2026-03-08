from models.personaje import Personaje
from models.stats import Stats

def validar_datos_personaje(nombre, genero, dificultad):
    """Valida los datos básicos de un personaje"""
    if not nombre or len(nombre) < 3:
        return False, "El nombre debe tener al menos 3 caracteres"
    
    generos_validos = ["masculino", "femenino", "no_especificar"]
    if genero not in generos_validos:
        return False, f"Género inválido. Debe ser uno de: {generos_validos}"
    
    dificultades_validas = ["facil", "normal", "dificil"]
    if dificultad not in dificultades_validas:
        return False, f"Dificultad inválida. Debe ser una de: {dificultades_validas}"
    
    return True, "Datos válidos"

def crear_nuevo_personaje(nombre, genero="no_especificar", dificultad="normal"):
    """Crea una instancia de Personaje validada para la API"""
    valido, mensaje = validar_datos_personaje(nombre, genero, dificultad)
    if not valido:
        return None, mensaje
    
    try:
        personaje = Personaje(nombre, genero, dificultad)
        return personaje, "Personaje creado con éxito"
    except Exception as e:
        return None, f"Error al crear personaje: {str(e)}"

# Funciones de utilidad para el juego que no dependen de la UI
def calcular_recompensa_exploracion(nivel_personaje):
    """Calcula oro y exp aleatoria basada en nivel (placeholder)"""
    import random
    oro = random.randint(5, 15) * nivel_personaje
    exp = random.randint(20, 50) * nivel_personaje
    return oro, exp

