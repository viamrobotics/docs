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
