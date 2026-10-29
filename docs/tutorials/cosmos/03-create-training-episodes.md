---
title: "Phase 3: Create training episodes"
linkTitle: "3. Create training episodes"
type: "docs"
slug: "create-training-episodes"
weight: 30
description: "Generate, review, and refine randomized demonstration episodes for policy training."
capabilities: ["data-capture", "datasets", "sequences", "docs"]
diataxis: tutorial
workshop: "cosmos"
toc_hide: true
phase: 3
phase_total: 5
prev: "/tutorials/cosmos/design-your-robot-and-tasks/"
next: "/tutorials/cosmos/train-your-policy/"
languages: ["python"]
draft: false
---

(TODO: IMAGE OF EPISODE GRID)

Now that you have a working robot and task, your next step is to collect randomized episodes to train on. If you’d rather skip ahead and see a working model post-trained by Viam, use the [existing trained policy fast path](/tutorials/cosmos/deploy-the-policy/#fast-path-existing-trained-policy).

Next to <file>oracle_episode.py</file> you should find <file>batch_episodes.py</file>; this will let you run tens of random copies. You may be able to use this with no changes. If you added new settings while you [designed the task in Phase 2](/tutorials/cosmos/design-your-robot-and-tasks/#design-and-run-your-task), the agent will need to update <file>batch_episodes.py</file> to pass them through.

Start by creating a short sample dataset:

1. Ask the agent to create a sample dataset of 5 episodes and pull down the episodes so it can evaluate them and so you can watch the videos. (You can also `uv run batch_episodes.py` with a `--count` and `--dataset` argument if you prefer)
1. Wait for the runs to complete. You can watch them execute on the control page in your web UI.

(A dataset in Viam is a collection of items used for training an ML model; they’re stored in our backend and accessible through the UI and SDKs).

Once this works to your satisfaction, we suggest post-training on 100 episodes for a usable policy. To begin with, start with 10 for a faster iteration loop.

There is some nuance in creating a good dataset, but the episode scripts and the episode-capture skill in our agent plugin have good defaults and guardrails to steer you towards something usable.

Your high-level steps for managing this process are:

1. By eye or through your agent, make sure that most of your episodes are succeeding. After the agent downloads your dataset, you should watch all 3 cameras for the first episode, and the scene camera for a few more.
1. If you’ve modified the workcell or task, it’s likely that some episodes will fail at first. Issues you’ll hit: positioning logic, workcell layouts that prevent the robot from reaching a target, moving too fast or too slow, physics settings causing the object to slide out of the gripper. The agent can fix most things by itself, but if the layout of the workcell looks obviously wrong to you, tell it what adjustments to make.
1. The episode runner has a success tracker built in so that bad episodes aren’t used for training, and it’s okay if a few fail. But if many fail, it’s likely a workcell issue and your post-trained motion policy will fail in the same way. Keep generating batches of 10 episodes, and adjusting, until you can run 10 episodes with 9 or 10 successes.
1. Next, make sure your episodes have random start points, random pick and target locations, and some small random noise in the arm’s motion, so the policy sees the arm drift off course and correct itself. The base oracle_episode.py has patterns for this, and the agent knows to follow them, but you should check as well. Inspect a few episode videos and eyeball that the arm is at a different place each time at the beginning of the video, and that the object to pick is in a different place, ideally with a different rotation. If there’s clutter, randomize that as well.

You don’t need to generate a full 100 episodes yet if you’re just testing the end-to-end flow. You can create 10 or so and submit the dataset for a short training session in [Phase 4](/tutorials/cosmos/train-your-policy/).

{{< workshop-nav >}}
