# Concept coverage analysis: 50 IoT/robotics use-cases

This branch adds four documentation sections that close concept gaps found by running a **use-case → concept coverage** analysis (Playbook 11) over 50 real IoT and robotics product use-cases. This README records the use-cases, the method, and the measured gap closure.

**Spreadsheet (full matrix, per-task concepts, gaps, learning objectives, before/after):** [`playbook11-use-case-coverage.xlsx`](https://drive.google.com/drive/folders/1ErpNHevOAVc_4YwqYM_dpG960QeAaLmA) (in the shared Drive folder).

## Method

1. Decompose each use-case into the platform + robotics concepts a user must understand to succeed.
2. Ownership sweep: for each concept, does one findable page **own** (define) it, or is it scattered/missing/buried? (grep-grounded against the docs + RDK source).
3. Turn gaps into target pages with a Diátaxis type, write learning objectives, then draft the pages.
4. Re-run the sweep to measure gap closure.

## Gap closure (63 concepts)

| Coverage | Before | After |
|---|---:|---:|
| OWNED | 29 | 46 |
| PARTIAL | 10 | 10 |
| BURIED | 7 | 7 |
| SCATTERED | 3 | 0 |
| MISSING | 14 | 0 |
| **No-owner gaps (MISSING+SCATTERED)** | **17** | **0** |

The 7 BURIED concepts (kinematics, frames, motion-planning) stay deferred: they are owned inside the motion-planning section, which is under active edit.

## New sections in this PR (19 pages)

- **`docs/concepts/`** — platform model, confidence scores, inference latency, capture frequency vs sample rate
- **`docs/ai-control/`** — learned & policy-based control, run a VLA, integrate an LLM, simulation & sim-to-real
- **`docs/navigation/`** — localization, SLAM & mapping, navigate a mobile base, sensor fusion, coordinate a fleet
- **`docs/manipulation/`** — force & compliance control, track & pick moving objects

## The 50 use-cases

| # | Category | Use case | Job |
|---|---|---|---|
| 1 | VLA / foundation-model control | VLA bin picking | Prompt a manipulator in natural language to pick a named item from a mixed bin |
| 2 | VLA / foundation-model control | NL task commanding | Command an arm with 'put the red block in the box' and have it execute |
| 3 | VLA / foundation-model control | Open-vocab perception | Detect arbitrary, un-trained objects from a text prompt on a robot camera |
| 4 | VLA / foundation-model control | LLM task planner | Use an LLM to decompose a goal into robot skills and dispatch them |
| 5 | VLA / foundation-model control | VLA mobile manipulation | A mobile manipulator tidies a room from a spoken instruction |
| 6 | VLA / foundation-model control | Voice-to-action control | Drive a robot by voice command with speech + a VLA policy |
| 7 | Policy-based / learned control | RL locomotion | Deploy an RL-trained gait policy on a legged/wheeled base |
| 8 | Policy-based / learned control | Imitation assembly | Teach an assembly skill from demonstrations and replay it |
| 9 | Policy-based / learned control | Visuomotor grasp policy | Run a learned pixel-to-action grasping policy in a loop |
| 10 | Policy-based / learned control | Sim-to-real transfer | Train a control policy in sim and deploy it on hardware |
| 11 | Policy-based / learned control | MPC mobile base | Run model-predictive control for smooth base trajectory tracking |
| 12 | Policy-based / learned control | Force-control insertion | Adaptive force policy for peg-in-hole insertion |
| 13 | Mobile robots / AMR | Warehouse AMR | Goods-to-person transport AMR navigating a mapped warehouse |
| 14 | Mobile robots / AMR | Outdoor delivery | GPS-navigated last-yard delivery robot on sidewalks |
| 15 | Mobile robots / AMR | SLAM cleaning robot | Indoor robot builds a map and cleans coverage-complete |
| 16 | Mobile robots / AMR | Multi-robot fleet coord | Coordinate a fleet of AMRs to avoid deadlock and share tasks |
| 17 | Mobile robots / AMR | Inventory scanning rover | Autonomous rover scans shelves and reports stock |
| 18 | Mobile robots / AMR | Person-following cart | A cart follows a worker through a facility |
| 19 | Mobile robots / AMR | Field-scouting rover | Ag rover autonomously scouts rows and geo-tags findings |
| 20 | Industrial manipulation | Machine tending | Arm picks molded parts, vision QC, sorts good/reject into bins |
| 21 | Industrial manipulation | Palletizing | Arm stacks boxes onto a pallet in a computed pattern |
| 22 | Industrial manipulation | Vision-guided kitting | Assemble a kit by picking parts located by vision |
| 23 | Industrial manipulation | Conveyor tracking pick | Pick moving parts off a running conveyor |
| 24 | Industrial manipulation | Dispensing path follow | Follow a Cartesian path for glue/weld dispensing |
| 25 | Industrial manipulation | CNC loader tending | Load/unload a CNC with force-sensed insertion |
| 26 | Industrial manipulation | Random bin picking | Pick randomly-oriented parts using 3D pose estimation |
| 27 | Fleet management / ops | Zero-touch provisioning | Provision 1,000 new devices with no per-unit manual setup |
| 28 | Fleet management / ops | Staged model rollout | Roll a new ML model to a fleet in canary then full stages |
| 29 | Fleet management / ops | Fleet config via fragments | Manage shared config across many machines with fragments |
| 30 | Fleet management / ops | RBAC for customer fleet | Grant scoped access to customers over their own machines |
| 31 | Fleet management / ops | Fleet health monitoring | Dashboard + alerts on fleet health and offline devices |
| 32 | Fleet management / ops | Remote teleop intervention | Remotely take control of a stuck robot to recover it |
| 33 | Fleet management / ops | Scheduled maintenance jobs | Run recurring jobs (calibration, logs) across a fleet |
| 34 | Fleet management / ops | White-labeled billing | Bill end customers under a partner brand for fleet usage |
| 35 | IoT sensing / monitoring | Cold-chain monitoring | Monitor temperature across assets and alert on excursions |
| 36 | IoT sensing / monitoring | Predictive maintenance | Vibration sensing to predict equipment failure |
| 37 | IoT sensing / monitoring | Air-quality network | Network of air-quality sensors reporting to the cloud |
| 38 | IoT sensing / monitoring | Smart-building occupancy | Occupancy + energy sensing for building automation |
| 39 | IoT sensing / monitoring | Utility meter aggregation | Edge-aggregate meter reads and sync upstream |
| 40 | IoT sensing / monitoring | Equipment anomaly detect | Detect leaks/anomalies on industrial equipment at the edge |
| 41 | Computer vision apps | Line defect detection | Detect product defects on a production line and reject |
| 42 | Computer vision apps | PPE compliance | Monitor a site for PPE compliance and alert |
| 43 | Computer vision apps | Access-control camera | License-plate / face access control at a gate |
| 44 | Computer vision apps | Shelf-stock analytics | Analyze retail shelves for out-of-stock |
| 45 | Computer vision apps | Queue/people analytics | Count people and measure queue length |
| 46 | Data / ML pipeline | Capture+sync for training | Continuously capture and sync robot data to build datasets |
| 47 | Data / ML pipeline | Auto-retraining loop | Detect model drift and retrain/redeploy automatically |
| 48 | Data / ML pipeline | Custom training script | Train a specialized model with a custom script on Viam data |
| 49 | Data / ML pipeline | Edge inference + upload | Run inference at the edge and conditionally upload hard cases |
| 50 | Data / ML pipeline | Sensor-data BI dashboard | Query and visualize fleet sensor data for business insight |
