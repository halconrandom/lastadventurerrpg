// API Client para Last Adventurer Backend

import type {
  Slot,
  DatosJuego,
  Personaje,
  CrearPersonajeRequest,
  NuevaPartidaResponse,
  EstadoCombateResponse,
  ResultadoAccion,
  RecompensasCombate,
  IniciarCombateRequest,
  EjecutarAccionRequest,
  EnemigoTemplate,
  EstadoMapa,
  MapaVisual,
  Tile,
  Ubicacion,
  Ruta,
  DestinoCercano,
  HabilidadCartografia,
  MapaItem,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";
const DEFAULT_TIMEOUT = 30000; // 30 segundos
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000; // 1 segundo

// Clase de error personalizada para errores de API
export class ApiError extends Error {
  public status: number;
  public endpoint: string;
  public retryable: boolean;

  constructor(message: string, status: number, endpoint: string, retryable: boolean = false) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.endpoint = endpoint;
    this.retryable = retryable;
  }
}

// Error de timeout
export class TimeoutError extends Error {
  public endpoint: string;

  constructor(endpoint: string, timeout: number) {
    super(`Request timeout after ${timeout}ms for ${endpoint}`);
    this.name = "TimeoutError";
    this.endpoint = endpoint;
  }
}

// Error de red
export class NetworkError extends Error {
  public endpoint: string;

  constructor(endpoint: string, originalError?: Error) {
    super(`Network error for ${endpoint}: ${originalError?.message || "Unknown error"}`);
    this.name = "NetworkError";
    this.endpoint = endpoint;
  }
}

// Helper para crear timeout
function createTimeout<T>(promise: Promise<T>, ms: number, endpoint: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new TimeoutError(endpoint, ms));
    }, ms);

    promise
      .then((result) => {
        clearTimeout(timer);
        resolve(result);
      })
      .catch((error) => {
        clearTimeout(timer);
        reject(error);
      });
  });
}

// Helper para delay
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Función principal de fetch con manejo de errores mejorado
async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit,
  retryCount: number = 0
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorMessage = `Error ${response.status}`;
      let errorData: any = null;
      
      try {
        errorData = await response.json();
        // El backend devuelve { success: false, message: "..." }
        errorMessage = errorData.message || errorData.detail || errorMessage;
      } catch {
        // Si no se puede parsear el JSON, usar el status
        errorMessage = `${response.status} ${response.statusText}`;
      }

      // Determinar si el error es recuperable
      const retryable = response.status >= 500 || response.status === 429;
      
      // Intentar reintento si es recuperable
      if (retryable && retryCount < MAX_RETRIES) {
        console.warn(`[API] Retrying ${endpoint} (attempt ${retryCount + 1}/${MAX_RETRIES})`);
        await delay(RETRY_DELAY * (retryCount + 1));
        return fetchApi<T>(endpoint, options, retryCount + 1);
      }

      throw new ApiError(errorMessage, response.status, endpoint, retryable);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    clearTimeout(timeoutId);

    // Si ya es un error nuestro, propagarlo
    if (error instanceof ApiError || error instanceof TimeoutError) {
      throw error;
    }

    // Error de abort (timeout)
    if (error instanceof Error && error.name === "AbortError") {
      throw new TimeoutError(endpoint, DEFAULT_TIMEOUT);
    }

    // Error de red
    if (error instanceof TypeError && error.message.includes("fetch")) {
      // Intentar reintento para errores de red
      if (retryCount < MAX_RETRIES) {
        console.warn(`[API] Network error, retrying ${endpoint} (attempt ${retryCount + 1}/${MAX_RETRIES})`);
        await delay(RETRY_DELAY * (retryCount + 1));
        return fetchApi<T>(endpoint, options, retryCount + 1);
      }
      throw new NetworkError(endpoint, error);
    }

    // Error desconocido
    console.error(`[API] Unknown error for ${endpoint}:`, error);
    throw new ApiError(
      error instanceof Error ? error.message : "Unknown error",
      0,
      endpoint,
      true
    );
  }
}

