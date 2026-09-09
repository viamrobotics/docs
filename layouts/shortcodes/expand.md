{{ $label := "Click to expand" }}
{{ if .IsNamedParams }}
  {{ $label = .Get "default" | default $label }}
{{ else }}
  {{ $label = .Get 0 | default $label }}
{{ end }}
**{{ $label }}**

{{ .Inner }}
