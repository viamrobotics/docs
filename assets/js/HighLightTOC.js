class HighlightTOC {
  constructor(tocElement) {
    this._tocElement = tocElement;

    this._index = 0;
    this._offset = window.pageYOffset;
    this._scrollDirection = false; // = Up/down -> down
    this._updateTimeout = null;

    this._elements = tocElement.querySelectorAll("a");
    this._anchors = [].reduce.call(
      this._elements,
      (anchors, el) => {
        const hash = decodeURIComponent(el.hash);
        return anchors.concat(document.getElementById(hash.substring(1)) || []);
      },
      []
    );

    // TODO work-around: ideally this would be done in HTML/CSS/Hugo but it is easier to do in JS
    if (this._elements.length === 0) {
      tocElement.parentNode.children[0].style.display = "none";
      document.querySelectorAll(".mobile-toc-icon").forEach(e => { e.style.display = "none" }); // TODO hardcoded name
      document.querySelectorAll(".side-control").forEach((e) => (e.style.display = "none")); // TODO hardcoded name
      document.getElementById("side-control").checked = false; // TODO hardcoded name
      tocElement.style.display = "none";
      return;
    }

    var tocWrapper = document.querySelector(".content-side"); // TODO hard coded name
    this._isElementVisible = tocWrapper.clientHeight !== 0 && tocWrapper.clientWidth !== 0;

    // Wire events
    window.addEventListener("scroll", () => {
      clearTimeout(this._updateTimeout); // Prevents the previous task from executing

      this._updateTimeout = window.setTimeout(() => { this._update(); }, 100); // Delay is required because some websites have a scroll delay which would cause _update to block scrolling. Effectively break the TOC links.
    });
    window.addEventListener("resize", () => { this._resize(); });
    new ResizeObserver(elems => { this._visibilityChanged(elems[0]); }).observe(tocWrapper); // Ideally we could detect this from the TOC element itself

    this._update();
  }

  _update() {
    // No need to waste CPU cycles; alternatively we could unsubscribe
    if (!this._isElementVisible) {
      return;
    }

    // offset = scroll position + height of the viewport
    const offset = (window.pageYOffset || document.documentElement.scrollTop) + (window.innerHeight || document.documentElement.clientHeight);
    const direction = this._offset - offset < 0;

    // Reset highlight
    this._elements[this._index].dataset.current = "";

    // Hack: reset index if direction changed to catch very fast scrolling, because otherwise we would have to register a timer and that sucks
    if (this._scrollDirection !== direction) this._index = direction ? (this._index = 0) : (this._index = this._elements.length - 1);

    // Scroll direction is down
    if (this._offset <= offset) {
      for (let i = this._index + 1; i < this._elements.length; i++) {
        if (this._anchors[i].offsetTop <= offset) {
          if (i > 0) this._elements[i - 1].dataset.state = "visited";
          this._index = i;
        } else {
          break;
        }
      }
    } else {
      //  Scroll direction is up
      for (let i = this._index; i >= 0; i--) {
        if (this._anchors[i].offsetTop > offset) {
          if (i > 0) this._elements[i - 1].dataset.state = "";
        } else {
          this._index = i;
          break;
        }
      }
    }

    // Highlight current
    // Optional: we could highlight/active all currently visible TOC entries instead of only the last one.
    const currentElement = this._elements[this._index];
    currentElement.dataset.current = "active";
    currentElement.scrollIntoView(false);

    this._offset = offset;
    this._scrollDirection = direction;
  }

  _visibilityChanged(elem) {
    const wasVisible = this._isElementVisible;

    this._isElementVisible = elem.contentRect.inlineSize !== 0 && elem.contentRect.blockSize !== 0;
    if (wasVisible !== this._isElementVisible) {
      if (this._isElementVisible) {
        this._update();
      } else {
        this._reset();
      }
    }
  }

  _resize() {
    this._reset();
    this._update();
  }

  _reset() {
    Array.prototype.forEach.call(this._elements, (el) => {
      el.dataset.state = "";
      el.dataset.current = "";
    });

    this._index = 0;
    this._offset = 0;
    this._scrollDirection = false;
  }
}

// ==========================================================================

window.addEventListener("load", function () {
  const tocElement = document.getElementById("TableOfContents"); // TOC element created by Hugo
  if (tocElement) { // Not all pages contain a TOC
    new HighlightTOC(tocElement);
  }
});