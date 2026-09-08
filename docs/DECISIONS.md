# Engineering decision record

[Back to the project overview](../README.md) · [Architecture](ARCHITECTURE.md) · [Engineering journey](ENGINEERING-JOURNEY.md)

This is a compact record of the decisions that shaped StudyCanvas. Each entry states the context, the choice, the alternatives and the cost accepted. Dates mark when the direction first became part of the product; the implementation has continued to evolve since then.

## ADR 001: Make the learning trail a graph

**Status:** Accepted  
**First adopted:** February 2026

### Context

A question about one paragraph often creates several independent follow-ups. A linear transcript hides which answer came from which passage and makes parallel lines of enquiry difficult to compare.

### Decision

Represent source material, answers and study artefacts as typed nodes connected by explicit edges on an infinite canvas. Keep an answer's source quote visible and allow both threaded and branched follow-ups.

### Alternatives considered

- A conventional chat beside the document
- A chat with collapsible thread groups
- A document annotation system with comments but no graph

### Consequences

The graph preserves provenance and makes parallel reasoning visible. It also makes layout, selection, persistence, keyboard access, mobile behaviour and stream lifecycle substantially harder than a transcript. React Flow provides the graph mechanics, but StudyCanvas still owns the meaning of every node and edge.

### Revisit when

The graph becomes a barrier for small screens or screen-reader navigation. A future design may need a synchronised linear outline rather than replacing the canvas.

## ADR 002: Keep workspaces local at rest

**Status:** Accepted  
**First adopted:** February 2026

### Context

Student workspaces contain source documents, personal notes and long-lived revision history. A central document database would add hosting cost, a larger privacy surface and an account dependency before the core study loop had proven useful.

### Decision

Store workspaces on the student's device. Use a real user-chosen folder when the File System Access API is available, and a versioned IndexedDB schema elsewhere. Keep both behind the same logical workspace model and support ZIP export.

### Alternatives considered

- A hosted relational database plus object storage
- IndexedDB on every browser
- Download-only JSON snapshots

### Consequences

Users own their files and the backend has no document library to protect. Folder mode survives browser-data clearing. IndexedDB mode improves compatibility but can be erased with site data. There is no automatic cross-device sync or real-time collaboration, and two storage adapters must stay behaviourally aligned.

### Revisit when

Users consistently need collaboration or cross-device continuity. Any hosted sync design must remain optional and preserve the local workspace as a first-class copy.

## ADR 003: Use direct scoped context instead of vector retrieval

**Status:** Accepted  
**First adopted:** February 2026

### Context

The main interaction starts from an exact selection in a document. Building embeddings and a vector index for every workspace would add ingestion time, storage, retrieval uncertainty and another system whose evidence is hidden from the student.

### Decision

Send bounded, labelled context directly: the selection, nearby page content, direct parent answer, recent history, relevant memories, explicit node mentions and optional visuals.

### Alternatives considered

- Chunk and embed every document at upload
- Keyword search over all workspace text
- Send the whole document for every turn

### Consequences

The evidence is exact and visible, context spend is bounded, and there is no index to maintain. The system is not a corpus-wide semantic search engine. Questions that need distant material must include an explicit reference, page range or supporting document.

### Revisit when

Multi-document research becomes a primary workflow and direct context can no longer cover it within model limits. Retrieval would need visible citations and measurable content-matched evaluation before adoption.

## ADR 004: Stream text and typed control frames over one response

**Status:** Accepted  
**First adopted:** February 2026

### Context

Answers should appear immediately, but one model turn can also produce usage data, sources, quizzes, flashcards, rolling summaries and images. The transport must survive a serverless HTTP proxy and support cancellation.

### Decision

Use `fetch` with a `ReadableStream`. Carry display text and delimited control frames in the same chunked response. Parse only complete frames, patch the answer node incrementally and create side artefacts from typed payloads.

### Alternatives considered

- Wait for one final JSON response
- Server-sent events with one event type per payload
- WebSockets
- Separate requests for each artefact

### Consequences

The user sees progress quickly and the existing HTTP path carries every result. The client parser must handle markers split across arbitrary network chunks, malformed tool payloads, aborts and late frames. A shared stream lifecycle registry is required to prevent stuck nodes.

### Revisit when

The control vocabulary becomes difficult to evolve safely. A versioned event protocol would then be worth the migration cost.

## ADR 005: Run student Python in the browser

**Status:** Accepted  
**First adopted:** March 2026

### Context

Students need to test code beside the explanation. Executing arbitrary snippets on the backend would require process isolation, resource limits, queueing, abuse controls and a much stronger sandbox.

### Decision

Run CPython through Pyodide in a Web Worker. Stream standard output and errors back to a terminal node. Remove browser networking and storage globals from the student environment after runtime setup.

