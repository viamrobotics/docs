{{- $title := .Get "title" -}}
{{- $link := .Get "link" -}}
{{- $body := strings.TrimSpace (partial "render-inner-md.html" (dict "Inner" .Inner)) -}}
{{- $titleLine := $title -}}
{{- if and $title $link -}}
{{- $titleLine = printf "[%s](%s)" $title $link -}}
{{- end -}}
{{- if $title -}}
{{- if findRE `\n[ \t]*\n` $body 1 -}}
- {{ $titleLine }}

{{ replaceRE "(?m)^(\\S)" "    $1" $body }}
{{ else -}}
- {{ $titleLine }}{{ with $body }}: {{ . }}{{ end }}
{{ end -}}
{{- else -}}
{{ $body }}
{{- end }}
