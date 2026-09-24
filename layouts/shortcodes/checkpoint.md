{{- $title := .Get "title" | default "Checkpoint" -}}
{{- replaceRE "(?m)^" "> " (printf "**%s:**\n\n%s" $title (strings.TrimSpace .Inner)) -}}
