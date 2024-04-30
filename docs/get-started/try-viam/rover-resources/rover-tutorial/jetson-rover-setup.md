---
title: "Set up your Rover 2 with a Jetson"
linkTitle: "Set Up your Rover 2 with a Jetson"
weight: 10
type: "docs"
tags: ["rover", "tutorial"]
images: ["/get-started/try-viam/rover-resources/viam-rover-2/box-contents.png"]
imageAlt: "A Viam Rover 2 in a box"
description: "Instructions for setting up a Viam Rover 2 with a Jetson Nano or Jetson Orin Nano."
---

The [Viam Rover 2](https://www.viam.com/resources/rover) arrives preassembled with two encoded motors with suspension, a webcam with a microphone unit, a 6 axis IMU, power management and more.
It is primarily designed for use with a Raspberry Pi 4, but you can use it with a larger Jetson board with some additional setup.

This guide provides supplemental instructions for setting up your rover with a Jetson Nano.

{{< tabs >}}
{{% tab name="Jetson Nano" %}}

{{% alert title="Important" color="tip" %}}
You must purchase the following hardware separately:

- Four 18650 batteries (with charger) or a RC type battery with dimensions no greater than 142mm x 47mm x 60mm (LxWxH) (with charger)
- A MicroSD card and an adapter/reader
- A longer 40 pin ribbon cable: female-female
- 4 25 mm female-female standoffs
- WiFi board: either [a board that directly interfaces with the Nano](https://www.amazon.com/Wireless-AC8265-Wireless-Developer-Support-Bluetooth/dp/B07V9B5C6M/) or [a USB based device](https://www.amazon.com/wireless-USB-WiFi-Adapter-PC/dp/B07P5PRK7J/)
- Electrical tape

The ribbon cable you purchase must meet these requirements:

- Female-female
- 2.54 mm spacing
- Both connectors facing the same direction
- Pin continuity order to be 12-12
- Recommended length ~200 mm
  {{% /alert %}}

## Safety

Read all instructions fully before using this product.

This product is not a toy and is not suitable for children under 12.

Switch the rover off when not in use.

{{< alert title="Warning" color="warning" >}}
Lithium-ion batteries may pose a flammable hazard.
This product requires four 18650 lithium-ion batteries OR an RC-type battery.
DO NOT connect multiple power sources simultaneously.
Refer to the battery manufacturer’s operating instructions to ensure safe operation of the Viam Rover.
Dispose of lithium-ion batteries per manufacturer instructions.
{{< /alert >}}

{{< alert title="Caution" color="caution" >}}
Damage may occur to the board and/or Viam Rover if wired incorrectly.
Refer to the manufacturer’s instructions for correct wiring.
{{< /alert >}}

Disclaimer: This product is preliminary and experimental in nature, and is provided "AS IS" without any representation or warranty of any kind.
Viam does not make any promise or warranty that the product will meet your requirements or be error free.
Some states do not allow the exclusion or disclaimer of implied warranties, so the above exclusions may not apply to you.

## Setup

1. Install the WiFi board/device on the Nano. Follow the manufacturer's instructions to do so.
2. Power the Jetson Nano with a power supply and [prepare the device and install `viam-server`](/get-started/installation/prepare/jetson-nano-setup/).
3. Switch back to the main guide and complete these two steps:
   [Add the power supply](/get-started/try-viam/rover-resources/rover-tutorial/#add-the-power-supply) and [Configure the low-voltage cutoff circuit](/get-started/try-viam/rover-resources/rover-tutorial/#configure-the-low-voltage-cutoff-circuit).
4. Unscrew the top of the rover with the biggest Allen key.
5. Take the [height extenders](/get-started/try-viam/rover-resources/rover-tutorial/#whats-inside-the-kit) provided in your kit.
   Apply them to the rover chassis posts.
6. Unscrew the standoffs in the motherboard and relocate them to the Jetson board hole pattern: {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/hole-patterning.png" resize="400x" declaredimensions=true alt="Viam rover 2 motherboard hole patterns" >}}
7. Connect the ribbon cable to the motherboard and Jetson Nano.
   The ribbon cable needs to be routed towards the front of the rover and flip back to the pins on the Jetson Nano, as pictured: {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/jetson-ribbon.png" resize="400x" declaredimensions=true alt="The Jetson ribbon cable" >}}
8. Use the smallest Allen key and the provided M2.5 screws to attach your board to your rover through these standoffs. The USB ports should be facing the left-hand side of the rover, when viewed from above: {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/jetson-motherboard.png" resize="400x" declaredimensions=true alt="The underside of a rover with the Jetson mounted" >}}
9. Connect the webcam's USB lead to any USB port on your board.
10. Flip the power switch to turn your rover on.

{{% /tab %}}
{{% tab name="Jetson Orin Nano" %}}

{{% alert title="Important" color="tip" %}}
You must purchase the following hardware separately:

- A 4S RC type battery with dimensions no greater than 142mm x 47mm x 60mm (LxWxH) (with charger)
- A MicroSD card and an adapter/reader
- A longer ribbon cable: female-female (ensure that the contacts are correct)
- 4 25 mm female-female standoffs
- WiFi board: either [a board that directly interfaces with the Nano](https://www.amazon.com/Wireless-AC8265-Wireless-Developer-Support-Bluetooth/dp/B07V9B5C6M/) or [a USB based device](https://www.amazon.com/wireless-USB-WiFi-Adapter-PC/dp/B07P5PRK7J/)
- A wired DC jack connector with the same polarity as the Jetson Orin Nano power input
- Electrical tape

The ribbon cable you purchase must meet these requirements:

- Female-female
- 2.54 mm spacing
- Both connectors facing the same direction
- Pin continuity order to be 12-12
- Recommended length ~200 mm
  {{% /alert %}}

## Safety

Read all instructions fully before using this product.

This product is not a toy and is not suitable for children under 12.

Switch the rover off when not in use.

{{< alert title="Warning" color="warning" >}}
Lithium-ion batteries may pose a flammable hazard.
This product requires four 18650 lithium-ion batteries OR an RC-type battery.
DO NOT connect multiple power sources simultaneously.
Refer to the battery manufacturer’s operating instructions to ensure safe operation of the Viam Rover.
Dispose of lithium-ion batteries per manufacturer instructions.
{{< /alert >}}

{{< alert title="Caution" color="caution" >}}
Damage may occur to the Jetson Orin Nano and/or Viam Rover if wired incorrectly.
Refer to the manufacturer’s instructions for correct wiring.
{{< /alert >}}

Disclaimer: This product is preliminary and experimental in nature, and is provided "AS IS" without any representation or warranty of any kind.
Viam does not make any promise or warranty that the product will meet your requirements or be error free.
Some states do not allow the exclusion or disclaimer of implied warranties, so the above exclusions may not apply to you.

## Setup

1. Power the Jetson Orin Nano with a power supply and [prepare the device and install `viam-server`](/get-started/installation/prepare/jetson-nano-setup/).
2. Switch back to the main guide and complete these two steps:
   [Add the power supply](/get-started/try-viam/rover-resources/rover-tutorial/#add-the-power-supply) and [Configure the low-voltage cutoff circuit](/get-started/try-viam/rover-resources/rover-tutorial/#configure-the-low-voltage-cutoff-circuit).
3. Unscrew the top of the rover with the biggest Allen key.
4. Take the [height extenders](/get-started/try-viam/rover-resources/rover-tutorial/#whats-inside-the-kit) provided in your kit.
   Apply them to the rover chassis posts.
5. Unscrew the standoffs in the motherboard and relocate them to the Jetson board hole pattern: {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/hole-patterning.png" resize="400x" declaredimensions=true alt="Viam rover 2 motherboard hole patterns" >}}
6. **IMPORTANT:** Disconnect the 5V buck converter. Unlike other boards, the Jetson Orin Nano requires a 7-20V input, which means that the board must be powered directly from the battery.
   **Before commencing, ensure that everything is powered off.**
   It is recommended that you clip the buck converter wires completely and place electrical tape over the exposed contacts, as pictured:
   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/clip-wires.png" resize="250x" declaredimensions=true alt="Clipping the buck converter wires" >}}
   {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/tape.png" resize="250x" declaredimensions=true alt="Placing electrical tape over the exposed contacts" >}}
7. Connect the ribbon cable to the motherboard and Jetson Orin Nano.
8. Use the smallest Allen key and the provided M2.5 screws to attach your board to your rover through these standoffs. The USB ports should be facing the left-hand side of the rover, when viewed from above: {{<imgproc src="get-started/try-viam/rover-resources/viam-rover-2/jetson-orin-motherboard.png" resize="400x" declaredimensions=true alt="The underside of a rover with the Jetson Orin Nano mounted" >}}
9. Connect a WiFi adapter or a board that directly interfaces to the underside of the Jetson Orin Nano.
10. Connect the webcam's USB lead to any USB port on your board.
11. Flip the power switch to turn your rover on.

{{% /tab %}}
{{< /tabs >}}

### Control your rover on the Viam app

If you followed the instructions in the [Jetson installation guide](/get-started/installation/prepare/jetson-nano-setup/), you should have already made an account on the [Viam app](https://app.viam.com), installed `viam-server` on the board, and added a new machine.

To configure your rover so you can start driving it, [add a Viam Rover 2 Fragment to your machine](/get-started/try-viam/rover-resources/rover-tutorial-fragments/).

## Next steps

After adding the appropriate fragment, follow one of these tutorials with your borrowed or owned rover:

{{< cards >}}
{{% card link="/tutorials/get-started/try-viam-sdk/" %}}
{{% card link="/tutorials/services/try-viam-color-detection/" %}}
{{< /cards >}}
