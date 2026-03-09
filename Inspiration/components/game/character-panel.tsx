"use client";

import { Character } from "@/types/game";
import { 
  Sword, 
  Shield, 
  Zap, 
  Target, 
  Wind,
  User,
  Scroll,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface CharacterPanelProps {
  character: Character;
  onClose?: () => void;
}

function StatBar({ 
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
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground uppercase tracking-wider">{label}</span>
        <span className="text-foreground font-medium">{current}/{max}</span>
      </div>
      <div className="h-2 bg-secondary rounded-full overflow-hidden border border-border">
        <div 
          className={cn("h-full transition-all duration-500", color)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

function AttributeCard({ 
  icon: Icon, 
  label, 
  value, 
  suffix = "" 
}: { 
  icon: React.ElementType;
  label: string; 
  value: number; 
  suffix?: string;
}) {
  return (
    <div className="bg-secondary/50 border border-border rounded-lg p-3 flex flex-col items-center gap-1 hover:border-primary/50 transition-colors">
      <Icon className="w-4 h-4 text-primary" />
      <span className="text-xs text-muted-foreground uppercase tracking-wider">{label}</span>
      <span className="text-lg font-serif text-foreground">{value}{suffix}</span>
    </div>
  );
}

export function CharacterPanel({ character, onClose }: CharacterPanelProps) {
  const [attributesExpanded, setAttributesExpanded] = useState(true);
  const [pathsExpanded, setPathsExpanded] = useState(true);

  return (
    <aside className="w-80 bg-card border-r border-border h-screen overflow-y-auto flex flex-col">
      {/* Header del personaje */}
      <div className="p-4 border-b border-border">
        <div className="flex items-start gap-3">
          <div className="w-16 h-16 rounded-lg bg-secondary border-2 border-primary/50 flex items-center justify-center">
            <User className="w-8 h-8 text-primary" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-serif text-primary tracking-wide">{character.name}</h2>
            <p className="text-xs text-muted-foreground italic">{character.title}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="px-2 py-0.5 bg-primary/20 text-primary text-xs rounded border border-primary/30">
                Nv. {character.level}
              </span>
              <span className="text-xs text-muted-foreground capitalize">{character.gender}</span>
            </div>
          </div>
          {onClose && (
            <button 
              onClick={onClose}
              className="text-muted-foreground hover:text-foreground transition-colors"
              aria-label="Cerrar panel"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Barras de estadísticas principales */}
      <div className="p-4 space-y-3 border-b border-border">
        <StatBar 
          label="Fuerza Vital" 
          current={character.health} 
          max={character.maxHealth} 
          color="bg-health" 
        />
        <StatBar 
          label="Éter Arcano" 
          current={character.mana} 
          max={character.maxMana} 
          color="bg-mana" 
        />
        <StatBar 
          label="Aguante Físico" 
          current={character.stamina} 
          max={character.maxStamina} 
          color="bg-stamina" 
        />
      </div>

      {/* Atributos del Alma - Expandible */}
      <div className="border-b border-border">
        <button 
          onClick={() => setAttributesExpanded(!attributesExpanded)}
          className="w-full p-4 flex items-center justify-between text-left hover:bg-secondary/30 transition-colors"
        >
          <h3 className="text-sm font-serif text-primary tracking-wider uppercase flex items-center gap-2">
            <Scroll className="w-4 h-4" />
            Atributos del Alma
          </h3>
          {attributesExpanded ? (
            <ChevronUp className="w-4 h-4 text-muted-foreground" />
          ) : (
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          )}
        </button>
        
        {attributesExpanded && (
          <div className="px-4 pb-4 grid grid-cols-3 gap-2">
            <AttributeCard icon={Sword} label="Ataque" value={character.attack} />
            <AttributeCard icon={Shield} label="Defensa" value={character.defense} />
            <AttributeCard icon={Zap} label="Velocidad" value={character.speed} />
            <AttributeCard icon={Target} label="Crítico" value={character.critical} suffix="%" />
            <AttributeCard icon={Wind} label="Evasión" value={character.evasion} suffix="%" />
          </div>
        )}
      </div>

      {/* Combate y Sendas - Expandible */}
      <div className="border-b border-border">
        <button 
          onClick={() => setPathsExpanded(!pathsExpanded)}
          className="w-full p-4 flex items-center justify-between text-left hover:bg-secondary/30 transition-colors"
        >
          <h3 className="text-sm font-serif text-primary tracking-wider uppercase flex items-center gap-2">
            <Sword className="w-4 h-4" />
            Combate y Sendas
          </h3>
          {pathsExpanded ? (
            <ChevronUp className="w-4 h-4 text-muted-foreground" />
          ) : (
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          )}
        </button>
        
        {pathsExpanded && (
          <div className="px-4 pb-4 space-y-2">
            <div className="bg-secondary/50 border border-border rounded-lg p-3">
              <span className="text-xs text-muted-foreground uppercase tracking-wider">Senda Actual</span>
              <p className="text-sm text-foreground mt-1">Senda del Destino</p>
            </div>
            <div className="bg-secondary/50 border border-border rounded-lg p-3">
              <span className="text-xs text-muted-foreground uppercase tracking-wider">Clase</span>
              <p className="text-sm text-foreground mt-1">{character.class}</p>
            </div>
          </div>
        )}
      </div>

      {/* Botón de Diario */}
      <div className="p-4 mt-auto">
        <button className="w-full py-3 bg-secondary hover:bg-secondary/80 border border-border text-foreground rounded-lg transition-colors text-sm uppercase tracking-wider">
          Sellar Diario
        </button>
      </div>
    </aside>
  );
}
