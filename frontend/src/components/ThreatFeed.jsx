import React, { useState } from "react";
import { 
  MapPin, 
  Clock, 
  ExternalLink, 
  Bot, 
  Filter, 
  ChevronLeft, 
  ChevronRight, 
  Radio, 
  Flame, 
  ShieldAlert, 
  AlertCircle,
  FileText
} from "lucide-react";

export default function ThreatFeed({ 
  events = [], 
  selectedItem = null, 
  onSelectItem = () => {}, 
  onAskChatbot = () => {},
  isCollapsed = false,
  setIsCollapsed = () => {}
}) {
  const [activeSubTab, setActiveSubTab] = useState("FEED"); // FEED, LIVE, REPORTS
  const [selectedCategory, setSelectedCategory] = useState("all");

  const categories = [
    { id: "all", label: "All" },
    { id: "political", label: "Political" },
    { id: "military", label: "Military" },
    { id: "maritime", label: "Maritime" },
    { id: "disaster", label: "Disaster" },
    { id: "trade", label: "Trade" },
    { id: "airspace", label: "Airspace" }
  ];

  // Helper to format relative time
  const getRelativeTime = (isoString) => {
    if (!isoString) return "just now";
    try {
      const diffMs = Date.now() - new Date(isoString).getTime();
      const diffSec = Math.max(0, Math.floor(diffMs / 1000));
      if (diffSec < 60) return `${diffSec}s ago`;
      const diffMin = Math.floor(diffSec / 60);
      if (diffMin < 60) return `${diffMin}m ago`;
      const diffHrs = Math.floor(diffMin / 60);
      if (diffHrs < 24) return `${diffHrs}h ago`;
      const diffDays = Math.floor(diffHrs / 24);
      return `${diffDays}d ago`;
    } catch {
      return "recently";
    }
  };

  const filteredEvents = events.filter((ev) => {
    if (selectedCategory !== "all" && (ev.category || "").toLowerCase() !== selectedCategory.toLowerCase()) {
      return false;
    }
    return true;
  });

  if (isCollapsed) {
    return (
      <div
        style={{
          width: "42px",
          height: "100%",
          background: "var(--bg-drawer)",
          borderRight: "1px solid var(--border-subtle)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "1rem 0",
          gap: "1rem",
          zIndex: 400
        }}
      >
        <button
          onClick={() => setIsCollapsed(false)}
          title="Expand Intelligence Feed"
          style={{
            background: "rgba(34, 211, 238, 0.1)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "4px",
            color: "var(--accent-cyan)",
            cursor: "pointer",
            padding: "6px"
          }}
        >
          <ChevronRight size={16} />
        </button>
        <div
          style={{
            writingMode: "vertical-rl",
            transform: "rotate(180deg)",
            color: "var(--text-secondary)",
            fontFamily: "var(--font-heading)",
            fontSize: "0.85rem",
            letterSpacing: "2px",
            fontWeight: 700
          }}
        >
          INTELLIGENCE FEED ({events.length})
        </div>
      </div>
    );
  }

  return (
    <aside
      style={{
        width: "360px",
        height: "100%",
        background: "var(--bg-drawer)",
        borderRight: "1px solid var(--border-subtle)",
        display: "flex",
        flexDirection: "column",
        zIndex: 400,
        boxShadow: "4px 0 24px rgba(0, 0, 0, 0.6)"
      }}
    >
      {/* Drawer Header with FEED | LIVE | REPORTS tabs matching screenshot 3 */}
      <div
        style={{
          padding: "0.75rem 1rem",
          background: "rgba(11, 19, 43, 0.95)",
          borderBottom: "1px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between"
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          {["FEED", "LIVE", "REPORTS"].map((tab) => {
            const isTabActive = activeSubTab === tab;
            return (
              <button
                key={tab}
                onClick={() => setActiveSubTab(tab)}
                style={{
                  background: isTabActive ? "rgba(34, 211, 238, 0.18)" : "transparent",
                  border: isTabActive ? "1px solid var(--accent-cyan)" : "1px solid transparent",
                  borderRadius: "4px",
                  color: isTabActive ? "#FFFFFF" : "var(--text-secondary)",
                  fontFamily: "var(--font-heading)",
                  fontWeight: 700,
                  fontSize: "0.75rem",
                  padding: "4px 10px",
                  cursor: "pointer",
                  letterSpacing: "0.5px"
                }}
              >
                {tab}
              </button>
            );
          })}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span
            style={{
              fontSize: "0.7rem",
              fontFamily: "var(--font-mono)",
              color: "var(--accent-cyan)",
              background: "rgba(34, 211, 238, 0.1)",
              padding: "2px 7px",
              borderRadius: "4px",
              border: "1px solid rgba(34, 211, 238, 0.25)"
            }}
          >
            {filteredEvents.length} events
          </span>
          <button
            onClick={() => setIsCollapsed(true)}
            title="Collapse Sidebar"
            style={{
              background: "transparent",
              border: "none",
              color: "var(--text-muted)",
              cursor: "pointer",
              padding: "2px",
              display: "flex"
            }}
          >
            <ChevronLeft size={18} />
          </button>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div
        style={{
          padding: "6px 0.75rem",
          background: "rgba(3, 7, 18, 0.6)",
          borderBottom: "1px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          gap: "4px",
          overflowX: "auto",
          whiteSpace: "nowrap"
        }}
      >
        {categories.map((cat) => {
          const isCatActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              style={{
                background: isCatActive ? "rgba(34, 211, 238, 0.15)" : "rgba(15, 23, 42, 0.5)",
                border: isCatActive ? "1px solid var(--accent-cyan)" : "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "3px",
                color: isCatActive ? "#FFFFFF" : "var(--text-secondary)",
                fontSize: "0.68rem",
                fontFamily: "var(--font-heading)",
                fontWeight: 600,
                padding: "2px 8px",
                cursor: "pointer"
              }}
            >
              {cat.label}
            </button>
          );
        })}
      </div>

      {/* Events List */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "0.6rem",
          display: "flex",
          flexDirection: "column",
          gap: "0.6rem"
        }}
      >
        {filteredEvents.length === 0 ? (
          <div style={{ padding: "2.5rem 1rem", textAlign: "center", color: "var(--text-muted)", fontSize: "0.82rem" }}>
            No signals matched the active filter criteria.
          </div>
        ) : (
          filteredEvents.map((ev) => {
            const isSelected = selectedItem?.id === ev.id;
            const category = ev.category || "political";
            const severity = ev.severity_global || 1;
            const relTime = getRelativeTime(ev.created_at);

            return (
              <div
                key={ev.id}
                onClick={() => onSelectItem(ev)}
                style={{
                  background: isSelected ? "rgba(34, 211, 238, 0.12)" : "rgba(13, 24, 46, 0.65)",
                  border: isSelected ? "1px solid var(--accent-cyan)" : "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  padding: "0.75rem",
                  cursor: "pointer",
                  transition: "all 0.18s ease",
                  boxShadow: isSelected ? "var(--shadow-neon-cyan)" : "none"
                }}
              >
                {/* Card Header: Category + Severity Badge + Timestamp */}
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "6px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <span className={`cat-badge cat-${category}`}>
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </span>
                    <span className={`sev-badge sev-s${severity}`}>
                      S{severity}
                    </span>
                  </div>

                  <span style={{ fontSize: "0.68rem", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
                    {relTime}
                  </span>
                </div>

                {/* Event Title */}
                <div
                  style={{
                    fontSize: "0.84rem",
                    fontWeight: 700,
                    color: isSelected ? "#FFFFFF" : "#E2E8F0",
                    lineHeight: 1.35,
                    marginBottom: "6px"
                  }}
                >
                  {ev.title}
                </div>

                {/* Event Summary */}
                <div
                  style={{
                    fontSize: "0.74rem",
                    color: "var(--text-secondary)",
                    lineHeight: 1.4,
                    marginBottom: "8px",
                    display: "-webkit-box",
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: "vertical",
                    overflow: "hidden"
                  }}
                >
                  {ev.summary}
                </div>

                {/* Card Footer: Location Tag & Action */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    fontSize: "0.68rem",
                    color: "var(--text-muted)",
                    borderTop: "1px solid rgba(255, 255, 255, 0.05)",
                    paddingTop: "6px",
                    marginTop: "4px"
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "4px", color: "var(--text-secondary)" }}>
                    <MapPin size={12} color="var(--accent-cyan)" />
                    <span>{ev.location?.name || `${ev.location?.lat}°N, ${ev.location?.lon}°E`}</span>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onAskChatbot(ev);
                    }}
                    title="Deep Dive with RAG Intelligence Engine"
                    style={{
                      background: "rgba(34, 211, 238, 0.1)",
                      border: "1px solid rgba(34, 211, 238, 0.25)",
                      borderRadius: "3px",
                      color: "var(--accent-cyan)",
                      fontSize: "0.65rem",
                      padding: "2px 6px",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "3px"
                    }}
                  >
                    <Bot size={11} />
                    <span>Ask AI</span>
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}
