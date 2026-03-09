"use client";

import { 
  Sparkles, 
  Lock,
  Zap,
  Flame,
  Droplets,
  Wind,
  Shield,
  Sword
} from "lucide-react";
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

const elementIcons: Record<string, React.ElementType> = {
  fuego: Flame,
  agua: Droplets,
  aire: Wind,
};

const elementColors: Record<string, string> = {
  fuego: "text-health border-health/30 bg-health/10",
  agua: "text-mana border-mana/30 bg-mana/10",
  aire: "text-stamina border-stamina/30 bg-stamina/10",
};

const typeIcons: Record<string, React.ElementType> = {
  ofensiva: Sword,
  defensiva: Shield,
  utilidad: Zap,
};

export function SkillsPanel({ 
  skills, 
  skillPoints, 
  characterLevel,
  onUpgradeSkill 
}: SkillsPanelProps) {
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [filter, setFilter] = useState<"todas" | "ofensiva" | "defensiva" | "utilidad">("todas");

  const filteredSkills = skills.filter(s => filter === "todas" || s.type === filter);

  return (
    <div className="flex-1 flex h-full overflow-hidden">
      {/* Skills Grid */}
      <div className="w-full lg:w-2/3 flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-border bg-card/50">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-3">
              <Sparkles className="w-6 h-6 text-primary" />
              <div>
                <h1 className="text-2xl font-serif text-primary tracking-wide">Habilidades</h1>
                <p className="text-sm text-muted-foreground">
                  Puntos disponibles: <span className="text-primary">{skillPoints}</span>
                </p>
              </div>
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
              const TypeIcon = typeIcons[skill.type] || Zap;
              const ElementIcon = skill.element ? elementIcons[skill.element] : null;
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
                        <Lock className="w-6 h-6 text-muted-foreground mx-auto mb-1" />
                        <span className="text-xs text-muted-foreground">Nv. {skill.requiredLevel}</span>
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between mb-3">
                    <div className={cn(
                      "w-10 h-10 rounded-lg flex items-center justify-center",
                      skill.element ? elementColors[skill.element] : "bg-primary/20"
                    )}>
                      {ElementIcon ? (
                        <ElementIcon className="w-5 h-5" />
                      ) : (
                        <TypeIcon className="w-5 h-5 text-primary" />
                      )}
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {skill.level}/{skill.maxLevel}
                    </span>
                  </div>

                  <h3 className="font-serif text-sm text-foreground mb-1">{skill.name}</h3>
                  
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Droplets className="w-3 h-3 text-mana" />
                      {skill.manaCost}
                    </span>
                    <span>{skill.cooldown}s</span>
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
              <div className={cn(
                "w-16 h-16 rounded-xl flex items-center justify-center mb-4",
                selectedSkill.element 
                  ? elementColors[selectedSkill.element] 
                  : "bg-primary/20"
              )}>
                {selectedSkill.element ? (
                  (() => {
                    const Icon = elementIcons[selectedSkill.element];
                    return <Icon className="w-8 h-8" />;
                  })()
                ) : (
                  (() => {
                    const Icon = typeIcons[selectedSkill.type];
                    return <Icon className="w-8 h-8 text-primary" />;
                  })()
                )}
              </div>
              
              <h2 className="text-xl font-serif text-primary mb-2">{selectedSkill.name}</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {selectedSkill.description}
              </p>
            </div>

            <div className="flex-1 p-6 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-secondary/30 rounded-lg p-3 border border-border">
                  <span className="text-xs text-muted-foreground block mb-1">Tipo</span>
                  <span className="text-sm text-foreground capitalize">{selectedSkill.type}</span>
                </div>
                <div className="bg-secondary/30 rounded-lg p-3 border border-border">
                  <span className="text-xs text-muted-foreground block mb-1">Elemento</span>
                  <span className="text-sm text-foreground capitalize">{selectedSkill.element || "Ninguno"}</span>
                </div>
                <div className="bg-secondary/30 rounded-lg p-3 border border-border">
                  <span className="text-xs text-muted-foreground block mb-1">Coste Maná</span>
                  <span className="text-sm text-mana">{selectedSkill.manaCost}</span>
                </div>
                <div className="bg-secondary/30 rounded-lg p-3 border border-border">
                  <span className="text-xs text-muted-foreground block mb-1">Enfriamiento</span>
                  <span className="text-sm text-foreground">{selectedSkill.cooldown}s</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-muted-foreground">Nivel de habilidad</span>
                  <span className="text-foreground">{selectedSkill.level}/{selectedSkill.maxLevel}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden border border-border">
                  <div 
                    className="h-full bg-primary transition-all duration-300"
                    style={{ width: `${(selectedSkill.level / selectedSkill.maxLevel) * 100}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-border">
              <button
                onClick={() => onUpgradeSkill(selectedSkill.id)}
                disabled={skillPoints === 0 || selectedSkill.level >= selectedSkill.maxLevel || !selectedSkill.unlocked}
                className={cn(
                  "w-full py-3 rounded-lg font-serif text-sm uppercase tracking-wider transition-colors",
                  skillPoints > 0 && selectedSkill.level < selectedSkill.maxLevel && selectedSkill.unlocked
                    ? "bg-primary text-primary-foreground hover:bg-primary/90"
                    : "bg-secondary text-muted-foreground cursor-not-allowed"
                )}
              >
                {selectedSkill.level >= selectedSkill.maxLevel 
                  ? "Nivel Máximo" 
                  : `Mejorar (${skillPoints} puntos)`}
              </button>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            <div className="text-center">
              <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p className="text-sm">Selecciona una habilidad</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
