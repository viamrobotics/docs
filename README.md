# Welcome to Viam Documenation

## Dependencies

* npm
  * Install 16 (LTS) via <https://nodejs.org/en/download/>.

* hugo
  * macOS/Linux: `brew install hugo`
  * Windows: <https://gohugo.io/getting-started/installing/>

## Local Development

* Production views
  * Standard production: `make serve-prod`
  * Production with draft files: `make serve-prod-draft`
  * Production with future files: `make serve-prod-future`
* Development views (likely not needed much)
  * Standard development: `make serve-dev`
  * Development with draft files: `make serve-dev-draft`
  * Development with future files: `make serve-dev-future`

## Building

This will build and serve public from a separate, non hugo server, at <http://localhost:9000>.

`make build-prod && python3 -m http.server 9000 --directory public`

## Publishing

This is handled automatically by a GitHub Action on push.

## Contributing

Don't hesitate to create a pull request. Every contribution is appreciated.

### Notes for contributors

- Don't make forks on the main repo, do in your own fork.
* Every sentence should be on a new line.
* Test locally before submitting a PR.
* Always submit a PR before merging.
* The author of the PR should merge unless they cannot and it's time-sensitive.

1. Fork the official repo into your personal GitHub.
2. The new forked copy is cloned to your local system.
3. Git remote path for the 'official' repository is added to the local clone: ```git remote add upstream git@github.com:viamrobotics/tutorials-and-docs.git```

When you are ready to contribute changes to the docs:

1. Make sure you are on the main branch: ```git switch main```
2. Sync your forked main branch with the official repo: ```git pull upstream main```
3. Create a new branch for your changes: ```git switch -c my-new-feature```
4. Edit some docs...
5. Commit your changes: ```git commit -am 'Add some feature'```
6. Make sure your local branch is still up-to-date with the official repo: ```git pull upstream main```
7. Push to the branch: ````git push origin my-new-feature````
8. Submit a pull request :D

## Important Things about Hugo

### Front Matter

```
---

title: "Build a line-following robot with only a rover and a webcam"

linkTitle: "Line Follower"

weight: 90

type: "docs"

description: "Instructions for building a line-following robot that uses a webcam to track lines."

---
```

* Hugo can display the description beneath the page title on the _index.html pages.
* The weight entry for  _index.html pages determines their placement as sections in the menu. The weight entry for each page in the directory determines that page’s placement in the section.
* Neglecting to add a weight entry causes Hugo to place the page at the very bottom of the menu.

### Linking

When linking to an image or another page in markdown, it's best to use a relative link. For example, if you were writing in `getting-started/high-level-overview.md`, hugo sees this as a directory on the site of `docs.viam.com/getting-started/high-level-overview/`.

* To link to another markdown file in the same directory as the markdown file, you would do e.g. `[mylink](../rpi-install/)`. **Note the trailing slash as another markdown file is another web directory in hugo**
* To link to some image in the same directory as the markdown file, you would do e.g. `[mylink](../img/image1.png)`.
* To link something in a different directory, you would do e.g. `[mylink](../../components/)`

### Prod/Draft/Future Pages

Add “Draft=true” to the Front Matter to set the page to Draft. Hugo will not build draft pages into production. You can commit and push the page and it won’t display in production. This could let you push the page to Main without displaying it in production, but let others access it locally from the git tree without changing the branch. To view the page locally, use `make serve-prod-draft` or `make serve-dev-draft`.

Add “Future=true” to the Front Matter to begin building a page to production on a certain date (e.g., a release date). This allows you to add a page in the production system and only display it from a selected date using Hugo's buildFuture build option in config.toml and the Future=true. To view the page locally prior to the date, use `make serve-prod-future` or `make serve-dev-future`.

#### Other Setup/Config Information

**LH Nav Menu**

Hugo builds the TOC from the pages under docs/. Because our docs use Page Bundles, each directory contains an _index.html file that serves as a landing page into that section. The following image is the_index.html page inside Getting Started:
<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

Hugo creates a section in the menu and applies the directory name as the page title for _index.html. Hugo lists all the pages in that section and can also display the descriptions (lead-in paragraph) beneath each link (if I can remember the setting).

**Top Banner Drop-Downs**

Hugo can build drop-downs for the top banner based on the settings contained in the config.toml file. The content can be pages or links. We aren’t using them yet.

**RH Menu**

This menu is a list of page sections and also has items to print or open a doc issue (not implemented in JIRA yet - We need Eric’s help to add this and feedback).

### The Index Files

There are two kinds: index.html and _index.html. The index.html works just as you’d expect. The_index.html is found inside page bundles, which are no more than a self-contained directory having the markdown files and image files under the same directory. We’re using _index.html files.
The_index.html file act as a landing page into the page bundle (i.e., directory). It lists the page title of each page in the bundle (you can have many pages) and can also display the lead-in paragraph (i.e., the description from the Front Matter) for the page.
The formatting works identically to MkDocs: it’s still markdown. But Hugo is better at handling basic html and the extra html that we need for some layout tasks. So now list indenting works as expected.

### Footnotes

To add a footnote:

```
“Some completely[^mfn] random text. “

[^mfn]: this is the text for the footnote
```

You can place the footnote text immediately beneath the paragraph where you dropped the marker. Hugo will place it at the bottom of the page.

### Text Wrapping

Nothing extra is required. Text wrapping works as expected in Hugo.
