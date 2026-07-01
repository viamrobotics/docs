# Viam Docs — Concept Gap Review

**Audience lens:** a software person with **no robotics background** learning to build a robotics product on Viam. The docs must teach _two_ things at once: the **platform** (how Viam is put together) and the **robotics concepts** underneath it. A "concept gap" here = something a newcomer must understand to succeed, but which no page defines — it is only assumed or scattered.

**Method:** we defined gaps as _blocked user jobs_, not missing pages, then asked of each core concept: does **one findable page own it**, or is it **scattered / missing**? A concept many pages _use_ but zero pages _own_ is the highest-value gap.

**Scope reviewed (now complete):** hardware components, set-up/onboarding, data, train, fleet, localization & navigation, build-modules, build-apps, tutorials, try/rover, cli, organization, monitor, and the glossary/SDK reference layer — plus a cross-cutting concept-ownership sweep. Every top-level docs section has now been reviewed.

**Caveat:** motion-planning and vision were excluded from _direct_ review because they are under active edit (vision was reviewed in an earlier pass). Several robotics concepts are currently _owned inside the motion-planning section_ — noted below — and that section is mid-restructure, so "owned there" is on shifting ground.

---

## 1. Headline: core robotics concepts and who owns them

Scored by whether the docs teach the concept to a newcomer. ("No owner page" = used across pages, defined in none.)

- **Localization — no owner page.** No page defines _how a robot knows where it is_, or compares odometry vs GPS vs SLAM (drift, indoor/outdoor, cost). Partial coverage exists (mobile-base world frame is explained inside motion-planning), but nothing carries the "localization" banner a newcomer would search for.
- **SLAM & mapping — missing.** Name-dropped in ~5 pages, defined nowhere. A newcomer can't learn what SLAM is, that it needs LIDAR, or how to run it.
- **Sensor fusion — missing.** Zero pages (grep: 0 hits). The `merged` movement sensor is failover/selection, _not_ statistical fusion — but "merged" invites a newcomer to assume fusion.
- **IMU / accelerometer / gyroscope / magnetometer — missing.** "IMU" is used in ~10 pages but "inertial measurement unit" appears **nowhere** in the repo (verified); what each sensor measures is never mapped to the API.
- **Real-time / control-loop rate / latency — no owner page.** Only appears as config fields (`control_frequency_hz`, `LoopFrequency`); nothing explains why loop rate matters.
- **Degrees of freedom — scattered.** "6-DOF arm" used before "DOF" is defined; the definition sits in one motion-planning sub-page.
- **Odometry — partial.** Defined as an "estimate," but **drift** and **dead reckoning** — the caveats that matter most — are never explained; the tick→distance→pose math is unowned.
- **Calibration — split.** Camera-intrinsics calibration is well owned (inside motion-planning); **sensor and motor calibration are effectively missing**; "calibration" as a general idea has no home.
- **Units & sign conventions — scattered.** No page states platform-wide conventions. Which way is positive for `Spin(90)`? Positive joint direction? deg/s vs rad/s? Base axis convention? Not stated where a newcomer meets them.

**The glossary confirms it.** Of 14 core concepts checked, the glossary owns exactly **one** (`component`). Missing entirely: pose, kinematics, PID, odometry, IMU, localization, SLAM, calibration, degrees of freedom, sensor fusion, waypoint, orientation vector, confidence score (verified by directory listing). Other sections _offload_ these terms to the glossary via tooltips — but the offload target is empty, so the tooltip resolves to nothing.

**Well-owned (for contrast):** coordinate frames, forward/inverse kinematics, closed-loop/PID mechanics, camera intrinsics, DoCommand (escape-hatch role), the connection model (WebRTC/gRPC/direct), sessions/reconnection, and the org→location→machine hierarchy. **Caveat:** the spatial/robotics owners all live _inside the motion-planning (arm) section_, which is mid-restructure — so a newcomer building a **mobile robot or a data product** may never find them.

---

## 1b. Correctness & safety flags (higher severity than concept gaps)

Two findings are not "missing explanation" — they are places the docs could lead a newcomer into an unsafe or insecure result. Flagging separately because they outrank the gaps.

- **Browser/mobile API keys are presented as secret when they are not.** `build-apps/concepts/authentication.md` frames environment variables as the security measure, but `build-apps/setup/typescript.md` puts the key in `VITE_API_KEY`, which Vite bundles into client JS shipped to every visitor's browser (same exposure for a distributed Flutter binary). Env-vars prevent source-control leaks but do **not** make the key secret at runtime — and neither page says so. A newcomer ships a live credential.
- **No teleop connection-loss / e-stop behavior is documented.** `monitor/teleop-workspaces.md` describes driving a physical robot remotely but never states what happens to a moving robot if the control link drops mid-command (command timeout? e-stop?). For a physically actuating machine this is a safety gap, not a docs nicety.

