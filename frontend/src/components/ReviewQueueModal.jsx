import React from "react";
import { CheckCircle2, XCircle, X, ShieldAlert } from "lucide-react";

export default function ReviewQueueModal({ isOpen, onClose, reviewQueue = [], onApprove, onReject }) {
  if (!isOpen) return null;

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 1000, background: "rgba(0,0,0,0.75)", backdropFilter: "blur(6px)", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: "550px", maxHeight: "80vh", background: "#0D1322", border: "1px solid rgba(245, 158, 11, 0.4)", borderRadius: "8px", display: "flex", flexDirection: "column", color: "#FFFFFF" }}>
        <div style={{ padding: "1rem", borderBottom: "1px solid rgba(255,255,255,0.08)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#F59E0B", fontWeight: 700 }}>
            <ShieldAlert size={18} />
            <span>ANALYST HUMAN-IN-THE-LOOP REVIEW QUEUE</span>
          </div>
          <button onClick={onClose} style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer" }}>
            <X size={18} />
          </button>
        </div>

        <div style={{ padding: "1rem", overflowY: "auto", flex: 1, display: "flex", flexDirection: "column", gap: "8px" }}>
          {(!reviewQueue || reviewQueue.length === 0) ? (
            <div style={{ textAlign: "center", padding: "2rem", color: "#94A3B8", fontSize: "0.85rem" }}>
              No intelligence items awaiting review. All current telemetry verified.
            </div>
          ) : (
            reviewQueue.map((item, idx) => (
              <div key={idx} style={{ background: "rgba(17, 24, 39, 0.8)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: "6px", padding: "0.8rem" }}>
                <div style={{ fontWeight: 700, fontSize: "0.85rem", marginBottom: "4px" }}>{item.title}</div>
                <div style={{ fontSize: "0.75rem", color: "#94A3B8", marginBottom: "8px" }}>{item.summary}</div>
                <div style={{ display: "flex", gap: "8px", justifyContent: "flex-end" }}>
                  <button onClick={() => onApprove && onApprove(item)} style={{ background: "#10B981", color: "#030712", border: "none", borderRadius: "4px", padding: "4px 10px", fontSize: "0.72rem", fontWeight: 700, cursor: "pointer" }}>
                    Approve Feed
                  </button>
                  <button onClick={() => onReject && onReject(item)} style={{ background: "#EF4444", color: "#FFFFFF", border: "none", borderRadius: "4px", padding: "4px 10px", fontSize: "0.72rem", fontWeight: 700, cursor: "pointer" }}>
                    Discard
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}