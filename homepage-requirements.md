# Docs homepage requirements

Status: draft for feedback. A working prototype is built on this branch (see "Prototype status" at the end).
Reviewers: marketing, education team and VP, technical writers.

## Problem

`docs.viam.com/` has no landing page.
`docs/_index.md` uses an empty layout with `canonical: "/what-is-viam/"`, so every visitor lands on the "What is Viam?" concept page.
That page serves readers who are new to Viam, but it doesn't help:

- returning users who want reference material (APIs, SDKs, CLI, MCP server)
- people who want to start building right away
- anyone deciding between docs, workshops, and courses, since nothing explains how the three differ

The top nav adds to the confusion: "Tutorials" and "Courses" sit next to each other with no context.

## Goals

1. Replace the redirect at `/` with a real homepage.
2. Give each audience relevant links without splitting the page into audience sections:
   - **New to Viam**: a platform overview (What is Viam?), a course, a beginner-friendly workshop
   - **Ready to build**: set up a machine, configure hardware, workshops
   - **Returning or reference users**: direct links to the MCP server, APIs, SDKs, CLI, and the left sidebar
3. Explain in one line each what docs, workshops, and courses are.
4. Rename the "Tutorials" nav label to "Workshops."
5. Make the content easy to keep current: editing a featured link or course is a one-line data change, not a template change.

## Non-goals (for this iteration)

- Changing the `/tutorials/` URL. Only the label changes. A URL move affects aliases, the Typesense index, `/tutorials/catalog.md`, and `llms.txt`, so it gets its own PR later.
- Reorganizing the short single-feature tutorials. For now, "Workshops" covers everything in `docs/tutorials/`.
- Adding search to the homepage body. Search stays in the top bar.
- Personalization or analytics-driven content.

## Page content

Section order on the page, top to bottom.
Every section is mandatory unless marked optional.

### 1. Hero

A headline and a one- or two-sentence description of Viam. Marketing to review the copy.

### 2. Announcement banner (optional)

A slim lime (`#c4f400`, the viam.com call-to-action color) banner directly below the hero description highlights one new feature, doc, workshop, or course, for example "New: Learn how to train a VLA with Viam. Get started →".
The whole banner is one link.
It's controlled by the `announcement` block in `data/homepage.yaml`: `enabled` turns it on or off, and `label`, `text`, `link_text`, and `path` (a docs page) or `url` (anything else) set its content.
Lime is the only color. The Markdown mirror includes the banner as a one-line quote.

### 3. Ways to learn

Explains the difference between learning formats, and gives new, building, and returning readers their starting links:

- **Docs**, full width: "Concepts, how-to guides, and reference for every part of the platform." It holds three links, each with a short label and one-line description: What is Viam? (Understand), Set up a machine (Build), and Reference (Look up: APIs, SDKs, the CLI, and the MCP server). Side by side when there's room, stacked on phones.
- **Workshops** and **Courses**, side by side below Docs:

| Card      | One-line description (draft)                                                          | Link                     |
| --------- | ------------------------------------------------------------------------------------- | ------------------------ |
| Workshops | Guided, multi-hour projects that take you from unboxing to a working robot.           | `/tutorials/`            |
| Courses   | Free, structured courses with videos and checkpoints, many with no hardware required. | `https://learn.viam.com` |

To the education team: please check the course description.

### 4. Featured workshops

Three tiles in a row on desktop, stacked on phones:

- Miniature palletizing with the SO-ARM101 (`/tutorials/so-arm101-palletizing/`)
- Vision-guided pick-and-place with the xArm6 (`/tutorials/pick-and-place/`), using the new workstation photo, which also replaces the photo at the top of that workshop's page (same file, `assets/tutorials/pick-and-place/hero-hardware-overview.jpeg`)
- An "All workshops" tile (title only) linking to `/tutorials/`

Long descriptions are cut off at three lines so the tiles stay compact.
Each tile's image, alt text, and optional crop focal point (`focus`) are set in `data/homepage.yaml`.

### 5. Featured courses

Mirrors featured workshops: two highlighted courses from `data/courses.yaml` (default: Viam 101 and SO-101) and an "All courses" tile (title only) linking to `https://learn.viam.com`. Courses have no images.
To the education team: which courses should be highlighted, and should the pick rotate?

### 6. Popular guides and reference

