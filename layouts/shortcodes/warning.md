{{ $inner := .Inner }}
{{ if .Get "spaces" }}
  {{ $regex := delimit (slice `(?m)^\s{` (.Get "spaces") `}`) "" }}
  {{ $inner = replaceRE $regex `` .Inner }}
{{ end }}
**Warning:**

{{ partial "render-inner-md.html" (dict "Inner" $inner) }}
