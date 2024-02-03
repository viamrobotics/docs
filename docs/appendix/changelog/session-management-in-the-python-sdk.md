---
title: Session management in the Python SDK
date: "2023-06-01"
color: "added"
---

The Python SDK now includes sessions, a safety feature that automatically cancels operations if the client loses connection to your machine.

[Session management](/build/program/apis/sessions/) helps you to ensure safer operation of your machine when dealing with actuating controls.
Sessions are enabled by default, with the option to [disable sessions](/build/program/apis/sessions/#disable-default-session-management).
