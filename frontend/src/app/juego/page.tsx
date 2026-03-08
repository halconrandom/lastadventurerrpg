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
  Heart,
  Zap,
  Shield,
} from "lucide-react";

type Tab = "personaje" | "inventario" | "explorar" | "combate";

export default function JuegoPage() {
  const router = useRouter();
  const { datos, slotActual, guardarPartida, reiniciar } = useGame();
  const [tabActiva, tabActivaSet] = useState<Tab>("personaje");
  const [guardando, guardandoSet] = useState(false);

  // Si no hay datos, redirigir al menú
  useEffect(() => {
    if (!datos) {
      router.push("/");
    }
  }, [datos, router]);

  if (!datos) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <p className="text-[#d4a843] font-medieval animate-pulse">Cargando...</p>
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

  const tabs: { id: Tab; nombre: string; icono: React.ReactNode }[] = [
    { id: "personaje", nombre: "Personaje", icono: <User className="w-5 h-5" /> },
    { id: "inventario", nombre: "Inventario", icono: <Package className="w-5 h-5" /> },
    { id: "explorar", nombre: "Explorar", icono: <Map className="w-5 h-5" /> },
    { id: "combate", nombre: "Combate", icono: <Swords className="w-5 h-5" /> },
  ];

  return (
    <main className="min-h-screen bg-[#0a0a0f] flex flex-col">
      {/* Header con info del personaje */}
      <header className="bg-gradient-to-b from-[#12121a] to-[#0a0a0f] border-b border-[#2a2a35] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          {/* Info del personaje */}
          <div className="flex items-center gap-6">
            <div>
              <h1 className="font-medieval text-xl text-[#d4a843]">
                {personaje.nombre}
              </h1>
              <p className="text-sm text-[#9a978a]">
                Nivel {stats.nivel} • {stats.dificultad.charAt(0).toUpperCase() + stats.dificultad.slice(1)}
              </p>
            </div>

            {/* Barra de experiencia */}
            <div className="w-48">
              <StatBar
                label="Experiencia"
                current={stats.experiencia}
                max={stats.experiencia_necesaria}
                type="exp"
                showNumbers={false}
              />
            </div>
          </div>

          {/* Acciones */}
          <div className="flex items-center gap-3">
            <Button variant="secondary" size="sm" onClick={handleGuardar} disabled={guardando}>
              <Save className="w-4 h-4 mr-2" />
              {guardando ? "Guardando..." : "Guardar"}
            </Button>
            <Button variant="danger" size="sm" onClick={handleSalir}>
              <LogOut className="w-4 h-4 mr-2" />
              Salir
            </Button>
          </div>
        </div>
      </header>

      {/* Tabs de navegación */}
      <nav className="bg-[#12121a] border-b border-[#2a2a35]">
        <div className="max-w-6xl mx-auto flex">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => tabActivaSet(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 font-medieval text-sm transition-all duration-300 border-b-2 ${
                tabActiva === tab.id
                  ? "text-[#d4a843] border-[#d4a843] bg-[#0a0a0f]/50"
                  : "text-[#9a978a] border-transparent hover:text-[#d4a843] hover:border-[#a67c00]"
              }`}
            >
              {tab.icono}
              {tab.nombre}
            </button>
          ))}
        </div>
      </nav>

      {/* Contenido principal */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto p-6">
          {/* Tab: Personaje */}
          {tabActiva === "personaje" && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-fade-in">
              {/* Stats principales */}
              <Card className="p-6">
                <h2 className="font-medieval text-xl text-[#d4a843] mb-4">
                  Stats
                </h2>
                <div className="space-y-4">
                  <StatBar
                    label="HP"
                    current={stats.hp}
                    max={stats.hp_max}
                    type="hp"
                  />
                  <StatBar
                    label="Mana"
                    current={stats.mana}
                    max={stats.mana_max}
                    type="mana"
                  />
                  <StatBar
                    label="Stamina"
                    current={stats.stamina}
                    max={stats.stamina_max}
                    type="stamina"
                  />
                </div>

                <div className="mt-6 grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2">
                    <Swords className="w-5 h-5 text-[#d4a843]" />
                    <span className="text-[#9a978a]">Ataque:</span>
                    <span className="text-[#e8e4d9]">{stats.ataque}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-[#3b82f6]" />
                    <span className="text-[#9a978a]">Defensa:</span>
                    <span className="text-[#e8e4d9]">{stats.defensa}%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-[#22c55e]" />
                    <span className="text-[#9a978a]">Velocidad:</span>
                    <span className="text-[#e8e4d9]">{stats.velocidad}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[#9a978a]">Crítico:</span>
                    <span className="text-[#e8e4d9]">{stats.critico}%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[#9a978a]">Evasión:</span>
                    <span className="text-[#e8e4d9]">{stats.evasion}%</span>
                  </div>
                </div>

                {stats.puntos_distribuibles > 0 && (
                  <div className="mt-4 p-3 bg-[#d4a843]/10 border border-[#d4a843] rounded">
                    <p className="text-[#d4a843] text-sm font-medieval">
                      ¡Tienes {stats.puntos_distribuibles} puntos para distribuir!
                    </p>
                  </div>
                )}
              </Card>

              {/* Habilidades */}
              <Card className="p-6">
                <h2 className="font-medieval text-xl text-[#d4a843] mb-4">
                  Habilidades
                </h2>
                <div className="space-y-3">
                  {Object.entries(personaje.habilidades).map(([nombre, datos]) => (
                    <div
                      key={nombre}
                      className="flex justify-between items-center py-2 border-b border-[#2a2a35]"
                    >
                      <div>
                        <p className="font-medieval text-[#e8e4d9] capitalize">
                          {nombre}
                        </p>
                        <p className="text-xs text-[#9a978a]">
                          Nivel {datos.nivel}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-[#d4a843]">
                          {datos.experiencia} / {datos.experiencia_necesaria}
                        </p>
                        <p className="text-xs text-[#9a978a]">EXP</p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {/* Tab: Inventario */}
          {tabActiva === "inventario" && (
            <div className="animate-fade-in">
              <Card className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="font-medieval text-xl text-[#d4a843]">
                    Inventario
                  </h2>
                  <div className="flex items-center gap-4">
                    <span className="text-[#d4a843] font-medieval">
                      💰 {datos.inventario.oro} oro
                    </span>
                    <span className="text-[#9a978a]">
                      {datos.inventario.items.length} / {datos.inventario.slots_maximos} slots
                    </span>
                  </div>
                </div>

                {/* Grid de inventario estilo Diablo */}
                <div className="grid grid-cols-6 gap-2">
                  {Array.from({ length: datos.inventario.slots_maximos }).map((_, i) => {
                    const item = datos.inventario.items[i];
                    return (
                      <div
                        key={i}
                        className="aspect-square bg-[#0a0a0f] border border-[#2a2a35] rounded flex items-center justify-center hover:border-[#d4a843] transition-colors cursor-pointer"
                      >
                        {item ? (
                          <div className="text-center">
                            <span className="text-2xl">📦</span>
                            {item.cantidad > 1 && (
                              <span className="absolute bottom-1 right-1 text-xs text-[#d4a843]">
                                {item.cantidad}
                              </span>
                            )}
                          </div>
                        ) : (
                          <span className="text-[#2a2a35] text-xs">Vacío</span>
                        )}
                      </div>
                    );
                  })}
                </div>

                {datos.inventario.items.length === 0 && (
                  <p className="text-center text-[#9a978a] mt-6">
                    Tu inventario está vacío. ¡Explora para encontrar items!
                  </p>
                )}
              </Card>
            </div>
          )}

          {/* Tab: Explorar */}
          {tabActiva === "explorar" && (
            <div className="animate-fade-in">
              <Card className="p-6">
                <h2 className="font-medieval text-xl text-[#d4a843] mb-4">
                  Exploración
                </h2>
                <div className="text-center py-12">
                  <Map className="w-16 h-16 text-[#9a978a] mx-auto mb-4" />
                  <p className="text-[#9a978a]">
                    Sistema de exploración en desarrollo...
                  </p>
                  <p className="text-[#9a978a]/70 text-sm mt-2">
                    Próximamente podrás explorar zonas y encontrar tesoros.
                  </p>
                </div>
              </Card>
            </div>
          )}

          {/* Tab: Combate */}
          {tabActiva === "combate" && (
            <div className="animate-fade-in">
              <Card className="p-6">
                <h2 className="font-medieval text-xl text-[#d4a843] mb-4">
                  Combate
                </h2>
                <div className="text-center py-12">
                  <Swords className="w-16 h-16 text-[#9a978a] mx-auto mb-4" />
                  <p className="text-[#9a978a]">
                    Sistema de combate en desarrollo...
                  </p>
                  <p className="text-[#9a978a]/70 text-sm mt-2">
                    Próximamente podrás luchar contra enemigos.
                  </p>
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}