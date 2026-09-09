{{ $type := .Get 0 }}
{{ $label := "Note" }}
{{ if eq $type "warning" }}{{ $label = "Warning" }}{{ end }}
{{ if eq $type "info" }}{{ $label = "Info" }}{{ end }}
{{ if eq $type "tip" }}{{ $label = "Tip" }}{{ end }}
> **{{ $label }}:** {{ .Inner }}
