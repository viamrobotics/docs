---
title: "Release Notes"
linkTitle: "Release Notes"
weight: 110
draft: false
type: "docs"
description:
# SME: Mike A.
---
## 28 November 2022

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions
* rdk - **v0.2.3**
* api - **v0.1.12**
* slam - **v0.1.9**
* viam-python-sdk - v0.2.0
* goutils - v0.1.4
* rust-utils - v0.0.5
<br><br><br>(**Bold=updated version**)

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}
<table style="margin-bottom:18px">

### Camera Reconnection Issue

<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>When a camera loses connection, it now automatically closes the connection to its video path. 
        Previously, when users supplied a video path in their camera configuration, they encountered issues if the camera tried to reconnect because the supplied video path was already being used for the old connection. </td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td>On losing their video path connection, cameras now automatically close the video path connection.</td>
    </tr>
<tbody>
</table>

{{% /tab %}}
{{% tab name="Improvements" %}}
## Improvements

### Camera Configuration Changes
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We updated the underlying configuration schemes for the following camera models. 
        We are also migrating  existing camera configurations to align with the new schemas. 
        To learn more about the changes, please refer to our <a href="https://docs.viam.com/components/camera/">camera documentation</a>. 
        <ul>
        <li>Webcam</li>
        <li>FFmpeg</li>
        <li>Transform</li>
        <li>Join Pointclouds</li>
        </ul>
</table>

### Robot Details Page

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Based on user feedback, we changed the name of the <strong>CONNECT</strong> tab to <strong>CODE SAMPLE</strong></td>
    </tr>
<tbody>
</table>

{{% /tab %}}
{{% /tabs %}}

## 15 November 2022

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions
* rdk - v0.2.0
* api - v0.1.7
* slam - v0.1.7
* viam-python-sdk - v0.2.0
* goutils - v0.1.4
* rust-utils - v0.0.5
{{% /tab %}}
{{% tab name="New Features" %}}
## New Features
### New servo model

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We added a new servo model called <code>GPIO</code>. This represents <emphasis>any</emphasis> servo that is connected directly to <emphasis>any</emphasis> board via GPIO pins. We created this component in response to the common practice of connecting servos to separate hats, such as the <code>PCA9685</code>, rather than connecting directly to the board. Our previous implementation required a direct connection from the servo to the Raspberry Pi.</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td>While Viam continues to support the <code>pi</code> model of servo, we encourage users to begin using the <code>GPIO</code> model in <emphasis>all<emphasis> of their robots moving forward because it is board-agnostic.</td>
    </tr>
<tbody>
</table>

### Added RTT to remote control page
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We added a new badge in the <code>Current Operations</code> card of the remote control page of the Viam app. This badge lists the RTT (round trip time) of a request from your client to the robot, i.e., the time to complete one request/response cycle.</td>
    </tr>
<tbody>
</table>



### Python 3.8 Support
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Our Python SDK now supports Python 3.8, in addition to 3.9 and 3.10. You will need to update the Python SDK to access the new feature.</td>
    </tr>
<tbody>
</table>

{{% /tab %}}
{{% tab name="Improvements" %}}
## Improvements

### New Parameter: extra
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We added a new API method parameter named, <code>extra</code>, that gives users the option of extending existing resource functionality by implementing the new field according to whatever logic they chose. 
<code>extra</code> is available to requests for all methods in the following APIs:<br><br>
<table style="margin-bottom: 12px;">
<tr><td><li>Arm</li>
<li>Data Manager</li>
<li>Gripper</li>
<li>Input Controller</li></td><td><li>Motion</li>
<li>Movement Sensor</li>
<li>Navigation</li>
<li>Pose Tracker</li></td><td><li>Sensor</li>
<li>SLAM</li>
<li>Vision</li></td></tr>
</table>
</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td>Users of the Go SDK <strong>must</strong> update their code to specify <code>extra</code> in the arguments that pass into each request.

{{% alert="Note" color="note" %}}
This breaking change does NOT affect users of the Python SDK.
{{% /alert %}}</td>
    </tr>
<tbody>
</table>


### Add dependencies to services

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Adding dependencies to services allows Viam to initialize and configure resources in the correct order. For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the service.</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td><strong>Breaking Change</strong>: This impacts users of the SLAM service. Users must now specify which sensors they are using in the <code>depends_on</code> field of the SLAM configuration.
Other service configurations are not affected.</td>
    </tr>
<tbody>
</table>

### Removed width & height fields from Camera API.
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We removed two fields (<code>width</code> and <code>height</code>) that were previously part of the response from the <code>GetImage</code> method in the camera API.
</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td><strong>Breaking Change</strong>: This <emphasis>does not<emphasis> impact any existing camera implementations. 
Users writing custom camera API implementations no longer need to implement the <code>width</code> or <code>height</code> fields.</td>
    </tr>
<tbody>
</table>

{{% /tab %}}
{{% /tabs %}}


