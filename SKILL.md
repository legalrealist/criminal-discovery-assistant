---
name: criminal-discovery-assistant
description: >-
  Use when a criminal defense attorney (public defender or CJA panel attorney)
  points Claude at a local case folder of government-produced discovery and
  wants a fast first pass to get up to speed. This skill builds an Excel
  discovery inventory/tracker from the documents and production letters,
  produces draft transcripts of recordings, reviews the indictment and takes a
  first pass through the discovery for evidence relevant to the specific charges
  against the client, and maintains a persistent case-memory document that it
  updates as new production arrives. Trigger this whenever the user mentions
  discovery, a government production, a CJA or criminal case folder, an
  indictment, Bates-stamped documents, bodycam/dashcam/jail-call/911
  recordings, "get me up to speed on this case," "review this production," or
  "build a discovery tracker" — even if they don't say "discovery tool." Works
  entirely on local files; it never uploads discovery anywhere.
---

# Criminal Discovery Assistant

A first-pass case assistant for criminal defense. Point it at a case folder of
government-produced discovery and it gives the defense team a running head
start: an inventory tracker, draft transcripts of the recordings, a
charge-by-charge read of what the evidence shows, and a living case-memory
document that grows as more discovery comes in.

This is the workflow that, in practice, has saved roughly 100 hours of attorney
time on a single large CJA production — and surfaced "nice to have" work that
would otherwise never get done under caseload pressure.

## What this is and is not

This produces a **first pass for attorney review, not a substitute** for the
lawyers digging into the evidence themselves. Everything it generates is a
starting point a human verifies. Three commitments make it safe to rely on:

- **Local only.** Operate exclusively on files already on the user's machine.
  Never upload, paste, or transmit discovery to any external service. Criminal
  discovery is routinely produced under protective orders that prohibit cloud
  upload, and client confidentiality applies to everything here.
  This local-only posture is the entire point — it is what lets the tool touch
  the actual discovery at all.
- **Cite to the source, never invent.** Every entry, summary, and quote points
  back to a specific file (and Bates number / timestamp when available). If
  something can't be located in the materials, say so plainly — do not fill the
  gap with plausible-sounding content. A fabricated citation or a hallucinated
  fact in a criminal matter is a serious harm, so err toward "not found in the
  production" over a confident guess.
- **Flag, don't conclude.** Surface issues for the attorney (possible
  exculpatory material, suppression hooks, missing items, contradictions) as
  flags to investigate, not as legal conclusions.

## Before you start

Confirm or establish three things, then proceed without further ceremony:

1. **The case folder** — the local path the user wants reviewed. If they
   haven't named it, ask for it.
2. **The indictment or charging document** — find it in the folder, or ask
   where it is. The charges drive the relevance review (Step 3), so this is
   worth locating early.
3. **Where outputs go** — default to a `_case-assistant/` subfolder inside the
   case folder so generated work stays with the case and never mixes with the
   produced discovery itself. Create it if absent.

Then take a quick inventory of the folder: how many files, what types
(documents, PDFs, images, audio, video, spreadsheets), and whether production
letters or a discovery index are present. Report this back briefly before
diving in so the user can redirect if needed.

## The workflow

Run these in order; each builds on the last. For a large production, work in
batches and checkpoint progress into the outputs as you go rather than holding
everything in memory.

### 1. Build the discovery inventory tracker (Excel)

Review the documents and any production/cover letters, then build an Excel
tracker at `_case-assistant/discovery-tracker.xlsx`. The tracker is the
backbone the rest of the case runs on, so make it something an attorney or
paralegal can actually work in and sort/filter. Use these columns:

| Column | What goes in it |
|---|---|
| Bates / File | Bates range if stamped, else the file name |
| Production | Which production volume + date received + cover-letter reference |
| Type | Report, recording, photo, lab/forensic, search warrant, etc. |
| Date | Date of the document/event, if determinable |
| Source | Authoring officer / agency / declarant |
| Description | One-line factual summary (no characterization) |
| Relevant counts | Which charge(s) this bears on (filled in Step 3) |
| Flags | Brady/Giglio, exculpatory, suppression hook, inconsistency, privileged |
| Status | Review status (e.g., Not reviewed / First-pass / Attorney-reviewed) |
| Notes | Working notes for the team |
| Path | Relative path to the file in the case folder |

Pull production-letter details (volume, date, what was said to be produced) into
the tracker too — they are the record of what the government *claims* it gave
you, which matters later for spotting gaps.

### 2. Draft transcripts of the recordings

Identify every audio/video file (bodycam, dashcam, jail calls, 911, interviews,
wiretaps). For each, produce a **draft** transcript saved under
`_case-assistant/transcripts/` mirroring the recording's name, using whatever
local transcription capability is available on the machine (a local model,
an installed CLI tool, or the platform's own audio tooling). If no local
transcription is available, list the recordings in the tracker, note that
transcription tooling is needed, and continue — do not skip inventorying them.

Mark transcripts clearly as **DRAFT — verify against the recording**: speaker
labels, timestamps, and inaudible passages are uncertain and must be confirmed
by a human before any courtroom use. Where the tool supports it, keep
timestamps so the attorney can jump to the moment in the source. Add each
recording as a row in the tracker with a pointer to its transcript.

### 3. Map the indictment to the discovery (charge-by-charge first pass)

Read the indictment and break each count into its elements. Then take a first
pass through the discovery asking, for **the specific charges against this
client**: what evidence supports each element, what undercuts it, and what's
simply missing. This is where the work compounds — it turns a pile of files
into a view of the actual case.

Record this in the case-memory document (Step 4), and back-fill the tracker's
"Relevant counts" and "Flags" columns as you go. While doing this pass, watch
for and flag:

- **Exculpatory / Brady-Giglio material** the defense will want to press.
- **Suppression hooks** — warrantless searches, consent questions, Miranda
  gaps, prolonged detention — as items to investigate, not adjudicate.
- **Referenced-but-not-produced evidence** — a report mentions a second bodycam
  angle, a 911 call, lab bench notes, an attachment that isn't in the
  production. These gaps are easy to miss and worth their own list.
- **Inconsistencies** between documents, or between a report and a recording.

### 4. Maintain the persistent case-memory document

Create and continuously update `_case-assistant/case-memory.md` — the working
document the team (and this skill) returns to instead of starting over each
time. When new production arrives, re-run the relevant steps and **append/update
this document rather than rewriting it**, keeping a dated log of what changed.

Structure it like this:

```markdown
# Case Memory — [Caption / Client] — [Case No.]

_Last updated: [date]. First pass by Criminal Discovery Assistant — for attorney review._

## Charges
[Each count + its elements, from the indictment]

## The government's theory
[How the production appears to connect to each count]

## Evidence by count
[Per count: what supports it, what undercuts it, key Bates/files]

## Flags to investigate
- Exculpatory / Brady-Giglio:
- Suppression hooks:
- Inconsistencies:

## Missing / referenced-but-not-produced
[Items the discovery references but did not include]

## Recordings index
[Each recording → transcript path → one-line gist]

## Open questions & next steps

## Production log
| Date received | Production | What it contained | Reviewed? |

## Changelog
- [date] — [what was added/updated this pass]
```

## When you finish a pass

Give the user a short orientation, not a wall of text: how many items were
inventoried, how many recordings (and how many transcribed), the charge map at
a glance, and the most important flags — each pointing to where the detail
lives in the tracker or case memory. Remind them the outputs are a first pass
for their review, and that re-running on the next production will update the
same files in place.
