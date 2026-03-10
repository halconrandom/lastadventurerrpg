"use client";

import { useState, useEffect } from 'react';

export default function TestNPCsPage() {
  const [slots, setSlots] = useState<any[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);
  const [npcs, setNpcs] = useState<any[]>([]);
  const [selectedNpc, setSelectedNpc] = useState<any>(null);
  const [mensaje, setMensaje] = useState("");
  const [chat, setChat] = useState<{ role: string, text: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [tiempo, setTiempo] = useState<any>(null);
  const [lastDebug, setLastDebug] = useState<any>(null);

  useEffect(() => {
    fetchSlots();
  }, []);

  const fetchSlots = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/slots');
      const data = await res.json();
      setSlots(data.slots || []);
    } catch (e) {
      console.error("Error fetching slots", e);
    }
  };

  const loadNpcs = async (slotNum: number) => {
    setSelectedSlot(slotNum);
    setLoading(true);
    try {
      // Cargar partida para asegurar que el manager esté inicializado
      await fetch(`http://localhost:5000/api/partida/${slotNum}`);
      
      const res = await fetch(`http://localhost:5000/api/npcs/lista?slot=${slotNum}`);
      const data = await res.json();
      setNpcs(data.data || []);

      // Obtener tiempo
      const resPartida = await fetch(`http://localhost:5000/api/partida/${slotNum}`);
      const dataPartida = await resPartida.json();
      if (dataPartida.success) {
        setTiempo(dataPartida.data.tiempo_estado || dataPartida.data.tiempo);
      }

    } catch (e) {
      console.error("Error loading NPCs", e);
    } finally {
      setLoading(false);
    }
  };

  const enviarMensaje = async () => {
    if (!selectedNpc || !mensaje || !selectedSlot) return;

    const nuevoChat = [...chat, { role: 'jugador', text: mensaje }];
    setChat(nuevoChat);
    setMensaje("");
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:5000/api/npcs/${selectedNpc.id}/hablar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slot: selectedSlot, mensaje })
      });
      const data = await res.json();
      
      if (data.success) {
        setChat([...nuevoChat, { role: 'npc', text: data.data.respuesta }]);
        setLastDebug(data.data.debug || null);
      } else {
        setChat([...nuevoChat, { role: 'error', text: data.message }]);
      }
    } catch (e) {
      setChat([...nuevoChat, { role: 'error', text: "Error de conexión con el backend" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 bg-zinc-950 text-zinc-100 min-h-screen font-mono">
      <h1 className="text-2xl font-bold mb-6 border-b border-zinc-800 pb-2 text-amber-500">
        NPC & LLM DEBUG TERMINAL
      </h1>

      {!selectedSlot ? (
        <div className="grid grid-cols-3 gap-4">
          {slots.map(s => (
            <button 
              key={s.numero}
              onClick={() => loadNpcs(s.numero)}
              className={`p-4 border ${s.ocupado ? 'border-zinc-700 hover:bg-zinc-900' : 'border-zinc-800 opacity-50 cursor-not-allowed'}`}
              disabled={!s.ocupado}
            >
              Slot {s.numero} {s.ocupado ? `(${s.info.nombre})` : '(Vacío)'}
            </button>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar NPCs */}
          <div className="col-span-3 border-r border-zinc-800 pr-4">
            <button onClick={() => setSelectedSlot(null)} className="text-xs mb-4 text-zinc-500 hover:text-white">
              &lt; Volver a Slots
            </button>
            <h2 className="text-sm font-bold mb-4 text-zinc-400 uppercase tracking-widest">NPCs Activos</h2>
            <div className="space-y-2">
              {npcs.map(n => (
                <div 
                  key={n.id}
                  onClick={() => { setSelectedNpc(n); setChat([]); }}
                  className={`p-2 text-sm cursor-pointer border ${selectedNpc?.id === n.id ? 'bg-amber-900/20 border-amber-700' : 'border-transparent hover:bg-zinc-900'}`}
                >
                  {n.nombre} <span className="text-xs text-zinc-500">[{n.rol.tipo}]</span>
                </div>
              ))}
            </div>
          </div>

          {/* Chat / Info */}
          <div className="col-span-9 flex flex-col h-[80vh]">
            {selectedNpc ? (
              <>
                <div className="mb-4 p-4 bg-zinc-900 border border-zinc-800 text-xs grid grid-cols-3 gap-2">
                  <div><span className="text-zinc-500">Raza:</span> {selectedNpc.raza}</div>
                  <div><span className="text-zinc-500">Personalidad:</span> {selectedNpc.personalidad.rasgos.join(", ")}</div>
                  <div><span className="text-zinc-500">Relación:</span> {selectedNpc.relaciones.jugador.reputacion.estado}</div>
                  <div><span className="text-zinc-500">Hora:</span> {tiempo?.hora || "08:00"}</div>
                  <div><span className="text-zinc-500">Fase:</span> {tiempo?.fase || "Día"}</div>
                  <div><span className="text-zinc-500">Ubicación:</span> {selectedNpc.ubicacion.ubicacion_id}</div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 bg-black border border-zinc-800 mb-4 space-y-4">
                  {chat.map((c, i) => (
                    <div key={i} className={`${c.role === 'jugador' ? 'text-right' : 'text-left'}`}>
                      <span className={`text-[10px] uppercase ${c.role === 'jugador' ? 'text-blue-500' : 'text-amber-500'}`}>
                        {c.role === 'jugador' ? 'Tú' : selectedNpc.nombre}
                      </span>
                      <p className={`mt-1 p-2 inline-block max-w-[80%] text-sm ${c.role === 'jugador' ? 'bg-blue-900/20 border border-blue-800' : 'bg-zinc-900 border border-zinc-800'}`}>
                        {c.text}
                      </p>
                    </div>
                  ))}
                  {loading && <div className="text-zinc-500 animate-pulse text-xs">Procesando respuesta...</div>}
                </div>

                {/* Panel de debug del nuevo pipeline cognitivo */}
                {lastDebug && (
                  <div className="mb-3 p-3 bg-zinc-900 border border-zinc-700 text-[11px] font-mono grid grid-cols-3 gap-x-4 gap-y-1">
                    <div>
                      <span className="text-zinc-500">INTENT </span>
                      <span className="text-cyan-400">{lastDebug.intent ?? '—'}</span>
                    </div>
                    <div>
                      <span className="text-zinc-500">AGRESIÓN </span>
                      <span className={lastDebug.agresion > 0.5 ? 'text-red-400' : 'text-green-400'}>
                        {lastDebug.agresion?.toFixed(2) ?? '—'}
                      </span>
                    </div>
                    <div>
                      <span className="text-zinc-500">META </span>
                      <span className="text-yellow-400">{lastDebug.meta_activa ?? '—'}</span>
                    </div>
                    <div>
                      <span className="text-zinc-500">EMOCIÓN </span>
                      <span className="text-purple-400">{lastDebug.emocion ?? '—'}</span>
                    </div>
                    <div>
                      <span className="text-zinc-500">INTENSIDAD </span>
                      <span className="text-purple-300">{lastDebug.emocion_intensidad?.toFixed(2) ?? '—'}</span>
                    </div>
                    <div>
                      <span className="text-zinc-500">EFECTO </span>
                      <span className={
                        lastDebug.efecto_jugador === 'ayuda' ? 'text-green-400' :
                        lastDebug.efecto_jugador === 'obstaculiza' ? 'text-red-400' :
                        'text-zinc-400'
                      }>{lastDebug.efecto_jugador ?? '—'}</span>
                    </div>
                  </div>
                )}

                <div className="flex gap-2">
                  <input 
                    type="text" 
                    value={mensaje}
                    onChange={(e) => setMensaje(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && enviarMensaje()}
                    placeholder="Escribe algo al NPC..."
                    className="flex-1 bg-zinc-900 border border-zinc-700 p-2 text-sm focus:outline-none focus:border-amber-500"
                  />
                  <button 
                    onClick={enviarMensaje}
                    className="bg-amber-600 hover:bg-amber-500 text-black px-4 py-2 text-sm font-bold"
                  >
                    ENVIAR
                  </button>
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-zinc-600 italic">
                Selecciona un NPC para iniciar el test de LLM
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
