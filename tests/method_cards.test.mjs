import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const gardenRoot = process.env.GARDEN_ROOT;
if (!gardenRoot) throw new Error("Set GARDEN_ROOT to the local garden project root before running this adapter test");
const moduleBase = pathToFileURL(resolve(gardenRoot, "src/lib/physical-intuition") + "/");
const { proposeIntuitionWithModel } = await import(new URL("model-proposal.ts", moduleBase));
const { prepareDistillation } = await import(new URL("distill-prepare.ts", moduleBase));
const bundle = JSON.parse(await readFile(new URL("../method_cards.json", import.meta.url), "utf8"));
const cards = bundle.cards.map(({ cardId, ruleText, applicability }) => ({ cardId, ruleText, applicability }));

const task = {
  taskId: "observer-method-interface-fixture",
  title: "Synthetic interface test, not a physics claim",
  objective: "Check method-card injection without claiming empirical discovery",
  observables: [{ name: "position", unit: "m", dimension: { L: 1 } }],
  constraints: [],
  baseline: { name: "continuum-baseline", description: "Synthetic comparison baseline" },
  evidence: [],
  triggers: { noncommutative: true, discreteOrder: true },
};

function chat(request) {
  return Promise.resolve({
    provider: "kimi",
    model: "offline-fixture",
    content: request.systemPrompt.includes("JSON")
      ? JSON.stringify({ proposals: [{ structureKey: "causal_poset", statement: "Compare a discrete candidate", rationale: "Candidate structure only" }] })
      : "Synthetic method review; no source or evidence upgrade",
    finishReason: "stop",
    usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
    latencyMs: 1,
  });
}

test("observer method bundle enters all existing garden roles without identity or evidence upgrade", async () => {
  const prompts = [];
  const report = await proposeIntuitionWithModel({
    task,
    methodCards: cards,
    generatedAt: "2026-11-15T00:00:00.000Z",
    chat: (request) => { prompts.push(request.userPrompt); return chat(request); },
  });
  assert.equal(report.status, "complete");
  assert.deepEqual(report.methodCards, cards);
  assert.equal(report.exchanges.length, 3);
  assert.ok(prompts.every((prompt) => cards.every((card) => prompt.includes(card.ruleText))));
  assert.ok(report.proposals.every((card) => card.mathStatus === "proposal" && card.physicalStatus === "analogy"));
  assert.equal(report.evidenceUpgrade, false);
  assert.ok(!JSON.stringify(report).includes("◎粒子宇宙观察者25"));
});

test("hard-check failure survives method generation and public-post permission stays out of training", async () => {
  const card = {
    ...bundle.cards[0],
    problemFamily: "discrete-modeling",
    review: { status: "verified", reviewerId: "method-audit-fixture", reviewedAt: "2026-11-15T00:00:00.000Z" },
  };
  const sources = card.sourceIds.map((id) => ({
    sourceId: id,
    sourceUrl: `https://tieba.baidu.com/p/${id}`,
    authorLabel: "Public account with AI-assisted material; authorship of individual generated passages not established",
    recordState: "reviewed",
    registeredAt: "2026-11-15T00:00:00.000Z",
    coverage: "Selected public posts; not complete-profile or private reasoning",
    authorship: "unknown",
    excerpt: { text: "Selected public methodological material", locator: `Post ${id}; audit extract` },
    permission: { status: "unverified", identifier: "unverified", evidenceLocator: "" },
  }));
  const failedTask = { ...task, taskId: "observer-hard-check-fixture", constraints: [{ kind: "probabilities", values: [0.2, 0.3], tolerance: 1e-9 }] };
  const teacherReport = await proposeIntuitionWithModel({
    task: failedTask,
    methodCards: [{ cardId: card.cardId, ruleText: card.ruleText, applicability: card.applicability }],
    generatedAt: "2026-11-01T00:00:00.000Z",
    chat,
  });
  assert.ok(teacherReport.evaluation.cards.some((entry) => entry.checks.some((check) => check.status === "fail")));
  const result = prepareDistillation({
    sources,
    methodCards: [card],
    candidates: [{
      sampleId: "observer-method-fixture",
      problemFamily: "discrete-modeling",
      teacherReport,
      teacherRole: "theory_gardener",
      review: { reviewerId: "method-audit-fixture", sourceVerified: true, contradictionCheck: "passed", leakageCheck: "passed", claimMode: "method_only" },
    }],
    partitionAssignments: { trainProblemFamilies: ["discrete-modeling"], validationProblemFamilies: ["other-validation"], testProblemFamilies: ["other-test"] },
    cutoffs: { trainBefore: "2026-11-10T00:00:00.000Z", validationBefore: "2026-11-20T00:00:00.000Z" },
  });
  assert.equal(result.samples.length, 0);
  assert.ok(result.excluded[0].reasons.includes("permission_unverified"));
  assert.ok(result.excluded[0].reasons.includes("hard_constraint_failure"));
  assert.equal(result.readyForTraining, false);
  assert.equal(result.evidenceUpgrade, false);
});
