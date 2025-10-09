import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@proficiency/ui": fileURLToPath(new URL("../../packages/ui/src", import.meta.url))
    }
  },
  server: {
    port: 5173
  }
});
