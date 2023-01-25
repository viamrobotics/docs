---
title: "Try Viam FAQ"
linkTitle: "Try Viam FAQ"
weight: 50
type: "docs"
description: "Frequently Asked Questions about Try Viam"
---
Try Viam is a way you can try out the platform without setting up any hardware yourself. You can take over a Viam Rover in our robotics lab for 15 minutes to play around!

## How do I make a reservation to take over a Viam Rover?

1. **Click on ‘TRY’ in Viam.** Log into Viam and go to the **[TRY](https://app.viam.com/try)** tab. (If you don’t have an account, it only takes a minute to sign up.)
2. **Click ‘Try Now’ to reserve your slot.** If no one’s using a Viam Rover, you’ll take over immediately. Otherwise, you’ll see an estimated time for the next slot on the TRY tab. If your reserved time slot is more than 30 minutes away, we’ll send you an email confirming your reservation and an email when it’s your turn to use the rover.
3. **Use your reserved Viam Rover on Viam.** See “What happens when my reservation starts?” below for info on how to use the Viam Rover you reserved.

## What happens when my reservation starts?

1. When it is your turn to take over a Viam Rover, the status on the **[TRY](https://app.viam.com/try)** tab will change to **SETTING UP ROBOT**. Once that is complete, the status on the TRY tab will change to **RUNNING**, and you can click “**Try Your Robot**” to access your reserved Viam Rover.
2. Viam creates a location called “Rover Rental” in your organization (if necessary), and adds a Viam Rover with a basic configuration and a random name (e.g., wispy-shape, black-moon, etc.) to your Rover Rental Location.
3. You’ll be able to control a Viam Rover in the Viam robotics lab for 15 minutes. A session timer will be displayed in the top banner. You can see how the rover is configured, write code to control the rover, teleoperate the rover, and more.

## My robot had an error, a system crash, or is physically stuck

1. The timer does not stop at any time.
2. Notify support via [our Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
3. Use the **Add Viam Support** button on your robot's Location page to give Viam Support access to your Location. Refer to [Managing Locations and sub-locations](/program/app-usage/#managing-locations-and-sub-locations) in the **Using the Viam App** topic.

## Can I extend my time?

Sure! If the next time slot is open, click **Extend Reservation** on the **Try** page _before your session ends_ to reset the timer to 15 minutes. When your session ends, you can no longer extend it. You can click **Try** to add a new reservation.

## Can I cancel my reservation/session?

Yes. Click **Cancel Reservation** on the **Try** page to either release your queued reservation or to immediately end your active session.

## Can I reuse my Rover Rental Robot?

Yes. However, note that each reservation is fulfilled with a _new_ robot having the standard configuration.
For your next session, you can copy the config from your previous robot to the new robot.
At any time prior to the start of your new rental:

1. Access [https://app.viam.com/](https://app.viam.com/try)
2. Under **LOCATIONS**, click “Rover Rental.”
3. Click the robot name whose configuration you wish to reuse.
4. Select “Raw JSON” on the **Mode** selector.
5. Click anywhere in the displayed JSON configuration and press **CTRL+A** on Windows and Linux platforms, or **CMD+A** on macOS, to copy the _entire_ configuration.

{{%  alert title="Note" color="note" %}}
The **COPY VIAM-SERVER CONFIG** button only copies the server connection information, _not the entire configuration_.
Save this configuration for later use, if desired.
{{% /alert %}}

When you open your new rental in Try Viam:

1. Click **CONFIG**.
2. Select “Raw JSON” from the **Mode** selector.
3. Click anywhere in the displayed JSON configuration and press **CTRL+A** on Windows and Linux, or **CMD+A** on macOS, to select the entire JSON configuration, then press **Delete**.
4. Paste in your saved configuration.
5. Click **Save Config**.
6. You can access your robot, write code using a Viam SDK, and modify its config even after your reservation time ends and you can no longer operate it.
This allows you to make updates between sessions to prepare for future sessions.

## What happens to my Rover Rental robot after the rental session?

1. On session expiration, Viam removes the “live” status from the robot.
2. Viam then removes your configuration from the physical robot in preparation for its next rental.
3. The Rover Rental Location and _the final configuration of all previous Rover Rental robots remain visible to your organization_.
You can continue modifying the configurations as desired.

## I accidentally deleted my robot

Unfortunately, there is no recovery path for a deleted robot.
If you delete your robot and have a current reservation, the only option available is to click **Cancel Reservation** and then request a new reservation.

## Can I rename my robot or Location?

You can rename your robot as desired.
However, changing the Location will break your robot.
If this occurs, use the Viam app to rename the Location name back to its default, which is “Rover Rental”.

{{% alert title="Caution" color="caution" %}}
Do not change the Location name.
The Location **must** be "Rover Rental"
{{% /alert %}}

## Which Org does this robot belong to?

Your robot belongs to the Org you were in when you made the request.

## Can I share this Location with a friend to work on the robot together?

1. Sure, you can invite other users to your Org to collaborate on your robot.
Note that as members of your organization, those users have full control of your robot.
2. Another collaboration option is to use screen sharing in a Zoom or Webex session.

## How many active rentals can I have?

Viam’s reservation system allows each user a single entry.
Each user may have one active rental session or one queued reservation, but not both.

{{% alert title="Note" color="note" %}}
The Try Viam reservation system allows each user one entry in the system.
If you are participating in an active session or awaiting your turn in the queue, you may not create another reservation.
{{% /alert %}}

## I loved my experience and want to play around more. Can I do that?

Yes! You can rent the rover as many times as you’d like. Also, we’re taking pre-orders for a limited quantity of Viam Rovers. Reserve yours today [here](http://viam.com/resources/rover?utm_source=slack&utm_medium=social&utm_campaign=try-viam).

## Why can't I use the Rover's microphone?

For security reasons, Viam has disabled the microphone on Rover Rentals. The microphone on Viam Rover's shipped to users functions normally.
