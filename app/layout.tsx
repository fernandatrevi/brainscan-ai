import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "BrainScan AI | Imaging Lab", description: "Interactive educational exploration of medical imaging and machine learning." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
