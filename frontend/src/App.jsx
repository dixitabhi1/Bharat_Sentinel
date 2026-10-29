import React, { useState, useEffect } from "react";
import SplashScreen from "./components/SplashScreen";
import Header from "./components/Header";
import TacticalMap from "./components/TacticalMap";
import ThreatFeed from "./components/ThreatFeed";
import ChatbotConsole from "./components/ChatbotConsole";
import DomesticStability from "./components/DomesticStability";
import AgentNeuralHUD from "./components/AgentNeuralHUD";
import ReviewQueueModal from "./components/ReviewQueueModal";
import EventSimulatorModal from "./components/EventSimulatorModal";

export default function App() {
  const [showSplash, setShowSplash] = useState(false);
  const [activeTab, setActiveTab] = useState("map"); // 'map', 'chat', 'stability', 'agents'
  
  // Timeframe, Search, and Global/India Scope filters
  const [timeframe, setTimeframe] = useState("6h");
  const [searchQuery, setSearchQuery] = useState("");
  const [scope, setScope] = useState("global"); // 'global' or 'india'
  const [isFeedCollapsed, setIsFeedCollapsed] = useState(false);

  // Intelligence Data Store
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [newsTicker, setNewsTicker] = useState([]);
  const [fleets, setFleets] = useState([]);
  const [leaders, setLeaders] = useState([]);
  const [flights, setFlights] = useState([]);
  const [vessels, setVessels] = useState([]);
  const [disasters, setDisasters] = useState([]);
  const [installations, setInstallations] = useState([]);
  const [geofence, setGeofence] = useState(null);
  const [reviewQueue, setReviewQueue] = useState([]);
  
  const [selectedItem, setSelectedItem] = useState(null);
  const [initialChatPrompt, setInitialChatPrompt] = useState("");

  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false);
  const [isSimulatorModalOpen, setIsSimulatorModalOpen] = useState(false);

  // Fetch filtered events when timeframe, search, or scope changes
  const fetchEvents = async () => {
    try {
      const params = new URLSearchParams();
      if (timeframe) params.append("timeframe", timeframe);
      if (searchQuery) params.append("search", searchQuery);
      if (scope) params.append("scope", scope);

      const res = await fetch(`/api/events?${params.toString()}`);
      if (res.ok) setEvents(await res.json());
    } catch (e) {
      console.error("Error fetching events:", e);
    }
  };

  // Fetch all core intelligence streams
  const refreshAllData = async () => {
    try {
      const [
        statsRes, 
        fleetsRes, 
        leadersRes, 
        flightsRes, 
        vesselsRes, 
        disastersRes, 
        installationsRes,
        tickerRes, 
        geoRes, 
        queueRes
      ] = await Promise.all([
        fetch(`/api/stats?scope=${scope}`),
        fetch(`/api/fleets?scope=${scope}`),
        fetch(`/api/leaders?scope=${scope}`),
        fetch(`/api/flights?scope=${scope}`),
        fetch(`/api/vessels?scope=${scope}`),
        fetch(`/api/disasters?scope=${scope}`),
        fetch("/api/installations"),
        fetch("/api/news-ticker"),
        fetch("/api/geofence"),
        fetch("/api/review-queue")
      ]);

      if (statsRes.ok) setStats(await statsRes.json());
      if (fleetsRes.ok) setFleets(await fleetsRes.json());
      if (leadersRes.ok) setLeaders(await leadersRes.json());
      if (flightsRes.ok) setFlights(await flightsRes.json());
      if (vesselsRes.ok) setVessels(await vesselsRes.json());
      if (disastersRes.ok) setDisasters(await disastersRes.json());
      if (installationsRes.ok) setInstallations(await installationsRes.json());
      if (tickerRes.ok) setNewsTicker(await tickerRes.json());
      if (geoRes.ok) setGeofence(await geoRes.json());
      if (queueRes.ok) setReviewQueue(await queueRes.json());
    } catch (e) {
      console.error("Error refreshing intelligence data:", e);
    }
  };

  useEffect(() => {
    refreshAllData();
    fetchEvents();
    const interval = setInterval(refreshAllData, 12000);

    // Live WebSocket connection for continuous real-time movement and events
    let ws;
    try {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      ws = new WebSocket(`${protocol}//${window.location.host}/ws/live`);
      
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === "TELEMETRY_TICK") {
            if (payload.flights) {
              setFlights(payload.flights);
            }
          } else if (payload.type === "NEW_FLAG" || payload.type === "EVENT_UPDATE") {
            refreshAllData();
            fetchEvents();
          }
        } catch (err) {}
      };
    } catch (err) {}

    return () => {
      clearInterval(interval);
      if (ws) ws.close();
    };
  }, [scope]);

  // Refetch events whenever timeframe, search query, or scope changes
  useEffect(() => {
    fetchEvents();
    refreshAllData();
  }, [timeframe, searchQuery, scope]);

  const handleAskChatbot = (item) => {
    const prompt = `Analyze this live intelligence vector / contact: "${item.title || item.callsign || item.ship_name || item.name || item.summary}". Explain tactical and strategic implications.`;
    setInitialChatPrompt(prompt);
    setActiveTab("chat");
  };

  const handleApproveReview = async (flagId, note) => {
    try {
      await fetch(`/api/review-queue/${flagId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note })
      });
      refreshAllData();
      fetchEvents();
    } catch (err) {
      console.error("Approve error:", err);
    }
  };

  const handleRejectReview = async (flagId, note) => {
    try {
      await fetch(`/api/review-queue/${flagId}/reject`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note })
      });
      refreshAllData();
      fetchEvents();
    } catch (err) {
      console.error("Reject error:", err);
    }
  };

  const handleEventSimulated = (result) => {
    refreshAllData();
    fetchEvents();
    if (result.flag) {
      setSelectedItem(result.flag);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", overflow: "hidden", background: "var(--bg-primary)" }}>
      {/* Splash Screen */}
      {showSplash && <SplashScreen onDone={() => setShowSplash(false)} />}

      {/* Top Header matching Monitor-the-Situation */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        stats={stats}
        timeframe={timeframe}
        setTimeframe={setTimeframe}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        scope={scope}
        setScope={setScope}
        newsTicker={newsTicker}
        onOpenReviewModal={() => setIsReviewModalOpen(true)}
        onOpenSimulatorModal={() => setIsSimulatorModalOpen(true)}
      />

      {/* Main View Area */}
      <main style={{ flex: 1, overflow: "hidden", display: "flex", position: "relative" }}>
        {activeTab === "map" && (
          <div style={{ display: "flex", width: "100%", height: "100%", position: "relative" }}>
            {/* Left Feed Drawer */}
            <ThreatFeed
              events={events}
              selectedItem={selectedItem}
              onSelectItem={(item) => setSelectedItem(item)}
              onAskChatbot={handleAskChatbot}
              isCollapsed={isFeedCollapsed}
              setIsCollapsed={setIsFeedCollapsed}
            />

            {/* Tactical Fullscreen Map Deck */}
            <div style={{ flex: 1, height: "100%", position: "relative" }}>
              <TacticalMap
                events={events}
                flights={flights}
                vessels={vessels}
                fleets={fleets}
                leaders={leaders}
                disasters={disasters}
                installations={installations}
                geofence={geofence}
                selectedItem={selectedItem}
                scope={scope}
                setScope={setScope}
                onSelectItem={(item) => setSelectedItem(item)}
                onAskChatbot={handleAskChatbot}
              />
            </div>
          </div>
        )}

        {activeTab === "chat" && (
          <div style={{ width: "100%", height: "100%", padding: "0.75rem" }}>
            <ChatbotConsole initialPrompt={initialChatPrompt} />
          </div>
        )}

        {activeTab === "stability" && (
          <div style={{ width: "100%", height: "100%", padding: "0.75rem" }}>
            <DomesticStability />
          </div>
        )}

        {activeTab === "agents" && (
          <div style={{ width: "100%", height: "100%", padding: "0.75rem" }}>
            <AgentNeuralHUD />
          </div>
        )}
      </main>

      {/* Analyst Review Gate Modal */}
      <ReviewQueueModal
        isOpen={isReviewModalOpen}
        onClose={() => setIsReviewModalOpen(false)}
        reviewQueue={reviewQueue}
        onApprove={handleApproveReview}
        onReject={handleRejectReview}
      />

      {/* Multi-Agent Event Simulator Modal */}
      <EventSimulatorModal
        isOpen={isSimulatorModalOpen}
        onClose={() => setIsSimulatorModalOpen(false)}
        onEventSimulated={handleEventSimulated}
      />
    </div>
  );
}
