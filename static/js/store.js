document.addEventListener('DOMContentLoaded', function () {
    const nameSearchInput = document.querySelector('.name-search-bar');
    const addressSearchInput = document.querySelector('.search-bar2');
    const categoryCheckboxes = document.querySelectorAll('.category-checkbox'); // Select checkboxes
    const storeItems = document.querySelectorAll('.store-item');

    function filterStores() {
        const nameSearchValue = nameSearchInput.value.toLowerCase().trim();
        const addressSearchValue = addressSearchInput.value.toLowerCase().trim();
        const selectedCategories = Array.from(categoryCheckboxes)
                                        .filter(checkbox => checkbox.checked)
                                        .map(checkbox => checkbox.nextElementSibling.textContent.toLowerCase().trim()); // Get category names

        storeItems.forEach(function (storeItem) {
            const storeName = storeItem.querySelector('.store-name').textContent.toLowerCase();
            const storeAddress = storeItem.querySelector('.store-address').textContent.toLowerCase();
            const storeCategory = storeItem.querySelector('.store-category').textContent.toLowerCase(); // Make sure the store category is correctly identified

            const matchesName = storeName.includes(nameSearchValue);
            const matchesAddress = storeAddress.includes(addressSearchValue);
            const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(storeCategory);

            // Show store item if it matches all criteria
            if (matchesName && matchesAddress && matchesCategory) {
                storeItem.parentElement.style.display = 'block'; // Show matching store
            } else if (!nameSearchValue && !addressSearchValue && selectedCategories.length === 0) {
                storeItem.parentElement.style.display = 'block'; // Show all if no filters
            } else {
                storeItem.parentElement.style.display = 'none'; // Hide non-matching store
            }
        });
    }

    // Add event listeners for search inputs and category checkboxes
    nameSearchInput.addEventListener('input', filterStores);
    addressSearchInput.addEventListener('input', filterStores);
    categoryCheckboxes.forEach(checkbox => checkbox.addEventListener('change', filterStores));
});

// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the toggle button and filter container
    const toggleButton = document.querySelector('.toggle-filters-btn');
    const filterContainer = document.querySelector('.filter-container');

    // Check if both elements exist before adding event listener
    if (toggleButton && filterContainer) {
        // Add click event listener to the toggle button
        toggleButton.addEventListener('click', function() {
            // Toggle the 'show' class on the filter container
            filterContainer.classList.toggle('show');
            // Hide or show the toggle button based on the filter container's visibility
            if (filterContainer.classList.contains('show')) {
                toggleButton.style.display = 'none'; // Hide the toggle button
            } else {
                toggleButton.style.display = 'block'; // Show the toggle button
            }
        });

        // Optional: Show the toggle button if the user clicks outside the filter container
        document.addEventListener('click', function(event) {
            if (!filterContainer.contains(event.target) && !toggleButton.contains(event.target)) {
                filterContainer.classList.remove('show');
                toggleButton.style.display = 'block'; // Ensure the button is visible when filter is hidden
            }
        });
    }
});





