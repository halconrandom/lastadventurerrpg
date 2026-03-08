"use client";

import { useState } from "react";

import { motion, AnimatePresence } from "framer-motion";
import { useGame } from "@/lib/GameContext";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipPortal,
} from "@/components/ui/tooltip";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import {
  User,
  X,
  Shield,
  Zap,
  Swords,
  Heart,
  Plus,
  Compass,
  Edit2,
  Check,
  Target,
  Wand2,
  Flame,
  Info
} from "lucide-react";
import { cn } from "@/lib/utils";

interface CharacterSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

// Helper para barras de energía con colores específicos
function RPGProgressBar({ label, value, max, colorClass, tooltipTitle, tooltipDesc }: {
  label: string,
  value: number,
  max: number,
  colorClass: string,
  tooltipTitle: string,
  tooltipDesc: string
}) {
  const percentage = Math.round((value / max) * 100);

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <div className="space-y-2 cursor-help group">
          <div className="flex justify-between items-end px-1">
            <span className="text-[10px] uppercase font-bold tracking-widest text-muted-foreground group-hover:text-foreground transition-colors">{label}</span>
            <span className="text-xs font-medieval tracking-tighter">{value} / {max}</span>
          </div>
          <div className="relative h-3 w-full overflow-hidden rounded-full bg-muted border border-white/5 shadow-inner">
            {/* Usamos un div manual para el indicador para tener control total del color sin modificar el componente Progress global demasiado */}
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${percentage}% ` }}
              className={cn("h-full transition-all", colorClass)}
            />
            <div className="absolute inset-0 bg-gradient-to-b from-white/10 to-transparent pointer-events-none" />
          </div>
        </div>
      </TooltipTrigger>
      <TooltipPortal>
        <TooltipContent side="bottom" align="start" className="bg-[#0f0f15] border-[#d4a843]/40 p-4 max-w-xs shadow-2xl z-[100] animate-in fade-in-0 zoom-in-95">
          <div className="space-y-1">
            <p className="font-medieval text-[#d4a843] flex items-center gap-2 border-b border-[#d4a843]/20 pb-1 mb-1">
              <Info className="size-3" /> {tooltipTitle}
            </p>
            <p className="text-[11px] italic leading-relaxed">"{tooltipDesc}"</p>
          </div>
        </TooltipContent>
      </TooltipPortal>

    </Tooltip>
  );
}

export function CharacterSidebar({ isOpen, onClose }: CharacterSidebarProps) {
  const { datos, mejorarStat, actualizarPersonaje } = useGame();
  const [mejorandoStat, mejorandoStatSet] = useState<string | null>(null);
  const [editandoAvatar, editandoAvatarSet] = useState(false);
  const [nuevoAvatarUrl, nuevoAvatarUrlSet] = useState("");

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

  const handleGuardarAvatar = async () => {
    try {
      await actualizarPersonaje({ imagen_url: nuevoAvatarUrl });
      editandoAvatarSet(false);
      nuevoAvatarUrlSet("");
    } catch (error) {
      console.error("Error al guardar avatar:", error);
    }
  };

  const sendasDisponibles = Object.entries(personaje.habilidades)
    .filter(([, h]) => h.nivel > 0 || h.experiencia > 0);

  const getSendaInfo = (nombre: string) => {
    const infos: Record<string, { desc: string, tipo: string, icono: any }> = {
      "Senda del Arco": { desc: "Precision letal desde las sombras", tipo: "Combate Distancia", icono: <Target className="size-5" /> },
      "Senda de las Dagas": { desc: "Velocidad y veneno en cada tajo", tipo: "Combate Ágil", icono: <Swords className="size-5 opacity-70" /> },
      "Senda de la Espada": { desc: "Honor y acero frente al enemigo", tipo: "Combate Físico", icono: <Swords className="size-5" /> },
      "Senda de la Magia": { desc: "Dominio de las artes arcanas", tipo: "Combate Mágico", icono: <Wand2 className="size-5" /> },
      "Senda de la Defensa": { desc: "Un muro inamovible ante el mal", tipo: "Soporte / Tanque", icono: <Shield className="size-5" /> },
    };
    return infos[nombre] || { desc: "Misterios por descubrir", tipo: "Desconocido", icono: <Flame className="size-5" /> };
  };

  return (
    <AnimatePresence mode="wait">
      {isOpen && (
        <motion.aside
          key="character-sidebar"
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -100, opacity: 0 }}
          className="h-full w-full max-w-[32rem] bg-background border-r border-[#d4a843]/20 flex flex-col relative z-50 shadow-2xl"
        >
          {/* Header decorativo superior */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent opacity-40" />

          <div className="pt-16 px-6 h-full flex flex-col gap-5 overflow-y-auto custom-scrollbar">






            {/* 1. CABECERA / PERFIL */}
            <div className="flex items-center justify-between">


              <div className="flex items-center gap-5">
                <div className="relative group">
                  <Avatar className="size-18 border-2 border-[#d4a843]/40 shadow-[0_0_20px_rgba(212,168,67,0.2)] transition-all group-hover:border-[#d4a843]">

                    <AvatarImage src={personaje.imagen_url || ""} alt={personaje.nombre} className="object-cover" />
                    <AvatarFallback className="bg-[#12121a] text-[#d4a843]/40">
                      <User className="size-10" />
                    </AvatarFallback>
                  </Avatar>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="absolute -bottom-1 -right-1 size-8 rounded-full bg-background border border-[#d4a843]/20 hover:bg-[#d4a843]/10 text-[#d4a843]"
                    onClick={() => editandoAvatarSet(!editandoAvatar)}
                  >
                    <Edit2 className="size-4" />
                  </Button>
                </div>

                <div>
                  <h2 className="font-medieval text-3xl text-[#d4a843] tracking-wider leading-none">{personaje.nombre}</h2>
                  <p className="text-[10px] uppercase font-black tracking-[0.2em] text-muted-foreground/80 mt-0.5">El Último Aventurero</p>
                  <div className="flex items-center gap-2 pt-1.5">

                    <span className="text-white font-medieval text-sm bg-[#d4a843]/20 px-3 py-0.5 rounded-lg border border-[#d4a843]/30">NV. {stats.nivel}</span>
                    <span className="text-muted-foreground text-xs capitalize italic">{personaje.genero}</span>
                  </div>
                </div>
              </div>

              <Button variant="ghost" size="icon" onClick={onClose} className="hover:rotate-90 text-muted-foreground transition-all">
                <X className="size-6" />
              </Button>
            </div>

            {/* Editor de Avatar si está activo */}
            <AnimatePresence>
              {editandoAvatar && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-5 rounded-2xl bg-muted/30 border border-[#d4a843]/20 space-y-4">
                    <input
                      type="text"
                      value={nuevoAvatarUrl}
                      onChange={(e) => nuevoAvatarUrlSet(e.target.value)}
                      placeholder="URL de imagen (Imgur preferible)"
                      className="w-full bg-background border border-border rounded-lg px-4 py-2 text-xs focus:ring-1 focus:ring-[#d4a843] focus:outline-none"
                    />
                    <div className="flex justify-end gap-3">
                      <Button variant="outline" size="sm" onClick={() => editandoAvatarSet(false)}>Cancelar</Button>
                      <Button size="sm" onClick={handleGuardarAvatar} className="bg-[#d4a843] text-black hover:bg-[#d4a843]/90">
                        <Check className="size-4 mr-2" /> Aplicar
                      </Button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <Separator className="bg-[#d4a843]/10" />



            {/* 2. ESTADÍSTICAS (HP / Mana / Stamina) */}
            <section className="space-y-6 px-1">



              <RPGProgressBar
                label="Fuerza Vital"
                value={stats.hp}
                max={stats.hp_max}
                colorClass="bg-gradient-to-r from-[#c44536] to-[#8b2942]"
                tooltipTitle="Salud (HP)"
                tooltipDesc="Representa tu fuerza vital. Si llega a 0, tu aventura podría terminar abruptamente."
              />
              <RPGProgressBar
                label="Eter Arcano"
                value={stats.mana}
                max={stats.mana_max}
                colorClass="bg-gradient-to-r from-[#3b82f6] to-[#1d4ed8]"
                tooltipTitle="Energía (Mana)"
                tooltipDesc="Recurso arcano necesario para canalizar habilidades mágicas y poderosos conjuros."
              />
              <RPGProgressBar
                label="Aguante Físico"
                value={stats.stamina}
                max={stats.stamina_max}
                colorClass="bg-gradient-to-r from-[#22c55e] to-[#16a34a]"
                tooltipTitle="Resistencia (Stamina)"
                tooltipDesc="Vital para la exploración física y el uso intensivo de habilidades de combate físico."
              />
            </section>

            {/* 3. ATRIBUTOS (Grid) */}
            <section className="space-y-6">


              <div className="flex justify-between items-center">
                <h3 className="font-medieval text-xl text-[#d4a843] tracking-wide">Atributos del Alma</h3>
                {stats.puntos_distribuibles > 0 && (
                  <span className="text-[9px] bg-[#d4a843] text-black px-2 py-1 rounded-md font-black animate-pulse">
                    {stats.puntos_distribuibles} PUNTOS
                  </span>
                )}
              </div>

              <div className="grid grid-cols-3 gap-4">



                {[
                  { id: "ataque", nombre: "Ataque", valor: stats.ataque, icono: <Swords className="size-4" />, help: "Aumenta el daño infligido a los enemigos." },
                  { id: "defensa", nombre: "Defensa", valor: `${stats.defensa}% `, icono: <Shield className="size-4" />, help: "Reduce el daño recibido." },
                  { id: "velocidad", nombre: "Velocidad", valor: stats.velocidad, icono: <Zap className="size-4" />, help: "Aumenta la probabilidad de actuar primero." },
                  { id: "critico", nombre: "Crítico", valor: `${stats.critico}% `, icono: <Heart className="size-4" />, help: "Probabilidad de infligir daño crítico." },
                  { id: "evasion", nombre: "Evasión", valor: `${stats.evasion}% `, icono: <Compass className="size-4" />, help: "Probabilidad de esquivar ataques." },
                ].map((stat) => (
                  <Tooltip key={stat.id}>
                    <TooltipTrigger asChild>
                      <div className="p-6 rounded-2xl bg-muted/20 border border-border hover:border-[#d4a843]/30 transition-all flex flex-col items-center gap-3 group relative cursor-help">

                        <div className="p-1.5 rounded-lg bg-background text-muted-foreground group-hover:text-[#d4a843] transition-colors shadow-inner opacity-70">

                          {stat.icono}
                        </div>
                        <div className="text-center">
                          <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest">{stat.nombre}</p>
                          <div className="flex items-center justify-center gap-2 mt-1">
                            <span className="text-xl font-medieval text-foreground">{stat.valor}</span>


                            {stats.puntos_distribuibles > 0 && (
                              <Button
                                size="icon"
                                variant="ghost"
                                className="size-5 rounded bg-[#d4a843] text-black hover:bg-white p-0"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleMejorarStat(stat.id);
                                }}
                                disabled={mejorandoStat !== null}
                              >
                                <Plus className="size-3" />
                              </Button>
                            )}
                          </div>
                        </div>
                      </div>
                    </TooltipTrigger>
                    <TooltipContent side="top" className="bg-[#0f0f15] border-[#d4a843]/40">
                      <p className="text-[11px] italic">"{stat.help}"</p>
                    </TooltipContent>
                  </Tooltip>
                ))}
              </div>
            </section>

            {/* 4. COMBATE (Accordion shadcn) */}
            <section className="mb-2">
              <Accordion type="single" collapsible className="w-full space-y-3">


                <AccordionItem value="paths" className="border-none">
                  <AccordionTrigger className="flex items-center justify-between p-5 rounded-2xl bg-muted/30 border border-border hover:border-[#d4a843]/10 hover:no-underline transition-all">

                    <div className="flex items-center gap-4">
                      <div className="p-3 rounded-2xl bg-[#d4a843]/10 text-[#d4a843]">
                        <Swords className="size-6" />
                      </div>
                      <div className="text-left">
                        <h3 className="font-medieval text-lg text-[#d4a843]">Combate y Sendas</h3>
                        <p className="text-[9px] text-muted-foreground uppercase tracking-[0.2em] leading-none mt-1">Senda del Destino</p>
                      </div>

                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="pt-4 pb-0">
                    <div className="space-y-3">
                      {sendasDisponibles.length > 0 ? (
                        sendasDisponibles.map(([nombre, h]) => {
                          const info = getSendaInfo(nombre);
                          const perc = Math.round((h.experiencia / h.experiencia_necesaria) * 100);
                          return (
                            <Tooltip key={nombre}>
                              <TooltipTrigger asChild>
                                <div className="p-4 bg-muted/20 border border-border rounded-2xl transition-all cursor-default group hover:bg-[#d4a843]/5 hover:border-[#d4a843]/20">
                                  <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                      <div className="p-2.5 rounded-xl bg-background text-muted-foreground group-hover:text-[#d4a843] transition-colors">{info.icono}</div>
                                      <div>
                                        <h4 className="font-medieval text-md text-foreground">{nombre}</h4>
                                        <p className="text-[10px] text-muted-foreground italic">Lv. {h.nivel} · {info.tipo}</p>
                                      </div>
                                    </div>
                                    <div className="text-right space-y-1">
                                      <span className="text-[10px] font-black text-[#d4a843]">{perc}%</span>
                                      <Progress value={perc} className="w-20 h-1 bg-muted/50" />
                                    </div>
                                  </div>
                                </div>
                              </TooltipTrigger>
                              <TooltipContent side="right" className="bg-[#0f0f15] border-[#d4a843]/40 p-3 max-w-xs">
                                <p className="text-[11px] italic leading-snug">"{info.desc}"</p>
                              </TooltipContent>
                            </Tooltip>
                          );
                        })
                      ) : (
                        <div className="py-12 text-center border-2 border-dashed border-muted rounded-3xl opacity-40">
                          <Compass className="size-10 text-muted-foreground mx-auto mb-4" />
                          <p className="font-medieval text-sm text-muted-foreground">Aún no has descubierto sendas de combate.</p>
                        </div>
                      )}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </section>

            {/* Footer */}
            <div className="mt-auto pt-4 pb-6">

              <Button
                variant="outline"
                className="w-full py-6 rounded-2xl border-border hover:bg-muted/40 text-muted-foreground hover:text-foreground font-medieval text-xs uppercase tracking-[0.3em] transition-all"
                onClick={onClose}
              >
                Sellar Diario
              </Button>
            </div>
          </div>
        </motion.aside>
      )}

      <style jsx>{`
  .custom - scrollbar:: -webkit - scrollbar {
  width: 4px;
}
        .custom - scrollbar:: -webkit - scrollbar - track {
  background: transparent;
}
        .custom - scrollbar:: -webkit - scrollbar - thumb {
  background: rgba(212, 168, 67, 0.1);
  border - radius: 10px;
}
        .custom - scrollbar:: -webkit - scrollbar - thumb:hover {
  background: rgba(212, 168, 67, 0.4);
}
`}</style>
    </AnimatePresence>
  );
}

