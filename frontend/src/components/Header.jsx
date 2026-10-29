import React, { useState, useEffect, useRef } from "react";
import { 
  Shield, 
  Search, 
  Maximize, 
  Minimize, 
  Radio, 
  Bot, 
  PlusCircle, 
  AlertTriangle, 
  Clock, 
  Globe2, 
  Activity, 
  Cpu, 
  Users,
  ChevronDown
} from "lucide-react";

export default function Header({ 
  activeTab, 
  setActiveTab, 
  stats, 
  timeframe = "6h", 
  setTimeframe = () => {},
  searchQuery = "",
  setSearchQuery = () => {},
  scope = "global",
  setScope = () => {},
  newsTicker = [],
  onOpenReviewModal = () => {}, 
  onOpenSimulatorModal = () => {} 
}) {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const searchInputRef = useRef(null);

  const pendingReviewCount = stats?.pending_review_count || 0;
  const totalTracked = stats?.total_tracked || 507;
  const eventsInWindow = stats?.events_in_6h || 57;

  // Fullscreen toggle handler
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
        setIsFullscreen(false);
      }
    }
  };

  // Keyboard shortcut '/' to focus search
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "/" && document.activeElement !== searchInputRef.current) {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const timeOptions = [
    { label: "6H", value: "6h" },
    { label: "12H", value: "12h" },
    { label: "24H", value: "24h" },
    { label: "7D", value: "7d" },
    { label: "ALL", value: "all" }
  ];

  return (
    <header
      style={{
        background: "rgba(6, 11, 22, 0.96)",
        backdropFilter: "blur(16px)",
        borderBottom: "1px solid var(--border-subtle)",
        display: "flex",
        flexDirection: "column",
        position: "sticky",
        top: 0,
        zIndex: 1000,
        width: "100%"
      }}
    >
      {/* Top Main Navigation Bar */}
      <div
        style={{
          padding: "0.55rem 1.25rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "0.85rem",
          flexWrap: "nowrap"
        }}
      >
        {/* Left: Branding & Fullscreen */}
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flexShrink: 0 }}>
          <button
            onClick={toggleFullscreen}
            title="Toggle Fullscreen"
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.15)",
              borderRadius: "4px",
              color: "#CBD5E1",
              padding: "5px",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}
          >
            {isFullscreen ? <Minimize size={14} /> : <Maximize size={14} />}
          </button>

          {/* Logo & Title */}
          <div 
            onClick={() => setActiveTab("map")}
            style={{ display: "flex", alignItems: "center", gap: "0.5rem", cursor: "pointer" }}
          >
            <div
              style={{
                width: "28px",
                height: "28px",
                borderRadius: "6px",
                background: "linear-gradient(135deg, rgba(34, 211, 238, 0.25), rgba(59, 130, 246, 0.2))",
                border: "1px solid var(--accent-cyan)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 0 10px rgba(34, 211, 238, 0.3)"
              }}
            >
              <Shield size={16} color="#22D3EE" />
            </div>
            <div>
              <div 
                style={{ 
                  fontFamily: "var(--font-display)", 
                  fontWeight: 900, 
                  fontSize: "1.05rem", 
                  letterSpacing: "1px", 
                  color: "#FFFFFF",
                  lineHeight: 1.1
                }}
              >
                Bharat Sentinel
              </div>
              <div 
                style={{ 
                  fontSize: "0.62rem", 
                  color: "var(--text-muted)", 
                  letterSpacing: "0.8px",
                  textTransform: "uppercase",
                  fontFamily: "var(--font-mono)"
                }}
              >
                Global & Regional Situation Room
              </div>
            </div>
          </div>
        </div>

        {/* Global vs India Specific Focus Switcher */}
        <div
          style={{
            display: "flex",
            background: "rgba(3, 7, 18, 0.85)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "6px",
            padding: "2px",
            flexShrink: 0
          }}
        >
          <button
            onClick={() => setScope("global")}
            style={{
              padding: "4px 10px",
              fontSize: "0.72rem",
              fontFamily: "var(--font-heading)",
              fontWeight: 700,
              borderRadius: "4px",
              border: "none",
              cursor: "pointer",
              background: scope === "global" ? "linear-gradient(135deg, #0284c7, #0369a1)" : "transparent",
              color: scope === "global" ? "#FFFFFF" : "#94A3B8",
              transition: "all 0.2s ease"
            }}
          >
            🌍 GLOBAL
          </button>
          <button
            onClick={() => setScope("india")}
            style={{
              padding: "4px 10px",
              fontSize: "0.72rem",
              fontFamily: "var(--font-heading)",
              fontWeight: 700,
              borderRadius: "4px",
              border: "none",
              cursor: "pointer",
              background: scope === "india" ? "linear-gradient(135deg, #f59e0b, #d97706)" : "transparent",
              color: scope === "india" ? "#FFFFFF" : "#94A3B8",
              transition: "all 0.2s ease"
            }}
          >
            🇮🇳 INDIA FOCUS
          </button>
        </div>

        {/* Search Bar matching Monitor-the-Situation */}
        <div
          style={{
            position: "relative",
            minWidth: "200px",
            maxWidth: "280px",
            flex: 1
          }}
        >
          <Search 
            size={14} 
            color="var(--text-muted)" 
            style={{ position: "absolute", left: "10px", top: "50%", transform: "translateY(-50%)" }} 
          />
          <input
            ref={searchInputRef}
            type="text"
            placeholder="Search events [/]"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: "100%",
              background: "rgba(3, 7, 18, 0.75)",
              border: "1px solid var(--border-subtle)",
              borderRadius: "4px",
              padding: "6px 28px 6px 30px",
              color: "#FFFFFF",
              fontSize: "0.78rem",
              fontFamily: "var(--font-body)",
              outline: "none"
            }}
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              style={{
                position: "absolute",
                right: "8px",
                top: "50%",
                transform: "translateY(-50%)",
                background: "transparent",
                border: "none",
                color: "var(--text-muted)",
                cursor: "pointer",
                fontSize: "0.75rem"
              }}
            >
              ✕
            </button>
          )}
        </div>

        {/* Timeframe Filter Buttons (6H, 12H, 24H, 7D, ALL) */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            background: "rgba(3, 7, 18, 0.8)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "4px",
            padding: "2px",
            gap: "2px",
            flexShrink: 0
          }}
        >
          {timeOptions.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setTimeframe(opt.value)}
              style={{
                padding: "3px 8px",
                fontSize: "0.72rem",
                fontFamily: "var(--font-mono)",
                fontWeight: 700,
                borderRadius: "3px",
                border: "none",
                cursor: "pointer",
                background: timeframe === opt.value ? "rgba(34, 211, 238, 0.25)" : "transparent",
                color: timeframe === opt.value ? "var(--accent-cyan)" : "var(--text-muted)",
                transition: "all 0.15s ease"
              }}
            >
              {opt.label}
            </button>
          ))}
        </div>

        {/* Live Counters & Viewer Stats */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            fontSize: "0.74rem",
            fontFamily: "var(--font-mono)",
            flexShrink: 0
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: "#10B981",
                boxShadow: "0 0 8px #10B981",
                display: "inline-block",
                animation: "pulse-glow 1.5s infinite"
              }}
            />
            <span style={{ color: "#34D399", fontWeight: 700 }}>Live</span>
          </div>

          <span style={{ color: "var(--text-muted)" }}>•</span>
          <span style={{ color: "#E2E8F0" }}>{totalTracked} tracked</span>
          <span style={{ color: "var(--text-muted)" }}>•</span>
          <span style={{ color: "var(--text-muted)" }}>{eventsInWindow} in {timeframe.toUpperCase()}</span>
          <span style={{ color: "var(--text-muted)" }}>•</span>
          <span style={{ color: "var(--text-muted)" }}>Updated 4m ago</span>

          <div style={{ display: "flex", alignItems: "center", gap: "4px", color: "var(--text-muted)" }}>
            <Users size={12} />
            <span>1.3k / 2.5k</span>
          </div>
        </div>

        {/* Action Buttons: Chat, Stability, Specialist Agents, Simulate, Review Gate */}
        <div style={{ display: "flex", alignItems: "center", gap: "6px", flexShrink: 0 }}>
          <button
            onClick={() => setActiveTab(activeTab === "chat" ? "map" : "chat")}
            className="btn-cyber"
            style={{
              padding: "5px 10px",
              fontSize: "0.74rem",
              background: activeTab === "chat" ? "rgba(34, 211, 238, 0.25)" : undefined,
              borderColor: activeTab === "chat" ? "var(--accent-cyan)" : undefined
            }}
            title="Ask Bharat Sentinel RAG Chatbot"
          >
            <Bot size={13} />
            <span>Chat</span>
          </button>

          <button
            onClick={() => setActiveTab(activeTab === "stability" ? "map" : "stability")}
            className="btn-cyber"
            style={{
              padding: "5px 10px",
              fontSize: "0.74rem",
              background: activeTab === "stability" ? "rgba(16, 185, 129, 0.25)" : undefined,
              borderColor: activeTab === "stability" ? "var(--accent-emerald)" : undefined
            }}
            title="Domestic Stability & Resilience Index"
          >
            <Activity size={13} color="#10B981" />
            <span>Stability</span>
          </button>

          <button
            onClick={() => setActiveTab(activeTab === "agents" ? "map" : "agents")}
            className="btn-cyber"
            style={{
              padding: "5px 10px",
              fontSize: "0.74rem",
              background: activeTab === "agents" ? "rgba(168, 85, 247, 0.25)" : undefined,
              borderColor: activeTab === "agents" ? "var(--accent-violet)" : undefined
            }}
            title="Specialist Agent Skills & Prompt Rubrics"
          >
            <Cpu size={13} color="#A855F7" />
            <span>Agents</span>
          </button>

          <button
            onClick={onOpenSimulatorModal}
            className="btn-cyber"
            style={{ padding: "5px 10px", fontSize: "0.74rem" }}
            title="Inject Event into Multi-Agent Pipeline"
          >
            <PlusCircle size={13} />
            <span>Simulate</span>
          </button>

          {/* Review Gatekeeper Modal Trigger */}
          <button
            onClick={onOpenReviewModal}
            className={pendingReviewCount > 0 ? "btn-cyber btn-cyber-danger" : "btn-cyber"}
            style={{ padding: "5px 10px", fontSize: "0.74rem" }}
            title="Human Review Gate for Tier 4 Signals"
          >
            <AlertTriangle size={13} />
            <span>Review Gate</span>
            {pendingReviewCount > 0 && (
              <span
                style={{
                  background: "#EF4444",
                  color: "#FFFFFF",
                  borderRadius: "50%",
                  padding: "1px 5px",
                  fontSize: "0.65rem",
                  fontWeight: 700
                }}
              >
                {pendingReviewCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Marquee Breaking News Ticker Track */}
      {newsTicker.length > 0 && (
        <div
          style={{
            background: "rgba(3, 7, 18, 0.9)",
            borderTop: "1px solid rgba(255, 255, 255, 0.06)",
            padding: "4px 1.25rem",
            display: "flex",
            alignItems: "center",
            overflow: "hidden",
            fontSize: "0.72rem",
            fontFamily: "var(--font-body)"
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              paddingRight: "12px",
              borderRight: "1px solid rgba(255, 255, 255, 0.1)",
              flexShrink: 0,
              color: "#F59E0B",
              fontWeight: 800,
              fontFamily: "var(--font-mono)",
              fontSize: "0.68rem"
            }}
          >
            <Radio size={12} color="#F59E0B" className="pulse-beacon" />
            <span>BREAKING DISPATCH:</span>
          </div>

          <div style={{ flex: 1, overflow: "hidden", position: "relative", whiteSpace: "nowrap" }}>
            <div className="ticker-track">
              {newsTicker.map((item, idx) => (
                <span
                  key={idx}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "6px",
                    marginRight: "2.5rem",
                    color: "#CBD5E1"
                  }}
                >
                  <span className={`cat-pill cat-${item.category || 'political'}`}>
                    {(item.category || 'NEWS').toUpperCase()}
                  </span>
                  <span className={`sev-badge sev-s${item.severity || 1}`}>
                    S{item.severity || 1}
                  </span>
                  <span style={{ color: "#F1F5F9" }}>{item.title}</span>
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
