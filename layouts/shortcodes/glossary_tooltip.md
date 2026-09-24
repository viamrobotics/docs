{{- $id := .Get "term_id" -}}
{{- partial "glossary-terms.html" $.Page -}}
{{- $term_info := ($.Page.Scratch.Get "glossary_items").GetMatch (printf "%s.md" $id) -}}
{{- if not $term_info -}}
  {{- errorf "%q: %q is not a valid glossary term_id, see ./docs/reference/glossary/* for a full list" .Page.Path $id -}}
{{- end -}}
{{- $text := .Get "text" | default $term_info.Title -}}
{{- $link := $term_info.Params.full_link | default (printf "/reference/glossary/#term-%s" $id) -}}
[{{ $text }}]({{ $link }})
