(()=>{"use strict";var e={d:(t,n)=>{for(var l in n)e.o(n,l)&&!e.o(t,l)&&Object.defineProperty(t,l,{enumerable:!0,get:n[l]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r:e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}},t={};function n(e){var t,n=[].forEach,l=[].some,o=document.body,r=!0,i=" ";function s(t,l){var o,r,a,d=l.appendChild((o=t,r=document.createElement("li"),a=document.createElement("a"),e.listItemClass&&r.setAttribute("class",e.listItemClass),e.onClick&&(a.onclick=e.onClick),e.includeTitleTags&&a.setAttribute("title",o.textContent),e.includeHtml&&o.childNodes.length?n.call(o.childNodes,(function(e){a.appendChild(e.cloneNode(!0))})):a.textContent=o.textContent,a.setAttribute("href",e.basePath+"#"+o.id),a.setAttribute("class",e.linkClass+i+"node-name--"+o.nodeName+i+e.extraLinkClasses),r.appendChild(a),r));if(t.children.length){var u=c(t.isCollapsed);t.children.forEach((function(e){s(e,u)})),d.appendChild(u)}}function c(t){var n=e.orderedList?"ol":"ul",l=document.createElement(n),o=e.listClass+i+e.extraListClasses;return t&&(o=(o=o+i+e.collapsibleClass)+i+e.isCollapsedClass),l.setAttribute("class",o),l}function a(t){var n=0;return null!==t&&(n=t.offsetTop,e.hasInnerContainers&&(n+=a(t.offsetParent))),n}function d(e,t){return e&&e.className!==t&&(e.className=t),e}function u(t){return t&&-1!==t.className.indexOf(e.collapsibleClass)&&-1!==t.className.indexOf(e.isCollapsedClass)?(d(t,t.className.replace(i+e.isCollapsedClass,"")),u(t.parentNode.parentNode)):t}return{enableTocAnimation:function(){r=!0},disableTocAnimation:function(t){var n=t.target||t.srcElement;"string"==typeof n.className&&-1!==n.className.indexOf(e.linkClass)&&(r=!1)},render:function(e,n){var l=c(!1);if(n.forEach((function(e){s(e,l)})),null!==(t=e||t))return t.firstChild&&t.removeChild(t.firstChild),0===n.length?t:t.appendChild(l)},updateToc:function(s){var c;c=e.scrollContainer&&document.querySelector(e.scrollContainer)?document.querySelector(e.scrollContainer).scrollTop:document.documentElement.scrollTop||o.scrollTop,e.positionFixedSelector&&function(){var n;n=e.scrollContainer&&document.querySelector(e.scrollContainer)?document.querySelector(e.scrollContainer).scrollTop:document.documentElement.scrollTop||o.scrollTop;var l=document.querySelector(e.positionFixedSelector);"auto"===e.fixedSidebarOffset&&(e.fixedSidebarOffset=t.offsetTop),n>e.fixedSidebarOffset?-1===l.className.indexOf(e.positionFixedClass)&&(l.className+=i+e.positionFixedClass):l.className=l.className.replace(i+e.positionFixedClass,"")}();var f,m=s;if(r&&null!==t&&m.length>0){l.call(m,(function(t,n){return a(t)>c+e.headingsOffset+10?(f=m[0===n?n:n-1],!0):n===m.length-1?(f=m[m.length-1],!0):void 0}));var h=t.querySelector("."+e.activeLinkClass),p=t.querySelector("."+e.linkClass+".node-name--"+f.nodeName+'[href="'+e.basePath+"#"+f.id.replace(/([ #;&,.+*~':"!^$[\]()=>|/\\@])/g,"\\$1")+'"]');if(h===p)return;var C=t.querySelectorAll("."+e.linkClass);n.call(C,(function(t){d(t,t.className.replace(i+e.activeLinkClass,""))}));var g=t.querySelectorAll("."+e.listItemClass);n.call(g,(function(t){d(t,t.className.replace(i+e.activeListItemClass,""))})),p&&-1===p.className.indexOf(e.activeLinkClass)&&(p.className+=i+e.activeLinkClass);var v=p&&p.parentNode;v&&-1===v.className.indexOf(e.activeListItemClass)&&(v.className+=i+e.activeListItemClass);var S=t.querySelectorAll("."+e.listClass+"."+e.collapsibleClass);n.call(S,(function(t){-1===t.className.indexOf(e.isCollapsedClass)&&(t.className+=i+e.isCollapsedClass)})),p&&p.nextSibling&&-1!==p.nextSibling.className.indexOf(e.isCollapsedClass)&&d(p.nextSibling,p.nextSibling.className.replace(i+e.isCollapsedClass,"")),u(p&&p.parentNode.parentNode)}}}}e.r(t),e.d(t,{_buildHtml:()=>r,_headingsArray:()=>s,_options:()=>d,_parseContent:()=>i,_scrollListener:()=>c,destroy:()=>f,init:()=>u,refresh:()=>m});const l={tocSelector:".js-toc",contentSelector:".js-toc-content",headingSelector:"h1, h2, h3",ignoreSelector:".js-toc-ignore",hasInnerContainers:!1,linkClass:"toc-link",extraLinkClasses:"",activeLinkClass:"is-active-link",listClass:"toc-list",extraListClasses:"",isCollapsedClass:"is-collapsed",collapsibleClass:"is-collapsible",listItemClass:"toc-list-item",activeListItemClass:"is-active-li",collapseDepth:0,scrollSmooth:!0,scrollSmoothDuration:420,scrollSmoothOffset:0,scrollEndCallback:function(e){},headingsOffset:1,throttleTimeout:50,positionFixedSelector:null,positionFixedClass:"is-position-fixed",fixedSidebarOffset:"auto",includeHtml:!1,includeTitleTags:!1,onClick:function(e){},orderedList:!0,scrollContainer:null,skipRendering:!1,headingLabelCallback:!1,ignoreHiddenElements:!1,headingObjectCallback:null,basePath:"",disableTocScrollSync:!1,tocScrollOffset:0};function o(e){var t=e.duration,n=e.offset,l=location.hash?o(location.href):location.href;function o(e){return e.slice(0,e.lastIndexOf("#"))}document.body.addEventListener("click",(function(r){var i;"a"!==(i=r.target).tagName.toLowerCase()||!(i.hash.length>0||"#"===i.href.charAt(i.href.length-1))||o(i.href)!==l&&o(i.href)+"#"!==l||r.target.className.indexOf("no-smooth-scroll")>-1||"#"===r.target.href.charAt(r.target.href.length-2)&&"!"===r.target.href.charAt(r.target.href.length-1)||-1===r.target.className.indexOf(e.linkClass)||function(e,t){var n,l,o=window.pageYOffset,r={duration:t.duration,offset:t.offset||0,callback:t.callback,easing:t.easing||function(e,t,n,l){return(e/=l/2)<1?n/2*e*e+t:-n/2*(--e*(e-2)-1)+t}},i=document.querySelector('[id="'+decodeURI(e).split("#").join("")+'"]')||document.querySelector('[id="'+e.split("#").join("")+'"]'),s="string"==typeof e?r.offset+(e?i&&i.getBoundingClientRect().top||0:-(document.documentElement.scrollTop||document.body.scrollTop)):e,c="function"==typeof r.duration?r.duration(s):r.duration;function a(e){l=e-n,window.scrollTo(0,r.easing(l,o,s,c)),l<c?requestAnimationFrame(a):(window.scrollTo(0,o+s),"function"==typeof r.callback&&r.callback())}requestAnimationFrame((function(e){n=e,a(e)}))}(r.target.hash,{duration:t,offset:n,callback:function(){var e,t;e=r.target.hash,(t=document.getElementById(e.substring(1)))&&(/^(?:a|select|input|button|textarea)$/i.test(t.tagName)||(t.tabIndex=-1),t.focus())}})}),!1)}let r,i,s,c,a,d={};function u(e){d=function(){const e={};for(let t=0;t<arguments.length;t++){const n=arguments[t];for(const t in n)h.call(n,t)&&(e[t]=n[t])}return e}(l,e||{}),d.scrollSmooth&&(d.duration=d.scrollSmoothDuration,d.offset=d.scrollSmoothOffset,o(d)),r=n(d),i=function(e){var t=[].reduce;function n(e){return e[e.length-1]}function l(e){return+e.nodeName.toUpperCase().replace("H","")}function o(t){if(!function(e){try{return e instanceof window.HTMLElement||e instanceof window.parent.HTMLElement}catch(t){return e instanceof window.HTMLElement}}(t))return t;if(e.ignoreHiddenElements&&(!t.offsetHeight||!t.offsetParent))return null;const n=t.getAttribute("data-heading-label")||(e.headingLabelCallback?String(e.headingLabelCallback(t.innerText)):(t.innerText||t.textContent).trim());var o={id:t.id,children:[],nodeName:t.nodeName,headingLevel:l(t),textContent:n};return e.includeHtml&&(o.childNodes=t.childNodes),e.headingObjectCallback?e.headingObjectCallback(o,t):o}return{nestHeadingsArray:function(l){return t.call(l,(function(t,l){var r=o(l);return r&&function(t,l){for(var r=o(t),i=r.headingLevel,s=l,c=n(s),a=i-(c?c.headingLevel:0);a>0&&(!(c=n(s))||i!==c.headingLevel);)c&&void 0!==c.children&&(s=c.children),a--;i>=e.collapseDepth&&(r.isCollapsed=!0),s.push(r)}(r,t.nest),t}),{nest:[]})},selectHeadings:function(t,n){var l=n;e.ignoreSelector&&(l=n.split(",").map((function(t){return t.trim()+":not("+e.ignoreSelector+")"})));try{return t.querySelectorAll(l)}catch(e){return console.warn("Headers not found with selector: "+l),null}}}}(d),f();const t=function(e){try{return e.contentElement||document.querySelector(e.contentSelector)}catch(t){return console.warn("Contents element not found: "+e.contentSelector),null}}(d);if(null===t)return;const u=C(d);if(null===u)return;if(s=i.selectHeadings(t,d.headingSelector),null===s)return;const m=i.nestHeadingsArray(s).nest;if(d.skipRendering)return this;r.render(u,m),c=p((function(e){r.updateToc(s),!d.disableTocScrollSync&&function(e){var t=e.tocElement||document.querySelector(e.tocSelector);if(t&&t.scrollHeight>t.clientHeight){var n=t.querySelector("."+e.activeListItemClass);if(n){var l=t.scrollTop,o=l+t.clientHeight,r=n.offsetTop,i=r+n.clientHeight;r<l+e.tocScrollOffset?t.scrollTop-=l-r+e.tocScrollOffset:i>o-e.tocScrollOffset-30&&(t.scrollTop+=i-o+e.tocScrollOffset+60)}}}(d);const t=e&&e.target&&e.target.scrollingElement&&0===e.target.scrollingElement.scrollTop;(e&&(0===e.eventPhase||null===e.currentTarget)||t)&&(r.updateToc(s),d.scrollEndCallback&&d.scrollEndCallback(e))}),d.throttleTimeout),c(),d.scrollContainer&&document.querySelector(d.scrollContainer)?(document.querySelector(d.scrollContainer).addEventListener("scroll",c,!1),document.querySelector(d.scrollContainer).addEventListener("resize",c,!1)):(document.addEventListener("scroll",c,!1),document.addEventListener("resize",c,!1));let g=null;a=p((function(e){d.scrollSmooth&&r.disableTocAnimation(e),r.updateToc(s),g&&clearTimeout(g),g=setTimeout((function(){r.enableTocAnimation()}),d.scrollSmoothDuration)}),d.throttleTimeout),d.scrollContainer&&document.querySelector(d.scrollContainer)?document.querySelector(d.scrollContainer).addEventListener("click",a,!1):document.addEventListener("click",a,!1)}function f(){const e=C(d);null!==e&&(d.skipRendering||e&&(e.innerHTML=""),d.scrollContainer&&document.querySelector(d.scrollContainer)?(document.querySelector(d.scrollContainer).removeEventListener("scroll",c,!1),document.querySelector(d.scrollContainer).removeEventListener("resize",c,!1),r&&document.querySelector(d.scrollContainer).removeEventListener("click",a,!1)):(document.removeEventListener("scroll",c,!1),document.removeEventListener("resize",c,!1),r&&document.removeEventListener("click",a,!1)))}function m(e){f(),u(e||d)}const h=Object.prototype.hasOwnProperty;function p(e,t,n){let l,o;return t||(t=250),function(){const r=n||this,i=+new Date,s=arguments;l&&i<l+t?(clearTimeout(o),o=setTimeout((function(){l=i,e.apply(r,s)}),t)):(l=i,e.apply(r,s))}}function C(e){try{return e.tocElement||document.querySelector(e.tocSelector)}catch(t){return console.warn("TOC element not found: "+e.tocSelector),null}}var g,v;g="undefined"!=typeof global?global:window||global,v=function(e){const n=!!(e&&e.document&&e.document.querySelector&&e.addEventListener);if("undefined"!=typeof window||n)return e.tocbot=t,t},"function"==typeof define&&define.amd?define([],v(g)):"object"==typeof exports?module.exports=v(g):g.tocbot=v(g)})();
// TOC highlighting

tocbot.init({
  // Where to render the table of contents.
  tocSelector: '.td-toc',
  // Where to grab the headings to build the table of contents.
  contentSelector: '.td-content',
  // Which headings to grab inside of the contentSelector element.
  headingSelector: '.td-content > h2, .td-content > h3',
  // For headings inside relative or absolute positioned containers within content.
  hasInnerContainers: true,
  orderedList: false,
  scrollSmoothOffset: -32,
  headingsOffset: 120
});

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