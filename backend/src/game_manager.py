import time
from models.personaje import Personaje
from models.stats import Stats


def limpiar_pantalla():
    """Limpia la consola"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_personaje():
    """Flujo completo de creación de personaje"""
    limpiar_pantalla()
    print("=" * 40)
    print("     CREACIÓN DE PERSONAJE")
    print("=" * 40)
    print()

    # Paso 1: Nombre
    nombre = pedir_nombre()
    if nombre is None:
        return None  # Cancelado

    # Paso 2: Género
    genero = pedir_genero()
    if genero is None:
        return None  # Cancelado

    # Paso 3: Dificultad
    dificultad = pedir_dificultad()
    if dificultad is None:
        return None  # Cancelado

    # Paso 4: Resumen y confirmación
    while True:
        if not mostrar_resumen(nombre, genero, dificultad):
            return None  # Cancelado

        opcion = input("¿Confirmar? (S)í / (E)ditar / (C)ancelar: ").lower()

        if opcion == "s" or opcion == "si":
            break
        elif opcion == "e" or opcion == "editar":
            nombre, genero, dificultad = editar_personaje(nombre, genero, dificultad)
        elif opcion == "c" or opcion == "cancelar":
            return None

    # Crear personaje
    personaje = Personaje(nombre, genero, dificultad)

    print(f"\n¡Bienvenido, {nombre}!")
    print("Tu aventura está por comenzar...")
    time.sleep(2)

    return personaje


def pedir_nombre():
    """Pide el nombre del personaje con validación"""
    while True:
        print("¿Cuál es tu nombre?")
        print("(Mínimo 3 caracteres, o escribe 'cancelar' para volver)")
        print()

        nombre = input("Nombre: ").strip()

        if nombre.lower() == "cancelar":
            return None

        if len(nombre) < 3:
            print("\nEl nombre debe tener al menos 3 caracteres.")
            time.sleep(1)
            limpiar_pantalla()
            print("=" * 40)
            print("     CREACIÓN DE PERSONAJE")
            print("=" * 40)
            print()
            continue

        return nombre


def pedir_genero():
    """Pide el género del personaje"""
    limpiar_pantalla()
    print("=" * 40)
    print("     CREACIÓN DE PERSONAJE")
    print("=" * 40)
    print()
    print("Selecciona tu género:")
    print()
    print("1. Masculino")
    print("2. Femenino")
    print("3. No especificar")
    print("4. Cancelar")
    print()

    while True:
        opcion = input("Selecciona (1-4): ").strip()

        if opcion == "1":
            return "masculino"
        elif opcion == "2":
            return "femenino"
        elif opcion == "3":
            return "no_especificar"
        elif opcion == "4":
            return None
        else:
            print("Opción inválida. Elige 1-4.")


def pedir_dificultad():
    """Pide la dificultad del juego"""
    limpiar_pantalla()
    print("=" * 40)
    print("     CREACIÓN DE PERSONAJE")
    print("=" * 40)
    print()
    print("Selecciona la dificultad:")
    print()
    print("1. Fácil")
    print("   └ HP +20%, enemigos -10% daño")
    print()
    print("2. Normal [RECOMENDADO]")
    print("   └ Sin modificadores")
    print()
    print("3. Difícil")
    print("   └ HP -10%, enemigos +10% daño")
    print()
    print("4. Cancelar")
    print()

    while True:
        opcion = input("Selecciona (1-4): ").strip()

        if opcion == "1":
            return "facil"
        elif opcion == "2":
            return "normal"
        elif opcion == "3":
            return "dificil"
        elif opcion == "4":
            return None
        else:
            print("Opción inválida. Elige 1-4.")


def mostrar_resumen(nombre, genero, dificultad):
    """Muestra el resumen del personaje antes de confirmar"""
    limpiar_pantalla()
    print("╔" + "═" * 38 + "╗")
    print("║" + " RESUMEN DEL PERSONAJE".center(38) + "║")
    print("╠" + "═" * 38 + "╣")
    print(f"║{' Nombre:':<18}{nombre:>19} ║")
    print(f"║{' Género:':<18}{formatear_genero(genero):>19} ║")
    print(f"║{' Dificultad:':<18}{formatear_dificultad(dificultad):>19} ║")
    print("╠" + "═" * 38 + "╣")
    print("║" + " STATS INICIALES".center(38) + "║")
    print("╠" + "═" * 38 + "╣")

    # Calcular HP según dificultad
    hp_base = Stats.HP_BASE_INICIAL
    mods = Stats.MODIFICADORES_DIFICULTAD[dificultad]
    hp_final = int(hp_base * mods["hp_mod"])

    print(f"║{' HP:':<18}{f'{hp_final}':>19} ║")
    print(f"║{' ATK:':<18}{f'{Stats.ATK_BASE_INICIAL}':>19} ║")
    print(f"║{' DEF:':<18}{f'{Stats.DEF_BASE_INICIAL}%':>19} ║")
    print(f"║{' Velocidad:':<18}{f'{Stats.VELOCIDAD_BASE_INICIAL}':>19} ║")
    print(f"║{' Crítico:':<18}{f'{Stats.CRITICO_BASE_INICIAL}%':>19} ║")
    print(f"║{' Evasión:':<18}{f'{Stats.EVASION_BASE_INICIAL}%':>19} ║")
    print(f"║{' Mana:':<18}{f'{Stats.MANA_BASE_INICIAL}':>19} ║")
    print(f"║{' Stamina:':<18}{f'{Stats.STAMINA_BASE_INICIAL}':>19} ║")
    print("╠" + "═" * 38 + "╣")
    print("║" + " INVENTARIO INICIAL".center(38) + "║")
    print("╠" + "═" * 38 + "╣")
    print("║" + " Ropajes básicos (cosmético)".center(38) + "║")
    print("╚" + "═" * 38 + "╝")
    print()

    return True


def formatear_genero(genero):
    """Formatea el género para mostrar"""
    generos = {
        "masculino": "Masculino",
        "femenino": "Femenino",
        "no_especificar": "No especificar"
    }
    return generos.get(genero, "No especificar")


def formatear_dificultad(dificultad):
    """Formatea la dificultad para mostrar"""
    dificultades = {
        "facil": "Fácil",
        "normal": "Normal",
        "dificil": "Difícil"
    }
    return dificultades.get(dificultad, "Normal")


def editar_personaje(nombre, genero, dificultad):
    """Permite editar los datos del personaje"""
    limpiar_pantalla()
    print("=" * 40)
    print("     EDITAR PERSONAJE")
    print("=" * 40)
    print()
    print("1. Cambiar nombre")
    print("2. Cambiar género")
    print("3. Cambiar dificultad")
    print("4. Volver")
    print()

    opcion = input("Selecciona: ").strip()

    if opcion == "1":
        nuevo_nombre = pedir_nombre()
        if nuevo_nombre:
            nombre = nuevo_nombre
    elif opcion == "2":
        nuevo_genero = pedir_genero()
        if nuevo_genero:
            genero = nuevo_genero
    elif opcion == "3":
        nueva_dificultad = pedir_dificultad()
        if nueva_dificultad:
            dificultad = nueva_dificultad

    return nombre, genero, dificultad
