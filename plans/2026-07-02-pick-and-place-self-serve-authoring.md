# Pick-and-Place Self-Serve Workshop Authoring — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure the pick-and-place workshop from 5 to 6 phases and author/reconcile every page to the finalized self-serve spec, with all code and JSON verified against the published companion repo.

**Architecture:** One mechanical restructure commit establishes the 6-phase skeleton (renames, split, renumber, nav chains) with the build green. Then one authoring commit per page (`_index`, Phases 1–6), each grounded in the finalized content spec and the real companion code, each passing the four pre-PR checks. A final consistency sweep closes it out.

**Tech Stack:** Hugo + Docsy static site (Markdown under `docs/tutorials/pick-and-place/`), project shortcodes (`workshop-phases`, `workshop-nav`, `checkpoint`, `alert`), prettier / markdownlint / vale / `make build-prod`.

**Sources of truth:**

- Content spec (per-page requirements): `../pick-and-place/pick-n-place-tutorial-plan.md`
- Self-serve rationale / decisions: `../pick-and-place/tutorial-review-notes.md`
- Verified code: `../pick-and-place/scripts/{starter-script.py,reference-solution.py,pyproject.toml,.python-version}`
- Verified config: `../pick-and-place/config/{machine-fragment.json,obstacles-template.json}`
- Design: `plans/2026-07-02-pick-and-place-self-serve-authoring-design.md`

**Key facts locked from the companion code (do not drift from these):**

- Detection is **shape-based**: vision service `vision-segment` (model `detections-to-segments`), fed by a `shape-detector`. Objects come from `vision.get_object_point_clouds("cam-1")`; the label is `obj.geometries.geometries[0].label`.
- There are **five poses**, one bin: `home-pose`, `approach-pose`, `grasp-pose`, `travel-pose`, `place-pose`. **Not** per-color bins.
- Poses are saved with `erh:vmodutils` arm-position-saver **switch** components; `set_position(2)` executes a saved pose, `set_position(1)` saves, `set_position(0)` clears.
- Obstacles are **`erh:vmodutils:obstacle` components** (`api: rdk:component:gripper`) added to the machine `components` array — **not** a motion-service WorldState array. They appear in `resource_names` as grippers.
- Motion service name is `"builtin"`. `motion.move(component_name="gripper-1", destination=PoseInFrame(reference_frame="world", pose=...))` drives the **gripper** frame to a world pose.
- Constants: `GRIPPER_LENGTH_MM = 60` (grasp offset), `APPROACH_MM = 100`, settle `0.3 s`. Optional straight-down descent uses `Constraints(linear_constraint=[LinearConstraint(line_tolerance_mm=5.0)])`.
- Python: `requires-python = ">=3.10"`, repo pins `3.11` via `.python-version`. `uv` is primary; pip is fallback.
- Companion repo is **published** at <https://github.com/viam-devrel/pick-and-place>; remove any "does not exist yet" TODO.

