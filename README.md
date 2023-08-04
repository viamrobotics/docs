# Welcome to the Viam Documentation

> **Note**
> Looking to contribute? Check out the [Contributor Guide](https://github.com/viamrobotics/docs/blob/main/CONTRIBUTING.md).

## Build the docs locally

To be able to build the docs locally, you need to install the following:

- [`npm`](https://nodejs.org/en/download/)
- Hugo
  - macOS/Linux: `brew install hugo`
  - Windows: [https://gohugo.io/getting-started/installing/](https://nodejs.org/en/download/)

You can build the docs for local development using the following command:

```sh
make serve-dev-draft
```

If you would like to see the production view (without drafts and with minified CSS), run:

```sh
make serve-prod
```

You can also run `hugo serve` after installing Hugo to show the production view.

### Generate HTML docs

To generate the full HTML version of the docs run:

```sh
make build-prod
```

You can serve the resulting docs with:

```sh
python3 -m http.server 9000 --directory public
```

## Test the docs locally

To ensure your markdown is properly formatted, run `make markdowntest`.

To check for broken links run `make htmltest`.

## Publishing

The docs are automatically published when a PR merges.

## Hugo Quickstart

We write our docs in Markdown.
If you haven't used Markdown before, have a look at this [cheat sheet](https://twitter.com/github/status/1378429343563722759/photo/1) or look at some of the other docs in the `docs` folder for examples.

### Front Matter

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

#### Prod/Draft/Future Pages

Add `draft: true` to the Front Matter to set a page to Draft.
You can commit and push the page and it won’t display in production.
Add `future: true` to the Front Matter to begin building a page to production on a certain date (for example, a release date).

### Links

When linking to an image or another page in markdown, it's best to use a relative link.
For example, if you were writing in `viam/high-level-overview.md`, Hugo sees this as a directory on the site of `docs.viam.com/viam/`.

- To link to another markdown file in the same directory as the markdown file, use `[mylink](../installation/)`.
  **Note the trailing slash as another markdown file is another web directory in Hugo**
- To link to some image in the same directory as the markdown file, use `[mylink](../image1.png)`.
- To link something in a different directory, use `[mylink](/components/)`

We are also using `htmltest` to ensure links within the docs work.
To test locally, install [`htmltest`](https://github.com/wjdp/htmltest).

### Shortcodes

We have a number of special [shortcodes](https://www.docsy.dev/docs/adding-content/shortcodes/) that use HTML templates.

This is how you use them:

**Tabs**:

```md
{{< tabs name="Example tabs">}}
{{% tab name="Tab 1"%}}

This will be inside Tab 1.

{{% /tab %}}
{{% tab name="Tab 2"%}}

This will be inside Tab 2.

{{% /tab %}}
{{< /tabs >}}
```

**Alerts**:

```md
{{< alert title="Tip" color="tip" >}}
A helpful tip
{{< /alert >}}
```

**Expanders**:

```md
{{%expand "Click this to see what's inside" %}}
This will be visible if the reader clicks on the expander
{{% /expand%}}
```

### Footnotes

To add a footnote:

```md
"Some completely[^f] random text."

[^f]: this is the text for the footnote
```

You can place the footnote text immediately beneath the paragraph where you put the marker.
Hugo will place it at the bottom of the page.
