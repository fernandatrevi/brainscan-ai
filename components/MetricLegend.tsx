const items=[["Accuracy","#61e6ff"],["Recall","#a78bfa"],["F1 score","#65d6bc"]];
export function MetricLegend(){return <div className="flex flex-wrap gap-4 text-xs text-slate-300">{items.map(([label,color])=><span key={label} className="flex items-center gap-2"><i aria-hidden="true" className="h-2.5 w-2.5 rounded-full" style={{backgroundColor:color}}/>{label}</span>)}</div>}
