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

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let errorMessage = `Error ${response.status}`;
    try {
      const errorData = await response.json();
      // El backend devuelve { success: false, message: "..." }
      errorMessage = errorData.message || errorData.detail || errorMessage;
    } catch {
      // Si no se puede parsear el JSON, usar el status
    }
    throw new Error(errorMessage);
  }

  return response.json();
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
  request: EjecutarAccionRequest
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

export async function resolverTurnoEnemigos(): Promise<{
  resultados: ResultadoAccion[];
  estado: EstadoCombateResponse;
}> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: { resultados: ResultadoAccion[]; estado: EstadoCombateResponse };
  }>("/api/combate/resolver-enemigos", {
    method: "POST",
  });
  return response.data;
}

export async function getEstadoCombate(): Promise<EstadoCombateResponse> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: EstadoCombateResponse;
  }>("/api/combate/estado");
  return response.data;
}

export async function getRecompensasCombate(): Promise<RecompensasCombate> {
  const response = await fetchApi<{
    success: boolean;
    message: string;
    data: RecompensasCombate;
  }>("/api/combate/recompensas");
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