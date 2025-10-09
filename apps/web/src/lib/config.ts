const DEFAULT_API_BASE_URL =
  typeof window === "undefined"
    ? "http://localhost:8000"
    : `${window.location.origin}/api`;

export const config = Object.freeze({
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL
});
