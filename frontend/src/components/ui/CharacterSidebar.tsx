"use client";

import { useState } from "react";
import { useGame } from "@/lib/GameContext";
import { StatBar } from "./StatBar";
import { Button } from "./Button";
import {
    User,
    X,
    Shield,
    Zap,
    Swords,
    Heart,
    Plus,
    Compass
} from "lucide-react";

interface CharacterSidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

export function CharacterSidebar({ isOpen, onClose }: CharacterSidebarProps) {
    const { datos, mejorarStat } = useGame();
    const [mejorandoStat, mejorandoStatSet] = useState<string | null>(null);

    if (!datos) return null;

    const { personaje } = datos;
    const { stats } = personaje;

    const handleMejorarStat = async (stat: string) => {
        mejorandoStatSet(stat);
        try {
            await mejorarStat(stat);
        } catch (error) {
            console.error(error);
        } finally {
            mejorandoStatSet(null);
        }
    };

    return (
        <aside
            className={`h-full w-full max-w-md bg-[#0a0a0f] border-r border-[#d4a843]/30 flex-shrink-0 overflow-y-auto custom-scrollbar transition-all duration-500 ease-out shadow-[10px_0_50px_rgba(0,0,0,0.5)] ${isOpen ? "opacity-100" : "w-0 opacity-0 border-r-0"
                }`}
        >
            {/* Header decorativo */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent opacity-50" />

            <div className="p-8 h-full flex flex-col">
                {/* Header */}
                <div className="flex justify-between items-center mb-10">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full border-2 border-[#d4a843] flex items-center justify-center bg-[#d4a843]/10 shadow-[0_0_15px_rgba(212,168,67,0.2)]">
                            <User className="w-6 h-6 text-[#d4a843]" />
                        </div>
                        <div>
                            <h2 className="font-medieval text-2xl text-[#d4a843] leading-none mb-1">
                                Personaje
                            </h2>
                            <p className="text-[#9a978a] text-xs uppercase tracking-widest">
                                Nivel {stats.nivel} • {personaje.genero}
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 text-[#9a978a] hover:text-[#d4a843] transition-colors rounded-full hover:bg-white/5"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Stats Principales */}
                <section className="space-y-6 mb-10 p-6 rounded-2xl bg-white/5 border border-white/10 shadow-inner">
                    <StatBar label="HP" current={stats.hp} max={stats.hp_max} type="hp" />
                    <StatBar label="Mana" current={stats.mana} max={stats.mana_max} type="mana" />
                    <StatBar label="Stamina" current={stats.stamina} max={stats.stamina_max} type="stamina" />
                </section>

                {/* Atributos con puntos */}
                <section className="mb-10">
                    <div className="flex justify-between items-end mb-6">
                        <h3 className="font-medieval text-xl text-[#d4a843]">Atributos</h3>
                        {stats.puntos_distribuibles > 0 && (
                            <span className="text-[10px] bg-[#d4a843] text-[#0a0a0f] px-2 py-0.5 rounded font-bold animate-pulse tracking-tighter">
                                {stats.puntos_distribuibles} PUNTOS
                            </span>
                        )}
                    </div>

                    <div className="grid gap-3">
                        {[
                            { id: "ataque", nombre: "Ataque", icono: <Swords className="w-4 h-4" />, valor: stats.ataque },
                            { id: "defensa", nombre: "Defensa", icono: <Shield className="w-4 h-4" />, valor: `${stats.defensa}%` },
                            { id: "velocidad", nombre: "Velocidad", icono: <Zap className="w-4 h-4" />, valor: stats.velocidad },
                            { id: "critico", nombre: "Crítico", icono: <Heart className="w-4 h-4" />, valor: `${stats.critico}%` },
                            { id: "evasion", nombre: "Evasión", icono: <Compass className="w-4 h-4" />, valor: `${stats.evasion}%` },
                        ].map((stat) => (
                            <div
                                key={stat.id}
                                className="flex items-center justify-between p-3.5 rounded-xl bg-[#12121a]/50 border border-[#2a2a35] hover:border-[#d4a843]/40 transition-all duration-300 group"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="p-2 rounded-lg bg-white/5 text-[#9a978a] group-hover:text-[#d4a843] transition-colors shadow-sm">
                                        {stat.icono}
                                    </div>
                                    <span className="text-[#9a978a] group-hover:text-[#e8e4d9] transition-colors text-sm font-medium">{stat.nombre}</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className="font-medieval text-lg text-white tabular-nums">{stat.valor}</span>
                                    {stats.puntos_distribuibles > 0 && (
                                        <button
                                            onClick={() => handleMejorarStat(stat.id)}
                                            disabled={mejorandoStat !== null}
                                            className="p-1.5 rounded-md bg-[#d4a843] text-[#0a0a0f] hover:bg-[#f3bc56] transition-all active:scale-90 disabled:opacity-30 shadow-[0_0_10px_rgba(212,168,67,0.2)]"
                                            title="Mejorar atributo"
                                        >
                                            <Plus className={`w-3.5 h-3.5 ${mejorandoStat === stat.id ? "animate-spin" : ""}`} />
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Habilidades - Vista rápida */}
                <section className="mb-6">
                    <h3 className="font-medieval text-xl text-[#d4a843] mb-5">Maestrías</h3>
                    <div className="space-y-4">
                        {Object.entries(personaje.habilidades).filter(([, h]) => h.nivel > 0 || h.experiencia > 0).slice(0, 4).map(([nombre, h]) => (
                            <div key={nombre} className="space-y-1.5">
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-[#9a978a] font-medium">{nombre}</span>
                                    <span className="text-[#d4a843] font-medieval">Nv. {h.nivel}</span>
                                </div>
                                <div className="h-1.5 bg-[#12121a] rounded-full overflow-hidden border border-white/5">
                                    <div
                                        className="h-full bg-gradient-to-r from-[#d4a843]/40 to-[#d4a843] shadow-[0_0_8px_rgba(212,168,67,0.3)] transition-all duration-700 ease-out"
                                        style={{ width: `${(h.experiencia / h.experiencia_necesaria) * 100}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Botón de cierre */}
                <div className="mt-auto pt-8">
                    <Button variant="secondary" className="w-full text-xs" onClick={onClose}>
                        Cerrar
                    </Button>
                </div>
            </div>

            <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #2a2a35;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #d4a843;
        }
      `}</style>
        </aside>
    );
}
