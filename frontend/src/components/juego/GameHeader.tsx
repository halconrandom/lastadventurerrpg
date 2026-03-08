"use client";

import { Save, LogOut, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import type { Personaje } from "@/lib/types";
import { cn } from "@/lib/utils";

interface GameHeaderProps {
  personaje: Personaje;
  guardando: boolean;
  onGuardar: () => void;
  onSalir: () => void;
  onOpenSidebar: () => void;
}

function HeaderStat({ label, current, max, type }: { label: string, current: number, max: number, type: 'hp' | 'mana' | 'exp' }) {
  const perc = Math.round((current / max) * 100);
  const colors = {
    hp: "bg-red-600",
    mana: "bg-blue-600",
    exp: "bg-amber-400"
  };

  return (
    <div className="w-full space-y-1">
      <div className="flex justify-between items-center px-1">
        <span className="text-[10px] font-black text-muted-foreground uppercase tracking-wider">{label}</span>
      </div>

      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden border border-white/5">
        <div
          className={cn("h-full transition-all duration-500", colors[type])}
          style={{ width: `${perc}%` }}
        />
      </div>
    </div>
  );
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
    <header className="bg-background/80 backdrop-blur-md border-b border-border px-8 py-6 flex-shrink-0 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-10">

        {/* Info del personaje */}
        <div className="flex items-center gap-8">

          <button
            onClick={onOpenSidebar}
            className="group relative focus:outline-none"
          >
            <Avatar className="size-12 border-2 border-[#d4a843]/40 group-hover:border-[#d4a843] transition-all duration-300 shadow-[0_0_15px_rgba(212,168,67,0.15)]">
              <AvatarImage src={personaje.imagen_url || ""} className="object-cover" />
              <AvatarFallback className="bg-muted text-[#d4a843]/60">
                <User className="size-6" />
              </AvatarFallback>
            </Avatar>
            {stats.puntos_distribuibles > 0 && (
              <span className="absolute -top-1 -right-1 size-4 bg-red-600 text-white text-[9px] font-black flex items-center justify-center rounded-full animate-bounce shadow-lg ring-2 ring-background">
                !
              </span>
            )}
          </button>

          <div className="hidden sm:block space-y-1">
            <div className="flex items-center gap-3">
              <h1 className="font-medieval text-xl text-[#d4a843] tracking-wider leading-none">
                {personaje.nombre}
              </h1>
              <span className="text-[10px] font-black bg-[#d4a843]/20 text-[#d4a843] px-2 py-1 rounded leading-none border border-[#d4a843]/30">
                LV.{stats.nivel}
              </span>

            </div>
            <div className="w-48">
              <HeaderStat label="Experiencia" current={stats.experiencia} max={stats.experiencia_necesaria} type="exp" />
            </div>
          </div>

          {/* Quick Stats Bars */}
          <div className="hidden lg:flex items-center gap-8 ml-4">
            <div className="w-28">
              <HeaderStat label="Salud" current={stats.hp} max={stats.hp_max} type="hp" />
            </div>
            <div className="w-28">
              <HeaderStat label="Energía" current={stats.mana} max={stats.mana_max} type="mana" />
            </div>
          </div>
        </div>

        {/* Acciones */}
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={onGuardar}
            disabled={guardando}
            className="border border-border/50 hover:border-[#d4a843]/40 text-muted-foreground hover:text-foreground h-9 px-4"
          >
            <Save className="size-4 mr-2" />
            <span className="hidden md:inline font-medieval text-[10px] uppercase tracking-widest">{guardando ? "Sellando..." : "Guardar"}</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={onSalir}
            className="text-muted-foreground hover:text-red-500 h-9 px-4"
          >
            <LogOut className="size-4 mr-2" />
            <span className="hidden md:inline font-medieval text-[10px] uppercase tracking-widest">Salir</span>
          </Button>
        </div>
      </div>
    </header>
  );
}

