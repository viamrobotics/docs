{{- $id := .Get 0 | default (.Get "id") -}}
{{- $course := index (where site.Data.courses.courses "id" $id) 0 -}}
{{- if not $course -}}
  {{- errorf "course shortcode: no course with id %q in data/courses.yaml (%s)" $id .Position -}}
{{- end -}}
{{- $eyebrow := .Get "eyebrow" | default "Free course" -}}
{{- $meta := slice -}}
{{- with $course.duration }}{{ $meta = $meta | append . }}{{ end -}}
{{- with $course.hardware }}{{ $meta = $meta | append . }}{{ end -}}
> **{{ $eyebrow }}{{ if eq $course.status "coming-soon" }} (coming soon){{ end }}:** [{{ $course.title }}]({{ $course.url }}): {{ $course.description }}{{ with $meta }} ({{ delimit . ", " | lower }}){{ end }}
