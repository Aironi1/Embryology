# Испортируем нужный класс из нашей папки
from PatientDataModels.Embrion import Embrion

# Класс Patient, тут ничего нового, только что я в инициализаторе указал типы явно
class Patient:
    def __init__(self, id: int, age: int, name: str, embrions: [Embrion]):
        self.id = id
        self.age = age
        self.name = name
        self.embrions = embrions
