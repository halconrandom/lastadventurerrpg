"use client";

import { Location, LogEntry } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ExplorationPanelProps {
  location: Location;
  logs: LogEntry[];
  onExplore: () => void;
  isExploring: boolean;
}

const dangerColors: Record<string, string> = {
  seguro: "text-stamina border-stamina/30 bg-stamina/10",
  bajo: "text-gold border-gold/30 bg-gold/10",
  moderado: "text-gold border-gold/30 bg-gold/10",
  alto: "text-health border-health/30 bg-health/10",
  extremo: "text-health border-health/30 bg-health/10",
};

const logTypeStyles: Record<string, string> = {
  exploration: "border-l-mana",
  combat: "border-l-health",
  item: "border-l-gold",
  quest: "border-l-primary",
  system: "border-l-muted-foreground",
};

export function ExplorationPanel({
  location,
  logs,
  onExplore,
  isExploring,
}: ExplorationPanelProps) {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      {/* Location Header */}
      <div className="p-6 border-b border-border bg-card/50">
        <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs text-muted-foreground uppercase tracking-wider">
                Ubicación Actual
              </span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-display text-primary tracking-wide text-balance">
              {location.name}
            </h1>
            <div className="flex flex-wrap items-center gap-3 mt-3">
              <span className="px-2 py-1 bg-secondary text-muted-foreground text-xs rounded border border-border">
                {location.type}
              </span>
              <span
                className={cn(
                  "px-2 py-1 text-xs rounded border capitalize",
                  dangerColors[location.danger]
                )}
              >
                {location.danger}
              </span>
              <span className="text-xs text-muted-foreground">
                Explorado: {location.explored}%
              </span>
            </div>
          </div>

          {/* Weather & Time */}
          <div className="flex items-center gap-4 bg-secondary/50 rounded-lg px-4 py-3 border border-border">
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground capitalize">
                {location.weather}
              </span>
            </div>
            <div className="w-px h-6 bg-border" />
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                {location.timeOfDay}
              </span>
              <span className="text-xs text-muted-foreground">
                ({location.time})
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Exploration Log */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="flex items-center gap-2 mb-4">
          <h2 className="text-sm font-display text-primary uppercase tracking-wider">
            Registro de Exploración
          </h2>
        </div>

        <div className="space-y-3">
          {logs.map((log) => (
            <div
              key={log.id}
              className={cn(
                "bg-secondary/30 rounded-lg p-4 border-l-4 border border-border",
                logTypeStyles[log.type]
              )}
            >
              <p className="text-sm text-foreground/90 leading-relaxed">
                {log.message}
              </p>
              <span className="text-xs text-muted-foreground mt-2 block">
                {log.timestamp.toLocaleTimeString("es-ES", {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Explore Action */}
      <div className="p-6 border-t border-border bg-card/50">
        <div className="flex flex-col items-center gap-4">
          <button
            onClick={onExplore}
            disabled={isExploring}
            className={cn(
              "px-8 py-3 rounded-lg font-display text-sm uppercase tracking-widest transition-all",
              "bg-primary text-primary-foreground hover:bg-primary/90",
              "border border-primary/50 shadow-lg shadow-primary/20",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          >
            {isExploring ? "Explorando..." : "Explorar Zona"}
          </button>
        </div>
      </div>
    </div>
  );
}
