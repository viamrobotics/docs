---
title: "Reserve a Viam Rover"
linkTitle: "Reserve a Viam Rover"
weight: 10
type: "docs"
description: "Reserve a Viam Rover located on-site at Viam in NYC."
images: ["/appendix/try-viam/try-viam-reserve-preview.png"]
imageAlt: "Rover reservation page"
tags: ["try viam", "app"]
aliases:
  - "/try-viam/reserve-a-rover/"
  - "/get-started/try-viam/reserve-a-rover/"
---

_Try Viam_ is a way to try out the Viam platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab to play around!

Watch this tutorial video for a walkthrough of Try Viam, including [how to reserve a Viam Rover](#using-the-reservation-system), [navigate the Viam platform](/fleet/), and [drive the rover](/components/base/wheeled/#test-the-base):

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/YYpZ9CVDwMU" max-width="600px">}}

## Using the reservation system

### Create a reservation

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

### Access your rover rental

Once your reservation starts and the system has configured your rover, click **TRY MY ROVER** from the [**TRY VIAM** page](https://app.viam.com/try) or, if you were queuing, click **Take Me to My Rover** in the confirmation email.

{{<gif webm_src="/appendix/try-viam/rover-reservation.webm" mp4_src="/appendix/try-viam/rover-reservation.mp4" alt="Rover reservation management page" max-width="1000px">}}

{{<imgproc src="appendix/try-viam/navigation-bar.png" resize="800x" alt="Navigation bar of the Viam app with the Viam Rover time remaining indicator.">}}

### Limitations

When using a rented Viam rover, adding [modules](/registry/) is disabled for security purposes.

### Extend your reservation

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

### Cancel my reservation/session

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

## Next steps

{{< cards >}}
{{% card link="/get-started/drive-rover/" %}}
{{% card link="/tutorials/services/basic-color-detection/" %}}
{{< /cards >}}

## FAQ

Try Viam allows you to try the Viam platform without setting up any hardware yourself.
No matter where you are in the world you can take over and play around with a Viam Rover in our robotics lab!

### How do I make a reservation to take over a Viam Rover?

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

### My machine had an error, a system crash, or is physically stuck

1. Please notify Viam support on [our Community Discord](https://discord.gg/viam).
2. Use the **Add Viam Support** button on your machine's Location page to give Viam Support access to your _location_.
   Refer to [Managing Locations and sub-locations](/cloud/locations/).

### Can I extend my time?

Sure!

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

### Can I cancel my reservation/session?

Yes.

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

### How can I reuse my borrowed rover?

After using Try Viam, your machine config stays in your Viam account.
You can access your machine page, write code to control it, and modify its config after your reservation time ends.

When you next borrow a rover you can choose to configure it with a previous rover configuration from your account or create a new rover with the standard starting config.

{{< alert title="Tip" color="tip" >}}
You can also reuse your code for the rover for other machines that you configure with Viam in the future.
{{< /alert >}}

### What happens to my borrowed rover after the rental session?

1. On session expiration, Viam removes the "live" status from the machine.
2. Viam then removes your config from the physical machine in preparation for its next rental.
3. The Rover Rental Location and the final config of all previous rental rovers remain visible to your organization.
   You can continue modifying the configurations as desired.

### I accidentally deleted my machine

Unfortunately, there is no recovery path for a deleted machine.
If you delete your machine and have a current reservation, click **Cancel Reservation** and then request a new reservation.

### Can I rename my machine or change the location?

You can rename your machine or change the location.
If you change the location, you must refresh the page.

### Which organization does this machine e belong to?

Your machine belongs to the [organization](/cloud/organizations/) you were in when you made the request.

### Can I share this Location with a friend to work on the machine together?

Sure, you can [invite other users to your organization](/cloud/locations/) to collaborate on your machine.
As members of your organization, those users have full control of your machine.
Another collaboration option is to use screen sharing in a Zoom or Webex session.

### How many active rentals can I have?

You can only borrow one rover at a time.
You cannot join the queue for another reservation while you have an active rental session.
If you would like to, you can [extend your reservation](/appendix/try-viam/reserve-a-rover/#can-i-extend-my-time).

### I loved my experience - can I play around more?

Yes! You can borrow the rover as many times as you’d like.
Here are some tutorials which you can follow:

- [Drive with the Viam SDK](/get-started/drive-rover/)
- [Detect a Color](/tutorials/services/basic-color-detection/)

If you want to get your own Viam Rover, [you can](https://viam.com/resources/rover).

### Why can't I use the rover's microphone?

For security reasons, Viam has disabled the microphone on rover rentals.
The microphone on [Viam Rovers shipped to you](/appendix/try-viam/rover-resources/) functions normally.

{{< snippet "social.md" >}}
