## Contributing to Viam Docs

Thank you for wanting to help us make the docs better.
Every contribution is appreciated.

### Code of Conduct
For our Code of Conduct, please see our website at: [viam.com/community-guidelines](https://www.viam.com/community-guidelines).

## Goals

The Viam documentation aims to:

- Educate users
- Help users accomplish tasks

We aim to be direct, friendly, and concise.

Depending on the type of content, the audience may be beginners or advanced users.
Use your judgment to determine the concepts that need to be explained and when in doubt link to supporting content.

## Project structure

All documentation is in the [docs folder](docs).
For information about Hugo and how to develop locally, see the [README](./README.md).

## Style Guide

### Vale Linting

> **Tip**
> We recommend you work in Visual Studio Code and install the [Vale extension](https://marketplace.visualstudio.com/items?itemName=errata-ai.vale-server) to make use of the vale linter.

When you open a PR, your changes will be checked against a few style rules.
To run this check locally, follow the instructions in the [Vale Readme](.github/vale/README.md).

### `markdownlint`

> **Tip**
> We recommend you work in Visual Studio Code and install the [markdownlint extension](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint).

### One sentence per line

To make reviews easier, each new sentence should begin on a new line.

## Pull requests

If you are making a small change, like fixing a typo or editing a few lines of text, you do not need to create an issue.
However, if you plan to make bigger changes, we ask that you create an issue and discuss the change with us in advance.

To get started:

1. Fork the official repo into your personal GitHub.
2. Clone the forked repo to your local system.
3. Add the remote path for the 'official' repository: `git remote add upstream git@github.com:viamrobotics/docs.git`

When you are ready to contribute changes to the docs:

1. Make sure you are on the main branch: ```git switch main```
2. Sync your forked main branch with the official repo: ```git pull upstream main```
3. Create a new branch for your changes: ```git switch -c my-new-feature```
4. Edit some docs...
5. Commit your changes: ```git commit -am 'Add some feature'```
6. Make sure your local branch is still up-to-date with the official repo: ```git pull upstream main```
7. Push to the branch: ````git push origin my-new-feature````
8. Submit a pull request

## Questions

If you have questions or would like to chat, please find us on the [Community Discord](https://discord.gg/viam).
