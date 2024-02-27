---
title: "Contributing to the Docs"
linkTitle: "Contributing to the docs"
weight: 99
type: "docs"
description: "Learn about our style guide and how to work with hugo to contribute to these docs."
---

Thank you for wanting to help us make the docs better.
Every contribution is appreciated.

{{< alert title="Note" color="note" >}}
Before you start, please review this document and our [Code of Conduct](https://www.viam.com/community-guidelines).
{{< /alert >}}

## Goals

The Viam documentation aims to:

- Educate users (explain concepts, provide an overview of what is possible)
- Help users accomplish tasks (performing an action, building a thing)

We do that by providing concise and well-structured documentation to users.
When users stumble, we provide avenues for feedback, so we can take action and prevent other users from running into similar issues.

## Voice

We aim to be friendly but not colloquial, direct, and concise.

Here are a few additional pointers:

| Subject              | Judgment      |
| -------------------- | ------------- |
| Emoji ✨             | No            |
| Exclamation marks    | Use sparingly |
| Rhetorical questions | No            |

## Audience

We write for a technical audience that spans from entry-level to expert.
However, common tools and concepts such as version control, moving files with ssh, JSON are beyond the scope of our docs.
To make the content as accessible as possible we will, where possible, include actions to be taken and text that guides the user as to what they are achieving when performing these actions.

For example, when copying a file to another machine with ssh, we would describe the action with words like "Use ssh to move the file onto the other machine" alongside the command to move the file.
Explaining ssh goes beyond the scope of our docs.
Where needed, we will link to supporting documentation but not provide supporting documentation ourselves where it would duplicate existing external documentation.
Use your judgment to determine when we need to explain more and when we need to link to supporting content.
When in doubt, ask during review.

## Project structure

All documentation is in the [docs folder](https://github.com/viamrobotics/docs/tree/main/docs).
For information about Hugo and how to develop locally, see the [README](https://github.com/viamrobotics/docs/blob/main/README.md).

## Content types

When creating a new piece of content, decide which one of the four content types the content should be.
Note this in a comment in the front matter of the file.

The docs use the [Diátaxis Framework](https://diataxis.fr/) as the basis of the content structure with the following four content types:

- **Explanation (conceptual)**: An understanding-oriented piece of content.
  This content provides background knowledge on a topic and tends to be referenced in how-to guides and tutorials.
  For example the [Robot Development Kit page](https://docs.viam.com/internals/rdk/) or the [Registry page](https://docs.viam.com/registry/).
  It’s useful to have a real or imagined "Why?" question to serve as a prompt.

  {{% expand "Click to view template" %}}

  ```md
  # Concept

  Introductory paragraph.
  Possibly containing further subsections or links to relevant conceptual information.

  ## Subconcept

  Paragraphs containing explanation. Add imagery as needed.

  - Provide context and address potential points of confusion. - Add real or hypothetical examples.

  Possibly more Subconcept sections.

  ### Do x with subconcept (optional)

  Information on potential ways to apply the concept (possibly linking to how-tos or containing how-tos).

  ## Next steps

  Links to related content.
  ```

  {{% /expand %}}

- **How-to Guide (procedural)**: A task-oriented piece of content that directs a reader to perform actions step by step to complete a task, like a recipe.
  Generally starts with a description of the task and things to consider, and then provides a set of numbered steps to follow.
  For example, the [Installation page](https://docs.viam.com/get-started/installation/) or the [Find module page](https://docs.viam.com/registry/configure/).

  {{% expand "Click to view template" %}}

  ```md
  # Do This Task

  Description of task and considerations. Possibly containing further subsections.

  ## Do x

  1. Ordered list of actions to perform. Written in imperative form. Add imagery as needed.

  (possibly more Do X sections)

  ## Next steps

  Links to related content.
  ```

  {{% /expand %}}

- **Tutorial**: A learning-oriented piece of content that functions as a lesson for the reader.
  A tutorial helps readers to learn and apply skills by doing something meaningful and attainable.

  {{% expand "Click to view template" %}}

  ```md
  # Do X with Y

  Outline the why.
  Tell the story of the machine.
  Explain the machine's use and origin.

  ## Requirements

  What does the reader need to already know.
  What will you be using (hardware/software).

  ## Build X

  Build steps.

  ## Configure your X

  Configuration steps.

  ## Program your X

  Code and directions.

  ## Next steps

  Link to other tutorials with cards or text.

  {{</* cards */>}}
  {{%/* card link="/tutorials/get-started/blink-an-led" */%}}
  {{</* /cards */>}}
  ```

  For the full template see [template.md](https://github.com/viamrobotics/docs/blob/main/docs/tutorials/template.md).

  {{% /expand %}}

- **Reference**: A concise, information-oriented piece of content that generally starts with an overview/introduction and then a list of some kind (configuration options, API methods, etc.).
  Examples include the [API pages](https://docs.viam.com/build/program/apis/) as well as [component and service pages](https://docs.viam.com/components/arm/).

  Example template: [Component template](https://github.com/viamrobotics/docs/blob/main/docs/components/component/_index.md).

  {{% expand "Click to view template" %}}

  ```md
  # Product, Feature or API Name

  Description or introduction.
  Possibly containing further subsections.

  ## List or table of items (heading optional as needed)

  - Unordered list of options

  (possibly more information for each option)

  ## Next steps

  Links to related content.
  ```

  {{% /expand %}}

## Style guide

All docs are written in [Hugo Markdown](https://www.markdownguide.org/tools/hugo/).
Most Markdown formatting is supported.
For a brief introduction to Markdown, check out this [Markdown Cheatsheet](https://gist.github.com/npentrel/e1dd14816f7c7724edf70ab2a2ed2952).
Some additional formatting options are supported with [Hugo Shortcodes](https://gohugo.io/content-management/shortcodes/).

We follow the [Rackspace Style Guide](https://web.archive.org/web/20200829151826/https://developer.rackspace.com/docs/style-guide/) with many rules encoded in Vale rules.

### Vale linting

{{< alert title="Tip" color="tip" >}}
We recommend you work in Visual Studio Code and install the [Vale extension](https://marketplace.visualstudio.com/items?itemName=errata-ai.vale-server) to make use of the vale linter.
{{< /alert >}}

When you open a PR, your changes will be checked against a few style rules.
To run this check locally, follow the instructions in the [Vale Readme](https://github.com/viamrobotics/docs/blob/main/.github/vale/README.md).

### `markdownlint`

We recommend you work in Visual Studio Code and install the [markdownlint extension](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint).

### UI elements

Use **bold** text for UI elements, such as tabs and buttons.

### Example values

Use examples that resemble real data. For emails this could be `amanda@viam.com`.

When using placeholders in code examples, follow the [Google developer documentation style guide's rules for formatting placeholders](https://developers.google.com/style/placeholders).

### Images and screenshots

Use screenshots in introductory materials and where the surrounding text is not enough to direct the reader. Be aware that screenshots tend to get outdated quickly and come with a maintenance burden.

Rules for images:

- **Place images in the `assets` folder.** The folder uses the same content structure as the docs. Your images should be in the folder the page that uses it is in. However, there is no need to duplicate an image into multiple places if you use it in multiple pages.
- All images require alt text.
- All images **should** be smaller than 1MB. Hugo throws a warning during local builds (such as `make serve-prod`) if an image exceeds this size. Use an image compressor like [TinyPNG](https://tinypng.com/). This is to reduce the overall page and repo size.

#### Remove EXIF data automatically

{{< alert title="Important" color="note" >}}

To ensure that you do not accidentally add `EXIF` data on images, please install [exiftool](https://exiftool.org/install.html) and add the following lines to the `.git/hooks/pre-commit` file in your local repository.

```sh
if [ "git diff --name-only | grep -EI '.*(png|jpg|jpeg)$' | wc -l" ];
then
list= $(git diff --diff-filter=d --name-only | grep -EI ".*(png|jpg|jpeg)$")
for item in $list
do
exiftool -all= $item
done
fi
```

If you don't already have a `.git/hooks/pre-commit` file in your `docs` git repo directory, you can copy the existing `pre-commit.sample` file in that directory as `pre-commit` to use the sample template, or create a new `pre-commit` file in that directory with the above content.
If you create a new file, you must also make it executable with: `chmod 755 /path/to/my/.git/hooks/pre-commit`.

With this configuration in place, each commit you make will remove EXIF data from any image files (with extension `.png`, `.jpg`, or `.jpeg`) that are part of your commit.
{{< /alert >}}

#### Image markup

If the image is supposed to take up the full width of the page use the regular markdown syntax: `![alt text](path)`.

```md
![Raspberry Pi](/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png)
```

If the image is smaller use the `imgproc` shortcode with an appropriate resize value.

```md
<!-- Remove space between curly braces -->

{ {<imgproc src="PATH/TO/IMAGE.png" resize="300x" declaredimensions=true alt="ALT">} }

{ {<imgproc src="/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x60" declaredimensions=true alt="Raspberry Pi">} }

{ {<imgproc src="/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x200" declaredimensions=true alt="Raspberry Pi">} }
```

![Raspberry Pi](/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png)

{{<imgproc src="/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x60" declaredimensions=true alt="Raspberry Pi">}}

{{<imgproc src="/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png" resize="x200" declaredimensions=true alt="Raspberry Pi">}}

The `imgproc` shortcode will:

- convert the image into the `webp` format (which is more efficient) and resize the image
- resize the image in the current format and set that image as a backup in case `webp` is not supported. This does reduce file size when the website is being served. However, the source file should still be smaller than 1MB to minimize overall page and repo size. For more information on the resize options see [Image Processing](https://gohugo.io/content-management/image-processing/).

Only specify `declaredimensions` if the image is **not** responsive (if it doesn't resize). The only images that you'd want to use declaredimensions on are the ones that take up the same space on mobile as on desktop.

An example of this are the small board icons on the front page which should never be a different size than they are.
The pictures in cards, however, need to resize because they change size based on the available screen space.

Screenshot should most often be added with normal markdown syntax. Then they'll take up the max size they can on a big screen but be smaller on mobile. If you want to resize a large image, use the largest size the image can take up as the image to `resize` the image to.

{{< alert title="Note" color="note" >}}
You cannot directly use the `<img>` html tag for images in the assets folder because the images, once built, are renamed.
If you really need to use html directly, place the image in the `static` folder.
{{< /alert >}}

### GIFs and videos

We encourage the use of GIFs and Videos.
Our docs have two kinds of videos:

- Regular videos with video controls and audio
- GIF-like videos that do not have video controls or audio and function like GIFs

#### Regular videos

For regular videos that should use the video shortcode as follows:

```md
<!-- remove space -->

{ {<video webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart" poster="/general/heart.jpg">} }
```

{{<video webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart" poster="/general/heart.jpg">}}

We use `webm` and `mp4` source files for videos because they are generally smaller.
The poster is an image that gets loaded as a preview.

{{% expand "Click to see the commands for converting videos to these formats" %}}

To create the `webm` and mp4 files use these commands:

{{< tabs >}}
{{% tab name="macOS" %}}

```sh {id="video-conversion-macos" class="command-line" data-prompt="$"}
ffmpeg -i PATH_TO_GIF_OR_VID -vcodec libx264 -vf "format=yuv420p,scale=720:-2" -b:v 300k PATH_TO_GIF_OR_VID.mp4
ffmpeg -i PATH_TO_GIF_OR_VID -c:v libvpx-vp9 -b:v 0 -crf 41 my-animation.webm
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

- uses the `libvpx-vp9` codec
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

{{% /expand%}}

#### GIF-like videos

GIF-like videos on our pages are generally used to show robot actions.
We do not use the GIF file format within our docs because it uses a lot of bandwidth - more than videos - and the [best practice](https://developer.chrome.com/en/docs/lighthouse/performance/efficient-animated-content/) is to not use them.

Instead, we use a video div with two sources:

```md
<!-- remove space -->

{ {<gif webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart">}}
```

{{<gif webm_src="/heart.webm" mp4_src="/heart.mp4" alt="A robot drawing a heart">}}

**Place the files into the `static` directory.**

{{% expand "Click to see instructions for creating the video files" %}}
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
ffmpeg -i PATH_TO_GIF_OR_VID -c:v libvpx-vp9 -b:v 0 -crf 41 my-animation.webm
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

- uses the `libvpx-vp9` codec
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
{{% /expand%}}

{{% expand "Click to see instructions for creating video commands for your terminal" %}}

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

{{% /expand%}}

{{% alert title="Note" color="note" %}}

If you use `videos` to add a video preview for a page (such as to a tutorial), you should also add a <file>.gif</file> version of the video to the front matter.
Hugo uses the GIF as a link preview image that gets displayed on external sites when someone shares the link, for example on Slack or Twitter.

Why?

- GIFs take more bandwidth than MP4 and WEBM videos, so on our page, we prefer to use MP4 and WEBM.
- Link previews using `og:image` only support GIFs
- Automatic conversion between the formats is possible but we also need to make sure that the resulting GIFs are presentable and under 1MB.

{{% /alert %}}

## Formatting guide

### Front matter

Each file that generates a page in Hugo starts with front matter that looks like this:

```markdown
---
title: "Build a line-following robot with only a rover and a webcam"
linkTitle: "Line Follower"
weight: 90
type: "docs"
description: "Instructions for building a line-following robot that uses a webcam to track lines."
# SME: "SME Name"
---
```

- The `description` gets used for previews.
- The `weight` determines the ordering of pages in the side navigation bar.

#### Prod/Draft/Future pages

Add `draft: true` to the Front Matter to set a page to Draft.
You can commit and push the page and it won’t display in production.
Add `future: true` to the Front Matter to begin building a page to production on a certain date (for example, a release date).

### File names

File names are kebab-case, with hyphens, such as `upload-model.md`.

### One sentence per line

To make reviews easier, each new sentence should begin on a new line.

### Add hyperlinks (sparingly)

Where related resources would be helpful to a reader, link them. However:

- Links are an opportunity for a reader to get lost or get distracted. If that happens, a link is not helpful. Placing links near the end of a section/page can help avoid this.
- Avoid a page becoming a sea of blue hyperlinks. Excessive linking can make a page harder to view and read.

{{< alert title="Important" color="note" >}}
Links should always have descriptive text. Never write "Click here" with `here` as the link text. Instead use "To learn more about X, read PAGE NAME" with the page name as the link text.
{{< /alert >}}

When linking to an image or another page within the docs please use relative links (`appendix/contributing/`) or (`/appendix/contributing/`).

{{< alert title="Note" color="note" >}}
You **must** add a trailing slash on links.\*\*
This is enforced with `htmltest`.
{{< /alert >}}

### Glossary

We have built a glossary into our docs. Jargon and product-specific concepts should have an entry in the `appendix/glossary` folder. You can use a glossary entry on any page like this:

```md
<!-- Remove spaces between curly braces -->

This text will have additional information on hover for the
word { {< glossary_tooltip term_id="smart-machine" text="smart machine" >} }.
```

### Reusable text snippets

If you need to use the same text in multiple locations, for example when cautioning users to disconnect power before changing connections or providing a commonly used instruction set or procedure, you can use reusable snippets.

The following is an example of the <file>secret-share.md</file> alert added using the snippet shortcode:

{{% figure src="/general/snippet-shortcode.png" alt="Snippet shortcode usage." title="Snippet Shortcode Usage" %}}

{{% snippet "secret-share.md" %}}

### Including another file

{{< readfile "/static/include/sample.md" >}}

Section content before this line is contained in an included file: <file>/static/include/sample.md</file>

### Tab Panels

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

### Not supported

- Footnotes
- Expanders

### Example usage

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
- **HTML Image Example** (with border)<br>
  {{<imgproc src="/general/expander-markdown.png" resize="800x" declaredimensions=true alt="Screen capture of Tab/Tabs Shortcode Usage">}}

</div>
<br>

{{% /tab %}}
{{< /tabs >}}

### Code with syntax highlighting

Line numbering is off by default.

```json {class="line-numbers linkable-line-numbers"}
{
  "word": "Three backticks and the language name enables Prism syntax highlighting."
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

### Alert shortcodes

{{< alert title="Important" color="note" >}}
This is an alert.
{{< /alert >}}

#### How to use notes, cautions, and warnings

**Info/Tip**: Use to convey helpful information or clarification.
They both use the same color.

**Note/Important/Stability Notice**: These call attention to something important.
When creating alerts about important messages, set the title attribute as `title="Important"`.
If you want to include a more detailed title or message, use `title="Important: $message"` to provide additional context.

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

### Using expanders

Expanders allow to you add long sections of code to your topic and hide them until the reader decides to view it.

Within the expander, you can still use most other shortcodes and syntax highlighting from Prism functions properly.
The shortcode displays your expander's title in a light blue bar to make it noticeable.<br><br>

**Screen Capture of an Expander**
{{<imgproc src="/general/expander-example.png" resize="1000x" declaredimensions=true alt="Screen capture of the expander control rendered on a documentation page" style="border:solid 1px black">}}

#### Usage

1. Add the shortcode tags.
   Make sure that the title is suitable for your use.
1. Drop in the material you want to hide until the reader wants it.

{{<imgproc src="/general/expander-markdown.png" resize="400x" declaredimensions=true alt="ALT" style="border:solid 1px black">}}

{{%expand "Click to view the source" %}}
<br>

Add the text to hide here.

**Prism syntax highlighting works in expanders, as do most other shortcodes.**

```python
print("Code snippets work")
```

{{% /expand%}}

### Figures

The figure shortcode enhances the existing figure and figurecaption html tags.
Figure supports the standard html attributes associated with the html img and figure tags, as well as an **attr** element for attribution text and **attrlink** if you wish to add a link to the attribution text.

{{< figure src="/general/figure-shortcode.png"  alt="The shortcode used to display an image, its caption, and its attribution." title="Figure Shortcode" >}}

This shortcode places the caption (that is the "title") above the table.
The **title** is set in 12pt italic with a green underline.

Figure styles the Attribution text as body text.

### Footnotes

To add a footnote:

```md
"Some completely[^f] random text."

[^f]: this is the text for the footnote
```

You can place the footnote text immediately beneath the paragraph where you put the marker.
Hugo will place it at the bottom of the page.

## Pull requests

If you are making a small change, like fixing a typo or editing a few lines of text, you do not need to create an issue.
However, if you plan to make bigger changes, we ask that you create an issue and discuss the change with us in advance.

To get started:

1. Fork the official repo into your personal GitHub.
2. Clone the forked repo to your local system.
3. Add the remote path for the 'official' repository: `git remote add upstream git@github.com:viamrobotics/docs.git`

When you are ready to contribute changes to the docs:

1. Make sure you are on the main branch: `git switch main`
2. Sync your forked main branch with the official repo: `git pull upstream main`
3. Create a new branch for your changes: `git switch -c my-new-feature`
4. Edit some docs...
5. Commit your changes: `git commit -am 'Add some feature'`
6. Make sure your local branch is still up-to-date with the official repo: `git pull upstream main`
7. Push to the branch: `git push origin my-new-feature`
8. Submit a pull request

## Questions

If you have questions or would like to chat, please find us on the [Community Discord](https://discord.gg/viam).
