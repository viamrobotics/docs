const mlmodel = document.getElementsByClassName("mr-model")[0].id;
console.log(mlmodel)
const typesenseInstantsearchAdapter2 = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "Qhooem9HCRuFMVZPNQOhABAdEWJaSnlY", // Be sure to use an API key that only allows search operations
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
    query_by: "model_id,description",
    sort_by: "total_organization_usage:desc,total_robot_usage:desc",
    infix: "always"
  },
});
const searchClient2 = typesenseInstantsearchAdapter2.searchClient;

const search2 = instantsearch({
  indexName: "mlmodels",
  searchClient: searchClient2,
});

let filters2;
let itemtemplate2;

filters2 = {
  hitsPerPage: 5,
};
itemtemplate2 = `
<div class="name"><p><code>{{#helpers.highlight}}{ "attribute": "model_id" }{{/helpers.highlight}}</code></p></div>
<div class="description">{{#helpers.highlight}}{ "attribute": "description" }{{/helpers.highlight}}</div>
`;


search2.addWidgets([
  instantsearch.widgets.hits({
    container: "#hits2",
    templates: {
      item: itemtemplate2,
    },
  }),
  instantsearch.widgets.searchBox({
    container: '#searchbox2',
    placeholder: 'Search for a model...',
    poweredBy: false,
    wrapInput: true,
    showReset: false,
    showSubmit: false,
    showLoadingIndicator: false
  }),
  instantsearch.widgets.stats({
    container: '#searchstats2',
    templates: {
      text(data, { html }) {
        let results2 = '';

        if (data.hasManyResults) {
          results2 += `${data.nbHits} results:`;
        } else if (data.hasOneResult) {
          results2 += `1 result:`;
        } else {
          results2 += ``;
        }

        return `<span>${results2}</span>`;
      },
    },
  }),
  instantsearch.widgets.configure(filters2),
  instantsearch.widgets.pagination({
    container: "#pagination2",
    scrollTo: false
  }),
]);

search2.start();
