---
title: "Mike's Test File"
linkTitle: "Test"
weight: 1
draft: true
type: "docs"
---

## Tab Panels

{{< tabs name="TabPanelExample" >}}
{{% tab name="Support"%}}
**Supported**
* Markdown and HTML images. 
* Alert Shortcode
* PRISM syntax highlighting (the three backticks)
* "codelang" highlighting (add codelang="language" to tab element). It's very ugly, needs css work, and is not recommended at this time.

**Not Supported**
* Footnotes
* Expanders

**Example Usage**

<img style="border:solid 1px black" alt="Screen capture of a Tab/Tabs Shortcode Block" src="/img/101.png">



{{% /tab %}}
{{% tab name="Examples" %}}
<div>
	<h3>What is Rendered?</h3>
	<p>It renders <i>vanilla</i> HTML and markdown, Alerts, and images. For example, these two images:</p>

* **Markdown Image Example**<br>
![expand example](/img/082.png)<br>
* **HTML Image Example** (with border)<br>
<img style="border:solid 1px black" src="/img/082.png">
</div>
<br>

### Syntax Highlighting with Backticks

```json-viam
{
"word":"Three backticks and the language name to use prism inside tabs",
"note":"Use "json-viam" as the language to highlight Viam keywords in json"
}
```

### Regular Markdown Formatting

This is **some markdown.**

### Alerts Shortcodes
{{< alert Type="Note" color="note" >}}
It can even contain shortcodes.
{{< /alert >}}


{{% /tab %}}
{{< /tabs >}}

## Using Expanders
Expanders allow to you add long sections of code to your topic and hide them until the reader decides to view it. 

Within the expander, you can still use most other shortcodes, and syntax highlighting via Prism still functions properly. The shortcode displays your expander's title in a light blue bar to make it noticeable.<br><br>

**Screen Capture of an Expander**
<img style="border:solid 1px black" alt="Screen capture of the expander control rendered on a documentation page" src="/img/083.png">

### Usage

1. Add the shortcode tags. Make sure that the title is suitable for your use.
1. Drop in the material you want to hide until the reader wants it.


### Markdown Example

<img style="border:solid 1px black" src="/img/082.png">

### Rendered Expander Example
{{%expand "Click to view the source" %}}
<br>

**Prism syntax highlighting works in expanders, as do most other shortcodes.**

``` go
	motion_svc = MotionServiceClient.from_robot(robot, "NAME”)
  	arm = Arm.from_robot(robot=robot, name='xArm6')
  	pos = await arm.get_end_position()
 	 
  	print("~~~~TESTING ARM LINEAR MOVE~~~~~")
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x += 300
  	# Note we are passing an empty worldstate
  	await arm.move_to_position(pose=pos, world_state=WorldState())
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x -= 300
  	await asyncio.sleep(1)
  	await arm.move_to_position(pose=pos, world_state=WorldState())
 	 
  	print("~~~~TESTING MOTION SERVICE MOVE~~~~~")
 	 
  	geom = Geometry(center=Pose(x=pos.x + 150, y=pos.y, z=pos.z), box=RectangularPrism(width_mm =2, length_mm =5, depth_mm =5))
  	geomFrame = GeometriesInFrame(reference_frame="xArm6", geometries=[geom])
  	worldstate = WorldState(obstacles=[geomFrame])
 	 
  	pos = await arm.get_end_position()
  	jpos = await arm.get_joint_positions()
  	print(pos)
  	print("joints", jpos)
  	pos.x += 300
 	 
  	for resname in robot.resource_names:
    	if resname.name == "xArm6":
      	armRes = resname
 	 
  	# We pass the WorldState above with the geometry. The arm should successfully route around it.
  	await motionServ.move(component_name=armRes, destination=PoseInFrame(reference_frame="world", pose=pos), world_state=worldstate)
  	pos = await arm.get_end_position()
  	jpos = await arm.get_joint_positions()
  	print(pos)
  	print("joints", jpos)
  	pos.x -= 300
  	await asyncio.sleep(1)
  	await motionServ.move(component_name=armRes, destination=PoseInFrame(reference_frame="world", pose=pos), world_state=worldstate)
 	 
  	print("~~~~TESTING ARM MOVE- SHOULD FAIL~~~~~")
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x += 300
  	# We pass the WorldState above with the geometry. As arm.move_to_position will enforce linear motion, this should fail
  	# since there is no linear path from start to goal that does not intersect the obstacle.
  	await arm.move_to_position(pose=pos, world_state=worldstate)
```

{{% /expand%}}



## How to use Notes, Cautions, and Warnings

**Info/Tip**: Exactly that. They both use the same color.

**Note**: These call attention to something important. Use it to expand on a point from the body text or to provide a tip or additional information.

**Caution**: Provide notice that a certain action or event could damage hardware or cause data loss.

**Warning**: Use to notify the reader of an issue to avoid loss of life, personal injury, and health hazards. (Think Universal Arm on an unannounced rampage.)



{{< alert title="Tip" color="tip" >}}  
Use for tips
{{< /alert >}}

{{< alert title="Info" color="tip" >}}  
Use for extra background infomation
{{< /alert >}}

{{< alert title="Note" color="note" >}}  
This is to call the reader's attention to something important. Use it to expand on something from the body text or to provide a tip or additional information.
{{< /alert >}}

{{< alert title="Caution" color="caution" >}}  
This provides notices that a certain action or event could damage hardware or cause data loss.
{{< /alert >}}


{{< alert title="Warning" color="warning" >}}  
Use to notify the reader of information to avoid loss of life, personal injury, and health hazards.
{{< /alert >}}

<img src="../img/078.png" alt="screen capture that demonstrates the styling applied to Info/Tip, Note, Caution, And Warning paragraphs." style="border: solid 1px"/>

## Demo of including another file

{{% include"/static/CNAME" %}}
**Content above this line is contained in /static/robot-ipsum.md**