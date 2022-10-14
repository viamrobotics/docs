---
title: "Troubleshooting"
linkTitle: "Troubleshooting"
weight: 
type: "docs"
description: "A guide to basic troubleshooting of a Viam-based robotic system, easy fixes to common problems, and a list of known issues."
---
This document lists known issues, common troubleshooting steps (e.g., check that the SBC plugged in and turned on, etc.) and common errors, and how we resolved them.
It differs from the FAQ in that the FAQ contains broad, high-level questions about Viam and its software while this section contains specific instructions for resolving software difficulties.

{{% alert title="Note" color="note" %}}  

While every effort has been made to include all common/known issues and their possible resolutions, this list is not comprehensive.
{{% /alert %}}

## Common Errors

### Viam App Logs

#### Error #1: Error reading cloud config
The following related errors may cause this issue:

<table border="solid black 1px">
<tr><th colspan="2">Related Error: Error validating "component s.2": "name" is required.</th>
</tr>
<tr>
<th>What/Why:
</th>
<td>Component name missing.
</td>
</tr>
<tr>
<th>Resolution
</th>
<td>Add the missing name in components and save the config. 
Run <file>sudo systemctl restart viam-server.service</file> in the terminal to restart the server.
</td>
</tr>
</table>

<table border="solid black 1px">
<tr><th colspan="3">Related Error: cannot parse config: JSON: cannot unmarshal string into Go struct field Component.components.frame of type float64.</th>
</tr>
<tr>
<th>What/Why:
</th>
<td colspan="2">Check if there is a frame attribute in the components in the fancy config or in the raw JSON config. 
It may be that the robot config generated broken “frame” information and pre-populated the translation values with empty strings when they are currently programmed to be floats on the backend. 
</td>
</tr>
<tr>
<th>Resolution
</th>
<td width="50%">
Delete the entire “frame” object from the JSON config if you are not using it. 
The frame object looks like this:</td>
</td>
<td><img src="../img/ts-del-frame.png" width="150px"/></td>
</tr>
</table>

<table border="solid black 1px">
<tr>
<th colspan="2">Related Error: cannot parse config: Unexpected end of JSON.</th>
</tr>

<tr>

<th>What/Why:
</th>
<td> - 
</td>

</tr>

<tr>
<th>Resolution
</th>
<td>Run <file>/root/viam -remove</file> in the terminal to clear cache config from the Pi. 
Re-try the operation.
</td>

</tr>
</table>

#### Error #2: SSH error on the terminal: “ssh:connect to host name-pi.local port 22: host is down”

<table border="solid black 1px">
<th>What/Why:
</th>
<td>The Pi does not have an internet connection.
</td>
</tr>
<tr>
<th>Resolution
</th>
<td>Restart both the Pi and the server.
</td>
</tr>
</table>

#### Error #3: “Rolling back draft changes due to error” or “Error reconfiguring robot”, both errors end with: ‘error: error processing draft changes: resource “rdk:component:board/local” not found”

<table border="solid black 1px">
<tr>
<th>What/Why:
</th>
<td>This issue can be caused by an incorrect new configuration, but it could also be caused by a code issue related to reconfiguring robots. 
</td>
</tr>
<tr>
<th>Resolution
</th>
<td>Run <file>sudo systemctl restart viam-server.service</file> in the terminal to restart the server.
</td>
</tr>
</table>


#### Error #4: Expected board name in config for motor. 
<table border="solid black 1px">
<th>What/Why: 
</th>
<td>Check if you forgot to enter the pi name and check for any other missing component specs in config.
</td>
</tr>
<tr>
<th>Resolution
</th>
<td>Add any missing components. 
Run <file>sudo systemctl restart viam-server.service</file> in the terminal to restart the server.
</td>
</tr>
</table>

#### Error #5: Failed to find the best driver that fits the constraints. 

<table border="solid black 1px">

<th><strong>What/Why:
</th>
<td>There are many possible reasons why this happens. Verify that Frame rate, frame format, path/path pattern, width height, have values. 
Viam specifies 0 for these values by default, but verify that the setting is actually there.
</td>
</tr>
<tr>
<th>Resolution
</th>
<td> Restore any missing values.
</td>
</tr>
</table>

#### Error #6: Error configuring robot.
Clearing this related error may resolve the issue.
<table border="solid black 1px">
<tr><th colspan="2">Related Error: error processing draft changes: expected board name in config for motor. </th>
</tr>
<tr>
<th><strong>What/Why:
</th>
<td>The motor config is missing the board name. Verify that the motor name is present in the config. 
</td>
</tr>
<tr>
<th>Resolution
</th>
<td>Add your Pi name and component dependencies and save your configuration.
</td>
</tr>
</table>

#### Error #7: Response closed without headers.

<table border="solid black 1px">
<th><strong>What/Why:
</th>
<td> - 
</td>
</tr>
<tr>
<th>Resolution
</th>
<td> -
</td>
</tr>
</table>

### Github Issues

#### Error #8: Git fetch invalid

<table border="solid black 1px">
<th><strong>What/Why:
</th>
<td>This issue is caused by a problem with the sudo env and the user env. 
When in sudo, the RSA tokens used to connect to GitHub are removed in order to use admin credentials.
</td>
</tr>
<tr>
<th>Resolution
</th>
<td> -
</td>
</tr>
</table>

#### Error #9: Error serving web.

<table border="solid black 1px">
<th><strong>What/Why:
</th>
<td> -
</td>
</tr>
<tr>
<th>Resolution
</th>
<td> -
</td>
</tr>
</table>



## Application and Plugin Conflicts

### Mac Applications
None at this time.
### Windows Applications
None at this time.
### Linux Applications 
None at this time.
### Browser Plugins
1. **PLUGIN:** "**Allow right click - simple copy**" - This Chrome plugin prevents the user from configuring a Service in the Viam app (**app.viam.com** > **Config** > **3 Services**).<br>
**Indication:** User unable to select a Service **Type** in the **Create Service** Pane.
After clicking to display the drop-down list, choosing an item does not populate the drop-down's "Selection."
