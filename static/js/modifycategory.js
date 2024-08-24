document.addEventListener("DOMContentLoaded", function() {
    const dropdownIcon = document.querySelector('.img3.dropdown-icon');
    const editSection = document.querySelector('.edit-section');

    dropdownIcon.addEventListener('click', function() {
        if (editSection.style.display === "none" || editSection.style.display === "") {
            editSection.style.display = "block";
        } else {
            editSection.style.display = "none";
        }
    });
});
