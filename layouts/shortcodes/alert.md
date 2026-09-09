{{ $label := .Get "title" }}
{{ if not $label }}
  {{ $color := .Get "color" | default "primary" }}
  {{ if or (eq $color "danger") (eq $color "warning") }}
    {{ $label = "Warning" }}
  {{ else if or (eq $color "success") (eq $color "tip") }}
    {{ $label = "Tip" }}
  {{ else }}
    {{ $label = "Note" }}
  {{ end }}
{{ end }}
**{{ $label }}:**

{{ partial "render-inner-md.html" (dict "Inner" .Inner) }}
