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
    let menuChildren = menu.querySelector("span>ul").children;
    if (open) {
        for (let c of menuChildren) {
            c.classList.remove("collapse");
        }
    } else {
        for (let c of menuChildren) {
            c.classList.add("collapse");
        }
    }
    let pageChildrenPage = menu.querySelector("span>div>ul")
    if (pageChildrenPage) {
        let pageChildren = pageChildrenPage.children;
        if (pageChildren) {
            if (open) {
                for (let c of pageChildren) {
                    c.classList.remove("collapse");
                }
            } else {
                for (let c of pageChildren) {
                    c.classList.add("collapse");
                }
            }
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
