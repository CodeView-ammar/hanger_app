document.addEventListener("DOMContentLoaded", function () {
    // Get references to the radio buttons and the adult and pedo sections
    var radioAdult = document.getElementById("reportTypeAdult");
    var radioPedo = document.getElementById("reportTypePedo");
    var adultSection = document.getElementById("adultSection");
    var pedoSection = document.getElementById("pedoSection");

    // Function to toggle visibility based on the selected radio button
    function toggleVisibility(adultSelected) {
      adultSection.style.display = adultSelected ? "block" : "none";
      pedoSection.style.display = adultSelected ? "none" : "block";
    }

    // Add event listeners to the radio buttons
    radioAdult.addEventListener("change", function () {
      toggleVisibility(true);
    });

    radioPedo.addEventListener("change", function () {
      toggleVisibility(false);
    });

    // Initial check to set the initial visibility based on the default checked state
    toggleVisibility(radioAdult.checked);
  });