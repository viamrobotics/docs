{{- $link := (path.Clean (.Get "link")) -}}
{{- $customTitle := .Get "customTitle" -}}
{{- $customDescription := .Get "customDescription" -}}
{{- $customCanonicalLink := .Get "canonical" -}}
{{- if site.GetPage ($link | string) -}}
  {{- with site.GetPage ($link | string) -}}
    {{- $href := $customCanonicalLink | default .RelPermalink -}}
    {{- $title := $customTitle | default .LinkTitle -}}
    {{- $description := $customDescription | default .Description -}}
**[{{ $title }}]({{ $href }})**

{{ $description }}
{{ end }}
{{- else -}}
  {{- errorf "Card has a bad link: %s" $link -}}
{{- end -}}
