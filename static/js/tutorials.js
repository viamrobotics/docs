const { algoliasearch, instantsearch } = window;

const searchClient = algoliasearch('1CE6L976W0', '69b45c725273606d93690c9e89c56ad3');

const search = instantsearch({
  indexName: 'tutorials',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      item: `
<div class="col tutorial hover-card">
    <a href="{{permalink}}">
    {{#webm}}
        <div class="hover-card-video">
            <div>
            <video autoplay loop muted playsinline alt="{{ .alt }}" width="100%" style="max-width: {{ .maxWidth }}" class="{{- if .class -}}{{ .class}}{{- end }} lozad">
                <source data-src="../{{webm}}" src="../{{webm}}" type="video/webm">
                <source data-src="../{{mp4}}" src="../{{mp4}}" type="video/mp4">
                There should have been a video here but your browser does not seem to support it.
            </video>
            </div>
        </div>
    {{/webm}}
    {{#image}}
        <div class="hover-card-img">
        <picture>
            <img src="../{{image}}" alt="{{ .alt }}" loading="lazy">
        </picture>
        </div>
    {{/image}}
    <div class="small-hover-card-div">
        <div>
            <span>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</span>
            <div class="pills">
                {{#languages}}<div class="pill pill-lang">{{.}}</div>{{/languages}}
                {{#viamcomponents}}<div class="pill pill-component">{{.}}</div>{{/viamcomponents}}
                {{#viamservices}}<div class="pill pill-component">{{.}}</div>{{/viamservices}}
            </div>
        </div>
    </div>
    </a>
</div>
`,
    },
  }),
  instantsearch.widgets.configure({
    hitsPerPage: 12,
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Languages' },
  })(instantsearch.widgets.refinementList)({
    container: '#languages-list',
    attribute: 'languages',
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Components' },
  })(instantsearch.widgets.refinementList)({
    container: '#components-list',
    attribute: 'viamcomponents',
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Services' },
  })(instantsearch.widgets.refinementList)({
    container: '#services-list',
    attribute: 'viamservices',
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Approximate cost' },
  })(instantsearch.widgets.rangeInput)({
    container: '#cost-range',
    attribute: 'cost',
  }),
  instantsearch.widgets.pagination({
    container: '#pagination',
  }),
]);

search.start();
