import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export default function AnimatedSparkleBadge({
  size = 64,
  className = "",
  sparkleClassName = "h-5 w-5 text-emerald-50",
}) {
  const s = `${size}px`;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.18 }}
      className={`relative inline-flex items-center justify-center rounded-full ${className}`}
      style={{ width: s, height: s }}
    >
      <motion.div
        className="absolute inset-0 flex items-center justify-center rounded-full"
        animate={{
          y: [3, -6, 3],
          scale: [0.98, 1, 0.98],
          x: [0, 1.5, 0],
        }}
        transition={{
          duration: 3.8,
          ease: "easeInOut",
          repeat: Infinity,
        }}
      >
        <motion.div
          className="absolute inset-0 rounded-full"
          style={{
            background:
              "linear-gradient(135deg, #0ea5e9 8%, #3ddc84 38%, #10b981 72%, #06b6d4 100%)",
          }}
          animate={{
            backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
          }}
          transition={{
            duration: 6.5,
            ease: "linear",
            repeat: Infinity,
          }}
        />

        <motion.div
          className="relative z-10 flex items-center justify-center"
          style={{ width: "60%", height: "60%" }}
          animate={{ rotate: [-6, 6, -6] }}
          transition={{
            duration: 3.2,
            ease: "easeInOut",
            repeat: Infinity,
          }}
        >
          <Sparkles className={sparkleClassName} />
        </motion.div>
      </motion.div>

      {/* Glow ring */}
      <motion.span
        className="absolute inset-0 rounded-full pointer-events-none"
        style={{
          boxShadow: "0 6px 30px rgba(16,185,129,0.12)",
          border: "1px solid rgba(255,255,255,0.06)",
        }}
        animate={{ scale: [1, 1.08, 1], opacity: [0.9, 0.6, 0.9] }}
        transition={{ duration: 2.2, ease: "easeInOut", repeat: Infinity }}
      />

      <motion.div
        aria-hidden
        className="absolute rounded-full pointer-events-none"
        style={{
          inset: "-8px",
          filter: "blur(16px)",
          background:
            "radial-gradient(circle at center, rgba(16,185,129,0.18), rgba(16,185,129,0.06) 30%, transparent 60%)",
        }}
        animate={{ opacity: [0.8, 0.45, 0.8] }}
        transition={{ duration: 3.5, ease: "easeInOut", repeat: Infinity }}
      />
    </motion.div>
  );
}
