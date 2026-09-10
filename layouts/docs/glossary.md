{{- $glossaryItems := site.GetPage "page" "reference/glossary" -}}
{{- if not $glossaryItems -}}
  {{- errorf "glossary.md: No glossary items found at reference/glossary" -}}
{{- end -}}
# {{ .Title }}
{{ with .Description }}
{{ . }}
{{ end -}}
> Source: {{ .Permalink }}

{{ $terms := sort ($glossaryItems.Resources.ByType "page") "Title" "asc" }}
{{ range $terms }}
### {{ .Title }}

{{ .RenderShortcodes }}
{{ end }}
