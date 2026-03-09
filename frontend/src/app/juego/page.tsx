"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";

import { useGame } from "@/lib/GameContext";
import {
  LoadingScreen,
  GameHeader,
  GameNav,
  CharacterSidebar,
  ExplorarPanel,
  InventarioPanel,
  CombatePanel,
  type Tab,
} from "@/components/juego";

export default function JuegoPage() {
  const router = useRouter();
  const { datos, slotActual, guardarPartida, reiniciar } = useGame();

  // Estados locales
  const [tabActiva, tabActivaSet] = useState<Tab>("explorar");
  const [guardando, guardandoSet] = useState(false);
  const [sidebarAbierto, sidebarAbiertoSet] = useState(false);

  // Si no hay datos, redirigir al menú
  useEffect(() => {
    if (!datos) {
      router.push("/");
    }
  }, [datos, router]);

  // Pantalla de carga
  if (!datos) {
    return <LoadingScreen />;
  }

  const { personaje } = datos;

  // Handlers
  const handleGuardar = async () => {
    guardandoSet(true);
    try {
      await guardarPartida();
      alert("Partida guardada correctamente");
    } catch (error) {
      console.error("Error al guardar:", error);
      alert("Error al guardar la partida");
    } finally {
      guardandoSet(false);
    }
  };

  const handleSalir = () => {
    if (confirm("¿Seguro que quieres salir? Se guardará tu progreso.")) {
      guardarPartida();
      reiniciar();
      router.push("/");
    }
  };

  return (
    <div className="flex bg-[#0a0a0f] min-h-screen">
      {/* Sidebar de Personaje */}
      <CharacterSidebar
        isOpen={sidebarAbierto}
        onClose={() => sidebarAbiertoSet(false)}
      />

      {/* Contenido Principal */}
      <main className="flex-1 flex flex-col selection:bg-[#d4a843]/30 transition-all duration-500 ease-out">
        {/* Header */}
        <GameHeader
          personaje={personaje}
          guardando={guardando}
          onGuardar={handleGuardar}
          onSalir={handleSalir}
          onOpenSidebar={() => sidebarAbiertoSet(true)}
        />

        {/* Navegación de Tabs */}
        <GameNav
          tabActiva={tabActiva}
          onTabChange={tabActivaSet}
        />

        {/* Contenido de Tabs */}
        <div className="flex-1 bg-[radial-gradient(circle_at_center,_#12121a_0%,_#0a0a0f_100%)] overflow-y-auto custom-scrollbar">
          <div className="max-w-7xl mx-auto p-12">

            <AnimatePresence mode="wait">
              {tabActiva === "explorar" ? (
                <motion.div
                  key="panel-explorar"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3 }}
                >
                  <ExplorarPanel slot={slotActual || 1} />
                </motion.div>
              ) : tabActiva === "inventario" ? (
                <motion.div
                  key="panel-inventario"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3 }}
                >
                  <InventarioPanel datos={datos} />
                </motion.div>
              ) : tabActiva === "combate" ? (
                <motion.div
                  key="panel-combate"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3 }}
                >
                  <CombatePanel />
                </motion.div>
              ) : null}
            </AnimatePresence>

          </div>
        </div>
      </main>
    </div>
  );
}
