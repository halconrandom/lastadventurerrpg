"use client";

interface StatBarProps {
  label: string;
  current: number;
  max: number;
  type: "hp" | "mana" | "stamina" | "exp";
  showNumbers?: boolean;
}

export function StatBar({
  label,
  current,
  max,
  type,
  showNumbers = true,
}: StatBarProps) {
  const percentage = Math.min(100, Math.max(0, (current / max) * 100));

  const colors = {
    hp: {
      bg: "bg-gradient-to-b from-[#c44536] to-[#8b2942]",
      text: "text-[#c44536]",
      glow: "shadow-[0_0_10px_rgba(196,69,54,0.3)]",
    },
    mana: {
      bg: "bg-gradient-to-b from-[#3b82f6] to-[#1d4ed8]",
      text: "text-[#3b82f6]",
      glow: "shadow-[0_0_10px_rgba(59,130,246,0.3)]",
    },
    stamina: {
      bg: "bg-gradient-to-b from-[#22c55e] to-[#16a34a]",
      text: "text-[#22c55e]",
      glow: "shadow-[0_0_10px_rgba(34,197,94,0.3)]",
    },
    exp: {
      bg: "bg-gradient-to-b from-[#d4a843] to-[#a67c00]",
      text: "text-[#d4a843]",
      glow: "shadow-[0_0_10px_rgba(212,168,67,0.3)]",
    },
  };

  const color = colors[type];

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-1">
        <span className={`font-medieval text-sm ${color.text}`}>{label}</span>
        {showNumbers && (
          <span className="text-[#9a978a] text-sm">
            {current} / {max}
          </span>
        )}
      </div>
      <div className="h-5 bg-[#0a0a0f] border border-[#2a2a35] rounded overflow-hidden relative">
        <div
          className={`h-full ${color.bg} transition-all duration-300 ${color.glow}`}
          style={{ width: `${percentage}%` }}
        >
          {/* Brillo superior */}
          <div className="absolute inset-0 bg-gradient-to-b from-white/10 to-transparent" />
        </div>
        {/* Texto dentro de la barra */}
        {showNumbers && percentage > 20 && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-white text-xs font-medium drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)]">
              {Math.round(percentage)}%
            </span>
          </div>
        )}
      </div>
    </div>
  );
}