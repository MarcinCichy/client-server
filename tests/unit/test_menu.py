import unittest
from unittest.mock import MagicMock
import server_package.server_response as server_response
from server_package.menu import CommandHandler


class TestMenu(unittest.TestCase):
    def setUp(self):
        # Mock ServerUserState i inne zależności
        self.logged_in_user_data = MagicMock()
        self.command_handler = CommandHandler(self.logged_in_user_data)
        self.command_handler.sys_utils = MagicMock()

    def test_use_command_with_valid_user_command(self):
        entrance_command = {'username': 'help'}
        expected_result = server_response.USER_HELP_DICT
        expected_result_with_additional_info = {'line1': 'line', 'Commands for All': ''}
        expected_result_with_additional_info.update(expected_result)

        # Ustawienie wartości zwracanej dla mocka metody help
        self.command_handler.sys_utils.help.return_value = expected_result_with_additional_info

        result = self.command_handler.use_command(entrance_command)

        # Assert, że wynik jest zgodny z oczekiwaniami
        self.assertEqual(result, expected_result_with_additional_info)

        # Weryfikacja, że metoda help została wywołana (jeśli to konieczne, określ argumenty)
        self.command_handler.sys_utils.help.assert_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)