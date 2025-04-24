[![published](https://github.com/viamrobotics/docs/actions/workflows/docs.yml/badge.svg)](https://github.com/viamrobotics/docs/actions/workflows/docs.yml)
[![external link check](https://github.com/viamrobotics/docs/actions/workflows/run-htmltest.yml/badge.svg)](https://github.com/viamrobotics/docs/actions/workflows/run-htmltest.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/f7bff5c9-699f-4753-9166-ffa405290d67/deploy-status)](https://app.netlify.com/sites/viam-docs/deploys)

# Welcome to the Viam Documentation

> [!NOTE]
> Looking to contribute? Check out the [Contributor Guide](https://docs.viam.com/appendix/contributing/).
> For help knowing what and how to write, check out [tutorial template](docs/tutorials/template.md) and our [component pages](docs/operate/reference/components).

## Build the docs locally

To be able to build the docs locally, you need to install the following:

- [`npm`](https://nodejs.org/en/download/)
- Hugo
  - macOS/Linux: `brew install hugo`
  - Windows: [https://gohugo.io/getting-started/installing/](https://gohugo.io/getting-started/installing/)

You can build the docs for local development using the following command:

```console
make serve-dev
```

To see the production view (without drafts and with minified CSS), run:

```console
make serve-prod
```

> [!TIP]
> You can also run `hugo serve` after installing Hugo to show the production view.

### Generate HTML docs

To generate the full HTML version of the docs, run:

```console
make build-prod
```

You can serve the resulting docs with:

```console
python3 -m http.server 9000 --directory public
```

## Test the docs locally

### Python snippets

To ensure all Python snippets are properly formatted before creating a commit, install [flake8-markdown](https://github.com/johnfraney/flake8-markdown):

```console
brew install flake8
```

Then, add the following lines to the `.git/hooks/pre-commit` file in your local repository:

```sh
if [ "git diff --diff-filter=d --name-only HEAD | grep '\.md$' | wc -l" ];
then
list= $(git diff --diff-filter=d --name-only HEAD | grep '\.md$')
for item in $list
do
flake8-markdown $item
done
fi
```

If you don't already have a `.git/hooks/pre-commit` file in your `docs` git repo directory, you can copy the existing `pre-commit.sample` file in that directory as `pre-commit` to use the sample template, or create a new `pre-commit` file in that directory with the above content.
If you create a new file, you must also make it executable with: `chmod +x /path/to/my/.git/hooks/pre-commit`.

### Check markdown formatting

To ensure your markdown is properly formatted, run:

```console
make markdowntest docs/**/*`
```

### Check for broken links

To check locally for broken links, install [`htmltest`](https://github.com/wjdp/htmltest):

```console
brew install htmltest
```

Then, and run `make htmltest`.

### Lint JS and Markdown files with Prettier on save

1. Install the [Prettier VS Code Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).
1. Run `npm install` in the docs folder where you have the docs checked out.
1. Inside VS code, open the _user_ `settings.json` file: Press `CMD+SHIFT+P`, type 'settings', select **Open User Settings (JSON)**, and append the following settings to the end of the file:

```json
  "[markdown]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "prettier.configPath": ".prettierrc",
  "prettier.documentSelectors": ["**/*.md"],
  "prettier.prettierPath": "./node_modules/prettier/index.cjs",
  "prettier.withNodeModules": true,
  "prettier.resolveGlobalModules": true,
  "prettier.requirePragma": true
```

## Publishing

A GitHub workflow automatically publishes the docs to [https://docs.viam.com/](https://docs.viam.com/) when new commits appear in the `main` branch.
