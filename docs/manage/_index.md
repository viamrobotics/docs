---
title: "Manage Robots with the Viam app"
linkTitle: "Manage"
weight: 22
type: docs
no_list: true
description: "A guide to getting started with app.viam.com, a web app for building and managing robots with Viam."
aliases:
  - "/viam/app.viam.com/"
---

The [Viam app](https://app.viam.com/) is a web UI for managing and building robots.

## Create Account and Log In

To get started on the Viam app, you must log in as an authorized user.
Viam support sign up using Google, GitHub, Apple, and Email.

Navigate to [the main page](https://app.viam.com/).
If you haven't created a user yet, click **Sign Up** to create a new user using your prefered Single Sign On method or your email address and a password.
If you already have a user, click **Log In** to log in using your Single Sign On credentials or your email address and password.

If you forget your password to the app, click **Forgot password** and enter your email address to obtain instructions to reset your password.

{{< alert title="Info" color="info" >}}
We do not automatically merge Single Sign On accounts.
If you use Google to log in and then sign up with Apple, Viam treats that as two separate accounts.
{{< /alert >}}


## Manage

You do not have to use the app to use Viam's platform to build your robot, but it has several key features to help you get started managing your robots, including configuring robots with more complicated architecture like sub-parts or remotes:

{{< cards >}}
  {{% card link="/manage/configuration" %}}
  {{% card link="/manage/fleet" %}}
  {{% card link="/manage/data" %}}
  {{% card link="/manage/ml" %}}
  {{% card link="/manage/parts-and-remotes" %}}
{{< /cards >}}

<br>

You can also manage and control your robots from the command line with our CLI:

{{< cards >}}
  {{% card link="/manage/cli" %}}
{{< /cards >}}

## Sign Out

To log out or sign out of the [Viam app](https://app.viam.com/), click on your profile icon in the upper right corner of your browser window.
Click **Sign out** to sign out of accessing all organizations, locations, and robots your credentials manage.
