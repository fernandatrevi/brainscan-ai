export type DemoCase = { id: string; title: string; description: string; category: "Example A" | "Example B" | "Example C"; features: number[]; confidence: number; imageLabel: string };
export type ModelMetric = { name: string; accuracy: number; recall: number; f1: number };
