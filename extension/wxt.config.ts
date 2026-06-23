import { defineConfig } from "wxt";

export default defineConfig({
  modules: ["@wxt-dev/module-react"],
  manifest: {
    name: "AI Brief Decoder Lite",
    description: "Decode brief text into structured goals, risks, and next actions.",
    permissions: ["clipboardWrite"],
    host_permissions: ["http://localhost:8000/*"],
    action: {
      default_title: "AI Brief Decoder Lite",
    },
  },
});