---

## 2. Platform mental-model gaps (onboarding / first run)

- **No conceptual on-ramp.** No single page teaches _machine → part → component/service → module/resource_; a newcomer assembles it from glossary fragments. `what-is-viam/_index.md` is capability-first, not model-first.
- **"Part" used before defined** in setup steps (`set-up-a-machine/first-machine.md`, `with-cli.md`); defined only in glossary.
- **Component vs. service is not taught.** "Component" is defined well; "service" is one glossary sentence, never contrasted side-by-side.
- **`set-up-a-machine/_index.md` is an empty stub** — no framing before the reader hits steps.
- **Terminology drift:** "machine" vs "smart machine" defined inconsistently.
- **"Module" defined 3 times** in different framings, no canonical page on the first-run track.
- **Unglossed prerequisites** dropped on newcomers: gRPC/WebRTC, the frame system, `depends_on` dependencies, config-JSON literacy (`rdk:component:<type>` triplets).

---

## 3. Section-specific concept gaps

### Hardware / components

- **Encoders:** quadrature 4× counting and PPR-vs-CPR-vs-`ticks_per_rotation` (classic newcomer trap) never explained; absolute vs incremental never taught.
- **Motors:** why a motor driver / H-bridge is needed never stated; brushed vs brushless used but undefined; steppers' open-loop step-loss risk unmentioned.
- **PID:** acronym never expanded; P/I/D deferred to one controls page.
- **Board / servo / gantry reference pages define nothing** — a newcomer isn't told what a board, servo, or gantry _is_.
- **Wiring basics:** PWM/GPIO expanded only on deep child pages; logic-power vs motor-power separation appears only in an image caption.
- **Arm:** forward/inverse kinematics, joint limits, reachable workspace, singularities only surface in troubleshooting asides.

### Data

