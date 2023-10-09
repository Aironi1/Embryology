# Испортируем нужные классы, в данном случае из файлов, лежащих в нашей папке
from GUI.GUIManager import GUIManager
from Managers.PatientsManager import PatientsManager

# Здесь создаём GUIManager, передаём в него экземпляр класса PatientsManager
# Мы могли бы экземпляр класса создать и внутри, но передавать зависимости через инициализатор - хорошая практика
# Передача зависимостей извне называется Dependency Injection
guiManager = GUIManager(patients_manager=PatientsManager())

# Начинаем получать события от графического интерфейса и обрабатывать их
# Реализация функции лежит в классе GUIManager в файле GUIManager.py
guiManager.start_receiving_events_from_window()
