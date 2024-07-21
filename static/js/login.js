document.addEventListener("DOMContentLoaded", function() {
    // Get references to the form elements and tab buttons
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const tabButtons = document.querySelectorAll(".tab-button");

    // Function to show the specified form and hide the other
    function showForm(formId) {
        if (formId === 'login') {
            loginForm.classList.remove("hide");
            loginForm.classList.add("show");
            registerForm.classList.remove("show");
            registerForm.classList.add("hide");
        } else if (formId === 'register') {
            registerForm.classList.remove("hide");
            registerForm.classList.add("show");
            loginForm.classList.remove("show");
            loginForm.classList.add("hide");
        }

        // Update active tab button
        tabButtons.forEach(button => {
            if (button.getAttribute("onclick").includes(formId)) {
                button.classList.add("active");
            } else {
                button.classList.remove("active");
            }
        });
    }

    // Add event listeners to tab buttons
    tabButtons.forEach(button => {
        button.addEventListener("click", function() {
            const formId = this.getAttribute("onclick").split('\'')[1];
            showForm(formId);
        });
    });

    // Initialize with the login form shown
    showForm('login');
});
