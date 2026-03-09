"use client";

import { Character } from "@/types/game";
import { 
  Swords, 
  Shield, 
  Zap, 
  Heart,
  Skull,
  Trophy,
  CircleDot
} from "lucide-react";
import { cn } from "@/lib/utils";

interface CombatPanelProps {
  character: Character;
  inCombat: boolean;
  enemy?: {
    name: string;
    level: number;
    health: number;
    maxHealth: number;
    type: string;
  };
  combatLog: string[];
  onAttack: () => void;
  onDefend: () => void;
  onSkill: () => void;
  onFlee: () => void;
}

export function CombatPanel({ 
  character, 
  inCombat,
  enemy,
  combatLog,
  onAttack,
  onDefend,
  onSkill,
  onFlee
}: CombatPanelProps) {
  if (!inCombat || !enemy) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center h-full p-6">
        <div className="text-center max-w-md">
          <div className="w-24 h-24 rounded-full bg-secondary border-2 border-border flex items-center justify-center mx-auto mb-6">
            <Swords className="w-12 h-12 text-muted-foreground" />
          </div>
          <h2 className="text-2xl font-serif text-primary mb-4">Sin Combate Activo</h2>
          <p className="text-muted-foreground mb-6">
            Explora el mundo para encontrar enemigos o acepta misiones de combate para enfrentarte a criaturas.
          </p>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="bg-secondary/50 rounded-lg p-4 border border-border">
              <Trophy className="w-6 h-6 text-gold mx-auto mb-2" />
              <p className="text-muted-foreground">Victorias</p>
              <p className="text-xl font-serif text-foreground">24</p>
            </div>
            <div className="bg-secondary/50 rounded-lg p-4 border border-border">
              <Skull className="w-6 h-6 text-health mx-auto mb-2" />
              <p className="text-muted-foreground">Derrotas</p>
              <p className="text-xl font-serif text-foreground">3</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const playerHealthPercent = (character.health / character.maxHealth) * 100;
  const enemyHealthPercent = (enemy.health / enemy.maxHealth) * 100;

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      {/* Combat Arena */}
      <div className="flex-1 p-6">
        <div className="h-full flex flex-col">
          {/* Combatants */}
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
            {/* Player */}
            <div className="bg-secondary/30 rounded-xl border border-border p-6 text-center">
              <div className="w-20 h-20 rounded-full bg-primary/20 border-2 border-primary/50 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-serif text-primary">
                  {character.name.charAt(0)}
                </span>
              </div>
              <h3 className="font-serif text-primary mb-1">{character.name}</h3>
              <p className="text-xs text-muted-foreground mb-4">Nivel {character.level}</p>
              
              <div className="space-y-2">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-muted-foreground">Salud</span>
                    <span className="text-foreground">{character.health}/{character.maxHealth}</span>
                  </div>
                  <div className="h-3 bg-secondary rounded-full overflow-hidden border border-border">
                    <div 
                      className="h-full bg-health transition-all duration-300"
                      style={{ width: `${playerHealthPercent}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-muted-foreground">Energía</span>
                    <span className="text-foreground">{character.mana}/{character.maxMana}</span>
                  </div>
                  <div className="h-3 bg-secondary rounded-full overflow-hidden border border-border">
                    <div 
                      className="h-full bg-mana transition-all duration-300"
                      style={{ width: `${(character.mana / character.maxMana) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* VS */}
            <div className="flex items-center justify-center">
              <div className="text-4xl font-serif text-primary/50">VS</div>
            </div>

            {/* Enemy */}
            <div className="bg-health/10 rounded-xl border border-health/30 p-6 text-center">
              <div className="w-20 h-20 rounded-full bg-health/20 border-2 border-health/50 flex items-center justify-center mx-auto mb-4">
                <Skull className="w-10 h-10 text-health" />
              </div>
              <h3 className="font-serif text-health mb-1">{enemy.name}</h3>
              <p className="text-xs text-muted-foreground mb-4">{enemy.type} · Nivel {enemy.level}</p>
              
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-muted-foreground">Salud</span>
                  <span className="text-foreground">{enemy.health}/{enemy.maxHealth}</span>
                </div>
                <div className="h-3 bg-secondary rounded-full overflow-hidden border border-border">
                  <div 
                    className="h-full bg-health transition-all duration-300"
                    style={{ width: `${enemyHealthPercent}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Combat Log */}
          <div className="mt-6 bg-secondary/30 rounded-xl border border-border p-4 h-32 overflow-y-auto">
            <div className="space-y-1">
              {combatLog.map((log, i) => (
                <p key={i} className="text-sm text-muted-foreground">
                  <CircleDot className="w-3 h-3 inline mr-2 text-primary" />
                  {log}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Combat Actions */}
      <div className="p-6 border-t border-border bg-card/50">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <button
            onClick={onAttack}
            className={cn(
              "py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all",
              "bg-health/20 text-health border border-health/30 hover:bg-health/30",
              "font-serif text-sm uppercase tracking-wider"
            )}
          >
            <Swords className="w-4 h-4" />
            Atacar
          </button>
          <button
            onClick={onDefend}
            className={cn(
              "py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all",
              "bg-mana/20 text-mana border border-mana/30 hover:bg-mana/30",
              "font-serif text-sm uppercase tracking-wider"
            )}
          >
            <Shield className="w-4 h-4" />
            Defender
          </button>
          <button
            onClick={onSkill}
            className={cn(
              "py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all",
              "bg-primary/20 text-primary border border-primary/30 hover:bg-primary/30",
              "font-serif text-sm uppercase tracking-wider"
            )}
          >
            <Zap className="w-4 h-4" />
            Habilidad
          </button>
          <button
            onClick={onFlee}
            className={cn(
              "py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all",
              "bg-secondary text-muted-foreground border border-border hover:bg-secondary/80",
              "font-serif text-sm uppercase tracking-wider"
            )}
          >
            <Heart className="w-4 h-4" />
            Huir
          </button>
        </div>
      </div>
    </div>
  );
}
