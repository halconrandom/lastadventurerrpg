"use client";

import { User, Save, LogOut } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { StatBar } from "@/components/ui/StatBar";
import type { Personaje } from "@/lib/types";

interface GameHeaderProps {
  personaje: Personaje;
  guardando: boolean;
  onGuardar: () => void;
  onSalir: () => void;
  onOpenSidebar: () => void;
}

export function GameHeader({
  personaje,
  guardando,
  onGuardar,
  onSalir,
  onOpenSidebar,
}: GameHeaderProps) {
  const { stats } = personaje;

  return (
    <header className="bg-gradient-to-b from-[#12121a] to-[#0a0a0f] border-b border-[#2a2a35] px-8 py-5 flex-shrink-0">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Info del personaje */}
        <div className="flex items-center gap-8">
          <button
            onClick={onOpenSidebar}
            className="group relative"
          >
            <div className="w-14 h-14 rounded-full border-2 border-[#d4a843]/40 flex items-center justify-center bg-[#d4a843]/5 group-hover:border-[#d4a843] group-hover:bg-[#d4a843]/10 transition-all duration-300 shadow-[0_0_20px_rgba(212,168,67,0.1)]">
              <User className="w-7 h-7 text-[#d4a843] group-hover:scale-110 transition-transform" />
              {stats.puntos_distribuibles > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-600 text-white text-[10px] font-bold flex items-center justify-center rounded-full animate-bounce shadow-lg">
                  !
                </span>
              )}
            </div>
          </button>

          <div className="hidden md:block">
            <div className="flex items-center gap-3 mb-1.5">
              <h1 className="font-medieval text-2xl text-[#d4a843] tracking-wide">
                {personaje.nombre}
              </h1>
              <span className="text-[10px] bg-[#2a2a35] text-[#9a978a] px-1.5 py-0.5 rounded border border-[#3a3a45]">
                NV. {stats.nivel}
              </span>
            </div>
            <div className="w-64">
              <StatBar
                label=""
                current={stats.experiencia}
                max={stats.experiencia_necesaria}
                type="exp"
                showNumbers={false}
              />
            </div>
          </div>

          {/* Quick Stats Bars */}
          <div className="hidden lg:flex items-center gap-6 ml-4">
            <div className="w-32">
              <StatBar label="HP" current={stats.hp} max={stats.hp_max} type="hp" showNumbers={false} />
            </div>
            <div className="w-32">
              <StatBar label="MP" current={stats.mana} max={stats.mana_max} type="mana" showNumbers={false} />
            </div>
          </div>
        </div>

        {/* Acciones */}
        <div className="flex items-center gap-3">
          <Button
            variant="secondary"
            size="sm"
            onClick={onGuardar}
            disabled={guardando}
            className="bg-transparent border border-[#2a2a35] hover:border-[#d4a843]/50"
          >
            <Save className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">{guardando ? "Salvando..." : "Guardar"}</span>
          </Button>
          <Button variant="danger" size="sm" onClick={onSalir} className="opacity-70 hover:opacity-100">
            <LogOut className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">Salir</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
