{{- $title := "" -}}
{{- $tasks := "" -}}
{{- $level := "" -}}
{{- if .IsNamedParams -}}
  {{- $title = .Get "title" -}}
  {{- $tasks = .Get "tasks" -}}
  {{- $level = .Get "level" -}}
{{- else -}}
  {{- $title = .Get 0 -}}
  {{- $tasks = .Get 1 -}}
  {{- $level = .Get 2 -}}
{{- end -}}
### {{ $title }}
{{ with $tasks }}_{{ . }} tasks{{ with $level }} | {{ . }}{{ end }}_{{ end }}

{{ partial "render-inner-md.html" (dict "Inner" .Inner) }}
