---
title: "Test File"
linkTitle: "Test"
weight: 1
draft: true
type: "docs"
description: "Information for writing docs with hugo - this is only rendered in test and dev environments."
---

## Reusable Text Snippets

There are situations where we need to repeat text blocks.
For example, when cautioning users to disconnect power before changing connections or providing a commonly used instruction set or procedure.

Rather than re-typing the material or making multiple copy/paste updates in many locations, you can simply update one file and its content flows to any location it was used.

The following is an example of the <file>secret-share.md</file> alert added using the snippet shortcode:

{{% figure src="/general/snippet-shortcode.png" alt="Snippet shortcode usage." title="Snippet Shortcode Usage" %}}

{{% snippet "secret-share.md" %}}

## Tab Panels

{{< tabs name="TabPanelExample" >}}
{{% tab name="Support"%}}
**Supported**

- Markdown and HTML images
  - Images should be included with the imgproc shortcode.
    You cannot directly use the `<img>` html tag for images in the assets folder because the images, once built, are renamed.
    If you really need to use html directly, place the image in the static folder.
- Alert Shortcode
- PRISM syntax highlighting (the three backticks)
- "codelang" highlighting (add codelang="language" to tab element).
  It's very ugly, needs css work, and is not recommended at this time.

### Not Supported

- Footnotes
- Expanders

### Example Usage

```md
# remove spaces
{ {<imgproc src="/general/tabbed-panel-markdown.png" resize="300x" declaredimensions=true alt="Screen capture of Tab/Tabs Shortcode Usage" style="border:solid 1px black">} }
```

{{<imgproc src="/general/tabbed-panel-markdown.png" resize="300x" declaredimensions=true alt="Screen capture of Tab/Tabs Shortcode Usage" style="border:solid 1px black">}}

{{% /tab %}}
{{% tab name="Examples" %}}

<div>
 <h3>What is Rendered?</h3>
 <p>It renders <i>vanilla</i> HTML and markdown, Alerts, and images.
 For example, these two images:</p>

- **Markdown Image Example**<br>
![expand example](/general/expander-markdown.png)<br>
- **HTML Image Example*- (with border)<br>
{{<imgproc src="/general/expander-markdown.png" resize="800x" declaredimensions=true alt="Screen capture of Tab/Tabs Shortcode Usage">}}

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

{{< alert title="Important" color="note" >}}
It can even contain shortcodes.
{{< /alert >}}

## Using Expanders

Expanders allow to you add long sections of code to your topic and hide them until the reader decides to view it.

Within the expander, you can still use most other shortcodes and syntax highlighting from Prism functions properly.
The shortcode displays your expander's title in a light blue bar to make it noticeable.<br><br>

**Screen Capture of an Expander**
{{<imgproc src="/general/expander-example.png" resize="1000x" declaredimensions=true alt="Screen capture of the expander control rendered on a documentation page" style="border:solid 1px black">}}

### Usage

1. Add the shortcode tags.
   Make sure that the title is suitable for your use.
1. Drop in the material you want to hide until the reader wants it.

### Markdown Example

{{<imgproc src="/general/expander-markdown.png" resize="400x" declaredimensions=true alt="ALT" style="border:solid 1px black">}}

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

**Info/Tip**: Use to convey helpful information or clarification.
They both use the same color.

**Note/Important/Stability Notice**: These call attention to something important.

**Caution**: Provide notice that a certain action or event could damage hardware or cause data loss.

**Warning**: Use to notify the reader of an issue to avoid loss of life, personal injury, and health hazards.
Electrical and physical safety fall into this category.

{{< alert title="Tip" color="tip" >}}
The "title" and "color" keywords and the names of colors ("tip," "note," and so on) are case sensitive.
If you use uppercase, alerts will not have a title and the color border will be incorrect.
{{< /alert >}}

{{< figure src="/general/alert-markdown.png"  alt="The shortcodes used to display Alerts." title="Shortcodes for Alerts" >}}

{{< alert title="Tip" color="tip" >}}
Provide a tip.
{{< /alert >}}

{{< alert title="Info" color="info" >}}
Use to expand on something from the body text or to provide additional information.
{{< /alert >}}

{{< alert title="Important" color="note" >}}
This is to call the reader's attention to something important.
{{< /alert >}}

{{< alert title="Stability Notice" color="note" >}}
Let the reader know that a feature is experimental and that breaking changes are likely to occur.
{{< /alert >}}

