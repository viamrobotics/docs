{{- /*
  /llms-full.txt: full text of pages flagged `full: true` in
  data/llms_pages.yaml, rendered via the same render-page-markdown.html
  partial every page's own .md mirror uses. See CLAUDE.md.

  $full is interpolated with | safeHTML below: Hugo's html/template
  escaper is active for bare interpolation in a top-level list.<format>
  template regardless of isPlainText/isHTML on the output format (verified
  empirically while building list.llmstxt.txt in the prior task), so
  without it apostrophes in real page content would render as &#39; etc.

  Filename note: this template's middle segment ("llmsfulltxt") must match
  the LLMSFULLTXT output format's Name field exactly, case-insensitive --
  baseName controls the public URL (llms-full.txt) separately. An earlier
  version named this file list.llms-full.txt, which silently collided with
  list.llms.txt (both rendered the same content) since neither's middle
  segment matched its format's actual Name.
*/ -}}
{{- $out := slice -}}
{{- range site.Data.llms_pages.sections -}}
  {{- range .pages -}}
    {{- if .full -}}
      {{- with site.GetPage .path -}}
        {{- $out = $out | append (partial "render-page-markdown.html" .) -}}
      {{- else -}}
        {{- warnf "data/llms_pages.yaml: no page found at %q" .path -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- $full := delimit $out "\n\n---\n\n" -}}
{{- if gt (len $full) 200000 -}}
  {{- warnf "llms-full.txt is %d bytes, over the 200KB sanity threshold -- review data/llms_pages.yaml's `full: true` entries" (len $full) -}}
{{- end -}}
# Viam — agent-facing pages, full text

> The full text of the pages flagged for full inclusion in [llms.txt]({{ "llms.txt" | absURL }}), inlined here so an agent can read them in one fetch instead of following each link separately.

{{ $full | safeHTML }}
