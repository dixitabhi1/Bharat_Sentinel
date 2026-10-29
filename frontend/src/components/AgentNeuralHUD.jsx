import React, { useEffect, useState } from "react";
import { 
  Cpu, 
  Code, 
  ShieldCheck, 
  Terminal, 
  Eye, 
  CheckCircle2, 
  Layers, 
  Sparkles,
  Plane,
  Ship,
  FileText,
  UserCheck,
  Zap
} from "lucide-react";

export default function AgentNeuralHUD() {
  const [skills, setSkills] = useState({});
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/skills")
      .then(res => res.json())
      .then(data => {
        setSkills(data);
        const keys = Object.keys(data);
        if (keys.length > 0) {
          setSelectedSkill(data[keys[0]]);
        }
      })
      .catch(err => console.error("Error fetching skills:", err))
      .finally(() => setLoading(false));
  }, []);

  const getAgentIcon = (name) => {
    if (name.includes("flight")) return <Plane size={20} color="#22D3EE" />;
    if (name.includes("naval")) return <Ship size={20} color="#34D399" />;
    if (name.includes("troop")) return <Layers size={20} color="#F87171" />;
    if (name.includes("leader")) return <UserCheck size={20} color="#FBBF24" />;
    if (name.includes("classifier")) return <Zap size={20} color="#A855F7" />;
    if (name.includes("chatbot")) return <Terminal size={20} color="#38BDF8" />;
    return <Cpu size={20} color="#22D3EE" />;
  };

  return (
    <div style={{ display: "flex", gap: "1.25rem", height: "100%", overflow: "hidden", padding: "0.5rem" }}>
      {/* Left List of Specialist Skills */}
      <div
        className="hud-panel"
        style={{
          width: "360px",
          display: "flex",
          flexDirection: "column",
          borderRadius: "8px",
          overflow: "hidden"
        }}
      >
        <div style={{ padding: "0.85rem 1rem", borderBottom: "1px solid var(--border-subtle)", background: "rgba(11, 19, 43, 0.9)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Cpu size={16} color="var(--accent-cyan)" />
            <span style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "0.9rem", color: "#FFFFFF", letterSpacing: "1px" }}>
              SPECIALIST AGENT SKILLS ({Object.keys(skills).length})
            </span>
          </div>
          <div style={{ fontSize: "0.68rem", color: "var(--text-muted)", marginTop: "2px" }}>
            Autonomous Multi-Agent Prompt Rubrics (.agents/skills/*)
          </div>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "0.6rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {Object.values(skills).map((skill) => {
            const isSelected = selectedSkill?.name === skill.name;
            return (
              <div
                key={skill.name}
                onClick={() => setSelectedSkill(skill)}
                style={{
                  background: isSelected ? "rgba(34, 211, 238, 0.12)" : "rgba(13, 24, 46, 0.6)",
                  border: isSelected ? "1px solid var(--accent-cyan)" : "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  padding: "0.75rem",
                  cursor: "pointer",
                  transition: "all 0.2s ease"
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                  {getAgentIcon(skill.name)}
                  <span style={{ fontFamily: "var(--font-heading)", fontWeight: 700, fontSize: "0.85rem", color: isSelected ? "#FFFFFF" : "#CBD5E1" }}>
                    {skill.name}
                  </span>
                </div>
                <div style={{ fontSize: "0.72rem", color: "var(--text-secondary)", lineHeight: 1.35 }}>
                  {skill.description?.length > 90 ? skill.description.slice(0, 90) + "..." : skill.description}
                </div>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "6px", fontSize: "0.65rem", fontFamily: "var(--font-mono)", color: "var(--accent-cyan)" }}>
                  <span>STATUS: RUNTIME ACTIVE</span>
                  <CheckCircle2 size={12} color="#10B981" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Right: Skill Inspector & Prompt Engine */}
      <div
        className="hud-panel hud-corners"
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          borderRadius: "8px",
          overflow: "hidden"
        }}
      >
        {selectedSkill ? (
          <>
            <div style={{ padding: "1rem 1.25rem", borderBottom: "1px solid var(--border-subtle)", background: "rgba(11, 19, 43, 0.95)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  {getAgentIcon(selectedSkill.name)}
                  <span style={{ fontFamily: "var(--font-display)", fontWeight: 800, fontSize: "1.1rem", color: "#FFFFFF" }}>
                    {selectedSkill.name}
                  </span>
                </div>
                <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", fontFamily: "var(--font-mono)", marginTop: "3px" }}>
                  SPECIFICATION: {selectedSkill.file_path}
                </div>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "6px", background: "rgba(34, 211, 238, 0.1)", border: "1px solid var(--accent-cyan)", padding: "4px 10px", borderRadius: "4px", fontSize: "0.72rem", color: "var(--accent-cyan)", fontFamily: "var(--font-mono)" }}>
                <Terminal size={13} />
                <span>DYNAMIC REASONING PROMPT</span>
              </div>
            </div>

            <div style={{ flex: 1, overflowY: "auto", padding: "1.25rem" }}>
              <div style={{ marginBottom: "1rem", padding: "10px", background: "rgba(3, 7, 18, 0.6)", border: "1px solid var(--border-subtle)", borderRadius: "6px" }}>
                <span style={{ fontSize: "0.72rem", fontFamily: "var(--font-heading)", color: "var(--accent-cyan)", fontWeight: 700 }}>
                  AGENT SCOPE & DESCRIPTION:
                </span>
                <div style={{ fontSize: "0.82rem", color: "#E2E8F0", marginTop: "4px", lineHeight: 1.45 }}>
                  {selectedSkill.description}
                </div>
              </div>

              <div>
                <span style={{ fontSize: "0.72rem", fontFamily: "var(--font-heading)", color: "var(--accent-cyan)", fontWeight: 700 }}>
                  SYSTEM INSTRUCTIONS / PROMPT BODY (SKILL.MD):
                </span>
                <pre
                  style={{
                    marginTop: "6px",
                    background: "#030712",
                    border: "1px solid var(--border-subtle)",
                    borderRadius: "6px",
                    padding: "1rem",
                    fontSize: "0.78rem",
                    fontFamily: "var(--font-mono)",
                    color: "#A5B4FC",
                    whiteSpace: "pre-wrap",
                    lineHeight: 1.5,
                    maxHeight: "450px",
                    overflowY: "auto"
                  }}
                >
                  {selectedSkill.system_prompt}
                </pre>
              </div>
            </div>
          </>
        ) : (
          <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
            Select a specialist agent skill from the list to inspect its prompt.
          </div>
        )}
      </div>
    </div>
  );
}
