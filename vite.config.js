import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ command, mode }) => {
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), "");
  return {
    build: {
      sourcemap: mode === "development",
      outDir: `${process.cwd()}/src/base/static/base/js/dist`,
      lib: {
        entry: [`${process.cwd()}/src/base/static/base/js/index.js`],
        formats: ["iife"],
        name: "__BASE_LIB__",
      },
    },
    define: {
      __APP_ENV__: env.APP_ENV,
    },
  };
});