**House style (follow the branch, not the plan's speculative schema):** frontmatter keys `title`, `linkTitle`, `type: "docs"`, `slug`, `weight`, `description`, `workshop: "pick-and-place"`, `toc_hide: true`, `phase`, `phase_total`, `time_estimate`, `prev`, `next`, `languages`. Body opens with `{{< workshop-phases >}}` and ends with `{{< workshop-nav >}}`. Callouts use `{{< checkpoint >}}` and `{{< alert title="…" color="note" >}}`. Companion links use real `https://github.com/viam-devrel/pick-and-place` URLs.

**Per-task verification convention:** after editing, run the four checks scoped to the workshop directory, in order (prettier → markdownlint → vale → build). Commit only when all pass. Full commands are in Task 9; abbreviated per task as "run the four checks."

---

### Task 1: Restructure to six phases (mechanical prep commit)

**Goal:** Establish the 6-phase file/frontmatter/nav skeleton with the build green. No prose authoring yet beyond moving existing stub content.

**Files:**

- Rename: `docs/tutorials/pick-and-place/04-local-python-script.md` → `04-control-the-robot-from-python.md`
- Create: `docs/tutorials/pick-and-place/05-perception-guided-picking.md`
- Rename: `docs/tutorials/pick-and-place/05-inline-module.md` → `06-inline-module.md`
- Modify: `01-platform-mental-model.md`, `02-configure-resources.md`, `03-static-positions.md`, `_index.md`

**Step 1: Rename files with git mv (preserve history)**

```bash
cd /Users/nick.hehr/src/viam-docs/docs/tutorials/pick-and-place
git mv 04-local-python-script.md 04-control-the-robot-from-python.md
git mv 05-inline-module.md 06-inline-module.md
```

**Step 2: Set `phase_total: 6` on all six phase pages**

In each of `01`…`06`, change `phase_total: 5` to `phase_total: 6`.

**Step 3: Fix Phase 4 frontmatter (renamed file)**

In `04-control-the-robot-from-python.md`, set:

```yaml
title: "Phase 4: Control the robot from Python"
linkTitle: "4. Control from Python"
slug: "control-the-robot-from-python"
weight: 40
phase: 4
phase_total: 6
time_estimate: "15 minutes"
prev: "/tutorials/pick-and-place/static-positions/"
next: "/tutorials/pick-and-place/perception-guided-picking/"
description: "Connect from your laptop and drive the saved static pick-and-place sequence from a Python script."
```

Then **remove the perception sections** from the Phase 4 body (the "The frame system and transforms", "Add perception", and "Pass obstacles to the motion service" TODO blocks) — they move to Phase 5 in Step 5. Leave the static-sequence and connection scaffolding.

**Step 4: Fix Phase 6 frontmatter (renamed file)**

In `06-inline-module.md`, set:

```yaml
title: "Phase 6: Inline module"
linkTitle: "6. Inline module"
weight: 60
phase: 6
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/perception-guided-picking/"
```

(Keep `slug: "inline-module"`.)

**Step 5: Create the Phase 5 stub**

Create `05-perception-guided-picking.md` with frontmatter and a section skeleton (prose authored in Task 7). Move the perception TODOs removed from Phase 4 here.

```yaml
---
title: "Phase 5: Perception-guided picking"
linkTitle: "5. Perception-guided picking"
type: "docs"
slug: "perception-guided-picking"
weight: 50
description: "Add the vision pipeline and write the perception loop that detects a block, transforms it to the world frame, and picks it with motion planning."
workshop: "pick-and-place"
toc_hide: true
phase: 5
phase_total: 6
time_estimate: "22 minutes"
prev: "/tutorials/pick-and-place/control-the-robot-from-python/"
next: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
---
```

Body: `{{< workshop-phases >}}` at top, `{{< workshop-nav >}}` at bottom, with `## Configure the vision pipeline`, `## The frame system and transform_pose`, `## Detect from home (the wrist-camera rule)`, `## Compute the approach and grasp poses`, `## Run the full pick loop`, `## Debugging guide` section stubs.

**Step 6: Update the remaining prev/next links for the renumber**

In `03-static-positions.md`, set `next: "/tutorials/pick-and-place/control-the-robot-from-python/"`.
Grep to confirm no stale slugs remain (old `/local-python-script/`; and `/inline-module/` must now only appear as Phase 5's `next` and Phase 6's own slug):

```bash
cd /Users/nick.hehr/src/viam-docs
grep -rn "local-python-script" docs/tutorials/pick-and-place/    # expect: zero
grep -rn "phase_total: 5" docs/tutorials/pick-and-place/         # expect: zero
```

**Step 7: Update the `_index.md` phase list to six entries (interim)**

In `_index.md`, replace the five-item Phases list (lines ~41-47) and the "structured as five sequential phases" sentence with six entries and corrected links/titles/estimates. (The full self-serve rewrite of surrounding prose is Task 2; here just keep links valid so the build passes.)

```markdown
## Phases

1. **[Platform mental model](/tutorials/pick-and-place/platform-mental-model/)** (~15 min)
2. **[Configure resources and explore the app](/tutorials/pick-and-place/configure-resources/)** (~20 min)
3. **[Static positions and safety obstacles](/tutorials/pick-and-place/static-positions/)** (~20 min)
4. **[Control the robot from Python](/tutorials/pick-and-place/control-the-robot-from-python/)** (~15 min) — milestone one
5. **[Perception-guided picking](/tutorials/pick-and-place/perception-guided-picking/)** (~22 min) — milestone two
6. **[Inline module](/tutorials/pick-and-place/inline-module/)** (~20 min, optional)
```

**Step 8: Run the four checks**

Run prettier → markdownlint → vale → `make build-prod` (see Task 9 for exact commands). Expected: build completes without errors; `workshop-phases`/`workshop-nav` render six phases.

**Step 9: Commit**

```bash
git add docs/tutorials/pick-and-place/
git commit -m "refactor(tutorials): restructure pick-and-place to six phases

Split perception into Phase 5, rename Phase 4 to control-the-robot-from-python,
renumber inline module to Phase 6, bump phase_total, rewire prev/next."
```

---

### Task 2: Rewrite `_index.md` (facilitated → self-serve)

**Goal:** Carry the orientation a facilitator would deliver live: two-milestone framing, a prerequisites gate, self-serve entry paths.

**Files:** Modify `docs/tutorials/pick-and-place/_index.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`pick-and-place/_index.md`" bullets, and `tutorial-review-notes.md` → Phase 0.

**Content requirements:**

- **Intro:** six phases; "Phases 1–5 are the core workshop; Phase 6 is optional." Correct the detection narrative to **shape-based sorting into a bin** (not "sorted by color"). Two-milestone framing: Phase 4 (drive the robot from your own code) = milestone one, a bankable win; Phase 5 (perception) = milestone two.
- **What you'll build:** one paragraph — xArm6 + finger gripper + wrist-mounted RealSense; a shape-detection vision service finds blocks, the motion service plans collision-free picks, blocks are placed in the bin; by end of Phase 5 a Python script runs the full detect-pick-place loop.
- **Hardware:** keep the existing four-item list.
- **Phases:** the six-item list from Task 1 Step 7, with the milestone annotations.
- **Prerequisites gate** (replace the current "Hardware pre-provisioned for you / guided workshop" block):
  - A checklist with verification commands **and** install links: Python 3.10+ (link to python.org / uv install), the Viam Python SDK (`uv add viam-sdk`; link to SDK docs), a working terminal, and a Viam account with an accessible machine (link to app.viam.com).
  - **Login/machine-access as a prerequisite:** "log in at app.viam.com, open your machine, confirm the green **Live** indicator."
  - **Environment validation** before Phase 4: a working Python env (`uv` recommended) that can `import viam`:

    ```sh
    python3 --version                                   # 3.10 or newer
    uv run python -c "import viam; print(viam.__version__)"   # prints a version
    ```

  - **Two entry paths**, distinguishing hardware provisioning from resource configuration: "Physical hardware ready → start at Phase 1" / "Provisioning your own hardware → complete the setup guide first (forthcoming)." Note that only physical hardware + viam-agent/server may be pre-provisioned; **resource configuration is always the learner's hands-on work.**
- **Companion code:** keep the `viam-devrel/pick-and-place` link; describe `config/` (check-your-work reference), `scripts/` (starter + reference). **Remove** the "companion repo does not exist yet" TODO.

**Verification:** run the four checks. `grep -n "pre-provisioned by instructor\|sorted by color\|does not exist yet" docs/tutorials/pick-and-place/_index.md` → expect zero.

**Commit:** `docs(tutorials): rewrite pick-and-place overview for self-serve (milestones, prerequisites gate)`

---

### Task 3: Author Phase 1 — `01-platform-mental-model.md`

**Goal:** Concept phase grounded in live app interaction, ending with a self-check.

**Files:** Modify `docs/tutorials/pick-and-place/01-platform-mental-model.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`01-platform-mental-model.md`"; `tutorial-review-notes.md` → Phase 1.

**Content requirements (replace TODO stubs with prose):**

- Three questions up top the learner should be able to answer by the end (state them; used by the closing self-check).
- Three-layer architecture (cloud app / `viam-agent` / `viam-server`), SDK connection, config-as-source-of-truth, resource model (components vs. services), the dependency graph.
- **Live grounding** in each section: "open your **CONFIGURE** tab, find `arm-1`, read its `namespace:family:model`," etc. — overrides any "no live interactions yet" stance.
- Keep the perception-pipeline **foreshadow**: use `shape-detector` and `vision-segment` as concrete examples of services / composing resources (they build these in Phase 5).
- **Builtin (RDK) vs. module-provided resources:** most added functionality comes from modules; explain how modules interact with `viam-server`, and preview the module-download moment (it lands in Phase 2 when they add the xArm).
- **Closing self-check** ({{< alert … >}} or plain): "you should now be able to answer the three questions from the top — if not, re-skim."

**Verification:** run the four checks.

**Commit:** `docs(tutorials): author Phase 1 platform mental model (self-serve)`

---

### Task 4: Author Phase 2 — `02-configure-resources.md`

**Goal:** First hands-on phase: configure every resource by hand and verify with test cards.

**Files:** Modify `docs/tutorials/pick-and-place/02-configure-resources.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`02-configure-resources.md`"; `tutorial-review-notes.md` → Phase 2 and the cross-cutting "resources are hands-on" correction.

**Content requirements:**

- Learner configures **each** hardware resource by hand: `arm-1` (`viam:ufactory:xArm6`), `gripper-1`, `cam-1`. Present the resource table as **target state**, not "what's pre-configured."
- Configuring the xArm is the **module-download moment**: add the arm, watch `viam-server` download + start the module live (delivers the Phase 1 builtin-vs-module lesson).
- **CONTROL tab test cards** with per-card **checkpoints**: camera card (see a frame), arm card (jog joints), gripper card.
- **3D scene tab active task:** "jog joint 1 and watch the `cam-1` frame move with the arm" — this is the wrist-mounted-camera insight, load-bearing for Phase 5's detect-from-home rule.
- **Gripper `IsHoldingSomething` task:** place a block between the fingers, press **Grab**, observe the status; add a gripper checkpoint for symmetry.
- **The vision pipeline is NOT configured here** — it moves to Phase 5. Remove any vision-service config from this page if present.

**Verification:** run the four checks. `grep -n "pre-configured\|vision-segment\|shape-detector" docs/tutorials/pick-and-place/02-configure-resources.md` → expect zero (vision belongs to Phase 5).

**Commit:** `docs(tutorials): author Phase 2 hands-on resource configuration`

---

### Task 5: Rewrite Phase 3 — `03-static-positions.md` (self-serve + model correction)

**Goal:** Self-serve rewrite AND correct the detection/obstacle model: five poses with a single `place-pose`, obstacles as `erh:vmodutils:obstacle` components, measure-your-own-workspace.

**Files:** Modify `docs/tutorials/pick-and-place/03-static-positions.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`03-static-positions.md`"; `tutorial-review-notes.md` → Phase 3. Verify JSON against `../pick-and-place/config/obstacles-template.json` and pose names against `reference-solution.py`.

**Content corrections from the current page (all required):**

1. **Five poses, single bin.** Replace the per-color bin poses (`red-bin-pose`, `blue-bin-pose`, `green-bin-pose`) with the five canonical poses: `home-pose`, `approach-pose`, `grasp-pose`, `travel-pose`, `place-pose`. Update the two tables accordingly.
2. **Hands-on pose setup** (remove "the machine is already configured… pre-loaded configuration"): add `erh:vmodutils` arm-position-saver from the Registry, add one **switch** per pose with `arm: arm-1`; configure `home-pose` fully, then use the app's **"duplicate" resource feature** for the other four. `machine-fragment.json` is the **check-your-work reference**, not an import.
3. **Measure your own workspace** (remove "Your workshop facilitator provides the table and bin dimensions"): teach how frame geometries are configured; the learner measures the table and obstacles with `GetEndPosition` and translates measurements into geometry config.
4. **Obstacles are components, not a WorldState array.** Replace the current `{"obstacles": [...]}` JSON with the real `erh:vmodutils:obstacle` component form. Use this verbatim (from `obstacles-template.json`), noting `REPLACE_WITH_MEASURED_*` placeholders and that these appear in `resource_names` as grippers:

    ```json
    {
      "name": "table",
      "api": "rdk:component:gripper",
      "model": "erh:vmodutils:obstacle",
      "attributes": {
        "geometries": [
          {
            "label": "table",
            "type": "box",
            "x": 1200,
            "y": 800,
            "z": 30,
            "translation": { "x": 0, "y": 0, "z": -15 },
            "parent": "world"
          }
        ]
      }
    }
    ```

   Explain: box `z` translation is the box **center** (half its height); the table sits below `world` z=0 so its z is negative half-thickness (`-15` for a 30 mm top). Then the two **safety walls** (`safety-wall-front`, `safety-wall-side`) as thin vertical boxes at the workspace boundary with `REPLACE_WITH_MEASURED_*` positions.
5. **Safety walls as a production-motion feature** — configured to fit the learner's workspace; pitch virtual walls as a demo of the motion planner honoring obstacles for real-world/production deployments, not just classroom safety.
6. **Keep the problem-isolation rationale** as proof of value (pose-to-pose motion is a real production workcell workflow).
7. **Keep** the SetPosition `1`=save / `2`=execute callout, plus the "SetPosition(2) does nothing → you didn't save first" troubleshooting aside.
8. Link `obstacles-template.json` and `machine-fragment.json` in the companion repo as check-your-work references; remove the "illustrative JSON must be reconciled" TODO once the JSON matches the template.

**Verification:** run the four checks. `grep -n "facilitator provides\|red-bin\|blue-bin\|green-bin\|\"obstacles\"" docs/tutorials/pick-and-place/03-static-positions.md` → expect zero. `grep -n "erh:vmodutils:obstacle\|place-pose" …/03-static-positions.md` → expect hits.

**Commit:** `docs(tutorials): rewrite Phase 3 for self-serve (five poses, component obstacles, measured workspace)`

---

### Task 6: Author Phase 4 — `04-control-the-robot-from-python.md`

**Goal:** Drive the **static** sequence from Python. No perception.

**Files:** Modify `docs/tutorials/pick-and-place/04-control-the-robot-from-python.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`04-control-the-robot-from-python.md`"; `tutorial-review-notes.md` → Phase 4. Code from `../pick-and-place/scripts/starter-script.py`.

**Content requirements:**

- **Why a script before a module** (comparison): programmability (loops/branches/logic) AND the Control-tab-UI-controls → SDK-method-name mapping (the cards map to methods). Make the payoff felt.
- **Get the companion project:** clone/download `viam-devrel/pick-and-place`, work in `scripts/`. `uv` is primary (`uv run python starter-script.py`; it reads `pyproject.toml`/`.python-version`); pip is fallback. Env was already validated in the prerequisites gate — this phase is connect + run.
- **Connection:** reference the **Connect tab → Python SDK** boilerplate; the starter's `connect()` mirrors it. Show the connection block and the `MACHINE_ADDRESS`/`API_KEY`/`API_KEY_ID` fill-ins. **Secrets note:** don't commit API keys; use the repo `.gitignore` or env vars.
- **Verify the connection** with `print(machine.resource_names)` — a **checkpoint**: you should see `arm-1`, `gripper-1`, `cam-1`, the poses as switches, and the obstacles as grippers.
- **Run the static sequence** (verbatim, matches `starter-script.py` TODO 4):

    ```python
    await home.set_position(2)
    await approach.set_position(2)
    await gripper.open()
    await grasp.set_position(2)
    await gripper.grab()
    await asyncio.sleep(0.3)  # finger gripper settle
    await travel.set_position(2)
    await place_pose.set_position(2)
    await gripper.open()
    await home.set_position(2)
    ```

- **Obstacles are not passed in code** — they live in the machine config (Phase 3) and apply to every `motion.move` automatically. No runtime WorldState.
- **Checkpoints:** `resource_names` prints all resources; the static sequence runs end-to-end from Python.
- Connection-debugging aside for common failures.

**Verification:** run the four checks. `grep -n "get_object_point_clouds\|transform_pose\|vision" …/04-control-the-robot-from-python.md` → expect zero (perception is Phase 5).

**Commit:** `docs(tutorials): author Phase 4 driving the static sequence from Python`

---

### Task 7: Author Phase 5 — `05-perception-guided-picking.md` (new page)

**Goal:** The hardest phase: configure vision, transform to world, compute offsets, run the pick loop. Code verified against `reference-solution.py`.

**Files:** Modify `docs/tutorials/pick-and-place/05-perception-guided-picking.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`05-perception-guided-picking.md`"; `tutorial-review-notes.md` → Phase 5.

**Content requirements:**

- **Configure the vision pipeline here** (moved from Phase 2): a `shape-detector` feeding `vision-segment` (model `detections-to-segments`); test it in the **CONTROL** tab. First sub-checkpoint: detector works in the app.
- **Frame system + `transform_pose`:** the detection is in the `cam-1` frame; the planner needs `world`. Show:

    ```python
    obj_in_cam = PoseInFrame(reference_frame=CAMERA_NAME, pose=geometry.center)
    obj_in_world = await machine.transform_pose(obj_in_cam, "world")
    ```

- **Detect from home (wrist-camera rule):** the camera is wrist-mounted, so its frame moves with the arm — you MUST detect from `home-pose`. **Home-pose guard clause** structurally enforced (`await home.set_position(2)` before every detect) and made the **first** entry in the debugging guide.
- **Detection** (verbatim from reference):

    ```python
    objects = await vision.get_object_point_clouds(CAMERA_NAME)
    if not objects:
        print("No objects detected")
        return False
    obj = max(objects, key=lambda o: len(o.point_cloud))   # len(), not .size
    geometry = obj.geometries.geometries[0]
    label = geometry.label
    ```

- **Approach offset worked; learner practices the grasp offset.** Walk through the approach pose fully: `approach_pose = offset_pose(obj_in_world.pose, APPROACH_MM)` (`APPROACH_MM = 100`). Then have the learner compute the grasp offset themselves; the answer is `grasp_pose = offset_pose(obj_in_world.pose, GRIPPER_LENGTH_MM)` (`GRIPPER_LENGTH_MM = 60`, the gripper-TCP-to-fingertip depth). Include the `offset_pose` helper.
- **`motion.move("gripper-1", …)` semantics explicit:** it drives the **gripper** coordinate frame to the destination world pose — NOT the arm end (which is what the UI MoveToPosition / the arm component `move_to_position` do). Contrast the two so the offset math makes sense.
- **Full pick loop** (hybrid: `motion.move` for the Cartesian pick, saved switches for the place), verbatim:

    ```python
    await motion.move(
        component_name=GRIPPER_NAME,
        destination=PoseInFrame(reference_frame="world", pose=approach_pose),
    )
    await gripper.open()
    await motion.move(
        component_name=GRIPPER_NAME,
        destination=PoseInFrame(reference_frame="world", pose=grasp_pose),
    )
    await gripper.grab()
    await asyncio.sleep(0.3)
    await travel.set_position(2)
    await place_pose.set_position(2)
    await gripper.open()
    await home.set_position(2)
    ```

  Mention the optional straight-down descent follow-up: `Constraints(linear_constraint=[LinearConstraint(line_tolerance_mm=5.0)])` on the grasp move.
- **Debugging guide:** symptom → **3D scene tab** (what to look for), with a back-link to Phase 3 obstacle/safety-wall config (skipping it bites here). Home-pose guard is entry #1.
- **Granular sub-checkpoints:** detector works → transform yields sane world coords → approach reachable → grasp succeeds → full loop completes.

**Verification:** run the four checks. `grep -n "point_cloud.size\|red-bin\|move_to_position(" …/05-perception-guided-picking.md` → expect zero (use `len(...)`, single bin, gripper-frame `motion.move`). `grep -n "get_object_point_clouds\|transform_pose\|GRIPPER_LENGTH_MM" …` → expect hits.

**Commit:** `docs(tutorials): author Phase 5 perception-guided picking`

---

### Task 8: Author Phase 6 — `06-inline-module.md` (optional; corrected API)

**Goal:** Package the script as an inline module, with the **corrected** in-module `RobotClient` pattern.

**Files:** Modify `docs/tutorials/pick-and-place/06-inline-module.md`

**Spec:** `pick-n-place-tutorial-plan.md` → "`06-inline-module.md`"; `tutorial-review-notes.md` → Phase 6.

**Content requirements:**

- **Framed as optional** (no time pressure). **Strong "why bother":** you'd want this when it must survive disconnection, auto-restart, OTA deploy, or run on a schedule.
- **Honest framing:** "mostly packaging + one real change" — the `transform_pose` access genuinely changes; don't let a "same logic, different entry point" line set a trap.
- **Tier the scope:** MVP (repackage + `do_command`, trigger manually) is the core optional path; scheduled jobs + autonomous operation are an explicit "level 2."
- Inline module editor walkthrough; `validate_config` + `reconfigure` (dependency injection).
- **CORRECTED `transform_pose` inside a module** — there is **no** `FrameSystemClient` and no injected frame-system dependency. Create a **single, reused `RobotClient`** from env vars. Verbatim:

    ```python
    import os
    from viam.robot.client import RobotClient

    async def create_robot_client_from_module():
        opts = RobotClient.Options.with_api_key(
            api_key=os.environ["VIAM_API_KEY"],
            api_key_id=os.environ["VIAM_API_KEY_ID"],
        )
        return await RobotClient.at_address(os.environ["VIAM_MACHINE_FQDN"], opts)

    # self.robot_client initialized to None; create once, reuse:
    if not self.robot_client:
        self.robot_client = await create_robot_client_from_module()
    world_pose = await self.robot_client.transform_pose(obj_in_cam, "world")
    ```

  Note: exactly one client, reused; do NOT create a connection per call; do NOT hardcode credentials (operator sets `VIAM_API_KEY`, `VIAM_API_KEY_ID`, `VIAM_MACHINE_FQDN` in the module's environment config). Close it on shutdown with `await self.robot_client.close()`. Reference: <https://docs.viam.com/build-modules/platform-apis/#use-the-machine-management-api-from-a-module>
- **Bridge callout:** side-by-side `from_robot` (local script) vs. `cast + get_resource_name` (module); resource names are identical in both.
- **`do_command` + scheduled job.** Cloud build time (~1 min for Python modules) stated upfront.

**Verification:** run the four checks. `grep -n "FrameSystemClient" docs/tutorials/pick-and-place/06-inline-module.md` → **zero**. `grep -n "VIAM_MACHINE_FQDN\|create_robot_client_from_module" …` → hits.

**Commit:** `docs(tutorials): author Phase 6 inline module with corrected in-module RobotClient`

---

### Task 9: Final consistency sweep + full build

**Goal:** Cross-page consistency and a clean full-site build.

**Files:** all of `docs/tutorials/pick-and-place/`

**Step 1: Cross-page grep sweep (expect zero hits each)**

```bash
cd /Users/nick.hehr/src/viam-docs
grep -rniE "FrameSystemClient|point_cloud\.size|facilitator provides|pre-provisioned by instructor|sorted by color|red-bin|blue-bin|green-bin|does not exist yet|phase_total: 5|local-python-script" docs/tutorials/pick-and-place/
```

**Step 2: Confirm the six-phase chain**

```bash
grep -rn "phase:\|phase_total:\|prev:\|next:" docs/tutorials/pick-and-place/*.md
```

Verify: phases 1–6, all `phase_total: 6`, prev/next form the chain platform-mental-model → configure-resources → static-positions → control-the-robot-from-python → perception-guided-picking → inline-module.

**Step 3: The four pre-PR checks (verbatim, in order)**

```bash
cd /Users/nick.hehr/src/viam-docs
npx prettier --write "docs/tutorials/pick-and-place/**/*.md"
npx markdownlint-cli --config .markdownlint.yaml "docs/tutorials/pick-and-place/**/*.md"
vale sync && vale docs/tutorials/pick-and-place/
make build-prod
```

Expected: prettier reformats in place; markdownlint clean; vale reports no errors; `make build-prod` completes without errors (old-date warnings OK).

**Step 4: Browser spot-check (optional but recommended)**

```bash
pkill -f "hugo server"; rm -rf public/
hugo server --port 1313 --disableFastRender
```

Open each phase: `workshop-phases` box and sidebar show six phases in order with the current one highlighted; `workshop-nav` prev/next chains across all six; the `/tutorials/` landing card and `/tutorials/all/` archive are unaffected.

**Step 5: Commit any sweep fixes**

```bash
git add docs/tutorials/pick-and-place/
git commit -m "docs(tutorials): final consistency sweep for six-phase self-serve workshop"
```

---

## Out of scope (deferred)

- Companion-repo code changes (e.g. adding the home-pose guard clause to `reference-solution.py`).
- The hardware-setup how-to guide (`docs/guides/hardware-setup/xarm6-pick-and-place.md`).
- The `code-file` shortcode and `data/tutorials.yaml`.
- Header/hardware-overview imagery.
- Any change to the landing page, `/tutorials/all/` archive, or sidebar layout (2026-06-30 work).
