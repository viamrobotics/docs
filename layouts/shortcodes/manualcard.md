{{- $title := .Get "title" -}}
{{- $link := .Get "link" -}}
{{- $body := strings.TrimSpace (partial "render-inner-md.html" (dict "Inner" .Inner)) -}}
{{- if and $title $link -}}
- [{{ $title }}]({{ $link }}){{ with $body }}: {{ . }}{{ end }}
{{- else if $title -}}
- {{ $title }}{{ with $body }}: {{ . }}{{ end }}
{{- else -}}
{{ $body }}
{{- end }}
