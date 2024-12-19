// frontend/scripts/devices.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const addDeviceBtn = document.getElementById('add-device-btn');
    const devicesList = document.getElementById('devices-list');
    const deviceFormModal = document.getElementById('device-form');
    const closeBtn = document.querySelector('.close-btn');
    const deviceFormInner = document.getElementById('device-form-inner');

    const fetchDevices = () => {
        fetch('http://localhost:5000/api/devices', {
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
            let html = '<table><thead><tr><th>Nom du Dispositif</th><th>Type</th><th>Patient</th><th>Actions</th></tr></thead><tbody>';
            data.forEach(device => {
                html += `
                    <tr>
                        <td>${device.device_name}</td>
                        <td>${device.device_type}</td>
                        <td>${device.patient ? device.patient.first_name + ' ' + device.patient.last_name : 'N/A'}</td>
                        <td>
                            <button onclick="editDevice('${device._id}')">Modifier</button>
                            <button onclick="deleteDevice('${device._id}')">Supprimer</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            devicesList.innerHTML = html;
        })
        .catch(error => {
            console.error('Erreur:', error);
            devicesList.innerHTML = `<p>${error.message}</p>`;
        });
    };

    const fetchPatientsForDevices = () => {
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

    window.editDevice = (deviceId) => {
        fetch(`http://localhost:5000/api/devices/${deviceId}`, {
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
        .then(device => {
            document.getElementById('device-id').value = device._id;
            document.getElementById('device_name').value = device.device_name;
            document.getElementById('device_type').value = device.device_type;
            document.getElementById('patient_id').value = device.patient ? device.patient._id : '';
            deviceFormModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la récupération des informations du dispositif médical.');
        });
    };

    window.deleteDevice = (deviceId) => {
        if (confirm('Êtes-vous sûr de vouloir supprimer ce dispositif médical?')) {
            fetch(`http://localhost:5000/api/devices/${deviceId}`, {
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
                fetchDevices();
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors de la suppression du dispositif médical.');
            });
        }
    };

    addDeviceBtn.addEventListener('click', async () => {
        try {
            await fetchPatientsForDevices();
            deviceFormInner.reset();
            document.getElementById('device-id').value = '';
            deviceFormModal.style.display = 'block';
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la préparation du formulaire de dispositif médical.');
        }
    });

    closeBtn.addEventListener('click', () => {
        deviceFormModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == deviceFormModal) {
            deviceFormModal.style.display = 'none';
        }
    };

    deviceFormInner.addEventListener('submit', (e) => {
        e.preventDefault();
        const deviceId = document.getElementById('device-id').value;
        const deviceName = document.getElementById('device_name').value.trim();
        const deviceType = document.getElementById('device_type').value.trim();
        const patientId = document.getElementById('patient_id').value;

        if (!deviceName || !deviceType || !patientId) {
            alert('Tous les champs sont obligatoires.');
            return;
        }

        const deviceData = {
            device_name: deviceName,
            device_type: deviceType,
            patient_id: patientId
        };

        const requestOptions = {
            method: deviceId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(deviceData)
        };

        const url = deviceId 
            ? `http://localhost:5000/api/devices/${deviceId}`
            : 'http://localhost:5000/api/devices';

        fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            deviceFormModal.style.display = 'none';
            fetchDevices();
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la création ou de la mise à jour du dispositif médical.');
        });
    });

    // Initialiser la liste des dispositifs médicaux
    fetchDevices();
});
