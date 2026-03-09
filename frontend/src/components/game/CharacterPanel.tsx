"use client";

import { Character } from "@/lib/types";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface CharacterPanelProps {
  character: Character;
  onClose?: () => void;
}

function StatBar({
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
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground uppercase tracking-wider">
          {label}
        </span>
        <span className="text-foreground font-medium">
          {current}/{max}
        </span>
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
  label,
  value,
  suffix = "",
}: {
  label: string;
  value: number;
  suffix?: string;
}) {
  return (
    <div className="bg-secondary/50 border border-border rounded-lg p-3 flex flex-col items-center gap-1 hover:border-primary/50 transition-colors">
      <span className="text-xs text-muted-foreground uppercase tracking-wider">
        {label}
      </span>
      <span className="text-lg font-display text-foreground">
        {value}
        {suffix}
      </span>
    </div>
  );
}

export function CharacterPanel({ character, onClose }: CharacterPanelProps) {
  const [attributesExpanded, setAttributesExpanded] = useState(true);

  return (
    <aside className="w-80 bg-card border-r border-border h-screen overflow-y-auto flex flex-col">
      {/* Header del personaje */}
      <div className="p-4 border-b border-border">
        <div className="flex items-start gap-3">
          <div className="w-16 h-16 rounded-lg bg-secondary border-2 border-primary/50 flex items-center justify-center">
            <span className="text-2xl font-display text-primary">
              {character.name.charAt(0)}
            </span>
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-display text-primary tracking-wide">
              {character.name}
            </h2>
            <p className="text-xs text-muted-foreground italic">
              {character.title}
            </p>
            <div className="flex items-center gap-2 mt-1">
              <span className="px-2 py-0.5 bg-primary/20 text-primary text-xs rounded border border-primary/30">
                Nv. {character.level}
              </span>
              <span className="text-xs text-muted-foreground capitalize">
                {character.gender}
              </span>
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

      {/* Barra de experiencia */}
      <div className="p-4 border-b border-border">
        <div className="space-y-1">
          <div className="flex justify-between text-xs">
            <span className="text-muted-foreground uppercase tracking-wider">
              Experiencia
            </span>
            <span className="text-foreground font-medium">
              {character.experience}/{character.experienceToLevel}
            </span>
          </div>
          <div className="h-2 bg-secondary rounded-full overflow-hidden border border-border">
            <div
              className="h-full transition-all duration-500 bg-gold"
              style={{
                width: `${(character.experience / character.experienceToLevel) * 100}%`,
              }}
            />
          </div>
        </div>
      </div>

      {/* Atributos del Alma - Expandible */}
      <div className="border-b border-border">
        <button
          onClick={() => setAttributesExpanded(!attributesExpanded)}
          className="w-full p-4 flex items-center justify-between text-left hover:bg-secondary/30 transition-colors"
        >
          <h3 className="text-sm font-display text-primary tracking-wider uppercase">
            Atributos del Alma
          </h3>
          <span className="text-muted-foreground">
            {attributesExpanded ? "−" : "+"}
          </span>
        </button>

        {attributesExpanded && (
          <div className="px-4 pb-4 grid grid-cols-3 gap-2">
            <AttributeCard label="Ataque" value={character.attack} />
            <AttributeCard label="Defensa" value={character.defense} />
            <AttributeCard label="Velocidad" value={character.speed} />
            <AttributeCard
              label="Crítico"
              value={character.critical}
              suffix="%"
            />
            <AttributeCard
              label="Evasión"
              value={character.evasion}
              suffix="%"
            />
          </div>
        )}
      </div>

      {/* Clase */}
      <div className="p-4">
        <div className="bg-secondary/50 border border-border rounded-lg p-3">
          <span className="text-xs text-muted-foreground uppercase tracking-wider">
            Clase
          </span>
          <p className="text-sm text-foreground mt-1">{character.class}</p>
        </div>
      </div>
    </aside>
  );
}
