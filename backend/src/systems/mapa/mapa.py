"""
Sistema de Mapa Mundial - Last Adventurer

Integra tiles, chunks, ubicaciones y rutas para crear
el mapa global del juego.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
import random

from systems.mapa.tile import Tile, EstadoVisibilidad, calcular_costo_movimiento
from systems.mapa.chunk import Chunk, GestorChunks
from systems.mapa.ubicacion import Ubicacion, UbicacionGenerator, TipoUbicacion
from systems.mapa.ruta import Ruta, RutaGenerator


@dataclass
class MapaMundo:
    """
    Mapa mundial del juego.
    
    Gestiona:
    - Tiles y chunks
    - Ubicaciones (pueblos, ciudades, etc.)
    - Rutas entre ubicaciones
    - Generación procedural
    - Persistencia
    """
    seed: any  # WorldSeed
    gestor_chunks: GestorChunks = field(default_factory=GestorChunks)
    ubicaciones: Dict[str, Ubicacion] = field(default_factory=dict)
    rutas: Dict[str, Ruta] = field(default_factory=dict)
    
    # Generadores
    ubicacion_gen: UbicacionGenerator = None
    ruta_gen: RutaGenerator = None
    
    # Estado
    posicion_jugador: Tuple[int, int] = (0, 0)  # Posición MUNDAL (tiles de 1km)
    posicion_local: Tuple[int, int] = (5, 5)   # Posición LOCAL dentro del tile actual (subtiles de 10m, 0-9)
    ubicacion_actual: Optional[str] = None  # ID de ubicación actual
    
    # Modo de mapa actual
    modo_mapa: str = "mundial"  # "mundial" o "local"
    
    def __post_init__(self):
        """Inicializa los generadores."""
        self.ubicacion_gen = UbicacionGenerator(self.seed)
        self.ruta_gen = RutaGenerator(self.seed)
    
    # ==================== GENERACIÓN ====================
    
    def generar_mundo_inicial(
        self,
        cantidad_pueblos: Tuple[int, int] = (10, 20),
        cantidad_ciudades: Tuple[int, int] = (3, 5),
        cantidad_capitales: Tuple[int, int] = (1, 2),
        cantidad_mazmorras: Tuple[int, int] = (20, 40),
        cantidad_pois: Tuple[int, int] = (30, 50),
        radio_mundo: int = 100
    ) -> None:
        """
        Genera el mundo inicial con ubicaciones y rutas.
        
        Args:
            cantidad_*: Tuplas (min, max) para cada tipo de ubicación
            radio_mundo: Radio del mundo en tiles
        """
        # Generar ubicaciones
        nuevas_ubicaciones = self.ubicacion_gen.generar_ubicaciones_iniciales(
            cantidad_pueblos=cantidad_pueblos,
            cantidad_ciudades=cantidad_ciudades,
            cantidad_capitales=cantidad_capitales,
            cantidad_mazmorras=cantidad_mazmorras,
            cantidad_pois=cantidad_pois,
            radio_mundo=radio_mundo
        )
        
        # Agregar al diccionario
        for ubicacion in nuevas_ubicaciones:
            self.ubicaciones[ubicacion.id] = ubicacion
        
        # Generar rutas
        nuevas_rutas = self.ruta_gen.generar_rutas_ubicaciones(
            list(self.ubicaciones.values())
        )
        
        # Agregar al diccionario
        for ruta in nuevas_rutas:
            self.rutas[ruta.id] = ruta
        
        # Generar tiles para las ubicaciones
        for ubicacion in self.ubicaciones.values():
            self._generar_tile_ubicacion(ubicacion)
    
    def _generar_tile_ubicacion(self, ubicacion: Ubicacion) -> None:
        """Genera el tile para una ubicación."""
        tile = Tile(
            x=ubicacion.x,
            y=ubicacion.y,
            bioma=ubicacion.bioma,
            ubicacion_id=ubicacion.id,
            visibilidad=EstadoVisibilidad.NO_DESCUBIERTO
        )
        
        # Generar sub-tiles (lazy - se generan cuando el jugador entra al tile)
        # Los sub-tiles se generan automáticamente cuando se accede a ellos
        
        self.gestor_chunks.set_tile(tile)
    
    def generar_chunk(self, chunk_x: int, chunk_y: int) -> Chunk:
        """
        Genera un chunk proceduralmente.
        
        Args:
            chunk_x: Coordenada X del chunk
            chunk_y: Coordenada Y del chunk
        
        Returns:
            Chunk generado
        """
        chunk = Chunk(x=chunk_x, y=chunk_y)
        
        # Coordenadas base
        base_x, base_y = self.gestor_chunks.chunk_a_tile_base(chunk_x, chunk_y)
        
        # Generar cada tile
        for local_y in range(3):
            for local_x in range(3):
                x = base_x + local_x
                y = base_y + local_y
                
                # Generar tile
                tile = self._generar_tile(x, y)
                chunk.set_tile(local_x, local_y, tile)
        
        chunk.generado = True
        self.gestor_chunks.agregar_chunk(chunk)
        
        return chunk
    
    def _generar_tile(self, x: int, y: int) -> Tile:
        """Genera un tile proceduralmente."""
        contexto = f"tile_{x}_{y}"
        rng = self.seed.get_rng(contexto)
        
        # Biomas disponibles
        biomas = [
            "bosque_ancestral",
            "paramo_marchito",
            "pantano_sombrio",
            "montanas_heladas",
            "desierto_ceniza",
            "ruinas_subterraneas",
            "pradera",
            "costa"
        ]
        
        # Seleccionar bioma
        bioma = rng.choice(biomas)
        
        # Terreno
        terrenos = {
            "bosque_ancestral": ["bosque_denso", "claro", "riachuelo"],
            "paramo_marchito": ["tierra_yerma", "tumbas", "niebla"],
            "pantano_sombrio": ["cienaga", "arboles_muertos", "aguas_negras"],
            "montanas_heladas": ["pico_nevado", "glaciar", "cueva"],
            "desierto_ceniza": ["ceniza", "crater", "oasis"],
            "ruinas_subterraneas": ["pasillo", "sala", "cripta"],
            "pradera": ["campo", "colina", "granja"],
            "costa": ["playa", "acantilado", "puerto"]
        }
        
        terreno = rng.choice(terrenos.get(bioma, ["normal"]))
        
        # Costo de movimiento
        costo = calcular_costo_movimiento(bioma, terreno)
        
        return Tile(
            x=x,
            y=y,
            bioma=bioma,
            terreno=terreno,
            costo_movimiento=costo,
            visibilidad=EstadoVisibilidad.NO_DESCUBIERTO
        )
    
    # ==================== MOVIMIENTO ====================
    
    def mover_jugador(self, x: int, y: int) -> Dict:
        """
        Mueve al jugador a una nueva posición MUNDIAL.
        
        IMPORTANTE: Este movimiento es en el mapa mundial (tiles de 1km).
        NO afecta los sub-tiles locales.
        
        Args:
            x: Nueva coordenada X (tiles)
            y: Nueva coordenada Y (tiles)
        
        Returns:
            Diccionario con información del movimiento
        """
        posicion_anterior = self.posicion_jugador
        self.posicion_jugador = (x, y)
        
        # Resetear posición local al cambiar de tile mundial
        self.posicion_local = (5, 5)
        
        # Actualizar chunks
        chunks_a_cargar = self.gestor_chunks.actualizar_posicion_jugador(x, y)
        
        # Cargar chunks necesarios
        for chunk_x, chunk_y in chunks_a_cargar:
            self.generar_chunk(chunk_x, chunk_y)
        
        # Descubrir tile MUNDIAL
        tile = self.gestor_chunks.get_tile(x, y)
        if tile:
            tile.descubrir()
        
        # Calcular tiempo de viaje
        dx = abs(x - posicion_anterior[0])
        dy = abs(y - posicion_anterior[1])
        distancia = dx + dy  # Distancia Manhattan
        
        # Tiempo base: 1 hora por tile
        tiempo_horas = distancia
        
        # Aplicar costo de terreno
        if tile:
            tiempo_horas *= tile.costo_movimiento
        
        return {
            "posicion_anterior": posicion_anterior,
            "posicion_nueva": (x, y),
            "distancia": distancia,
            "tiempo_horas": tiempo_horas,
            "tile": tile.to_dict() if tile else None,
            "chunks_cargados": len(chunks_a_cargar)
        }
    
    def mover_jugador_local(self, x: int, y: int) -> Dict:
        """
        Mueve al jugador dentro del tile actual (sub-tiles de 10m).
        
        IMPORTANTE: Este movimiento es LOCAL dentro del tile mundial.
        NO descubre tiles mundiales adyacentes.
        
        Args:
            x: Coordenada X local (0-9)
            y: Coordenada Y local (0-9)
        
        Returns:
            Diccionario con información del movimiento
        """
        if not (0 <= x <= 9 and 0 <= y <= 9):
            return {"error": "Coordenadas locales inválidas (deben ser 0-9)"}
        
        posicion_anterior = self.posicion_local
        self.posicion_local = (x, y)
        
        # Obtener tile actual y generar sub-tiles si es necesario
        tile = self.gestor_chunks.get_tile(*self.posicion_jugador)
        if not tile:
            return {"error": "Tile no encontrado"}
        
        # Generar sub-tiles lazy
        if not tile.sub_tiles_generados:
            tile.generar_sub_tiles()
        
        # Descubrir sub-tile LOCAL
        sub_tile = tile.get_sub_tile(x, y)
        if sub_tile:
            sub_tile.explorar()
        
        # Calcular tiempo de viaje (1 minuto por sub-tile)
        dx = abs(x - posicion_anterior[0])
        dy = abs(y - posicion_anterior[1])
        distancia = dx + dy
        tiempo_minutos = distancia  # 1 minuto por sub-tile
        
        return {
            "posicion_anterior": posicion_anterior,
            "posicion_nueva": (x, y),
            "distancia": distancia,
            "tiempo_minutos": tiempo_minutos,
            "sub_tile": sub_tile.to_dict() if sub_tile else None,
            "tile_mundial": tile.to_dict()
        }
    
    def mover_a_ubicacion(self, ubicacion_id: str) -> Dict:
        """
        Mueve al jugador a una ubicación conocida.
        
        Args:
            ubicacion_id: ID de la ubicación destino
        
        Returns:
            Diccionario con información del viaje
        """
        if ubicacion_id not in self.ubicaciones:
            return {"error": "Ubicación no encontrada"}
        
        ubicacion = self.ubicaciones[ubicacion_id]
        
        # Buscar ruta
        ruta = None
        for r in self.rutas.values():
            if (r.origen == self.ubicacion_actual and r.destino == ubicacion_id) or \
               (r.destino == self.ubicacion_actual and r.origen == ubicacion_id):
                ruta = r
                break
        
        if not ruta:
            # No hay ruta directa, calcular tiempo por distancia
            dx = abs(ubicacion.x - self.posicion_jugador[0])
            dy = abs(ubicacion.y - self.posicion_jugador[1])
            tiempo_horas = dx + dy
        else:
            tiempo_horas = ruta.calcular_tiempo()
        
        # Mover
        resultado = self.mover_jugador(ubicacion.x, ubicacion.y)
        self.ubicacion_actual = ubicacion_id
        ubicacion.visitada = True
        
        resultado["ubicacion"] = ubicacion.to_dict()
        resultado["tiempo_horas"] = tiempo_horas
        
        if ruta:
            resultado["ruta"] = ruta.to_dict()
        
        return resultado
    
    # ==================== EXPLORACIÓN ====================
    
    def explorar_tile_actual(self) -> Dict:
        """
        Explora el tile actual del jugador.
        
        Returns:
            Diccionario con información de la exploración
        """
        x, y = self.posicion_jugador
        tile = self.gestor_chunks.get_tile(x, y)
        
        if not tile:
            return {"error": "Tile no encontrado"}
        
        tile.explorar()
        
        # Verificar si hay ubicación
        ubicacion = None
        if tile.ubicacion_id and tile.ubicacion_id in self.ubicaciones:
            ubicacion = self.ubicaciones[tile.ubicacion_id]
            ubicacion.descubierta = True
        
        return {
            "tile": tile.to_dict(),
            "ubicacion": ubicacion.to_dict() if ubicacion else None
        }
    
    def get_tiles_visibles(self, radio: int = 3) -> List[Tile]:
        """
        Obtiene los tiles visibles desde la posición actual.
        
        Args:
            radio: Radio de visión en tiles
        
        Returns:
            Lista de tiles visibles
        """
        return self.gestor_chunks.get_tiles_visibles(radio)
    
    def get_destinos_cercanos(self, radio: int = 50) -> List[Dict]:
        """
        Obtiene las ubicaciones cercanas al jugador.
        
        Args:
            radio: Radio de búsqueda en tiles
        
        Returns:
            Lista de ubicaciones con información de ruta
        """
        x, y = self.posicion_jugador
        destinos = []
        
        for ubicacion in self.ubicaciones.values():
            distancia = abs(ubicacion.x - x) + abs(ubicacion.y - y)
            
            if distancia <= radio:
                # Buscar ruta
                ruta = None
                for r in self.rutas.values():
                    if (r.origen == self.ubicacion_actual and r.destino == ubicacion.id) or \
                       (r.destino == self.ubicacion_actual and r.origen == ubicacion.id):
                        ruta = r
                        break
                
                destinos.append({
                    "ubicacion": ubicacion.to_dict(),
                    "distancia": distancia,
                    "ruta": ruta.to_dict() if ruta else None,
                    "descubierta": ubicacion.descubierta or distancia <= 10
                })
        
        # Ordenar por distancia
        destinos.sort(key=lambda d: d["distancia"])
        
        return destinos
    
    # ==================== MAPA PROGRESIVO ====================
    
    def get_estado_mapa(self) -> Dict:
        """
        Obtiene el estado actual del mapa para el jugador.
        
        Returns:
            Diccionario con el estado del mapa
        """
        tiles_explorados = self.gestor_chunks.contar_tiles_explorados()
        ubicaciones_descubiertas = sum(1 for u in self.ubicaciones.values() if u.descubierta)
        ubicaciones_visitadas = sum(1 for u in self.ubicaciones.values() if u.visitada)
        
        # Contar sub-tiles descubiertos en el tile actual
        sub_tiles_descubiertos = 0
        tile_actual = self.gestor_chunks.get_tile(*self.posicion_jugador)
        if tile_actual and tile_actual.sub_tiles_generados:
            for fila in tile_actual.sub_tiles:
                for sub_tile in fila:
                    if sub_tile.descubierto:
                        sub_tiles_descubiertos += 1
        
        return {
            "posicion_jugador": list(self.posicion_jugador),
            "posicion_local": list(self.posicion_local),
            "ubicacion_actual": self.ubicacion_actual,
            "modo_mapa": self.modo_mapa,
            "tiles_explorados": tiles_explorados,
            "sub_tiles_descubiertos": sub_tiles_descubiertos,
            "ubicaciones_descubiertas": ubicaciones_descubiertas,
            "ubicaciones_visitadas": ubicaciones_visitadas,
            "total_ubicaciones": len(self.ubicaciones),
            "rutas_descubiertas": sum(1 for r in self.rutas.values() if r.descubierta)
        }
    
    def get_mapa_visual(self, radio: int = 10) -> List[List[str]]:
        """
        Obtiene una representación visual del mapa MUNDIAL.
        
        Args:
            radio: Radio de tiles a mostrar
        
        Returns:
            Matriz de caracteres representando el mapa
        """
        x, y = self.posicion_jugador
        mapa = []
        
        # Símbolos por bioma
        simbolos_bioma = {
            "bosque_ancestral": "🌲",
            "paramo_marchito": "💀",
            "pantano_sombrio": "🌫️",
            "montanas_heladas": "🏔️",
            "desierto_ceniza": "🏜️",
            "ruinas_subterraneas": "🏛️",
            "pradera": "🌾",
            "costa": "🌊",
            "desconocido": "❓"
        }
        
        # Símbolos por tipo de ubicación
        simbolos_ubicacion = {
            "pueblo": "🏘️",
            "ciudad": "🏰",
            "capital": "👑",
            "mazmorra": "⚔️",
            "poi": "✨"
        }
        
        for dy in range(-radio, radio + 1):
            fila = []
            for dx in range(-radio, radio + 1):
                tile_x, tile_y = x + dx, y + dy
                tile = self.gestor_chunks.get_tile(tile_x, tile_y)
                
                # Posición del jugador
                if dx == 0 and dy == 0:
                    fila.append("📍")
                    continue
                
                # Ubicación
                if tile and tile.ubicacion_id:
                    ubicacion = self.ubicaciones.get(tile.ubicacion_id)
                    if ubicacion and ubicacion.descubierta:
                        simbolo = simbolos_ubicacion.get(ubicacion.tipo.value, "?")
                        fila.append(simbolo)
                        continue
                
                # Tile explorado
                if tile and tile.visibilidad == EstadoVisibilidad.EXPLORADO:
                    simbolo = simbolos_bioma.get(tile.bioma, "?")
                    fila.append(simbolo)
                # Tile descubierto
                elif tile and tile.visibilidad == EstadoVisibilidad.DESCUBIERTO:
                    fila.append("·")
                # No descubierto
                else:
                    fila.append("?")
            
            mapa.append(fila)
        
        return mapa
    
    def get_mapa_local_visual(self, radio: int = 6) -> List[List[str]]:
        """
        Obtiene una representación visual del mapa LOCAL (sub-tiles).
        
        Args:
            radio: Radio de sub-tiles a mostrar (default 6 = 13x13 grid)
        
        Returns:
            Matriz de caracteres representando el mapa local
        """
        tile = self.gestor_chunks.get_tile(*self.posicion_jugador)
        if not tile:
            return [["?" for _ in range(radio * 2 + 1)] for _ in range(radio * 2 + 1)]
        
        # Generar sub-tiles si no existen
        if not tile.sub_tiles_generados:
            tile.generar_sub_tiles()
        
        x_local, y_local = self.posicion_local
        mapa = []
        
        # Símbolos por tipo de sub-tile
        simbolos_subtile = {
            "bosque_denso": "🌲",
            "claro": "🌿",
            "arbol_grande": "🌳",
            "arbustos": "🪴",
            "tierra_yerma": "🟫",
            "roca": "🪨",
            "hierba_seca": "🌾",
            "ruinas": "🏛️",
            "cienaga": "🌫️",
            "tierra_firme": "🟫",
            "niebla": "🌫️",
            "agua_estancada": "💧",
            "nieve": "❄️",
            "cueva": "🕳️",
            "pico": "🏔️",
            "arena": "🏜️",
            "duna": "🏜️",
            "oasis": "🌴",
            "hierba": "🌿",
            "flores": "🌸",
            "arbol": "🌳",
            "rio": "🌊",
            "playa": "🏖️",
            "acantilado": "🪨",
            "agua": "🌊",
            "terreno": "·",
            "vacio": "·",
        }
        
        for dy in range(-radio, radio + 1):
            fila = []
            for dx in range(-radio, radio + 1):
                sub_x, sub_y = x_local + dx, y_local + dy
                
                # Posición del jugador
                if dx == 0 and dy == 0:
                    fila.append("📍")
                    continue
                
                # Fuera del tile
                if not (0 <= sub_x <= 9 and 0 <= sub_y <= 9):
                    fila.append("⬛")
                    continue
                
                sub_tile = tile.get_sub_tile(sub_x, sub_y)
                if sub_tile:
                    if sub_tile.descubierto:
                        simbolo = simbolos_subtile.get(sub_tile.tipo, "·")
                        fila.append(simbolo)
                    else:
                        fila.append("?")
                else:
                    fila.append("?")
            
            mapa.append(fila)
        
        return mapa
    
    # ==================== PERSISTENCIA ====================
    
    def to_dict(self) -> dict:
        """Serializa el mapa completo."""
        return {
            "gestor_chunks": self.gestor_chunks.to_dict(),
            "ubicaciones": {id: u.to_dict() for id, u in self.ubicaciones.items()},
            "rutas": {id: r.to_dict() for id, r in self.rutas.items()},
            "posicion_jugador": list(self.posicion_jugador),
            "posicion_local": list(self.posicion_local),
            "ubicacion_actual": self.ubicacion_actual,
            "modo_mapa": self.modo_mapa
        }
    
    @classmethod
    def from_dict(cls, data: dict, seed) -> 'MapaMundo':
        """Deserializa el mapa."""
        mapa = cls(seed=seed)
        
        mapa.gestor_chunks = GestorChunks.from_dict(data.get("gestor_chunks", {}))
        mapa.ubicaciones = {
            id: Ubicacion.from_dict(u) 
            for id, u in data.get("ubicaciones", {}).items()
        }
        mapa.rutas = {
            id: Ruta.from_dict(r) 
            for id, r in data.get("rutas", {}).items()
        }
        mapa.posicion_jugador = tuple(data.get("posicion_jugador", [0, 0]))
        mapa.posicion_local = tuple(data.get("posicion_local", [5, 5]))
        mapa.ubicacion_actual = data.get("ubicacion_actual")
        mapa.modo_mapa = data.get("modo_mapa", "mundial")
        
        return mapa
    
    def __repr__(self) -> str:
        return f"MapaMundo(ubicaciones={len(self.ubicaciones)}, rutas={len(self.rutas)})"