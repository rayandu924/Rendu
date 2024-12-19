// frontend/scripts/appointments.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const addAppointmentBtn = document.getElementById('add-appointment-btn');
    const appointmentsList = document.getElementById('appointments-list');
    const appointmentFormModal = document.getElementById('appointment-form');
    const closeBtn = document.querySelector('.close-btn');
    const appointmentFormInner = document.getElementById('appointment-form-inner');

    const fetchAppointments = () => {
        fetch('http://localhost:5000/api/appointments', {
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
            let html = '<table><thead><tr><th>Patient</th><th>Professionnel</th><th>Date et Heure</th><th>Motif</th><th>Actions</th></tr></thead><tbody>';
            data.forEach(appointment => {
                html += `
                    <tr>
                        <td>${appointment.patient ? appointment.patient.first_name + ' ' + appointment.patient.last_name : 'N/A'}</td>
                        <td>${appointment.professional ? appointment.professional.first_name + ' ' + appointment.professional.last_name : 'N/A'}</td>
                        <td>${new Date(appointment.date).toLocaleString()}</td>
                        <td>${appointment.reason}</td>
                        <td>
                            <button onclick="editAppointment('${appointment._id}')">Modifier</button>
                            <button onclick="deleteAppointment('${appointment._id}')">Supprimer</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            appointmentsList.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
            appointmentsList.innerHTML = `<p>${error.message}</p>`;
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

    const fetchProfessionals = () => {
        return fetch('http://localhost:5000/api/professionals', {
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
            const professionalSelect = document.getElementById('professional_id');
            professionalSelect.innerHTML = '<option value="">Sélectionner un professionnel</option>';
            data.forEach(professional => {
                professionalSelect.innerHTML += `<option value="${professional._id}">${professional.first_name} ${professional.last_name}</option>`;
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    };

    window.editAppointment = (appointmentId) => {
        fetch(`http://localhost:5000/api/appointments/${appointmentId}`, {
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
        .then(appointment => {
            document.getElementById('appointment-id').value = appointment._id;
            document.getElementById('patient_id').value = appointment.patient ? appointment.patient._id : '';
            document.getElementById('professional_id').value = appointment.professional ? appointment.professional._id : '';
            document.getElementById('date').value = new Date(appointment.date).toISOString().slice(0,16);
            document.getElementById('reason').value = appointment.reason;
            appointmentFormModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la récupération des informations du rendez-vous.');
        });
    };

    window.deleteAppointment = (appointmentId) => {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce rendez-vous?')) {
            fetch(`http://localhost:5000/api/appointments/${appointmentId}`, {
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
                fetchAppointments();
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors de la suppression du rendez-vous.');
            });
        }
    };

    addAppointmentBtn.addEventListener('click', async () => {
        try {
            await fetchPatients();
            await fetchProfessionals();
            appointmentFormInner.reset();
            document.getElementById('appointment-id').value = '';
            appointmentFormModal.style.display = 'block';
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la préparation du formulaire de rendez-vous.');
        }
    });

    closeBtn.addEventListener('click', () => {
        appointmentFormModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == appointmentFormModal) {
            appointmentFormModal.style.display = 'none';
        }
    };

    appointmentFormInner.addEventListener('submit', (e) => {
        e.preventDefault();
        const appointmentId = document.getElementById('appointment-id').value;
        const patientId = document.getElementById('patient_id').value;
        const professionalId = document.getElementById('professional_id').value;
        const date = document.getElementById('date').value;
        const reason = document.getElementById('reason').value;

        const appointmentData = {
            patient_id: patientId,
            professional_id: professionalId,
            date: new Date(date).toISOString(),
            reason: reason
        };

        const requestOptions = {
            method: appointmentId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(appointmentData)
        };

        const url = appointmentId 
            ? `http://localhost:5000/api/appointments/${appointmentId}`
            : 'http://localhost:5000/api/appointments';

        fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            appointmentFormModal.style.display = 'none';
            fetchAppointments();
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'enregistrement du rendez-vous.');
        });
    });

    // Initialiser la liste des rendez-vous
    fetchAppointments();
});
