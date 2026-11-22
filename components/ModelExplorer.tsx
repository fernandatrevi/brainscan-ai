import { SectionHeading } from "./ui/SectionHeading";

const approaches = [
  {
    title: "Majority-class baseline",
    label: "Reference",
    text: "Predicts the most frequent training class. Every learned model must be evaluated against this simple reference.",
  },
  {
    title: "HOG + SVM",
    label: "Classical ML",
    text: "Extracts image gradients and fits a support-vector classifier with scaling limited to the training set.",
  },
  {
    title: "HOG + Random Forest",
    label: "Classical ML",
    text: "Fits an ensemble of decision trees on the same handcrafted image features and evaluation split.",
  },
];

export function ModelExplorer() {
  return (
    <section id="models" className="scroll-mt-6">
      <SectionHeading
        eyebrow="Reproducible ML pipeline"
        title="From features to evaluation"
        description="The Python training pipeline contains real classifiers and quality checks. No medical-image benchmark scores have been independently verified or connected to this web demo."
      />
      <div className="glass rounded-2xl p-5 md:p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h3 className="font-semibold">Evaluation protocol</h3>
          <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-xs font-semibold text-amber-200">Measured MRI results: pending</span>
        </div>
        <div className="mt-5 grid gap-4 md:grid-cols-3">
          {approaches.map((model) => (
            <article key={model.title} className="rounded-xl border border-slate-700/70 bg-slate-950/30 p-4">
              <p className="text-xs font-semibold uppercase tracking-widest text-cyan">{model.label}</p>
              <h4 className="mt-2 text-base font-semibold text-slate-100">{model.title}</h4>
              <p className="mt-3 text-sm leading-6 text-slate-400">{model.text}</p>
            </article>
          ))}
        </div>
        <div className="mt-5 grid gap-5 rounded-xl border border-slate-700/70 bg-slate-950/20 p-4 md:grid-cols-2">
          <div>
            <h4 className="text-sm font-semibold text-slate-100">What the code measures</h4>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-400">
              <li>Accuracy, balanced accuracy and macro F1</li>
              <li>Per-class precision, recall and confusion matrix</li>
              <li>Class distributions and exact-file duplicate checks</li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-100">Limits before any medical claim</h4>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-400">
              <li>Patient-separated evaluation requires patient IDs</li>
              <li>Independent validation, uncertainty and calibration remain necessary</li>
              <li>Public samples and model outputs are not diagnostic</li>
            </ul>
          </div>
        </div>
        <a
          className="mt-5 inline-flex rounded-xl border border-cyan/30 px-4 py-2 text-sm font-semibold text-cyan transition hover:bg-cyan/10"
          href="https://github.com/fernandatrevi/brainscan-ai/blob/main/docs/ml-evaluation.md"
          target="_blank"
          rel="noopener noreferrer"
        >
          Review the evaluation methodology ↗
        </a>
      </div>
    </section>
  );
}
