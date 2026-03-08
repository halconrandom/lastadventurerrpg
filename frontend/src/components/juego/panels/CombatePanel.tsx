"use client";

import { motion } from "framer-motion";
import { Swords } from "lucide-react";
import { Card } from "@/components/ui/Card";

export function CombatePanel() {
  return (
    <motion.div
      key="combate"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
    >
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
    </motion.div>
  );
}
