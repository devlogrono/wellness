import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
    strictPort: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "*",
      "Access-Control-Allow-Methods": "*",
      "X-Frame-Options": "ALLOWALL",
      "Content-Security-Policy": "frame-ancestors *;"
    }
  },
  build: {
    outDir: "../dist",
  }
});
