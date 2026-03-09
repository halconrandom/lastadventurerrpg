"use client";

import { Character, GameTab } from "@/lib/types";
import { cn } from "@/lib/utils";

interface TopBarProps {
  character: Character;
  activeTab: GameTab;
  onTabChange: (tab: GameTab) => void;
  onSave: () => void;
  onExit: () => void;
}

const tabs: { id: GameTab; label: string }[] = [
  { id: "explorar", label: "Explorar" },
  { id: "inventario", label: "Inventario" },
  { id: "combate", label: "Combate" },
  { id: "misiones", label: "Misiones" },
  { id: "habilidades", label: "Habilidades" },
];

function MiniStatBar({
  label,
  current,
  max,
  color,
}: {
  label: string;
  current: number;
  max: number;
  color: string;
}) {
  const percentage = (current / max) * 100;

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-muted-foreground uppercase tracking-wider w-12">
        {label}
      </span>
      <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden border border-border">
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
}: TopBarProps) {
  return (
    <header className="h-14 bg-card border-b border-border flex items-center justify-between px-4">
      {/* Izquierda: Info del personaje */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="font-display text-primary">{character.name}</span>
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

      {/* Centro: Navegación de tabs */}
      <nav className="flex items-center gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={cn(
              "px-3 py-2 rounded-lg transition-all text-sm",
              activeTab === tab.id
                ? "bg-primary/20 text-primary border border-primary/30"
                : "text-muted-foreground hover:text-foreground hover:bg-secondary"
            )}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Derecha: Oro + Acciones */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-1 text-gold">
          <span className="text-sm font-medium">
            {character.gold.toLocaleString()} oro
          </span>
        </div>

        <div className="flex items-center gap-1 border-l border-border pl-3">
          <button
            onClick={onSave}
            className="px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground hover:bg-secondary rounded transition-colors"
          >
            Guardar
          </button>
          <button
            onClick={onExit}
            className="px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground hover:bg-secondary rounded transition-colors"
          >
            Salir
          </button>
        </div>
      </div>
    </header>
  );
}
