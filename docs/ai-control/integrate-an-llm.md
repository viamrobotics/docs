---
linkTitle: "Integrate an LLM"
title: "Integrate an LLM with a robot"
weight: 30
layout: "docs"
type: "docs"
description: "Build a logic module that uses an LLM to turn a high-level goal into a validated sequence of robot skills, then dispatches them through the Viam APIs."
---

Give a robot a high-level goal in plain language, such as "clear the cups off the table," and have it carry out a bounded sequence of actions: drive to the table, pick up a cup, place it in the bin, repeat.
A large language model (LLM) is well suited to decomposing that goal into steps.
Your module calls the LLM to propose which robot skills to run and with what arguments, validates each proposed action, and then dispatches the approved actions through the Viam APIs.

Viam does not host the LLM.
Your module calls an external LLM provider (such as an OpenAI-compatible API) or a local model that you run yourself, using that provider's own SDK.
Everything below is the code you write inside a [module](/build-modules/).

{{% alert title="Safety first" color="caution" %}}
An LLM produces unconstrained text.
Keep a validation layer between the model's proposed action and any [Viam API](/reference/apis/) call.
That layer admits only actions in a fixed allowlist, within fixed parameter bounds, so a malformed or out-of-range response never reaches an actuator.
Steps 4 and 5 cover this validation and the timeouts and human-confirmation gates that back it up.
{{% /alert %}}

## Prerequisites

- A machine with the components and services your robot uses (for example a [base](/reference/apis/components/base/) and an [arm](/reference/apis/components/arm/)), already [configured](/hardware/).
- Credentials for an LLM provider, or a local model you can query.
- Familiarity with [writing a module](/build-modules/).

## Author the logic module

1. **Scaffold a logic module.**
   Generate a [generic component or service](/build-modules/) module in your language of choice.
   A logic module holds no hardware of its own; it depends on the components and services it orchestrates and coordinates them.
   Declare those resources as [dependencies](/build-modules/dependencies/) so your module receives clients for them at runtime.

2. **Define a set of robot skills.**
   A skill is a small function that wraps one or more [Viam API](/reference/apis/) calls into a named, self-contained action.
   Give each skill a clear name, a short description, and a typed set of arguments.
   Keep the surface small and the arguments bounded.

   ```python {class="line-numbers linkable-line-numbers"}
   async def drive_to(self, zone: str):
       """Drive the base to a named zone in the workspace."""
       pose = self.zones[zone]                     # look up a known target
       await self.motion.move(...)                 # see the Motion API reference

   async def pick_cup(self):
       """Close the gripper on a cup at the current pose."""
       await self.gripper.grab()

   SKILLS = {
       "drive_to": {"zones": list(self.zones)},    # allowed values
       "pick_cup": {},
   }
   ```

   The `SKILLS` table is the allowlist.
   It is the single source of truth for what the robot can be asked to do and which arguments are legal.
   For exact method signatures, see the [component and service APIs](/reference/apis/).

## Prompt the LLM to choose a skill

3. **Ask the model to select a skill and arguments.**
   Send the goal and the skill definitions to your LLM provider using its function-calling (also called tool-use) API.
   That style constrains the response to a structured choice: a skill name plus arguments, rather than free-form prose you would have to parse.

   ```python {class="line-numbers linkable-line-numbers"}
   response = llm_client.chat(
       goal=goal,
       tools=self.skill_schemas,   # your SKILLS table as the provider's tool schema
   )
   proposed = response.tool_call   # e.g. {"skill": "drive_to", "args": {"zone": "table"}}
   ```

   The provider returns a proposed action.
   Treat it as a request, not a command: nothing runs until it passes validation.

## Validate before executing

4. **Check the proposed action against the allowlist and bounds.**
   Run this check on every proposed action, before any API call.
   This is the guardrail that keeps an LLM from issuing an unsafe actuator command.

   ```python {class="line-numbers linkable-line-numbers"}
   def validate(self, proposed):
       skill = proposed["skill"]
       if skill not in self.SKILLS:                 # reject unknown skills
           raise ValueError(f"unknown skill: {skill}")
       for name, value in proposed["args"].items():
           allowed = self.SKILLS[skill].get(name)
           if allowed is not None and value not in allowed:
               raise ValueError(f"{name}={value} out of bounds")
       return proposed
   ```

   Each rule maps to a specific failure it prevents:

   - The **allowlist** check admits only skills you wrote and tested, so a hallucinated or misspelled action name never becomes an API call.
   - The **parameter-bounds** check confirms every argument falls in a legal range, so an out-of-range value, such as a velocity above your safe cap, is refused before it reaches a motor.

   If validation fails, log the rejected action and either stop or ask the model to try again.
   A rejected action costs nothing; an unchecked one can move hardware.

## Execute through the Viam APIs

5. **Dispatch the validated action, with timeouts and optional confirmation.**
   Only actions that pass step 4 reach the Viam APIs.
   Two further guardrails bound what execution can do:

   - **Timeouts** bound each dispatched action in time, so a stalled or long-running motion returns control to your module instead of running unattended.
   - **Human confirmation** gates high-consequence skills, such as moving an arm near a person, on an explicit approval before the action runs.

   ```python {class="line-numbers linkable-line-numbers"}
   async def execute(self, action):
       action = self.validate(action)                      # never skip this
       if action["skill"] in self.CONFIRM_REQUIRED:
           if not await self.confirm(action):              # await a person's approval
               return
       async with asyncio.timeout(self.step_timeout_s):    # bound the action
           await self.skills[action["skill"]](**action["args"])
   ```

   Loop steps 3 through 5 until the goal is met or a step fails, feeding the outcome of each action back to the model as context for the next choice.

## Next steps

- For a worked example of driving a robot from an LLM, see [Integrate Viam with ChatGPT](/tutorials/projects/integrating-viam-with-openai/).
- To package and deploy your logic module, see [Build and deploy modules](/build-modules/).
- To review the exact methods your skills call, see the [component and service APIs](/reference/apis/).
