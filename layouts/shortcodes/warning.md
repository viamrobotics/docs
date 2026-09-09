{{ $inner := .Inner }}
{{ if .Get "spaces" }}
  {{ $regex := delimit (slice `(?m)^\s{` (.Get "spaces") `}`) "" }}
  {{ $inner = replaceRE $regex `` .Inner }}
{{ end }}
> **Warning:** {{ $inner }}
