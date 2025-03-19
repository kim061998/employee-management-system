document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Simple client-side validation
            if (username === '' || password === '') {
                alert('Please fill in both fields.');
                return;
            }

            // Simulate a login request (this should be replaced with an actual AJAX call)
            alert('Logging in as ' + username);
            // Here you would typically send the data to the server
        });
    }
});