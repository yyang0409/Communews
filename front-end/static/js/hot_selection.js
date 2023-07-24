function hot_selection(){
    // Function to handle the page transfer when an option is selected
    function handleDropdownChange() {
      var selectedValue = document.getElementById("dropdown").value;

      // Check if a valid option is selected
      if (selectedValue !== "") {
        // Redirect to the selected page
        window.location.href = selectedValue;
      }
    }

    // Add an event listener to the dropdown to trigger the page transfer on change
    document.getElementById("dropdown").addEventListener("change", handleDropdownChange);
}

hot_selection()