// Helper para loggear errores de API
export function logApiError(error: unknown, context?: string): void {
  if (error instanceof ApiError) {
    console.error(`[API Error${context ? ` - ${context}` : ""}]`, {
      message: error.message,
      status: error.status,
      endpoint: error.endpoint,
      retryable: error.retryable,
    });
  } else if (error instanceof TimeoutError) {
    console.error(`[Timeout Error${context ? ` - ${context}` : ""}]`, {
      endpoint: error.endpoint,
    });
  } else if (error instanceof NetworkError) {
    console.error(`[Network Error${context ? ` - ${context}` : ""}]`, {
      endpoint: error.endpoint,
    });
  } else {
    console.error(`[Unknown Error${context ? ` - ${context}` : ""}]`, error);
  }
}

// Helper para obtener mensaje de error amigable
export function getErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 401) return "No autorizado. Por favor, inicia sesión.";
    if (error.status === 403) return "No tienes permiso para realizar esta acción.";
    if (error.status === 404) return "Recurso no encontrado.";
    if (error.status === 429) return "Demasiadas solicitudes. Espera un momento.";
    if (error.status >= 500) return "Error del servidor. Intenta más tarde.";
    return error.message;
  }
  if (error instanceof TimeoutError) {
    return "La solicitud tardó demasiado. Verifica tu conexión.";
  }
  if (error instanceof NetworkError) {
    return "Error de conexión. Verifica tu conexión a internet.";
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Error desconocido.";
}

// ============== SLOTS ==============

export async function obtenerSlots(): Promise<Slot[]> {
  const response = await fetchApi<{ slots: Slot[] }>("/api/slots");
  return response.slots;
}

export async function obtenerSlot(slotNum: number): Promise<Slot> {
  return fetchApi<Slot>(`/api/slots/${slotNum}`);
}

// ============== PARTIDA ==============

export async function crearNuevaPartida(
  datos: CrearPersonajeRequest
): Promise<NuevaPartidaResponse> {
  const response = await fetchApi<{ success: boolean; message: string; data: NuevaPartidaResponse }>(
    "/api/partida/nueva",
    {
      method: "POST",
      body: JSON.stringify(datos),
    }
  );
  return response.data;
}

export async function cargarPartida(slotNum: number): Promise<DatosJuego> {
  const response = await fetchApi<{ success: boolean; message: string; data: DatosJuego }>(
    `/api/partida/${slotNum}`
  );
  return response.data;
}

export async function guardarPartida(
  slotNum: number,
  datos: DatosJuego
): Promise<void> {
  await fetchApi(`/api/partida/${slotNum}`, {
    method: "PUT",
    body: JSON.stringify({ datos }),
  });
}

export async function eliminarPartida(slotNum: number): Promise<void> {
  await fetchApi(`/api/partida/${slotNum}`, {
    method: "DELETE",
  });
}

// ============== PERSONAJE ==============

export async function obtenerPersonaje(
  slotNum: number
): Promise<Personaje> {
  const response = await fetchApi<{ success: boolean; message: string; data: Personaje }>(
    `/api/personaje/${slotNum}`
  );
  return response.data;
}

// ============== DATOS DEL JUEGO ==============

export async function obtenerItems(): Promise<Record<string, unknown>[]> {
  const response = await fetchApi<{ items: Record<string, unknown>[] }>(
    "/api/data/items"
  );
  return response.items;
}

export async function obtenerArquetipos(): Promise<Record<string, unknown>[]> {
  const response = await fetchApi<{ arquetipos: Record<string, unknown>[] }>(
    "/api/data/arquetipos"
  );
  return response.arquetipos;
}

// ============== JUEGO ==============

export async function mejorarStat(
  slot: number,
  stat: string,
  cantidad: number = 1
): Promise<Personaje> {
  const response = await fetchApi<{ success: boolean; message: string; data: Personaje }>(
    "/api/personaje/stats/mejorar",
    {
      method: "POST",
      body: JSON.stringify({ slot, stat, cantidad }),
    }
  );
  return response.data;
}

export async function explorar(slot: number): Promise<{
  mensaje: string;
  recompensas: { oro: number; exp: number };
  personaje: Personaje;
  inventario: any;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: {
      mensaje: string;
      recompensas: { oro: number; exp: number };
      personaje: Personaje;
      inventario: any;
    };
  }>("/api/juego/explorar", {
    method: "POST",
    body: JSON.stringify({ slot }),
  });
  return response.data;
}

