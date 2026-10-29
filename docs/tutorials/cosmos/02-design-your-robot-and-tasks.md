---
title: "Phase 2: Design your robot and tasks"
linkTitle: "2. Design your robot and tasks"
type: "docs"
slug: "design-your-robot-and-tasks"
weight: 20
description: "Design a simulated workcell and an oracle task for generating training data."
capabilities: ["machine-config", "scene-3d", "hw-arm", "docs"]
diataxis: tutorial
workshop: "cosmos"
toc_hide: true
phase: 2
phase_total: 5
prev: "/tutorials/cosmos/setting-up-your-environment/"
next: "/tutorials/cosmos/create-training-episodes/"
languages: ["python"]
---

In this phase you’ll use our agent skills to design a simple automation cell and a few tasks. In later phases you’ll [generate demonstration episodes](/tutorials/cosmos/create-training-episodes/), [train a policy](/tutorials/cosmos/train-your-policy/), and [run the policy](/tutorials/cosmos/deploy-the-policy/).

If you get stuck in this phase and want to skip ahead, or want to experiment with a completed solution, complete [Design your robot](#design-your-robot) through step 4 (installing the fragment), then continue with [Phase 3: Create training episodes](/tutorials/cosmos/create-training-episodes/).

## Design your robot

Your goal here is to create a simple automation cell with a single arm and the ability to perform one task. More advanced layouts are possible, but will require you to modify the action space of the policy.

Start by booting a simulator and installing the starter arm for this tutorial:

1. Create a fresh machine at app.viam.com to use for this. (A machine is an individual robot in our system). Use the ‘Simulate’ button to create a sim container for your robot; this is a GPU-enabled remote machine where your robot will run. (TODO HERE: IMAGE OF SETUP / SIMULATE)
1. The rest of these steps will be in your coding agent, but can be done from the web UI if you prefer.
1. In the terminal, start your agent in the cosmos-tutorial folder so that it has easy access to the scripts it will need.
1. Prompt your agent to install the `viam-labs/cosmos-tutorial` fragment on the new machine. A fragment, in our system, is a bundle containing multiple sub-objects; in this case an arm, table, the simulator logic, and toy blocks to pick up.
1. Wait for everything to start. You can watch progress in the Logs tab or ask the agent to monitor startup and ping you when done. This should take about 90 seconds after adding the fragment. You’ll know you’re done when you can visit the Control page and see a running robot below.
1. Now you have a fully running simulator. Switch to the Control tab and check out your robot. If you click ‘scene-cam’ resource on the left panel, you should see your scene: (TODO IMAGE OF SCENE)
1. Then switch the camera to ‘Live’ mode, pop it out using the browser’s picture-in-picture controls
1. Last, click the ‘pick-arm’ resource on the left panel. If you hit the ‘jog’ toggles on the arm controls, you should see the arm move in response. You can also ask the agent to do some sample motions for you.

## Save machine credentials

1. In the web UI, go to the page for the new machine you created, click the ‘Online’ dropdown, and click ‘Machine cloud credentials’ to copy what you need. (TODO IMAGE OF MACHINE CLOUD CREDENTIALS UI)
1. Paste that into /etc/viam.json on your laptop; the scripts will look for it there.

Now comes the fun part: designing the robot and task you want to train.

1. If you installed the Viam plugin during [Phase 1’s harness setup](/tutorials/cosmos/setting-up-your-environment/#harness-setup), your agent should automatically use the agent skills to guide you around hard edges. Just to be safe, ask it if it has access to `workcell-design` and the other Viam skills, and repeat the plugin installation if not.
1. Decide on a robot layout. A good prompt here is ‘Can you guide me through a basic workcell design?’. We recommend a single arm, ideally the UFACTORY Lite 6 we use in our demos, to start; if you plan to train a bimanual, non-6-DOF, or non-arm robot, that’s great! But bear in mind your agent will have to edit some training scripts. Ping us on discord if you try a different design and run into trouble.
1. As you design the robot, the agent will add and subtract components from the initial ‘cosmos-tutorial’ fragment. Try prompting it to add shelving or racks, clutter on the table, or colors and textures.
1. Decide on a task. Consider variations on picking up something, putting something somewhere, turning something, or selecting a specific object from a group. See [Design and run your task](#design-and-run-your-task) for more details.

The agent knows what to do here, can configure your machine, and can query logs and look at cameras if you run into trouble. You should manage it at whatever level you’re comfortable with.

## Design and run your task

At a high level, a ‘task’ is a series of commands that your policy will associate with a prompt. For example, ‘pick up the red block’ will move the gripper to a spot above the red block, descend, grip, and lift.

Frontier models are very good at the spatial reasoning required to get this right, and the visual reasoning required to evaluate your results; our agent plugin will route this kind of request to a larger model as needed.

You or your agent will write your tasks by modifying the <file>oracle_episode.py</file> script in the <file>cosmos-tutorial</file> repo. These are ‘oracle’ tasks in that they have perfect knowledge of the state of the simulation, and are not relying on vision or learned actions. The Cosmos model you train in [Phase 4](/tutorials/cosmos/train-your-policy/) will use these perfect-knowledge episodes to learn how to execute these tasks using vision.

{{< workshop-nav >}}
