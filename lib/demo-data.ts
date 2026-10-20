import type { DemoCase, ModelMetric } from "./types";
export const demoCases: DemoCase[] = [
{id:"sample-01",title:"Sample 01",description:"High contrast, asymmetric texture",category:"Example A",features:[12,18,28,44,62,73,68,51,29,17,11,8],confidence:0.87,imageLabel:"Illustrative signal pattern A"},
{id:"sample-02",title:"Sample 02",description:"Diffuse signal, subtle gradient",category:"Example B",features:[8,13,20,31,45,53,49,42,30,20,14,9],confidence:0.79,imageLabel:"Illustrative signal pattern B"},
{id:"sample-03",title:"Sample 03",description:"Balanced, low variance signal",category:"Example C",features:[16,18,20,22,25,24,23,21,20,18,17,16],confidence:0.91,imageLabel:"Illustrative signal pattern C"}
];
export const exampleMetrics:ModelMetric[]=[{name:"SVM",accuracy:88,recall:84,f1:86},{name:"Random Forest",accuracy:91,recall:89,f1:90},{name:"Ensemble",accuracy:93,recall:90,f1:91}];
