---
title: "Phase 10: Score a Yahtzee roll"
linkTitle: "10. Score a Yahtzee roll"
weight: 100
type: "docs"
layout: "docs"
slug: "score-a-yahtzee-roll"
description: "Write an inline module in the Viam app that reads a settled roll of five dice from the vision service and returns its Yahtzee scores."
capabilities: ["inline-modules", "vision-service"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 10
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/deploy-the-winning-model/"
next: "/tutorials/dice-vision/wrap-up/"
toc_hide: true
---

At the end of this phase, a Yahtzee scorer runs on your machine.
You send it a command, and it reads the five dice through `dice-detector` and returns what the roll scores in each Yahtzee category.
This is where your model stops being a number on an evaluation page and starts doing a job.

## What you're building {#what-youre-building}

You write the scorer as an inline module.
A module is code that `viam-server` runs as part of your machine, the same way it runs the webcam driver and the ML model service you deployed in [Phase 9](/tutorials/dice-vision/deploy-the-winning-model/).
An inline module is one you write in a code editor in the Viam app.
When you save, Viam stores your code and deploys it to your machine, so you don't need a terminal, a local Python install or an API key.

Your module is a generic service: a service with no fixed set of methods of its own.
You run it by sending it a command, a small piece of JSON such as `{"score": {}}`, from the **TEST** section of its card.
Its `do_command` method reads the command and decides what to do.

The module doesn't connect to the machine; it's already part of it.
Instead, you tell it which resources to use in its configuration, and `viam-server` hands them to it when it starts.

## Create the module {#create-the-module}

1. On the **CONFIGURE** tab, click **+** and select **Code**.
1. Select **Viam-hosted** and click **Choose**.
1. Read the **Before you write code** checklist and click **Proceed**.
   You've already done both things it lists: configured the camera and the vision service, and tested them.
1. Name the module `yahtzee`, select **Python**, and click **Create module**.

The Viam app adds a generic service to your machine and opens its card with a code editor.
The editor holds a template with three methods to fill in: `validate_config`, `new` and `do_command`.

{{< checkpoint >}}
The **CONFIGURE** tab shows a new service with a code editor, and the code starts with `from typing import ClassVar`.
If you don't see the editor, click the new service in the list on the left.
{{< /checkpoint >}}

## Write the scorer {#write-the-scorer}

The code goes in two places in the template.

First, add the scoring code above the class.
Find the line that starts with `class MyGenericService` and paste this code above the comment block just before it:

```python
import asyncio
from collections import Counter

from viam.services.vision import VisionClient

SETTLED_READS = 4  # matching reads in a row, about one second
MAX_READS = 40  # give up after about 10 seconds
UPPER = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]


def score(dice):
    counts = sorted(Counter(dice).values(), reverse=True)
    faces = set(dice)
    total = sum(dice)
    scores = {}
    for face, name in enumerate(UPPER, start=1):
        scores[name] = face * dice.count(face)
    scores["Three of a kind"] = total if counts[0] >= 3 else 0
    scores["Four of a kind"] = total if counts[0] >= 4 else 0
    scores["Full house"] = 25 if counts == [3, 2] else 0
    small = any({s, s + 1, s + 2, s + 3} <= faces for s in (1, 2, 3))
    scores["Small straight"] = 30 if small else 0
    scores["Large straight"] = 40 if faces in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0
    scores["Yahtzee"] = 50 if counts[0] == 5 else 0
    scores["Chance"] = total
    return {name: points for name, points in scores.items() if points}
```

The `score` function works out every category's points for five dice, and returns only the categories worth more than zero.

Next, replace the methods.
Keep the `class MyGenericService` line and the `MODEL` line below it exactly as they are; Viam uses them to identify your module.
Select everything after the `MODEL` line, to the end of the file, and replace it with this code:

```python
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        attrs = struct_to_dict(config.attributes)
        for name in ("detector", "camera"):
            if not isinstance(attrs.get(name), str) or not attrs[name]:
                raise ValueError(f"attribute '{name}' is required")
        return [attrs["detector"]], []

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        self = super().new(config, dependencies)
        attrs = struct_to_dict(config.attributes)
        self.detector = dependencies[VisionClient.get_resource_name(attrs["detector"])]
        self.camera = attrs["camera"]
        return self

    async def read_dice(self):
        detections = await self.detector.get_detections_from_camera(self.camera)
        return sorted(int(d.class_name) for d in detections)

    async def read_settled_roll(self):
        last, matches = None, 0
        for _ in range(MAX_READS):
            dice = await self.read_dice()
            matches = matches + 1 if dice == last else 1
            last = dice
            if matches == SETTLED_READS:
                return dice
            await asyncio.sleep(0.25)
        return None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        if "read" in command:
            return {"dice": await self.read_dice()}
        if "score" in command:
            dice = await self.read_settled_roll()
            if dice is None:
                return {"error": "The dice didn't settle. Keep them still and try again."}
            if len(dice) != 5:
                return {"dice": dice, "error": f"I see {len(dice)} dice. Reroll so all five show."}
            return {"dice": dice, "scores": score(dice)}
        raise ValueError('Send {"score": {}} or {"read": {}}.')

    async def get_status(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, ValueTypes]:
        return {}
```

Here's what each part does:

- `validate_config` checks the module's configuration for two names: `detector`, the vision service to read from, and `camera`, the camera it reads. It returns `detector` as a dependency, so `viam-server` starts the module only after `dice-detector` is running.
- `new` runs when the module starts. It looks up `dice-detector` in the dependencies `viam-server` passes in, and keeps it for later.
- `read_dice` asks the vision service to take an image from the camera and run the model on it. Each detection's `class_name` is the label you drew in [Phase 2](/tutorials/dice-vision/label-the-starter-set/), `1` through `6`, and the vision service has already dropped boxes below your confidence threshold.
- `read_settled_roll` handles dice that are still rolling, which read differently in each image. It reads the dice every quarter of a second and returns a roll only when four reads in a row agree. If the dice don't settle within about 10 seconds, it gives up.
- `do_command` runs a command. `{"read": {}}` returns what the model sees right now. `{"score": {}}` waits for a settled roll and, if it sees exactly five dice, returns their scores. A sixth box usually means a misread or an extra die in view.

## Configure and save {#configure-and-save}

1. In the module's service card, find its attributes and replace them with:

   ```json
   {
     "detector": "dice-detector",
     "camera": "camera"
   }
   ```

1. Click **Save**.

Saving deploys your code to the machine.
Python inline modules run from source, so there's no build step; the module starts as soon as the machine receives it.

{{< checkpoint >}}
After a few seconds, the service shows no error on the **CONFIGURE** tab.
If it shows an error, open the **LOGS** tab and read it.
An error about an attribute being required means the attributes don't match the JSON above.
A Python error with a line number usually means part of the code was pasted in the wrong place; check that the `MODEL` line is still there and that the pasted methods are indented under the class.
{{< /checkpoint >}}

## Score a roll {#score-a-roll}

1. Roll five dice onto the background.
1. In the module's service card, open the **TEST** section and expand **DoCommand**.
1. Enter `{"read": {}}` and click **Execute**.
1. Check that the five values match the dice.
1. Enter `{"score": {}}` and click **Execute**.

{{< checkpoint >}}
For a roll of `3 3 3 5 5`, `{"score": {}}` returns:

```json
{
  "dice": [3, 3, 3, 5, 5],
  "scores": {
    "Threes": 9,
    "Fives": 10,
    "Three of a kind": 19,
    "Full house": 25,
    "Chance": 19
  }
}
```

If it returns an `error` saying it sees fewer or more than five dice, run `{"read": {}}` to see what it reads, or check the `dice-detector` test panel.
If it says the dice didn't settle, keep them still and run it again.
{{< /checkpoint >}}

## Count how often it scores correctly {#count-how-often-it-scores-correctly}

Your evaluation in [Phase 8](/tutorials/dice-vision/evaluate-both-models/) measured boxes.
This test measures what you care about: whole rolls.

1. Roll 10 times, running `{"score": {}}` after each roll.
1. For each roll, check the returned `dice` against the dice, and count the rolls where all five values are right.

Expect this number to be lower than the recall from Phase 8.
Recall counts each die on its own, but a roll is right only when all five dice are right at once.
If the model reads each die correctly 95% of the time, the chance that it reads all five correctly is 0.95 multiplied by itself five times, about 77%.
A stray extra box also makes a roll wrong, so the real number can be lower still.

{{< checkpoint title="Milestone" >}}
A Yahtzee scorer built on your own trained model runs on your machine as a module.
Write down how many of the 10 rolls it read correctly.
A model with 95% recall gets about 7 or 8 right, and a different 10 rolls can easily come out one or two higher or lower.
If it got 5 or fewer, look at which faces it got wrong, and compare them with the per-class breakdown from [Phase 8](/tutorials/dice-vision/evaluate-both-models/#compare-the-results).
{{< /checkpoint >}}

{{< workshop-nav >}}
