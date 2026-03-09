export interface Character {
  name: string;
  title: string;
  level: number;
  gender: "masculino" | "femenino";
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
