"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

interface Skill {
  id: string;
  name: string;
  description: string;
  type: "ofensiva" | "defensiva" | "utilidad";
  element?: "fuego" | "agua" | "aire" | "tierra";
  level: number;
  maxLevel: number;
  manaCost: number;
  cooldown: number;
  unlocked: boolean;
  requiredLevel: number;
}

interface SkillsPanelProps {
  skills: Skill[];
  skillPoints: number;
  characterLevel: number;
  onUpgradeSkill: (id: string) => void;
}

const elementColors: Record<string, string> = {
  fuego: "text-health border-health/30 bg-health/10",
  agua: "text-mana border-mana/30 bg-mana/10",
  aire: "text-stamina border-stamina/30 bg-stamina/10",
  tierra: "text-gold border-gold/30 bg-gold/10",
};

const elementIcons: Record<string, string> = {
  fuego: "🔥",
  agua: "💧",
  aire: "🌪️",
  tierra: "🪨",
};

const typeLabels: Record<string, string> = {
  ofensiva: "Ofensiva",
  defensiva: "Defensiva",
  utilidad: "Utilidad",
};

export function SkillsPanel({
  skills,
  skillPoints,
  characterLevel,
  onUpgradeSkill,
}: SkillsPanelProps) {
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [filter, setFilter] = useState<"todas" | "ofensiva" | "defensiva" | "utilidad">("todas");

  const filteredSkills = skills.filter((s) => filter === "todas" || s.type === filter);

  return (
    <div className="flex-1 flex h-full overflow-hidden">
      {/* Skills Grid */}
      <div className="w-full lg:w-2/3 flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-border bg-card/50">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-display text-primary tracking-wide">
                Habilidades
              </h1>
              <p className="text-sm text-muted-foreground">
                Puntos disponibles:{" "}
                <span className="text-primary">{skillPoints}</span>
              </p>
            </div>

            {/* Filters */}
            <div className="flex items-center gap-2">
              {(["todas", "ofensiva", "defensiva", "utilidad"] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={cn(
                    "px-3 py-1.5 rounded-lg text-xs transition-colors capitalize",
                    filter === f
                      ? "bg-primary/20 text-primary border border-primary/30"
                      : "bg-secondary text-muted-foreground hover:text-foreground border border-transparent"
                  )}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Skills Grid */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredSkills.map((skill) => {
              const isLocked = !skill.unlocked;

              return (
                <button
                  key={skill.id}
                  onClick={() => setSelectedSkill(skill)}
                  disabled={isLocked}
                  className={cn(
                    "relative rounded-xl border p-4 transition-all text-left",
                    selectedSkill?.id === skill.id
                      ? "border-primary bg-primary/10"
                      : "border-border bg-secondary/30 hover:bg-secondary/50",
                    isLocked && "opacity-50 cursor-not-allowed"
                  )}
                >
                  {isLocked && (
                    <div className="absolute inset-0 bg-background/50 rounded-xl flex items-center justify-center">
                      <div className="text-center">
                        <span className="text-2xl">🔒</span>
                        <p className="text-xs text-muted-foreground mt-1">
                          Nv. {skill.requiredLevel}
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between mb-3">
                    <div
                      className={cn(
                        "w-10 h-10 rounded-lg flex items-center justify-center",
                        skill.element
                          ? elementColors[skill.element]
                          : "bg-primary/20"
                      )}
                    >
                      <span className="text-lg">
                        {skill.element ? elementIcons[skill.element] : "✨"}
                      </span>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {skill.level}/{skill.maxLevel}
                    </span>
                  </div>

                  <h3 className="font-display text-sm text-foreground mb-1">
                    {skill.name}
                  </h3>

                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      💧 {skill.manaCost}
                    </span>
                    <span>⏱️ {skill.cooldown}s</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Skill Detail */}
      <div className="hidden lg:flex lg:w-1/3 flex-col border-l border-border bg-card/30">
        {selectedSkill ? (
          <>
            <div className="p-6 border-b border-border">
              <div
                className={cn(
                  "w-16 h-16 rounded-xl flex items-center justify-center mb-4",
                  selectedSkill.element
                    ? elementColors[selectedSkill.element]
                    : "bg-primary/20"
                )}
              >
                <span className="text-3xl">
                  {selectedSkill.element
                    ? elementIcons[selectedSkill.element]
                    : "✨"}
                </span>
              </div>

              <h2 className="text-xl font-display text-primary mb-1">
                {selectedSkill.name}
              </h2>
              <p className="text-xs text-muted-foreground">
                {typeLabels[selectedSkill.type]}
                {selectedSkill.element && ` · ${selectedSkill.element}`}
              </p>
            </div>

            <div className="flex-1 p-6 space-y-6 overflow-y-auto">
              {/* Description */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                  Descripción
                </h3>
                <p className="text-sm text-foreground leading-relaxed">
                  {selectedSkill.description}
                </p>
              </div>

              {/* Level */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                  Nivel
                </h3>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden border border-border">
                    <div
                      className="h-full bg-primary transition-all"
                      style={{
                        width: `${(selectedSkill.level / selectedSkill.maxLevel) * 100}%`,
                      }}
                    />
                  </div>
                  <span className="text-sm text-foreground">
                    {selectedSkill.level}/{selectedSkill.maxLevel}
                  </span>
                </div>
              </div>

              {/* Stats */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-3">
                  Estadísticas
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Costo de maná</span>
                    <span className="text-mana">{selectedSkill.manaCost}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Enfriamiento</span>
                    <span className="text-foreground">
                      {selectedSkill.cooldown}s
                    </span>
                  </div>
                </div>
              </div>

              {/* Upgrade */}
              {selectedSkill.unlocked &&
                selectedSkill.level < selectedSkill.maxLevel && (
                  <div className="pt-4 border-t border-border">
                    <button
                      onClick={() => onUpgradeSkill(selectedSkill.id)}
                      disabled={skillPoints === 0}
                      className={cn(
                        "w-full py-2 px-4 rounded-lg transition-colors font-display text-sm uppercase tracking-wider",
                        skillPoints > 0
                          ? "bg-primary/20 text-primary border border-primary/30 hover:bg-primary/30"
                          : "bg-secondary text-muted-foreground border border-border cursor-not-allowed"
                      )}
                    >
                      {skillPoints > 0
                        ? `Mejorar (1 punto)`
                        : "Sin puntos disponibles"}
                    </button>
                  </div>
                )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            <p className="text-sm">Selecciona una habilidad para ver detalles</p>
          </div>
        )}
      </div>
    </div>
  );
}
