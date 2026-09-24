{{- /*
  Triggers /llms-full.txt's generation (see CLAUDE.md's "Agent
  discoverability files" section) from here rather than from
  head.html/agent-discoverability-files.html, deliberately. Confirmed
  empirically: a Hugo Pipes resource's shortcode-template resolution
  inherits whichever output format's render pass is *actually executing*
  the resources.Get | ExecuteAsTemplate call, not anything about the
  resource's own naming or the page context passed to it. head.html only
  ever renders as part of an HTML page, so triggering llms-full.txt from
  there resolved shortcodes to their raw HTML variants; this template
  only ever renders as part of the MARKDOWN output format, so triggering
  it from here resolves them to the clean .md variants instead -- the
  same behavior every page's own Markdown mirror already gets.

  IMPORTANT: removing this trigger, or this template, silently stops
  /llms-full.txt from being generated, or reintroduces raw HTML/shortcode
  leakage into it -- neither produces a build error.
*/ -}}
{{- $llmsFullTXT := resources.Get "llms-full.txt" | resources.ExecuteAsTemplate "llms-full.txt" site.Home -}}
{{- $_ := $llmsFullTXT.RelPermalink -}}
{{- partial "render-page-markdown.html" . }}
