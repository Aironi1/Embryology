from pymongo import MongoClient
from PatientDataModels.Patient import Patient


class DatabaseManager:
    __DATABASE_NAME: str = "PatientsDataBase"
    __COLLECTION_NAME: str = "PatientsCollection"


    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.__DATABASE_NAME]
        self.collection = self.db[self.__COLLECTION_NAME]
        print(self.db)

    def get_patients(self) -> [Patient]:
        return list(map(lambda document: Patient.init_with_mongo_document(document), self.collection.find()))

    def add_patient(self, patient: Patient):
        embrions = []
        for embrion in patient.embrions:
            embrions.append(embrion.value)

        document = {
            "_id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "embrions": embrions
        }

        self.collection.insert_one(document)

    def clear_database(self):
        self.collection.delete_many({})