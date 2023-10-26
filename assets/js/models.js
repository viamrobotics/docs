const { TypesenseInstantSearchAdapter, instantsearch } = window;

const api = document.getElementsByClassName("mr-component")[0].id;
console.log(api)
const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "EzBPJyIM1x2jv1C8oplyUjeONokTcJcZ", // Be sure to use an API key that only allows search operations
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
    query_by: "api,model,description",
    sort_by: "total_organization_usage:desc,total_robot_usage:desc",
    infix: "always"
  },
});
const searchClient = typesenseInstantsearchAdapter.searchClient;

const search = instantsearch({
  indexName: "modular_resources",
  searchClient,
});

let filters;
let itemtemplate;

if (api == "") {
  filters = {
    hitsPerPage: 5,
  };
  itemtemplate = `
  <div class="type"><p><code>{{#helpers.highlight}}{ "attribute": "api" }{{/helpers.highlight}}</code></p></div>
  <div class="name"><p><a href="{{url}}"><code>{{#helpers.highlight}}{ "attribute": "model" }{{/helpers.highlight}}</code></a></p></div>
  <div class="description">{{#helpers.highlight}}{ "attribute": "description" }{{/helpers.highlight}}</div>
  `;
} else {
  filters = {
    facetFilters: ["api: " + api],
    hitsPerPage: 5,
  };
  itemtemplate = `
  <div class="name"><p><a href="{{url}}"><code>{{#helpers.highlight}}{ "attribute": "model" }{{/helpers.highlight}}</code></a></p></div>
  <div class="description">{{#helpers.highlight}}{ "attribute": "description" }{{/helpers.highlight}}</div>
  `;
}


search.addWidgets([
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: itemtemplate,
    },
  }),
  instantsearch.widgets.searchBox({
    container: '#searchbox',
    placeholder: 'Search for a model...',
    poweredBy: false,
    wrapInput: true,
    showReset: false,
    showSubmit: false,
    showLoadingIndicator: false
  }),
  instantsearch.widgets.stats({
    container: '#searchstats',
    templates: {
      text(data, { html }) {
        let results = '';

        if (data.hasManyResults) {
          results += `${data.nbHits} results:`;
        } else if (data.hasOneResult) {
          results += `1 result:`;
        } else {
          results += ``;
        }

        return html`<span>${results}</span>`;
      },
    },
  }),
  instantsearch.widgets.configure(filters),
  instantsearch.widgets.pagination({
    container: "#pagination",
    scrollTo: false
  }),
]);

search.start();
