import pytest
from unittest.mock import patch
from src.aeroplane import Aeroplane

from src.cli import user_interface


@pytest.fixture
def mock_dependencies():
    """Фикстура для изоляции внешних классов adapter и storage."""
    with patch('src.cli.OpenSkyAdapter') as MockAdapter, \
            patch('src.cli.JSONStorage') as MockStorage:
        mock_adapter = MockAdapter.return_value
        mock_storage = MockStorage.return_value

        yield mock_adapter, mock_storage


@patch('builtins.input', side_effect=['5'])
@patch('builtins.print')
def test_user_interface_exit(mock_print, mock_input, mock_dependencies):
    """Проверка корректного выхода из программы."""
    user_interface()
    mock_print.assert_any_call("Завершение работы программы.")


@patch('builtins.input', side_effect=['1', 'Canada', '5'])
@patch('builtins.print')
def test_user_interface_fetch_and_save_success(mock_print, mock_input, mock_dependencies):
    """Успешный запрос самолетов и сохранение в базу."""
    mock_adapter, mock_storage = mock_dependencies

    mock_adapter.get_country_bounds.return_value = [45.0, 50.0, -75.0, -70.0]
    mock_adapter.get_aircraft.return_value = [
        [None, "ACA123 ", "Canada", None, None, None, None, 10000.0, None, 250.0]
    ]

    user_interface()

    mock_adapter.get_country_bounds.assert_called_with('Canada')
    mock_storage.save_aircraft.assert_called_once()

    mock_print.assert_any_call("Успешно загружено и сохранено самолетов: 1")


@patch('builtins.input', side_effect=['1', 'UnknownCountry', '5'])
@patch('builtins.print')
def test_user_interface_fetch_country_not_found(mock_print, mock_input, mock_dependencies):
    """Случай, когда координаты страны не найдены."""
    mock_adapter, _ = mock_dependencies
    mock_adapter.get_country_bounds.return_value = None

    user_interface()

    mock_print.assert_any_call("Не удалось найти страну или получить ее координаты.")


@patch('builtins.input', side_effect=['2', '2', '5'])
@patch('builtins.print')
def test_user_interface_top_n_altitude(mock_print, mock_input, mock_dependencies):
    """Получение ТОП N самолетов (проверяется сортировка sorted(reverse=True))."""
    _, mock_storage = mock_dependencies

    plane_low = Aeroplane(callsign="LOW", origin_country="US", velocity=100, geo_altitude=5000)
    plane_high = Aeroplane(callsign="HIGH", origin_country="US", velocity=100, geo_altitude=12000)

    mock_storage.get_aeroplanes.return_value = [plane_low, plane_high]

    user_interface()

    mock_print.assert_any_call(plane_high)


@patch('builtins.input', side_effect=[
    '2', 'invalid',
    '2', '0',
    '2', '1',
    '5'
])
@patch('builtins.print')
def test_user_interface_top_n_validation(mock_print, mock_input, mock_dependencies):
    """Обработка ошибок ввода N (строка, ноль, отрицательное число)."""
    _, mock_storage = mock_dependencies
    mock_storage.get_aeroplanes.return_value = []

    user_interface()

    mock_print.assert_any_call("Пожалуйста, введите корректное число.")
    mock_print.assert_any_call("Пожалуйста, введите число больше 0.")


@patch('builtins.input', side_effect=['3', 'France', '5'])
@patch('builtins.print')
def test_user_interface_filter_by_country(mock_print, mock_input, mock_dependencies):
    """Поиск самолетов по стране регистрации."""
    _, mock_storage = mock_dependencies
    plane = Aeroplane(callsign="SFR1',", origin_country="France", velocity=200, geo_altitude=9000)
    mock_storage.get_aeroplanes.return_value = [plane]

    user_interface()

    mock_storage.get_aeroplanes.assert_called_with(criteria={"origin_country": "France"})
    mock_print.assert_any_call(plane)


@patch('builtins.input', side_effect=['4', 'DLH456', '5'])
@patch('builtins.print')
def test_user_interface_delete_aircraft(mock_print, mock_input, mock_dependencies):
    """Удаление самолета по позывному."""
    _, mock_storage = mock_dependencies

    user_interface()

    mock_storage.delete_aeroplane.assert_called_with('DLH456')
    mock_print.assert_any_call("Запрос на удаление самолета DLH456 выполнен.")


@patch('builtins.input', side_effect=['9', '5'])
@patch('builtins.print')
def test_user_interface_invalid_choice(mock_print, mock_input, mock_dependencies):
    """Ввод несуществующего пункта меню."""
    user_interface()
    mock_print.assert_any_call("Неверный ввод. Пожалуйста, выберите существующий пункт меню.")
