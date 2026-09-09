{{ $fparameter := "" }}
{{ if .IsNamedParams }}
  {{ $fparameter = .Get "file" }}
{{ else }}
  {{ $fparameter = .Get 0 }}
{{ end }}
{{ $filepath := printf "/static/include/snippet/%s" $fparameter }}
{{ if fileExists $filepath }}
  {{ os.ReadFile $filepath }}
{{ else }}
  {{ errorf "snippet.md: The file %s was not found %s" $filepath .Page }}
{{ end }}
