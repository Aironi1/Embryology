# Испортируем нужный класс из нашей папки
from PatientDataModels.Embrion import Embrion
from pymongo import ReturnDocument

class Patient:
    def __init__(self, id: int, age: int, name: str, embrions: [Embrion]):
        self.id = id
        self.age = age
        self.name = name
        self.embrions = embrions

    @classmethod
    def init_with_mongo_document(cls, document: ReturnDocument):
        embrions_from_document = document['embrions']
        embrions = []
        for embrion in embrions_from_document:
            embrions.append(Embrion(embrion))

        return cls(
            id=document['_id'],
            age=document['age'],
            name=document['name'],
            embrions=embrions
        )