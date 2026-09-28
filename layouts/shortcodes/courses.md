{{- $learn := site.Data.courses.learn_url -}}
{{ range site.Data.courses.courses -}}
{{- $meta := slice -}}
{{- with .duration }}{{ $meta = $meta | append . }}{{ end -}}
{{- with .hardware }}{{ $meta = $meta | append . }}{{ end -}}
{{- if eq .status "coming-soon" }}
- **{{ .title }}** (coming soon): {{ .description }}
{{- else }}
- [{{ .title }}]({{ $learn }}): {{ .description }}{{ with $meta }} ({{ delimit . ", " | lower }}){{ end }}
{{- end }}
{{ end }}
[Start learning at {{ strings.TrimPrefix "https://" $learn }}]({{ $learn }})
