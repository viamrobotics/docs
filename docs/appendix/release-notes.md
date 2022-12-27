---
title: "Release Notes"
linkTitle: "Release Notes"
weight: 110
draft: false
type: "docs"
description:
# SME: Mike A.
---
## XX December 2022

{{< tabs >}}
{{% tab name="Versions" %}}

## Release Versions - new numbers coming
* rdk - v0.2.3
* api - v0.1.12
* slam - v0.1.9
* viam-python-sdk - v0.2.0
* goutils - v0.1.4
* rust-utils - v0.0.5
<br><br><br>(**Bold=updated version**)

{{% /tab %}}


{{% tab name="New Features" %}}
## New Features
### Custom Modular Resources
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>This new feature allows users to implement their own custom components or component models using our Go SDK. 
        We are now working to add support in each of our SDKs so that users can create custom resources in a variety of programming languages.</td>
    </tr>
<tbody>
</table>

### URDF Support
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Users that are implementing their own arms are now able to supply kinematic information via URDF files. 
        This is a convenience for our users since URDF files are readily available for common hardware. </td>
    </tr>
<tbody>
</table>

### New Movement Sensors

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We added support for two new movement sensors. 
        Refer to the <a href="/components/movement-sensor/">Movement Sensor</a> topic for more information.
		<ul>
		<li>ADXL345: A 3 axis accelerometer</li>
		<li>MPU6050: 6 axis accelerometer + gyroscope</li>
		</ul>
		<td>
    </tr>
<tbody>
</table>
{{% /tab %}}

{{% tab name="Improvements" %}}
## Improvements
### Improved Camera Performance/Reliability
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td><ol><li>Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request. 
        <stron>The default mime type for color cameras is now JPEG</strong>, which improves the streaming rate across every SDK. </li>
		<li>Added discoverability when a camera reconnects without changing video paths. 
        This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.</li>
		</ol>
 </td>
    </tr>

<tbody>
</table>

### Motion Planning with Remote Components
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We made several improvements to the motion service that make it agnostic to the networking topology of a users robot.</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td><ol><li>Kinematic information is now transferred over the robot API. 
        This means that the motion service is able to get kinematic information for every component on the robot, regardless of whether it is on a main or remote Viam server.</li>
		<li>Arms are now an input to the motion service. 
        This means that the motion service can plan for a robot that has an arm component regardless of whether the arm is on a main or remote Viam server.</li>
		</ol>
</td>
    </tr>
<tbody>
</table>

### Motion Planning Path Smoothing
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>Various small improvements to follow the last major development.</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td><ol><li>Implementation of rudimentary smoothing for RRT* paths, resulting in improvements to path quality, with negligible change to planning performance".</li>
		<li>Changes to plan manager behavior to perform direct interpolation for any solution within some factor of the best score, instead of only in the case where the best IK solution could be interpolated.</li></ol></td>
    </tr>
<tbody>
</table>

### Improved Data Synchronization Reliability

<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>What is it?</strong></td>
        <td>We updated how captured data is uploaded from robots to app.viam.com</td>
    </tr>
    <tr>
        <td><strong>What does it affect?</strong></td>
        <td>We previously used bidirectional streaming, with the robot streaming sensor readings to the app and the app streaming acknowledgements of progress back to the robot. 
        We switched to a simpler unary approach which is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.<br>
{{< alert title="Note" color="note" >}}
This breaking change will NOT affect most users. 
If you have previously captured data on your robot that has not yet been synced, enable syncing to get that data into app.viam before using the new release.
{{< /alert >}}

</td>
</tr>
<tbody>
</table>

{{% /tab %}}
{{% tab name="Issue Resolutions" %}}
<table style="margin-bottom:18px">
<tbody style="vertical-align:top;">
    <tr>
        <td width="120px"><strong>RDK Shutdown Failure</strong></td>
        <td>Fixed a bug where RDK shutdown requests sometimes failed when connected to serial components. </td>
    </tr>
    <tr>
        <td><strong>Python Documentation</strong></td>
        <td>Fixed issues around documentation rendering improperly in some browsers.</td>
    </tr>
<tbody>
</table>
{{% /tab %}}
{{< /tabs >}}
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
        To learn more about the changes, please refer to our <a href="/components/camera/">camera documentation</a>. 
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
		        <td>Based on user feedback, we changed the name of the <strong>CONNECT</strong> tab to 	<strong>CODE SAMPLE</strong></td>
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

{{% alert title="Note" color="note" %}}
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


