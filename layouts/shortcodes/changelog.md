{{ $title := .Get "title" }}
{{ $date := .Get "date" }}
### {{ $title }}{{ with $date }} ({{ . | time.Format "Jan 2006" }}){{ end }}

{{ .Inner }}
