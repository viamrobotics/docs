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
  {{ printf "```%s\n%s\n```" (.Get "lang") (os.ReadFile $filepath) }}
{{ else }}
  {{ errorf "read-code-snippet.md: The file %s was not found %s" $filepath .Page }}
{{ end }}
