import type { Config } from "tailwindcss";
export default { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: { colors: { ink: "#070c1c", cyan: "#61e6ff", violet: "#a78bfa" } } }, plugins: [] } satisfies Config;