// ============== COMBATE ==============

export async function iniciarCombate(
  request: IniciarCombateRequest
): Promise<EstadoCombateResponse> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: EstadoCombateResponse;
  }>("/api/combate/iniciar", {
    method: "POST",
    body: JSON.stringify(request),
  });
  return response.data;
}

export async function ejecutarAccionCombate(
  request: EjecutarAccionRequest & { slot: number }
): Promise<ResultadoAccion> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: ResultadoAccion;
  }>("/api/combate/accion", {
    method: "POST",
    body: JSON.stringify(request),
  });
  return response.data;
}

export async function resolverTurnoEnemigos(slot: number): Promise<{
  resultados: ResultadoAccion[];
  estado: EstadoCombateResponse;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: { resultados: ResultadoAccion[]; estado: EstadoCombateResponse };
  }>("/api/combate/resolver-enemigos", {
    method: "POST",
    body: JSON.stringify({ slot }),
  });
  return response.data;
}

export async function getEstadoCombate(slot: number): Promise<EstadoCombateResponse> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: EstadoCombateResponse;
  }>(`/api/combate/estado?slot=${slot}`);
  return response.data;
}

export async function getRecompensasCombate(slot: number): Promise<RecompensasCombate> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: RecompensasCombate;
  }>(`/api/combate/recompensas?slot=${slot}`);
  return response.data;
}

export async function finalizarCombate(
  slot: number
): Promise<{ estado: string; recompensas?: RecompensasCombate }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: { estado: string; recompensas?: RecompensasCombate };
  }>("/api/combate/finalizar", {
    method: "POST",
    body: JSON.stringify({ slot }),
  });
  return response.data;
}

export async function getEnemigosDisponibles(): Promise<
  Record<string, EnemigoTemplate[]>
> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: Record<string, EnemigoTemplate[]>;
  }>("/api/combate/enemigos-disponibles");
  return response.data;
}

// ============== MAPA ==============

export async function getEstadoMapa(
  slot: number
): Promise<EstadoMapa> {
  const response = await fetchApi<{
    success: boolean;
    data: EstadoMapa;
  }>(`/api/mapa/estado?slot=${slot}`);
  return response.data;
}

export async function getMapaVisual(
  slot: number,
  radio: number = 10
): Promise<MapaVisual> {
  const response = await fetchApi<{
    success: boolean;
    data: MapaVisual;
  }>(`/api/mapa/visual?slot=${slot}&radio=${radio}`);
  return response.data;
}

export async function moverJugador(
  slot: number,
  x: number,
  y: number
): Promise<{
  posicion_anterior: [number, number];
  posicion_nueva: [number, number];
  distancia: number;
  tiempo_horas: number;
  tile: Tile | null;
  chunks_cargados: number;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: {
      posicion_anterior: [number, number];
      posicion_nueva: [number, number];
      distancia: number;
      tiempo_horas: number;
      tile: Tile | null;
      chunks_cargados: number;
    };
  }>("/api/mapa/mover", {
    method: "POST",
    body: JSON.stringify({ slot, x, y }),
  });
  return response.data;
}

export async function getUbicacionesCercanas(
  slot: number,
  radio: number = 50
): Promise<{ ubicaciones: DestinoCercano[]; total: number }> {
  const response = await fetchApi<{
    success: boolean;
    data: { ubicaciones: DestinoCercano[]; total: number };
  }>(`/api/mapa/ubicaciones?slot=${slot}&radio=${radio}`);
  return response.data;
}

export async function getUbicacion(
  slot: number,
  ubicacionId: string
): Promise<Ubicacion> {
  const response = await fetchApi<{
    success: boolean;
    data: Ubicacion;
  }>(`/api/mapa/ubicacion/${ubicacionId}?slot=${slot}`);
  return response.data;
}

