// Tipos para el juego Last Adventurer

// ============== TIPOS DE UI (Inspiration) ==============

export interface Character {
  name: string;
  title: string;
  level: number;
  gender: "masculino" | "femenino" | "no_especificar";
  class: string;
  
  // Stats principales
  health: number;
  maxHealth: number;
  mana: number;
  maxMana: number;
  stamina: number;
  maxStamina: number;
  experience: number;
  experienceToLevel: number;
  
  // Atributos del alma
  attack: number;
  defense: number;
  speed: number;
  critical: number;
  evasion: number;
  
  // Oro
  gold: number;
}

export interface Location {
  name: string;
  type: string;
  danger: "seguro" | "bajo" | "moderado" | "alto" | "extremo";
  explored: number;
  weather: string;
  timeOfDay: string;
  time: string;
}

export interface LogEntry {
  id: string;
  message: string;
  type: "exploration" | "combat" | "item" | "quest" | "system";
  timestamp: Date;
}

export interface InventoryItem {
  id: string;
  name: string;
  type: "weapon" | "armor" | "consumable" | "quest" | "material";
  rarity: "comun" | "poco_comun" | "raro" | "epico" | "legendario";
  quantity: number;
  description: string;
  stats?: Record<string, number>;
}

export type GameTab = "explorar" | "inventario" | "combate" | "misiones" | "habilidades";

// ============== TIPOS DE BACKEND ==============

export interface Stats {
  hp: number;
  hp_max: number;
  mana: number;
  mana_max: number;
  stamina: number;
  stamina_max: number;
  ataque: number;
  defensa: number;
  velocidad: number;
  critico: number;
  evasion: number;
  nivel: number;
  experiencia: number;
  experiencia_necesaria: number;
  puntos_distribuibles: number;
  dificultad: "facil" | "normal" | "dificil";
}

export interface Habilidad {
  nivel: number;
  experiencia: number;
  experiencia_necesaria: number;
}

export interface Habilidades {
  [nombre: string]: Habilidad;
}

export interface Personaje {
  nombre: string;
  genero: "masculino" | "femenino" | "no_especificar";
  imagen_url?: string | null;
  stats: Stats;
  habilidades: Habilidades;
}

export interface ItemInventario {
  id: string;
  cantidad: number;
}

export interface Inventario {
  oro: number;
  slots_maximos: number;
  items: ItemInventario[];
}

export interface DatosJuego {
  version: string;
  personaje: Personaje;
  inventario: Inventario;
  zona_actual: string;
  tiempo_jugado: number;
}

export interface SlotInfo {
  nombre: string;
  nivel: number;
  dificultad: string;
  zona: string;
}

export interface Slot {
  numero: number;
  ocupado: boolean;
  info: SlotInfo | null;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}

// Tipos para la API
export interface CrearPersonajeRequest {
  nombre: string;
  genero: "masculino" | "femenino" | "no_especificar";
  dificultad: "facil" | "normal" | "dificil";
}

export interface NuevaPartidaResponse {
  slot: number;
  datos: DatosJuego;
}

// Tipos para el estado del juego
export interface GameState {
  slotActual: number | null;
  datos: DatosJuego | null;
  cargando: boolean;
  error: string | null;
}

// ============== TIPOS DE COMBATE ==============

export interface ParticipanteCombate {
  id: string;
  nombre: string;
  tipo: "jugador" | "enemigo";
  hp: number;
  hp_max: number;
  mana: number;
  mana_max: number;
  stamina: number;
  stamina_max: number;
  ataque: number;
  defensa: number;
  velocidad: number;
  critico: number;
  evasion: number;
  nivel: number;
  esta_vivo: boolean;
  esta_bloqueando: boolean;
  es_jugador: boolean;
  habilidades: HabilidadCombate[];
}

export interface HabilidadCombate {
  nombre: string;
  tipo: string;
  multiplicador: number;
  costo: number;
  efecto?: string;
}

export interface EntradaLogCombate {
  turno: number;
  actor_id: string;
  actor_nombre: string;
  accion: string;
  objetivo_id?: string;
  objetivo_nombre?: string;
  daño?: number;
  es_critico: boolean;
  es_evasion: boolean;
  mensaje: string;
}

export type EstadoCombate =
  | "iniciado"
  | "turno_jugador"
  | "turno_enemigo"
  | "victoria"
  | "derrota"
  | "huida";

export interface EstadoCombateResponse {
  estado: EstadoCombate;
  turno: number;
  orden_turnos: string[];
  jugadores: Record<string, ParticipanteCombate>;
  enemigos: Record<string, ParticipanteCombate>;
  log: EntradaLogCombate[];
  acciones_disponibles: string[];
}

export interface ResultadoAccion {
  success: boolean;
  accion: string;
  actor_id?: string;
  objetivo_id?: string;
  daño?: number;
  es_critico?: boolean;
  evasion?: boolean;
  objetivo_hp?: number;
  objetivo_vivo?: boolean;
  escapo?: boolean;
  mensaje: string;
  fin_combate?: boolean;
  estado_final?: EstadoCombate;
}

export interface RecompensasCombate {
  experiencia: number;
  oro: number;
  drops: { item_id: string; cantidad: number }[];
}

// Request/Response para API de combate
export interface IniciarCombateRequest {
  slot: number;
  enemigos: string[]; // IDs de enemigos
  zona?: string;
}

export interface EjecutarAccionRequest {
  actor_id?: string;
  accion: "atacar" | "habilidad" | "item" | "bloquear" | "huir";
  objetivo_id?: string;
  habilidad_nombre?: string;
  item_id?: string;
}

export interface EnemigoTemplate {
  id: string;
  nombre: string;
  categoria: string;
  nivel_sugerido: number;
}