### Alternatives considered

- Remote containers or ephemeral functions
- A JavaScript-only evaluator
- Static code blocks without execution

### Consequences

Code is real and the server never executes it. The initial WebAssembly download is large, package compatibility is narrower than native Python, and browser capability removal is defence in depth rather than a formal sandbox guarantee.

### Revisit when

Courses require native packages, multiple languages or long-running workloads that cannot fit a browser worker.

## ADR 006: Keep two document extraction paths behind one contract

**Status:** Accepted  
**First adopted:** February 2026, expanded August 2026

### Context

The best local extraction libraries are too heavy for the production serverless bundle, while large raw uploads can exceed request-body limits. The canvas still needs consistent page boundaries for navigation, highlights and prompts.

### Decision

Use a deployable pure-Python extraction path on the server, a higher-fidelity native path in local development, and PDF.js extraction in the browser for oversized uploads. Make every path emit the same page-delimited text contract and apply shared text hygiene.

### Alternatives considered

- One native service on a dedicated server
- Browser-only extraction
- Accept smaller files only
- Different frontend handling for every extraction engine

### Consequences

The frontend has one document model and the production bundle remains viable. Extraction quality can differ between paths, so regression fixtures and explicit error handling are required. Scanned pages still need the visual or OCR path.

### Revisit when

Document volume or fidelity justifies a dedicated asynchronous ingestion service.

## ADR 007: Use static model tiers and durable cost controls

**Status:** Accepted  
**First adopted:** February 2026, hardened June to September 2026

### Context

Titles, OCR, suggestions, grounded answers, image generation and exam synthesis have different cost and reliability needs. Serverless instances can disappear at any time, so in-memory usage counters cannot enforce a real project budget.

### Decision

Assign model tiers by task rather than predicting question complexity. Enforce durable per-user quotas, a project-wide ceiling and feature kill switches. Retain a limited in-memory floor for the most expensive paths if durable state is unavailable.

### Alternatives considered

- One model for every request
- A model-based complexity router
- Per-instance counters only
- Uncapped use behind authentication

### Consequences

Cost is predictable and routing decisions are easy to inspect. Some individual requests could be cheaper or better on another tier. Quota storage becomes an operational dependency, although the fallback avoids turning a storage outage into uncapped spending.

### Revisit when

There is enough labelled traffic to prove that dynamic routing improves cost or answer quality without hiding failure cases.

## ADR 008: Treat Exam Forecast as map-reduce synthesis

**Status:** Accepted  
**First adopted:** July 2026, redesigned September 2026

### Context

Putting several complete past papers into one prompt is expensive and makes it hard to preserve which patterns came from which paper. Supporting specifications and canvas notes also have different evidential roles from historical papers.

### Decision

Summarise each historical paper concurrently into a structured digest, then reduce those digests into a practice paper with source rationales. Keep past papers, specifications and canvas material role-labelled and deduplicated. Stream grading progress per question.

### Alternatives considered

- One large generation prompt
- Frequency counting with no model synthesis
- Treat every attached source as equivalent evidence
- Generate and grade the whole paper in one blocking response

### Consequences

The pipeline scales across several papers, preserves source roles and gives the Exam Room structured output. It makes multiple model calls and remains a revision aid rather than a validated predictor of future questions. Grading needs verifier logic and honest unmarked states for failures.

### Revisit when

A content-matched evaluation shows a simpler or more accurate approach, or when examination providers supply a reliable structured syllabus and question taxonomy.

## ADR 009: Optimise handwriting for perceived latency

**Status:** Accepted  
**First adopted:** February 2026, redesigned August 2026

### Context

A moving average can make handwriting smooth but causes fast strokes to trail the pen. Repainting every existing stroke on every pointer event also wastes the frame budget.

### Decision

Use a one-euro filter that adapts smoothing to movement speed. Draw the wet stroke incrementally on a scratch layer, then commit it to the durable layer when the pointer ends. Keep a hidden performance overlay for frame rate and input-to-paint measurements.

### Alternatives considered

- Raw pointer samples
- Fixed-window moving average
- Full-canvas repaint on every sample
- SVG paths for every wet-stroke update

### Consequences

Slow strokes lose jitter while fast strokes stay close to the nib. The renderer has more state and must handle pointer cancellation, zoom transforms and layer cleanup carefully.

### Revisit when

Pointer-event coalescing and measured device data support a simpler renderer with equal pen feel.

## Decision principles that emerged

Across these records, four principles kept repeating:

1. Make the source of an AI answer visible.
2. Put untrusted or heavy work at the safest practical boundary.
3. Treat platform limits and cost as architecture inputs, not deployment details.
4. State the cost of every decision and keep a condition for revisiting it.
