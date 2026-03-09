"use client";

import * as React from "react";
import { ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import {
  GameLayout,
  SidebarContent,
  SidebarSection,
  SidebarHeader,
  SidebarFooter,
  SidebarToggle,
  useSidebar,
} from "./GameLayout";
import { ProgressBar, ProgressBarCompact, ProgressBarWithIcon } from "@/components/ui/ProgressBar";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipPortal,
} from "@/components/ui/tooltip";
import {
  User,
  Sword,
  Shield,
  Zap,
  Target,
  Heart,
  TrendingUp,
  ChevronDown,
  ChevronRight,
  Lock,
  Sparkles,
} from "lucide-react";

// ============================================
// TIPOS
// ============================================

interface CharacterStats {
  nivel: number;
  experiencia: number;
  experienciaNecesaria: number;
  hp: number;
  hpMax: number;
  mana: number;
  manaMax: number;
  stamina: number;
  staminaMax: number;
  ataque: number;
  defensa: number;
  velocidad: number;
  critico: number;
  evasion: number;
  puntosDistribuibles: number;
}

interface CharacterSenda {
  nombre: string;
  nivel: number;
  experiencia: number;
  experienciaNecesaria: number;
  tipo: string;
  descripcion: string;
}

interface CharacterSidebarProps {
  /** Datos del personaje */
  nombre: string;
  titulo?: string;
  imagenUrl?: string;
  stats: CharacterStats;
  sendas?: CharacterSenda[];
  /** Callback para mejorar stat */
  onMejorarStat?: (stat: string) => void;
  /** Callback para cambiar avatar */
  onCambiarAvatar?: (url: string) => void;
  /** Si está mejorando un stat */
  mejorando?: boolean;
  /** Clases adicionales */
  className?: string;
}

// ============================================
// ICONOS DE STATS
// ============================================

const statIcons: Record<string, ReactNode> = {
  ataque: <Sword className="w-4 h-4" />,
  defensa: <Shield className="w-4 h-4" />,
  velocidad: <Zap className="w-4 h-4" />,
  critico: <Target className="w-4 h-4" />,
  evasion: <Heart className="w-4 h-4" />,
};

const statDescriptions: Record<string, string> = {
  ataque: "Aumenta el daño infligido a los enemigos.",
  defensa: "Reduce el daño recibido de los ataques.",
  velocidad: "Determina quién actúa primero en combate.",
  critico: "Probabilidad de infligir daño crítico.",
  evasion: "Probabilidad de esquivar ataques enemigos.",
};

// ============================================
// COMPONENTE PRINCIPAL
// ============================================

