"use client";

import { useState, useCallback } from "react";
import { CharacterPanel } from "@/components/game/character-panel";
import { TopBar } from "@/components/game/top-bar";
import { ExplorationPanel } from "@/components/game/exploration-panel";
import { InventoryPanel } from "@/components/game/inventory-panel";
import { CombatPanel } from "@/components/game/combat-panel";
import { QuestsPanel } from "@/components/game/quests-panel";
import { SkillsPanel } from "@/components/game/skills-panel";
import { Character, GameTab, Location, LogEntry, InventoryItem } from "@/types/game";
import { cn } from "@/lib/utils";

// Mock data
const mockCharacter: Character = {
  name: "Halcón",
  title: "El Último Aventurero",
  level: 15,
  gender: "masculino",
  class: "Cazador de Sombras",
  health: 850,
  maxHealth: 1000,
  mana: 320,
  maxMana: 500,
  stamina: 180,
  maxStamina: 200,
  experience: 7500,
  experienceToLevel: 10000,
  attack: 145,
  defense: 78,
  speed: 92,
  critical: 18,
  evasion: 12,
  gold: 15750,
};

const mockLocation: Location = {
  name: "Bosque Ancestral Corrupto",
  type: "Bosque Maldito",
  danger: "moderado",
  explored: 34,
  weather: "nublado",
  timeOfDay: "Día",
  time: "12:00",
};

const mockLogs: LogEntry[] = [
  {
    id: "1",
    message: "Llegaste a Pantano Sombrío Místico. Ciénagas pestilentes ocultan secretos ancestrales.",
    type: "exploration",
    timestamp: new Date(Date.now() - 300000),
  },
  {
    id: "2",
    message: "Llegaste a Bosque Ancestral Corrupto. Árboles milenarios se alzan hacia el cielo, corrompidos por fuerzas oscuras.",
    type: "exploration",
    timestamp: new Date(Date.now() - 180000),
  },
  {
    id: "3",
    message: "Encontraste un cofre oxidado entre las raíces. Contiene: 50 monedas de oro y una Poción de Vitalidad.",
    type: "item",
    timestamp: new Date(Date.now() - 60000),
  },
  {
    id: "4",
    message: "Un lobo sombrío te observa desde las sombras. Parece esperar el momento adecuado para atacar.",
    type: "combat",
    timestamp: new Date(),
  },
];

const mockItems: InventoryItem[] = [
  {
    id: "1",
    name: "Espada del Alba",
    type: "weapon",
    rarity: "epico",
    quantity: 1,
    description: "Una espada forjada en los primeros rayos del amanecer. Emite un suave resplandor dorado.",
    stats: { ataque: 45, crítico: 8 },
  },
  {
    id: "2",
    name: "Armadura de Escamas",
    type: "armor",
    rarity: "raro",
    quantity: 1,
    description: "Armadura hecha con escamas de dragón menor. Ligera pero resistente.",
    stats: { defensa: 32, velocidad: -5 },
  },
  {
    id: "3",
    name: "Poción de Vitalidad",
    type: "consumable",
    rarity: "poco_comun",
    quantity: 5,
    description: "Restaura 200 puntos de salud al consumirla.",
  },
  {
    id: "4",
    name: "Amuleto del Viajero",
    type: "quest",
    rarity: "legendario",
    quantity: 1,
    description: "Un antiguo amuleto que guía a su portador hacia destinos desconocidos.",
  },
  {
    id: "5",
    name: "Hierba Lunar",
    type: "material",
    rarity: "comun",
    quantity: 12,
    description: "Hierba que solo florece bajo la luz de la luna llena. Útil para pociones.",
  },
  {
    id: "6",
    name: "Colmillo de Lobo Sombrío",
    type: "material",
    rarity: "poco_comun",
    quantity: 3,
    description: "Un colmillo afilado de lobo corrompido por la sombra.",
  },
];

const mockQuests = [
  {
    id: "1",
    title: "La Corrupción del Bosque",
    description: "El Bosque Ancestral ha sido corrompido por una fuerza oscura. Investiga el origen de esta maldición y purifica el corazón del bosque.",
    type: "principal" as const,
    status: "activa" as const,
    location: "Bosque Ancestral Corrupto",
    rewards: { gold: 500, exp: 1500 },
    objectives: [
      { text: "Explora el Bosque Ancestral", current: 3, required: 5 },
      { text: "Derrota lobos sombríos", current: 2, required: 5 },
      { text: "Encuentra el Corazón del Bosque", current: 0, required: 1 },
    ],
  },
  {
    id: "2",
    title: "Recolecta Hierbas Lunares",
    description: "El alquimista del pueblo necesita hierbas lunares para preparar un antídoto. Recolecta 10 hierbas en los claros del bosque.",
    type: "secundaria" as const,
    status: "activa" as const,
    location: "Bosque Ancestral",
    rewards: { gold: 150, exp: 300 },
    objectives: [
      { text: "Recolecta Hierbas Lunares", current: 12, required: 10 },
    ],
  },
  {
    id: "3",
    title: "Caza Diaria",
    description: "Elimina criaturas hostiles para mantener los caminos seguros.",
    type: "diaria" as const,
    status: "disponible" as const,
    location: "Cualquier zona",
    rewards: { gold: 100, exp: 200 },
    objectives: [
      { text: "Derrota enemigos", current: 0, required: 10 },
    ],
  },
];

