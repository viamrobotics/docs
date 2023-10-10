const { TypesenseInstantSearchAdapter, instantsearch } = window;

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "doFRbKhVNu5cRp776sdnAhsv30A3l7n6", // Be sure to use an API key that only allows search operations
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
  },
});
const searchClient = typesenseInstantsearchAdapter.searchClient;

const search = instantsearch({
  indexName: "modular_models",
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `
<div class="name"><a href="{{url}}"><code>{{model}}</code></a></div>
<div class="description">{{description}}</div>
`,
    },
  }),
  instantsearch.widgets.configure({
    facetFilters: ["api: rdk:component:sensor"],
    hitsPerPage: 5,
  }),
  instantsearch.widgets.pagination({
    container: "#pagination",
  }),
]);

search.start();

console.log("here")
