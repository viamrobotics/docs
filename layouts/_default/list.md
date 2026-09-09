{{- $redirectTo := partial "resolve-chain.html" (dict "path" .RelPermalink "depth" 0) -}}
{{- $canonical := .Params.canonical -}}
{{- $body := "" -}}
{{- if ne $redirectTo .RelPermalink -}}
  {{- $body = partial "resolve-redirect-body.html" (dict "target" $redirectTo "context" .RelPermalink) -}}
{{- else if and $canonical (ne $canonical .RelPermalink) -}}
  {{- $body = partial "resolve-redirect-body.html" (dict "target" $canonical "context" .RelPermalink) -}}
{{- else -}}
  {{- $body = .RenderShortcodes -}}
{{- end }}
# {{ .Title }}
{{ with .Description }}
{{ . }}
{{ end -}}
> Source: {{ .Permalink }}{{ with .Params.updated }} · Last updated: {{ . }}{{ end }}

{{ $body }}
