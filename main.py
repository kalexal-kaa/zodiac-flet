from flet import View, AppBar, ElevatedButton, Page, Text, TextField, Image, DatePicker, TimePicker, FilePicker, FilePickerResultEvent, SnackBar, Column, ScrollMode, colors, icons, app
from datetime import datetime
from pathlib import Path
from kerykeion import AstrologicalSubject, KerykeionChartSVG, Report

def main(page: Page):
    page.title = "Zodiac"

    def button_clicked(e):
        if (len(name_tf.value.strip()) == 0 or len(day_tf.value.strip()) == 0 or len(year_tf.value.strip()) == 0 or
                len(hours_tf.value.strip()) == 0 or len(minutes_tf.value.strip()) == 0 or
                len(place_tf.value.strip()) == 0):
            show_snack_bar("Заполните все поля!")
            page.update()
            return

        name = name_tf.value
        day = int(day_tf.value)
        month = int(month_tf.value)
        year = int(year_tf.value)
        hours = int(hours_tf.value)
        minutes = int(minutes_tf.value)
        place = place_tf.value

        if not is_valid_date_time(day, month, year, hours, minutes):
            show_snack_bar("Введите корректные значения даты и времени рождения")
            page.update()
            return

        path = Path(path_tf.value)

        if not path.exists():
            show_snack_bar("Путь до места сохранения файла не существует")
            page.update()
            return

        subject = AstrologicalSubject(name, year, month, day, hours, minutes, place)
        chart = KerykeionChartSVG(subject, chart_type="Natal")

        if not len(path_tf.value.strip()) == 0:
            chart.set_output_directory(path)

        chart.makeSVG()

        report = Report(subject)

        t.value = report.get_full_report()

        image.src = chart.chartname

        page.go("/result")

    def change_date(e):
        day_tf.value = str(date_picker.value.day)
        month_tf.value = str(date_picker.value.month)
        year_tf.value = str(date_picker.value.year)
        page.update()

    def change_time(e):
        hours_tf.value = str(time_picker.value.hour)
        minutes_tf.value = str(time_picker.value.minute)
        page.update()

    def on_picker_result(e: FilePickerResultEvent):
        path_tf.value = e.path
        page.update()

    def show_snack_bar(msg):
        snack_bar = SnackBar(content=Text(msg), bgcolor=colors.RED)
        page.snack_bar = snack_bar
        snack_bar.open = True

    def is_valid_date_time(day, month, year, hours, minutes):
        try:
            datetime(year, month, day, hours, minutes)
            return True
        except ValueError:
            return False

    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Ввод данных"), bgcolor=colors.GREEN_100),
                    input_column
                ],
                scroll=ScrollMode.ADAPTIVE
            )
        )
        if page.route == "/result":
            page.views.append(
                View(
                    "/result",
                    [
                        AppBar(title=Text("Результат"), bgcolor=colors.BLUE_100),
                        output_column
                    ],
                    scroll=ScrollMode.ADAPTIVE
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    name_tf = TextField(label="Имя", autofocus=True)
    day_tf = TextField(label="День рождения")
    month_tf = TextField(label="Месяц рождения")
    year_tf = TextField(label="Год рождения")
    date_button = ElevatedButton(
        "Выбор даты рождения",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
    )
    hours_tf = TextField(label="Время рождения(часы)")
    minutes_tf = TextField(label="Время рождения(минуты)")
    time_button = ElevatedButton(
        "Выбор времени рождения",
        icon=icons.LOCK_CLOCK,
        on_click=lambda _: time_picker.pick_time(),
    )
    place_tf = TextField(label="Место рождения")
    path_tf = TextField(label="Место сохранения файла")
    path_button = ElevatedButton(
        "Выбор места сохранения файла",
        icon=icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.get_directory_path()
    )
    b = ElevatedButton(text="ПОКАЗАТЬ ГОРОСКОП", on_click=button_clicked)
    t = Text(size=15, selectable=True)
    image = Image(src="***", width=1000, height=600)

    input_column = Column(
        [name_tf, day_tf, month_tf, year_tf, date_button, hours_tf, minutes_tf, time_button, place_tf, path_tf,
         path_button, b])
    output_column = Column([image, t])

    date_picker = DatePicker(
        confirm_text="Подтвердить",
        cancel_text="Отмена",
        error_invalid_text="Дата вне диапазона",
        help_text="Выберите дату",
        on_change=change_date
    )

    time_picker = TimePicker(
        confirm_text="Подтвердить",
        cancel_text="Отмена",
        error_invalid_text="Время вне диапазона",
        help_text="Выберите время",
        on_change=change_time
    )

    file_picker = FilePicker(on_result=on_picker_result)

    page.overlay.append(date_picker)
    page.overlay.append(time_picker)
    page.overlay.append(file_picker)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

app(main)