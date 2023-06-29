---
title: "Test File"
linkTitle: "Test"
weight: 1
draft: true
type: "docs"
description: "Information for writing docs with hugo - this is only rendered in test and dev environments."
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

- Markdown and HTML images.
- Alert Shortcode
- PRISM syntax highlighting (the three backticks)
- "codelang" highlighting (add codelang="language" to tab element). It's very ugly, needs css work, and is not recommended at this time.

### Not Supported

- Footnotes
- Expanders

### Example Usage

<img style="border:solid 1px black" alt="Screen capture of Tab/Tabs Shortcode Usage" src="/img/tabbed-panel-markdown.png">

{{% /tab %}}
{{% tab name="Examples" %}}

<div>
 <h3>What is Rendered?</h3>
 <p>It renders <i>vanilla</i> HTML and markdown, Alerts, and images. For example, these two images:</p>

- **Markdown Image Example**<br>
![expand example](/img/expander-markdown.png)<br>
- **HTML Image Example*- (with border)<br>
<img style="border:solid 1px black" src="/img/expander-markdown.png" alt="Screen capture of Tab/Tabs Shortcode Usage">

</div>
<br>

{{% /tab %}}
{{< /tabs >}}

## You can use `code` in headers

[You can use `code` in links](www.viam.com)

### Syntax Highlighting with Backticks

Line numbering is off by default.

```json {class="line-numbers linkable-line-numbers"}
{
"word":"As before, three backticks and the language name enables Prism syntax highlighting.",
}
```

With just line 6 highlighted.
See [the prism line highlight extension](https://prismjs.com/plugins/line-highlight/) for more info:

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

Within the expander, you can still use most other shortcodes and syntax highlighting from Prism functions properly. The shortcode displays your expander's title in a light blue bar to make it noticeable.<br><br>

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
motion_svc = MotionClient.from_robot(robot, "NAME")
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

**Info/Tip**: Use to convey helpful information or clarification. They both use the same color.

**Note**: These call attention to something important. Use it to expand on a point from the body text or to provide additional information.

**Caution**: Provide notice that a certain action or event could damage hardware or cause data loss.

**Warning**: Use to notify the reader of an issue to avoid loss of life, personal injury, and health hazards. Electrical and physical safety fall into this category.

{{< alert title="Tip" color="tip" >}}
The "title" and "color" keywords and the names of colors ("tip," "note," and so on) are case sensitive. If you use uppercase, Alerts will not have a title and the color border will be incorrect.
{{< /alert >}}

{{< figure src="/img/alert-markdown.png"  alt="The shortcodes used to display Alerts." title="Shortcodes for Alerts" >}}

{{< alert title="Tip" color="tip" >}}
Use for tips
{{< /alert >}}

{{< alert title="Info" color="info" >}}
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

The figure shortcode enhances the existing figure and figurecaption html tags. Figure supports the standard html attributes associated with the html img and figure tags, as well as an **attr*- element for attribution text and **attrlink*- if you wish to add a link to the attribution text.

{{< figure src="/img/figure-shortcode.png"  alt="The shortcode used to display an image, its caption, and its attribution." title="Figure Shortcode" >}}

This shortcode places the caption (that is the "title") above the table. The **title*- is set in 12pt italic with a green underline.

Figure styles the Attribution text as body text.

## Demo of including another file

{{< readfile "/static/include/sample.md" >}}

Section content before this line is contained in an included file: /static/include/sample.md

## GIFs and Videos

There are a few issues to consider with these:

- Some MP4 files aren't natively supported on iPhones.
  If you add an MP4 file, test it on mobile with the deployed link on the PR.
- GIFs use a lot of bandwidth.
  More than videos.
  The [best practice](https://developer.chrome.com/en/docs/lighthouse/performance/efficient-animated-content/) is to not use them.

Instead use a video div with two sources and a poster that gets loaded as a preview:

```md
<!-- remove space -->
{ {<video webm_src="../img/heart.webm" mp4_src="../img/heart.mp4" alt="A robot drawing a heart" poster="../img/heart.jpg">} }
```

{{<video webm_src="../img/heart.webm" mp4_src="../img/heart.mp4" alt="A robot drawing a heart" poster="../img/heart.jpg">}}

or if you want a video without controls - mimicking a GIF:

```md
<!-- remove space -->
{ {<gif webm_src="../img/heart.webm" mp4_src="../img/heart.mp4" alt="A robot drawing a heart">}}
```

{{<gif webm_src="../img/heart.webm" mp4_src="../img/heart.mp4" alt="A robot drawing a heart">}}

And to create the source files you can use [Ezgif gif to mp4](https://ezgif.com/gif-to-mp4) and [Ezgif gif to webm](https://ezgif.com/gif-to-webm) or run these commands:

{{< tabs >}}
{{% tab name="macOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec hevc_videotoolbox -b:v 2000k -tag:v hvc1 -c:a eac3 -b:a 224k PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{% tab name="Linux" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -b:v 2000k -c:a eac3 -b:a 224k PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c:v libvpx-vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{< /tabs >}}

If you'd like to use commands like `webm2mp4` add this to your `.zshrc`:

```sh
function webm2gif() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -t 8 -i ${vdirname}/${vfname}webm -vf "fps=5,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ${vdirname}/${vfname}gif
}

function mp42gif() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -t 8 -i ${vdirname}/${vfname}mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ${vdirname}/${vfname}gif
}

function gif2webm() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}gif -c vp9 -b:v 0 -crf 41 ${vdirname}/${vfname}webm
}

function gif2mp4() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}gif -vcodec hevc_videotoolbox -b:v 2000k -tag:v hvc1 -c:a eac3 -b:a 224k ${vdirname}/${vfname}mp4
}


function mp42webm() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}mp4 -c vp9 -b:v 0 -crf 41 ${vdirname}/${vfname}webm
}

function webm2mp4() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}webm -vcodec hevc_videotoolbox -b:v 2000k -tag:v hvc1 -c:a eac3 -b:a 224k ${vdirname}/${vfname}mp4
}

function mp42jpg {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}mp4 -vf "select=eq(n\,0)" -q:v 3 ${vdirname}/${vfname}jpg
}
```

{{< alert title="Note" color="note" >}}
The `2gif` commands only turn the first 5 seconds of a video into a low res gif.
{{< /alert >}}
