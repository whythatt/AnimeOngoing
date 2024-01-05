from datetime import datetime


def date_form(date_str):
    # Исходная строка с датой и временем
    input_date = date_str

    # Преобразование строки в объект datetime
    dt = datetime.strptime(input_date, "%Y-%m-%dT%H:%M%z")

    # Форматирование объекта datetime в желаемый формат
    output_date = dt.strftime("%b %d, %Y")

    return output_date  # Вывод: Nov 07, 2024
