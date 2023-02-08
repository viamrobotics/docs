---
title: "Mike's Test File"
linkTitle: "Test"
weight: 1
draft: true
type: "docs"
---

## Reusable Text Snippets

There are situations where we need to repeat text blocks. For example, when cautioning users to disconnect power before changing connections or providing a commonly used instruction set or procedure.

Rather than re-typing the material or making multiple copy/paste updates in many locations, you can simply update one file and its content flows to any location it was used.

The following is an example of the <file>secret-share.md</file> alert added using the snippet shortcode:

{{% figure src="/img/snippet-shortcode.png" alt="Snippet shortcode usage." title="Snippet Shortcode Usage" %}}

{{% snippet "secret-share.md" %}}

## Tab Panels

{{< tabs name="TabPanelExample" >}}
{{% tab name="Support"%}}
**Supported**

* Markdown and HTML images.
* Alert Shortcode
* PRISM syntax highlighting (the three backticks)
* "codelang" highlighting (add codelang="language" to tab element). It's very ugly, needs css work, and is not recommended at this time.

### Not Supported

* Footnotes
* Expanders

### Example Usage

<img style="border:solid 1px black" alt="Screen capture of Tab/Tabs Shortcode Usage" src="/img/tabbed-panel-markdown.png">

{{% /tab %}}
{{% tab name="Examples" %}}

<div>
 <h3>What is Rendered?</h3>
 <p>It renders <i>vanilla</i> HTML and markdown, Alerts, and images. For example, these two images:</p>

* **Markdown Image Example**<br>
![expand example](/img/expander-markdown.png)<br>
* **HTML Image Example** (with border)<br>
<img style="border:solid 1px black" src="/img/expander-markdown.png" alt="Screen capture of Tab/Tabs Shortcode Usage">

</div>
<br>

{{% /tab %}}
{{< /tabs >}}

## You can use `code` in headers

[You can use `code` in links](www.viam.com)

### Syntax Highlighting with Backticks

Line numbering is on by default.

```json-viam {class="line-numbers linkable-line-numbers"}
{
"word":"As before, three backticks and the language name enables Prism syntax highlighting.",
"note":"Use "json-viam" as the language to highlight Viam's keywords."
}
```

With just line 6 highlighted. See <https://prismjs.com/plugins/line-highlight/> for more:

```python {class="line-numbers linkable-line-numbers" data-line="6"}
while (True):
    # When True, sets the LED pin to high or on.
    await led.set(True)
    print('LED is on')

    await asyncio.sleep(1)

    # When False, sets the pin to low or off.
    await led.set(False)
    print('LED is off')

    await asyncio.sleep(1)
```

With linked lines and lines 8-10 highlighted.

```python {id="some-python-unique-id" class="linkable-line-numbers" data-line="8-10"}
while (True):
    # When True, sets the LED pin to high or on.
    await led.set(True)
    print('LED is on')

    await asyncio.sleep(1)

    # When False, sets the pin to low or off.
    await led.set(False)
    print('LED is off')

    await asyncio.sleep(1)
```

### Regular Markdown Formatting

This is **some markdown.**

### Alerts Shortcodes

{{< alert title="Note" color="note" >}}
It can even contain shortcodes.
{{< /alert >}}

## Using Expanders

Expanders allow to you add long sections of code to your topic and hide them until the reader decides to view it.

Within the expander, you can still use most other shortcodes and syntax highlighting via Prism functions properly. The shortcode displays your expander's title in a light blue bar to make it noticeable.<br><br>

**Screen Capture of an Expander**
<img style="border:solid 1px black" alt="Screen capture of the expander control rendered on a documentation page" src="/img/expander-example.png">

### Usage

1. Add the shortcode tags. Make sure that the title is suitable for your use.
1. Drop in the material you want to hide until the reader wants it.

### Markdown Example

<img style="border:solid 1px black" src="/img/expander-markdown.png">

### Rendered Expander Example

{{%expand "Click to view the source" %}}
<br>

**Prism syntax highlighting works in expanders, as do most other shortcodes.**

``` python
motion_svc = MotionServiceClient.from_robot(robot, "NAME")
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

**Note**: These call attention to something important. Use it to expand on a point from the body text or to provide additional information.

**Caution**: Provide notice that a certain action or event could damage hardware or cause data loss.

**Warning**: Use to notify the reader of an issue to avoid loss of life, personal injury, and health hazards. Electrical and physical safety fall into this category.

{{< alert title="Tip" color="tip" >}}
The "title" and "color" keywords and the names of colors ("tip," "note," etc.) are case sensitive. If you use uppercase, Alerts will not have a title and the color border will be incorrect.
{{< /alert >}}

{{< figure src="/img/alert-markdown.png"  alt="The shortcodes used to display Alerts." title="Shortcodes for Alerts" >}}

{{< alert title="Tip" color="tip" >}}
Use for tips
{{< /alert >}}

{{< alert title="Info" color="tip" >}}
Use for extra background information
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

## Using the Figure Shortcode

The figure shortcode enhances the existing figure and figurecaption html tags. Figure supports the standard html attributes associated with the html img and figure tags, as well as an **attr** element for attribution text and **attrlink** if you wish to add a link to the attribution text.

{{< figure src="/img/figure-shortcode.png"  alt="The shortcode used to display an image, its caption, and its attribution." title="Figure Shortcode" >}}

This shortcode places the caption (i.e., the "title") above the table. The **title** is set in 12pt italic with a green underline.

Figure styles the Attribution text as body text.

## Demo of including another file

{{< readfile "/static/include/sample.md" >}}

Section content before this line is contained in an included file: /static/include/sample.md
