{{- $title := .Get "title" -}}
{{- $date := .Get "date" -}}
### {{ $title }}{{ with $date }} ({{ . | time.Format "Jan 2006" }}){{ end }}

{{ partial "render-inner-md.html" (dict "Inner" .Inner) }}
