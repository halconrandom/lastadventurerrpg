"use client";

import { Character, GameTab } from "@/types/game";
import { 
  Map, 
  Package, 
  Swords, 
  ScrollText,
  Sparkles,
  Save, 
  LogOut,
  Menu,
  Coins
} from "lucide-react";
import { cn } from "@/lib/utils";

interface TopBarProps {
  character: Character;
  activeTab: GameTab;
  onTabChange: (tab: GameTab) => void;
  onSave: () => void;
  onExit: () => void;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
}

const tabs: { id: GameTab; label: string; icon: React.ElementType }[] = [
  { id: "explorar", label: "Explorar", icon: Map },
  { id: "inventario", label: "Inventario", icon: Package },
  { id: "combate", label: "Combate", icon: Swords },
  { id: "misiones", label: "Misiones", icon: ScrollText },
  { id: "habilidades", label: "Habilidades", icon: Sparkles },
];

function MiniStatBar({ 
  label, 
  current, 
  max, 
  color 
}: { 
  label: string; 
  current: number; 
  max: number; 
  color: string;
}) {
  const percentage = (current / max) * 100;
  
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-muted-foreground uppercase tracking-wider w-12">{label}</span>
      <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden">
        <div 
          className={cn("h-full transition-all duration-500", color)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

export function TopBar({ 
  character, 
  activeTab, 
  onTabChange, 
  onSave, 
  onExit,
  onToggleSidebar,
  sidebarOpen
}: TopBarProps) {
  return (
    <header className="h-14 bg-card border-b border-border flex items-center justify-between px-4">
      {/* Izquierda: Toggle sidebar + Info del personaje */}
      <div className="flex items-center gap-4">
        <button 
          onClick={onToggleSidebar}
          className="p-2 hover:bg-secondary rounded-lg transition-colors lg:hidden"
          aria-label={sidebarOpen ? "Cerrar menú" : "Abrir menú"}
        >
          <Menu className="w-5 h-5 text-foreground" />
        </button>
        
        <div className="hidden sm:flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="font-serif text-primary">{character.name}</span>
            <span className="px-1.5 py-0.5 bg-primary/20 text-primary text-xs rounded">
              {character.level}
            </span>
          </div>
          
          <div className="hidden md:flex items-center gap-4 pl-4 border-l border-border">
            <MiniStatBar 
              label="Salud" 
              current={character.health} 
              max={character.maxHealth} 
              color="bg-health" 
            />
            <MiniStatBar 
              label="Energía" 
              current={character.mana} 
              max={character.maxMana} 
              color="bg-mana" 
            />
          </div>
        </div>
      </div>

      {/* Centro: Navegación de tabs */}
      <nav className="flex items-center gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={cn(
              "px-3 py-2 rounded-lg flex items-center gap-2 transition-all text-sm",
              activeTab === tab.id
                ? "bg-primary/20 text-primary border border-primary/30"
                : "text-muted-foreground hover:text-foreground hover:bg-secondary"
            )}
          >
            <tab.icon className="w-4 h-4" />
            <span className="hidden lg:inline">{tab.label}</span>
          </button>
        ))}
      </nav>

      {/* Derecha: Oro + Acciones */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-1 text-gold">
          <Coins className="w-4 h-4" />
          <span className="text-sm font-medium">{character.gold.toLocaleString()}</span>
        </div>
        
        <div className="flex items-center gap-1 border-l border-border pl-3">
          <button 
            onClick={onSave}
            className="p-2 hover:bg-secondary rounded-lg transition-colors text-muted-foreground hover:text-foreground"
            aria-label="Guardar"
          >
            <Save className="w-4 h-4" />
          </button>
          <button 
            onClick={onExit}
            className="p-2 hover:bg-secondary rounded-lg transition-colors text-muted-foreground hover:text-foreground"
            aria-label="Salir"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
