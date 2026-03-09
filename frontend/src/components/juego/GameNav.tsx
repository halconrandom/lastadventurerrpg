"use client";

import { Map, Package, Swords, Compass } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";


export type Tab = "inventario" | "explorar" | "combate" | "mapa";

interface TabItem {
  id: Tab;
  nombre: string;
  icono: React.ReactNode;
}

const tabs: TabItem[] = [
  { id: "explorar", nombre: "Explorar", icono: <Map className="w-5 h-5" /> },
  { id: "mapa", nombre: "Mapa", icono: <Compass className="w-5 h-5" /> },
  { id: "inventario", nombre: "Inventario", icono: <Package className="w-5 h-5" /> },
  { id: "combate", nombre: "Combate", icono: <Swords className="w-5 h-5" /> },
];

interface GameNavProps {
  tabActiva: Tab;
  onTabChange: (tab: Tab) => void;
}

export function GameNav({ tabActiva, onTabChange }: GameNavProps) {
  return (
    <nav className="bg-background/80 backdrop-blur-md border-b border-border sticky top-0 z-30 flex-shrink-0">
      <div className="max-w-7xl mx-auto flex justify-center sm:justify-start">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={cn(
              "flex items-center gap-3 px-12 py-5 font-medieval text-[11px] uppercase tracking-[0.25em] transition-all duration-300 relative focus:outline-none",
              tabActiva === tab.id
                ? "text-[#d4a843]"
                : "text-muted-foreground hover:text-foreground/80"
            )}
          >

            <div className={cn("transition-transform duration-300", tabActiva === tab.id && "scale-110")}>
              {tab.icono}
            </div>
            {tab.nombre}
            {tabActiva === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent shadow-[0_0_10px_rgba(212,168,67,0.3)]"
              />
            )}
          </button>
        ))}
      </div>
    </nav>

  );
}
