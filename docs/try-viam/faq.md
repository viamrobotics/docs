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

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

## My robot had an error, a system crash, or is physically stuck

1. Please notify Viam support on [our Community Discord](https://discord.gg/viam).
2. Use the **Add Viam Support** button on your robot's Location page to give Viam Support access to your *location*.
   Refer to [Managing Locations and sub-locations](/manage/app-usage/#managing-locations-and-sub-locations).

## Can I extend my time?

Sure!

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

## Can I cancel my reservation/session?

Yes.

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

## How can I reuse my rented rover?

After using Try Viam, your robot config stays in your Viam account.
You can access your robot page, write code to control it, and modify its config after your reservation time ends.

When you next rent a rover you can choose to configure it with a previous rover configuration from your account or create a new rover with the standard starting config.

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

Your robot belongs to the [organization](/manage/app-usage/#navigating-organizations) you were in when you made the request.

## Can I share this Location with a friend to work on the robot together?

Sure, you can [invite other users to your organization](/manage/app-usage/#managing-locations-and-sub-locations) to collaborate on your robot.
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
Reserve yours today [here](https://viam.com/resources/rover).

## Why can't I use the rover's microphone?

For security reasons, Viam has disabled the microphone on rover rentals.
The microphone on [Viam Rovers shipped to users](/try-viam/rover-resources/) functions normally.
