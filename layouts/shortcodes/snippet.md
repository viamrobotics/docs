{{- $fparameter := "" -}}
{{- if .IsNamedParams -}}
  {{- $fparameter = .Get "file" -}}
{{- else -}}
  {{- $fparameter = .Get 0 -}}
{{- end -}}
{{- $filepath := printf "/static/include/snippet/%s" $fparameter -}}
{{- if fileExists $filepath -}}
  {{- partial "resolve-includes.html" (dict "content" (os.ReadFile $filepath) "dir" (printf "/%s" .Page.File.Dir) "depth" 0) -}}
{{- else -}}
  {{- errorf "snippet.md: The file %s was not found %s" $filepath .Page -}}
{{- end -}}
