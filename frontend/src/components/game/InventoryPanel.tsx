"use client";

import { InventoryItem } from "@/lib/types";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface InventoryPanelProps {
  items: InventoryItem[];
  capacity: number;
  usedSlots: number;
}

const rarityColors: Record<string, string> = {
  comun: "border-muted-foreground/30 bg-secondary/50",
  poco_comun: "border-stamina/50 bg-stamina/10",
  raro: "border-mana/50 bg-mana/10",
  epico: "border-primary/50 bg-primary/10",
  legendario: "border-gold/50 bg-gold/10 shadow-gold/20 shadow-lg",
};

const rarityTextColors: Record<string, string> = {
  comun: "text-muted-foreground",
  poco_comun: "text-stamina",
  raro: "text-mana",
  epico: "text-primary",
  legendario: "text-gold",
};

const typeLabels: Record<string, string> = {
  weapon: "Armas",
  armor: "Armadura",
  consumable: "Consumibles",
  quest: "Misión",
  material: "Materiales",
};

type FilterType = "todos" | "weapon" | "armor" | "consumable" | "quest" | "material";

export function InventoryPanel({ items, capacity, usedSlots }: InventoryPanelProps) {
  const [filter, setFilter] = useState<FilterType>("todos");
  const [search, setSearch] = useState("");

  const filteredItems = items.filter((item) => {
    const matchesFilter = filter === "todos" || item.type === filter;
    const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const filters: { id: FilterType; label: string }[] = [
    { id: "todos", label: "Todos" },
    { id: "weapon", label: "Armas" },
    { id: "armor", label: "Armadura" },
    { id: "consumable", label: "Consumibles" },
    { id: "quest", label: "Misión" },
    { id: "material", label: "Materiales" },
  ];

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-border bg-card/50">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-display text-primary tracking-wide">
              Inventario
            </h1>
            <p className="text-sm text-muted-foreground">
              {usedSlots}/{capacity} espacios usados
            </p>
          </div>

          {/* Search */}
          <div className="relative">
            <input
              type="text"
              placeholder="Buscar objeto..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full lg:w-64 px-4 py-2 bg-secondary border border-border rounded-lg text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2 mt-4 overflow-x-auto pb-2">
          {filters.map((f) => (
            <button
              key={f.id}
              onClick={() => setFilter(f.id)}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs transition-colors flex-shrink-0",
                filter === f.id
                  ? "bg-primary/20 text-primary border border-primary/30"
                  : "bg-secondary text-muted-foreground hover:text-foreground border border-transparent"
              )}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Items Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        {filteredItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
            <p className="text-sm">No se encontraron objetos</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredItems.map((item) => (
              <div
                key={item.id}
                className={cn(
                  "rounded-lg border p-4 cursor-pointer transition-all hover:scale-105",
                  rarityColors[item.rarity]
                )}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-background/50">
                    <span className={cn("text-lg", rarityTextColors[item.rarity])}>
                      {item.type === "weapon"
                        ? "⚔"
                        : item.type === "armor"
                        ? "🛡"
                        : item.type === "consumable"
                        ? "🧪"
                        : item.type === "quest"
                        ? "📜"
                        : "💎"}
                    </span>
                  </div>
                  {item.quantity > 1 && (
                    <span className="px-2 py-0.5 bg-background/50 rounded text-xs text-foreground">
                      x{item.quantity}
                    </span>
                  )}
                </div>
                <h3
                  className={cn(
                    "font-display text-sm mb-1",
                    rarityTextColors[item.rarity]
                  )}
                >
                  {item.name}
                </h3>
                <p className="text-xs text-muted-foreground line-clamp-2">
                  {item.description}
                </p>
                {item.stats && (
                  <div className="mt-2 pt-2 border-t border-border/50 space-y-1">
                    {Object.entries(item.stats).map(([stat, value]) => (
                      <div key={stat} className="flex justify-between text-xs">
                        <span className="text-muted-foreground capitalize">
                          {stat}
                        </span>
                        <span className="text-foreground">
                          {value > 0 ? "+" : ""}
                          {value}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
