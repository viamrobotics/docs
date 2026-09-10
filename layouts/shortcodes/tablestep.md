{{- $start := .Get "start" -}}
{{- $stepNumber := .Get "number" -}}
{{- if not $stepNumber -}}
  {{- if $start -}}
    {{- $.Page.Scratch.Set "tablestepMDCounter" (sub $start 1) -}}
  {{- end -}}
  {{- $currentCounter := $.Page.Scratch.Get "tablestepMDCounter" -}}
  {{- if not $currentCounter -}}
    {{- $currentCounter = 0 -}}
  {{- end -}}
  {{- $stepNumber = add $currentCounter 1 -}}
  {{- $.Page.Scratch.Set "tablestepMDCounter" $stepNumber -}}
{{- end -}}
{{- $content := partial "render-inner-md.html" (dict "Inner" .Inner) -}}
### Step {{ $stepNumber }}

{{ $content }}
