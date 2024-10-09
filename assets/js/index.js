// script for menu toggles
var siteMenuSubmenus = document.getElementsByClassName(
    "nav-fold"
);

function submenuToggle(menu, toggle) {
    let open = false;
    if (toggle.children[0].className === "fas fa-chevron-right") {
        open = true;
    }

    // toggle displayed icon
    if (open) {
        toggle.children[0].className = "fas fa-chevron-down";
    } else {
        toggle.children[0].className = "fas fa-chevron-right";
    }

    // add or remove collapse class to children
    let immediateChildren = menu.querySelector("ul").children;
    if (open) {
        for (let c of immediateChildren) {
            c.classList.remove("collapse");
        }
    } else {
        for (let c of immediateChildren) {
            c.classList.add("collapse");
        }
    }
}

for (let menu of siteMenuSubmenus) {
    // add event listener on menu toggle
    let toggle = menu.querySelector("span").querySelector(".menu-toggle");
    if (toggle) {
        if (menu.classList.contains('empty-node-submenu')) {
            menu.querySelector(".emptynode").addEventListener('click', function () {
                submenuToggle(menu, toggle);
            });
        }
        toggle.addEventListener('click', function () {
            submenuToggle(menu, toggle);
        });
    }
};

// script for the scroll button
const main = document.body;
const scrollBtn = document.getElementById("scrollButton");
function toTop() {
    window.scroll({top: 0, left: 0, behavior: 'smooth'});
}

function btnVisibility(payload) {
    if (payload[0].boundingClientRect.y <= -400) {
        scrollBtn.style.visibility = "visible";
        scrollBtn.style.opacity = "1";
    } else {
        scrollBtn.style.opacity = "0";
        scrollBtn.style.visibility = "hidden";
    }
}

if(main && scrollBtn) {
    const observer = new IntersectionObserver(btnVisibility, {
        threshold: [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    });
    observer.observe(main);
}

function handleSearch(inputSelector) {
    const searchConfig = {
        inputSelector: inputSelector,
        typesenseCollectionName: 'docsearch',
        typesenseServerConfig: {
            nodes: [{
                host: 'cgnvrk0xwyj9576lp-1.a1.typesense.net',
                port: '443',
                protocol: 'https'
            }],
            apiKey: 'GHQK6od8KfpvTEh4YpA113gUc2dU5fGR'
        },
        typesenseSearchParams: {
            query_by: 'hierarchy.lvl0,hierarchy.lvl1,url_without_anchor',
            query_by_weight: '100,50,1',
            sort_by: "_text_match:desc,item_priority:desc",
            prioritize_token_position: true,
            group_by: "url_without_anchor",
            group_limit: 1
        },
        autocompleteOptions: {
            autoselect: false,
            debug: false,
            hint: false
        }
    };

    const search = docsearch(searchConfig);

    let opened = false;
    search.autocomplete.on('autocomplete:shown', (e, a, b, c) => {
        opened = true;
    });
    search.autocomplete.on('autocomplete:closed', () => {
        opened = false;
    });
    let cursorUsed = false;
    // we can't detect the cursor changing to an empty auto complete entry,
    // so the only case where getting to search results via Enter will work is
    // text typed followed by Enter.
    search.autocomplete.on('autocomplete:cursorchanged', (event, suggestion) => {
        cursorUsed = true;
    });
    // search.autocomplete.on('keydown', (e) => {
    //     if (opened && !cursorUsed && e.key === 'Enter' && search.input[0].value !== '') {
    //         const query = encodeURIComponent(search.input[0].value);
    //         window.location = `${window.location.origin}/search?query=${query}`;
    //     }
    // });
}

handleSearch('.navbar-nav .td-search-input');
handleSearch('.td-sidebar__search .td-search-input');

// Userflow START
!function(){var e="undefined"==typeof window?{}:window,r=e.userflow;if(!r){var t="https://js.userflow.com/",n=null;r=e.userflow={_stubbed:!0,load:function(){return n||(n=new Promise((function(r,o){var s=document.createElement("script");s.async=!0;var a=e.USERFLOWJS_ENV_VARS||{};"es2020"===(a.USERFLOWJS_BROWSER_TARGET||function(e){for(var r=[[/Edg\//,/Edg\/(\d+)/,80],[/OPR\//,/OPR\/(\d+)/,67],[/Chrome\//,/Chrome\/(\d+)/,80],[/Safari\//,/Version\/(\d+)/,14],[/Firefox\//,/Firefox\/(\d+)/,74]],t=0;t<r.length;t++){var n=r[t],o=n[0],s=n[1],a=n[2];if(e.match(o)){var u=e.match(new RegExp(s));if(u&&parseInt(u[1],10)>=a)return"es2020";break}}return"legacy"}(navigator.userAgent))?(s.type="module",s.src=a.USERFLOWJS_ES2020_URL||t+"es2020/userflow.js"):s.src=a.USERFLOWJS_LEGACY_URL||t+"legacy/userflow.js",s.onload=function(){r()},s.onerror=function(){document.head.removeChild(s),n=null;var e=new Error("Could not load Userflow.js");console.error(e.message),o(e)},document.head.appendChild(s)}))),n}};var o=e.USERFLOWJS_QUEUE=e.USERFLOWJS_QUEUE||[],s=function(e){r[e]=function(){var t=Array.prototype.slice.call(arguments);r.load(),o.push([e,null,t])}},a=function(e){r[e]=function(){var t,n=Array.prototype.slice.call(arguments);r.load();var s=new Promise((function(e,r){t={resolve:e,reject:r}}));return o.push([e,t,n]),s}},u=function(e,t){r[e]=function(){return t}};s("_setTargetEnv"),s("closeResourceCenter"),s("init"),s("off"),s("on"),s("prepareAudio"),s("registerCustomInput"),s("remount"),s("reset"),s("setBaseZIndex"),s("setCustomInputSelector"),s("setCustomNavigate"),s("setCustomScrollIntoView"),s("setInferenceAttributeFilter"),s("setInferenceAttributeNames"),s("setInferenceClassNameFilter"),s("setResourceCenterLauncherHidden"),s("setScrollPadding"),s("setShadowDomEnabled"),s("setPageTrackingDisabled"),s("setUrlFilter"),s("openResourceCenter"),s("toggleResourceCenter"),a("endAll"),a("endAllFlows"),a("endChecklist"),a("group"),a("identify"),a("identifyAnonymous"),a("start"),a("startFlow"),a("startWalk"),a("track"),a("updateGroup"),a("updateUser"),u("getResourceCenterState",null),u("isIdentified",!1)}}();

userflow.init("ct_dybdwc2fkna4lmih2zyqb6eune");
userflow.setResourceCenterLauncherHidden(true);

async function initAndClick() {
    // unclear why it needs to be called twice but otherwise you need to click the button twice.
    await userflow.identifyAnonymous({});
    await userflow.identifyAnonymous({});
    userflow.openResourceCenter()
}

// Userflow END
