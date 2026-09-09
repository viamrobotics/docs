{{ $fparameter := "" }}
{{ if .IsNamedParams }}
  {{ $fparameter = .Get "file" }}
{{ else }}
  {{ $fparameter = .Get 0 }}
{{ end }}
{{ $filepath := "" }}
{{ if eq (substr $fparameter 0 1) "/" }}
  {{ $filepath = $fparameter }}
{{ else }}
  {{ $filepath = printf "/%s%s" .Page.File.Dir $fparameter }}
{{ end }}
{{ if fileExists $filepath }}
  {{ if eq (.Get "code") "true" }}
    {{ printf "```%s\n%s\n```" (.Get "lang") (os.ReadFile $filepath) }}
  {{ else }}
    {{ os.ReadFile $filepath }}
  {{ end }}
{{ else }}
  {{ errorf "readfile.md: The file %s was not found %s" $filepath .Page }}
{{ end }}
