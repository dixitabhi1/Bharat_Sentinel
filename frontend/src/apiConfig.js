// Bharat Sentinel Centralized API & WebSocket Configuration

const isLocal = typeof window !== "undefined" && (
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "0.0.0.0"
);

// Canonical backend URL on Vercel for Bharat_Sentinel repository (translates underscore to double hyphen)
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || (
  isLocal ? "" : "https://bharat--sentinel.vercel.app"
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
