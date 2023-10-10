from typing import Any
from enum import Enum
import PySimpleGUI as sg
from PatientDataModels.Patient import Patient
from GUI.ElementKey import ElementKey
from GUI.EventName import EventName


class GUIElementsFactory:
    # Private types

    class _ColumnName(Enum):
        id = "ID"
        age = "Возраст"
        name = "Имя"
        embrions = "Эмбрионы"

    class Constants(Enum):
        button_size = (5, 1)
        window_size = (750, 500)

    @classmethod
    def create_table_rows_from_patients(cls, patients: [Patient]) -> [Any]:
        return [
            [
                patient.id,
                patient.age,
                patient.name,
                ",".join([embrion.value for embrion in patient.embrions])
            ]
            for patient in patients
        ]

    @classmethod
    def _create_table_from_patients(cls, patients: [Patient]) -> sg.Table:
        return sg.Table(
            values=cls.create_table_rows_from_patients(patients),
            headings=[case.value for case in cls._ColumnName.__members__.values()],
            display_row_numbers=False,
            justification='left',
            key=ElementKey.table.value,
            selected_row_colors='red on yellow',
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True,
            num_rows=50
        )

    @classmethod
    def _create_right_column(cls):
        age_filter_label = cls._create_label('Фильтр по возрасту')

        from_label = cls._create_label("от")
        left_age_input = cls._create_input(ElementKey.age_left.value)
        from_column = sg.Column([[left_age_input], [from_label]])

        to_label = cls._create_label("до")
        right_age_input = cls._create_input(ElementKey.age_right.value)
        to_column = sg.Column([[right_age_input], [to_label]])
        apply_age_filter_button = cls._create_button('Применить фильтр', EventName.apply_age_filter.value)
        clear_age_filter_button = cls._create_button('Очистить фильтр', EventName.clear_age_filter.value)

        return [[age_filter_label], [from_column, to_column], [apply_age_filter_button], [clear_age_filter_button]]

    @classmethod
    def _create_window_layout(cls, patients: [Patient]):
        table = cls._create_table_from_patients(patients)
        age_filter_column = cls._create_right_column()

        return [
            [
                sg.Col([[table]], expand_x=True, expand_y=True),
                sg.VSeparator(),
                sg.Col(age_filter_column, element_justification='center', vertical_alignment='top')
            ]
        ]

    @classmethod
    def create_window(cls, patients: [Patient]):
        return sg.Window(
            "Эмбриология",
            cls._create_window_layout(patients),
            size=cls.Constants.window_size.value,
            resizable=True,
            finalize=True
        )

    # Helping methods

    @classmethod
    def _create_label(cls, text: str):
        return sg.Text(text)

    @classmethod
    def _create_input(cls, key: str, size: (int, int) = Constants.button_size.value):
        return sg.In(size=size, enable_events=True, key=key)

    @classmethod
    def _create_button(cls, text: str, key:str):
        return sg.Button(text, key=key)