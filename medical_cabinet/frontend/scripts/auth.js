// frontend/scripts/auth.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const loginMessage = document.getElementById('login-message');

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            loginMessage.textContent = 'Nom d\'utilisateur et mot de passe requis.';
            loginMessage.style.color = 'red';
            return;
        }

        fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Échec de la connexion'); });
            }
            return response.json();
        })
        .then(data => {
            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
                window.location.href = 'index.html';
            } else {
                throw new Error('Token non reçu');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            loginMessage.textContent = error.message || 'Erreur lors de la connexion';
            loginMessage.style.color = 'red';
        });
    });
});
