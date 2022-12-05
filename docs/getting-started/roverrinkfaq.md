--- 
title: Try Viam FAQ"
linkTitle: "Try Viam FAQ"
weight: 50
type: "docs"
description: "Frequently Asked Question's about using the 'Try Viam' feature."
---

### What happens when my reservation starts?

1. Prior to your reservation, Viam assigns your session an Rover Rink, creates the “Rover Rental” Location in your organization (if necessary), and finally adds a Rover Rental robot with a basic configuration and a random name (e.g., wispy-shape, black-moon, etc.) to your Rental Rover Location.
You cannot choose a specific physical rover or Rover Rink.
2. If you made your reservation more than 30 minutes in advance, Viam sends you a reservation confirmation email.
   Viam also sends a "Ready to Play" notification when your Rover Rental is ready for use.
The notification contains a link to the specific robot for this session.
1. When it’s your turn, your robot’s status on the Try page changes to **RUNNING** and Try displays the Session timer in the top banner.
2. Click **TRY YOUR ROBOT** to access your Rover Rental robot in the Viam app.

### My robot had an error, a system crash, or is physically stuck

1. The timer does not stop at any time.
2. Notify support via our Community Slack[^cs].
3. Use the **Add Viam Support** button on your robot's Location page to give Viam Support access to your Location. Refer to [Managing Locations and sub-locations](../app-usage/#managing-locations-and-sub-locations) in the **Using the Viam App** topic.

[^cs]: Viam Support on Slack: [(ht<span></span>tps://viamrobotics.slack.com/archives/C042LE6LWQ6)](https://viamrobotics.slack.com/archives/C042LE6LWQ6)

### Can I extend my time?

Sure! If the next time slot is open, click **Extend Reservation** on the **Try** page _before your session ends_ to reset the timer to 15 minutes. When your session ends, you can no longer extend it. You can click **Try** to add a new reservation.

### Can I cancel my reservation/session?

Yes. Click **Cancel Reservation** on the **Try** page to either release your queued reservation or to immediately end your active session.

### Can I reuse my Rover Rental Robot?

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

### What happens to my Rover Rental robot after the rental session?

1. On session expiration, Viam removes the “live” status from the robot.
2. Viam then removes your configuration from the physical robot in preparation for its next rental.
3. The Rover Rental Location and _the final configuration of all previous Rover Rental robots remain visible to your organization_.
You can continue modifying the configurations as desired.

### I accidentally deleted my robot

Unfortunately, there is no recovery path for a deleted robot.
If you delete your robot and have a current reservation, the only option available is to click **Cancel Reservation** and then request a new reservation.

### Can I rename my robot or Location?

You can rename your robot as desired.
However, changing the Location will break your robot.
If this occurs, use the Viam app to rename the Location name back to its default, which is “Rover Rental”.

{{% alert title="Caution" color="caution" %}}
Do not change the Location name.
The Location **must** be "Rover Rental"
{{% /alert %}}

### Which Org does this robot belong to?

Your robot belongs to the Org you were in when you made the request.

### Can I share this Location with a friend to work on the robot together?

1. Sure, you can invite other users to your Org to collaborate on your robot.
Note that as members of your organization, those users have full control of your robot.
2. Another collaboration option is to use screen sharing in a Zoom or Webex session.

### How many active rentals can I have?

Viam’s reservation system allows each user a single entry.
Each user may have one active rental session or one queued reservation, but not both.

{{% alert title="Note" color="note" %}}
The Try Viam reservation system allows each user one entry in the system.
If you are participating in an active session or awaiting your turn in the queue, you may not create another reservation.
{{% /alert %}}
