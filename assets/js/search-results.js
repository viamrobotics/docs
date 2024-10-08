const { TypesenseInstantSearchAdapter, instantsearch } = window;
const observer = lozad();

const indexName = 'docsearch';
const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "GHQK6od8KfpvTEh4YpA113gUc2dU5fGR",
    nodes: [
      {
        host: "cgnvrk0xwyj9576lp-1.a1.typesense.net",
        port: "443",
        protocol: "https",
      },
    ],
    cacheSearchResultsForSeconds: 2 * 60,
  },
  additionalSearchParameters: {
    query_by: 'hierarchy.lvl0,hierarchy.lvl1,url_without_anchor',
    query_by_weight: '100,50,1',
    sort_by: "_text_match:desc,item_priority:desc",
    prioritize_token_position: true,
    group_by: "url_without_anchor",
    group_limit: 1,
  },
});

const searchClient = typesenseInstantsearchAdapter.searchClient;

const search = instantsearch({
  indexName: indexName,
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `
<div class="col hover-card">
    <a href="{{url}}" target="_blank">
    <div class="small-hover-card-div">
            <div class="title">{{hierarchy.lvl0}}</div>
            <div class="description">
                <p>{{#helpers.highlight}}{ "attribute": "hierarchy.lvl1", "highlightedTagName": "mark" }{{/helpers.highlight}}</p>
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
  instantsearch.widgets.pagination({
    container: "#pagination",
  }),
  instantsearch.widgets.searchBox({
    container: '#search-box',
  }),
]);

search.start();

const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get('query');

search.setUiState({
  [indexName]: {
    query: query
  }
});
