"use client";

import { 
  ScrollText, 
  CheckCircle2, 
  Circle, 
  MapPin,
  Coins,
  Star,
  ChevronRight
} from "lucide-react";
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

export function QuestsPanel({ quests, onAcceptQuest, onAbandonQuest }: QuestsPanelProps) {
  const [filter, setFilter] = useState<"todas" | "activa" | "completada" | "disponible">("todas");
  const [selectedQuest, setSelectedQuest] = useState<Quest | null>(null);

  const filteredQuests = quests.filter(q => filter === "todas" || q.status === filter);

  const activeQuests = quests.filter(q => q.status === "activa").length;
  const completedQuests = quests.filter(q => q.status === "completada").length;

  return (
    <div className="flex-1 flex h-full overflow-hidden">
      {/* Quest List */}
      <div className="w-full lg:w-1/2 flex flex-col border-r border-border">
        {/* Header */}
        <div className="p-6 border-b border-border bg-card/50">
          <div className="flex items-center gap-3 mb-4">
            <ScrollText className="w-6 h-6 text-primary" />
            <div>
              <h1 className="text-2xl font-serif text-primary tracking-wide">Misiones</h1>
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
              <ScrollText className="w-12 h-12 mb-4 opacity-50" />
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
                    {quest.status === "completada" ? (
                      <CheckCircle2 className="w-4 h-4 text-stamina" />
                    ) : (
                      <Circle className="w-4 h-4 text-muted-foreground" />
                    )}
                    <h3 className="font-serif text-foreground">{quest.title}</h3>
                  </div>
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </div>
                <div className="flex items-center gap-2 pl-6">
                  <span className={cn(
                    "px-2 py-0.5 text-xs rounded border",
                    typeColors[quest.type]
                  )}>
                    {typeLabels[quest.type]}
                  </span>
                  <span className="text-xs text-muted-foreground flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {quest.location}
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
              <span className={cn(
                "inline-block px-2 py-1 text-xs rounded border mb-3",
                typeColors[selectedQuest.type]
              )}>
                {typeLabels[selectedQuest.type]}
              </span>
              <h2 className="text-xl font-serif text-primary mb-2">{selectedQuest.title}</h2>
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
                  <MapPin className="w-4 h-4 text-primary" />
                  {selectedQuest.location}
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
                      className="flex items-center gap-3 bg-secondary/30 rounded-lg p-3 border border-border"
                    >
                      {obj.current >= obj.required ? (
                        <CheckCircle2 className="w-4 h-4 text-stamina flex-shrink-0" />
                      ) : (
                        <Circle className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                      )}
                      <span className="text-sm text-foreground flex-1">{obj.text}</span>
                      <span className="text-xs text-muted-foreground">
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
                  <div className="flex items-center gap-2 bg-gold/10 rounded-lg px-3 py-2 border border-gold/30">
                    <Coins className="w-4 h-4 text-gold" />
                    <span className="text-sm text-gold">{selectedQuest.rewards.gold}</span>
                  </div>
                  <div className="flex items-center gap-2 bg-primary/10 rounded-lg px-3 py-2 border border-primary/30">
                    <Star className="w-4 h-4 text-primary" />
                    <span className="text-sm text-primary">{selectedQuest.rewards.exp} EXP</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="p-6 border-t border-border">
              {selectedQuest.status === "disponible" ? (
                <button
                  onClick={() => onAcceptQuest(selectedQuest.id)}
                  className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-serif text-sm uppercase tracking-wider hover:bg-primary/90 transition-colors"
                >
                  Aceptar Misión
                </button>
              ) : selectedQuest.status === "activa" ? (
                <button
                  onClick={() => onAbandonQuest(selectedQuest.id)}
                  className="w-full py-3 bg-secondary text-muted-foreground rounded-lg font-serif text-sm uppercase tracking-wider hover:bg-secondary/80 transition-colors border border-border"
                >
                  Abandonar Misión
                </button>
              ) : (
                <div className="text-center text-stamina font-serif text-sm uppercase tracking-wider">
                  <CheckCircle2 className="w-5 h-5 inline mr-2" />
                  Misión Completada
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            <div className="text-center">
              <ScrollText className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p className="text-sm">Selecciona una misión para ver los detalles</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
