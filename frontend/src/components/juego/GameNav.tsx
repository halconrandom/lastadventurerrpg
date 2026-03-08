"use client";

import { Map, Package, Swords } from "lucide-react";

export type Tab = "inventario" | "explorar" | "combate";

interface TabItem {
  id: Tab;
  nombre: string;
  icono: React.ReactNode;
}

const tabs: TabItem[] = [
  { id: "explorar", nombre: "Explorar", icono: <Map className="w-5 h-5" /> },
  { id: "inventario", nombre: "Inventario", icono: <Package className="w-5 h-5" /> },
  { id: "combate", nombre: "Combate", icono: <Swords className="w-5 h-5" /> },
];

interface GameNavProps {
  tabActiva: Tab;
  onTabChange: (tab: Tab) => void;
}

export function GameNav({ tabActiva, onTabChange }: GameNavProps) {
  return (
    <nav className="bg-[#12121a]/80 backdrop-blur-md border-b border-[#2a2a35] sticky top-0 z-30 flex-shrink-0">
      <div className="max-w-6xl mx-auto flex justify-center sm:justify-start">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-3 px-10 py-4 font-medieval text-sm uppercase tracking-widest transition-all duration-500 relative ${
              tabActiva === tab.id
                ? "text-[#d4a843]"
                : "text-[#9a978a] hover:text-[#d4a843]/70"
            }`}
          >
            {tab.icono}
            {tab.nombre}
            {tabActiva === tab.id && (
              <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent" />
            )}
          </button>
        ))}
      </div>
    </nav>
  );
}
