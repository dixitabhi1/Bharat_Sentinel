// Bharat Sentinel Centralized API & WebSocket Configuration

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || (
  typeof window !== "undefined" && window.location.hostname === "bharatsentinel.vercel.app"
    ? "https://bharat-sentinel.vercel.app"
    : ""
);

export function getApiUrl(endpoint) {
  const clean = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  return `${BACKEND_URL}${clean}`;
}

export function getWsUrl() {
  if (typeof window === "undefined") return "";
  if (BACKEND_URL.startsWith("http")) {
    const wsBase = BACKEND_URL.replace(/^http/, "ws");
    return `${wsBase}/ws/live`;
  }
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/ws/live`;
}

export default { getApiUrl, getWsUrl };

