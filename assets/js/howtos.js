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
    query_by: "resource,title,description",
    sort_by: "featured:desc,date:desc",
  },
});

const searchClient = typesenseInstantsearchAdapter.searchClient;

const search = instantsearch({
  indexName: "tutorials",
  searchClient,
});


const customRefinementList = instantsearch.connectors.connectRefinementList(
  ({ items, refine, widgetParams }, isFirstRender) => {

    const container = document.getElementById(widgetParams.container);

    if (isFirstRender) {
      container.addEventListener("click", ({ target }) => {
        const input = target.closest("input");

        if (input) {
          let refinements = search.helper.state.disjunctiveFacetsRefinements["platformarea"];
          if (refinements.length) {
            if (refinements[0] == input.name) {
              refine(refinements[0]);
            } else {
              refine(refinements[0]);
              refine(input.name)
            }
          } else {
            refine(input.name)
          }
        }
      });

      return;
    }

    const list = widgetParams.items.map(({ label: staticLabel, value: staticValue }) => {
      const elem = items.find(({ label }) => label === staticValue);

      let count = 0;
      let isRefined = false;
      if (elem) {
        count = elem.count;
        isRefined = elem.isRefined;
      }

      return `
        <li>
          <label>
            <input
              type="button"
              value="${staticLabel}"
              name="${staticValue}"
              class="filterbutton ${isRefined ? "refined" : ""}"
              ${isRefined || count ? "" : "disabled"}
            />
          </label>
        </li>
      `;
    });

    container.innerHTML = `
    <ul>
      ${list.join("")}
    </ul>
    `;
  },
);

let refinementLists = [customRefinementList({
  container: "platformarea-list",
  attribute: "platformarea",
  operator: "or",
  sortBy: ["name:asc"],
  items: [
    { label: "Data Management", value: "data" },
    { label: "Machine Learning", value: "ml" },
    { label: "Core", value: "core" },
    { label: "Fleet Management", value: "fleet" },
    { label: "Registry", value: "registry" },
    { label: "Mobility", value: "mobility" },
  ],
}),
customRefinementList({
  container: "resource-list",
  attribute: "resource",
  operator: "or",
  sortBy: ["name:asc"],
  items: [
    { label: "tutorial" },
    { label: "how-to" },
    { label: "quickstart" },
    { label: "blogpost" },
    { label: "codelab" },
  ],
})]

let searchWidgets = [
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `
<div class="col hover-card">
    <a href="{{relpermalink}}" target="_blank">
    <div class="small-hover-card-div">
            <div class="title">{{title}}</div>
            <div class="description">
                {{#description}}<p>{{description}}</p>{{/description}}
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
];

search.addWidgets(refinementLists);

search.start();
// Only show guide & howtos
search.addWidgets([{
  init: function(options) {
    options.helper.toggleRefinement('resource', 'how-to');
    options.helper.toggleRefinement('resource', 'quickstart');
  }
}]);

let widgetsAdded = true;

search.on("render", function () {
  if (search.helper.state.disjunctiveFacetsRefinements.platformarea.length) {
    if (!widgetsAdded) {
      widgetsAdded = true;
      // Only show expanders to begin with
      search.addWidgets(searchWidgets);
      document.getElementById("how-to-paths").classList.add("isHidden");
    }
  } else {
    if (widgetsAdded) {
      widgetsAdded = false;
      search.removeWidgets(searchWidgets);
      document.getElementById("how-to-paths").classList.remove("isHidden");
    }
  }

  if (
    search.helper.state.facetsRefinements &&
    search.helper.state.disjunctiveFacetsRefinements.platformarea
  ) {
    document
      .querySelectorAll(".pill-component")
      .forEach((e) =>
        search.helper.state.disjunctiveFacetsRefinements.platformarea.includes(
          e.textContent,
        )
          ? e.classList.add("pill-highlight")
          : e.classList.remove("pill-highlight"),
      );
  }

  observer.observe();
});