- **Capture frequency vs sensor sample rate** never distinguished (capture Hz = how often the server polls, independent of the sensor's own rate).
- **No undersampling/aliasing concept** — only storage cost is framed.
- **Units of captured readings** never addressed (sensor-defined, not normalized by Viam).
- **Coordinate frame/units of spatial captures** (poses, point clouds, lat/long) assumed.
- **Time-series two-clock model** (`time_requested` vs `time_received`) given field-by-field but never explained.

### Train (ML for beginners)

- **"Model," "generalize," train/validation/test split, overfitting** used but never defined for a non-ML reader (overfitting symptoms given as tips without naming the concept).
- **Confidence score** central to deploy guidance but never defined (~0–1 certainty, not accuracy).
- **Train-in-cloud vs infer-on-device** implied but never stated.

### Fleet

- **"Machine part"** used throughout but never defined for someone with one machine.
- **Org → location → machine → part hierarchy** never laid out, yet keys/IDs/fragments depend on it.
- **Config inheritance / override precedence** underspecified.
- **Versioning** uses semantic-versioning ideas without introducing them; MongoDB `$set`/`$unset` override syntax leaned on without a plain-language model.

### Localization & navigation (most broken path)

- **Navigation how-to is gone** — the navigation service page is now a redirect to motion planning (verified); the "drive a base to a waypoint / GPS route" workflow has no replacement how-to.
- **No `move-a-base` how-to** exists (verified — arm and gantry have move pages, base doesn't). `MoveOnMap` / `MoveOnGlobe` _are_ documented in the motion service reference, but only there — not surfaced as a newcomer base-navigation path (and that reference sits in the motion-planning area under active edit).
- **GPS under-surfaced** — GPS is mentioned across several pages, but no built-in GPS movement-sensor model is documented in the component reference (drivers live in the registry), and no page owns outdoor/global positioning as a concept.
- **"Pose" and orientation vectors (`o_x/o_y/o_z/theta`)** used pervasively with no glossary entry or definition.
- **World-frame contradiction:** glossary calls the world frame "fixed/static," but for a mobile base it moves with the robot — a conflict a newcomer will hit.
- **The chain "movement sensor → pose in world frame → navigate to a goal" is never assembled end-to-end.**

### Build-modules (authoring your own components)

- **The script→module inversion of control is never stated.** In a client script _you_ connect and call the API; in a module _you_ implement the API and `viam-server` calls your code and owns its lifecycle. This mental flip — the exact jump a script-writer needs — has no owner (`build-modules/overview.md`).
- **Concurrency/thread-safety is unowned.** Go examples use `sync.Mutex` without explaining that the server calls your API methods concurrently with your background loop, so shared state must be guarded. A driver author hits races unwarned (`module-anatomy.md`).
- **Real hardware I/O is sidestepped** — the "driver" worked example reads an HTTP endpoint, never serial/I2C/GPIO, so someone building an actual sensor driver gets no bridge to hardware buses or blocking I/O (`write-a-driver-module.md`).
- **`ResourceName`, the reconfigure lifecycle, and `run.sh` entrypoint** are used before defined; "service vs component" is defined only deep in `advanced-patterns.md`.

### Build-apps (client / UI layer)

- **Components, services, "resources," parts, fragments are used but never defined** for a UI developer; nothing links to a primer (`build-apps/tasks/control-components.md`). A front-end dev told to call a "vision service" has nothing to read.
- **Control-command latency is unset** — every `motor.setPower` is a network round-trip; only video latency is discussed (`control-components.md`).
- **"Captured data is stale" is not stated** — a dashboard on `dataClient` queries data that had to be captured _and synced_ (minute-scale lag); the newcomer isn't told this isn't live history (`tasks/query-data.md`).
- _(Well-owned here: transport model, sessions/heartbeat, reconnection, RobotClient-vs-ViamClient, video streaming — good templates.)_

### Tutorials & Try-Viam (learn-by-doing)

- **The rover path is click-and-run, not concept-teaching** — `drive-rover.md` uses `spin`/`move_straight` but treats the base as a black box (no odometry, no "how does spin know the angle"). Deep concepts appear only in Intermediate tutorials that already assume the vocabulary.
- **No beginner progression** — the tutorials landing is a filterable card grid (~35 projects), not a sequenced path; prerequisites are stated inconsistently.
- **Positive models to replicate:** the Gazebo Try path (`try/part-1..5`) with expandable "What's a component?" / "What happened behind the scenes" callouts, and `tutorials/get-started/blink-an-led.md` (teaches GPIO, resistor, LED polarity with _why_). These are the house style the concept-gap pages should copy.
- **Minor freshness:** `tutorials/configure/configure-rover.md` JSON still uses legacy `"model": "pi"` while its own prose says use `viam:raspberry-pi:rpi`/`pi5`.

### CLI / Organization / Monitor (ops & admin)

- **Component jargon hits non-robotics readers cold** — `monitor/overview.md` and `teleop-workspaces.md` say "move bases," "base actuation widget" as plain text; a software newcomer doesn't know a "base" is a wheeled platform.
- **CLI-vs-SDK boundary undrawn** — `cli/overview.md` says the CLI does "everything you can do in the app" but never mentions the SDK, so a scripting-minded newcomer may try to script robot _control_ via CLI (the SDK's job).
- **RBAC is defined via app-UI tabs** (CONTROL/CONFIGURE/LOGS/CONNECT) that are introduced in a different section — an ordering gap for someone reading admin docs first.
- _(Well-owned here: the org→location→machine hierarchy and diagram — this is the single source of truth other sections correctly defer to.)_

---

## 4. Recommended priorities (for discussion)

0. **Fix the two correctness/safety flags first** (Section 1b) — they can produce an insecure app or an unsafe robot, which outranks any missing explanation. Cheap to fix: one honest paragraph each.
1. **Create owner pages for the genuinely-missing robotics concepts** — a short "concepts" home each for **localization, sensor fusion, IMU/movement-sensor types, SLAM**. Highest value: load-bearing and currently absent.
2. **Lift the arm-coupled concepts up a level** — frames, kinematics, PID, calibration are well written but buried in motion-planning; a rover or data-product builder can't find them. Give them a section-neutral home and link in.
3. **Add a single platform on-ramp** — one "how Viam fits together" page teaching machine → part → component/service → module _before_ the setup steps; define "part" and "service" where first used. Bridge the **script → module inversion of control** here too.
4. **Fix the broken base-navigation path** — restore or replace `move-a-base`, surface GPS + `MoveOnMap`/`MoveOnGlobe` as a newcomer path, define "pose."
5. **Seed the empty glossary** — add real entries (or link-through stubs) for the 13 missing concepts so the tooltips other sections already point at actually resolve. Low effort, broad reach.
6. **Replicate the teaching patterns that already work** — the Gazebo Try callouts and `blink-an-led` (concept + _why_, not just steps) are house style; use them for the new concept pages instead of inventing a format.
7. **Add newcomer definitions inline** for the cheap, high-frequency traps — PID acronym, DOF, quadrature/encoder counts, confidence score, capture-rate vs sample-rate, units & sign conventions, and the component vocabulary (base/arm/gripper) where a non-robotics reader meets it.

**The repeatable test behind all of this:** a concept that many pages _use_ but zero pages _own_ is your highest-value gap. Localization, sensor fusion, and IMU each fail that test today.
