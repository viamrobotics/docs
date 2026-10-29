---
title: "Phase 5: Deploy the policy to your robot"
linkTitle: "5. Deploy the policy"
type: "docs"
slug: "deploy-the-policy"
weight: 50
description: "Deploy the trained Cosmos policy and run it against the simulated workcell."
capabilities: ["ml-models", "hw-generic", "docs"]
diataxis: tutorial
workshop: "cosmos"
toc_hide: true
phase: 5
phase_total: 5
prev: "/tutorials/cosmos/train-your-policy/"
next: "/tutorials/cosmos/next-steps/"
languages: ["python"]
draft: true
---

You’re now ready to run a policy on your robot. If you’d rather test our prebuilt model, scroll to the ‘existing trained policy’ fast path below.

(TODO EMBED pick-blue-3002.mp4)

### Deploy

To run your post-trained policy:

1. First find your model in Data -> Models in the web UI. Hit the Deploy button, then follow the prompts to add this model to your robot. Initially, deploy to the same robot where you generated the training data (or an identical layout). (TODO MODEL PAGE SCREENSHOT)
1. Follow the prompts to add this model to your target robot.
1. This should result in a ‘generic-1’ instance on your robot’s Configure page. If you’ve renamed any of the components in the original ‘viam-labs/cosmos-tutorial’ fragment, ask your agent to update the config for generic-1, otherwise proceed.
1. Wait for the model to download. You can watch progress in the Logs tab.
1. Back on the Configure page, in the generic-1 component again, scroll down to the DoCommand panel.
1. Start the policy server by pasting in `{“command”: “policy_server”, “action”: “start”}` and hitting Execute. Keep this browser tab running so that the command isn’t interrupted. You’ll get an output in 30 or so seconds when it finishes starting up. This is managing NVIDIA’s upstream cosmos-framework runner under the surface.
1. In the <file>cosmos-tutorial/episodes</file> folder, run:

   ```sh
   uv run arm-policy-workflow <machine_address> --policy generic-1 --prompt "Pick up the block" --action-prefix-duration-sec 1.0 --world sim-world
   ```

   Or ask your agent to do this. If this fails to connect, make sure you ran the ‘grab credentials’ step above.

1. Open the Control page in a new browser tab, scroll down to the scene camera, switch it from ‘Refresh every second’ to ‘Live’ mode if you want, and watch as your policy is executed.
1. If you don’t see motion, switch back to the browser tab where your Configure page is running and look for errors. Paste errors into your agent if something goes wrong, and ask it to look at your robot’s logs as well.
1. You have now successfully run a world action model! Thank you for following along with us to the end.

## Fast path: existing trained policy

First, follow the instructions above to create a fresh robot with a running sim container and the ‘cosmos-tutorial’ fragment.

Then visit the [existing public trained model](https://app.viam.com/ml-model/viam/cosmos-xarm-pick) and click ‘Add to machine’. After that, follow the normal ‘Run the policy’ instructions above to get this model onto your fresh robot.

{{< workshop-nav >}}