Two plain lists of links, side by side on wider screens, with no descriptions:

- **Popular guides:** Set up a machine, Configure hardware, Move an arm, Train a model, Set up the MCP server
- **Reference:** MCP server, APIs, SDKs, CLI, All reference

The Markdown mirror adds each page's own description to these links for agents.
Possible future guides: capture and sync data (`/data/`), use Viam from an AI agent (`/build-apps/use-viam-from-an-agent/`), write a module (`/build-modules/`).

### 7. Footer strip

Kept visually quiet:

- viam.com
- Discord (`https://discord.gg/viam`)
- GitHub (`https://github.com/viamrobotics/`)

Community links live in `data/homepage.yaml` with the rest of the homepage content.

## Layout

The homepage is a standard docs page with the left sidebar, so returning users see the whole information architecture right away.
It uses the normal `docs` layout (no table of contents column), and the old `frontpage` class that hid the sidebar on `/` is gone.
An earlier prototype also had a full-width layout without the sidebar (option A). This version replaces both options.

## Nav changes

- `docs/tutorials/_index.md`: change `linkTitle` (and `title`) from "Tutorials" to "Workshops." The URL stays `/tutorials/`. Templates that matched the literal title "Tutorials" (`footer.html`, `rss.xml`, `sidebar-tree.html`) now match the `/tutorials/` URL instead, so a future rename can't silently break them.
- Other hardcoded labels now say "Workshops": the sidebar headings in `sidebar-tree.html` and `sidebar-workshop.html`, the "Browse all workshops" link in `layouts/docs/tutorials.html`, and the `/tutorials/all/` page title ("All Workshops").
- Not renamed: the "Tutorials" tab in the Ask AI search widget (`assets/js/inkeep.js`). It's tied to the search index configuration, so renaming it needs a separate change.

## Technical requirements

- **Data-driven content.** Featured workshops, articles, and reference links live in `data/homepage.yaml`. Courses come from the existing `data/courses.yaml`.
- **Remove the canonical redirect from `docs/_index.md`.** Its `aliases` (for example, `/get-started/` and `/platform/`) move to `docs/what-is-viam/_index.md`, so those old URLs keep landing on "What is Viam?" instead of the new homepage.
- **Frontmatter checks.** The home page needs `diataxis: overview` once it stops being a redirect stub (`scripts/frontmatter_rules.py`).
- **Markdown mirror.** `/index.md` (and the `llms.txt` / `sitetree.json` root entry) should render the homepage's links as a Markdown list, not raw HTML. The Markdown mirror must stay useful to agents.
- **Mobile first.** Write the base styles for a phone-width single column, and add columns with `min-width` container queries as the space widens. Container queries (not media queries) size the layout by the width the homepage actually gets next to the sidebar. Nothing should depend on hover, overflow sideways, or need horizontal scrolling at 360px. Tap targets are at least 44px tall. Check every change at 360px, 768px, and desktop widths. The Courses top-nav item is already hidden on phones, so the homepage's Courses section is the main path to courses on mobile.
- **Accessibility.** Mark external links with the existing external-link icon and screen-reader text. Images need alt text, set per tile in `data/homepage.yaml`.
- **SEO.** Keep `sitemap.priority: 1.0`. Write a real `description` for the meta tag.

## Open questions for reviewers

1. **Marketing:** Hero headline and description. Is a link back to viam.com in the footer strip enough, or should there be a CTA such as "Sign up free"?
2. **Education:** Which courses to highlight, and the "Ways to learn" course description.
3. **Writers:** The popular-guides list.

## Known issues

- The pick-and-place workshop page says the robot places blocks "in the bin," but the new photo shows a wooden board and no bin.
- On phones, the site's top navbar is about 10px wider than the screen on every page, so pages scroll sideways slightly. This existed before this project and is tracked separately.

## Before merging

- Point the announcement banner at the real VLA page or course. It currently links to "Train a model" as a placeholder. Or set `enabled: false`.
- Apply reviewer copy changes in `data/homepage.yaml`.
- Delete this file, or move it out of the repo root.

## Prototype status

Done: `data/homepage.yaml`, the sidebar layout, the Workshops rename, the announcement banner, the new pick-and-place photo, and passing pre-PR checks (prettier, markdownlint, vale, frontmatter, `make build-prod`).
Next: open a draft PR to get a Netlify deploy preview link for reviewers.
