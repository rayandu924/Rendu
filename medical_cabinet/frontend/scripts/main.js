// frontend/scripts/main.js

document.addEventListener('DOMContentLoaded', () => {
    const homeBtn = document.getElementById('home');
    const patientsBtn = document.getElementById('patients');
    const professionalsBtn = document.getElementById('professionals');
    const appointmentsBtn = document.getElementById('appointments');
    const devicesBtn = document.getElementById('devices');
    const observationsBtn = document.getElementById('observations');
    const logoutBtn = document.getElementById('logout');
    const content = document.getElementById('content');

    homeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'index.html';
    });

    patientsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'patients.html';
    });

    professionalsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'professionals.html';
    });

    appointmentsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'appointments.html';
    });

    devicesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'devices.html';
    });

    observationsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'observations.html';
    });

    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    });

    // Vérifier si l'utilisateur est authentifié
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }
});
