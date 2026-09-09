{{ $inner := .Inner }}
{{ if .Get "spaces" }}
  {{ $regex := delimit (slice `(?m)^\s{` (.Get "spaces") `}`) "" }}
  {{ $inner = replaceRE $regex `` .Inner }}
{{ end }}
> **Caution:** {{ $inner }}
