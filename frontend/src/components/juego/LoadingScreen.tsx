"use client";

export function LoadingScreen() {
  return (
    <div className="flex min-h-screen bg-[#0a0a0f] items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-[#d4a843]/20 border-t-[#d4a843] rounded-full animate-spin mx-auto mb-4" />
        <p className="text-[#d4a843] font-medieval text-xl">Cargando Mundo...</p>
      </div>
    </div>
  );
}
