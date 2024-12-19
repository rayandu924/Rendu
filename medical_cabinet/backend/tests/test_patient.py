import pytest
from models.patient import create_patient, get_patient_by_id, update_patient, delete_patient

@pytest.fixture
def sample_patient():
    patient_data = {
        "first_name": "Jean",
        "last_name": "Dupont",
        "gender": "male",
        "birth_date": "1980-01-01",
        "contact": "jean.dupont@example.com"
    }
    create_patient(patient_data)
    yield patient_data
    # Nettoyer après le test
    patient = get_patient_by_id(patient_data['_id'])
    if patient:
        delete_patient(patient['_id'])

def test_create_patient(sample_patient):
    patient = get_patient_by_id(sample_patient['_id'])
    assert patient is not None
    assert patient['first_name'] == "Jean"

def test_update_patient(sample_patient):
    update_data = {"last_name": "Durand"}
    update_patient(sample_patient['_id'], update_data)
    patient = get_patient_by_id(sample_patient['_id'])
    assert patient['last_name'] == "Durand"

def test_delete_patient(sample_patient):
    delete_patient(sample_patient['_id'])
    patient = get_patient_by_id(sample_patient['_id'])
    assert patient is None
