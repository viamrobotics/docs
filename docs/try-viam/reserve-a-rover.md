---
title: "Reserve a Viam Rover"
linkTitle: "Reserve a Viam Rover"
weight: 10
type: "docs"
description: "Reserve a Viam Rover located on-site at Viam in NYC."
tags: ["try viam", "app"]
---

_Try Viam_ is a way to try out the Viam platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab for 15 minutes to play around!

Watch this tutorial video for a walkthrough of Try Viam, including [how to reserve a Viam Rover](#using-the-reservation-system), [navigate the Viam platform](/manage/app-usage/), and [drive the rover](../try-viam-tutorial/#control-tab):

<div class="embed-responsive embed-responsive-16by9">
    <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/YYpZ9CVDwMU" allowfullscreen></iframe>
</div>

## Using the reservation system

### Create a reservation

{{< readfile "/static/include/try-viam/create-a-reservation.md" >}}

### Access your rover rental

Once your reservation start and the system has reset the rover configuration for you, click **TRY YOUR ROBOT** from [the **TRY** tab](https://app.viam.com/try) or, if you were queuing, click **Take Me to My Rover** in the confirmation email.

![The Try Viam reservation management page with the try your robot button.](../img/try-viam/reservation-management.png)

{{< alert title="Note" color="note" >}}
During your rental, if you want to extend the reservation, go back to [the **TRY** tab](https://app.viam.com/try) and click **EXTEND RESERVATION**.
If the option is not available, that means there is another reservation waiting.
In this case join the queue again once your rental is over.

If you want to cancel the reservation, go back to [the **TRY** tab](https://app.viam.com/try) and click **CANCEL RESERVATION**

{{< /alert >}}

You can also click on the timer at the top to go back to the rental rover's **CONTROL** tab where you can drive the robot.

![Screenshot of the top navigation bar of the Viam app with the Viam Rover time remaining indicator/button.](../img/try-viam/timer.png)

## Extend your reservation

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

## Cancel my reservation/session

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

## Next steps

<div class="container text-center td-max-width-on-larger-screens">
  <div class="row">
    <div class="col hover-card">
        <br>
        <img src="../rover-resources/img/viam-rover/rover-front.jpg" style="max-width:400px;width:100%" alt="The front of the assembled Viam Rover" />
        <br>
        <a href="../rover-resources/">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Control a Rented Rover</h4>
            <p style="text-align: left;">Remotely configure and control a Viam Rover located on-site at Viam in NYC.</p>
        <a>
    </div>
    <div class="col hover-card">
        <br>
        <img src="../../tutorials/img/try-viam-sdk/image1.gif" alt="Overhead view of the Viam rover showing it as it drives in a square.">
        <br>
        <a href="../../tutorials/viam-rover/try-viam-sdk">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Drive with the Viam SDK</h4>
            <p style="text-align: left;">Use the Viam SDK to make your Viam Rover move in a square.</p>
        </a>
    </div>
    <div class="col hover-card">
        <br>
        <img src="../../tutorials/img/try-viam-color-detection/detectioncam-comp-stream.png" alt="detectionCam stream displaying a color detection.">
        <br>
        <a href="../../tutorials/viam-rover/try-viam-color-detection">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Detect a Color</h4>
            <p style="text-align: left;">Use the Vision Service in the Viam app to detect a color.</p>
        <a>
    </div>
  </div>
</div>

{{< snippet "social.md" >}}
