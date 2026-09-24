{{- $img := resources.GetMatch (.Get "src") -}}
{{- if $img -}}
![{{ .Get "alt" }}]({{ $img.RelPermalink }})
{{- else -}}
{{- errorf "Image not found - is it in the assets folder? %s" (.Get "src") -}}
{{- end -}}