const mockSkills = [
  {
    id: "1",
    name: "Golpe Flamígero",
    description: "Inflige daño de fuego al enemigo, causando quemaduras durante 3 turnos.",
    type: "ofensiva" as const,
    element: "fuego" as const,
    level: 3,
    maxLevel: 5,
    manaCost: 25,
    cooldown: 4,
    unlocked: true,
    requiredLevel: 1,
  },
  {
    id: "2",
    name: "Barrera Arcana",
    description: "Crea un escudo mágico que absorbe daño igual al 30% de tu maná máximo.",
    type: "defensiva" as const,
    level: 2,
    maxLevel: 5,
    manaCost: 40,
    cooldown: 8,
    unlocked: true,
    requiredLevel: 5,
  },
  {
    id: "3",
    name: "Ráfaga de Viento",
    description: "Invoca una ráfaga de viento que daña y empuja a los enemigos.",
    type: "ofensiva" as const,
    element: "aire" as const,
    level: 1,
    maxLevel: 5,
    manaCost: 20,
    cooldown: 3,
    unlocked: true,
    requiredLevel: 8,
  },
  {
    id: "4",
    name: "Torrente Glacial",
    description: "Lanza un chorro de agua helada que congela al enemigo.",
    type: "ofensiva" as const,
    element: "agua" as const,
    level: 0,
    maxLevel: 5,
    manaCost: 35,
    cooldown: 6,
    unlocked: false,
    requiredLevel: 20,
  },
  {
    id: "5",
    name: "Paso Sombrío",
    description: "Te vuelves invisible durante 2 turnos, aumentando tu evasión.",
    type: "utilidad" as const,
    level: 2,
    maxLevel: 3,
    manaCost: 30,
    cooldown: 10,
    unlocked: true,
    requiredLevel: 10,
  },
  {
    id: "6",
    name: "Furia del Guerrero",
    description: "Aumenta tu ataque en un 50% durante 3 turnos, pero reduce tu defensa.",
    type: "ofensiva" as const,
    level: 1,
    maxLevel: 5,
    manaCost: 45,
    cooldown: 12,
    unlocked: true,
    requiredLevel: 12,
  },
];

export default function GamePage() {
  const [activeTab, setActiveTab] = useState<GameTab>("explorar");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isExploring, setIsExploring] = useState(false);
  const [character] = useState(mockCharacter);
  const [location] = useState(mockLocation);
  const [logs, setLogs] = useState(mockLogs);

  const handleExplore = useCallback(() => {
    setIsExploring(true);
    setTimeout(() => {
      const newLog: LogEntry = {
        id: Date.now().toString(),
        message: "Descubriste un sendero oculto entre los árboles retorcidos. El camino parece llevar a lo más profundo del bosque...",
        type: "exploration",
        timestamp: new Date(),
      };
      setLogs(prev => [...prev, newLog]);
      setIsExploring(false);
    }, 2000);
  }, []);

  const handleSave = useCallback(() => {
    console.log("[v0] Guardando partida...");
  }, []);

  const handleExit = useCallback(() => {
    console.log("[v0] Saliendo del juego...");
  }, []);

  const handleAcceptQuest = useCallback((id: string) => {
    console.log("[v0] Aceptando misión:", id);
  }, []);

  const handleAbandonQuest = useCallback((id: string) => {
    console.log("[v0] Abandonando misión:", id);
  }, []);

  const handleUpgradeSkill = useCallback((id: string) => {
    console.log("[v0] Mejorando habilidad:", id);
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case "explorar":
        return (
          <ExplorationPanel
            location={location}
            logs={logs}
            onExplore={handleExplore}
            isExploring={isExploring}
          />
        );
      case "inventario":
        return (
          <InventoryPanel
            items={mockItems}
            capacity={30}
            usedSlots={mockItems.reduce((acc, item) => acc + item.quantity, 0)}
          />
        );
      case "combate":
        return (
          <CombatPanel
            character={character}
            inCombat={false}
            combatLog={[]}
            onAttack={() => {}}
            onDefend={() => {}}
            onSkill={() => {}}
            onFlee={() => {}}
          />
        );
      case "misiones":
        return (
          <QuestsPanel
            quests={mockQuests}
            onAcceptQuest={handleAcceptQuest}
            onAbandonQuest={handleAbandonQuest}
          />
        );
      case "habilidades":
        return (
          <SkillsPanel
            skills={mockSkills}
            skillPoints={3}
            characterLevel={character.level}
            onUpgradeSkill={handleUpgradeSkill}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      <TopBar
        character={character}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onSave={handleSave}
        onExit={handleExit}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        sidebarOpen={sidebarOpen}
      />
      
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Desktop */}
        <div className={cn(
          "hidden lg:block transition-all duration-300",
          sidebarOpen ? "w-80" : "w-0"
        )}>
          {sidebarOpen && <CharacterPanel character={character} />}
        </div>

        {/* Sidebar - Mobile Overlay */}
        {sidebarOpen && (
          <div className="lg:hidden fixed inset-0 z-50 flex">
            <div 
              className="absolute inset-0 bg-background/80 backdrop-blur-sm"
              onClick={() => setSidebarOpen(false)}
            />
            <div className="relative z-10">
              <CharacterPanel 
                character={character} 
                onClose={() => setSidebarOpen(false)}
              />
            </div>
          </div>
        )}

        {/* Main Content */}
        <main className="flex-1 flex flex-col overflow-hidden bg-background">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
