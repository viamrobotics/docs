{{ $inner := .Inner }}
{{ if .Get "spaces" }}
  {{ $regex := delimit (slice `(?m)^\s{` (.Get "spaces") `}`) "" }}
  {{ $inner = replaceRE $regex `` .Inner }}
{{ end }}
{{ $inner = partial "render-inner-md.html" (dict "Inner" $inner) }}
{{ replaceRE "(?m)^" "> " (printf "**Caution:**\n\n%s" $inner) }}
