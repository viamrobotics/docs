---
title: "Phase 4: Train your policy"
linkTitle: "4. Train your policy"
type: "docs"
slug: "train-your-policy"
weight: 40
description: "Submit and monitor a Viam training job that post-trains Cosmos 3 Edge on your episodes."
capabilities: ["ml-training", "datasets", "cli", "docs"]
diataxis: tutorial
workshop: "cosmos"
toc_hide: true
phase: 4
phase_total: 5
prev: "/tutorials/cosmos/create-training-episodes/"
next: "/tutorials/cosmos/deploy-the-policy/"
languages: ["python"]
draft: true
---

In this phase you’ll use the [demonstration episodes you recorded in Phase 3](/tutorials/cosmos/create-training-episodes/) to post-train a robot policy. At the end of this step you'll have a motion policy based on NVIDIA's Cosmos 3 Edge world model, but specialized for your task and your simulated workcell. If you’d rather skip the training steps and try an action policy created by Viam, use the [existing trained policy fast path](/tutorials/cosmos/deploy-the-policy/#fast-path-existing-trained-policy).

The training script lives in the <file>training/</file> folder of the <file>cosmos-tutorial</file> repo. You won’t have to modify anything in here as long as your robot is a 6-DOF arm with a gripper. If you built something more complex (multi-arm, hands, etc), ask your agent to modify the action space in the training script and the policy runner in the [deployment phase](/tutorials/cosmos/deploy-the-policy/).

For this step you’ll also need our CLI:

1. Install it from the [Viam CLI installation instructions](https://docs.viam.com/cli/overview/#install).
1. Then run `viam login` in your terminal and follow the login flow in your browser.

## Submit the job

To submit a robot policy training job, in any folder on your terminal, fill in the two ‘xxxx’ fields in the snippet below and run it in your shell. Your agent can also do this.

```sh {class="wrap"}
# Submit your training job.
# This takes 30 minutes to several hours and costs money; see 'Setting iterations' below.

MODEL_NAME=cosmos-edge-lite6 # up to you
ITERS=10 # see 'Setting iterations' below
CONTAINER_ID=08d4a43e-f7c2-4463-83ef-67f836ac5ae9 # this is the common base container defined in the cosmos-tutorial repo
ORG_ID=xxxx # get this from the web UI (your org -> settings) or from running `viam org list` on the CLI
DATASET_ID=xxxx # you can find this in the Data -> Datasets section of the UI, or ask your agent. It's 'Copy Dataset ID' in the 3-dot menu

viam train submit custom from-registry --dataset-id $DATASET_ID --org-id $ORG_ID \
    --model-name $MODEL_NAME --script-name 6efeb7e5-91aa-4187-8ed3-e84764726078:cosmos-edge-7d \
    --version 0.1.1 --container-id $CONTAINER_ID \
    --args max_iter=$ITERS,dataset_id=$DATASET_ID

# you can view your in-progress job at https://app.viam.com/models
```

The training jobs run on Viam hosted hardware and it will bill your Viam account by the minute once you exceed our free tier. See [How to set training iterations](#how-to-set-training-iterations) for approximate runtimes.

If you’ve modified the robot cell enough to need a new action space (that is, a non-6-DOF arm or other changes to the number of dimensions in the control policy), you’ll need to modify the training script in cosmos-tutorial and upload a custom one. There are instructions for this in the `cosmos-tutorial/cosmos_train/README.md` and your agent can help.

## How to set training iterations

The training script’s defaults are set for a 6-DOF arm with around 100 episodes. The one setting you need to choose is the number of iterations; everything else is optional.

You set this with `max_iter`, the `ITERS` variable in the [submit command](#submit-the-job). Training takes time and costs money, so it pays to build up to a full run. We recommend working up in steps, each checking something before you spend more on the next:

- 10 iterations (about 15–20 minutes) to check that your dataset and the script work end to end.
- Optional: 50 iterations (about 35 minutes) to try deploying your own policy. It won’t complete your task, but you can see the arm move under its control.
- Optional: 500 iterations (about 4 hours) to see how training is going: the arm should move with purpose toward the task, though it will likely still fail often.
- 1,500 iterations for about 100 episodes (about 12 hours) for a usable policy. Scale it with your data: double the episodes, double the iterations. Don’t stop early: in our internal use, the model keeps improving through the end of these runs.

When your training job finishes, or if it fails, you’ll get an email notification.

{{< workshop-nav >}}
