// frontend/scripts/professionals.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const addProfessionalBtn = document.getElementById('add-professional-btn');
    const professionalsList = document.getElementById('professionals-list');
    const professionalFormModal = document.getElementById('professional-form');
    const closeBtn = document.querySelector('.close-btn');
    const professionalFormInner = document.getElementById('professional-form-inner');

    const fetchProfessionals = () => {
        fetch('http://localhost:5000/api/professionals', {
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
            let html = '<table><thead><tr><th>Prénom</th><th>Nom</th><th>Spécialité</th><th>Contact</th><th>Actions</th></tr></thead><tbody>';
            data.forEach(professional => {
                html += `
                    <tr>
                        <td>${professional.first_name}</td>
                        <td>${professional.last_name}</td>
                        <td>${professional.specialty}</td>
                        <td>${professional.contact}</td>
                        <td>
                            <button onclick="editProfessional('${professional._id}')">Modifier</button>
                            <button onclick="deleteProfessional('${professional._id}')">Supprimer</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            professionalsList.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
            professionalsList.innerHTML = `<p>${error.message}</p>`;
        });
    };

    window.editProfessional = (professionalId) => {
        fetch(`http://localhost:5000/api/professionals/${professionalId}`, {
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
        .then(professional => {
            document.getElementById('professional-id').value = professional._id;
            document.getElementById('first_name').value = professional.first_name;
            document.getElementById('last_name').value = professional.last_name;
            document.getElementById('specialty').value = professional.specialty;
            document.getElementById('contact').value = professional.contact;
            professionalFormModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la récupération des informations du professionnel.');
        });
    };

    window.deleteProfessional = (professionalId) => {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce professionnel?')) {
            fetch(`http://localhost:5000/api/professionals/${professionalId}`, {
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
                fetchProfessionals();
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors de la suppression du professionnel.');
            });
        }
    };

    addProfessionalBtn.addEventListener('click', () => {
        professionalFormInner.reset();
        document.getElementById('professional-id').value = '';
        professionalFormModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        professionalFormModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == professionalFormModal) {
            professionalFormModal.style.display = 'none';
        }
    };

    professionalFormInner.addEventListener('submit', (e) => {
        e.preventDefault();
        const professionalId = document.getElementById('professional-id').value;
        const firstName = document.getElementById('first_name').value.trim();
        const lastName = document.getElementById('last_name').value.trim();
        const specialty = document.getElementById('specialty').value.trim();
        const contact = document.getElementById('contact').value.trim();

        if (!firstName || !lastName || !specialty || !contact) {
            alert('Tous les champs sont obligatoires.');
            return;
        }

        const professionalData = {
            first_name: firstName,
            last_name: lastName,
            specialty: specialty,
            contact: contact
        };

        const requestOptions = {
            method: professionalId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(professionalData)
        };

        const url = professionalId 
            ? `http://localhost:5000/api/professionals/${professionalId}`
            : 'http://localhost:5000/api/professionals';

        fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            professionalFormModal.style.display = 'none';
            fetchProfessionals();
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'enregistrement du professionnel.');
        });
    });

    // Initialiser la liste des professionnels
    fetchProfessionals();
});
