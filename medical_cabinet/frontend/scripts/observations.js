// frontend/scripts/observations.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const addObservationBtn = document.getElementById('add-observation-btn');
    const observationsList = document.getElementById('observations-list');
    const observationFormModal = document.getElementById('observation-form');
    const closeBtn = document.querySelector('.close-btn');
    const observationFormInner = document.getElementById('observation-form-inner');

    const fetchObservations = () => {
        fetch('http://localhost:5000/api/observations', {
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
            let html = '<table><thead><tr><th>Patient</th><th>Date et Heure</th><th>Tension Systolique</th><th>Tension Diastolique</th><th>Rythme Cardiaque</th><th>Oxymétrie</th><th>Actions</th></tr></thead><tbody>';
            data.forEach(observation => {
                html += `
                    <tr>
                        <td>${observation.patient ? observation.patient.first_name + ' ' + observation.patient.last_name : 'N/A'}</td>
                        <td>${new Date(observation.date).toLocaleString()}</td>
                        <td>${observation.tension_systolic}</td>
                        <td>${observation.tension_diastolic}</td>
                        <td>${observation.rythme_cardiaque}</td>
                        <td>${observation.oxymetrie}</td>
                        <td>
                            <button onclick="editObservation('${observation._id}')">Modifier</button>
                            <button onclick="deleteObservation('${observation._id}')">Supprimer</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            observationsList.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
            observationsList.innerHTML = `<p>${error.message}</p>`;
        });
    };

    const fetchPatients = () => {
        return fetch('http://localhost:5000/api/patients', {
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
            const patientSelect = document.getElementById('patient_id');
            patientSelect.innerHTML = '<option value="">Sélectionner un patient</option>';
            data.forEach(patient => {
                patientSelect.innerHTML += `<option value="${patient._id}">${patient.first_name} ${patient.last_name}</option>`;
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    };

    window.editObservation = (observationId) => {
        fetch(`http://localhost:5000/api/observations/${observationId}`, {
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
        .then(observation => {
            document.getElementById('observation-id').value = observation._id;
            document.getElementById('patient_id').value = observation.patient ? observation.patient._id : '';
            document.getElementById('date').value = new Date(observation.date).toISOString().slice(0,16);
            document.getElementById('tension_systolic').value = observation.tension_systolic;
            document.getElementById('tension_diastolic').value = observation.tension_diastolic;
            document.getElementById('rythme_cardiaque').value = observation.rythme_cardiaque;
            document.getElementById('oxymetrie').value = observation.oxymetrie;
            observationFormModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la récupération des informations de l\'observation.');
        });
    };

    window.deleteObservation = (observationId) => {
        if (confirm('Êtes-vous sûr de vouloir supprimer cette observation?')) {
            fetch(`http://localhost:5000/api/observations/${observationId}`, {
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
                fetchObservations();
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors de la suppression de l\'observation.');
            });
        }
    };

    addObservationBtn.addEventListener('click', async () => {
        try {
            await fetchPatients();
            observationFormInner.reset();
            document.getElementById('observation-id').value = '';
            observationFormModal.style.display = 'block';
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la préparation du formulaire d\'observation.');
        }
    });

    closeBtn.addEventListener('click', () => {
        observationFormModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == observationFormModal) {
            observationFormModal.style.display = 'none';
        }
    };

    observationFormInner.addEventListener('submit', (e) => {
        e.preventDefault();
        const observationId = document.getElementById('observation-id').value;
        const patientId = document.getElementById('patient_id').value;
        const date = document.getElementById('date').value;
        const tension_systolic = parseInt(document.getElementById('tension_systolic').value, 10);
        const tension_diastolic = parseInt(document.getElementById('tension_diastolic').value, 10);
        const rythme_cardiaque = parseInt(document.getElementById('rythme_cardiaque').value, 10);
        const oxymetrie = parseInt(document.getElementById('oxymetrie').value, 10);

        if (!patientId || !date || isNaN(tension_systolic) || isNaN(tension_diastolic) || isNaN(rythme_cardiaque) || isNaN(oxymetrie)) {
            alert('Tous les champs sont obligatoires et doivent être valides.');
            return;
        }

        const observationData = {
            patient_id: patientId,
            date: new Date(date).toISOString(),
            tension_systolic: tension_systolic,
            tension_diastolic: tension_diastolic,
            rythme_cardiaque: rythme_cardiaque,
            oxymetrie: oxymetrie
        };

        const requestOptions = {
            method: observationId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(observationData)
        };

        const url = observationId 
            ? `http://localhost:5000/api/observations/${observationId}`
            : 'http://localhost:5000/api/observations';

        fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            observationFormModal.style.display = 'none';
            fetchObservations();
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'enregistrement de l\'observation.');
        });
    });

    // Initialiser la liste des observations
    fetchObservations();
});
