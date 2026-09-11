{{- /*
  /tutorials/catalog.md: a flat, agent-facing catalog of tutorials,
  reusing the same filter and canonical-URL-fallback logic as
  list.typesense.json's tutorials branch (this repo's real search index)
  -- see CLAUDE.md's "Agent discoverability files" section for why this
  is its own minimal template rather than reusing that JSON output
  directly (it's a search-backend schema, not meant to double as a
  public agent contract).

  Scoped to /tutorials/ only via this section's own outputs: frontmatter
  override (docs/tutorials/_index.md), matching how sitetree.json/
  llms.txt/llms-full.txt are Pipes assets rather than output formats --
  NOT added to the global [outputs] section default, which would emit
  an empty catalog.md under every section site-wide (as Typesense's own
  output already does, mostly harmlessly).

  KNOWN RISK, loudly noted: this file's entire existence depends on
  docs/tutorials/_index.md existing and carrying this outputs: override.
  If /tutorials/ is ever removed from this site, this template stops
  being invoked -- silently, no build error -- and /tutorials/catalog.md
  disappears with it. llms.txt links to this file; if tutorials are ever
  removed, remove that link in the same change, or it will 404.
*/ -}}
{{- $section := $.Site.GetPage "section" .Section -}}
# Tutorials catalog

> Worked examples and walkthroughs. Several are hosted outside this site (codelabs.viam.com, viam.com/post/*) -- that's not a mistake, follow the link. Not part of the site structure in sitetree.json: many tutorials apply across several hardware/software combinations at once and don't fit a single-parent hierarchy.
{{ range .Site.AllPages }}
{{- if eq .Section $section.Section }}
{{- if or (and (.IsDescendant $section) (and (and (not .Draft) (not .Params.toc_hide)) (and (not .Params.private) (not .Params.empty_node)))) $section.IsHome }}
{{- if eq .Section "tutorials" }}
{{- $url := .Permalink }}
{{- with .Params.canonical }}{{ $url = . }}{{ end }}
- [{{ .Title }}]({{ $url }}){{ with .Description }}: {{ . }}{{ end }}
{{- $facets := slice }}
{{- with .Params.level }}{{ $facets = $facets | append (printf "level: %s" .) }}{{ end }}
{{- with .Params.languages }}{{ $facets = $facets | append (printf "languages: %s" (delimit . ", ")) }}{{ end }}
{{- with .Params.viamresources }}{{ $facets = $facets | append (printf "components/services: %s" (delimit . ", ")) }}{{ end }}
{{- if gt (len $facets) 0 }}
  `{{ delimit $facets " · " }}`
{{- end }}
{{- end }}
{{- end }}
{{- end }}
{{- end }}
