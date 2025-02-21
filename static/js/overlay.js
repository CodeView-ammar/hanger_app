document.addEventListener('DOMContentLoaded', function () {
    // Get the modal and overlay elements using the new class "overlay-info"
    var modal = document.querySelector('.overlay-info');
    var overlay = document.querySelector('.overlay-info'); // Use the same class as the modal
    
    // Function to show the overlay
    window.showOverlay = function () {
      // Remove the d-none class and add the d-block class to show the modal and overlay
      modal.classList.remove('d-none');
      overlay.classList.remove('d-none');
    };
  });
  
  