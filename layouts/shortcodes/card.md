{{- $link := (path.Clean (.Get "link")) -}}
{{- $customTitle := .Get "customTitle" -}}
{{- $customDescription := .Get "customDescription" -}}
{{- $customCanonicalLink := .Get "canonical" -}}
{{- if site.GetPage ($link | string) -}}
{{- with site.GetPage ($link | string) -}}
{{- $href := $customCanonicalLink | default .RelPermalink -}}
{{- $title := $customTitle | default .LinkTitle -}}
{{- $description := strings.TrimSpace ($customDescription | default .Description) -}}
- [{{ $title }}]({{ $href }}){{ with $description }}: {{ . }}{{ end }}
{{ end -}}
{{- else -}}
{{- errorf "Card has a bad link: %s" $link -}}
{{- end -}}
