# Импортируем пакет для графического интерфейса
import PySimpleGUI as psg

# Испортируем нужные классы(лежат в папке)
from PatientDataModels.Patient import Patient
from Managers.PatientsManager import PatientsManager

# Класс для управления графическим интерфейсов
class GUIManager:
    # Поле класса для пациентов. Явно указан тип "list с типом элементов Patient"
    patients: [Patient]
    # Поле класса для менеджера пациентов. Явно указан тип "PatientsManager"
    patientsManager: PatientsManager
    # Поле класса для рядов с пациентами в таблице.
    # Явно указан тип "list list'ов c типом элементов "int или str или list""
    # То есть элементы этих типов могут быть в листе
    # В нашем случае id и age будут типа int, name будет типа str, а embrions будет типа list c типом элементов Embrion
    patientsRows: [[int | str | list]] = []
    # Поле класса для окна с графическим интерфейсом. Имеет тип psg.Window. Почему такой?
    # Мы импортировали библиотеку для работы с графическим интерфейсом на 2 строчке как psg для дальнейшего
    # использования в коде. Внутри psg есть тип Window. Поэтому окно у нас типа psg.Window
    window: psg.Window

    # Инициализация экземпляра класса, передаём в него PatientsManager
    def __init__(self, patients_manager: PatientsManager):
        # Присваиваем нашему полю patientsManager переданный в инициализатор patientsManager
        self.patientsManager = patients_manager
        # Присваиваем нашему полю patients результат вызова функции fetch_patients() у patients_manager
        self.patients = patients_manager.fetch_patients()
        # Создаём ряды таблицы из пациентов
        self.patientsRows = self.__createTableRowsFromPatients(self.patients)
        # Выполняем первоначальную настройку графического интерфейса
        self.__perform_gui_setup()

        # ТОП ИНФА: чтобы прыгнуть к определению какой-либо функции достаточно в месте её вызова
        # нажать ctrl + левый клик мыши

    # GUI Setup

    # Начальная конфигурация графического интерфейса
    def __perform_gui_setup(self):
        # Устанавливаем шрифт Arial с кеглем 14
        psg.set_options(font=("Arial", 14))
        # Создаём окно для нашего графического интерфейса
        self.__create_window()

    # Получение названий колонок
    def __get_top_row(self) -> [str]:
        # Возвращаем название колонок в таком формате. Если тебе нужно добавить ещё колонку,
        # то будь осторожен. В методе __createTableRowsFromPatients идёт наполнение рядов колонок
        # сейчас там передаётся 4 значения. Если появится ещё одна колонка, то придётся передавать 5 значений
        return ['ID', 'Возраст', 'Имя', 'Эмбрионы']

    # Managing Table Data

    # Создание рядов для табоицы из листа пациентов(list с типом элементов Patient)
    def __createTableRowsFromPatients(self, patients: [Patient]):
        # создаём пустой лист
        patients_rows = []
        # Итерируемся по пациентам, добавляем лист из 4-х значений(именно про него речь на строчке 51)
        # и добавляем в patients_rows list со значениями для колонок
        for patient in patients:
            patients_rows.append(
                [
                    patient.id,
                    patient.age,
                    patient.name,
                    ",".join(map(lambda embrion: embrion.value, patient.embrions))
                ]
            )
        # В конце свойству экземпляра класса patientsRows присваиваем patients_rows
        return patients_rows

    # Создание таблицы из данных пациентов
    def __create_table_from_patients(self) -> psg.Table:
        # Я взял этот код с какого-то сайта, можешь сам поразбираться и погуглить
        # Но на всякий случай я подпишу, за что отвечают поля по моему мнению(читай "почти 100%)
        # На что стоит обратить внимание: в values передаём self.patientsRows
        # Мы их устанавливали в функции __createTableRowsFromPatients
        # В headings передаём результат вызова функции __get_top_row(), она определена выше
        # И в key передаём ключ '-TABLE-'. Значение может быть любым на самом деле
        # Но дальше мы это значение будет использовать для обновления рядов в таблице
        return psg.Table(
            values=self.patientsRows, # Значения для рядов
            headings=self.__get_top_row(), # Значения для названий рядов
            display_row_numbers=False, # Показывать ли порядковые номера рядов
            justification='left', # Выравнивание текста внутри рядов
            key='-TABLE-', # Ключ элемента
            selected_row_colors='red on yellow', # Цвет выделенного ряда
            enable_events=True, # Включить ли обработку ивентов(events)
            expand_x=True, # Можно ли расширять ряды по x оси
            expand_y=True, # Можно ли расширять ряды по y оси (у меня не получилось)
            enable_click_events=True, # Включить ли обработку нажатий,
            num_rows=50
        )

    # Здесь создаём секцию графического интерфейса для возрастного фильтра
    def __create_age_column(self) -> [psg.Button | psg.Text | psg.Input]:
        age_filter_text = [psg.Text("Фильтр возраста")]
        from_column = psg.Column([[psg.In(size=(5, 1), enable_events=True, key="-AGE_LEFT-")], [psg.Text("от")]])
        to_column = psg.Column([[psg.In(size=(5, 1), enable_events=True, key="-AGE_RIGHT-")], [psg.Text("до")]])
        return [age_filter_text,[from_column,to_column],[psg.Button('Применить фильтр')]]

    # Здесь создаём вёрстку для нашего графического интерфейса
    def __create_layout(self) -> list[list]:
        # Создаём таблицу
        table = self.__create_table_from_patients()
        # Создаём секцию с возрастным фильтром
        ageColumn = self.__create_age_column()

        # Возвращаем вёрстку в таком формате
        # Говоря "В таком формате" я имею в виду, что библиотека графического интерфейса
        # ожидает от нас данные вёрстки именно в таком формате
        return [[psg.Col([[table]], expand_x=True,expand_y=True), psg.VSeparator(), psg.Col(ageColumn,justification='left',vertical_alignment='top')]]
    # ,[psg.VSeparator()], psg.Col([[table]])

    # Создаём окно
    def __create_window(self):
        # Присваем полю экземпляр класса экземляр класса psg.Windows(именно такой тип указан у нашего поля)
        self.window = psg.Window(
            "Эмбриология", # Название окна, оно отображается в самом верху
            self.__create_layout(), # Вёрстку, её создание описании в функции __create_layout
            size=(750, 500), # Размеры окна
            resizable=True, # Можно ли изменять размер окна. В данном случае True, то есть можно
            finalize=True
        )

    # Здесь мы обрабатываем события(ивенты) графического интерфейса
    # Типа нажатия, ввод данных и т.д.
    def start_receiving_events_from_window(self):
        # Запускаем бесконечный цикл, чтобы обрабатывать ивенты окна, пока мы сами его не закроем
        while True:
            # Получаем ивенты и значения от окна
            event, values = self.window.read()
            # Вот этот принт выведет в терминале какой пришёл ивент и какие события
            print("event:", event, "values:", values)
            # Если событие == закрыть окно, то выходим из цикла с помощью break
            # В таком случае исполняется самая последняя строчка в этом файле
            # Так как это единственная строчка, идущая после while, а мы его прервали только что
            if event == psg.WIN_CLOSED:
                break
            # Если событие == 'Применить фильтр', то обрабатываем фильтр. Предчуствую вопрос: откуда
            # я взял 'Применить фильтр'? Я его сам указал на 104 строке. Это ключ этого события
            if 'Применить фильтр' in event:
                # Получаем значение левого поля для ввода возраста. '-AGE_LEFT-' и '-AGE_RIGHT-' опять же я
                # сам указал в функции __create_age_column.
                left_age_string = values['-AGE_LEFT-']
                # Получаем значение правого поля для ввода возраста.
                right_age_string = values['-AGE_RIGHT-']
                # Проверяем, что значения не пустые, а если пустые то заполняем таблицу изначальными данными
                if len(left_age_string) == 0 or len(right_age_string) == 0:
                    # Заполнение таблицы данными
                    # Для этого у нашего окна по ключу '-TABLE-'(который мы сами определили, можешь выполнить поиск
                    # по файлу, чтобы посмотреть, где именно) вызываем функцию update, в которую в качестве аргумента
                    # передаём значения - изначальные ряды с пациентами
                    self.window['-TABLE-'].update(values=self.patientsRows)
                # Если значения непустые
                else:
                    # Приводим левый возраст к типу int
                    left_age = int(left_age_string)
                    # Приводим првый возраст к типу int
                    right_age = int(right_age_string)
                    # Фильтруем пациентов. Я подкорректировал наш предыдущий код, убрал передачу функции-фильтра
                    # в функция получения пациентов у менеджера пациенто, так как существует встроенная функция
                    # фильтрации. Она представлена ниже, для тебя должно быть ничего нового
                    filtered_patients = filter(lambda patient: left_age < patient.age < right_age, self.patients)
                    # Создаём ряды с отфильтрованными пациентами
                    filtered_rows = self.__createTableRowsFromPatients(filtered_patients)
                    # Обновляем данные в таблице
                    self.window['-TABLE-'].update(values=filtered_rows)
            # Если ивент == 'Очистить фильтр', то обрабатываем этот случай
            if 'Очистить фильтр' in event:
                # Обновляем данные в таблице исходными данными пациентов
                self.window['-TABLE-'].update(values=self.patientsRows)
                # Левому возрасту присваиваем пустое значение
                self.window['-AGE_LEFT-'].update(value='')
                # Правому возрасту присваиваем пустое значение
                self.window['-AGE_RIGHT-'].update(value='')
        # Если вышли из цикла while, то закрываем окно
        self.window.close()
