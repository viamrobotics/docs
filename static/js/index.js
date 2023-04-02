// script for menu toggles
var siteMenuSubmenus = document.getElementsByClassName(
    "td-sidebar-nav__section-title td-sidebar-nav__section with-child"
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
    let toggle = menu.querySelector("span").querySelector(".submenu-toggle");
    if (toggle) {
        if (menu.classList.contains('empty-node-submenu')) {
            menu.querySelector("span").addEventListener('click', function () {
                submenuToggle(menu, toggle);
            });
        } else {
            toggle.addEventListener('click', function () {
                submenuToggle(menu, toggle);
            });
        }
    }
};

// TOC highlighting

var toc = document.querySelector( '#TableOfContents' );
var tocItems;

// Factor of screen size that the element must cross
// before it's considered visible
var TOP_MARGIN = 0.1,
BOTTOM_MARGIN = 0.2;

window.addEventListener( 'resize', getTocItems, false );
window.addEventListener( 'scroll', setActiveElements, false );

getTocItems();

function getTocItems() {
    tocItems = [].slice.call( toc.querySelectorAll( 'li' ) );

    // Cache element references and measurements
    tocItems = tocItems.map( function( item ) {
        var anchor = item.querySelector( 'a' );
        var target = document.getElementById( anchor.getAttribute( 'href' ).slice( 1 ) );

        return {
            listItem: item,
            anchor: anchor,
            target: target
        };
    } );

    setActiveElements();
}

function setActiveElements() {
    var windowHeight = window.innerHeight;
    var visibleItems = 0;

    tocItems.forEach( function( item ) {
        var targetBounds = item.target.getBoundingClientRect();

        if( targetBounds.bottom > windowHeight * TOP_MARGIN && targetBounds.top < windowHeight * ( 1 - BOTTOM_MARGIN ) ) {
            visibleItems += 1;
            item.listItem.classList.add( 'toc-active' );
        }
        else {
            item.listItem.classList.remove( 'toc-active' );
        }
    } );
}
