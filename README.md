# Welcome to Hugo

We’ve ported the documentation to Hugo. Hugo is more versatile than MkDocs and provides a better platform for our docs.

## What you’ll need to do:

**Install Hugo**: [https://gohugo.io/getting-started/installing/](https://gohugo.io/getting-started/installing/)

On Mac: 
```
brew install hugo
```

On windows: Chocolatey

**New Doc Path**: docs

## Running Locally

Run Hugo from the tutorials-and-docs directory where config.toml is located.

View the Prod version:

```
hugo server
```

View the Draft version (show files marked as Draft)

```
hugo server -D
```

View the Future version (Show files marked as Future, which could allow us to prep a release’s new pages ahead of time and only show them on the release date)

```
hugo server -F
```

## Notes for those editing docs
- every sentence on a new line
- test locally before submitting a PR
- always submit a PR before merging
- the authoer of PR should merge unless they cannot and it's time sensitive

## Important Things about Hugo


### Front Matter

Please note the differences between the two versions:  

**MkDocs Version**:

---

title: Build a line following robot with only a webcam

summary: Instructions for building a line following robot that uses a webcam to track lines.

authors:

    - Jessamy Taylor

date: 2022-08-18

—

**Hugo Version**:

---

title: "Build a line following robot with only a rover and a webcam"

linkTitle: "Build a line following robot with only a rover and a webcam"

weight: 90

type: "docs"

description: "Instructions for building a line following robot that uses a webcam to track lines."

---

Hugo can display the description beneath the page title on the _index.html pages.

The weight entry for  _index.html pages determines their placement as sections in the menu. The weight entry for each page in the directory determines that page’s placement in the section.

Neglecting to add a weight entry causes Hugo to place the page at the very bottom of the menu. 

### Prod/Draft/Future Pages

Add “Draft=true” to the Front Matter to set the page to Draft. Hugo will not build draft pages into production. You can commit and push the page and it won’t display in production. This could let you push the page to the Master without displaying it in production, but let others access it locally from the git tree without changing the branch. To view the page locally, use the -D option: \
hugo server -D

Add “Future=true” to the Front Matter to begin building a page to production on a certain date (e.g., a release date). This allows you to add a page in the production system and only display it from a selected date using Hugo's buildFuture build option in config.toml and the Future=true. To view the page locally prior to the date, use the -F option: \
hugo server -F

#### Other Setup/Config Information

**LH Nav Menu**

Hugo builds the TOC from the pages under content/en. Because our docs use Page Bundles, each directory contains an _index.html file that serves as a landing page into that section. The following image is the _index.html page inside Getting Started:

<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

Hugo creates a section in the menu and applies the directory name as the page title for _index.html. Hugo lists all the pages in that section and can also display the descriptions (lead-in paragraph) beneath each link (if I can remember the setting).

**Top Banner Drop-Downs**

Hugo can build drop-downs for the top banner based on the settings contained in the config.toml file. The content can be pages or links. We aren’t using them yet.

**RH Menu**

This menu is a list of page sections and also has items to print or open a doc issue (not implemented in JIRA yet - We need Ed’s help to add this and feedback).


### The Index Files

There are two kinds: index.html and _index.html. The index.html works just as you’d expect. The _index.html is found inside page bundles, which are no more than a self-contained directory having the markdown files and image files under the same directory. We’re using _index.html files.

The _index.html file act as a landing page into the page bundle (i.e., directory). It lists the page title of each page in the bundle (you can have many pages) and can also display the lead-in paragraph (i.e., the description from the Front Matter) for the page.

The formatting works identically to MkDocs: it’s still markdown. But Hugo is better at handling basic html and the extra html that we need for some layout tasks. So now list indenting works as expected.


### Footnotes

To add a footnote:

“Some completely[^mfn] random text. “

[^mfn]: this is the text for the footnote

You can place the footnote text immediately beneath the paragraph where you dropped the marker. Hugo will place it at the bottom of the page.


### Text Wrapping

Nothing extra is required. Text wrapping works as expected in Hugo.


