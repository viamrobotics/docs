# Documentation Concept-Gap Playbook

A lightweight, repeatable method for finding **concept gaps** in documentation from the _user's_ perspective — the way a small docs team can run without a research budget. This is the method used to produce [`docs-concept-gaps.md`](./docs-concept-gaps.md); this file is the reusable process behind it.

**Audience assumption for Viam:** a software person with **no robotics background** learning to build a robotics product. The docs must teach two things at once — the **platform** (how Viam fits together) and the **robotics concepts** underneath it. A gap in either blocks the user.

---

## The core definition

> A **concept gap** is a user job that cannot be completed because a concept the job depends on is never defined in a findable place — it is only assumed or scattered.

Note what this is _not_: it is not "a page is missing." A section can be complete, well-written, and still have concept gaps, because gaps live in the seams **between** pages and in the concepts every page assumes but none owns.

The single most productive question:

> **Which concepts do many pages _use_ but zero pages _own_?**

A concept that N pages depend on and 0 pages define is, analytically, the highest-value gap you have.

---

## The five steps

### 1. Anchor to jobs, not topics

Start from what a user is trying to _do_, written as a job statement:

> "When I'm \[situation], I want to \[motivation], so I can \[outcome]."

Then a gap is defined precisely: a job where the user cannot form a correct mental model from the docs alone. Gap = job blocked, not page missing.

### 2. Walk the journey and find the breakpoints

For each job, lay out the steps and mark where a newcomer stalls. Gaps cluster at predictable seams:

| Gap type         | The user's experience                          | Diagnostic question                          |
| ---------------- | ---------------------------------------------- | -------------------------------------------- |
| **Prerequisite** | "This assumes I already know X"                | Is a term used before it's defined?          |
| **Conceptual**   | "I can follow the steps but don't know _why_"  | Can they predict the outcome of a change?    |
| **Bridging**     | "I get A and C but not how to get from A to C" | Is there a leap between two pages?           |
| **Boundary**     | "What happens when it fails / at the edges?"   | Are failure modes and limits covered?        |
| **Mental-model** | "I have the wrong picture in my head"          | Does the doc correct a likely misconception? |

Conceptual and mental-model gaps are what people usually mean by "concept gaps" — and they are invisible if you only audit for missing how-to steps.

### 3. Gather cheap evidence

A small team triangulates from whatever signal exists, instead of guessing:

- **Support / Discord / forum questions** — every repeated question is a documented gap. Tag and count.
- **Search-log misses** — what people search for and bounce from.
- **The "explain it back" test** — have someone in the target persona paraphrase the concept. A wrong paraphrase = a mental-model gap.
- **Assumed-knowledge audit** — read each page, underline every term used but not defined or linked. Each underline is a candidate gap.
- **Code / source-of-truth diffing** — compare what the SDK/API actually does against what the page claims. Behavior the code has but the docs don't explain is a gap by definition. _(This was the highest-yield technique for Viam — it surfaced the tracker overloading `class_name`, raw-tensor `viam infer` output, and the API-key-not-secret issue.)_
- **Ownership sweep** — for each core concept, grep the whole doc set and ask: is there **one** page that defines this, or is it only name-dropped? An empty glossary entry is a broken offload.

### 4. Classify and score each gap

Make it a table, not a vibe. Two axes:

- **Severity / frequency** — how many users hit it, how badly does it block them? (Support-ticket volume is a good proxy.)
- **Effort to close** — a sentence, a callout, a diagram, or a whole new page?

Plot them:

- **High frequency + low effort** → first sprint.
- **High severity + high effort** → roadmap.
- **Low / low** → backlog note.

This keeps a 3-person team from boiling the ocean.

### 5. Write each gap as a falsifiable statement

The deliverable is not "the frame docs are confusing." It is a row like:

> **Gap:** Users can't predict which orientation tolerance a constraint enforces.
> **Job blocked:** debugging a rejected arm move.
> **Evidence:** 4 Discord questions last quarter; the page lists constraints but not their tolerance semantics.
> **Type:** conceptual / boundary. **Severity:** high. **Effort:** low (one table).
> **Done when:** a user can state, before running, whether their pose will be accepted.

That **"done when → the user can \_\_\_"** line is what separates a professional gap analysis from a wishlist. Every gap closes against an observable user capability.

---

## Severity ordering (learned on the Viam pass)

Rank findings in this order, because not all "gaps" are equal:

1. **Correctness / safety** — the docs lead the user to an _insecure or unsafe result_ (e.g. shipping a client-bundled API key as if it were secret; no documented e-stop behavior when a teleop link drops). These outrank every missing explanation.
2. **Missing owner for a load-bearing concept** — a concept many pages depend on that no page defines (localization, sensor fusion, IMU).
3. **Buried owner** — the concept _is_ well explained, but only inside a section a newcomer on a different path won't find (frames/kinematics living only inside motion-planning).
4. **Cheap inline traps** — a single undefined acronym or unit used at high frequency (PID, DOF, deg/s vs rad/s).

---

## Anti-patterns to avoid in the analysis itself

- **Don't trust dramatic absolutes without a grep.** "Appears nowhere," "no page owns," "is missing" are exactly the claims a reviewer will test. Verify each load-bearing absolute with one command before it ships. (On the Viam pass, this correctly downgraded a "GPS is undocumented" claim to "under-surfaced.")
- **Don't call something MISSING when partial coverage exists.** "No single owner page" is both more accurate and harder to rebut than "missing."
- **Don't audit a section that's mid-rewrite as if it were stable.** Note the moving ground; a concept "owned" there today may move tomorrow.
- **State your coverage scope.** Say what you did _not_ review so the report isn't misread as exhaustive.
- **Cite `file:line`.** Every finding should be checkable in one click.

---

## Reusing this on another doc set

1. List the top ~10 user jobs for the audience.
2. Fan out one reviewer per section (or per job), each applying steps 1–3 and the gap-type table above.
3. Run one **ownership sweep** across the whole set for the domain's core concepts — this is where the highest-value gaps surface.
4. Merge, dedup, verify every absolute, then score and write "done when" statements.
5. Lead the report with correctness/safety, then unowned concepts, then buried owners, then cheap traps.

The test to keep coming back to: **a concept many pages use but zero pages own is your highest-value gap.**