export async function viajarAUbicacion(
  slot: number,
  ubicacionId: string
): Promise<{
  posicion_anterior: [number, number];
  posicion_nueva: [number, number];
  distancia: number;
  tiempo_horas: number;
  tile: Tile | null;
  ubicacion: Ubicacion;
  ruta?: Ruta;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: {
      posicion_anterior: [number, number];
      posicion_nueva: [number, number];
      distancia: number;
      tiempo_horas: number;
      tile: Tile | null;
      ubicacion: Ubicacion;
      ruta?: Ruta;
    };
  }>("/api/mapa/viajar", {
    method: "POST",
    body: JSON.stringify({ slot, ubicacion_id: ubicacionId }),
  });
  return response.data;
}

export async function explorarTileActual(
  slot: number
): Promise<{ tile: Tile; ubicacion: Ubicacion | null }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: { tile: Tile; ubicacion: Ubicacion | null };
  }>("/api/mapa/explorar", {
    method: "POST",
    body: JSON.stringify({ slot }),
  });
  return response.data;
}

export async function getCartografiaStats(
  slot: number
): Promise<HabilidadCartografia> {
  const response = await fetchApi<{
    success: boolean;
    data: HabilidadCartografia;
  }>(`/api/mapa/cartografia?slot=${slot}`);
  return response.data;
}

export async function crearMapa(
  slot: number,
  tipo: string,
  calidad: string,
  centroX: number,
  centroY: number,
  radio?: number
): Promise<MapaItem> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: MapaItem;
  }>("/api/mapa/cartografia/mapa", {
    method: "POST",
    body: JSON.stringify({
      slot,
      tipo,
      calidad,
      centro_x: centroX,
      centro_y: centroY,
      radio,
    }),
  });
  return response.data;
}

export async function usarMapa(
  slot: number,
  mapaId: string
): Promise<{
  mapa: MapaItem;
  tiles_revelados: number;
  ubicaciones_reveladas: Ubicacion[];
  rutas_reveladas: Ruta[];
  experiencia_ganada: number;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: {
      mapa: MapaItem;
      tiles_revelados: number;
      ubicaciones_reveladas: Ubicacion[];
      rutas_reveladas: Ruta[];
      experiencia_ganada: number;
    };
  }>("/api/mapa/cartografia/usar", {
    method: "POST",
    body: JSON.stringify({ slot, mapa_id: mapaId }),
  });
  return response.data;
}

export async function getMapasDisponibles(
  slot: number
): Promise<{ mapas: MapaItem[]; total: number }> {
  const response = await fetchApi<{
    success: boolean;
    data: { mapas: MapaItem[]; total: number };
  }>(`/api/mapa/cartografia/mapas?slot=${slot}`);
  return response.data;
}

// ============== MAPA LOCAL ==============

export async function getMapaLocalVisual(
  slot: number,
  radio: number = 6
): Promise<MapaVisual> {
  const response = await fetchApi<{
    success: boolean;
    data: MapaVisual;
  }>(`/api/mapa/local?slot=${slot}&radio=${radio}`);
  return response.data;
}

export async function moverJugadorLocal(
  slot: number,
  x: number,
  y: number
): Promise<{
  posicion_anterior: [number, number];
  posicion_nueva: [number, number];
  distancia: number;
  tiempo_minutos: number;
  sub_tile: any;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: {
      posicion_anterior: [number, number];
      posicion_nueva: [number, number];
      distancia: number;
      tiempo_minutos: number;
      sub_tile: any;
    };
  }>("/api/mapa/mover-local", {
    method: "POST",
    body: JSON.stringify({ slot, x, y }),
  });
  return response.data;
}

// ============== INVENTARIO ==============

export interface InventarioResponse {
  items: any[];
  materiales: any[];
  oro: number;
  slots_maximos: number;
  equipamiento: {
    casco: any | null;
    peto: any | null;
    guantes: any | null;
    botas: any | null;
    mano_izquierda: any | null;
    mano_derecha: any | null;
  };
}

export async function getInventario(slot: number): Promise<InventarioResponse> {
  const response = await fetchApi<{
    success: boolean;
    inventario: InventarioResponse;
  }>(`/api/inventario?slot=${slot}`);
  return response.inventario;
}

