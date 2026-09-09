# {{ .Title }}
{{ with .Description }}
{{ . }}
{{ end -}}
> Source: {{ .Permalink }}{{ with .Params.updated }} · Last updated: {{ . }}{{ end }}

{{ .RenderShortcodes }}
