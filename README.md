# Welcome to the Viam Documentation

> **Note**
> Looking to contribute? Check out the [Contributor Guide](https://docs.viam.com/appendix/contributing/).
> For help knowing what and how to write, check out our templates: our [tutorial template](docs/tutorials/template/) and [component page template](docs/components/component/) are accessible on the site when building the docs in Draft mode, or accessible here on GitHub.

## Build the docs locally

To be able to build the docs locally, you need to install the following:

- [`npm`](https://nodejs.org/en/download/)
- Hugo
  - macOS/Linux: `brew install hugo`
  - Windows: [https://gohugo.io/getting-started/installing/](https://gohugo.io/getting-started/installing/)

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

### Python snippets

To ensure all python snippets are properly formatted before creating a commit, install [flake8-markdown](https://github.com/johnfraney/flake8-markdown) and add the following lines to the `.git/hooks/pre-commit` file in your local repository:

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
If you create a new file, you must also make it executable with: `chmod 755 /path/to/my/.git/hooks/pre-commit`.

To ensure your markdown is properly formatted, run `make markdowntest`.

To check locally for broken links, install [`htmltest`](https://github.com/wjdp/htmltest) and run `make htmltest`.

### Lint JS and Markdown files with Prettier on save

1. Install the [Prettier VS Code Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).
2. Run `npm install` in the docs folder where you have the docs checked out.
3. Inside VS code, open user `settings.json` by pressing `CMD+SHIFT+P` and typing in settings, and ensure the following settings are in the file:

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

The docs are automatically published when a PR merges.
