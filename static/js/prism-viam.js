(function () {
  document.querySelectorAll(".code-toolbar").forEach((el) => {
    el.classList.add('highlight');
  });
  document.querySelectorAll("body").forEach((el) => {
    el.classList.add('no-line-numbers');
  });
  var obs = new MutationObserver(function (e) {
    Prism.highlightAll();
  });
  document.querySelectorAll(".tab-pane").forEach((el) => {
    obs.observe(el, { attributes: true });
  });
  Prism.highlightAll()
  // need two passes for whatever reason; who cares
  Prism.highlightAll()
}())
