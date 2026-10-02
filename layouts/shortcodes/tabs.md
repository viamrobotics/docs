{{ if .Inner }}{{ end }}
{{ $tabs := .Scratch.Get "tabs" }}
{{ range $tabs }}
### {{ .name }}

{{ .content }}
{{ end }}
