const allh2 = document.getElementsByTagName("h2");
for (i = 0; i < allh2.length; i++) {
  allh2[i].className += "show";
}

filterSelection("all")
function filterSelection(choice) {
  let x, i;
  x = document.getElementsByClassName("filterable");
  if (choice == "all") choice = "";
  for (i = 0; i < x.length; i++) {
    RemoveClass(x[i], "show");
    if (x[i].className.indexOf(choice) > -1) AddClass(x[i], "show");
  }
}

// Show filtered elements
function AddClass(element, name) {
  let i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function RemoveClass(element, name) {
  let i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Hide headings that don't contain anything
function cleanHeadings() {
  let headings = document.getElementsByTagName("h2")
  let lastclassname = "placeholder";
  for (let i = 0; i < headings.length; i++) {
    let nextel = headings[i].nextElementSibling;
    let nextSibTag = headings[i].nextElementSibling.tagName;
    while (nextSibTag  == "DIV") {
      lastclassname = nextel.className;
      if (nextel.className.includes("show")) {
        AddClass(headings[i], "show");
        RemoveClass(headings[i], "hidethisone");
        break;
      } else {
        RemoveClass(headings[i], "show");
        AddClass(headings[i], "hidethisone");
      }
      if (nextel.nextElementSibling) {
        nextSibTag = nextel.nextElementSibling.tagName;
        nextel = nextel.nextElementSibling;
      } else {
        break;
      }
    }
  }
}

// Add active class to the current control button (highlight it)
let btnContainer = document.getElementById("changelog-filters");
let btns = btnContainer.getElementsByClassName("filter-button");
for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    let current = document.getElementsByClassName("filter-button active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
    cleanHeadings()
  });
}