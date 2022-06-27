# Viam Documentation

An (mkdocs)[https://www.mkdocs.org/] repo of our tutorials and documentation

# setup instructions
to install mkdocs:
pip install mkdocs

to spin up the docs website locally:
mkdocs serve

## Working on the content

- See VitePress docs on supported [Markdown Extensions](https://vitepress.vuejs.org/guide/markdown.html) and the ability to [use Vue syntax inside markdown](https://vitepress.vuejs.org/guide/using-vue.html).

- See the [Writing Guide](https://github.com/vuejs/docs/blob/main/.github/contributing/writing-guide.md) for our rules and recommendations on writing and maintaining documentation content.

## Contributing

This site is built with [VitePress](https://github.com/vuejs/vitepress) and depends on [@vue/theme](https://github.com/vuejs/vue-theme). Site content is written in Markdown format located in `src`. For simple edits, you can directly edit the file on GitHub and generate a Pull Request.

For local development, [pnpm](https://pnpm.io/) is preferred as package manager:

```bash
pnpm i
pnpm run dev
```

This project requires Node.js to be `v14.0.0` or higher, because we use new JavaScript features in our code, such as optional chaining.