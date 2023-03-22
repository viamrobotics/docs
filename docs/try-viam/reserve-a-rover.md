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

Once your reservation starts and the system has configured your rover, click **TRY MY ROVER** from the [**TRY VIAM** page](https://app.viam.com/try) or, if you were queuing, click **Take Me to My Rover** in the confirmation email.

{{<gif webm_src="img/rover-reservation.webm" mp4_src="../img/rover-reservation.mp4" alt="Rover reservation management page" max-width="1000px">}}

![Navigation bar of the Viam app with the Viam Rover time remaining indicator.](../img/navigation-bar.png)

## Extend your reservation

{{< readfile "/static/include/try-viam/extend-a-reservation.md" >}}

## Cancel my reservation/session

{{< readfile "/static/include/try-viam/cancel-a-reservation.md" >}}

## Next steps

<div class="container text-center td-max-width-on-larger-screens">
  <div class="row">
    <div class="col hover-card hover-card-small">
        <a href="../try-viam-tutorial/">
            <img src="../rover-resources/img/viam-rover/rover-front.jpg" width=100% style="padding-top: 1em" alt="The front of the assembled Viam Rover" />
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Control a Rented Rover</h4>
            <p style="text-align: left;">Remotely configure and control a Viam Rover located on-site at Viam in NYC.</p>
        <a>
    </div>
    <div class="col hover-card hover-card-small">
        <a href="../../tutorials/viam-rover/try-viam-sdk">
            <div class="landing-video-container" style="padding-top: 1em">
                <video autoplay loop muted playsinline alt="Overhead view of the Viam rover showing it as it drives in a square." width="100%">
                    <source src="../../tutorials/img/try-viam-sdk/image1.webm" type="video/webm" />
                    <source src="../../tutorials/img/try-viam-sdk/image1.mp4" type="video/mp4" />
                </video>
            </div>
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Drive with the Viam SDK</h4>
            <p style="text-align: left;">Use the Viam SDK to make your Viam Rover move in a square.</p>
        </a>
    </div>
    <div class="col hover-card hover-card-small">
        <a href="../../tutorials/viam-rover/try-viam-color-detection">
            <img src="../../tutorials/img/try-viam-color-detection/detectioncam-comp-stream.png" width=100% style="padding-top: 1em" alt="detectionCam stream displaying a color detection.">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Detect a Color</h4>
            <p style="text-align: left;">Use the Vision Service in the Viam app to detect a color.</p>
        <a>
    </div>
  </div>
</div>

{{< snippet "social.md" >}}
