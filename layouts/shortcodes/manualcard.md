{{- $title := .Get "title" -}}
{{- $link := .Get "link" -}}
{{- if and $title $link }}
**[{{ $title }}]({{ $link }})**
{{- else if $title }}
**{{ $title }}**
{{- end }}

{{ partial "render-inner-md.html" (dict "Inner" .Inner) }}
