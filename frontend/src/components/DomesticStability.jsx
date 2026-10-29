import React from "react";
import { ShieldCheck, AlertTriangle, Activity, MapPin, Zap } from "lucide-react";

export default function DomesticStability() {
  const sectors = [
    { name: "Northern Command (J&K / Ladakh)", status: "Heightened Alert", score: 88, color: "#F59E0B", incidents: 3 },
    { name: "Eastern Command (Arunachal / LAC)", status: "Active Surveillance", score: 92, color: "#34D399", incidents: 1 },
    { name: "Western Command (Punjab / Rajasthan)", status: "Stable", score: 96, color: "#34D399", incidents: 0 },
    { name: "Southern Chokepoints (IOR / Andaman)", status: "Maritime Vigilance", score: 90, color: "#38BDF8", incidents: 2 }
  ];

  return (
    <div style={{ background: "#0D1322", borderRadius: "8px", border: "1px solid var(--border-subtle)", padding: "1.2rem", height: "100%", color: "#FFFFFF", overflowY: "auto" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1.2rem" }}>
        <div>
          <h2 style={{ fontFamily: "var(--font-display)", fontSize: "1.2rem", margin: 0, color: "#FFFFFF" }}>
            DOMESTIC STABILITY & THEATER STATUS MATRIX
          </h2>
          <div style={{ fontSize: "0.75rem", color: "#94A3B8", marginTop: "2px" }}>
            Live Composite Threat Index across National Strategic Commands
          </div>
        </div>
        <div style={{ background: "rgba(16, 185, 129, 0.15)", border: "1px solid #10B981", borderRadius: "4px", padding: "4px 10px", fontSize: "0.75rem", fontFamily: "var(--font-mono)", color: "#34D399", fontWeight: 700 }}>
          OVERALL INDEX: 91.5 / 100 (HIGH STABILITY)
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "10px", marginBottom: "1.5rem" }}>
        {sectors.map((s, idx) => (
          <div key={idx} style={{ background: "rgba(17, 24, 39, 0.8)", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "6px", padding: "1rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
              <span style={{ fontFamily: "var(--font-heading)", fontWeight: 700, fontSize: "0.85rem", color: "#FFFFFF" }}>{s.name}</span>
              <span style={{ fontSize: "0.7rem", fontFamily: "var(--font-mono)", color: s.color, fontWeight: 700 }}>{s.status}</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "0.75rem", color: "#94A3B8" }}>
              <span>Stability Score: <strong style={{ color: "#FFFFFF" }}>{s.score}%</strong></span>
              <span>Active Vectors: <strong style={{ color: s.color }}>{s.incidents}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}