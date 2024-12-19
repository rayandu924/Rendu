// frontend/scripts/patients.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const addPatientBtn = document.getElementById('add-patient-btn');
    const patientsList = document.getElementById('patients-list');
    const patientFormModal = document.getElementById('patient-form');
    const closeBtn = document.querySelector('.close-btn');
    const patientFormInner = document.getElementById('patient-form-inner');

    const fetchPatients = () => {
        console.log('Token utilisé pour la requête:', token);
        fetch('http://localhost:5000/api/patients', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                throw new Error('Format de données incorrect');
            }
            let html = '<table><thead><tr><th>Prénom</th><th>Nom</th><th>Genre</th><th>Date de Naissance</th><th>Contact</th><th>Actions</th></tr></thead><tbody>';
            data.forEach(patient => {
                html += `
                    <tr>
                        <td>${patient.first_name}</td>
                        <td>${patient.last_name}</td>
                        <td>${patient.gender}</td>
                        <td>${patient.birth_date}</td>
                        <td>${patient.contact}</td>
                        <td>
                            <button onclick="editPatient('${patient._id}')">Modifier</button>
                            <button onclick="deletePatient('${patient._id}')">Supprimer</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            patientsList.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
            patientsList.innerHTML = `<p>${error.message}</p>`;
        });
    };

    window.editPatient = (patientId) => {
        fetch(`http://localhost:5000/api/patients/${patientId}`, {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(patient => {
            document.getElementById('patient-id').value = patient._id;
            document.getElementById('first_name').value = patient.first_name;
            document.getElementById('last_name').value = patient.last_name;
            document.getElementById('gender').value = patient.gender;
            document.getElementById('birth_date').value = patient.birth_date;
            document.getElementById('contact').value = patient.contact;
            patientFormModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la récupération des informations du patient.');
        });
    };

    window.deletePatient = (patientId) => {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce patient?')) {
            fetch(`http://localhost:5000/api/patients/${patientId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
                }
                return response.json();
            })
            .then(data => {
                alert(data.message);
                fetchPatients();
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors de la suppression du patient.');
            });
        }
    };

    addPatientBtn.addEventListener('click', () => {
        patientFormInner.reset();
        document.getElementById('patient-id').value = '';
        patientFormModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        patientFormModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == patientFormModal) {
            patientFormModal.style.display = 'none';
        }
    };

    patientFormInner.addEventListener('submit', (e) => {
        e.preventDefault();
        const patientId = document.getElementById('patient-id').value;
        const firstName = document.getElementById('first_name').value.trim();
        const lastName = document.getElementById('last_name').value.trim();
        const gender = document.getElementById('gender').value;
        const birthDate = document.getElementById('birth_date').value;
        const contact = document.getElementById('contact').value.trim();

        if (!firstName || !lastName || !gender || !birthDate || !contact) {
            alert('Tous les champs sont obligatoires.');
            return;
        }

        const patientData = {
            first_name: firstName,
            last_name: lastName,
            gender: gender,
            birth_date: birthDate,
            contact: contact
        };

        const requestOptions = {
            method: patientId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(patientData)
        };

        const url = patientId 
            ? `http://localhost:5000/api/patients/${patientId}`
            : 'http://localhost:5000/api/patients';

        fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            patientFormModal.style.display = 'none';
            fetchPatients();
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'enregistrement du patient.');
        });
    });

    // Initialiser la liste des patients
    fetchPatients();
});
