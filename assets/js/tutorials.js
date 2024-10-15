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
    sort_by: "featured:asc,date:desc",
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
          refine(input.value.split(" ")[0]);
        }
      });

      return;
    }

    const list = widgetParams.items.map(({ label: staticLabel }) => {
      const elem = items.find(({ label }) => label === staticLabel);
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
              value="${staticLabel} (${count})"
              class="${isRefined ? "refined" : ""}"
              ${isRefined || count ? "" : "disabled"}
            />
          </label>
        </li>
      `;
    });

    if (widgetParams.container == "resource-list") {
      container.innerHTML = `
      <ul>
        ${list.join("")}
      </ul>
      <ul class="pill-explainer">
      <li><p><strong>tutorial</strong>: Projects that show you how to use different parts of Viam.</p></li>
      <li><p><strong>how-to</strong>: Step-by-step guides to complete tasks.</p></li>
      <li><p><strong>quickstart</strong>: <5 min step-by-step guide to complete tasks.</p></li>
      <li><p><strong>blogpost</strong>: Sample projects you can build.</p></li>
      <li><p><strong>codelab</strong>: Community projects and example project.</p></li>
      </ul>
      `;
    } else {
      container.innerHTML = `
      <ul>
        ${list.join("")}
      </ul>
      `;
    }
  },
);

search.addWidgets([
  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `
<div class="col tutorial hover-card {{resource}}">
    <a href="{{relpermalink}}" target="_blank">
    {{#webm}}
        <div class="hover-card-video">
            <div>
            <video autoplay loop muted playsinline alt="{{videoAlt}}" width="100%" style="width: {{ .maxWidth }}" class="{{- if .class -}}{{ .class}}{{- end }} lozad">
                <source data-src="{{webm}}" type="video/webm">
                <source data-src="{{mp4}}" type="video/mp4">
                There should have been a video here but your browser does not seem to support it.
            </video>
            </div>
        </div>
    {{/webm}}
    {{#image}}
        <div class="hover-card-img">
        <picture>
            <img src="{{image}}" alt="{{imageAlt}}" loading="lazy">
        </picture>
        </div>
    {{/image}}
    <div class="small-hover-card-div">
        <div>
            <div class="title">{{title}}</div>
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
    // filters: ["resource: docs-tutorial"],
  }),
  customRefinementList({
    container: "languages-list",
    attribute: "languages",
    operator: "or",
    sortBy: ["name:asc"],
    items: [{label: "flutter"}, { label: "go" }, { label: "python" }, { label: "typescript" }, { label: "c++" }],
  }),
  customRefinementList({
    container: "components-list",
    attribute: "viamcomponents",
    operator: "and",
    sortBy: ["name:asc"],
    items: [
      { label: "arm" },
      { label: "base" },
      { label: "board" },
      { label: "camera" },
      { label: "encoder" },
      { label: "gantry" },
      { label: "generic" },
      { label: "gripper" },
      { label: "input_controller" },
      { label: "motor" },
      { label: "movement_sensor" },
      { label: "power_sensor" },
      { label: "sensor" },
      { label: "servo" },
    ],
  }),
  customRefinementList({
    container: "services-list",
    attribute: "viamservices",
    operator: "and",
    sortBy: ["name:asc"],
    items: [
      { label: "data_manager" },
      { label: "motion" },
      { label: "frame_system" },
      { label: "mlmodel" },
      { label: "navigation" },
      { label: "base_remote_control" },
      { label: "sensors" },
      { label: "slam" },
      { label: "vision" },
    ],
  }),
  customRefinementList({
    container: "level-list",
    attribute: "level",
    operator: "or",
    sortBy: ["name:asc"],
    items: [
      { label: "Beginner" },
      { label: "Intermediate" },
      { label: "Advanced" },
    ],
  }),
  customRefinementList({
    container: "platformarea-list",
    attribute: "platformarea",
    operator: "or",
    sortBy: ["name:asc"],
    items: [
      { label: "data" },
      { label: "ml" },
      { label: "core" },
      { label: "fleet" },
      { label: "registry" },
      { label: "mobility" },
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
  }),
  instantsearch.widgets.pagination({
    container: "#pagination",
  }),
]);

search.start();
// Only show tutorials and blogposts to begin with
search.addWidgets([{
  init: function(options) {
    options.helper.toggleRefinement('resource', 'tutorial');
    options.helper.toggleRefinement('resource', 'blogpost');
  }
}]);
search.on("render", function () {
  if (
    search.helper.state.disjunctiveFacetsRefinements.languages &&
    search.helper.state.disjunctiveFacetsRefinements.languages.length
  ) {
    document.getElementById("filter-languages").textContent =
      "Languages (" +
      search.helper.state.disjunctiveFacetsRefinements.languages.length +
      ")";
  } else {
    document.getElementById("filter-languages").textContent = "Languages";
  }
  if (
    search.helper.state.facetsRefinements.viamcomponents &&
    search.helper.state.facetsRefinements.viamcomponents.length
  ) {
    document.getElementById("filter-components").textContent =
      "Components (" +
      search.helper.state.facetsRefinements.viamcomponents.length +
      ")";
  } else {
    document.getElementById("filter-components").textContent = "Components";
  }
  if (
    search.helper.state.facetsRefinements.viamservices &&
    search.helper.state.facetsRefinements.viamservices.length
  ) {
    document.getElementById("filter-services").textContent =
      "Services (" +
      search.helper.state.facetsRefinements.viamservices.length +
      ")";
  } else {
    document.getElementById("filter-services").textContent = "Services";
  }
  if (
    search.helper.state.disjunctiveFacetsRefinements.level &&
    search.helper.state.disjunctiveFacetsRefinements.level.length
  ) {
    document.getElementById("filter-level").textContent =
      "Level (" +
      search.helper.state.disjunctiveFacetsRefinements.level.length +
      ")";
  } else {
    document.getElementById("filter-level").textContent = "Level";
  }
  if (
    search.helper.state.facetsRefinements.platformarea &&
    search.helper.state.facetsRefinements.platformarea.length
  ) {
    document.getElementById("filter-platformarea").textContent =
      "Areas (" +
      search.helper.state.facetsRefinements.platformarea.length +
      ")";
  } else {
    document.getElementById("filter-platformarea").textContent = "Platform Areas";
  }
  if (
    search.helper.state.facetsRefinements &&
    search.helper.state.disjunctiveFacetsRefinements.languages &&
    search.helper.state.facetsRefinements.viamcomponents &&
    search.helper.state.disjunctiveFacetsRefinements.platformarea
  ) {
    document
      .querySelectorAll(".pill-lang")
      .forEach((e) =>
        search.helper.state.disjunctiveFacetsRefinements.languages.includes(
          e.textContent,
        )
          ? e.classList.add("pill-highlight")
          : e.classList.remove("pill-highlight"),
      );
    document
      .querySelectorAll(".pill-component")
      .forEach((e) =>
        search.helper.state.facetsRefinements.viamcomponents.includes(
          e.textContent,
        ) ||
        search.helper.state.facetsRefinements.viamservices.includes(
          e.textContent,
        )
          ? e.classList.add("pill-highlight")
          : e.classList.remove("pill-highlight"),
      );
  }

  observer.observe();
});

document.body.addEventListener(
  "click",
  function (event) {
    let filter_box = document.getElementById("tutorial-filter-items");
    let tutorial_menu = document.getElementById("tutorial-menu");
    if (
      !filter_box.contains(event.target) &&
      !tutorial_menu.contains(event.target)
    ) {
      document.querySelectorAll(".filter").forEach((el) => {
        el.setAttribute("aria-expanded", false);
        if (el && el.classList) {
          el.classList.add("collapsed");
        }
      });
      let open_elem = filter_box.getElementsByClassName("show");
      if (open_elem) {
        open_elem[0].classList.remove("show");
      }
    }
  },
  true,
);
