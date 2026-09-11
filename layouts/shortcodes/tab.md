{{ if .Parent }}
  {{ $name := trim (.Get "name") " " }}
  {{ if not (.Parent.Scratch.Get "tabs") }}
    {{ .Parent.Scratch.Set "tabs" slice }}
  {{ end }}
  {{ $content := partial "render-inner-md.html" (dict "Inner" .Inner) }}
  {{ $.Parent.Scratch.Add "tabs" (dict "name" $name "content" $content) }}
{{ else }}
  {{ errorf "[%s] %q: tab shortcode missing its parent" site.Language.Lang .Page.Path }}
{{ end }}
