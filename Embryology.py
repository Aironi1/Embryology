from enum import Enum

class Embrion(Enum):
    embrion_4AB = "4AB"
    embrion_5AA = "5AA"
    embrion_3BB = "3BB"

class Patient:
    def __init__(self, id, age, name, embrions):
        self.id = id
        self.age = age
        self.name = name
        self.embrions = embrions

class PatientsManager:
    patients = [
        Patient(0, 26, "Lasha", [Embrion.embrion_4AB, Embrion.embrion_3BB]),
        Patient(1, 37, "Artur", [Embrion.embrion_4AB]),
        Patient(2, 36, "Nikita", []),
        Patient(3, 41, "Max", []),
        Patient(4, 46, "Incognito", [])
    ]

    def add_patient(self, patient):
        self.patients.append(patient)

    def fetchPatients(self, filter):
        filteredPatients = []
        for patient in self.patients:
            if filter(patient):
                filteredPatients.append(patient)
        return filteredPatients

# id,age,name,embrion1, embrion2
# 0,20,Lashs,4AB,5AA
#def fetch_patients_from_db():
    # Загрузка CSV файла
    # На этой строчке у тебя будет CSV файл
    # Парсишь(parse) CSV
    # Тут уже будет лист пациентов типа patients на строчке 17

patientsManager = PatientsManager()
filteredPatients = patientsManager.fetchPatients(
    lambda patient:
        Embrion.embrion_4AB in patient.embrions and
        20 < patient.age < 35
)
patients_string = ''
for patient in filteredPatients:
    patients_string += '\n' + patient.name + ', age: ' + str(patient.age)

print('Filtered patients:', patients_string)

embrions = [Embrion.embrion_4AB, Embrion.embrion_3BB]
embrion = Embrion.embrion_4AB

match embrion:
    case Embrion.embrion_4AB:
        print("Это 4АБ")
    case Embrion.embrion_3BB:
        print("Это 3ББ")
    case Embrion.embrion_5AA:
        print("Это 5AA")

dfgsdfds
dfsfs


sdfsdf