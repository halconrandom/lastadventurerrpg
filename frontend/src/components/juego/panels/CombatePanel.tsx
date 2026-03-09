"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Swords,
  Shield,
  Zap,
  Heart,
  Footprints,
  Package,
  Skull,
  Trophy,
  AlertCircle,
  ChevronRight,
  Info
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipProvider,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { useCombate } from "@/hooks/useCombate";
import type { ParticipanteCombate, HabilidadCombate } from "@/lib/types";

export function CombatePanel() {
  const {
    enCombate,
    estado,
    turno,
    jugadores,
    enemigos,
    log,
    cargando,
    error,
    atacar,
    usarHabilidad,
    usarItem,
    bloquear,
    huir,
    resolverTurnoEnemigos,
    finalizarCombate,
    getEnemigosVivos,
    getJugadorActivo,
    esTurnoJugador,
    combateTerminado,
    victoria,
    derrota
  } = useCombate();

  const [objetivoId, objetivoIdSet] = useState<string | null>(null);
  const [recompensas, recompensasSet] = useState<any>(null);
  const [mostrandoRecompensas, mostrandoRecompensasSet] = useState(false);
  const logRef = useRef<HTMLDivElement>(null);

  const jugador = getJugadorActivo();
  const enemigosVivos = getEnemigosVivos();

  // Scroll automático del log
  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [log]);

  // Efecto para autoseleccionar objetivo
  useEffect(() => {
    if (enemigosVivos.length > 0 && (!objetivoId || !enemigosVivos.find(e => e.id === objetivoId))) {
      objetivoIdSet(enemigosVivos[0].id);
    }
  }, [enemigosVivos, objetivoId]);

  // Manejar acciones
  const handleAtacar = async () => {
    if (!objetivoId) return;
    const res = await atacar(objetivoId);
    if (res?.fin_combate) return;

    // Si no ha terminado, esperar un poco y resolver turno enemigo
    setTimeout(async () => {
      await resolverTurnoEnemigos();
    }, 1000);
  };

  const handleBloquear = async () => {
    await bloquear();
    setTimeout(async () => {
      await resolverTurnoEnemigos();
    }, 1000);
  };

  const handleHuir = async () => {
    const res = await huir();
    if (res?.escapo) {
      setTimeout(() => finalizarCombate(), 1500);
    } else {
      setTimeout(async () => {
        await resolverTurnoEnemigos();
      }, 1000);
    }
  };

  const handleFinalizar = async () => {
    const res = await finalizarCombate();
    if (res) {
      recompensasSet(res);
      mostrandoRecompensasSet(true);
    }
  };

  if (!enCombate || !jugador) {
    return (
      <div className="flex items-center justify-center p-20 border-2 border-dashed border-border rounded-3xl opacity-50">
        <p className="font-medieval text-xl text-muted-foreground italic">No hay combate activo...</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto">

      {/* ARENA DE COMBATE (IZQUIERDA) */}
      <div className="lg:col-span-8 space-y-6">
        <Card className="bg-card/40 border-[#d4a843]/10 overflow-hidden relative min-h-[500px] flex flex-col pt-12">
          {/* Fondo decorativo */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(196,69,54,0.05)_0%,_transparent_70%)] pointer-events-none" />

          <CardContent className="flex-1 flex flex-col justify-between relative z-10 p-8">
            {/* ENEMIGOS */}
            <div className="flex justify-center gap-8 py-8">
              <AnimatePresence>
                {enemigos.map((enemigo) => (
                  <motion.div
                    key={enemigo.id}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{
                      scale: enemigo.esta_vivo ? 1 : 0.9,
                      opacity: enemigo.esta_vivo ? 1 : 0.4,
                      y: objetivoId === enemigo.id ? -10 : 0
                    }}
                    className={cn(
                      "relative flex flex-col items-center gap-4 cursor-pointer group p-4 rounded-2xl transition-all",
                      objetivoId === enemigo.id && "bg-[#d4a843]/10 ring-2 ring-[#d4a843]/40"
                    )}
                    onClick={() => enemigo.esta_vivo && objetivoIdSet(enemigo.id)}
                  >
                    {!enemigo.esta_vivo && (
                      <div className="absolute inset-0 flex items-center justify-center z-20">
                        <Skull className="size-16 text-muted-foreground/30 rotate-12" />
                      </div>
                    )}

                    <div className="size-32 rounded-full border-4 border-border bg-muted/20 flex items-center justify-center relative overflow-hidden group-hover:border-[#d4a843]/30 transition-colors">
                      <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-black/60 to-transparent" />
                      <Skull className="size-16 text-muted-foreground/20" />
                    </div>

                    <div className="text-center space-y-1">
                      <h3 className="font-medieval text-xl text-foreground group-hover:text-[#d4a843] transition-colors">
                        {enemigo.nombre}
                      </h3>
                      <Badge variant="outline" className="text-[9px] uppercase tracking-widest bg-red-500/10 text-red-400 border-red-500/20">
                        Nivel {enemigo.nivel}
                      </Badge>

                      <div className="w-32 mt-2">
                        <div className="flex justify-between items-center px-1 mb-1">
                          <span className="text-[10px] text-muted-foreground">HP</span>
                          <span className="text-[10px] text-muted-foreground">{enemigo.hp}/{enemigo.hp_max}</span>
                        </div>
                        <Progress value={(enemigo.hp / enemigo.hp_max) * 100} className="h-1.5 bg-red-950/30 overflow-hidden border border-red-900/10">
                          <div className="h-full bg-red-600 transition-all duration-500" />
                        </Progress>
                      </div>
                    </div>

                    {objetivoId === enemigo.id && enemigo.esta_vivo && (
                      <motion.div
                        layoutId="target"
                        className="absolute -top-4 left-1/2 -translate-x-1/2 text-[#d4a843]"
                        animate={{ y: [0, -5, 0] }}
                        transition={{ repeat: Infinity, duration: 1 }}
                      >
                        <ChevronRight className="size-8 rotate-90" />
                      </motion.div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* JUGADOR */}
            <div className="flex justify-center mt-auto pb-8">
              <motion.div
                className="flex flex-col items-center gap-4"
                animate={{ scale: esTurnoJugador() ? 1.05 : 1 }}
              >
                <div className="size-24 rounded-full border-4 border-[#d4a843]/40 bg-[#12121a] flex items-center justify-center relative shadow-[0_0_30px_rgba(212,168,67,0.1)]">
                  <Swords className="size-10 text-[#d4a843]" />
                  {jugador.esta_bloqueando && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="absolute -top-2 -right-2 bg-blue-600 p-1.5 rounded-lg shadow-lg border-2 border-background"
                    >
                      <Shield className="size-4 text-white" />
                    </motion.div>
                  )}
                </div>

                <div className="text-center w-64 space-y-3">
                  <h3 className="font-medieval text-2xl text-[#d4a843] tracking-wider">{jugador.nombre}</h3>
                  <div className="space-y-2">
                    <Progress value={(jugador.hp / jugador.hp_max) * 100} className="h-2 bg-red-950/20">
                      <div className="h-full bg-gradient-to-r from-red-600 to-red-500 transition-all" />
                    </Progress>
                    <div className="flex justify-between gap-2">
                      <Progress value={(jugador.mana / jugador.mana_max) * 100} className="h-1.5 flex-1 bg-blue-950/20">
                        <div className="h-full bg-gradient-to-r from-blue-600 to-blue-500 transition-all" />
                      </Progress>
                      <Progress value={(jugador.stamina / jugador.stamina_max) * 100} className="h-1.5 flex-1 bg-green-950/20">
                        <div className="h-full bg-gradient-to-r from-green-600 to-green-500 transition-all" />
                      </Progress>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </CardContent>

          {/* MENSAJE DE ESTADO (TURNO) */}
          <div className="absolute bottom-0 left-0 w-full p-4 bg-gradient-to-t from-black/80 to-transparent flex justify-center">
            <div className="px-6 py-2 rounded-full bg-muted/80 backdrop-blur-md border border-border flex items-center gap-3">
              <Badge variant="outline" className="border-[#d4a843]/20 text-[#d4a843]">Turno {turno}</Badge>
              <span className="text-sm font-medieval italic text-foreground/80">
                {combateTerminado()
                  ? (victoria() ? "¡Victoria Real!" : "Has sido derrotado...")
                  : (esTurnoJugador() ? "Tu turno ha llegado, aventurero" : "El enemigo se prepara...")}
              </span>
            </div>
          </div>
        </Card>

        {/* LOG DE COMBATE (Largo abajo) */}
        <Card className="bg-[#0a0a0f] border-border/50">
          <CardContent className="p-4">
            <div className="flex items-center gap-3 mb-3 px-2">
              <Zap className="size-4 text-[#d4a843]" />
              <span className="text-[10px] uppercase font-black tracking-[0.3em] text-muted-foreground">Crónicas de la Batalla</span>
            </div>
            <div
              ref={logRef}
              className="h-32 overflow-y-auto custom-scrollbar space-y-1.5"
            >
              {log.map((entry, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-start gap-3 px-2 py-1 rounded hover:bg-white/5 transition-colors group"
                >
                  <span className="text-[9px] text-[#d4a843]/40 font-medieval shrink-0 pt-0.5">T.{entry.turno}</span>
                  <p className={cn(
                    "text-xs leading-relaxed",
                    entry.actor_id === jugador.id ? "text-foreground" : "text-muted-foreground"
                  )}>
                    {entry.mensaje}
                  </p>
                </motion.div>
              ))}
              {log.length === 0 && (
                <p className="p-4 text-center text-xs italic text-muted-foreground/30">El silencio precede a la tormenta...</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* CONTROLES (DERECHA) */}
      <div className="lg:col-span-4 space-y-6">
        <Card className="bg-gradient-to-b from-[#12121e] to-black border-[#d4a843]/20 shadow-2xl h-full flex flex-col">
          <CardContent className="p-8 flex-1 flex flex-col gap-8">
            <div className="text-center space-y-2">
              <h2 className="font-medieval text-2xl text-[#d4a843]">Acciones Reales</h2>
              <p className="text-[9px] uppercase tracking-[0.2em] text-muted-foreground">Elige tu destino con sabiduría</p>
            </div>

            <Separator className="bg-[#d4a843]/10" />

            {/* BOTONES PRINCIPALES */}
            <div className="grid grid-cols-2 gap-4">
              <Button
                onClick={handleAtacar}
                disabled={!esTurnoJugador() || cargando || combateTerminado() || !objetivoId}
                className="h-24 flex flex-col gap-3 rounded-2xl bg-gradient-to-br from-[#c44536]/10 to-[#8b2942]/10 border-[#c44536]/30 hover:border-[#c44536] hover:bg-[#c44536]/20 transition-all group"
              >
                <Swords className="size-6 text-[#c44536] group-hover:scale-110 transition-transform" />
                <span className="font-medieval text-[11px] tracking-widest uppercase">Atacar</span>
              </Button>

              <Button
                onClick={handleBloquear}
                disabled={!esTurnoJugador() || cargando || combateTerminado()}
                className="h-24 flex flex-col gap-3 rounded-2xl bg-gradient-to-br from-blue-500/10 to-blue-700/10 border-blue-500/30 hover:border-blue-500 hover:bg-blue-500/20 transition-all group"
              >
                <Shield className="size-6 text-blue-400 group-hover:scale-110 transition-transform" />
                <span className="font-medieval text-[11px] tracking-widest uppercase">Bloquear</span>
              </Button>
            </div>

            {/* LISTA DE HABILIDADES / ITEMS */}
            <div className="space-y-4">
              <div className="flex items-center justify-between px-1">
                <span className="text-[10px] uppercase font-black tracking-widest text-[#d4a843]">Perks Activos</span>
                <Zap className="size-3 text-[#d4a843]/40" />
              </div>

              <div className="space-y-2 max-h-48 overflow-y-auto custom-scrollbar pr-2">
                {jugador.habilidades.length > 0 ? (
                  jugador.habilidades.map((hab, i) => (
                    <Button
                      key={i}
                      variant="outline"
                      size="sm"
                      disabled={!esTurnoJugador() || cargando || combateTerminado() || (jugador.mana < hab.costo && jugador.stamina < hab.costo)}
                      className="w-full justify-between h-12 bg-muted/20 border-border/50 hover:border-[#d4a843]/40"
                      onClick={() => usarHabilidad(hab.nombre, objetivoId || undefined)}
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-1.5 rounded bg-background border border-border">
                          <Zap className="size-3 text-[#d4a843]" />
                        </div>
                        <span className="text-xs font-medieval tracking-wide">{hab.nombre}</span>
                      </div>
                      <Badge variant="secondary" className="text-[9px] bg-blue-500/10 text-blue-400">-{hab.costo} MP</Badge>
                    </Button>
                  ))
                ) : (
                  <div className="text-center py-6 px-4 rounded-xl border border-dashed border-border/40 bg-white/[0.02]">
                    <p className="text-[10px] text-muted-foreground italic leading-relaxed">No has aprendido artes secretas aún...</p>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-auto space-y-4">
              <Separator className="bg-[#d4a843]/10" />
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={handleHuir}
                  disabled={!esTurnoJugador() || cargando || combateTerminado()}
                  className="flex-1 border-[#d4a843]/20 hover:bg-[#d4a843]/10 text-muted-foreground hover:text-[#d4a843] h-12 rounded-xl group"
                >
                  <Footprints className="size-4 mr-2 group-hover:-translate-x-1 transition-transform" />
                  <span className="text-[10px] uppercase tracking-widest font-black">Escapar</span>
                </Button>

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-12 w-12 rounded-xl border-border/50"
                      >
                        <Package className="size-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent className="p-3 bg-black border-[#d4a843]/40 shadow-2xl">
                      <p className="text-[10px] uppercase font-black text-[#d4a843] mb-1">Ítems de Combate</p>
                      <p className="text-[10px] text-muted-foreground">Usa pociones para recuperar vitalidad o éter.</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>

              {combateTerminado() && (
                <Button
                  onClick={handleFinalizar}
                  className="w-full h-14 bg-gradient-to-r from-[#d4a843] to-[#b8860b] text-black font-medieval text-lg rounded-xl shadow-[0_0_40px_rgba(212,168,67,0.3)] animate-pulse"
                >
                  {victoria() ? "Sellar Victoria" : "Aceptar Destino"}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* MODAL DE RECOMPENSAS / FIN */}
      <AnimatePresence>
        {mostrandoRecompensas && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-background/90 backdrop-blur-sm"
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              className="max-w-md w-full bg-gradient-to-b from-[#1a1a2e] to-black border-2 border-[#d4a843]/40 rounded-3xl p-10 text-center shadow-[0_0_100px_rgba(212,168,67,0.2)]"
            >
              <div className="mb-8">
                <div className="size-24 rounded-full bg-[#d4a843]/10 border-2 border-[#d4a843]/30 flex items-center justify-center mx-auto mb-6">
                  {victoria() ? (
                    <Trophy className="size-12 text-[#d4a843] animate-bounce" />
                  ) : (
                    <Skull className="size-12 text-muted-foreground/40" />
                  )}
                </div>
                <h2 className="font-medieval text-4xl text-[#d4a843] mb-2 tracking-tighter">
                  {victoria() ? "¡Combate Vencido!" : "Caído en Combate"}
                </h2>
                <p className="text-muted-foreground italic">{victoria() ? "El destino te sonríe una vez más..." : "Tus cenizas descansarán aquí..."}</p>
              </div>

              {victoria() && recompensas && (
                <div className="bg-white/[0.03] rounded-2xl p-6 border border-white/[0.05] space-y-6 mb-10">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1">
                      <p className="text-[10px] uppercase font-black text-blue-400 tracking-widest">Experiencia</p>
                      <p className="text-3xl font-medieval text-white">+{recompensas.experiencia}</p>
                    </div>
                    <div className="space-y-1">
                      <p className="text-[10px] uppercase font-black text-[#d4a843] tracking-widest">Monedas</p>
                      <p className="text-3xl font-medieval text-white">+{recompensas.oro}</p>
                    </div>
                  </div>

                  {recompensas.drops?.length > 0 && (
                    <div className="space-y-3 pt-4 border-t border-white/[0.05]">
                      <p className="text-[9px] uppercase font-black text-muted-foreground tracking-[0.3em]">Artefactos Hallados</p>
                      <div className="flex flex-wrap justify-center gap-2">
                        {recompensas.drops.map((drop: any, i: number) => (
                          <div key={i} className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 flex items-center gap-2">
                            <span className="text-xs">{drop.item_id}</span>
                            <span className="text-[10px] font-black text-[#d4a843]">x{drop.cantidad}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              <Button
                onClick={() => window.location.reload()} // Forzar recarga para resetear estado global si es necesario o manejar vía context
                className="w-full h-14 bg-foreground text-background font-medieval text-lg rounded-xl hover:scale-105 transition-transform"
              >
                Continuar Viaje
              </Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
