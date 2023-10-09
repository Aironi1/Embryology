# Импортируем нужные классы из нашей папки
from PatientDataModels.Patient import Patient
from PatientDataModels.Embrion import Embrion
from Managers.DatabaseManager import DatabaseManager

# Класс для управления пациентами
class PatientsManager:
    database_manager = DatabaseManager()
    # def __init__(self):
    #     patients = [
    #         Patient(0, 26, "Lasha", [Embrion.embrion_4AB, Embrion.embrion_3BB]),
    #         Patient(1, 37, "Artur", [Embrion.embrion_4AB]),
    #         Patient(2, 36, "Nikita", []),
    #         Patient(3, 41, "Max", []),
    #         Patient(4, 46, "Incognito", [])
    #     ]
    #
    #     self.database_manager.clear_database()
    #     for patient in patients:
    #         self.database_manager.add_patient(patient)

    # Функция добавления пациентов, но сейчас не используется
    def add_patient(self, patient: Patient):
        self.database_manager.add_patient(patient)

    # Функция запроса пациентов(теперь без фильтра, объяснение в GUIManager.py на 165 строчке)
    def fetch_patients(self) -> [Patient]:
        return self.database_manager.get_patients()
