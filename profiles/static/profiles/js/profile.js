// Change the country selector's colour if the placeholder value is selected.
let countrySelector = document.getElementById("id_default_country");
countrySelector.setAttribute("value", countrySelector.value);

countrySelector.addEventListener("change", () => {
  countrySelector.setAttribute("value", countrySelector.value);
});
