"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useGame } from "@/lib/GameContext";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { StatBar } from "@/components/ui/StatBar";
import {
  User,
  Package,
  Map,
  Swords,
  Save,
  LogOut,
  ChevronDown,
  ChevronUp,
  Lock,
  Heart,
  Shield,
  Zap,
  LayoutDashboard,
  ScrollText,
} from "lucide-react";
import { CharacterSidebar } from "@/components/ui/CharacterSidebar";


type Tab = "inventario" | "explorar" | "combate";

// Habilidades de combate disponibles
const HABILIDADES_COMBATE = ["Espada", "Espadón", "Arco", "Magia", "Dagas", "Defensa"];

export default function JuegoPage() {
  const router = useRouter();
  const { datos, slotActual, guardarPartida, reiniciar, explorar } = useGame();
  const [tabActiva, tabActivaSet] = useState<Tab>("explorar");
  const [guardando, guardandoSet] = useState(false);
  const [explorando, explorandoSet] = useState(false);
  const [mensajeExploracion, mensajeExploracionSet] = useState<string | null>(null);
  const [sidebarAbierto, sidebarAbiertoSet] = useState(false);

  // Si no hay datos, redirigir al menú
  useEffect(() => {
    if (!datos) {
      router.push("/");
    }
  }, [datos, router]);

  if (!datos) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-[#d4a843]/20 border-t-[#d4a843] rounded-full animate-spin mx-auto mb-4" />
          <p className="text-[#d4a843] font-medieval text-xl">Cargando Mundo...</p>
        </div>
      </div>
    );
  }

  const { personaje } = datos;
  const { stats } = personaje;

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

  const handleExplorar = async () => {
    explorandoSet(true);
    mensajeExploracionSet(null);
    try {
      const msg = await explorar();
      mensajeExploracionSet(msg);
    } catch (error) {
      console.error("Error explorando:", error);
    } finally {
      explorandoSet(false);
    }
  };

  const tabs: { id: Tab; nombre: string; icono: React.ReactNode }[] = [
    { id: "explorar", nombre: "Explorar", icono: <Map className="w-5 h-5" /> },
    { id: "inventario", nombre: "Inventario", icono: <Package className="w-5 h-5" /> },
    { id: "combate", nombre: "Combate", icono: <Swords className="w-5 h-5" /> },
  ];

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      {/* Sidebar de Personaje - Empuja el contenido */}
      <CharacterSidebar
        isOpen={sidebarAbierto}
        onClose={() => sidebarAbiertoSet(false)}
      />

      {/* Contenido Principal - Se mueve cuando el sidebar está abierto */}
      <main className={`flex-1 flex flex-col selection:bg-[#d4a843]/30 transition-all duration-500 ease-out ${sidebarAbierto ? "ml-0" : ""}`}>
        {/* Header con info del personaje */}
      <header className="bg-gradient-to-b from-[#12121a] to-[#0a0a0f] border-b border-[#2a2a35] px-8 py-5">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          {/* Info del personaje */}
          <div className="flex items-center gap-8">
            <button
              onClick={() => sidebarAbiertoSet(true)}
              className="group relative"
            >
              <div className="w-14 h-14 rounded-full border-2 border-[#d4a843]/40 flex items-center justify-center bg-[#d4a843]/5 group-hover:border-[#d4a843] group-hover:bg-[#d4a843]/10 transition-all duration-300 shadow-[0_0_20px_rgba(212,168,67,0.1)]">
                <User className="w-7 h-7 text-[#d4a843] group-hover:scale-110 transition-transform" />
                {stats.puntos_distribuibles > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-600 text-white text-[10px] font-bold flex items-center justify-center rounded-full animate-bounce shadow-lg">
                    !
                  </span>
                )}
              </div>
            </button>

            <div className="hidden md:block">
              <div className="flex items-center gap-3 mb-1.5">
                <h1 className="font-medieval text-2xl text-[#d4a843] tracking-wide">
                  {personaje.nombre}
                </h1>
                <span className="text-[10px] bg-[#2a2a35] text-[#9a978a] px-1.5 py-0.5 rounded border border-[#3a3a45]">
                  NV. {stats.nivel}
                </span>
              </div>
              <div className="w-64">
                <StatBar
                  label=""
                  current={stats.experiencia}
                  max={stats.experiencia_necesaria}
                  type="exp"
                  showNumbers={false}
                />
              </div>
            </div>

            {/* Quick Stats Bars */}
            <div className="hidden lg:flex items-center gap-6 ml-4">
              <div className="w-32"><StatBar label="HP" current={stats.hp} max={stats.hp_max} type="hp" showNumbers={false} /></div>
              <div className="w-32"><StatBar label="MP" current={stats.mana} max={stats.mana_max} type="mana" showNumbers={false} /></div>
            </div>
          </div>

          {/* Acciones */}
          <div className="flex items-center gap-3">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleGuardar}
              disabled={guardando}
              className="bg-transparent border border-[#2a2a35] hover:border-[#d4a843]/50"
            >
              <Save className="w-4 h-4 mr-2" />
              <span className="hidden sm:inline">{guardando ? "Salvando..." : "Guardar"}</span>
            </Button>
            <Button variant="danger" size="sm" onClick={handleSalir} className="opacity-70 hover:opacity-100">
              <LogOut className="w-4 h-4 mr-2" />
              <span className="hidden sm:inline">Salir</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Nav de Pestañas */}
      <nav className="bg-[#12121a]/80 backdrop-blur-md border-b border-[#2a2a35] sticky top-0 z-30">
        <div className="max-w-6xl mx-auto flex justify-center sm:justify-start">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => tabActivaSet(tab.id)}
              className={`flex items-center gap-3 px-10 py-4 font-medieval text-sm uppercase tracking-widest transition-all duration-500 relative ${tabActiva === tab.id
                ? "text-[#d4a843]"
                : "text-[#9a978a] hover:text-[#d4a843]/70"
                }`}
            >
              {tab.icono}
              {tab.nombre}
              {tabActiva === tab.id && (
                <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent" />
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Contenido principal */}
      <div className="flex-1 overflow-auto bg-[radial-gradient(circle_at_center,_#12121a_0%,_#0a0a0f_100%)]">
        <div className="max-w-6xl mx-auto p-8">

          {/* Tab: Explorar */}
          {tabActiva === "explorar" && (
            <div className="animate-fade-in max-w-4xl mx-auto">
              <Card className="p-10 border-[#d4a843]/10 bg-[#0a0a0f]/50 backdrop-blur-sm relative overflow-hidden group">
                <div className="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity">
                  <Map className="w-64 h-64" />
                </div>

                <div className="relative z-10">
                  <h2 className="font-medieval text-3xl text-[#d4a843] mb-2">
                    Tierras Desconocidas
                  </h2>
                  <p className="text-[#9a978a] mb-10 italic">
                    El horizonte se extiende ante ti, lleno de peligros y tesoros por descubrir...
                  </p>

                  {mensajeExploracion && (
                    <div className="mb-10 p-6 rounded-xl bg-[#d4a843]/10 border border-[#d4a843]/30 animate-scale-in">
                      <div className="flex items-start gap-4">
                        <ScrollText className="w-6 h-6 text-[#d4a843] shrink-0" />
                        <p className="text-[#e8e4d9] text-lg font-medieval leading-relaxed">
                          {mensajeExploracion}
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="flex flex-col items-center justify-center py-12 border-2 border-dashed border-[#2a2a35] rounded-3xl bg-[#0a0a0f]/40">
                    <div className={`w-32 h-32 rounded-full border-2 border-[#d4a843]/20 flex items-center justify-center mb-8 bg-[#d4a843]/5 ${explorando ? "animate-pulse" : ""}`}>
                      <Map className={`w-14 h-14 text-[#9a978a] ${explorando ? "scale-110 text-[#d4a843]" : ""}`} />
                    </div>

                    <Button
                      size="lg"
                      onClick={handleExplorar}
                      disabled={explorando}
                      className="min-w-64 py-6 text-xl shadow-[0_0_30px_rgba(212,168,67,0.15)] hover:shadow-[0_0_40px_rgba(212,168,67,0.25)] transition-all"
                    >
                      {explorando ? (
                        <div className="flex items-center gap-3">
                          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          <span>Explorando...</span>
                        </div>
                      ) : (
                        "ADENTRARSE EN EL BOSQUE"
                      )}
                    </Button>
                    <p className="text-[#9a978a]/50 text-xs mt-6 uppercase tracking-widest font-bold">
                      Consume 10 de Stamina (Próximamente)
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* Tab: Inventario */}
          {tabActiva === "inventario" && (
            <div className="animate-fade-in">
              <Card className="p-10 bg-[#0a0a0f]/60 backdrop-blur-md border-[#2a2a35]">
                <div className="flex flex-col md:flex-row justify-between items-center gap-6 mb-12">
                  <div className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-[#d4a843]/10 text-[#d4a843]">
                      <Package className="w-8 h-8" />
                    </div>
                    <div>
                      <h2 className="font-medieval text-3xl text-[#d4a843]">Alforjas del Aventurero</h2>
                      <p className="text-[#9a978a] text-sm uppercase tracking-widest">Capacidad: {datos.inventario.items.length} / {datos.inventario.slots_maximos}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-8 py-3 px-8 rounded-full bg-[#12121a] border border-[#d4a843]/20 shadow-[0_0_20px_rgba(212,168,67,0.05)]">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">💰</span>
                      <span className="text-[#d4a843] font-medieval text-2xl tabular-nums">
                        {datos.inventario.oro}
                      </span>
                      <span className="text-[#9a978a] text-[10px] ml-1 uppercase font-bold">oro</span>
                    </div>
                  </div>
                </div>

                {/* Grid de inventario premium */}
                <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4">
                  {Array.from({ length: datos.inventario.slots_maximos }).map((_, i) => {
                    const item = datos.inventario.items[i];
                    return (
                      <div
                        key={i}
                        className={`aspect-square bg-[#0a0a0f] border-2 rounded-2xl flex items-center justify-center transition-all duration-300 cursor-pointer group relative shadow-inner ${item
                          ? "border-[#d4a843]/30 hover:border-[#d4a843] bg-gradient-to-br from-[#12121a] to-[#0a0a0f]"
                          : "border-[#2a2a35] hover:border-[#3a3a45] opacity-40 hover:opacity-60"
                          }`}
                      >
                        {item ? (
                          <div className="text-center group-hover:scale-110 transition-transform">
                            <span className="text-4xl drop-shadow-[0_0_10px_rgba(0,0,0,0.5)]">📦</span>
                            {item.cantidad > 1 && (
                              <span className="absolute bottom-2 right-2 bg-[#d4a843] text-[#0a0a0f] text-[10px] font-bold px-1.5 py-0.5 rounded-lg shadow-md">
                                x{item.cantidad}
                              </span>
                            )}
                          </div>
                        ) : (
                          <div className="w-4 h-4 rounded-full border border-[#2a2a35]" />
                        )}
                      </div>
                    );
                  })}
                </div>

                {datos.inventario.items.length === 0 && (
                  <div className="text-center py-20 border-t border-[#2a2a35] mt-10">
                    <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                      <Package className="w-8 h-8 text-[#9a978a]/30" />
                    </div>
                    <p className="text-[#9a978a] italic">
                      Tus alforjas están vacías por ahora...
                    </p>
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* Tab: Combate */}
          {tabActiva === "combate" && (
            <div className="animate-fade-in">
              <Card className="p-16 border-dashed border-2 border-[#2a2a35] bg-transparent">
                <div className="text-center">
                  <div className="w-24 h-24 rounded-full bg-[#c44536]/5 border-2 border-[#c44536]/20 flex items-center justify-center mx-auto mb-8">
                    <Swords className="w-12 h-12 text-[#c44536]/40" />
                  </div>
                  <h2 className="font-medieval text-3xl text-[#d4a843] mb-4">
                    Arena de Combate
                  </h2>
                  <p className="text-[#9a978a] max-w-md mx-auto leading-relaxed">
                    Las espadas chocan y la magia vuela. El sistema de combate está siendo forjado por los herreros más hábiles.
                  </p>
                  <div className="mt-10 flex justify-center gap-2">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="w-2 h-2 rounded-full bg-[#d4a843]/20 animate-pulse" style={{ animationDelay: `${i * 0.2}s` }} />
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </main>
    </div>
  );
}