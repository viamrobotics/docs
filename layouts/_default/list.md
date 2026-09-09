{{ $redirectTo := partial "resolve-chain.html" (dict "path" .RelPermalink "depth" 0) }}
{{ $body := "" }}
{{ if ne $redirectTo .RelPermalink }}
  {{ if not (hasPrefix $redirectTo "/") }}
    {{ $body = printf "This page redirects to [%s](%s). See that page for the full content.\n" $redirectTo $redirectTo }}
  {{ else }}
    {{ $target := site.GetPage $redirectTo }}
    {{ if not $target }}
      {{ errorf "list.md: %s force-redirects to %s, which is not a published page" .RelPermalink $redirectTo }}
    {{ end }}
    {{ $body = printf "This page redirects to [%s](%s). See that page for the full content.\n" $target.LinkTitle $target.RelPermalink }}
  {{ end }}
{{ else }}
  {{ $body = .RenderShortcodes }}
{{ end }}
# {{ .Title }}
{{ with .Description }}
{{ . }}
{{ end -}}
> Source: {{ .Permalink }}{{ with .Params.updated }} · Last updated: {{ . }}{{ end }}

{{ $body }}
