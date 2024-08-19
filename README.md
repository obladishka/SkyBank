# SkyBank - приложение для анализа транзакций

SkyBank - приложение для анализа транзакций - это приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение генерирует JSON-данные для веб-страниц, формирует отчеты, а также предоставляет другие сервисы.

## Начало работы

Для запуска приложения:

1. Клонируйте репозиторий, выполнив в своем терминале команду
```commandline
git clone https://github.com/obladishka/SkyBank.git
```
2. Установите зависимости через poetry:
```commandline
poetry intall
```
3. Запустите приложение, выполнив в терминале команду
```commandline
python3 main.py # для MacOC
python main.py # для Windows
```

## Использование
Приложение предоставляет на выбор 3 функциональности:

### 1. Переход на Главную страницу
Генерирует JSON-ответ по текущей дате, содержащий приветствие, актуальные курс валют и стоимость акций компаний S&P 500, 
а также данные по каждой карте (включая номер карты, общую сумму расходов и кешбэк) и топ-5 транзакций по абсолютной
сумме платежа. 
Валюты и акции для отображения на Главной странице задаются пользователем при первом запуске приложения. 
Данные для анализа берутся за период начиная с начала месяца, на который выпадает текущая дата, по текущую дату.

Пример JSON-ответа:
```commandline
{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}
```
### 2. Просмотр доходов по Инвесткопилке
Сервис предоставляет функциональность для подсчета денег, которые можно было бы отложить на Инвесткопилку в указанном
месяце. При первом запуске пользователь устанавливает комфортный порог округления: *10*, *50* и *100* рублей, после
чего его будут округляться до указанного порога, и разница между фактической суммой трат по карте и суммой округления 
будет попадать на Инвесткопилку.

***Например***

*При настройке шага округления в 50 ₽, покупка на 1712 ₽ автоматически округлится до 1750 ₽, и 38 ₽ попадут 
в Инвесткопилку.*

Сервис возвращает JSON-ответ формата:
```commandline
{"month": "2024-08", "investment_amount": 204.5}
```
По умолчанию для анализа берется текущий месяц, при желании его можно поменять на интересующий, указав его в формате
YYYY-MM.
### 3. Подготовка и выгрузка отчетов по тратам определенной категории
Для формирования отчета берется период в 3 месяца, начиная от переданной даты (по умолчанию - текущей). Выгрузка отчетов
возможна в 3-х форматах *.json, .xlxs* и *.csv* (по умолчанию - *.json*). Отчеты сохраняются в папке *data/* 
с названием *report*.

## Тестирование
Код на 100% покрыт юнит-тестами Pytest. Для запуска выполните команды:
```commandline
poetry add --group dev pytest # установка pytest в виртуальное окружение приложения
pytest # запуск тестов
```
Подробный отчет о покрытии можно найти в файле *index.html* в папке *htmlcov*, запустив в терминале команду:
```commandline
pytest --cov=src --cov-report=html
```

## Источники
<a href="https://www.cbr-xml-daily.ru/">Курсы ЦБ РФ в XML и JSON, API</a>

[FMP - financial data API](https://site.financialmodelingprep.com/developer/docs)
