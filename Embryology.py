from GUI.GUIManager import GUIManager
from Managers.PatientsManager import PatientsManager


guiManager = GUIManager(patients_manager=PatientsManager())
guiManager.start_receiving_events_from_window()
