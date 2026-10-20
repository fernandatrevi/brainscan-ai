import { Sidebar } from "@/components/Sidebar";
import { Hero } from "@/components/Hero";
import { Workspace } from "@/components/Workspace";
import { ModelExplorer } from "@/components/ModelExplorer";
import { AboutSection } from "@/components/AboutSection";
import { Disclaimer } from "@/components/ui/Disclaimer";
import { StatCard } from "@/components/ui/StatCard";
export default function Home(){return <main className="mx-auto grid min-h-screen max-w-[1600px] gap-6 p-4 md:grid-cols-[245px_1fr] md:p-6"><Sidebar/><div className="min-w-0 space-y-8"><Hero/><Disclaimer/><div className="grid gap-4 sm:grid-cols-3"><StatCard label="Demo samples" value="03" detail="Synthetic signal examples"/><StatCard label="Model approaches" value="03" detail="Illustrative benchmark only"/><StatCard label="Clinical use" value="None" detail="Educational demonstration"/></div><Workspace/><ModelExplorer/><AboutSection/><footer className="pb-5 text-center text-xs text-slate-500">© 2026 BrainScan AI · Educational prototype · Not a medical device</footer></div></main>}
