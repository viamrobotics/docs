This folder contains a [Vale-compatible](https://github.com/errata-ai/vale) implementation of the *Viam Documentation Style Guide*.

## Getting Started

The following will install vale globally.
### Global Installation [Recommended]

> :exclamation: Viam requires Vale >= **1.0.0**. :exclamation:

1. Install `vale`. If you do not have `brew` installed follow [these
   installation instructions](https://docs.errata.ai/vale/install).
   ```sh
   brew install vale
   ```
3. In your docs repo run the following:
   ```sh
   pwd
   ```
4. Depending on your chosen shell, open up your `~/.bashrc` or
   `~/.zshrc` file and append the following lines swapping out VALEDIR
   for the output you received in the previous step:
   ```sh
   export PATH=$PATH:VALEDIR/.github/vale/bin
   alias vale="vale --config VALEDIR/.vale.ini"
   # Example of both
   # export PATH=$PATH:/Users/naomi/coding/viam-docs/.github/vale/bin
   # alias vale="vale --config /Users/naomi/coding/viam-docs/.vale.ini"
   ```
5. If you want to be able to run vale from anywhere, open the `vale-check` script inside `.github/vale/bin`
   and change the link to .vale.ini to the full file path:
   step 3.

   Example file:
   ```sh
   #! /bin/bash

   vale --config /Users/naomi/coding/vale-viam/.vale.ini $(git diff --diff-filter=d --name-only $1)
   ```

   Optionally, if you want to have the ability to run `markdown-check` locally, open up the `markdown-check` script inside
   the `bin` folder and add the full file path for .markdownlint.yaml.

   Example file:
   ```sh
   #! /bin/bash

   markdownlint --config /Users/naomi/coding/vale-viam/.markdownlint.yaml $(git diff --diff-filter=d --name-only $1 | grep '\.md$')
   single-line-check HEAD

   # USAGE: markdown-check HEAD~
   ```

6. Run `source ~/.bashrc` or `source ~/.zshrc`. Or restart your terminal.

7. To run `vale` against a file use:
   ```sh
   vale /path/to/file
   ```
   Inside vale folder in .github, you can run `vale test.rst` to run vale on an
   example file.

8. If you want to run vale against all files that have changed since a given commit hash use the `vale-check` wrapper:
   ```sh
   vale-check <HASH>
   # example: vale-check
   # example: vale-check HEAD
   # example: vale-check HEAD~3
   # example: vale-check abc123
   ```

## Usage

To learn how to use Vale, see [Usage](https://github.com/errata-ai/vale/#usage).

### Turning Rules Off

To turn off a given rule open the `.vale.ini` file and set the respective variable to `NO`. Example:

```ini
Vale.Abbreviations = NO
```

### Using Vale in VSCode

> **NOTE**: Please follow the steps in Getting Started first!

1. Install the [vale extension](https://marketplace.visualstudio.com/items?itemName=errata-ai.vale-server)
2. Navigate to the vale extension settings:
   * Specify the absolute path to the `.vale.ini` file for `Vale CLI: Config`. The file is in the repo you cloned in `Getting Started`.
   * Set the min alert level to `suggestion` - a lot of the rules are coded as suggestions.
   * Specify the path to your vale installation. To find this path run `where vale` in your terminal and copy the path.
     This path can't include any spaces before or after the path.

If you cannot use the VSCode UI to configure vale you will need to add
these settings to your settings.json:
```json
    "vale.valeCLI.config": "/path/to/your/.vale.ini",
    "vale.valeCLI.minAlertLevel": "suggestion",
    "vale.valeCLI.path": "/usr/local/bin/vale",
```

### Using `markdown-check` and `single-line-check` as a pre-commit hook

If you add `markdown-check` and `single-line-check` as a pre-commit hook, git will perform both checks on all files that have changed since the last commit.

Inside your local docs directory add a `pre-commit` file inside the `.git/hooks` directory:

```sh
markdownlint --config VALEDIR/.markdownlint.yaml $(git diff --diff-filter=d --name-only HEAD | grep '\.md$'
single-line-check HEAD
```

This will run the markdownlinter on all changed files before you commit. It will also not allow you to commit unless the markdownlinter passes.

**To skip the pre-commit check if you need to quickly commit something use `--no-verify`**

## Credits

Some rules, especially regexes, are based on other projects' rules. Where I didn't leave rules in a folder with the name of the creator, I have pointed out in the individual files where the rules/regexes stem from.

Most commonly reused rules are from:
- [https://github.com/errata-ai/Google](https://github.com/errata-ai/Google)
- [https://github.com/errata-ai/Microsoft](https://github.com/errata-ai/Microsoft)
- [https://gitlab.com/gitlab-org/gitlab/-/tree/master/doc/.vale/gitlab](https://gitlab.com/gitlab-org/gitlab/-/tree/master/doc/.vale/gitlab)
