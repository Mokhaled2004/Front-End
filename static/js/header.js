document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.menue');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    menuButton.addEventListener('click', () => {
        // Toggle the visibility of the dropdown menu
        if (dropdownContent.classList.contains('show-dropdown')) {
            dropdownContent.classList.remove('show-dropdown');
        } else {
            dropdownContent.classList.add('show-dropdown');
        }
    });

    // Optionally, close the dropdown when clicking outside of it
    document.addEventListener('click', (event) => {
        if (!menuButton.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.classList.remove('show-dropdown');
        }
    });
});

document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', () => {
        const url = item.getAttribute('data-url');
        if (url) {
            window.location.href = url;
        }
    });
});
