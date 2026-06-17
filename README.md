# Criminal Discovery Assistant

A [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) that helps overworked criminal defense attorneys — public defenders and CJA panel attorneys — get up to speed on a case fast. Point Claude at a local folder of government-produced discovery and it gives the defense team a running head start.

It is built around a workflow that, in real CJA practice, has saved roughly **100 hours of attorney time on a single large production** — and surfaced "nice to have" work that would otherwise never get done under caseload pressure.

## What it does

When you point it at a case folder, it:

1. **Builds a discovery inventory tracker** (`discovery-tracker.xlsx`) from the documents and production letters — Bates ranges, source, type, relevant counts, issue flags, review status.
2. **Drafts transcripts of recordings** (bodycam, dashcam, jail calls, 911) using local transcription tooling, clearly marked *DRAFT — verify against the recording*.
3. **Maps the indictment to the discovery** — breaks each count into its elements and takes a first pass through the evidence on the specific charges against *your* client (what supports, what undercuts, what's missing).
4. **Maintains a persistent case-memory document** (`case-memory.md`) that updates in place as new production arrives, with a production log and changelog.

Along the way it flags possible **Brady/Giglio material**, **suppression hooks**, **inconsistencies**, and **referenced-but-not-produced evidence** — as items to investigate, not legal conclusions.

## Why local-first

Criminal discovery is routinely produced under **protective orders that prohibit uploading to any cloud service**, and client confidentiality (Rule 1.6) covers everything. This skill operates **entirely on local files and never transmits discovery anywhere**. That posture is the whole point — it is what lets the tool touch the actual discovery at all, where cloud tools cannot.

## What it is and is not

This produces a **first pass for attorney review, not a substitute** for the lawyers digging into the evidence themselves. Three commitments make it safe to rely on:

- **Local only** — nothing leaves the machine.
- **Cite to the source, never invent** — every entry points back to a specific file/Bates/timestamp; gaps are reported as "not found in the production," never filled with plausible-sounding content.
- **Flag, don't conclude** — issues are surfaced for the attorney, not adjudicated.

## Install

**Claude Code / Claude desktop:** copy the `SKILL.md` (and this folder) into your skills directory, e.g.:

```bash
mkdir -p ~/.claude/skills/criminal-discovery-assistant
cp SKILL.md ~/.claude/skills/criminal-discovery-assistant/
```

Then just describe the task — e.g. *"Get me up to speed on this CJA case, the discovery is in ~/cases/US-v-Smith"* — and the skill triggers.

## Try it

A synthetic example case (a two-count federal indictment with planted suppression hooks, an exculpatory witness, a consent inconsistency, and referenced-but-not-produced items) lives in [`examples/US-v-Doe`](examples/US-v-Doe). Point the skill at it:

> Get me up to speed on this case — the discovery is in examples/US-v-Doe.

The example contains **synthetic, fictional** data for demonstration only.

## Evals

[`evals/evals.json`](evals/evals.json) holds the test prompts and assertions used to develop the skill (built with the `skill-creator` workflow). In testing, a strong base model already handles much of this task; the skill's measured value is **consistency, persistence (the updating case-memory doc), and the baked-in local-only / cite-to-source / flag-don't-conclude guardrails** rather than a large raw-capability lift.

## License

MIT — see [LICENSE](LICENSE).

---

*This skill assists with legal work; it does not practice law. Outputs are a first pass requiring attorney review and verification.*
