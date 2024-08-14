import json
import os
from datetime import datetime

from src.reports import spending_by_category, write_to_file
from src.services import get_transactions_list, investment_bank
from src.utils import get_data_from_user, get_data_from_xlsx
from src.views import generate_json_response


def main():
    """Главная функция для использования приложения."""

    with open("user_settings.json") as settings_file:

        try:
            print("Добро пожаловать в SkyBank!")
            result = json.load(settings_file)

        except json.JSONDecodeError:
            print(
                """Для корректной работы приложения, пожалуйста, укажите интересующие Вас
            валюты и акции компаний S&P 500, которые будут отображаться на главное странице приложения
            при его отрытии."""
            )

            currencies = input("Введите валюты для отображения на главной странице через запятую или пробел: ")
            stocks = input(
                "Введите тикеры акций компаний S&P 500 для отображения на главной странице через запятую или пробел: "
            )

            check_input = get_data_from_user(currencies, stocks)

            while check_input:
                print(check_input)
                currencies = input("\nВведите валюты для отображения на главной странице через запятую или пробел: ")
                stocks = input(
                    "Введите тикеры акций компаний S&P 500 для отображения на главной странице "
                    "через запятую или пробел: "
                )
                check_input = get_data_from_user(currencies, stocks)

        else:
            user_input = input(
                """\nВыберите интересующий Вас пункт меню:
1. Перейти на главную
2. Посмотреть доходы по инвесткопилке
3. Выгрузить отчет по тратам определенной категории
"""
            )
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            base_path = os.path.join(os.path.dirname(__file__), "data")
            df = get_data_from_xlsx(os.path.join(base_path, "operations.xlsx"))

            if user_input == "1":
                print(generate_json_response(date))

            elif user_input == "2":

                if result.get("limit") is None:
                    print("\nВыберите лимит, до которого будут округляться траты: 10, 50 или 100.")

                    limit = int(input())

                    while limit not in [10, 50, 100]:
                        print("\nУказан неверный лимит. Выберите лимит из возможных вариантов: 10, 50, 100")
                        limit = int(input())

                    result["limit"] = limit

                    with open("user_settings.json", "w", encoding="utf-8") as settings_file:
                        json.dump(result, settings_file)

                limit = result.get("limit")
                month = input(
                    "Введите интересующий месяц в формате YYYY-MM или нажмите Enter для выбора " "текущего месяца: "
                )
                if not month:
                    month = date[:7]

                while True:
                    try:
                        datetime.strptime(month, "%Y-%m")
                        break
                    except ValueError:
                        print("Неправильный формат даты. Введите дату в формате YYYY-MM")
                        month = input()

                transactions_list = get_transactions_list(df)
                investment = investment_bank(month, transactions_list, limit)
                print(investment)

            elif user_input == "3":
                file_format = input(
                    "\nВыберите формат для выгрузки отчета (xlsx, csv, json) или нажмите Enter "
                    "для выбора формата по умолчанию (json): "
                ).lower()

                if file_format:
                    while file_format not in ["csv", "xlsx", "json"]:
                        print("\nУказан неверный формат. Выберите формат из возможных вариантов: json, csv, excel")
                        file_format = input()
                    file_name = f"report.{file_format}"

                else:
                    file_name = None

                category = input("\nВыберите интересующую категорию: ").title()
                report_date = input(
                    "\nВведите интересующую месяц в формате DD.MM.YYYY HH:MM:SS или нажмите Enter "
                    "для выбора сегодняшней даты: "
                )

                if not report_date:
                    report_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                while True:
                    try:
                        datetime.strptime(report_date, "%d.%m.%Y %H:%M:%S")
                        break
                    except ValueError:
                        print("Неправильный формат даты. Введите дату в формате DD.MM.YYYY HH:MM:SS")
                        report_date = input()

                write_to_file(file_name)(spending_by_category)(df, category, report_date)
                print(
                    f"Отчет успешно сформирован. Для просмотра перейдите в папку data/ "
                    f"и откройте report.{file_format if file_format else json}"
                )

            else:
                print("Я не знаю такой команды.")


if __name__ == "__main__":
    main()
