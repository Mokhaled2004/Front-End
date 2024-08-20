document.addEventListener("DOMContentLoaded", function () {
    const userStores = document.querySelector(".user-stores");

    // Check if the user-stores container has any child elements
    if (userStores.children.length === 0) {
        userStores.style.marginBottom = "8rem";
    } else {
        userStores.style.marginBottom = "-8rem";
    }
});
