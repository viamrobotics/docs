{{ $title := .Get "title" }}
{{ $link := .Get "link" }}
{{ if and $title $link }}
**[{{ $title }}]({{ $link }})**
{{ else if $title }}
**{{ $title }}**
{{ end }}

{{ .Inner }}