export async function equiparItem(
  slot: number,
  indiceAlforjas: number,
  slotEquipamiento: string
): Promise<{ success: boolean; message: string; inventario: InventarioResponse }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    inventario: InventarioResponse;
  }>("/api/inventario/equipar", {
    method: "POST",
    body: JSON.stringify({ slot, indice_alforjas: indiceAlforjas, slot_equipamiento: slotEquipamiento }),
  });
  return response;
}

export async function desequiparItem(
  slot: number,
  slotEquipamiento: string,
  indiceAlforjas?: number
): Promise<{ success: boolean; message: string; inventario: InventarioResponse }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    inventario: InventarioResponse;
  }>("/api/inventario/desequipar", {
    method: "POST",
    body: JSON.stringify({ slot, slot_equipamiento: slotEquipamiento, indice_alforjas: indiceAlforjas }),
  });
  return response;
}

export async function usarItem(
  slot: number,
  indice: number
): Promise<{ success: boolean; message: string; inventario?: InventarioResponse }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    inventario?: InventarioResponse;
  }>("/api/inventario/usar", {
    method: "POST",
    body: JSON.stringify({ slot, indice }),
  });
  return response;
}

export async function tirarItem(
  slot: number,
  indice: number
): Promise<{ success: boolean; message: string; inventario?: InventarioResponse }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    inventario?: InventarioResponse;
  }>("/api/inventario/tirar", {
    method: "DELETE",
    body: JSON.stringify({ slot, indice }),
  });
  return response;
}

export async function toggleFavorito(
  slot: number,
  indice: number
): Promise<{ success: boolean; message: string; inventario: InventarioResponse }> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    inventario: InventarioResponse;
  }>("/api/inventario/favorito", {
    method: "POST",
    body: JSON.stringify({ slot, indice }),
  });
  return response;
}

export async function getStatsEquipados(
  slot: number
): Promise<Record<string, number>> {
  const response = await fetchApi<{
    success: boolean;
    stats: Record<string, number>;
  }>(`/api/inventario/stats?slot=${slot}`);
  return response.stats;
}

// ========== CRAFTEO ==========

export interface EstacionCrafteo {
  tipo: string;
  nombre: string;
  descripcion: string;
  recetas_craft: RecetaCrafteo[];
  recetas_items: RecetaCrafteo[];
}

export interface RecetaCrafteo {
  id: string;
  nombre: string;
  id_item?: string;
  materiales: { id: string; cantidad: number }[];
  tiempo: number;
  nivel_requerido: number;
  herramienta?: string;
}

export async function getEstaciones(): Promise<EstacionCrafteo[]> {
  const response = await fetchApi<{
    success: boolean;
    estaciones: EstacionCrafteo[];
  }>("/api/crafteo/estaciones");
  return response.estaciones;
}

export async function getRecetasDesbloqueadas(nivel: number): Promise<Record<string, RecetaCrafteo[]>> {
  const response = await fetchApi<{
    success: boolean;
    recetas: Record<string, RecetaCrafteo[]>;
  }>(`/api/crafteo/recetas_desbloqueadas?nivel=${nivel}`);
  return response.recetas;
}

export async function getRecetasEstacion(estacion: string): Promise<RecetaCrafteo[]> {
  const response = await fetchApi<{
    success: boolean;
    recetas: RecetaCrafteo[];
  }>(`/api/crafteo/recetas/${estacion}`);
  return response.recetas;
}

export async function craftearItem(
  slot: number,
  recetaId: string
): Promise<{
  success: boolean;
  message: string;
  item?: any;
  inventario?: any;
}> {
  return fetchApi<{
    success: boolean;
    message: string;
    item?: any;
    inventario?: any;
  }>("/api/crafteo/craftear", {
    method: "POST",
    body: JSON.stringify({ slot, receta_id: recetaId }),
  });
}

export async function craftearEstacion(
  slot: number,
  estacion: string
): Promise<{
  success: boolean;
  message: string;
  estacion?: EstacionCrafteo;
  inventario?: any;
}> {
  return fetchApi<{
    success: boolean;
    message: string;
    estacion?: EstacionCrafteo;
    inventario?: any;
  }>("/api/crafteo/craftear_estacion", {
    method: "POST",
    body: JSON.stringify({ slot, estacion }),
  });
}