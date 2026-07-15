---
linkTitle: "AI assistant"
title: "Configure a machine with the AI assistant"
weight: 11
layout: "docs"
type: "docs"
description: "Configure components, services, and modules by describing the change to the AI assistant, then review and save each staged edit."
date: "2026-07-15"
---

On your machine's **CONFIGURE** tab, you can describe a configuration change in
plain language and have the **AI assistant** propose it for you, instead of
adding each resource through the form fields or writing the JSON by hand.
You type a request such as "Add a fake sensor named test-sensor", and the
assistant replies in a panel and stages the change in the Builder for you to
review. The change takes effect on your machine only when you click **Save**.

This page shows how to configure resources with the AI assistant, review each
staged edit, use the assistant on a fragment, and decide when to reach for it.

## What the AI assistant does

The **AI assistant** turns a plain-language request into a proposed
configuration change that you review before it takes effect.

- **Where it lives.** The assistant is available on the **CONFIGURE** tab for
  both machine configuration and [fragment](/hardware/fragments/)
  configuration, in the **Builder** and **JSON** config views (the config view
  toggle is labeled **Builder** / **JSON**). Open it from the **AI assistant**
  button (sparkle icon) at the bottom right of the Builder view. The assistant
  opens in a panel on the right side of the page.
- **What it can change.** From your request, the assistant adds, updates, or
  deletes components, services, modules, remotes, and triggers.
- **What it reads.** The assistant reads your current configuration (including
  unsaved edits and resolved fragments), your machine's status, its logs, and
  any validation errors, and uses them when it generates a proposal. For
  example, when you ask it to fix a problem, it reads the error the machine
  reported and proposes a change that addresses it.

The assistant stages every proposal for your review, and you save it or discard
it (see [Review each staged edit](#review-each-staged-edit-then-save-or-discard)).

The panel also has these controls:

- **New conversation** starts a fresh conversation.
- **Conversation history** reopens a past conversation. Conversations are saved,
  so you can return to earlier requests.
- **Collapse** hides the panel.
- **AI assistant feedback** opens a form where you can report how a response
  worked for you.

## Configure a resource by describing it

Use the assistant to add or change a resource when you can describe what you
want in plain terms.

1. Open your machine's **CONFIGURE** tab in the [Viam app](https://app.viam.com).
2. In the **Builder** view, click the **AI assistant** button (sparkle icon) at
   the bottom right. The panel opens on the right.
3. In the input field (placeholder **Describe a task or ask a question…**),
   type the change you want, then click **Send**. For example: "Add a fake
   sensor component named test-sensor."

When the panel is empty, it shows the heading **Let's start configuring** and
the prompt **What do you want to do?**, along with suggested starter requests
you can select instead of typing your own:

- **Add components to control my hardware**
- **Detect objects in a webcam feed**
- **Configure an arm to pick something up**
- **Help me fix the issues with my machine**
- **Learn Viam's basic concepts**

You can also ask a question rather than request a change. For example, ask the
assistant to explain what a component does before you add it.

After you send a request, the assistant replies in the panel and stages the
change: the new or updated resource appears in the Builder marked as modified.
For the request above, the assistant replies with a confirmation such as
"Added the fake sensor `test-sensor`. Save the config to apply it.", and the
sensor appears in the Builder, ready for you to review.

## Review each staged edit, then save or discard

A staged edit is a change the assistant has prepared for your review. You decide
whether it takes effect.

When the assistant stages a change, the config toolbar shows **Unsaved changes**
with **Save** and **Discard** controls:

1. Review the modified resource in the Builder. Confirm the model, name, and
   attributes match what you asked for.
2. To apply the change, click **Save** (or press **Cmd + S** / **Ctrl + S**).
   `viam-server` reloads the configuration and initializes the change. You do
   not need to restart anything.
3. To reject the change, click **Discard**. The staged edit reverts and your
   saved configuration is unchanged.

Because every proposal waits for you to save or discard it, you review each
change before it reaches your machine. You can also edit a staged resource by
hand in the Builder or in JSON before you save.

## Use the assistant on a fragment

The AI assistant is also available when you edit a
[fragment](/hardware/fragments/), a configuration you define once and apply to
every machine that uses it.

1. Open the fragment on the **CONFIGURE** tab.
2. Open the **AI assistant** and describe the change you want, the same way you
   would for a machine. The assistant stages the edit for you to review.

Changes you save to a fragment apply to every machine that uses the fragment on
its next config sync, so you can make a shared change once and let it propagate
across the machines that share the fragment.

## When to use the assistant instead of editing the configuration directly

Reach for the **AI assistant** when:

- You know what you want but not the exact model name or JSON structure. For
  example, "add a webcam" rather than searching for the `webcam` model yourself.
- You want to add more than one related resource in a single request.
- You want to fix an error the machine reported. The assistant reads the
  validation error or log and proposes a change that addresses it.
- You want to learn what a resource does before you add it.

Edit the configuration directly, through the form fields or in **JSON** mode,
when:

- You know the exact model and attributes you want to set.
- You are making a precise change to one attribute value.
- You are copying a configuration between machines or making bulk edits, which
  are faster in [JSON mode](/hardware/machine-configuration/#editing-configuration).

Because the assistant stages every change for review, you can start with a
request and then refine the result by hand before you save. The two approaches
edit the same configuration.

## What's next

{{< cards >}}
{{% card link="/hardware/machine-configuration/" %}}
{{% card link="/hardware/configure-hardware/" %}}
{{% card link="/hardware/fragments/" %}}
{{< /cards >}}
