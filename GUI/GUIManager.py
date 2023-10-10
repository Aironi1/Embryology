import PySimpleGUI as sg
from PatientDataModels.Patient import Patient
from Managers.PatientsManager import PatientsManager
from GUI.GUIElementsFactory import GUIElementsFactory
from GUI.EventName import EventName
from GUI.ElementKey import ElementKey
from Utils.StringUtils import string_is_empty


class GUIManager:
    # Constants

    FONT = ("Arial", 14)

    patients: [Patient]
    patientsManager: PatientsManager
    patientsRows: [[int | str | list]] = []
    window: sg.Window

    def __init__(self, patients_manager: PatientsManager):
        self.patientsManager = patients_manager
        self.patients = patients_manager.fetch_patients()
        self.patientsRows = GUIElementsFactory.create_table_rows_from_patients(self.patients)
        self.__perform_gui_setup()

    # GUI Setup

    def __perform_gui_setup(self):
        sg.set_options(font=self.FONT)
        self.window = GUIElementsFactory.create_window(self.patients)

    # Managing Table Data

    def start_receiving_events_from_window(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break

            if EventName.apply_age_filter.value in event:
                self._handle_apply_age_filter_event(values)

            if EventName.clear_age_filter.value in event:
                self._handle_clear_age_filter_event()

        self.window.close()

    def _handle_apply_age_filter_event(self, values):
        left_age_string = values[ElementKey.age_left.value]
        right_age_string = values[ElementKey.age_right.value]
        if string_is_empty(left_age_string) or string_is_empty(right_age_string):
            self.window[ElementKey.table.value].update(values=self.patientsRows)
        else:
            left_age = int(left_age_string)
            right_age = int(right_age_string)
            filtered_patients = filter(lambda patient: left_age < patient.age < right_age, self.patients)
            filtered_rows = GUIElementsFactory.create_table_rows_from_patients(filtered_patients)
            self.window[ElementKey.table.value].update(values=filtered_rows)

    def _handle_clear_age_filter_event(self):
        self.window[ElementKey.table.value].update(values=self.patientsRows)
        self.window[ElementKey.age_left.value].update(value='')
        self.window[ElementKey.age_right.value].update(value='')