import gspread
from gspread import Client, Spreadsheet, service_account
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from gsheet_service.configs import load_config

config = load_config()

# Google Sheets setup
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = config.gsheet.credentials
SHEET_NAME = config.gsheet.sheet_name

# Initialize Google Sheets client
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
gc = gspread.authorize(credentials)


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename=CREDENTIALS_FILE)


def get_table_by_id(client: Client, table_url):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)


def get_table_id(client: Client, table_name: str) -> str:
    """Получение ID таблицы по ее названию."""
    return client.open(table_name).id


def get_worksheet_info(table: Spreadsheet) -> dict:
    """Возвращает количество листов в таблице и их названия."""
    worksheets = table.worksheets()
    worksheet_info = {
        "count": len(worksheets),
        "names": [worksheet.title for worksheet in worksheets],
    }
    return worksheet_info


def create_worksheet(table: Spreadsheet, title: str, rows: int, cols: int):
    """Создание листа в таблице."""
    return table.add_worksheet(title, rows, cols)


def delete_worksheet(table: Spreadsheet, title: str):
    """Удаление листа из таблицы."""
    table.del_worksheet(table.worksheet(title))


def extract_data_from_sheet(table: Spreadsheet, sheet_name: str) -> list[dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    rows = worksheet.get_all_records()
    return rows


def test():
    table_id = get_table_id(gc, SHEET_NAME)
    table = get_table_by_id(gc, table_id)
    info = get_worksheet_info(table)
    print(f"Количество листов: {info['count']}")
    print("Названия листов:")
    for name in info["names"]:
        print(name)


def get_data():
    """Тестирование извлечения данных из таблицы Google Sheets."""
    table_id = get_table_id(gc, SHEET_NAME)
    table = get_table_by_id(gc, table_id)
    data = extract_data_from_sheet(table, config.gsheet.list_name)
    res_dict = {}
    for i in data:
        for key, value in i.items():
            if value:
                res_dict.setdefault(key, []).append(value)

    message = ""
    for key, value in res_dict.items():
        message += f"{key}: {'\n '.join(value)}\n\n"
    return message


if __name__ == "__main__":
    test_data = get_data()
    logger.success(test_data)
    logger.info(len(test_data))
