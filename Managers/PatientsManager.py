# Импортируем нужные классы из нашей папки
from PatientDataModels.Patient import Patient
from PatientDataModels.Embrion import Embrion

# Класс для управления пациентами
class PatientsManager:
    # Лист пациентов, его ты уже видел
    patients = [
        Patient(0, 26, "Lasha", [Embrion.embrion_4AB, Embrion.embrion_3BB]),
        Patient(1, 37, "Artur", [Embrion.embrion_4AB]),
        Patient(2, 36, "Nikita", []),
        Patient(3, 41, "Max", []),
        Patient(4, 46, "Incognito", [])
    ]

    # Функция добавления пациентов, но сейчас не используется
    def add_patient(self, patient):
        self.patients.append(patient)

    # Функция запроса пациентов(теперь без фильтра, объяснение в GUIManager.py на 165 строчке)
    def fetch_patients(self):
        return self.patients
