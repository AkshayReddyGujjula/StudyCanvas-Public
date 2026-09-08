# Quality and verification

[Back to the project overview](../README.md) · [Architecture](ARCHITECTURE.md) · [Privacy and security](PRIVACY-AND-SECURITY.md)

## What this report can and cannot prove

The production source is private, so a visitor cannot run its full test suite from this repository. This report therefore separates three kinds of evidence:

- **Automated source checks:** commands run against the private production revision.
- **Implementation inspection:** a claim traced to a concrete source path and control flow.
- **Manual product checks:** behaviour observed in a real browser or captured from the live product.

Passing tests show that their stated contracts hold. They do not prove that every browser, document or model response behaves correctly.

## Latest verified snapshot

The following commands were rerun on 8 September 2026 against private revision `f5065d6`:

| Gate | Result | Scope |
|---|---:|---|
| Frontend focused regression runner | 46 of 46 passed | Selection, PDF lifecycle, streams, timers, versions, canvas behaviour, CSP and supporting utilities |
| Backend focused test runner | 9 of 9 passed | Validation, quotas, PDF limits, flashcard selection, quiz policy, model migration and exam contracts |

The frontend suite must be run from the `frontend` directory because several fixtures resolve files relative to that working directory. The backend runner is invoked with the project's virtual environment from the repository root.

Reference commands, shown for audit clarity rather than public reproduction:

```powershell
Set-Location frontend
node --experimental-strip-types scripts/run-all-regressions.mjs

Set-Location ..
& .venv\Scripts\python.exe backend/scripts/run_all_tests.py
```

The private runners discover matching test scripts rather than maintaining a handwritten list. This prevents a new regression file from existing outside the main gate.

## Frontend regression strategy

The frontend tests are small executable contracts built around bugs that reached realistic code paths. Representative areas include:

### Selection and context

- selection races between PDF, modal and canvas state
- multi-selection and selection clearing
- page-aware selection in continuous PDF view
- question modal cancellation
- node mention parsing and attachment budgets

### Stream lifecycle

- answer stream cancellation and abort cleanup
- summary requests interrupted by navigation
- code-chat stream framing
- incomplete or split control markers
- stale request protection

### Persistence and recovery

- timer and alarm persistence
- canvas version revert refresh
- PDF data restoration
- secondary PDF state
- filename and export handling
- workspace hydration

### Canvas interaction

- responsive viewports
- whiteboard gestures and straight-line assistance
- node placement for generated study artefacts
- multi-node selection
- dark-theme colour contracts

### Browser and embedding boundaries

- content security policy requirements for Desmos and YouTube
- YouTube URL normalisation
- PDF worker cleanup
- ResizeObserver fallback behaviour

These are contract tests rather than screenshot snapshots. They are fast enough to run as a complete gate and specific enough that a failure points to one behaviour.

## Backend test strategy

Backend scripts run in separate processes so one import or global-state failure cannot prevent the rest from reporting. The current set covers:

- request shape, decoded-byte and total multimodal budgets
- quota fallback and cost-control behaviour
- PDF size, page and text limits
- source-grounded flashcard creation
- quiz and generated-artefact policy
- model-name migration and fallback reporting
- Exam Forecast source roles, modes and deduplication
- exam grading verdict and unmarked-failure behaviour

External paid-model calls are not treated as deterministic unit tests. Provider responses are replaced with controlled fixtures when testing parsing and policy. Live calls belong in a separate smoke check because they can fail for quota, credentials, provider state or model drift.

## Manual browser matrix

The storage architecture makes browser coverage especially important.

| Browser family | Critical behaviour |
|---|---|
| Chromium desktop | File System Access workspace, directory permission recovery, full canvas interaction |
| Firefox desktop | IndexedDB fallback, PDF interaction, export and import |
| Safari desktop | IndexedDB fallback, PDF rendering and storage warnings |
| iOS Safari | Touch interaction, IndexedDB persistence, constrained canvas layout |
| Android Chromium | Touch interaction, IndexedDB persistence, upload and export behaviour |

The focused source audit on 8 September did not repeat this full manual matrix. Previous release work used real browser checks for canvas, PDF and marketing flows, but that historical evidence should not be mistaken for a current clean pass after every new commit.

## Product-capture evidence

The images in [`assets/product`](../assets/product) come from the running StudyCanvas application. They show:

- highlighted text becoming a grounded question
- answer branches on the real canvas
- browser-executed Python with terminal output
- the Exam Room with marks and timing
- a complete learning canvas with source and study artefacts

The capture flow uses real application state. It saves through the product's normal path and checks persisted IndexedDB records because React Flow deliberately removes off-screen nodes from the DOM. Exact PDF selections use a real mouse drag based on the rendered text range.

These captures prove the surfaces exist and were connected at capture time. They do not prove model accuracy or all edge cases.

## Performance evidence

Performance work is kept narrow and tied to the bottleneck it addressed:

| Area | Change | Evidence type |
|---|---|---|
| Handwriting | Speed-adaptive one-euro filtering and an incremental wet-stroke layer | Implementation inspection and dedicated gesture regressions |
| Frontend loading | Lazy workspace routes and manual bundle boundaries | Build output and implementation inspection |
| Saving | Reduced redundant serialisation and hot selector work | Implementation inspection and behaviour regressions |
| Backend latency | CPU-heavy file work moved off the event loop; clients reused | Implementation inspection and route tests |

An earlier product description included a percentage token-saving figure that could not be traced to a repeatable benchmark. It is intentionally absent here. Likewise, this report does not publish an FPS, latency percentile or model-accuracy number without a retained measurement method.

## Security verification approach

Security-relevant checks focus on boundaries that can create concrete harm:

- bearer authentication on protected API routes
- strict schema and binary validation before paid work
- raw user input removed from validation logs and error responses
- exact browser-origin allow-listing
- content security policy and frame denial
- temporary upload deletion in final cleanup
- durable quotas, project ceilings and feature kill switches
- server-owned content and separate abuse limits for the public demo
- short-lived voice tokens instead of browser-exposed provider credentials
- sanitisation of URLs and rich text before rendering

The [privacy and security report](PRIVACY-AND-SECURITY.md) documents the threat boundaries and honest limitations.

## Public repository quality gate

This public repository has its own small CI gate. It checks:

- no em dash appears in any tracked text file
- Markdown links to local files resolve
- required portfolio documents and product assets exist
- no obvious secret file such as `.env` is tracked
- UK spelling is used for a small set of common project terms
- Markdown files do not contain trailing whitespace except the deliberate two-space line break

Run it locally with:

```powershell
python scripts/check_docs.py
```

This gate keeps the report tidy. It does not inspect the private application.

## Known gaps

- No public source means the architecture cannot be independently built from this repository.
- No published model-quality benchmark covers grounded answers, handwriting recognition, grading or Exam Forecast prediction.
- External model and browser behaviour can change independently of the application.
- The latest source audit did not repeat the full manual browser matrix.
- Production analytics are intentionally not exported here, so usage claims are omitted.

Those gaps are stated because a smaller truthful claim is more useful than a broad one that cannot be checked.
