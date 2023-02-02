---
title: "Try Viam FAQ"
linkTitle: "Try Viam FAQ"
weight: 50
type: "docs"
description: "Frequently Asked Questions about Try Viam."
---

Try Viam allows you to try the Viam platform without setting up any hardware yourself.
For 15 minutes, no matter where you are in the world, you can take over and play around with a Viam Rover in our robotics lab!

## How do I make a reservation to take over a Viam Rover?

{{< readfile "create-a-reservation.md" >}}

## My robot had an error, a system crash, or is physically stuck

1. Please notify Viam support on [our Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
2. Use the **Add Viam Support** button on your robot's Location page to give Viam Support access to your *location*.
   Refer to [Managing Locations and sub-locations](/program/app-usage/#managing-locations-and-sub-locations).

## Can I extend my time?

Sure!
If the next time slot is open, you can click **Extend Reservation** on the **Try** page.
You must do this *before your session ends* to reset the timer to 15 minutes.
When your session ends, you can no longer extend it.
If your session ends, you can always create a new reservation.

## Can I cancel my reservation/session?

Yes.
Click **Cancel Reservation** on the **[Try page](https://app.viam.com/try)** to either release your queued reservation or to immediately end your active session.

## How can I reuse my rented rover?

After using Try Viam, your robot config stays in your Viam account.
You can access your robot page, write code to control it, and modify its config after your reservation time ends.
However, you can no longer operate it.

Each reservation is fulfilled with a *new* robot with the standard starting config.
To reuse the config from your previous rental rover, copy the config from your previous robot to the new robot:

1. Access the [Fleet page](https://app.viam.com/robots)
2. Select **Rover Rental** on the **LOCATIONS** navigation bar on the left.
3. Click the robot name whose config you wish to reuse.
4. Select "Raw JSON" on the **Mode** selector.
5. Copy the *entire* config.

Once you have your new rental rover:

1. Access the [Fleet page](https://app.viam.com/robots)
2. Select **Rover Rental** on the **LOCATIONS** navigation bar on the left.
3. Click on your new rental robot name.
4. Click **CONFIG**.
5. Select "Raw JSON" from the **Mode** selector.
6. Replace the *entire* existing config with your copied config.
7. Click **Save Config**.

{{< alert title="Tip" color="tip" >}}
You can also reuse your code for the rover for other robots that you configure with Viam in the future.
{{< /alert >}}

## What happens to my rented rover after the rental session?

1. On session expiration, Viam removes the "live" status from the robot.
2. Viam then removes your config from the physical robot in preparation for its next rental.
3. The Rover Rental Location and the final config of all previous rental rovers remain visible to your organization.
   You can continue modifying the configurations as desired.

## I accidentally deleted my robot

Unfortunately, there is no recovery path for a deleted robot.
If you delete your robot and have a current reservation, click **Cancel Reservation** and then request a new reservation.

## Can I rename my robot or change the location?

You can rename your robot or change the location.
If you change the location, you must refresh the page.

## Which organization does this robot belong to?

Your robot belongs to the [organization](/program/app-usage/#navigating-organizations) you were in when you made the request.

## Can I share this Location with a friend to work on the robot together?

Sure, you can [invite other users to your organization](/program/app-usage/#managing-locations-and-sub-locations) to collaborate on your robot.
As members of your organization, those users have full control of your robot.
Another collaboration option is to use screen sharing in a Zoom or Webex session.

## How many active rentals can I have?

You can only rent one rover at a time.
You cannot join the queue for another reservation while you have an active rental session.
If you would like to, you can [extend your reservation](/try-viam/faq/#can-i-extend-my-time).

## I loved my experience - can I play around more?

Yes! You can rent the rover as many times as you’d like.
Here are some tutorials which you can follow:

- [Drive with the Viam SDK](/tutorials/viam-rover/try-viam-sdk)
- [Detect a Color](/tutorials/viam-rover/try-viam-color-detection)

If you want to get your own Viam Rover, we’re also taking pre-orders for a limited quantity of Viam Rovers.
Reserve yours today [here](http://viam.com/resources/rover?utm_source=slack&utm_medium=social&utm_campaign=try-viam).

## Why can't I use the Rover's microphone?

For security reasons, Viam has disabled the microphone on Rover Rentals.
The microphone on [Viam Rovers shipped to users](/try-viam/rover-resources/) functions normally.
