"use client";

import { motion } from "framer-motion";
import { Map, Compass, MapPin, Navigation, Footprints, Eye, Sparkles } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useState, useEffect, useCallback } from "react";
import {
  getEstadoMapa,
  getMapaVisual,
  getUbicacionesCercanas,
  moverJugador,
  viajarAUbicacion,
  explorarTileActual,
  getCartografiaStats,
} from "@/lib/api";
import type { EstadoMapa, MapaVisual, DestinoCercano, Ubicacion } from "@/lib/types";

// Iconos para tipos de ubicacion
const UBICACION_ICONS: Record<string, string> = {
  pueblo: "🏘️",
  ciudad: "🏰",
  capital: "👑",
  mazmorra: "⚔️",
  poi: "✨",
};

// Colores para tipos de ubicacion
const UBICACION_COLORS: Record<string, string> = {
  pueblo: "text-green-400",
  ciudad: "text-blue-400",
  capital: "text-yellow-400",
  mazmorra: "text-red-400",
  poi: "text-purple-400",
};

interface MapaPanelProps {
  slot: number;
}

export function MapaPanel({ slot }: MapaPanelProps) {
  const [estado, setEstado] = useState<EstadoMapa | null>(null);
  const [visual, setVisual] = useState<MapaVisual | null>(null);
  const [ubicaciones, setUbicaciones] = useState<DestinoCercano[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedUbicacion, setSelectedUbicacion] = useState<Ubicacion | null>(null);

  // Cargar datos del mapa
  const cargarMapa = useCallback(async () => {
    if (!slot) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const [estadoData, visualData, ubicacionesData] = await Promise.all([
        getEstadoMapa(slot),
        getMapaVisual(slot, 8),
        getUbicacionesCercanas(slot, 30),
      ]);
      
      setEstado(estadoData);
      setVisual(visualData);
      setUbicaciones(ubicacionesData.ubicaciones);
    } catch (err) {
      console.error("Error cargando mapa:", err);
      setError(err instanceof Error ? err.message : "Error al cargar el mapa");
    } finally {
      setLoading(false);
    }
  }, [slot]);

  useEffect(() => {
    cargarMapa();
  }, [cargarMapa]);

  // Mover a una posicion
  const handleMover = async (x: number, y: number) => {
    if (!slot) return;
    
    setLoading(true);
    try {
      await moverJugador(slot, x, y);
      await cargarMapa();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al mover");
    } finally {
      setLoading(false);
    }
  };

  // Viajar a ubicacion
  const handleViajar = async (ubicacionId: string) => {
    if (!slot) return;
    
    setLoading(true);
    try {
      await viajarAUbicacion(slot, ubicacionId);
      await cargarMapa();
      setSelectedUbicacion(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al viajar");
    } finally {
      setLoading(false);
    }
  };

  // Explorar tile actual
  const handleExplorar = async () => {
    if (!slot) return;
    
    setLoading(true);
    try {
      await explorarTileActual(slot);
      await cargarMapa();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al explorar");
    } finally {
      setLoading(false);
    }
  };

  // Renderizar celda del mapa
  const renderCelda = (fila: string[], y: number) => {
    return fila.map((celda, x) => {
      const isJugador = celda === "📍";
      const isDescubierto = celda === "·";
      const isNoDescubierto = celda === "?";
      
      // Determinar si es una ubicacion
      const isUbicacion = Object.values(UBICACION_ICONS).includes(celda);
      
      return (
        <div
          key={`${x}-${y}`}
          onClick={() => {
            if (!isJugador && !isNoDescubierto) {
              const posX = (visual?.posicion[0] || 0) - 8 + x;
              const posY = (visual?.posicion[1] || 0) - 8 + y;
              handleMover(posX, posY);
            }
          }}
          className={cn(
            "w-8 h-8 flex items-center justify-center text-lg transition-all cursor-pointer rounded",
            isJugador && "bg-[#d4a843]/20 border-2 border-[#d4a843] animate-pulse",
            isDescubierto && "bg-[#1a1a24] hover:bg-[#2a2a35]",
            isNoDescubierto && "bg-[#0a0a0f] text-[#2a2a35] cursor-not-allowed",
            isUbicacion && "bg-[#1a1a24] hover:bg-[#2a2a35] hover:scale-110",
            !isJugador && !isNoDescubierto && "hover:ring-1 hover:ring-[#d4a843]/50"
          )}
          title={isJugador ? "Tu posicion" : isNoDescubierto ? "No descubierto" : `(${(visual?.posicion[0] || 0) - 8 + x}, ${(visual?.posicion[1] || 0) - 8 + y})`}
        >
          {celda}
        </div>
      );
    });
  };

  return (
    <motion.div
      key="mapa"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="max-w-5xl mx-auto"
    >
      <Card className="border-[#d4a843]/10 bg-card/60 backdrop-blur-md relative overflow-hidden group shadow-2xl">
        <CardContent className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Map className="w-8 h-8 text-[#d4a843]" />
              <h2 className="font-medieval text-3xl text-[#d4a843] tracking-tighter">
                Mapa del Mundo
              </h2>
            </div>
            
            {estado && (
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-2 text-[#9a978a]">
                  <Eye className="w-4 h-4" />
                  <span>{estado.tiles_explorados} tiles</span>
                </div>
                <div className="flex items-center gap-2 text-[#9a978a]">
                  <MapPin className="w-4 h-4" />
                  <span>{estado.ubicaciones_descubiertas}/{estado.total_ubicaciones}</span>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* Grid del Mapa */}
          {visual && (
            <div className="mb-6 p-4 rounded-xl bg-[#0a0a0f]/60 border border-[#2a2a35]">
              <div className="flex justify-center">
                <div className="grid gap-0.5" style={{ gridTemplateColumns: `repeat(${visual.mapa[0]?.length || 17}, 1fr)` }}>
                  {visual.mapa.map((fila, y) => renderCelda(fila, y))}
                </div>
              </div>
              
              {/* Leyenda */}
              <div className="mt-4 flex flex-wrap justify-center gap-4 text-xs text-[#9a978a]">
                <span className="flex items-center gap-1">
                  <span className="text-lg">📍</span> Tu posicion
                </span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">·</span> Descubierto
                </span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">?</span> No explorado
                </span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">🏘️</span> Pueblo
                </span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">🏰</span> Ciudad
                </span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">⚔️</span> Mazmorra
                </span>
              </div>
            </div>
          )}

          {/* Posicion actual */}
          {estado && (
            <div className="mb-6 p-4 rounded-xl bg-[#0a0a0f]/40 border border-[#2a2a35]">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Compass className="w-5 h-5 text-[#d4a843]" />
                  <div>
                    <p className="text-[#e8e4d9] font-medium">
                      Posicion: ({estado.posicion_jugador[0]}, {estado.posicion_jugador[1]})
                    </p>
                    {estado.ubicacion_actual && (
                      <p className="text-[#9a978a] text-sm">
                        Ubicacion: {estado.ubicacion_actual}
                      </p>
                    )}
                  </div>
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleExplorar}
                  disabled={loading}
                  className="border-[#d4a843]/30 hover:bg-[#d4a843]/10"
                >
                  <Footprints className="w-4 h-4 mr-2" />
                  Explorar Area
                </Button>
              </div>
            </div>
          )}

          {/* Ubicaciones cercanas */}
          <div className="space-y-4">
            <h3 className="font-medieval text-xl text-[#d4a843] flex items-center gap-2">
              <Navigation className="w-5 h-5" />
              Ubicaciones Cercanas
            </h3>
            
            {ubicaciones.length === 0 ? (
              <p className="text-[#9a978a] text-center py-8">
                No hay ubicaciones cercanas. Explora para descubrir nuevas areas.
              </p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {ubicaciones.slice(0, 8).map((destino, i) => (
                  <motion.div
                    key={destino.ubicacion.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    onClick={() => setSelectedUbicacion(destino.ubicacion)}
                    className={cn(
                      "p-4 rounded-xl border cursor-pointer transition-all",
                      destino.descubierta
                        ? "bg-[#1a1a24] border-[#2a2a35] hover:border-[#d4a843]/30"
                        : "bg-[#0a0a0f] border-[#1a1a24] opacity-60"
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">
                          {UBICACION_ICONS[destino.ubicacion.tipo] || "❓"}
                        </span>
                        <div>
                          <p className={cn(
                            "font-medium",
                            destino.descubierta ? "text-[#e8e4d9]" : "text-[#9a978a]"
                          )}>
                            {destino.descubierta ? destino.ubicacion.nombre : "???"}
                          </p>
                          <p className="text-xs text-[#9a978a]">
                            {destino.ubicacion.tipo} - {destino.distancia} km
                          </p>
                        </div>
                      </div>
                      
                      {destino.descubierta && destino.ubicacion.visitada && (
                        <span title="Visitado">
                          <Sparkles className="w-4 h-4 text-[#d4a843]" />
                        </span>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>

          {/* Modal de ubicacion seleccionada */}
          {selectedUbicacion && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
              onClick={() => setSelectedUbicacion(null)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                onClick={(e) => e.stopPropagation()}
                className="max-w-md w-full bg-[#1a1a24] border border-[#d4a843]/30 rounded-2xl p-6 shadow-2xl"
              >
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-4xl">
                    {UBICACION_ICONS[selectedUbicacion.tipo] || "❓"}
                  </span>
                  <div>
                    <h3 className="font-medieval text-2xl text-[#d4a843]">
                      {selectedUbicacion.nombre}
                    </h3>
                    <p className={cn("text-sm", UBICACION_COLORS[selectedUbicacion.tipo])}>
                      {selectedUbicacion.tipo}
                    </p>
                  </div>
                </div>
                
                <div className="space-y-3 mb-6 text-sm">
                  <p className="text-[#9a978a]">
                    <span className="text-[#e8e4d9]">Bioma:</span> {selectedUbicacion.bioma}
                  </p>
                  <p className="text-[#9a978a]">
                    <span className="text-[#e8e4d9]">Tamano:</span> {selectedUbicacion.tamanio[0]}x{selectedUbicacion.tamanio[1]}
                  </p>
                  <p className="text-[#9a978a]">
                    <span className="text-[#e8e4d9]">Segura:</span> {selectedUbicacion.segura ? "Si" : "No"}
                  </p>
                  {selectedUbicacion.servicios.length > 0 && (
                    <p className="text-[#9a978a]">
                      <span className="text-[#e8e4d9]">Servicios:</span> {selectedUbicacion.servicios.join(", ")}
                    </p>
                  )}
                </div>
                
                <div className="flex gap-3">
                  <Button
                    variant="outline"
                    onClick={() => setSelectedUbicacion(null)}
                    className="flex-1 border-[#2a2a35]"
                  >
                    Cancelar
                  </Button>
                  <Button
                    onClick={() => handleViajar(selectedUbicacion.id)}
                    disabled={loading}
                    className="flex-1 bg-[#d4a843] hover:bg-[#d4a843]/80 text-black"
                  >
                    {loading ? "Viajando..." : "Viajar"}
                  </Button>
                </div>
              </motion.div>
            </motion.div>
          )}

          {/* Loading overlay */}
          {loading && (
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center rounded-xl">
              <div className="flex items-center gap-3 text-[#d4a843]">
                <div className="w-6 h-6 border-2 border-[#d4a843]/30 border-t-[#d4a843] rounded-full animate-spin" />
                <span>Cargando...</span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}