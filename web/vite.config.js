const path = require("path");
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
    resolve: {
        alias: {
            src: path.resolve(__dirname, "./src"),
            services: path.resolve(__dirname, "./src/services"),
            components: path.resolve(__dirname, "./src/components")
        }
    },
    server: {
        hmr: {
            host: "base.test",
            clientPort: 443,
            protocol: "wss"
        }
    },
    plugins: [react()]
});
