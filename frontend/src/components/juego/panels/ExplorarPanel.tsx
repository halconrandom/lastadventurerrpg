"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Map, ScrollText, Cloud, Sun, Moon, Sunrise, Sunset, Sparkles, AlertTriangle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useExploracion } from "@/hooks/useExploracion";
import { useState, useEffect } from "react";

interface ExplorarPanelProps {
  slot: number;
}

type FaseKey = "madrugada" | "amanecer" | "dia" | "atardecer" | "anochecer" | "noche";

const FASE_ICONS: Record<FaseKey, typeof Sun> = {
  madrugada: Moon,
  amanecer: Sunrise,
  dia: Sun,
  atardecer: Sunset,
  anochecer: Sunset,
  noche: Moon,
};

const FASE_COLORS: Record<FaseKey, string> = {
  madrugada: "text-indigo-400",
  amanecer: "text-orange-400",
  dia: "text-yellow-400",
  atardecer: "text-orange-500",
  anochecer: "text-purple-400",
  noche: "text-blue-300",
};

export function ExplorarPanel({ slot }: ExplorarPanelProps) {
  const {
    zona,
    clima,
    ciclo,
    evento,
    resultadoExploracion,
    resultadoEvento,
    loading,
    log,
    iniciarExploracion,
    explorar,
    obtenerEvento,
    resolverEvento,
    clearEvento,
  } = useExploracion(slot);

  const [showEventoModal, setShowEventoModal] = useState(false);

  useEffect(() => {
    if (evento) {
      setShowEventoModal(true);
    }
  }, [evento]);

  useEffect(() => {
    // Iniciar exploracion al montar
    if (!zona) {
      iniciarExploracion(0, 0);
    }
  }, [zona, iniciarExploracion]);

  const handleExplorar = async () => {
    await explorar();
    
    // 30% de probabilidad de evento
    if (Math.random() < 0.3) {
      await obtenerEvento();
    }
  };

  const handleResolverEvento = async (opcionIndex: number) => {
    await resolverEvento(opcionIndex);
    setShowEventoModal(false);
  };

  const faseKey = (ciclo?.fase || "dia") as FaseKey;
  const FaseIcon = FASE_ICONS[faseKey] || Sun;
  const faseColor = FASE_COLORS[faseKey] || "text-yellow-400";

  return (
    <motion.div
      key="explorar"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="max-w-4xl mx-auto"
    >
      <Card className="border-[#d4a843]/10 bg-card/60 backdrop-blur-md relative overflow-hidden group shadow-2xl">
        <CardContent className="p-10 md:p-14">
          {/* Decorative background */}
          <div className="absolute top-0 right-0 p-12 opacity-5 group-hover:opacity-10 transition-opacity">
            <Map className="w-64 h-64" />
          </div>

          <div className="relative z-10 space-y-8">
            {/* Header con zona y clima */}
            {zona && (
              <div className="space-y-4">
                <h2 className="font-medieval text-4xl text-[#d4a843] tracking-tighter">
                  {zona.nombre}
                </h2>
                
                {/* Info del bioma */}
                <div className="flex flex-wrap gap-3">
                  <span className="px-3 py-1 rounded-full bg-[#d4a843]/10 border border-[#d4a843]/30 text-[#d4a843] text-sm">
                    {zona.bioma.nombre}
                  </span>
                  {zona.bioma.variacion.tipo !== "normal" && (
                    <span className="px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-sm">
                      {zona.bioma.variacion.tipo}
                    </span>
                  )}
                  <span className="px-3 py-1 rounded-full bg-[#2a2a35]/50 text-[#9a978a] text-sm">
                    {zona.estado}
                  </span>
                </div>

                {/* Clima y ciclo */}
                {clima && ciclo && (
                  <div className="flex flex-wrap items-center gap-4 p-4 rounded-xl bg-[#0a0a0f]/40 border border-[#2a2a35]">
                    <div className="flex items-center gap-2">
                      <Cloud className="w-5 h-5 text-[#9a978a]" />
                      <span className="text-[#e8e4d9]">{clima.tipo}</span>
                      <span className="text-[#9a978a] text-sm">({clima.intensidad})</span>
                    </div>
                    
                    <div className="w-px h-4 bg-[#2a2a35]" />
                    
                    <div className="flex items-center gap-2">
                      <FaseIcon className={cn("w-5 h-5", faseColor)} />
                      <span className="text-[#e8e4d9] capitalize">{ciclo.fase}</span>
                      <span className="text-[#9a978a] text-sm">({ciclo.hora}:00)</span>
                    </div>
                  </div>
                )}

                {/* Descripcion del clima */}
                {clima && (
                  <p className="text-[#9a978a] italic text-sm">
                    {clima.descripcion}
                  </p>
                )}
              </div>
            )}

            {/* Log de exploracion */}
            {log.length > 0 && (
              <div className="p-4 rounded-xl bg-[#0a0a0f]/60 border border-[#2a2a35] max-h-48 overflow-y-auto">
                <div className="flex items-center gap-2 mb-3">
                  <ScrollText className="w-4 h-4 text-[#d4a843]" />
                  <span className="text-[#d4a843] text-sm font-bold uppercase tracking-wider">
                    Registro de Exploracion
                  </span>
                </div>
                <div className="space-y-1">
                  {log.map((mensaje, i) => (
                    <motion.p
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="text-[#9a978a] text-sm"
                    >
                      {mensaje}
                    </motion.p>
                  ))}
                </div>
              </div>
            )}

            {/* Resultado de exploracion */}
            {resultadoExploracion && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 rounded-xl bg-[#d4a843]/5 border border-[#d4a843]/20"
              >
                <p className="text-[#e8e4d9]">{resultadoExploracion.descripcion}</p>
                
                {resultadoExploracion.encuentros.length > 0 && (
                  <div className="mt-3 flex items-center gap-2 text-orange-400">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-sm">
                      Encuentro: {resultadoExploracion.encuentros[0].entidad_nombre}
                    </span>
                  </div>
                )}
                
                {resultadoExploracion.poi_descubierto && (
                  <div className="mt-3 flex items-center gap-2 text-[#d4a843]">
                    <Sparkles className="w-4 h-4" />
                    <span className="text-sm">
                      Descubriste: {resultadoExploracion.poi_descubierto.nombre}
                    </span>
                  </div>
                )}
              </motion.div>
            )}

            {/* Boton de explorar */}
            <div className="flex flex-col items-center justify-center py-8 border-2 border-dashed border-[#2a2a35] rounded-3xl bg-[#0a0a0f]/40">
              <div className={cn(
                "w-24 h-24 rounded-full border-2 border-[#d4a843]/20 flex items-center justify-center mb-6 bg-[#d4a843]/5",
                loading && "animate-pulse"
              )}>
                <Map className={cn(
                  "w-10 h-10 text-[#9a978a]",
                  loading && "scale-110 text-[#d4a843]"
                )} />
              </div>

              <Button
                size="lg"
                onClick={handleExplorar}
                disabled={loading || zona?.estado === "agotada"}
                className="min-w-56 py-5 text-lg shadow-[0_0_30px_rgba(212,168,67,0.15)] hover:shadow-[0_0_40px_rgba(212,168,67,0.25)] transition-all"
              >
                {loading ? (
                  <div className="flex items-center gap-3">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Explorando...</span>
                  </div>
                ) : zona?.estado === "agotada" ? (
                  "Zona Agotada"
                ) : (
                  "EXPLORAR ZONA"
                )}
              </Button>
              
              <p className="text-[#9a978a]/50 text-xs mt-4 uppercase tracking-widest">
                Exploraciones: {zona?.veces_explorada || 0}/5
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Modal de Evento */}
      <AnimatePresence>
        {showEventoModal && evento && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => {}}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="max-w-lg w-full bg-[#1a1a24] border border-[#d4a843]/30 rounded-2xl p-8 shadow-2xl"
            >
              <div className="flex items-center gap-3 mb-4">
                <Sparkles className="w-6 h-6 text-[#d4a843]" />
                <span className="text-[#d4a843] text-sm uppercase tracking-wider">
                  {evento.rareza}
                </span>
              </div>
              
              <h3 className="font-medieval text-3xl text-[#d4a843] mb-4">
                {evento.titulo}
              </h3>
              
              <p className="text-[#e8e4d9] mb-8 leading-relaxed">
                {evento.descripcion}
              </p>
              
              <div className="space-y-3">
                {evento.opciones.map((opcion, i) => (
                  <Button
                    key={i}
                    variant="outline"
                    className="w-full justify-start text-left py-4 px-5 border-[#2a2a35] hover:border-[#d4a843]/50 hover:bg-[#d4a843]/5"
                    onClick={() => handleResolverEvento(i)}
                    disabled={loading}
                  >
                    <span className="text-[#d4a843] mr-3">{i + 1}.</span>
                    <span className="text-[#e8e4d9]">{opcion.texto}</span>
                  </Button>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Modal de Resultado de Evento */}
      <AnimatePresence>
        {resultadoEvento && !showEventoModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => clearEvento()}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className={cn(
                "max-w-lg w-full border rounded-2xl p-8 shadow-2xl",
                resultadoEvento.tipo_resultado === "exito"
                  ? "bg-[#1a2418] border-green-500/30"
                  : resultadoEvento.tipo_resultado === "fallo"
                  ? "bg-[#241818] border-red-500/30"
                  : "bg-[#1a1a24] border-[#d4a843]/30"
              )}
            >
              <h3 className={cn(
                "font-medieval text-2xl mb-4",
                resultadoEvento.tipo_resultado === "exito"
                  ? "text-green-400"
                  : resultadoEvento.tipo_resultado === "fallo"
                  ? "text-red-400"
                  : "text-[#d4a843]"
              )}>
                {resultadoEvento.tipo_resultado === "exito"
                  ? "Exito!"
                  : resultadoEvento.tipo_resultado === "fallo"
                  ? "Fallo..."
                  : "Resultado"}
              </h3>
              
              <p className="text-[#e8e4d9] mb-6 leading-relaxed">
                {resultadoEvento.texto_resultado}
              </p>
              
              {resultadoEvento.recompensa && (
                <div className="mb-4 p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                  <span className="text-green-400 text-sm">
                    Recompensa: {JSON.stringify(resultadoEvento.recompensa)}
                  </span>
                </div>
              )}
              
              {resultadoEvento.consecuencia && (
                <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                  <span className="text-red-400 text-sm">
                    Consecuencia: {JSON.stringify(resultadoEvento.consecuencia)}
                  </span>
                </div>
              )}
              
              <Button
                onClick={() => clearEvento()}
                className="w-full"
              >
                Continuar
              </Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
