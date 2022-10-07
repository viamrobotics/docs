---
title: "Learning Resources"
linkTitle: "Learning Resources"
description: "A collection of links to external sources discussing robotics topics which we believe users may find helpful."
type: "docs"
---
# Overview
The following sections contain links that we think you will find very useful during your journey into robotics.

## Basic Electronics
### Resistors
<a href="https://goodcalculators.com/resistor-color-code-calculator/" target="_blank">Online Resistor Color Code Calculator</a>[^orccc] - Enter the desired resistor value in Ohms, kOhms, or MOhms, and press enter and this site will display the color bands for that resistor value.

[^orccc]: Online Resistor Color Code Calculator: <a href="https://goodcalculators.com/resistor-color-code-calculator/" target="_blank">https://goodcalculators.com/resistor-color-code-calculator/</a>

**Resistor Value Chart**
<img src="../img/resistor.png" alt="Chart of standard colors to values for electronic components. An example resistor with green, red, and orange bands is shown. The value is 52 times 10 to the third power, or 52,000 Ohms." />

You can easily learn resistor color markings without referring to a chart by remembering this jingle:

"Badly Burnt Resistors On Your Ground Bus Void General Warranty."

Now, equate the jingle to the colors in this order:
Black, Brown, Red, Orange, Yellow, Green, Blue, Violet, Gray, White

And their values on a resistor:
0, 1, 2, 3, 4, 5, 6, 7, 8, 9

- The bands 1 and 2 indicate the first two significant digits on a resistor. 
- Band 3 is a multiplier on four-band resistors. 
For example, a resistor with brown, green, orange bands representing, 1, 5, and  3, respectively, which equates to 15 times ten to the third, or 15,000 Ohms, or 15 kOhms.
- On resistors with four bands, the band 4 indicates tolerance, with gold being +/- 5% and silver being +/- 10%. 
- On five-band resistors, band 3 becomes an additional significant digit, band 4 becomes the multiplier, and band 5 becomes the tolerance band. 
- Six-band resistors are read identically to five-band resistors, their difference being that the sixth band indicates the resistor's temperature coefficient.

### Light Emitting Diodes - LEDs
Light Emitting Diodes come in a variety of form factors:
<img src="../img/Verschiedene_LEDs.jpg" alt="Image of various Light Emitting Diode form factors." />
LEDs commonly have two leads, although specialty LEDs are available that are capable of simultaneously displaying two colors or of displaying a blended shade. These specialty LEDs have 4-6 leads and 2-4 LED junctions.

LEDs work by applying a voltage with a positive and negative polarity to the leads in such a manner that the positive voltage is attached to the anode of the LED and the negative voltage lead is attached to the LED's cathode. On a two-pin LED, the longer pin is the anode and the short pin is the cathode.

LEDs require current-limiting resistors to avoid destroying the LED junction via an over-current situation. Always include a current-limiting resistor in basic LED circuits. The following schematic illustrates this circuit:

<img src="../img/LED_circuit2.png" alt="This image displays a schematic showing the arrangement of a DC voltage source with the positive lead to the LED's anode, the LED's cathode connected to a one end of a current-limiting resistor and the other end of the voltage drop resistor connected to the negative lead of the voltage source, completing the circuit." />