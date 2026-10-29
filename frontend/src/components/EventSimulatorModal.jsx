import React, { useState } from "react";
import { Zap, X, AlertTriangle } from "lucide-react";

export default function EventSimulatorModal({ isOpen, onClose, onEventSimulated }) {
  const [eventType, setEventType] = useState("airspace_violation");
  const [title, setTitle] = useState("Simulated Radar Track: Unidentified Fast Jet Crossing LAC");
  const [severity, setSeverity] = useState(3);

  if (!isOpen) return null;

  const handleSimulate = () => {
    if (onEventSimulated) {
      onEventSimulated({
        id: "sim-" + Date.now(),
        title,
        category: eventType,
        severity,
        location: { lat: 34.2, lon: 78.5 },
        summary: title + " detected near Eastern Ladakh sector. Automated tracking engaged.",
        is_india_relevant: true,
        created_at: new Date().toISOString()
      });
    }
    onClose();
  };

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 1000, background: "rgba(0,0,0,0.75)", backdropFilter: "blur(6px)", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: "480px", background: "#0D1322", border: "1px solid var(--accent-cyan)", borderRadius: "8px", padding: "1.2rem", color: "#FFFFFF" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--accent-cyan)", fontWeight: 700 }}>
            <Zap size={18} />
            <span>MULTI-AGENT EVENT SIMULATOR</span>
          </div>
          <button onClick={onClose} style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer" }}>
            <X size={18} />
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "1.2rem" }}>
          <div>
            <label style={{ fontSize: "0.72rem", color: "#94A3B8", display: "block", marginBottom: "4px" }}>INCIDENT TITLE</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} style={{ width: "100%", padding: "6px 8px", background: "#111827", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "4px", color: "#FFFFFF", fontSize: "0.8rem" }} />
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
            <div>
              <label style={{ fontSize: "0.72rem", color: "#94A3B8", display: "block", marginBottom: "4px" }}>CATEGORY</label>
              <select value={eventType} onChange={(e) => setEventType(e.target.value)} style={{ width: "100%", padding: "6px 8px", background: "#111827", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "4px", color: "#FFFFFF", fontSize: "0.8rem" }}>
                <option value="airspace_violation">Airspace Incursion</option>
                <option value="naval_intercept">Naval Intercept</option>
                <option value="border_movement">Troop Movement</option>
                <option value="cyber_telemetry">Radar Signal</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: "0.72rem", color: "#94A3B8", display: "block", marginBottom: "4px" }}>SEVERITY LEVEL</label>
              <select value={severity} onChange={(e) => setSeverity(Number(e.target.value))} style={{ width: "100%", padding: "6px 8px", background: "#111827", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "4px", color: "#FFFFFF", fontSize: "0.8rem" }}>
                <option value={1}>Severity 1 (Advisory)</option>
                <option value={2}>Severity 2 (Elevated)</option>
                <option value={3}>Severity 3 (Critical Alert)</option>
                <option value={4}>Severity 4 (Direct Confrontation)</option>
              </select>
            </div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px" }}>
          <button onClick={onClose} style={{ padding: "6px 12px", background: "transparent", border: "1px solid rgba(255,255,255,0.15)", borderRadius: "4px", color: "#94A3B8", cursor: "pointer" }}>Cancel</button>
          <button onClick={handleSimulate} style={{ padding: "6px 14px", background: "linear-gradient(135deg, #0284c7, #0369a1)", border: "1px solid #38bdf8", borderRadius: "4px", color: "#FFFFFF", fontWeight: 700, cursor: "pointer" }}>Inject Simulation</button>
        </div>
      </div>
    </div>
  );
}