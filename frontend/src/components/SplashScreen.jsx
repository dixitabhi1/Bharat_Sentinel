import React, { useEffect, useState } from "react";
import { Shield, Radio, Activity } from "lucide-react";

export default function SplashScreen({ onDone }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(onDone, 300);
          return 100;
        }
        return prev + 15;
      });
    }, 70);
    return () => clearInterval(interval);
  }, [onDone]);

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 9999, background: "#030712", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "1rem" }}>
        <Shield size={36} color="#38BDF8" />
        <h1 style={{ fontFamily: "var(--font-display)", fontSize: "2rem", color: "#FFFFFF", letterSpacing: "2px", margin: 0 }}>
          BHARAT SENTINEL
        </h1>
      </div>
      <div style={{ fontSize: "0.8rem", color: "#94A3B8", fontFamily: "var(--font-mono)", marginBottom: "1.5rem", letterSpacing: "1px" }}>
        STRATEGIC SITUATIONAL INTELLIGENCE PLATFORM
      </div>
      <div style={{ width: "280px", height: "4px", background: "#1F2937", borderRadius: "2px", overflow: "hidden" }}>
        <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, #38BDF8, #818CF8)", transition: "width 0.1s ease" }} />
      </div>
      <div style={{ marginTop: "8px", fontSize: "0.7rem", fontFamily: "var(--font-mono)", color: "#38BDF8" }}>
        INITIALIZING SENSOR MESH... {progress}%
      </div>
    </div>
  );
}