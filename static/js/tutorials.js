const { TypesenseInstantSearchAdapter, instantsearch } = window;
const observer = lozad();

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "oRW875O3vjeV3qX4ENl1iIA0u2IRDbTQ", // Be sure to use an API key that only allows search operations
    nodes: [
      {
        host: "cgnvrk0xwyj9576lp-1.a1.typesense.net",
        port: "443",
        protocol: "https",
      },
    ],
    cacheSearchResultsForSeconds: 2 * 60, // Cache search results from server. Defaults to 2 minutes. Set to 0 to disable caching.
  },
  // The following parameters are directly passed to Typesense's search API endpoint.
  //  So you can pass any parameters supported by the search endpoint below.
  //  query_by is required.
  additionalSearchParameters: {
    query_by: "title,description",
    sort_by: "featured:asc,date:desc"
  },
});
const searchClient = typesenseInstantsearchAdapter.searchClient;

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
            <video autoplay loop muted playsinline alt="{{videoAlt}}" width="100%" style="max-width: {{ .maxWidth }}" class="{{- if .class -}}{{ .class}}{{- end }} lozad">
                <source data-src="..{{webm}}" type="video/webm">
                <source data-src="..{{mp4}}" type="video/mp4">
                There should have been a video here but your browser does not seem to support it.
            </video>
            </div>
        </div>
    {{/webm}}
    {{#image}}
        <div class="hover-card-img">
        <picture>
            <img src="../{{image}}" alt="{{imageAlt}}" loading="lazy">
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
    sortBy: ['name:asc']
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Components' },
  })(instantsearch.widgets.refinementList)({
    container: '#components-list',
    attribute: 'viamcomponents',
    operator: 'and',
    sortBy: ['name:asc']
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Services' },
  })(instantsearch.widgets.refinementList)({
    container: '#services-list',
    attribute: 'viamservices',
    operator: 'and',
    sortBy: ['name:asc']
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Approximate cost' },
  })(instantsearch.widgets.rangeInput)({
    container: '#cost-range',
    attribute: 'cost',
  }),
  instantsearch.widgets.panel({
    templates: { header: 'Level' },
  })(instantsearch.widgets.refinementList)({
    container: '#level-list',
    attribute: 'level',
    operator: 'and'
  }),
  instantsearch.widgets.pagination({
    container: '#pagination',
  }),
]);

search.start();
search.on('render', function() {
  observer.observe()
});
