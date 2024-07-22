// JavaScript to hide flash messages after 3 seconds
setTimeout(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        message.style.display = 'none';
    });
}, 3000);