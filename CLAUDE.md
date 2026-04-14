# CLAUDE.md

## Pre-PR checks for viam-docs

Run these checks from the worktree directory before committing or pushing. All four must pass.

### 1. Format with prettier

```bash
npx prettier --write docs/[section]/**/*.md
```

Prettier auto-formats markdown. Run with `--write` to fix in place, or `--check` to see what would change without modifying files.

### 2. Lint markdown structure

```bash
npx markdownlint-cli --config .markdownlint.yaml docs/[section]/**/*.md
```

Catches structural issues: fenced code blocks without language tags, inconsistent list markers, heading levels, etc. Fix errors manually.

### 3. Check prose style with vale

```bash
vale sync
vale docs/[section]/
```

`vale sync` downloads the latest style rules. `vale` then checks for style violations: em dashes, "e.g.", "via", "(s)" plurals, title case in headings, and other Viam style rules. Fix errors manually.

### 4. Build the full site

```bash
make build-prod
```

This runs a production Hugo build. It catches broken shortcodes, missing pages referenced by links, invalid frontmatter, and template errors. Warnings about old page dates are expected and can be ignored. The build must complete without errors.

### 5. Spot-check in the browser (optional but recommended)

Kill any running Hugo servers, clear the `public/` directory, and start a fresh dev server:

```bash
pkill -f "hugo server"
rm -rf public/
hugo server --port 1313 --disableFastRender
```

Open the changed pages in a browser and verify they render correctly.

### Order matters

Run prettier first because it can change line breaks that affect markdownlint results. Run vale after markdownlint because some markdownlint fixes (like adding language tags to code blocks) can resolve vale false positives. Run `make build-prod` last because it is the slowest and catches the broadest class of errors.