{{< alert title="Caution" color="caution" >}}
This provides notices that a certain action or event could damage hardware or cause data loss.
{{< /alert >}}

{{< alert title="Warning" color="warning" >}}
Use to notify the reader of information to avoid loss of life, personal injury, and health hazards.
{{< /alert >}}

## Using the Figure Shortcode

The figure shortcode enhances the existing figure and figurecaption html tags.
Figure supports the standard html attributes associated with the html img and figure tags, as well as an **attr*- element for attribution text and **attrlink*- if you wish to add a link to the attribution text.

{{< figure src="/general/figure-shortcode.png"  alt="The shortcode used to display an image, its caption, and its attribution." title="Figure Shortcode" >}}

This shortcode places the caption (that is the "title") above the table.
The **title*- is set in 12pt italic with a green underline.

Figure styles the Attribution text as body text.

## Demo of including another file

{{< readfile "/static/include/sample.md" >}}

Section content before this line is contained in an included file: <file>/static/include/sample.md</file>

## Videos

Our docs have two kinds of videos:

- Regular videos with video controls and audio
- GIF-like videos that do not have video controls or audio and function like GIFs

### Regular Videos

For regular videos that should use the video shortcode as follows:

```md
<!-- remove space -->
{ {<video webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart" poster="/general/heart.jpg">} }
```

{{<video webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart" poster="/general/heart.jpg">}}

We use `webm` and `mp4` source files for videos because they are generally smaller.
The poster is an image that gets loaded as a preview.

To create the `webm` and mp4 files use these commands:

{{< tabs >}}
{{% tab name="macOS" %}}

```sh {id="video-conversion-macos" class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec libx264 -vf "format=yuv420p,scale=720:-2" -b:v 300k PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec libx264 -vf "format=yuv420p,scale=720:-2" -b:v 300k PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c:v libvpx-vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{< /tabs >}}

The first command:

- uses the `libx264` codec
- uses the `yuv420p` pixel format
- scales the video to `720px` width
- changes the bitrate to `300k` - you can change this value but check that the result is usable and reasonably small

The second command:

- uses the `vp9` codec
- `-crf 41` sets the quality level.
  Valid values are 0-63.
  Lower numbers are higher quality

To create a preview image use this command:

{{< tabs >}}
{{% tab name="macOS" %}}

```sh {class="command-line" data-prompt="$"}
ffmpeg -ss 00:00:05 -i PATH_TO_GIF_OR_VID.mp4 -frames:v 1 PATH_TO_GIF_OR_VID.jpg
```

{{% /tab %}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
ffmpeg -ss 00:00:05 -i PATH_TO_GIF_OR_VID.mp4 -frames:v 1 PATH_TO_GIF_OR_VID.jpg
```

{{% /tab %}}
{{< /tabs >}}

The command takes a screenshot at `00:00:05`.

### GIF-like videos

GIF-like videos on our pages are generally used to show robot actions.
We do not use the GIF file format because it uses a lot of bandwidth - more than videos - and the [best practice](https://developer.chrome.com/en/docs/lighthouse/performance/efficient-animated-content/) is to not use them.

Instead, we use a video div with two sources:

```md
<!-- remove space -->
{ {<gif webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart">}}
```

{{<gif webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart">}}

**Place the files into the `static` directory.**

To create the `webm` and `mp4` source files, you need to convert the video/gif you have.
**The resulting `webm` and `mp4` file should always be less than 1MB.**
A good first thing to do is to upload the video to [Ezgif](https://ezgif.com) and reduce the file size by:

- cutting the video
- cropping the video
- changing the size
- (on GIFs) changing the quality
- (on GIFs) using the optimize function to remove every second frame and then adjusting the speed
- (on GIFs) using the frames editor to remove frames that are similar and holding the previous frame longer instead

Once you have a gif that is reasonably small, run these commands:

{{< tabs >}}
{{% tab name="macOS" %}}

```sh {class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec libx264 -vf "format=yuv420p,scale=400:-2" -b:v 300k -an PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec libx264 -vf "format=yuv420p,scale=400:-2" -b:v 300k -an PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c:v libvpx-vp9 -b:v 0 -crf 41 my-animation.webm
```

{{% /tab %}}
{{< /tabs >}}

The first command:

- uses the `libx264` codec
- uses the `yuv420p` pixel format
- scales the video to `400px` width - if you are working with screenshots that need to be bigger, adjust this number.
- changes the bitrate to `300k` - you can change this value but check that the result is usable
- removes the audiotrack with `-an`

The second command:

- uses the `vp9` codec
- `-crf 41` sets the quality level.
  Valid values are 0-63.
  Lower numbers are higher quality

{{< alert title="Caution" color="caution" >}}

Some MP4 files aren't natively supported on iPhones depending on the [video codec used](https://confluence.atlassian.com/confkb/unable-to-play-embedded-mp4-videos-on-ipad-or-iphone-in-confluence-305037325.html).
If you add an MP4 file, test it on an iPhone with the deployed link on the PR.

{{< /alert >}}

{{< alert title="Important" color="note" >}}
The gif can and should be used only in the frontmater `images` variable and only if close in size to 1MB.
The `images` variable sets it to be the preview image on social platforms (for example it will be the preview when you share a link on slack).
Link previews do not support `webm` and `mp4` but they do support gifs.
{{< /alert >}}

### Add video commands to terminal

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
ffmpeg -i ${vdirname}/${vfname}gif -c vp9 -b:v 0 -crf 41 -an ${vdirname}/${vfname}webm
}

function gif2mp4() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}gif -vcodec libx264 -vf "format=yuv420p,scale=400:-2" -b:v 300k -an ${vdirname}/${vfname}mp4
}

function gif2mp4-withsound() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}gif -vcodec libx264 -vf "format=yuv420p,scale=-2:720" -b:v 300k ${vdirname}/${vfname}mp4
}

function mp42webm() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}mp4 -c vp9 -b:v 0 -crf 41 -an ${vdirname}/${vfname}webm
}

