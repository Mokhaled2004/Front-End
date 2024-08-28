document.querySelectorAll('.menu').forEach(menu => {
    const navText = menu.querySelector('.nav-text');
    const nestedMenu = menu.querySelector('.nested-menu');

    navText.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior

        // Toggle the 'open' class on the parent menu
        menu.classList.toggle('open');

        // Ensure the menu container height adjusts to fit the nested menu
        if (menu.classList.contains('open')) {
            nestedMenu.style.display = 'flex';
            menu.style.marginBottom = nestedMenu.offsetHeight + 'px'; // Adjust margin based on nested menu height
        } else {
            nestedMenu.style.display = 'none';
            menu.style.marginBottom = '0'; // Reset margin when menu is hidden
        }
    });
});
