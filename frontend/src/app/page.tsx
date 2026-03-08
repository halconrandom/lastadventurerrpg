"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useGame } from "@/lib/GameContext";
import * as api from "@/lib/api";
import type { Slot } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();
  const { crearNuevaPartida, cargarPartida } = useGame();
  const [slots, setSlots] = useState<Slot[]>([]);
  const [cargando, cargandoSet] = useState(false);
  const [mostrarCargar, mostrarCargarSet] = useState(false);

  // Cargar slots al iniciar
  useEffect(() => {
    async function fetchSlots() {
      try {
        const slotsData = await api.obtenerSlots();
        setSlots(slotsData);
      } catch (error) {
        console.error("Error al cargar slots:", error);
      }
    }
    fetchSlots();
  }, []);

  const handleNuevaPartida = async () => {
    router.push("/nueva-partida");
  };

  const handleCargarPartida = () => {
    mostrarCargarSet(true);
  };

  const handleSeleccionarSlot = async (slot: Slot) => {
    if (!slot.ocupado) return;
    
    cargandoSet(true);
    try {
      await cargarPartida(slot.numero);
      router.push("/juego");
    } catch (error) {
      console.error("Error al cargar partida:", error);
      alert("Error al cargar la partida");
    } finally {
      cargandoSet(false);
    }
  };

  const handleVolver = () => {
    mostrarCargarSet(false);
  };

  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* Fondo animado de calabozo */}
      <div className="absolute inset-0 bg-[#0a0a0f]">
        {/* Patrón de piedras del calabozo */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `
              linear-gradient(90deg, rgba(42,42,53,0.3) 1px, transparent 1px),
              linear-gradient(rgba(42,42,53,0.3) 1px, transparent 1px)
            `,
            backgroundSize: "50px 50px",
          }}
        />

        {/* Gradiente de oscuridad en los bordes */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-transparent to-[#0a0a0f]" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#0a0a0f] via-transparent to-[#0a0a0f]" />
      </div>

      {/* Antorchas animadas */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Antorcha izquierda */}
        <div className="absolute left-[10%] top-[20%]">
          <div className="relative">
            {/* Base de la antorcha */}
            <div className="w-4 h-20 bg-gradient-to-b from-[#4a3728] to-[#2a1f18] rounded-b" />
            {/* Llama */}
            <div className="absolute -top-8 left-1/2 -translate-x-1/2">
              <div className="torch w-6 h-10 bg-gradient-to-t from-[#d4a843] via-[#f0c654] to-[#fff7e0] rounded-full blur-[2px]" />
            </div>
            {/* Resplandor */}
            <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-40 h-40 bg-[#d4a843]/10 rounded-full blur-3xl torch" />
          </div>
        </div>

        {/* Antorcha derecha */}
        <div className="absolute right-[10%] top-[20%]">
          <div className="relative">
            <div className="w-4 h-20 bg-gradient-to-b from-[#4a3728] to-[#2a1f18] rounded-b" />
            <div className="absolute -top-8 left-1/2 -translate-x-1/2">
              <div className="torch w-6 h-10 bg-gradient-to-t from-[#d4a843] via-[#f0c654] to-[#fff7e0] rounded-full blur-[2px]" style={{ animationDelay: "0.25s" }} />
            </div>
            <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-40 h-40 bg-[#d4a843]/10 rounded-full blur-3xl torch" style={{ animationDelay: "0.25s" }} />
          </div>
        </div>

        {/* Antorchas adicionales en la parte inferior */}
        <div className="absolute left-[25%] bottom-[15%]">
          <div className="relative">
            <div className="w-3 h-14 bg-gradient-to-b from-[#4a3728] to-[#2a1f18] rounded-b" />
            <div className="absolute -top-6 left-1/2 -translate-x-1/2">
              <div className="torch w-4 h-8 bg-gradient-to-t from-[#d4a843] via-[#f0c654] to-[#fff7e0] rounded-full blur-[1px]" style={{ animationDelay: "0.5s" }} />
            </div>
            <div className="absolute -top-16 left-1/2 -translate-x-1/2 w-32 h-32 bg-[#d4a843]/5 rounded-full blur-2xl torch" style={{ animationDelay: "0.5s" }} />
          </div>
        </div>

        <div className="absolute right-[25%] bottom-[15%]">
          <div className="relative">
            <div className="w-3 h-14 bg-gradient-to-b from-[#4a3728] to-[#2a1f18] rounded-b" />
            <div className="absolute -top-6 left-1/2 -translate-x-1/2">
              <div className="torch w-4 h-8 bg-gradient-to-t from-[#d4a843] via-[#f0c654] to-[#fff7e0] rounded-full blur-[1px]" style={{ animationDelay: "0.75s" }} />
            </div>
            <div className="absolute -top-16 left-1/2 -translate-x-1/2 w-32 h-32 bg-[#d4a843]/5 rounded-full blur-2xl torch" style={{ animationDelay: "0.75s" }} />
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-8">
        {/* Logo/Título */}
        <div className="mb-16 animate-fade-in">
          <h1 className="font-medieval text-6xl md:text-8xl text-[#d4a843] text-center mb-2 tracking-wider drop-shadow-[0_0_30px_rgba(212,168,67,0.5)]">
            LAST ADVENTURER
          </h1>
          <div className="h-[2px] bg-gradient-to-r from-transparent via-[#d4a843] to-transparent" />
          <p className="text-center text-[#9a978a] mt-4 font-medieval tracking-widest">
            Un viaje hacia lo desconocido
          </p>
        </div>

        {/* Menú principal o selector de slots */}
        {!mostrarCargar ? (
          <div className="flex flex-col gap-4 animate-fade-in" style={{ animationDelay: "0.3s" }}>
            <Button onClick={handleNuevaPartida} size="lg">
              Nueva Partida
            </Button>
            <Button
              onClick={handleCargarPartida}
              variant="secondary"
              size="lg"
              disabled={slots.filter((s) => s.ocupado).length === 0}
            >
              Cargar Partida
            </Button>
            <Button variant="secondary" size="lg" disabled>
              Opciones
            </Button>
          </div>
        ) : (
          <div className="w-full max-w-md animate-fade-in">
            <h2 className="font-medieval text-2xl text-[#d4a843] text-center mb-6">
              Cargar Partida
            </h2>
            <div className="flex flex-col gap-3">
              {slots.map((slot) => (
                <Card
                  key={slot.numero}
                  hoverable={slot.ocupado}
                  selected={false}
                  className={`p-4 ${!slot.ocupado ? "opacity-50" : ""}`}
                  onClick={() => slot.ocupado && handleSeleccionarSlot(slot)}
                >
                  {slot.ocupado ? (
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medieval text-[#d4a843]">
                          {slot.info?.nombre}
                        </p>
                        <p className="text-sm text-[#9a978a]">
                          Nivel {slot.info?.nivel} • {slot.info?.dificultad}
                        </p>
                      </div>
                      <p className="text-sm text-[#9a978a]">
                        {slot.info?.zona}
                      </p>
                    </div>
                  ) : (
                    <p className="text-[#9a978a] text-center">Slot {slot.numero} - Vacío</p>
                  )}
                </Card>
              ))}
            </div>
            <div className="mt-6 text-center">
              <Button variant="secondary" onClick={handleVolver}>
                Volver
              </Button>
            </div>
          </div>
        )}

        {/* Indicador de carga */}
        {cargando && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
            <div className="text-[#d4a843] font-medieval text-xl animate-pulse">
              Cargando...
            </div>
          </div>
        )}
      </div>

      {/* Versión del juego */}
      <div className="absolute bottom-4 right-4 text-[#9a978a]/50 text-sm">
        v1.0.0
      </div>
    </main>
  );
}