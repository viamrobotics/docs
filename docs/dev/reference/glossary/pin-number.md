---
title: Pin Number
id: pin-number
full_link:
short_description: A pin number is the index of the pin on the board. Not the same as a pin's GPIO number.
---

A pin number is the physical index of a pin on a {{< glossary_tooltip term_id="board" text="board" >}}.

This number is distinct from the GPIO number assigned to general purpose input/output (GPIO) pins.
For example, pin number "11" on a NVIDIA Jetson Nano is GPIO "50", and pin number "11" on a Raspberry Pi 4 is GPIO "17".
When Viam documentation refers to pin number, it will always mean the pin's physical index and not GPIO number.

Pin numbers are found on a board's pinout diagram and data sheet.
