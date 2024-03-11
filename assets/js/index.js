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

// TOC highlighting

var toc = document.querySelector( '#TableOfContents' );
var tocItems;

// Factor of screen size that the element must cross
// before it's considered visible
var TOP_MARGIN = 0.1,
BOTTOM_MARGIN = 0.2;

if (toc) {
    window.addEventListener( 'resize', getTocItems, false );
    window.addEventListener( 'scroll', setActiveElements, false );

    getTocItems();

    function getTocItems() {
        tocItems = [].slice.call( toc.querySelectorAll( 'li' ) );

        // Cache element references and measurements
        tocItems = tocItems.map( function( item ) {
            var anchor = item.querySelector( 'a' );
            if(anchor) {
                var target = document.getElementById( anchor.getAttribute( 'href' ).slice( 1 ) );

                return {
                    listItem: item,
                    anchor: anchor,
                    target: target
                };
            }
        } );

        setActiveElements();
    }

    function setActiveElements() {
        var windowHeight = window.innerHeight;
        var visibleItems = 0;

        // ensure at least one elem visible
        let atLeastOne = false;
        let lastElem;

        for (var i = 0; i < tocItems.length; i++) {
            let item = tocItems[i];
            if (item && item.target) {

                var targetBounds = item.target.getBoundingClientRect();

                if( targetBounds.bottom > windowHeight * TOP_MARGIN && targetBounds.top < windowHeight * ( 1 - BOTTOM_MARGIN ) ) {
                    visibleItems += 1;
                    item.listItem.classList.add( 'toc-active' );
                    atLeastOne = true;
                } else {
                    item.listItem.classList.remove( 'toc-active' );
                }

                if (targetBounds.bottom < windowHeight) {
                    lastElem = item;
                }
            }

        }

        if (!atLeastOne && lastElem) {
            lastElem.listItem.classList.add( 'toc-active' );
        }
    }
}

// script for the scroll button
const main = document.body;
const scrollBtn = document.getElementById("scrollButton");
function toTop() {
    window.scroll({top: 0, left: 0, behavior: 'smooth'});
}

function btnVisibility(payload) {
    if (payload[0].boundingClientRect.y <= -400) {
        scrollBtn.style.visibility = "visible";
    } else {
        scrollBtn.style.visibility = "hidden";
    }
}

if(main && scrollBtn) {
    const observer = new IntersectionObserver(btnVisibility, {
        threshold: [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    });
    observer.observe(main);
}

docsearch({
    inputSelector: '.navbar-nav .td-search-input',
    typesenseCollectionName: 'docsearch',
    typesenseServerConfig: {
      nodes: [{
        host: 'cgnvrk0xwyj9576lp-1.a1.typesense.net',
        port: '443',
        protocol: 'https'
      }],
      apiKey: 'GHQK6od8KfpvTEh4YpA113gUc2dU5fGR'
    }
  });
  docsearch({
    inputSelector: '.td-sidebar__search .td-search-input',
    typesenseCollectionName: 'docsearch',
    typesenseServerConfig: {
      nodes: [{
        host: 'cgnvrk0xwyj9576lp-1.a1.typesense.net',
        port: '443',
        protocol: 'https'
      }],
      apiKey: 'GHQK6od8KfpvTEh4YpA113gUc2dU5fGR'
    }
});