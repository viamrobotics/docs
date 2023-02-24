---
title: "Testing Vale for Viam"
linkTitle: "How does Vale help Viam's Docs?"
weight: 1
type: "docs"
description: "A high-level overview of the benefits of Vale for Viam's Docs."
---

Vale[^vale] is a syntax-aware linter for prose built with speed and extensibility in mind.
To ensure consistency and adherance to the style guide across the Viam Docs, we have confirgured a set of vale rules.

## Examples of rules

### Testing plurals

Plural(s) with parentheses generate errors.

### Testing Latin abbreviations and words

Examples of latin abbreviations and words include:

- e.g. which stands for Exempli gratia meaning for example
- i.e. which stands for id est meaning that is
- via which translates to path but is frequently used in its ablative case indicating movement

Did you know that _viam_ is the accusative case of the word via marking the noun as the direct object of a transitive verb?
A transitive verb is a verb that uses a direct object, which shows who or what receives the action in a sentence.
Therefore, in Latin _viam_ might be used when you say "I see the path".

### Substitution Suggestions

When you say in the website or Scuttlebot you do not get to merge!
Exclamations are also frowned upon but they only generate a warning.

## More information about Vale

You can see all the rules that Viam's linter is applying in this repo by exploring the styles folder.
If there are any rules you think we should remove or change, create an issue or chat with the team.
If there are any you'd like to add, create an issue or a pull request.

Of course, use your best judgement on all of the guidance the Vale rules provide. For example, using 'is' is not always bad - but when seeing the warning just consider if there is a better alternative.

[^vale]: <a href="https://github.com/errata-ai/vale" target="_blank">Vale</a>