function mp42webm-withsound() {
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
ffmpeg -i ${vdirname}/${vfname}webm -vcodec libx264 -vf "format=yuv420p,scale=400:-2" -b:v 300k -an ${vdirname}/${vfname}mp4
}

function webm2mp4-withsound() {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -i ${vdirname}/${vfname}webm -vcodec libx264 -vf "format=yuv420p,scale=-2:720" -b:v 300k ${vdirname}/${vfname}mp4
}

function mp42jpg {
vid=$1
ext=${vid##*.}
vdirname=`dirname $vid`
vfname=`basename $vid $ext`
ffmpeg -ss 00:00:05 -i ${vdirname}/${vfname}mp4 -frames:v 1 ${vdirname}/${vfname}jpg
}
```

{{< alert title="Important" color="note" >}}
The `2gif` commands only turn the first 5 seconds of a video into a low res gif.
{{< /alert >}}

## Images

**Place images in the `assets` folder.**

If the image is supposed to take up the full width of the page use the regular markdown syntax: `![alt text](path)`.

If the image is smaller use the `imgproc` shortcode with an appropriate resize value.

{{< alert title="Important" color="note" >}}

You cannot directly use the `<img>` html tag for images in the assets folder because the images, once built, are renamed.
If you really need to use html directly, place the image in the static folder.

{{< /alert >}}

```md
<!-- remove space -->
![Raspberry Pi](/installation/thumbnails/raspberry-pi-4-b-2gb.png)

{ {<imgproc src="/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x60" declaredimensions=true alt="Raspberry Pi">} }

{ {<imgproc src="/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x200" declaredimensions=true alt="Raspberry Pi">} }
```

![Raspberry Pi](/installation/thumbnails/raspberry-pi-4-b-2gb.png)

{{<imgproc src="/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x60" declaredimensions=true alt="Raspberry Pi">}}

{{<imgproc src="/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x200" declaredimensions=true alt="Raspberry Pi">}}

The `imgproc` shortcode will:

- convert the image into the `webp` format (which is more efficient) and resize the image
- resize the image in the current format and set that image as a backup in case `webp` is not supported

For more information on the resize options see [Image Processing](https://gohugo.io/content-management/image-processing/).

{{< alert title="Important" color="note" >}}
Only specify `declaredimensions` if the image is **not** responsive (if it doesn't resize).

An example of this are the small board icons on the front page which should never be a different size than they are.
The pictures in cards, however, need to resize because they change size based on the available screen space.
Screenshot images are as big as they can be generally but on mobile they're smaller.

Basically the only images that you'd want to use declaredimensions on are the ones that take up the same space on mobile as on desktop.

If it does resize, use the largest size the image can take up as the image to `resize` the image to.
{{< /alert >}}
