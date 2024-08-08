from unittest.mock import patch

from src.utils import get_data_from_xlsx


@patch("src.utils.pd.read_excel")
def test_get_data_from_xlsx(mock_read_excel, get_df):
    """Tests normal work of get_data_from_xlsx function."""
    mock_read_excel.return_value = get_df
    assert get_data_from_xlsx("existing.xlsx").equals(get_df)
    mock_read_excel.assert_called_once_with("existing.xlsx")


def test_get_data_from_xlsx_no_such_file(get_empty_df, capsys):
    """Tests get_get_data_from_xlsx function when an Excel-file does not exist."""
    file_name = "no_such_file.xlsx"
    get_data_from_xlsx(file_name)
    captured = capsys.readouterr()
    assert captured.out == "Файл не найден. Проверьте правильность введенных данных.\n"
    assert get_data_from_xlsx(file_name).equals(get_empty_df)
