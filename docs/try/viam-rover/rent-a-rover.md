---
title: "Rent a Viam Rover"
linkTitle: "Rent a Viam Rover"
weight: 5
type: "docs"
tags: ["rover", "try viam", "rental"]
images: ["/appendix/try-viam/try-viam-reserve-preview.png"]
imageAlt: "Rover reservation page"
description: "Try Viam by reserving a Viam Rover in our robotics lab — no hardware required."
aliases:
  - /dev/reference/try-viam/
  - /dev/reference/try-viam/reserve-a-rover/
  - /dev/reference/try-viam/try-viam-tutorial/
  - /try-viam/
  - /try-viam/reserve-a-rover/
  - /try-viam/try-viam-tutorial/
  - /try-viam/faq/
  - /get-started/try-viam/
  - /get-started/try-viam/reserve-a-rover/
  - /get-started/try-viam/try-viam-tutorial/
  - /get-started/try-viam/faq/
  - /appendix/try-viam/
  - /appendix/try-viam/reserve-a-rover/
  - /appendix/try-viam/reserve-a-rover
  - /appendix/try-viam/tutorials/
  - /appendix/try-viam-faq/
  - /appendix/get-started/try-viam/faq/
  - /getting-started/try-viam/
  - /tutorials/viam-rover/
date: "2026-05-23"
---

_Try Viam_ is a way to try the Viam platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab from anywhere in the world.

Watch this walkthrough for a tour of Try Viam, including how to reserve a Viam Rover, navigate the Viam platform, and drive the rover:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/YYpZ9CVDwMU" max-width="600px">}}

<table>
  <tr>
    <th>{{<imgproc src="/appendix/try-viam/try-viam-1.svg" class="fill alignright" style="width: 300px" declaredimensions=true alt="Click TRY in Viam">}}
      <b>1. Click on TRY in Viam</b>
      <p>Log in to Viam and go to the <a href="https://app.viam.com/try">TRY tab</a>. Don't have a Viam account? Follow the prompts to sign up for an account.</p>
    </th>
  </tr>
  <tr>
    <td>{{<imgproc src="/appendix/try-viam/try-viam-2.svg" class="fill alignleft" style="width: 300px" declaredimensions=true alt="Reserve your slot">}}
      <b>2. Reserve your slot</b>
      <p>If no one's using a Viam Rover, you'll take over immediately. Otherwise, you'll see an estimated time for the next slot, and we'll send you an email when it's your turn. See <a href="#create-a-reservation">detailed instructions</a>.</p>
    </td>
  </tr>
  <tr>
    <td>{{<imgproc src="/appendix/try-viam/try-viam-3.svg" class="fill alignright" style="width: 300px" declaredimensions=true alt="Get started with Viam">}}
      <b>3. Get started with Viam</b>
      <p>Try a Viam Rover in our robotics lab. <a href="/monitor/default-interface/#web-ui">Drive</a> or <a href="/try/viam-rover/drive-rover/">program</a> the rover to see how you can build a machine with Viam.</p>
    </td>
  </tr>
</table>

## Using the reservation system

### Create a reservation

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

### Access your rover rental

Once your reservation starts and the system has configured your rover, click **TRY MY ROVER** from the [**TRY VIAM** page](https://app.viam.com/try) or, if you were queuing, click **Take Me to My Rover** in the confirmation email.

{{<gif webm_src="/appendix/try-viam/rover-reservation.webm" mp4_src="/appendix/try-viam/rover-reservation.mp4" alt="Rover reservation management page" max-width="1000px">}}

{{<imgproc src="appendix/try-viam/navigation-bar.png" resize="800x" alt="Navigation bar with the Viam Rover time remaining indicator.">}}

### Limitations

When using a rented Viam Rover, adding {{< glossary_tooltip term_id="module" text="modules" >}} is disabled for security purposes.
The microphone is also disabled.

### Extend your reservation

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

### Cancel your reservation

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

## Next steps

{{< cards >}}
{{% card link="/try/viam-rover/drive-rover/" %}}
{{< /cards >}}

## FAQ

### How do I make a reservation to take over a Viam Rover?

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

### My machine had an error, a system crash, or is physically stuck

1. Notify Viam support on [our Community Discord](https://discord.gg/viam).
2. Use the **Add Viam Support** button on your machine's Location page to give Viam Support access to your location.
   Refer to [Grant access](/organization/access/#grant-access).

### Can I extend my time?

Sure.

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

### Can I cancel my reservation or session?

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

### Can I rename my machine or change the location?

You can rename your machine or change the location.
If you change the location, you must refresh the page.

### Which organization does this machine belong to?

Your machine belongs to the [organization](/organization/overview/) you were in when you made the request.

### Can I share this location with a friend to work on the machine together?

Sure, you can [invite other users to your organization](/organization/access/#grant-access) to collaborate on your machine.
As members of your organization, those users have full control of your machine.
Another collaboration option is to use screen sharing in a Zoom or Webex session.

### How many active rentals can I have?

You can only borrow one rover at a time.
You cannot join the queue for another reservation while you have an active rental session.
If you would like to, you can [extend your reservation](#extend-your-reservation).

### I loved my experience, can I play around more?

Yes. You can borrow the rover as many times as you'd like.
You can also follow this tutorial:

- [Drive a rover in a square with the Viam SDK](/try/viam-rover/drive-rover/)

If you want to get your own Viam Rover, [you can](https://www.viam.com/resources/rover).

### Why can't I use the rover's microphone?

For security reasons, Viam has disabled the microphone on rover rentals.
The microphone on [Viam Rovers shipped to you](/try/viam-rover/) functions normally.

{{< snippet "social.md" >}}
