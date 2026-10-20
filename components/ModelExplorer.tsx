import { ModelChart } from "./ModelChart";
import { MetricLegend } from "./MetricLegend";
import { SectionHeading } from "./ui/SectionHeading";
export function ModelExplorer(){return <section id="models" className="scroll-mt-6"><SectionHeading eyebrow="Model explorer" title="Compare approaches" description="Sample metrics below demonstrate how evaluation can be visualized. They are not measurements from trained models."/><div className="glass rounded-2xl p-5"><div className="mb-4 flex flex-wrap items-center justify-between gap-3"><h3 className="font-semibold">Illustrative benchmark (%)</h3><span className="rounded-full border border-violet/30 bg-violet/10 px-3 py-1 text-xs text-violet">Mock data</span></div><ModelChart/><MetricLegend/></div></section>}
