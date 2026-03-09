"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

interface Quest {
  id: string;
  title: string;
  description: string;
  type: "principal" | "secundaria" | "diaria";
  status: "activa" | "completada" | "disponible";
  location: string;
  rewards: {
    gold: number;
    exp: number;
  };
  objectives: {
    text: string;
    current: number;
    required: number;
  }[];
}

interface QuestsPanelProps {
  quests: Quest[];
  onAcceptQuest: (id: string) => void;
  onAbandonQuest: (id: string) => void;
}

const typeColors: Record<string, string> = {
  principal: "text-gold border-gold/30 bg-gold/10",
  secundaria: "text-mana border-mana/30 bg-mana/10",
  diaria: "text-stamina border-stamina/30 bg-stamina/10",
};

const typeLabels: Record<string, string> = {
  principal: "Principal",
  secundaria: "Secundaria",
  diaria: "Diaria",
};

export function QuestsPanel({
  quests,
  onAcceptQuest,
  onAbandonQuest,
}: QuestsPanelProps) {
  const [filter, setFilter] = useState<"todas" | "activa" | "completada" | "disponible">("todas");
  const [selectedQuest, setSelectedQuest] = useState<Quest | null>(null);

  const filteredQuests = quests.filter((q) => filter === "todas" || q.status === filter);

  const activeQuests = quests.filter((q) => q.status === "activa").length;
  const completedQuests = quests.filter((q) => q.status === "completada").length;

  return (
    <div className="flex-1 flex h-full overflow-hidden">
      {/* Quest List */}
      <div className="w-full lg:w-1/2 flex flex-col border-r border-border">
        {/* Header */}
        <div className="p-6 border-b border-border bg-card/50">
          <div className="flex items-center gap-3 mb-4">
            <div>
              <h1 className="text-2xl font-display text-primary tracking-wide">
                Misiones
              </h1>
              <p className="text-sm text-muted-foreground">
                {activeQuests} activas · {completedQuests} completadas
              </p>
            </div>
          </div>

          {/* Filters */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2">
            {(["todas", "activa", "disponible", "completada"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-xs transition-colors capitalize flex-shrink-0",
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

        {/* Quest List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {filteredQuests.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
              <p className="text-sm">No hay misiones</p>
            </div>
          ) : (
            filteredQuests.map((quest) => (
              <button
                key={quest.id}
                onClick={() => setSelectedQuest(quest)}
                className={cn(
                  "w-full text-left p-4 rounded-lg border transition-all",
                  "bg-secondary/30 hover:bg-secondary/50",
                  selectedQuest?.id === quest.id
                    ? "border-primary/50"
                    : "border-border"
                )}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">
                      {quest.status === "completada" ? "✅" : "○"}
                    </span>
                    <h3 className="font-display text-foreground">
                      {quest.title}
                    </h3>
                  </div>
                  <span className="text-muted-foreground">→</span>
                </div>
                <div className="flex items-center gap-2 pl-6">
                  <span
                    className={cn(
                      "px-2 py-0.5 text-xs rounded border",
                      typeColors[quest.type]
                    )}
                  >
                    {typeLabels[quest.type]}
                  </span>
                  <span className="text-xs text-muted-foreground flex items-center gap-1">
                    📍 {quest.location}
                  </span>
                </div>
              </button>
            ))
          )}
        </div>
      </div>

      {/* Quest Detail */}
      <div className="hidden lg:flex lg:w-1/2 flex-col bg-card/30">
        {selectedQuest ? (
          <>
            <div className="p-6 border-b border-border">
              <span
                className={cn(
                  "inline-block px-2 py-1 text-xs rounded border mb-3",
                  typeColors[selectedQuest.type]
                )}
              >
                {typeLabels[selectedQuest.type]}
              </span>
              <h2 className="text-xl font-display text-primary mb-2">
                {selectedQuest.title}
              </h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {selectedQuest.description}
              </p>
            </div>

            <div className="flex-1 p-6 space-y-6 overflow-y-auto">
              {/* Location */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                  Ubicación
                </h3>
                <div className="flex items-center gap-2 text-sm text-foreground">
                  📍 {selectedQuest.location}
                </div>
              </div>

              {/* Objectives */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-3">
                  Objetivos
                </h3>
                <div className="space-y-2">
                  {selectedQuest.objectives.map((obj, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between text-sm"
                    >
                      <span className="text-foreground">{obj.text}</span>
                      <span
                        className={cn(
                          obj.current >= obj.required
                            ? "text-stamina"
                            : "text-muted-foreground"
                        )}
                      >
                        {obj.current}/{obj.required}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Rewards */}
              <div>
                <h3 className="text-xs text-muted-foreground uppercase tracking-wider mb-3">
                  Recompensas
                </h3>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1 text-gold">
                    <span>🪙</span>
                    <span>{selectedQuest.rewards.gold}</span>
                  </div>
                  <div className="flex items-center gap-1 text-primary">
                    <span>⭐</span>
                    <span>{selectedQuest.rewards.exp} EXP</span>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="pt-4 border-t border-border">
                {selectedQuest.status === "disponible" && (
                  <button
                    onClick={() => onAcceptQuest(selectedQuest.id)}
                    className="w-full py-2 px-4 rounded-lg bg-primary/20 text-primary border border-primary/30 hover:bg-primary/30 transition-colors font-display text-sm uppercase tracking-wider"
                  >
                    Aceptar Misión
                  </button>
                )}
                {selectedQuest.status === "activa" && (
                  <button
                    onClick={() => onAbandonQuest(selectedQuest.id)}
                    className="w-full py-2 px-4 rounded-lg bg-secondary text-muted-foreground border border-border hover:bg-secondary/80 transition-colors font-display text-sm uppercase tracking-wider"
                  >
                    Abandonar Misión
                  </button>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            <p className="text-sm">Selecciona una misión para ver detalles</p>
          </div>
        )}
      </div>
    </div>
  );
}
