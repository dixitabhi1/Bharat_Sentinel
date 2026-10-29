import React, { useState, useRef, useEffect } from "react";
import { 
  Bot, 
  Send, 
  Sparkles, 
  ShieldCheck, 
  AlertTriangle, 
  ExternalLink, 
  Compass, 
  RefreshCw,
  FileText,
  User,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Radio
} from "lucide-react";

export default function ChatbotConsole({ initialPrompt = "" }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "### Welcome to Ask Bharat Sentinel\n\nI am your **RAG-grounded Geopolitical Intelligence Analyst**. Every assessment I provide is synthesized strictly from our live, multi-source event database (ADS-B aircraft vectors, AIS maritime traffic, official MEA/MoD briefings, and corroborated wire journalism) combined with the strategic geography knowledge base.\n\n*How may I assist your situational awareness today?*",
      citations: [],
      confidence: "high"
    }
  ]);

  // Voice Control States (Browser-Native Web Speech API)
  const [isListening, setIsListening] = useState(false);
  const [voiceSupported, setVoiceSupported] = useState(true);
  const [voiceNotice, setVoiceNotice] = useState("");
  const [isAudioMuted, setIsAudioMuted] = useState(true); // Default OFF
  const recognitionRef = useRef(null);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (initialPrompt) {
      setQuery(initialPrompt);
      handleSend(initialPrompt);
    }
  }, [initialPrompt]);

  // Check browser speech recognition support
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceSupported(false);
      setVoiceNotice("Voice input unavailable in this browser (Web Speech API requires Chromium/Safari)");
    }
  }, []);

  const presetQueries = [
    "What is the current force posture and infrastructure update near the LAC Depsang sector?",
    "Why did the Strait of Hormuz VLCC tanker course deviation matter for India?",
    "Summarize recent official MEA statements regarding Indian Ocean maritime navigation.",
    "What flight anomaly was detected in the Western border corridor?",
    "Test Guardrail: How to evade radar near border air defense?"
  ];

  // Text-To-Speech (TTS) read aloud
  const speakText = (text) => {
    if (isAudioMuted || !window.speechSynthesis) return;
    try {
      window.speechSynthesis.cancel();
      const cleanText = text
        .replace(/[*#_`>]/g, "")
        .replace(/\[.*?\]\(.*?\)/g, "")
        .replace(/https?:\/\/\S+/g, "")
        .slice(0, 450);
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("TTS Error:", e);
    }
  };

  // Start / Stop Browser Voice Speech Recognition
  const toggleVoiceInput = () => {
    if (!voiceSupported) {
      alert("Voice input is unavailable in this browser. Please use a browser supporting Web Speech API (such as Chrome, Edge, or Safari).");
      return;
    }

    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
    } else {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) return;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = "en-IN";
      rec.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        setQuery(transcript);
        handleSend(transcript);
        setIsListening(false);
      };
      rec.onerror = () => setIsListening(false);
      rec.onend = () => setIsListening(false);
      recognitionRef.current = rec;
      rec.start();
      setIsListening(true);
    }
  };

  const handleSend = async (textToSend) => {
    const q = textToSend || query;
    if (!q.trim() || loading) return;

    const userMsg = { role: "user", content: q };
    setMessages((prev) => [...prev, userMsg]);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("/api/chatbot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q })
      });
      if (res.ok) {
        const data = await res.json();
        const botMsg = {
          role: "assistant",
          content: data.answer || "No response received.",
          citations: data.citations || [],
          confidence: data.confidence || "high",
          ethicalGuardrail: data.ethical_guardrail_triggered
        };
        setMessages((prev) => [...prev, botMsg]);
        speakText(botMsg.content);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "Error communicating with intelligence backend." }
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Network error reaching strategic RAG engine." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "#0D1322", borderRadius: "8px", border: "1px solid var(--border-subtle)", overflow: "hidden" }}>
      {/* Header */}
      <div style={{ padding: "0.8rem 1rem", background: "rgba(11, 19, 43, 0.95)", borderBottom: "1px solid rgba(255, 255, 255, 0.08)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <Bot size={18} color="var(--accent-cyan)" />
          <span style={{ fontFamily: "var(--font-heading)", fontWeight: 800, fontSize: "0.95rem", color: "#FFFFFF" }}>
            ASK BHARAT SENTINEL — RAG GEOPOLITICS CONSOLE
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <button
            onClick={() => setIsAudioMuted(!isAudioMuted)}
            style={{ background: isAudioMuted ? "rgba(255,255,255,0.06)" : "rgba(34, 211, 238, 0.2)", border: isAudioMuted ? "1px solid rgba(255,255,255,0.15)" : "1px solid var(--accent-cyan)", borderRadius: "4px", padding: "4px 8px", color: "#FFFFFF", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", fontSize: "0.68rem" }}
            title={isAudioMuted ? "Audio Speech is Muted" : "Audio Speech Output Active"}
          >
            {isAudioMuted ? <VolumeX size={13} color="#94A3B8" /> : <Volume2 size={13} color="var(--accent-cyan)" />}
            <span>{isAudioMuted ? "MUTED" : "VOICE ON"}</span>
          </button>
        </div>
      </div>

      {/* Preset Queries Bar */}
      <div style={{ padding: "6px 10px", background: "#080E1C", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", gap: "6px", overflowX: "auto", scrollbarWidth: "none" }}>
        {presetQueries.map((pq, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(pq)}
            style={{ padding: "3px 8px", background: "rgba(17, 24, 39, 0.8)", border: "1px solid rgba(255, 255, 255, 0.1)", borderRadius: "12px", color: "#CBD5E1", fontSize: "0.65rem", whiteSpace: "nowrap", cursor: "pointer" }}
          >
            {pq.length > 40 ? pq.slice(0, 40) + "..." : pq}
          </button>
        ))}
      </div>

      {/* Messages Feed */}
      <div style={{ flex: 1, overflowY: "auto", padding: "1rem", display: "flex", flexDirection: "column", gap: "12px" }}>
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              flexDirection: "column",
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              maxWidth: "85%",
              background: m.role === "user" ? "linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(29, 78, 216, 0.2))" : "rgba(17, 24, 39, 0.85)",
              border: m.role === "user" ? "1px solid #3B82F6" : (m.ethicalGuardrail ? "1.5px solid #EF4444" : "1px solid rgba(255, 255, 255, 0.08)"),
              borderRadius: "8px",
              padding: "0.8rem 1rem",
              color: "#FFFFFF"
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "4px", fontSize: "0.68rem", fontFamily: "var(--font-mono)", color: m.role === "user" ? "#93C5FD" : "var(--accent-cyan)" }}>
              {m.role === "user" ? <User size={12} /> : <Bot size={12} />}
              <span>{m.role === "user" ? "OPERATOR QUERY" : "BHARAT SENTINEL RAG RESPONSE"}</span>
              {m.confidence && (
                <span style={{ marginLeft: "auto", background: "rgba(16, 185, 129, 0.2)", color: "#34D399", padding: "1px 5px", borderRadius: "3px", fontSize: "0.62rem" }}>
                  {m.confidence.toUpperCase()} CONFIDENCE
                </span>
              )}
            </div>

            <div style={{ fontSize: "0.82rem", lineHeight: 1.5, whiteSpace: "pre-wrap", color: "#F1F5F9" }}>
              {m.content}
            </div>

            {m.citations && m.citations.length > 0 && (
              <div style={{ marginTop: "8px", paddingTop: "6px", borderTop: "1px solid rgba(255,255,255,0.08)", fontSize: "0.65rem", color: "#94A3B8" }}>
                <span style={{ fontWeight: 700, color: "#CBD5E1" }}>Sources Cited: </span>
                {m.citations.join(" • ")}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div style={{ alignSelf: "flex-start", background: "rgba(17, 24, 39, 0.85)", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "8px", padding: "0.6rem 1rem", color: "var(--accent-cyan)", fontSize: "0.75rem", fontFamily: "var(--font-mono)" }}>
            Synthesizing intelligence telemetry & doctrine archives...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div style={{ padding: "0.75rem 1rem", background: "rgba(8, 14, 26, 0.95)", borderTop: "1px solid rgba(255, 255, 255, 0.08)", display: "flex", alignItems: "center", gap: "8px" }}>
        {voiceSupported && (
          <button
            onClick={toggleVoiceInput}
            style={{
              background: isListening ? "#EF4444" : "rgba(255,255,255,0.08)",
              border: isListening ? "1px solid #EF4444" : "1px solid rgba(255,255,255,0.15)",
              borderRadius: "50%",
              width: "36px",
              height: "36px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FFFFFF",
              cursor: "pointer",
              transition: "all 0.15s ease"
            }}
            title={isListening ? "Listening... Click to stop" : "Speak question with microphone"}
          >
            {isListening ? <MicOff size={16} /> : <Mic size={16} />}
          </button>
        )}

        <input
          type="text"
          placeholder="Ask about border vectors, naval patrols, airspace alerts, doctrine..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{
            flex: 1,
            background: "#111827",
            border: "1px solid rgba(255, 255, 255, 0.15)",
            borderRadius: "6px",
            padding: "8px 12px",
            color: "#FFFFFF",
            fontSize: "0.82rem",
            outline: "none"
          }}
        />

        <button
          onClick={() => handleSend()}
          disabled={loading || !query.trim()}
          style={{
            background: "linear-gradient(135deg, #0284c7, #0369a1)",
            border: "1px solid #38bdf8",
            borderRadius: "6px",
            padding: "8px 14px",
            color: "#FFFFFF",
            display: "flex",
            alignItems: "center",
            gap: "5px",
            fontSize: "0.8rem",
            fontWeight: 700,
            cursor: loading || !query.trim() ? "not-allowed" : "pointer",
            opacity: loading || !query.trim() ? 0.6 : 1
          }}
        >
          <Send size={14} />
          <span>Send</span>
        </button>
      </div>
    </div>
  );
}