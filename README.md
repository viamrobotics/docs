# Viam Documentation

An [mkdocs](https://www.mkdocs.org/) repo of Viam's tutorials and documentation. Site content is written in Markdown format located in `/docs`. [Pull requests welcome!](https://github.com/viamrobotics/tutorials-and-docs/blob/update-contribution-guide/CONTRIBUTING.md)

## Setup instructions

To install mkdocs:

```bash
pip install mkdocs
```

To spin up the docs website locally:

```bash
mkdocs serve
```

## Working on the documentation

Viam documentation must be authored in [Markdown](https://daringfireball.net/projects/markdown/), a lightweight markup language which results in easy-to-read, easy-to-write plain text documents that can be converted to valid HTML documents in a predictable manner.

MkDocs uses the [Python-Markdown](https://python-markdown.github.io/) library to render Markdown documents to HTML. [Python-Markdown](https://python-markdown.github.io/) is almost completely compliant with the reference implementation, although there are a few very minor [differences](https://python-markdown.github.io/#differences).

See the [Writing Guide](https://github.com/viamrobotics/tutorials-and-docs/blob/update-contribution-guide/WRITING_GUIDE.md) for our rules and recommendations on writing and maintaining documentation content.

Please see the [mkdocs Documentation](https://www.mkdocs.org/) for an introductory tutorial and a full user guide.

## Deploying

The site is automatically deployed when commits land in `main`.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/viamrobotics/tutorials-and-docs/blob/update-contribution-guide/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### TLDR

1. Fork it!
1. Create your feature branch: `git checkout -b my-new-feature`
1. Commit your changes: `git commit -am 'Add some feature'`
1. Push to the branch: `git push origin my-new-feature`
1. Submit a pull request :D