export function CharacterSidebar({
  nombre,
  titulo = "El Último Aventurero",
  imagenUrl,
  stats,
  sendas = [],
  onMejorarStat,
  onCambiarAvatar,
  mejorando = false,
  className,
}: CharacterSidebarProps) {
  const { isCollapsed } = useSidebar();

  return (
    <SidebarContent className={className}>
      {/* Header con avatar y nombre */}
      <SidebarHeader>
        <div className={cn("flex items-center gap-3", isCollapsed && "hidden")}>
          <div className="relative group">
            <Avatar className="w-12 h-12 border-2 border-[#d4a843]/40 shadow-[0_0_15px_rgba(212,168,67,0.2)] group-hover:border-[#d4a843] transition-all">
              <AvatarImage src={imagenUrl} alt={nombre} className="object-cover" />
              <AvatarFallback className="bg-[#12121a] text-[#d4a843]/60">
                <User className="w-6 h-6" />
              </AvatarFallback>
            </Avatar>
            {stats.puntosDistribuibles > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-600 text-white text-[9px] font-bold flex items-center justify-center rounded-full animate-pulse ring-2 ring-[#12121a]">
                !
              </span>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <h2 className="font-[Cinzel] text-lg text-[#d4a843] tracking-wide truncate">
              {nombre}
            </h2>
            <p className="text-[10px] uppercase tracking-widest text-[#9a978a]">
              {titulo}
            </p>
          </div>
        </div>

        {/* Versión colapsada */}
        {isCollapsed && (
          <div className="flex flex-col items-center gap-2">
            <Avatar className="w-10 h-10 border-2 border-[#d4a843]/40">
              <AvatarImage src={imagenUrl} alt={nombre} className="object-cover" />
              <AvatarFallback className="bg-[#12121a] text-[#d4a843]/60">
                <User className="w-5 h-5" />
              </AvatarFallback>
            </Avatar>
            {stats.puntosDistribuibles > 0 && (
              <span className="w-4 h-4 bg-red-600 text-white text-[9px] font-bold flex items-center justify-center rounded-full animate-pulse">
                !
              </span>
            )}
          </div>
        )}
      </SidebarHeader>

      {/* Sección de nivel y experiencia */}
      {!isCollapsed && (
        <div className="px-4 py-3 border-b border-white/5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs uppercase tracking-wider text-[#9a978a]">Nivel</span>
            <span className="font-[Cinzel] text-lg text-[#d4a843]">{stats.nivel}</span>
          </div>
          <ProgressBar
            current={stats.experiencia}
            max={stats.experienciaNecesaria}
            variant="exp"
            size="sm"
            showPercentage
          />
        </div>
      )}

      {/* Barras de estado */}
      {!isCollapsed && (
        <SidebarSection title="Estado" className="pt-4">
          <div className="space-y-3">
            <ProgressBarWithIcon
              current={stats.hp}
              max={stats.hpMax}
              variant="hp"
              icon={<Heart className="w-4 h-4 text-red-400" />}
              label="Salud"
            />
            <ProgressBarWithIcon
              current={stats.mana}
              max={stats.manaMax}
              variant="mana"
              icon={<Sparkles className="w-4 h-4 text-blue-400" />}
              label="Energía"
            />
            <ProgressBarWithIcon
              current={stats.stamina}
              max={stats.staminaMax}
              variant="stamina"
              icon={<Zap className="w-4 h-4 text-green-400" />}
              label="Resistencia"
            />
          </div>
        </SidebarSection>
      )}

      {/* Atributos */}
      {!isCollapsed && (
        <SidebarSection
          title={
            <div className="flex items-center justify-between w-full">
              <span>Atributos</span>
              {stats.puntosDistribuibles > 0 && (
                <span className="text-[9px] bg-[#d4a843] text-black px-2 py-0.5 rounded font-bold animate-pulse">
                  {stats.puntosDistribuibles} PTS
                </span>
              )}
            </div>
          }
          className="pt-2"
        >
          <div className="grid grid-cols-2 gap-2">
            {(["ataque", "defensa", "velocidad", "critico", "evasion"] as const).map((stat) => (
              <Tooltip key={stat}>
                <TooltipTrigger asChild>
                  <div className="flex items-center justify-between p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors cursor-help group">
                    <div className="flex items-center gap-2">
                      <span className="text-[#9a978a] group-hover:text-[#d4a843] transition-colors">
                        {statIcons[stat]}
                      </span>
                      <span className="text-[10px] uppercase tracking-wider text-[#9a978a]">
                        {stat.slice(0, 3)}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span className="text-sm font-medium text-[#e8e4d9]">
                        {stat === "defensa" || stat === "critico" || stat === "evasion"
                          ? `${stats[stat]}%`
                          : stats[stat]}
                      </span>
                      {stats.puntosDistribuibles > 0 && onMejorarStat && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onMejorarStat(stat);
                          }}
                          disabled={mejorando}
                          className="w-4 h-4 rounded bg-[#d4a843] text-black flex items-center justify-center hover:bg-[#f0c654] transition-colors disabled:opacity-50"
                        >
                          <TrendingUp className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  </div>
                </TooltipTrigger>
                <TooltipPortal>
                  <TooltipContent side="top" className="bg-[#0f0f15] border border-[#d4a843]/30 p-3 max-w-xs">
                    <p className="text-[11px] text-[#9a978a] italic">{statDescriptions[stat]}</p>
                  </TooltipContent>
                </TooltipPortal>
              </Tooltip>
            ))}
          </div>
        </SidebarSection>
      )}

      {/* Sendas de combate */}
      {!isCollapsed && sendas.length > 0 && (
        <SidebarSection title="Sendas" collapsible defaultOpen={false}>
          <div className="space-y-2">
            {sendas.map((senda) => (
              <Tooltip key={senda.nombre}>
                <TooltipTrigger asChild>
                  <div className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors cursor-default">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-[#e8e4d9]">{senda.nombre}</span>
                      <span className="text-[10px] text-[#d4a843]">Lv. {senda.nivel}</span>
                    </div>
                    <ProgressBarCompact
                      current={senda.experiencia}
                      max={senda.experienciaNecesaria}
                      variant="exp"
                      showValues={false}
                    />
                  </div>
                </TooltipTrigger>
                <TooltipPortal>
                  <TooltipContent side="left" className="bg-[#0f0f15] border border-[#d4a843]/30 p-3 max-w-xs">
                    <p className="text-[11px] text-[#9a978a] italic">{senda.descripcion}</p>
                  </TooltipContent>
                </TooltipPortal>
              </Tooltip>
            ))}
          </div>
        </SidebarSection>
      )}

      {/* Footer con toggle */}
      <SidebarFooter>
        <SidebarToggle className="w-full justify-center" />
      </SidebarFooter>
    </SidebarContent>
  );
}

// ============================================
// EXPORTS
// ============================================

export { GameLayout, useSidebar };
export type { CharacterSidebarProps, CharacterStats, CharacterSenda };