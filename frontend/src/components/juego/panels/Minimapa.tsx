"use client";

import { motion } from "framer-motion";
import { Map, Compass, MapPin, Navigation, Eye } from "lucide-react";
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

interface MinimapaProps {
  slot: number;
}

export function Minimapa({ slot }: MinimapaProps) {
  const [estado, setEstado] = useState<EstadoMapa | null>(null);
  const [visual, setVisual] = useState<MapaVisual | null>(null);
  const [ubicaciones, setUbicaciones] = useState<DestinoCercano[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedUbicacion, setSelectedUbicacion] = useState<Ubicacion | null>(null);

  // Cargar datos del mapa
  const cargarMapa = useCallback(async () => {
    if (!slot) return;
    
    try {
      const [estadoData, visualData, ubicacionesData] = await Promise.all([
        getEstadoMapa(slot),
        getMapaVisual(slot, 6),
        getUbicacionesCercanas(slot, 20),
      ]);
      
      setEstado(estadoData);
      setVisual(visualData);
      setUbicaciones(ubicacionesData.ubicaciones);
    } catch (err) {
      console.error("Error cargando mapa:", err);
    }
  }, [slot]);

  useEffect(() => {
    cargarMapa();
  }, [cargarMapa]);

  // Mover a una posicion
  const handleMover = async (x: number, y: number) => {
    if (!slot || loading) return;
    
    setLoading(true);
    try {
      await moverJugador(slot, x, y);
      await cargarMapa();
    } catch (err) {
      console.error("Error al mover:", err);
    } finally {
      setLoading(false);
    }
  };

  // Viajar a ubicacion
  const handleViajar = async (ubicacionId: string) => {
    if (!slot || loading) return;
    
    setLoading(true);
    try {
      await viajarAUbicacion(slot, ubicacionId);
      await cargarMapa();
      setSelectedUbicacion(null);
    } catch (err) {
      console.error("Error al viajar:", err);
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
      const isUbicacion = Object.values(UBICACION_ICONS).includes(celda);
      
      return (
        <div
          key={`${x}-${y}`}
          onClick={() => {
            if (!isJugador && !isNoDescubierto && !loading) {
              const posX = (visual?.posicion[0] || 0) - 6 + x;
              const posY = (visual?.posicion[1] || 0) - 6 + y;
              handleMover(posX, posY);
            }
          }}
          className={cn(
            "w-6 h-6 flex items-center justify-center text-sm transition-all cursor-pointer rounded-sm",
            isJugador && "bg-[#d4a843]/30 border border-[#d4a843] animate-pulse",
            isDescubierto && "bg-[#1a1a24] hover:bg-[#2a2a35]",
            isNoDescubierto && "bg-[#0a0a0f] text-[#1a1a24] cursor-not-allowed",
            isUbicacion && "bg-[#1a1a24] hover:bg-[#2a2a35] hover:scale-110",
            !isJugador && !isNoDescubierto && "hover:ring-1 hover:ring-[#d4a843]/30"
          )}
        >
          {celda}
        </div>
      );
    });
  };

  return (
    <div className="space-y-4">
      {/* Header del minimapa */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Map className="w-5 h-5 text-[#d4a843]" />
          <span className="font-medieval text-lg text-[#d4a843]">Mapa</span>
        </div>
        {estado && (
          <div className="flex items-center gap-3 text-xs text-[#9a978a]">
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              {estado.tiles_explorados}
            </span>
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {estado.ubicaciones_descubiertas}/{estado.total_ubicaciones}
            </span>
          </div>
        )}
      </div>

      {/* Grid del Minimapa */}
      {visual && (
        <div className="p-2 rounded-lg bg-[#0a0a0f]/60 border border-[#2a2a35]">
          <div className="flex justify-center">
            <div className="grid gap-0.5" style={{ gridTemplateColumns: `repeat(${visual.mapa[0]?.length || 13}, 1fr)` }}>
              {visual.mapa.map((fila, y) => renderCelda(fila, y))}
            </div>
          </div>
        </div>
      )}

      {/* Posicion actual */}
      {estado && (
        <div className="p-3 rounded-lg bg-[#0a0a0f]/40 border border-[#2a2a35]">
          <div className="flex items-center gap-2 text-sm">
            <Compass className="w-4 h-4 text-[#d4a843]" />
            <span className="text-[#e8e4d9]">
              ({estado.posicion_jugador[0]}, {estado.posicion_jugador[1]})
            </span>
            {estado.ubicacion_actual && (
              <span className="text-[#9a978a] text-xs">
                - {estado.ubicacion_actual}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Ubicaciones cercanas */}
      <div className="space-y-2">
        <div className="flex items-center gap-2 text-sm text-[#9a978a]">
          <Navigation className="w-4 h-4" />
          <span>Cercanos</span>
        </div>
        
        <div className="space-y-1 max-h-40 overflow-y-auto custom-scrollbar">
          {ubicaciones.length === 0 ? (
            <p className="text-xs text-[#9a978a]/60 text-center py-2">
              Sin ubicaciones cercanas
            </p>
          ) : (
            ubicaciones.slice(0, 6).map((destino) => (
              <div
                key={destino.ubicacion.id}
                onClick={() => destino.descubierta && setSelectedUbicacion(destino.ubicacion)}
                className={cn(
                  "flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-all text-sm",
                  destino.descubierta
                    ? "bg-[#1a1a24] hover:bg-[#2a2a35]"
                    : "bg-[#0a0a0f] opacity-50"
                )}
              >
                <span className="text-base">
                  {UBICACION_ICONS[destino.ubicacion.tipo] || "❓"}
                </span>
                <div className="flex-1 min-w-0">
                  <p className={cn(
                    "truncate",
                    destino.descubierta ? "text-[#e8e4d9]" : "text-[#9a978a]"
                  )}>
                    {destino.descubierta ? destino.ubicacion.nombre : "???"}
                  </p>
                  <p className="text-xs text-[#9a978a]">
                    {destino.distancia} km
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
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
            className="max-w-sm w-full bg-[#1a1a24] border border-[#d4a843]/30 rounded-xl p-5 shadow-2xl"
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">
                {UBICACION_ICONS[selectedUbicacion.tipo] || "❓"}
              </span>
              <div>
                <h3 className="font-medieval text-xl text-[#d4a843]">
                  {selectedUbicacion.nombre}
                </h3>
                <p className="text-xs text-[#9a978a] capitalize">
                  {selectedUbicacion.tipo}
                </p>
              </div>
            </div>
            
            <div className="space-y-2 mb-4 text-xs text-[#9a978a]">
              <p><span className="text-[#e8e4d9]">Bioma:</span> {selectedUbicacion.bioma}</p>
              <p><span className="text-[#e8e4d9]">Segura:</span> {selectedUbicacion.segura ? "Si" : "No"}</p>
              {selectedUbicacion.servicios.length > 0 && (
                <p><span className="text-[#e8e4d9]">Servicios:</span> {selectedUbicacion.servicios.join(", ")}</p>
              )}
            </div>
            
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedUbicacion(null)}
                className="flex-1 border-[#2a2a35]"
              >
                Cancelar
              </Button>
              <Button
                size="sm"
                onClick={() => handleViajar(selectedUbicacion.id)}
                disabled={loading}
                className="flex-1 bg-[#d4a843] hover:bg-[#d4a843]/80 text-black"
              >
                {loading ? "..." : "Viajar"}
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center rounded-lg">
          <div className="w-4 h-4 border-2 border-[#d4a843]/30 border-t-[#d4a843] rounded-full animate-spin" />
        </div>
      )}
    </div>
  );
}