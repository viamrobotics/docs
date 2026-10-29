{{- /* Markdown mirror of the homepage shortcode (homepage.html), from the same
     data/homepage.yaml. Links are absolute so they work from /index.md. */ -}}
{{- $d := site.Data.homepage -}}
{{- with $d.hero -}}
{{ .description }}
{{- end }}
{{- with $d.announcement }}
{{- if .enabled }}
{{- $l := partial "homepage-link.html" . }}

> **{{ .label | default "New" }}:** [{{ .text }}]({{ $l.permalink }})
{{- end }}
{{- end }}
{{- with $d.ways_to_learn }}

## {{ .title }}
{{ with .docs }}
- **{{ .title }}:** {{ .description }}
{{- range .links }}
{{- $l := partial "homepage-link.html" . }}
  - [{{ $l.title }}]({{ $l.permalink }}): {{ $l.description }}
{{- end }}
{{- end }}
{{- range .items }}
{{- $l := partial "homepage-link.html" . }}
- [{{ .title }}]({{ $l.permalink }}): {{ .description }}
{{- end }}
{{- end }}
{{- with $d.workshops }}

## {{ .title }}
{{ range .items }}
{{- $l := partial "homepage-link.html" . }}
- [{{ $l.title }}]({{ $l.permalink }}): {{ $l.description }}
{{- end }}
{{ $all := partial "homepage-link.html" .all -}}
- [{{ $all.title }}]({{ $all.permalink }})
{{- end }}
{{- with $d.featured }}

## {{ .title }}
{{ range .items }}
{{- $l := partial "homepage-link.html" . }}
- [{{ $l.title }}]({{ $l.permalink }}): {{ $l.description }}
{{- end }}
{{- end }}
{{- with $d.reference }}

## {{ .title }}
{{ range .items }}
{{- $l := partial "homepage-link.html" . }}
- [{{ $l.title }}]({{ $l.permalink }}): {{ $l.description }}
{{- end }}
{{ $all := partial "homepage-link.html" .all -}}
- [{{ $all.title }}]({{ $all.permalink }})
{{- end }}
{{- with $d.courses }}
{{- $learn := site.Data.courses.learn_url }}

## {{ .title }}
{{ range .highlight }}
{{- $id := . }}
{{- $c := index (where site.Data.courses.courses "id" $id) 0 }}
- [{{ $c.title }}]({{ $c.url | default $learn }}): {{ $c.description }}
{{- end }}
- [{{ .all_title }}]({{ $learn }})
{{- end }}
{{- with $d.community }}

## Community

{{ range . -}}
- [{{ .name }}]({{ .url }})
{{ end -}}
{{- end }}
